#!/bin/bash

# Manual Test Case Generator
# Interactive workflow for creating comprehensive test cases

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║       Manual Test Case Generator                 ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════╝${NC}"
echo ""

# Helper functions
prompt_input() {
    local prompt_text="$1"
    local var_name="$2"
    local required="$3"
    
    while true; do
        echo -e "${CYAN}${prompt_text}${NC}"
        read -r input
        
        if [ -n "$input" ]; then
            printf -v "$var_name" '%s' "$input"
            break
        elif [ "$required" != "true" ]; then
            printf -v "$var_name" '%s' ""
            break
        else
            echo -e "${RED}This field is required.${NC}"
        fi
    done
}

# Step 1: Basic Info
echo -e "${MAGENTA}━━━ Step 1: Test Case Basics ━━━${NC}"
echo ""

prompt_input "Test Case ID (e.g., TC-LOGIN-001):" TC_ID true
prompt_input "Test Case Title:" TC_TITLE true
prompt_input "Ticket key this covers (e.g. PROJ-123, blank if none):" JIRA_TASK false

echo ""
echo "Priority:"
echo "1) P0 - Critical (blocks release)"
echo "2) P1 - High (important features)"
echo "3) P2 - Medium (nice to have)"
echo "4) P3 - Low (minor issues)"
echo ""

prompt_input "Select priority (1-4):" PRIORITY_NUM true

case $PRIORITY_NUM in
    1) PRIORITY="P0 (Critical)" ;;
    2) PRIORITY="P1 (High)" ;;
    3) PRIORITY="P2 (Medium)" ;;
    4) PRIORITY="P3 (Low)" ;;
    *) PRIORITY="P2 (Medium)" ;;
esac

echo ""
echo "Test Type:"
echo "1) Functional"
echo "2) UI/Visual"
echo "3) Integration"
echo "4) Regression"
echo "5) Performance"
echo "6) Security"
echo ""

prompt_input "Select test type (1-6):" TYPE_NUM true

case $TYPE_NUM in
    1) TEST_TYPE="Functional" ;;
    2) TEST_TYPE="UI/Visual" ;;
    3) TEST_TYPE="Integration" ;;
    4) TEST_TYPE="Regression" ;;
    5) TEST_TYPE="Performance" ;;
    6) TEST_TYPE="Security" ;;
    *) TEST_TYPE="Functional" ;;
esac

prompt_input "Estimated test time (minutes):" EST_TIME false

# Step 2: Objective and Description
echo ""
echo -e "${MAGENTA}━━━ Step 2: Test Objective ━━━${NC}"
echo ""

prompt_input "What are you testing? (objective):" OBJECTIVE true
prompt_input "Why is this test important?" WHY_IMPORTANT false

# Step 3: Preconditions
echo ""
echo -e "${MAGENTA}━━━ Step 3: Preconditions ━━━${NC}"
echo ""

echo "Enter preconditions (one per line, press Enter twice when done):"
PRECONDITIONS=""
while true; do
    read -r line
    if [ -z "$line" ]; then
        break
    fi
    PRECONDITIONS="${PRECONDITIONS}- ${line}\n"
done

# Step 4: Test Steps
echo ""
echo -e "${MAGENTA}━━━ Step 4: Test Steps ━━━${NC}"
echo ""

echo "Enter test steps (format: action | expected result)"
echo "Type 'done' when finished"
echo ""

TEST_STEPS=""
STEP_NUM=1
# Parallel arrays: the markdown string above is for people, these are for the JSON contract
# (test_cases/<KEY>.json). Keeping both from one pass is what stops the two drifting apart.
STEP_ACTIONS=()
STEP_EXPECTED=()

while true; do
    echo -e "${YELLOW}Step $STEP_NUM:${NC}"
    prompt_input "Action:" ACTION false
    
    if [ "$ACTION" = "done" ] || [ -z "$ACTION" ]; then
        break
    fi
    
    prompt_input "Expected result:" EXPECTED true
    
    TEST_STEPS="${TEST_STEPS}${STEP_NUM}. ${ACTION}\n   **Expected:** ${EXPECTED}\n\n"
    STEP_ACTIONS+=("$ACTION")
    STEP_EXPECTED+=("$EXPECTED")
    ((STEP_NUM++))
