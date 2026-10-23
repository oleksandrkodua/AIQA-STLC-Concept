# Autonomy ladder and risk tiers

Autonomy maturity, lowest to highest:

GUIDED → ASSISTED → SEMI-AUTONOMOUS → CONTROLLED AUTONOMOUS

Do not start at the top. Principle: an agent observes and recommends before it acts.

Risk-based action model. As consequence and persistence increase, stronger controls are required:

READ → ANALYZE → RECOMMEND → PREPARE → EXECUTE → MODIFY

Risk tiers (define them for the project during Discovery; this is the target model):

| Tier | Examples |
|---|---|
| LOW | analysis, classification, recommendations |
| MEDIUM | preparation, non-critical artifact changes, reviewed automation changes |
| HIGH | write actions, external system changes, shared artifact changes, security-sensitive actions |
| CRITICAL | production mutations, privilege changes, governance changes, irreversible actions |

CRITICAL and prohibited actions are never autonomous.
