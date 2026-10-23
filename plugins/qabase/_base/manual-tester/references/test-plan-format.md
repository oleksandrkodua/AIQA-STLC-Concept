# Test Plan Format

Test plans are written to `$RESULTS_DIR/TEST_PLAN.md`.

---

## File Header

```markdown
# Test Plan
**URL**: <url>
**Date**: <ISO date>
**Flows**: <comma-separated list of selected flows>
**Auth Required**: Yes / No
**Generated**: <ISO timestamp>

---

| Step | Description | Expected Outcome | Depends On |
|------|-------------|-----------------|------------|
```

---

## Row Format

Each step is one row:

```
| N | <imperative action sentence> | <observable success criterion> | <step N or —> |
```

**Rules:**
- Step numbers are sequential integers starting at 1
- Description is an imperative sentence: "Click the Submit button", "Fill the email field with test@example.com"
- Expected outcome is observable: "Form submits and success banner appears", NOT "it works"
- Depends On is the step number this step requires to have PASSed, or `—` if independent

---

## Step Generation Guide

### For each selected flow, generate these step types:

**Navigation step**
```
| N | Navigate to <URL or path> | Page loads, title is "<expected title>", no 404/500 error | — |
```

**Element presence step**
```
| N | Verify <element> is visible on the page | <element> is present and readable | N-1 |
```

**Interaction step**
```
| N | Click / fill / select <element> with <value if applicable> | <observable state change> | N-1 |
```

**State verification step**
```
| N | Verify <expected state after action> | <exact observable criterion> | N-1 |
```

**Auth steps (prepend to all auth-required flows)**
```
| 1 | Navigate to <URL> | Page loads without error | — |
| 2 | Fill email field with <username> | Email field shows the entered value | 1 |
| 3 | Fill password field with credentials | Password field is filled | 2 |
| 4 | Click the login/submit button | Page redirects to authenticated area | 3 |
| 5 | Verify authenticated state | User name or dashboard element is visible | 4 |
```

---

## Example Plan

```markdown
| Step | Description | Expected Outcome | Depends On |
|------|-------------|-----------------|------------|
| 1 | Navigate to https://myapp.com | Homepage loads, title is "MyApp", HTTP 200 | — |
| 2 | Verify navigation bar is visible | Nav contains: Home, Features, Pricing, Login | 1 |
| 3 | Click the "Login" link in the navigation | Login page loads at /login | 2 |
| 4 | Fill email field with test@example.com | Email field shows test@example.com | 3 |
| 5 | Fill password field with test credentials | Password field is filled (masked) | 4 |
| 6 | Click the "Sign In" button | Redirect to /dashboard, user name visible | 5 |
| 7 | Verify dashboard page content | Dashboard heading visible, no error messages | 6 |
| 8 | Click the account menu or logout button | Logout option is visible | 7 |
| 9 | Click Logout | Redirect to / or /login, session cleared | 8 |
```
