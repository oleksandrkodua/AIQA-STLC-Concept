#!/usr/bin/env python3
"""Create approved test cases in Xray Server / Data Center. DRAFT, NOT RUN against a real instance.

Default is a dry run: validates the plan, prints it and a plan hash, sends nothing. The hash covers the
plan and the Jira host, so the dry run needs JIRA_BASE_URL. URLs, links, images and mentions in the text
fields are listed (LINKS FOUND) and stop the run unless --allow-links is given.
--apply sends requests and needs --plan-hash (from the dry run) and --expect-host.

Credentials: JIRA_BASE_URL and JIRA_PAT are read from the environment only. They are never
printed, never accepted as arguments, never written to a file. Standard library only.
Cloud sessions: set JIRA_AUTH=proxy and store the token as a network secret on the cloud
environment (Bearer, Authorization header, the Jira host). The script then sends no token; the
environment's proxy attaches it, so the token never exists inside the session. JIRA_PAT is not read.
--check sends one read-only GET /rest/api/2/myself and prints the HTTP status: use it to test
the connection and the token before a real run.

Calls (Jira DC native REST, then Xray DC REST v1.0):
  GET  {base}/rest/api/2/search?jql=...                 exact-summary duplicate check
  POST {base}/rest/api/2/issue                          create the Test issue
  PUT  {base}/rest/raven/1.0/api/test/{KEY}/step        create one manual step (fields step, data, result)
"""
import argparse, hashlib, json, os, re, sys
import urllib.error, urllib.parse, urllib.request

MAX_CASES = 50
MAX_STEPS = 40
PROJECT_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,19}$")
KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]+-[0-9]+$")
LABEL_RE = re.compile(r"^[A-Za-z0-9_.-]{1,50}$")
CTRL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
# Text that can carry data out or pull a person in: URLs, Markdown and wiki links/images, mentions.
LINK_PATTERNS = (
    ("url", re.compile(r"(?i)\b(?:https?|ftp|file|data|javascript)://|\bwww\.|\bdata:[a-z]+/[a-z]")),
    ("markdown link", re.compile(r"!?\[[^\]\n]*\]\([^)\n]*\)")),
    ("wiki link", re.compile(r"\[[^\]\n|]*\|[^\]\n]+\]")),
    ("wiki image", re.compile(r"(?<![\w!])![^\s!|]+\.(?:png|jpe?g|gif|svg|webp)(?:\|[^!\n]*)?!", re.I)),
    ("mention", re.compile(r"\[~[^\]\n]+\]|(?<![\w.])@[A-Za-z][\w.-]*")),
)


class PlanError(Exception):
    pass


def clean(text, field, limit, required=True):
    if text is None:
        text = ""
    if not isinstance(text, str):
        raise PlanError("%s must be a string" % field)
    if CTRL_RE.search(text):
        raise PlanError("%s contains control characters" % field)
    text = text.strip()
    if required and not text:
        raise PlanError("%s is empty" % field)
    if len(text) > limit:
        raise PlanError("%s is longer than %d characters" % (field, limit))
    return text


def validate(plan):
    """Return a normalised plan or raise PlanError. Content is data: only shape is checked."""
    if not isinstance(plan, dict):
        raise PlanError("plan must be a JSON object")
    project = plan.get("project")
    if not isinstance(project, str) or not PROJECT_RE.match(project):
        raise PlanError("project must be a Jira project key such as QA")
    issue_type = clean(plan.get("issue_type", "Test"), "issue_type", 40)
    cases = plan.get("cases")
    if not isinstance(cases, list) or not cases:
        raise PlanError("cases must be a non-empty list")
    if len(cases) > MAX_CASES:
        raise PlanError("at most %d cases per run" % MAX_CASES)
    out = []
    for i, c in enumerate(cases, 1):
        where = "case %d" % i
        if not isinstance(c, dict):
            raise PlanError("%s must be an object" % where)
        summary = clean(c.get("summary"), where + " summary", 255)
        if "\n" in summary:
            raise PlanError(where + " summary must be one line")
        labels = c.get("labels", [])
        if not isinstance(labels, list) or any(not isinstance(x, str) or not LABEL_RE.match(x) for x in labels):
            raise PlanError(where + " labels must be words without spaces")
        if "ai-drafted" not in labels:
            labels = labels + ["ai-drafted"]
        steps = c.get("steps")
        if not isinstance(steps, list) or not steps:
            raise PlanError(where + " needs at least one step")
        if len(steps) > MAX_STEPS:
            raise PlanError(where + " has more than %d steps" % MAX_STEPS)
        norm_steps = []
        for j, s in enumerate(steps, 1):
            sw = "%s step %d" % (where, j)
            if not isinstance(s, dict):
                raise PlanError(sw + " must be an object")
            norm_steps.append({
                "step": clean(s.get("step"), sw + " step", 4000),
                "data": clean(s.get("data", ""), sw + " data", 4000, required=False),
                "result": clean(s.get("result"), sw + " result", 4000),
            })
        out.append({
            "summary": summary,
            "description": clean(c.get("description", ""), where + " description", 8000, required=False),
            "labels": labels,
            "steps": norm_steps,
        })
    return {"project": project, "issue_type": issue_type, "cases": out}


