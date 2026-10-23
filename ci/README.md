# CI

STATUS: UNKNOWN. The CI tool, runners and secret store are not confirmed (Discovery item 6).
Do not write pipeline files before that. Requirements already known:

- one job per automation project; `working-directory` set to the project;
- DEV only; credentials from the CI secret store, never from the repository;
- the mobile job fails when the environment check or build fingerprint is missing;
- jobs run without any AI service; Claude may read results afterwards for failure analysis;
- evidence artifacts follow `policy/ai-usage-policy.md` item 12;
- job names and artifacts documented in `docs/schemes/04-automation-ci.md`.