done

# Step 5: Test Data
echo ""
echo -e "${MAGENTA}━━━ Step 5: Test Data ━━━${NC}"
echo ""

prompt_input "Test data required (e.g., user credentials, sample data):" TEST_DATA false

# Step 6: Figma Design (if UI test)
echo ""
if [ "$TEST_TYPE" = "UI/Visual" ]; then
    echo -e "${MAGENTA}━━━ Step 6: Figma Design Validation ━━━${NC}"
    echo ""
    
    prompt_input "Figma design URL (if applicable):" FIGMA_URL false
    prompt_input "Visual elements to validate:" VISUAL_CHECKS false
fi

# Step 7: Edge Cases
echo ""
echo -e "${MAGENTA}━━━ Step 7: Additional Info ━━━${NC}"
echo ""

prompt_input "Edge cases or variations to consider:" EDGE_CASES false
prompt_input "Related test cases (IDs):" RELATED_TCS false
prompt_input "Notes or comments:" NOTES false

# Generate filename
# Sanitise the id, then add the extension — doing it the other way round strips the dot
# and produces files called "TC-LOGIN-001md".
SAFE_ID="${TC_ID//[^a-zA-Z0-9_-]/}"
FILENAME="${SAFE_ID}.md"

OUTPUT_DIR="."
if [ ! -z "$1" ]; then
    OUTPUT_DIR="$1"
fi

OUTPUT_FILE="$OUTPUT_DIR/$FILENAME"

# Generate test case
echo ""
echo -e "${BLUE}Generating test case...${NC}"
echo ""

cat > "$OUTPUT_FILE" << EOF
# ${TC_ID}: ${TC_TITLE}

**Priority:** ${PRIORITY}
**Type:** ${TEST_TYPE}
**Status:** Not Run
**Estimated Time:** ${EST_TIME:-TBD} minutes
**Created:** $(date +%Y-%m-%d)

---

## Objective

${OBJECTIVE}

${WHY_IMPORTANT:+**Why this matters:** ${WHY_IMPORTANT}}

---

## Preconditions

${PRECONDITIONS}

---

## Test Steps

${TEST_STEPS}

---

## Test Data

${TEST_DATA:-No specific test data required}

---

EOF

# Add Figma section if UI test
if [ "$TEST_TYPE" = "UI/Visual" ] && [ -n "$FIGMA_URL" ]; then
    cat >> "$OUTPUT_FILE" << EOF
## Visual Validation (Figma)

**Design Reference:** ${FIGMA_URL}

**Elements to validate:**
${VISUAL_CHECKS}

**Verification checklist:**
- [ ] Layout matches Figma design
- [ ] Spacing (padding/margins) accurate
- [ ] Typography (font, size, weight, color) correct
- [ ] Colors match design system
- [ ] Component states (hover, active, disabled) implemented
- [ ] Responsive behavior as designed

---

EOF
fi

cat >> "$OUTPUT_FILE" << EOF
## Post-conditions

- [Describe system state after test execution]
- [Any cleanup required]

---

## Edge Cases & Variations

${EDGE_CASES:-Consider boundary values, null inputs, special characters, concurrent users}

---

## Related Test Cases

${RELATED_TCS:-None}

---

## Execution History

| Date | Tester | Build | Result | Notes |
|------|--------|-------|--------|-------|
| | | | Not Run | |

---

## Notes

${NOTES}

---

## Attachments

- [ ] Screenshots
- [ ] Screen recordings
- [ ] Console logs
- [ ] Network traces

EOF

echo -e "${GREEN}✅ Test case generated successfully!${NC}"
echo ""
echo -e "File location: ${BLUE}$OUTPUT_FILE${NC}"

# ── Machine-readable output ────────────────────────────────────────────────────
# The markdown above is for a person. Automation needs the contract described in
# SKILL.md ("Machine-readable output"), so offer it from the same answers rather than
# asking anyone to retype them. Appends to an existing file instead of overwriting it:
# that file may hold cases someone edited by hand.
echo ""
echo -e "${CYAN}Also write the machine-readable test_cases/<KEY>.json? [y/N]${NC}"
read -r WRITE_JSON