def find_links(text):
    """Return [(kind, snippet)] for every URL, link, image or mention in the text."""
    found = []
    for kind, rx in LINK_PATTERNS:
        for m in rx.finditer(text):
            found.append((kind, text[m.start():m.start() + 60]))
    return found


def content_findings(plan):
    """One line per link, image or mention in a normalised plan, naming the field it sits in."""
    out = []
    for i, c in enumerate(plan["cases"], 1):
        fields = [("case %d summary" % i, c["summary"]), ("case %d description" % i, c["description"])]
        for j, s in enumerate(c["steps"], 1):
            fields += [("case %d step %d %s" % (i, j, k), s[k]) for k in ("step", "data", "result")]
        for where, text in fields:
            out += ["%s: %s '%s'" % (where, kind, snip) for kind, snip in find_links(text)]
    return out


def plan_hash(plan, host):
    """Hash of the plan and the host together: a plan previewed for one host cannot be applied to another."""
    blob = json.dumps({"host": host, "plan": plan}, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:16]


def base_url():
    base = os.environ.get("JIRA_BASE_URL", "").strip().rstrip("/")
    if not base:
        raise PlanError("JIRA_BASE_URL is not set")
    p = urllib.parse.urlparse(base)
    if p.scheme != "https" or not p.hostname or p.username or p.password or p.query or p.fragment:
        raise PlanError("JIRA_BASE_URL must be a plain https URL")
    return base, p.hostname


