# 04 Automation projects and CI

STATUS: DRAFT. CI tool UNKNOWN until Discovery.
Projects are NOT PORTED yet.

```mermaid
flowchart LR
  subgraph repo[Repository]
    W[automation/web - package.json, tsconfig, config, data]
    MA[automation/mobile/android - WDIO + Appium]
    MI[automation/mobile/ios - scaffold]
    HLP[automation/mobile/helpers - shared]
  end
  MA --- HLP
  MI --- HLP
  subgraph ci[CI jobs - one per project, working directory set]
    J1[web-smoke: type-check, run on DEV]
    J2[android-regression: build identity, env check, run]
    J3[ios: not enabled]
  end
  W --> J1
  MA --> J2
  MI -.-> J3
  J1 & J2 --> R[(Reports + evidence artifacts)]
  R --> HUM{Human reads failures}
```

Rules shown: each project self-contained; CI needs no AI to run; the mobile job fails if the
environment check is missing; the iOS job is off until its check passes (record it in `decisions/verification-log.md`); evidence artifacts may
contain client data and follow `ai-usage-policy.md` item 12.
