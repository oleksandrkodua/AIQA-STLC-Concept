"""Offline tests for xray_dc_create.py. No network: the HTTP opener is a fake. Run: python3 -m unittest -v"""
import io, json, os, sys, tempfile, unittest, urllib.error
sys.path.insert(0, os.path.dirname(__file__))
import xray_dc_create as x

PLAN = {"project": "QA", "cases": [{"summary": "Login with valid account", "labels": ["smoke"],
        "steps": [{"step": "Open login", "result": "Form shown"}, {"step": "Submit", "data": "user A", "result": "Home shown"}]}]}


class FakeResp:
    def __init__(self, status, body):
        self.status, self._b = status, body.encode()
    def read(self): return self._b
    def __enter__(self): return self
    def __exit__(self, *a): return False


class Fake:
    def __init__(self, script):
        self.script, self.calls = script, []
    def __call__(self, req, timeout=0):
        self.calls.append((req.get_method(), req.full_url, req.data, req.get_header("Authorization")))
        status, body = self.script(req)
        if status >= 400:
            raise urllib.error.HTTPError(req.full_url, status, "err", {}, io.BytesIO(body.encode()))
        return FakeResp(status, body)


class T(unittest.TestCase):
    def setUp(self):
        os.environ["JIRA_PAT"] = "dummy-test-value"
        os.environ["JIRA_BASE_URL"] = "https://jira.example.test"

    def test_validate_adds_label_and_hash_is_stable(self):
        p = x.validate(PLAN)
        self.assertIn("ai-drafted", p["cases"][0]["labels"])
        self.assertEqual(x.plan_hash(p, "jira.example.test"), x.plan_hash(x.validate(json.loads(json.dumps(PLAN))), "jira.example.test"))

    def test_validate_rejects_bad_input(self):
        bad = [dict(PLAN, project="qa lower"), dict(PLAN, cases=[]),
               dict(PLAN, cases=[{"summary": "", "steps": PLAN["cases"][0]["steps"]}]),
               dict(PLAN, cases=[{"summary": "a", "steps": []}]),
               dict(PLAN, cases=[{"summary": "a", "steps": [{"step": "s"}]}]),
               dict(PLAN, cases=[{"summary": "a\nb", "steps": PLAN["cases"][0]["steps"]}]),
               dict(PLAN, cases=[{"summary": "a", "labels": ["has space"], "steps": PLAN["cases"][0]["steps"]}])]
        for b in bad:
            with self.assertRaises(x.PlanError, msg=str(b)):
                x.validate(b)

    def test_base_url_must_be_plain_https(self):
        for u in ["http://j.test", "https://u:p@j.test", "https://j.test/?a=1", ""]:
            os.environ["JIRA_BASE_URL"] = u
            with self.assertRaises(x.PlanError):
                x.base_url()

    def test_apply_happy_path_and_header(self):
        def script(req):
            if "/search" in req.full_url: return 200, '{"issues":[]}'
            if req.get_method() == "POST": return 201, '{"key":"QA-7"}'
            return 200, "ok"
        f = Fake(script)
        r = x.apply_plan(x.validate(PLAN), x.Client("https://jira.example.test", f))
        self.assertEqual((r[0]["key"], r[0]["steps_created"], r[0]["note"]), ("QA-7", 2, "created"))
        methods = [c[0] for c in f.calls]
        self.assertEqual(methods, ["GET", "POST", "PUT", "PUT"])
        self.assertTrue(all(c[3] == "Bearer dummy-test-value" for c in f.calls))
        self.assertIn("/rest/raven/1.0/api/test/QA-7/step", f.calls[2][1])
        self.assertEqual(json.loads(f.calls[2][2]), {"step": "Open login", "data": "", "result": "Form shown"})

    def test_duplicate_is_skipped(self):
        f = Fake(lambda req: (200, '{"issues":[{"key":"QA-1","fields":{"summary":"login with valid account"}}]}'))
        r = x.apply_plan(x.validate(PLAN), x.Client("https://jira.example.test", f))
        self.assertTrue(r[0]["note"].startswith("SKIPPED"))
        self.assertEqual([c[0] for c in f.calls], ["GET"])

    def test_step_failure_stops_without_retry(self):
        def script(req):
            if "/search" in req.full_url: return 200, '{"issues":[]}'
            if req.get_method() == "POST": return 201, '{"key":"QA-8"}'
            return 500, "boom"
        f = Fake(script)
        r = x.apply_plan(x.validate(PLAN), x.Client("https://jira.example.test", f))
        self.assertEqual(r[0]["steps_created"], 0)
        self.assertTrue(r[0]["note"].startswith("FAILED at step 1"))
        self.assertEqual(len(f.calls), 3)

    def test_network_error_mid_run_still_reports_created(self):
        posts = []
        def script(req):
            if "/search" in req.full_url: return 200, '{"issues":[]}'
            if req.get_method() == "POST":
                posts.append(1)
                if len(posts) == 2: raise urllib.error.URLError("connection reset")
                return 201, '{"key":"QA-9"}'
            return 200, "ok"
        two = dict(PLAN, cases=PLAN["cases"] + [dict(PLAN["cases"][0], summary="Second case")])
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as t:
            json.dump(two, t)
        out = io.StringIO(); old = (sys.stdout, x.urllib.request.urlopen)
        sys.stdout, x.urllib.request.urlopen = out, Fake(script)
        try:
            h = x.plan_hash(x.validate(two), "jira.example.test")
            self.assertEqual(x.main([t.name, "--apply", "--plan-hash", h, "--expect-host", "jira.example.test"]), 1)
        finally:
            sys.stdout, x.urllib.request.urlopen = old; os.unlink(t.name)
        self.assertIn("QA-9 | Login with valid account | steps 2/2 | created", out.getvalue())
        self.assertIn("- | Second case | steps 0/2 | FAILED: ", out.getvalue())

    def test_main_dry_run_then_gates(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as t:
            json.dump(PLAN, t)
        out = io.StringIO(); old = sys.stdout; sys.stdout = out
        try:
            self.assertEqual(x.main([t.name]), 0)
            h = x.plan_hash(x.validate(PLAN), "jira.example.test")
            self.assertIn(h, out.getvalue())
            self.assertEqual(x.main([t.name, "--apply", "--plan-hash", "0000", "--expect-host", "jira.example.test"]), 2)
            self.assertEqual(x.main([t.name, "--apply", "--plan-hash", h, "--expect-host", "other.test"]), 2)
        finally:
            sys.stdout = old; os.unlink(t.name)

    # R3 (injection defense): links, images and mentions in text fields are listed and rejected unless --allow-links;
    # the plan hash covers the plan and the host together.
    def _plan_with(self, text, field="result"):
        steps = [{"step": "Open login", "result": "Form shown"}, {"step": "Submit", "result": "Home shown"}]
        steps[1][field] = text
        return dict(PLAN, cases=[dict(PLAN["cases"][0], steps=steps)])

    def _run_main(self, plan, *extra):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as t:
            json.dump(plan, t)
        out = io.StringIO(); old = (sys.stdout, x.urllib.request.urlopen)
        fake = Fake(lambda req: (200, '{"issues":[]}'))
        sys.stdout, x.urllib.request.urlopen = out, fake
        try:
            code = x.main([t.name, *extra])
        finally:
            sys.stdout, x.urllib.request.urlopen = old; os.unlink(t.name)
        return code, out.getvalue(), fake

    def test_find_links_kinds(self):
        for text in ["see https://evil.invalid/x", "[click](http://a.invalid)", "![img](http://a.invalid/i.png)",
                     "[text|http://a.invalid]", "!shot.png!", "[~admin] please look", "ping @admin", "go to www.evil.invalid"]:
            self.assertTrue(x.find_links(text), text)
        for text in ["Open the login page and press Submit", "Total is 10 (ten) items", "mail qa@example.test", "Wow! Done!"]:
            self.assertEqual(x.find_links(text), [], text)

    def test_content_findings_name_the_field(self):
        f = x.content_findings(x.validate(self._plan_with("open https://evil.invalid/p")))
        self.assertEqual(len(f), 1)
        self.assertIn("case 1 step 2 result", f[0])
        self.assertIn("https://evil.invalid/p", f[0])
        d = dict(PLAN, cases=[dict(PLAN["cases"][0], summary="Login [~admin]", description="see www.evil.invalid")])
        self.assertEqual(len(x.content_findings(x.validate(d))), 2)

    def test_dry_run_lists_links_and_stops(self):
        code, out, fake = self._run_main(self._plan_with("open https://evil.invalid/p"))
        self.assertEqual(code, 2)
        self.assertIn("LINKS FOUND", out)
        self.assertIn("https://evil.invalid/p", out)
        self.assertEqual(fake.calls, [])

    def test_allow_links_still_lists_them(self):
        code, out, _ = self._run_main(self._plan_with("open https://evil.invalid/p"), "--allow-links")
        self.assertEqual(code, 0)
        self.assertIn("LINKS FOUND", out)

    def test_apply_rejects_links_even_with_the_right_hash(self):
        plan = self._plan_with("open https://evil.invalid/p")
        h = x.plan_hash(x.validate(plan), "jira.example.test")
        code, out, fake = self._run_main(plan, "--apply", "--plan-hash", h, "--expect-host", "jira.example.test")
        self.assertEqual(code, 2)
        self.assertEqual(fake.calls, [])
        code, out, fake = self._run_main(plan, "--apply", "--plan-hash", h, "--expect-host", "jira.example.test", "--allow-links")
        self.assertIn(code, (0, 1))
        self.assertTrue(fake.calls)

    def test_hash_covers_the_host(self):
        p = x.validate(PLAN)
        self.assertNotEqual(x.plan_hash(p, "jira.example.test"), x.plan_hash(p, "other.example.test"))
        os.environ["JIRA_BASE_URL"] = "https://other.example.test"
        code, out, fake = self._run_main(PLAN, "--apply", "--plan-hash", x.plan_hash(p, "jira.example.test"), "--expect-host", "other.example.test")
        self.assertEqual(code, 2)
        self.assertEqual(fake.calls, [])

    def test_dry_run_needs_the_host(self):
        os.environ["JIRA_BASE_URL"] = ""
        code, out, _ = self._run_main(PLAN)
        self.assertEqual(code, 2)
        self.assertIn("JIRA_BASE_URL", out)

    def test_proxy_mode_sends_no_token(self):
        os.environ.pop("JIRA_PAT", None); os.environ["JIRA_AUTH"] = "proxy"
        try:
            f = Fake(lambda req: (200, '{"name":"someone"}'))
            c = x.Client("https://jira.example.test", f)
            self.assertEqual(x.check_connection(c), (200, " as someone"))
            self.assertIsNone(f.calls[0][3])
            self.assertEqual(f.calls[0][1], "https://jira.example.test/rest/api/2/myself")
        finally:
            os.environ.pop("JIRA_AUTH", None); os.environ["JIRA_PAT"] = "dummy-test-value"

    def test_missing_token_without_proxy_stops(self):
        os.environ.pop("JIRA_PAT", None)
        try:
            with self.assertRaises(x.PlanError):
                x.Client("https://jira.example.test", Fake(lambda r: (200, "{}")))
        finally:
            os.environ["JIRA_PAT"] = "dummy-test-value"

    def test_token_never_printed(self):
        out = io.StringIO(); old = sys.stdout; sys.stdout = out
        try:
            x.main(["/nonexistent.json"])
        finally:
            sys.stdout = old
        self.assertNotIn("dummy-test-value", out.getvalue())


if __name__ == "__main__":
    unittest.main()