if [ "$WRITE_JSON" = "y" ] || [ "$WRITE_JSON" = "Y" ]; then
    JSON_KEY="${JIRA_TASK:-$TC_ID}"
    JSON_KEY="${JSON_KEY//[^a-zA-Z0-9_-]/}"
    [ -n "$JSON_KEY" ] || JSON_KEY="test_case"
    JSON_DIR="$OUTPUT_DIR/test_cases"
    mkdir -p "$JSON_DIR"
    JSON_FILE="$JSON_DIR/${JSON_KEY}.json"

    TC_TITLE="$TC_TITLE" TC_ID="$TC_ID" PRIORITY="$PRIORITY" TEST_TYPE="$TEST_TYPE" \
    OBJECTIVE="$OBJECTIVE" JIRA_TASK="$JIRA_TASK" JSON_FILE="$JSON_FILE" \
    STEPS_JOINED="$(printf '%s\n' "${STEP_ACTIONS[@]}")" \
    EXPECTED_JOINED="$(printf '%s\n' "${STEP_EXPECTED[@]}")" \
    python3 - <<'PYEOF'
import json, os, re, sys

def env(k):
    return os.environ.get(k, "").strip()

steps = [l for l in env("STEPS_JOINED").splitlines() if l.strip()]
expected = [l for l in env("EXPECTED_JOINED").splitlines() if l.strip()]

# `name` is the stable identifier downstream tooling maps on: snake_case, no spaces or
# punctuation. `summary` stays the human title. They are different fields on purpose.
slug = re.sub(r"[^a-z0-9]+", "_", env("TC_TITLE").lower()).strip("_") or env("TC_ID").lower()

case = {
    "name": slug,
    "summary": env("TC_TITLE"),
    "description": env("OBJECTIVE"),
    "steps": steps,
    # The per-step expectations are kept in order; the last one is the case's outcome.
    "expected_result": expected[-1] if expected else "",
    # The interactive menu speaks P0..P3; the JSON contract speaks Critical/High/Medium/Low.
    # Map here rather than letting two vocabularies into one file.
    "priority": {"P0": "Critical", "P1": "High", "P2": "Medium", "P3": "Low"}.get(
        env("PRIORITY").split(" ")[0], env("PRIORITY") or "Medium"),
    "type": env("TEST_TYPE") or "Functional",
    "jira_task": env("JIRA_TASK") or None,
}

path = env("JSON_FILE")
existing = []
if os.path.exists(path):
    try:
        with open(path, encoding="utf-8") as fh:
            existing = json.load(fh)
        if not isinstance(existing, list):
            print(f"  ! {path} is not a JSON array - leaving it alone.")
            sys.exit(1)
    except json.JSONDecodeError as exc:
        print(f"  ! {path} is not valid JSON ({exc}) - leaving it alone, fix it by hand.")
        sys.exit(1)

if any(c.get("name") == case["name"] for c in existing):
    print(f"  ! a case named '{case['name']}' is already in {path} - not added.")
    print("    Rename this one, or edit the file by hand. Nothing was overwritten.")
    sys.exit(0)

existing.append(case)
with open(path, "w", encoding="utf-8") as fh:
    json.dump(existing, fh, indent=2, ensure_ascii=False)
    fh.write("\n")
print(f"  {path} now holds {len(existing)} case(s).")
PYEOF

    if [ -f "$JSON_FILE" ]; then
        echo -e "${GREEN}✅ JSON written${NC}"
        echo -e "File location: ${BLUE}$JSON_FILE${NC}"
        if [ -z "$JIRA_TASK" ]; then
            echo -e "${YELLOW}No ticket key was given, so jira_task is null and the file is named after the test case id.${NC}"
        fi
    fi
fi
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Review test case for completeness"
echo "2. Add to test suite"
echo "3. Execute test and update results"
if [ "$TEST_TYPE" = "UI/Visual" ] && [ -n "$FIGMA_URL" ]; then
    echo "4. Validate against Figma design using MCP"
fi
echo ""
echo -e "${CYAN}Tip: Create multiple test cases for comprehensive coverage${NC}"
echo ""
