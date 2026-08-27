#!/usr/bin/env bash

set -euo pipefail

BASE_URL="${1:-http://127.0.0.1:8000}"
ENV_FILE="${HOME}/.config/runtime-validity/runtime-validity.env"

if [[ ! -r "${ENV_FILE}" ]]; then
    echo "Cannot read experimental-control environment file: ${ENV_FILE}" >&2
    exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

if [[ "${RUNTIME_VALIDITY_ENABLE_EXPERIMENTAL_CONTROL:-}" != "1" ]]; then
    echo "Experimental authority control is not enabled." >&2
    exit 1
fi

if [[ -z "${RUNTIME_VALIDITY_EXPERIMENTAL_CONTROL_TOKEN:-}" ]]; then
    echo "Experimental control token is not configured." >&2
    exit 1
fi

TMP_DIR="$(mktemp -d)"
TRANSITION_FILE="${TMP_DIR}/transition.json"
DECISION_FILE="${TMP_DIR}/decision.json"

reset_authority() {
    curl -fsS \
        -X POST \
        "${BASE_URL}/experimental/authority-state" \
        -H "Content-Type: application/json" \
        -H "X-Experimental-Control-Token: ${RUNTIME_VALIDITY_EXPERIMENTAL_CONTROL_TOKEN}" \
        -d '{"authority_valid": true}' \
        >/dev/null
}

cleanup() {
    local exit_status=$?

    trap - EXIT

    if ! reset_authority 2>/dev/null; then
        echo "WARNING: failed to reset authority state to true." >&2
    fi

    rm -rf "${TMP_DIR}"
    unset RUNTIME_VALIDITY_ENABLE_EXPERIMENTAL_CONTROL
    unset RUNTIME_VALIDITY_EXPERIMENTAL_CONTROL_TOKEN

    exit "${exit_status}"
}

trap cleanup EXIT

echo
echo "=== Runtime Validity demo ==="
echo "Target: ${BASE_URL}"

echo
echo "=== 1. Establish clean authority state ==="

reset_authority

curl -fsS \
    -X POST \
    "${BASE_URL}/decide" \
    -H "Content-Type: application/json" \
    -d '{
      "action_proposal": "demo consequential action",
      "prior_decision": {
        "decision_id": "demo-baseline",
        "outcome": "PROCEED",
        "obligations": [
          {
            "obligation_id": "authority-valid-001",
            "kind": "authority_valid",
            "expected": true
          }
        ]
      },
      "revalidation_mode": "full"
    }' \
    > "${DECISION_FILE}"

python -m json.tool "${DECISION_FILE}"

python - "${DECISION_FILE}" <<'PY'
import json
import sys

with open(sys.argv[1]) as f:
    body = json.load(f)

evaluation = body["evidence"]["obligation_evaluations"][0]

assert body["outcome"] == "PROCEED"
assert evaluation["current"] is True
assert evaluation["result"] == "MATCH"

print("CHECK: baseline is PROCEED / MATCH")
PY

echo
echo "=== 2. Induce controlled authority change true -> false ==="

curl -fsS \
    -X POST \
    "${BASE_URL}/experimental/authority-state" \
    -H "Content-Type: application/json" \
    -H "X-Experimental-Control-Token: ${RUNTIME_VALIDITY_EXPERIMENTAL_CONTROL_TOKEN}" \
    -d '{"authority_valid": false}' \
    > "${TRANSITION_FILE}"

python -m json.tool "${TRANSITION_FILE}"

TRANSITION_ID="$(
    python - "${TRANSITION_FILE}" <<'PY'
import json
import sys

with open(sys.argv[1]) as f:
    transition = json.load(f)

assert transition["previous_authority_valid"] is True
assert transition["current_authority_valid"] is False

print(transition["transition_id"])
PY
)"

echo
echo "CHECK: transition recorded as true -> false"

echo
echo "=== 3. Retrieve retained transition evidence ==="

curl -fsS \
    "${BASE_URL}/authority-transitions/${TRANSITION_ID}" \
    | python -m json.tool

echo
echo "=== 4. Revalidate prior decision ==="

curl -fsS \
    -X POST \
    "${BASE_URL}/decide" \
    -H "Content-Type: application/json" \
    -d '{
      "action_proposal": "demo consequential action",
      "prior_decision": {
        "decision_id": "demo-after-authority-change",
        "outcome": "PROCEED",
        "obligations": [
          {
            "obligation_id": "authority-valid-001",
            "kind": "authority_valid",
            "expected": true
          }
        ]
      },
      "revalidation_mode": "full"
    }' \
    > "${DECISION_FILE}"

python -m json.tool "${DECISION_FILE}"

python - "${DECISION_FILE}" <<'PY'
import json
import sys

with open(sys.argv[1]) as f:
    body = json.load(f)

evaluation = body["evidence"]["obligation_evaluations"][0]

assert body["outcome"] == "HOLD"
assert evaluation["current"] is False
assert evaluation["result"] == "MISMATCH"

print("CHECK: changed authority produces HOLD / MISMATCH")
PY

echo
echo "=== Demo complete ==="
echo "Authority state will be reset to true on exit."
