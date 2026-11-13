# Knowledge index

STATUS: DRAFT. Written by hand from the files' own headers; nothing here is a claim about quality.
Covers `docs/`, `context/`, `decisions/`, `knowledge/`. Not covered: `.claude/`, `plugins/`, `evals/`, `policy/`, `runs/`, `feedback/` (see README Map).

- Date = last commit touching the file (`git log -1`), not review date.
- Status = as stated in the file; "not stated" means the file has no status line.
- When you add or delete a file in these four folders, add or delete its row here.

| Path | Topic | Tags | Date | Status |
|---|---|---|---|---|
| `context/discovery.md` | Discovery checklist, all items open | discovery,access,unknown | 2026-10-27 | all items OPEN |
| `context/project-context.template.md` | Template for per-project context | template,context | 2026-10-23 | not stated (template) |
| `context/sources.md` | Source authority matrix | sources,authority,conflicts | 2026-10-23 | TEMPLATE, matrix UNKNOWN |
| `decisions/CONFLICTS.md` | Register of unresolved source conflicts | conflicts,register | 2026-10-23 | empty |
| `decisions/DECISIONS.md` | Decision log D-xxx | decisions,log | 2026-11-04 | per row |
| `decisions/PROPOSAL-security-rule-7-2026-10-23.md` | Rewrite of security rule 7 | security,proposal,rules | 2026-10-23 | APPROVED 2026-10-23 |
| `decisions/README.md` | How decisions are recorded | decisions,process | 2026-10-23 | not stated |
| `decisions/verification-log.md` | Verification log V-xxx, open blockers | verification,evals,log | 2026-11-04 | per row |
| `docs/AIQA-SUMMARY.md` | Two-page summary of the AI-assisted QA system | summary,concept | 2026-10-23 | not stated |
| `docs/ALIGNMENT-WITH-R-10.md` | Gap list against the ten commandments in R-10 | gaps,register,talks | 2026-10-23 | DRAFT |
| `docs/CLOUD-SESSION.md` | Working from a cloud session | cloud,session | 2026-10-27 | DRAFT v0.1 |
| `docs/CONCEPT.md` | AIQA STLC concept | concept,stlc | 2026-10-23 | DRAFT v0.1 |
| `docs/DISTRIBUTION-OPTIONS.md` | Two ways the package reaches other QAs | distribution,plugin | 2026-10-23 | DRAFT |
| `docs/GETTING-STARTED.md` | Getting started and handing over | onboarding,handoff | 2026-10-27 | DRAFT v0.1 |
| `docs/HANDOFF-cloud.md` | Cloud handoff | cloud,handoff | 2026-10-27 | DRAFT |
| `docs/MODEL-AND-EFFORT.md` | Model and effort per skill (proposal table) | models,effort,skills | 2026-10-23 | proposal, not in any SKILL.md |
| `docs/TEST-DESIGN-TECHNIQUES.md` | Catalogue of test design techniques (unverified) and task: adaptive technique choice in create-test-cases | test-design,techniques,create-test-cases,codex | 2026-11-12 | DRAFT, not approved |
| `docs/PLAN-next-steps.md` | Next-steps plan: tasks A-F, hard rules, open items | plan,next-steps,codex,ci,evals | 2026-11-10 | DRAFT, not approved |
| `docs/PLAYWRIGHT-SETUP.md` | Playwright setup and daily use | playwright,web,setup | 2026-10-23 | not stated |
| `docs/REQUIRED-ACCESS-AND-ENVIRONMENT.md` | Required access and environment for the qabase plugin | access,environment,onboarding | 2026-10-27 | DRAFT v0.1 |
| `docs/TOKEN-TALLY-DESIGN.md` | Token counting per skill session | tokens,cost,design | 2026-10-23 | not stated |
| `docs/TRIAL-RUN-PLAN.md` | Trial run plan | trial,plan | 2026-10-23 | not stated |
| `docs/research/2026-10-23-injection-defense/report.md` | Prompt-injection defense report | security,injection,research | 2026-10-23 | not stated |
| `docs/research/2026-10-23-injection-defense/notes/anthropic.md` | Anthropic guidance on prompt injection | security,injection,vendor | 2026-10-23 | not stated |
| `docs/research/2026-10-23-injection-defense/notes/design_patterns.md` | Design patterns against prompt injection | security,injection,patterns | 2026-10-23 | not stated |
| `docs/research/2026-10-23-injection-defense/notes/incidents_threat_model.md` | Injection incidents and threat model | security,injection,threats | 2026-10-23 | not stated |
| `docs/research/2026-10-23-injection-defense/notes/openai.md` | OpenAI guidance on injection defense | security,injection,vendor | 2026-10-23 | not stated |
| `docs/research/2026-10-23-injection-defense/notes/standards.md` | Standards and frameworks on injection | security,injection,standards | 2026-10-23 | not stated |
| `docs/schemes/01-architecture.md` | Architecture, layers and owners | scheme,architecture | 2026-10-23 | DRAFT |
| `docs/schemes/02-workflow.md` | Workflow with gates | scheme,workflow | 2026-10-23 | DRAFT |
| `docs/schemes/03-enforcement.md` | Enforcement, what stops a bad action | scheme,hooks,permissions | 2026-10-23 | DRAFT |
| `docs/schemes/04-automation-ci.md` | Automation projects and CI | scheme,automation,ci | 2026-10-23 | DRAFT |
| `docs/schemes/05-rollout.md` | Rollout phases and exit checks | scheme,rollout | 2026-10-23 | DRAFT |
| `docs/schemes/06-mobile-run.md` | Mobile run preconditions and reporting | scheme,mobile | 2026-10-23 | DRAFT |
| `docs/schemes/07-base-and-variants.md` | Reusable base and variants | scheme,base | 2026-10-23 | WORKING DRAFT |
| `docs/schemes/08-mvp-chain.md` | MVP chain: humans, Claude, deterministic steps | scheme,mvp | 2026-10-23 | WORKING DRAFT |
| `docs/schemes/09-mvp-implementation-plan.md` | MVP implementation plan, five stages | scheme,mvp,plan | 2026-10-23 | WORKING DRAFT |
| `docs/schemes/10-tooling-and-roles.md` | Tooling and team roles | scheme,roles,tools | 2026-10-23 | WORKING DRAFT |
| `docs/schemes/11-sdlc-full.md` | Full SDLC, ten stages mapped to skills | scheme,sdlc,skills | 2026-10-23 | WORKING DRAFT |
| `docs/specs/2026-10-13-feedback-loop-design.md` | Feedback and improvement loop design | feedback,design,skills | 2026-10-23 | first build done, see file |
| `docs/specs/2026-10-13-skills-navigator-design.md` | Skills navigator design | navigator,skills,design | 2026-10-23 | DRAFT |
| `docs/specs/skills-navigator-draft-sectors.md` | Navigator sectors and intents | navigator,skills | 2026-10-23 | DRAFT |
| `docs/superpowers/specs/2026-10-23-aiqa-sdlc-concept-design.md` | Concept page and Demo Shop examples design | concept,examples,design | 2026-10-23 | DRAFT v0.1 |
| `docs/superpowers/specs/2026-10-23-injection-defense-design.md` | Injection defense execution plan | security,injection,plan | 2026-10-27 | DRAFT v0.1 |
| `knowledge/INTAKE.md` | Intake process for outside material | intake,process,sources | 2026-10-23 | DRAFT process |
| `knowledge/register.md` | Register of outside material R-xx | register,sources,talks,articles | 2026-11-04 | per entry |
