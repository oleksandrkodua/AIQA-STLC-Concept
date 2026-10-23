# Xray Server / Data Center calls used by this skill

STATUS: DRAFT, read from documentation 2026-10-23, not run on an instance.

| Step | Call | Source | Label |
|---|---|---|---|
| Check connection | `GET /rest/api/2/myself` (read-only) | Jira DC REST API | standard Jira call, not re-read |
| Authenticate | `Authorization: Bearer <personal access token>` on Jira DC REST calls | Atlassian developer docs and community answer on PAT use | EVIDENCE-SUPPORTED INFERENCE (docs describe PAT for Jira REST; use on `/rest/raven/` paths is not stated) |
| Duplicate check | `GET /rest/api/2/search?jql=...` | Jira DC REST API | standard Jira call, not re-read |
| Create Test | `POST /rest/api/2/issue`, `fields.issuetype.name = Test` | Xray docs: tests are created with Jira's native REST API "taking into account Xray custom fields" | CLAIM (Xray docs); type name `Test` ASSUMPTION |
| Create step | `PUT /rest/raven/1.0/api/test/{testKey}/step`, body `{step, data, result, attachments?}` | Xray Server + DC docs, "Test Steps - REST" | VERIFIED FACT (page read); the page does not say whether the test must be Manual |
| Other | REST v1.0 pages are marked deprecated in places; v2.0 mirrors v1.0 paths | Xray docs | CLAIM; replace `1.0` with `2.0` only after checking on the instance |

Not used on purpose: importing tests through "Import Execution Results" (it creates tests as a side effect of a run).
Xray Cloud uses a different API (client id and secret, tokens from an authenticate call). This skill does not cover it.
