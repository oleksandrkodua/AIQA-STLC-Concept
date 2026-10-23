# Intake Questions

Use `AskUserQuestion` with all questions in a single call. Maximum 4 questions per call.

---

## Question 1 — Target URL

**question**: "What is the URL of the app you want to test? (e.g. https://myapp.com or http://localhost:3000)"
**header**: "URL"
**multiSelect**: false
**options**:
- label: "http://localhost:3000", description: "Local dev server on port 3000"
- label: "http://localhost:8080", description: "Local dev server on port 8080"
- label: "Staging environment", description: "Your staging URL — type it in Other"
- label: "Production URL", description: "Your live production URL — type it in Other"

> Note: If `$ARGUMENTS` already contains a URL, skip this question.

---

## Question 2 — Flows to Test

**question**: "Which pages or user flows do you want to test? Select all that apply."
**header**: "Flows"
**multiSelect**: true
**options**:
- label: "Home / Landing page", description: "Load and verify the homepage"
- label: "Authentication (login/signup)", description: "Login, signup, logout, and session flows"
- label: "Core user flow", description: "The main action a user comes to do (checkout, dashboard, form submission, etc.)"
- label: "Navigation & links", description: "All nav links, breadcrumbs, and internal links resolve correctly"

> The user will select options and/or type custom flows in "Other".
> After receiving the answer, expand each selection into concrete test steps.

---

## Question 3 — Authentication

**question**: "Does the app require login to test? If yes, provide credentials in the format: username::password"
**header**: "Auth"
**multiSelect**: false
**options**:
- label: "No auth needed", description: "The pages under test are publicly accessible"
- label: "Use test credentials", description: "Type your test credentials in Other as: email::password"
- label: "Skip auth steps", description: "Skip any flows that require login"

> If the user selects "Use test credentials" and types credentials, extract them.
> NEVER write credentials to any file. Pass only as subagent prompt variables.

---

## Question 4 — Final Action

**question**: "What should happen after the audit completes?"
**header**: "Final Action"
**multiSelect**: false
**options**:
- label: "Save report to file (Recommended)", description: "Write TEST_REPORT.md to the test-results directory"
- label: "Send via email", description: "Draft and send the report to your email using Gmail MCP"
- label: "Post to Slack", description: "Post a summary to a Slack channel using Slack MCP"
- label: "Show inline only", description: "Print the report in this conversation, no file saved"