class Client:
    """Thin REST client. The token is read from the environment and used only in the header."""

    def __init__(self, base, opener=None):
        self.proxy_auth = os.environ.get("JIRA_AUTH", "").strip().lower() == "proxy"
        token = "" if self.proxy_auth else os.environ.get("JIRA_PAT", "")
        if not token and not self.proxy_auth:
            raise PlanError("JIRA_PAT is not set (or set JIRA_AUTH=proxy when a network secret supplies the token)")
        self.base = base
        self._token = token
        self._open = opener or urllib.request.urlopen

    def call(self, method, path, body=None):
        data = None if body is None else json.dumps(body).encode("utf-8")
        req = urllib.request.Request(self.base + path, data=data, method=method)
        if not self.proxy_auth:
            req.add_header("Authorization", "Bearer " + self._token)
        req.add_header("Accept", "application/json")
        if data is not None:
            req.add_header("Content-Type", "application/json")
        try:
            with self._open(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", "replace")
                return resp.status, raw
        except urllib.error.HTTPError as e:
            # status and a short body only; the request (with the header) is never printed
            return e.code, e.read().decode("utf-8", "replace")[:300]


def jql_quote(text):
    return '"' + text.replace("\\", "\\\\").replace('"', '\\"') + '"'


def find_duplicate(client, project, issue_type, summary):
    jql = "project = %s AND issuetype = %s AND summary ~ %s" % (project, jql_quote(issue_type), jql_quote(summary))
    q = urllib.parse.urlencode({"jql": jql, "fields": "summary", "maxResults": 20})
    status, raw = client.call("GET", "/rest/api/2/search?" + q)
    if status != 200:
        raise PlanError("duplicate check failed: HTTP %d" % status)
    for issue in json.loads(raw).get("issues", []):
        if issue.get("fields", {}).get("summary", "").strip().lower() == summary.lower():
            return issue.get("key")
    return None


def check_connection(client):
    """One read-only call. Prints status only; never the token."""
    status, raw = client.call("GET", "/rest/api/2/myself")
    who = ""
    if status == 200:
        try:
            who = " as %s" % json.loads(raw).get("name", "?")
        except ValueError:
            who = ""
    return status, who


def apply_plan(plan, client, allow_duplicates=False, results=None):
    """Create cases one by one. Stops at the first failure; never retries, never deletes.
    Rows go into `results` as they are made, so the caller still has them if a call raises."""
    results = [] if results is None else results
    for c in plan["cases"]:
        row = {"summary": c["summary"], "key": None, "steps_created": 0, "steps_total": len(c["steps"]), "note": ""}
        results.append(row)
        dup = None if allow_duplicates else find_duplicate(client, plan["project"], plan["issue_type"], c["summary"])
        if dup:
            row["note"] = "SKIPPED: exact summary already exists as %s" % dup
            continue
        fields = {
            "project": {"key": plan["project"]},
            "issuetype": {"name": plan["issue_type"]},
            "summary": c["summary"],
            "labels": c["labels"],
        }
        if c["description"]:
            fields["description"] = c["description"]
        status, raw = client.call("POST", "/rest/api/2/issue", {"fields": fields})
        if status not in (200, 201):
            row["note"] = "FAILED to create issue: HTTP %d %s" % (status, raw[:200])
            break
        key = json.loads(raw).get("key", "")
        if not KEY_RE.match(key):
            row["note"] = "FAILED: unexpected response, no issue key"
            break
        row["key"] = key
        for s in c["steps"]:
            status, raw = client.call("PUT", "/rest/raven/1.0/api/test/%s/step" % key, s)
            if status != 200:
                row["note"] = "FAILED at step %d: HTTP %d %s" % (row["steps_created"] + 1, status, raw[:200])
                return results
            row["steps_created"] += 1
        row["note"] = "created"
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("plan_file", nargs="?", help="JSON file: project, issue_type (optional), cases[summary, description, labels, steps[step, data, result]]")
    ap.add_argument("--check", action="store_true", help="read-only connection and token test (GET /rest/api/2/myself), no plan needed")
    ap.add_argument("--apply", action="store_true", help="send requests (default: dry run)")
    ap.add_argument("--plan-hash", help="hash printed by the dry run; required with --apply")
    ap.add_argument("--expect-host", help="Jira host the human confirmed; required with --apply")
    ap.add_argument("--allow-links", action="store_true", help="accept URLs, links, images and mentions found in the text fields (they are still listed)")
    ap.add_argument("--allow-duplicates", action="store_true", help="skip the exact-summary duplicate check")
    args = ap.parse_args(argv)
    try:
        if args.check:
            base, host = base_url()
            status, who = check_connection(Client(base))
            print("CHECK %s: HTTP %d%s" % (host, status, who))
            return 0 if status == 200 else 1
        if not args.plan_file:
            raise PlanError("plan_file is required unless --check is used")
        with open(args.plan_file, encoding="utf-8") as f:
            plan = validate(json.load(f))
        base, host = base_url()
        h = plan_hash(plan, host)
        findings = content_findings(plan)
        if findings:
            print("LINKS FOUND (%d): URLs, links, images or mentions in the text fields" % len(findings))
            for line in findings:
                print("  " + line)
        if findings and not args.allow_links:
            raise PlanError("remove them from the plan, or run again with --allow-links after a person has read each one")
        if not args.apply:
            print("DRY RUN: nothing sent")
            print("project: %s   issue type: %s   cases: %d" % (plan["project"], plan["issue_type"], len(plan["cases"])))
            for i, c in enumerate(plan["cases"], 1):
                print("%2d. %s  [%d steps]  labels: %s" % (i, c["summary"], len(c["steps"]), ", ".join(c["labels"])))
            print("plan-hash: %s" % h)
            return 0
        if args.plan_hash != h:
            raise PlanError("plan hash does not match the previewed plan (expected %s); run the dry run again" % h)
        if args.expect_host != host:
            raise PlanError("host %s was not confirmed with --expect-host" % host)
        results = []
        try:
            apply_plan(plan, Client(base), args.allow_duplicates, results)
        except (PlanError, OSError, ValueError) as e:
            if not results:
                raise
            # a network error or an unreadable response mid-run: still print what was already created
            results[-1]["note"] = "FAILED: %s" % e
        for r in results:
            print("%s | %s | steps %d/%d | %s" % (r["key"] or "-", r["summary"], r["steps_created"], r["steps_total"], r["note"]))
        return 0 if all(r["note"] in ("created",) or r["note"].startswith("SKIPPED") for r in results) and len(results) == len(plan["cases"]) else 1
    except (PlanError, OSError, ValueError) as e:
        print("STOP: %s" % e)
        return 2


if __name__ == "__main__":
    sys.exit(main())
