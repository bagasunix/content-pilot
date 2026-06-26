#!/usr/bin/env bash
# job-state.sh — State management untuk blog lifecycle jobs
# Usage:
#   job-state.sh create <job_id> <topic>     — buat job baru
#   job-state.sh get <job_id>                 — lihat state
#   job-state.sh transition <job_id> <phase>  — pindah phase
#   job-state.sh complete <job_id> <phase>    — tandai phase COMPLETE
#   job-state.sh fail <job_id> <phase>        — tandai phase FAILED
#   job-state.sh abort <job_id> <reason>      — abort job
#   job-state.sh check-event <job_id> <phase> — cek idempotency
#   job-state.sh list                         — list semua jobs

set -uo pipefail

STATE_DIR="$(dirname "$0")/jobs"
TEMPLATE="$STATE_DIR/_template.json"

ensure_dir() {
  mkdir -p "$STATE_DIR"
}

now() {
  date -u +"%Y-%m-%dT%H:%M:%S+07:00"
}

case "${1:-help}" in
  create)
    ensure_dir
    JOB_ID="$2"
    TOPIC="$3"
    FILE="$STATE_DIR/$JOB_ID.json"
    if [ -f "$FILE" ]; then
      echo "{\"error\": \"Job $JOB_ID already exists\"}"
      exit 1
    fi
    sed -e "s/\"BLG-001\"/\"$JOB_ID\"/" \
        -e "s|\"topic\": \"\"|\"topic\": \"$TOPIC\"|" \
        -e "s|\"created_at\": \"[^\"]*\"|\"created_at\": \"$(now)\"|" \
        -e "s|\"updated_at\": \"[^\"]*\"|\"updated_at\": \"$(now)\"|" \
        "$TEMPLATE" > "$FILE"
    cat "$FILE"
    ;;

  get)
    FILE="$STATE_DIR/$2.json"
    if [ ! -f "$FILE" ]; then
      echo "{\"error\": \"Job $2 not found\"}"
      exit 1
    fi
    cat "$FILE"
    ;;

  transition)
    FILE="$STATE_DIR/$2.json"
    PHASE="$3"
    if [ ! -f "$FILE" ]; then
      echo "{\"error\": \"Job $2 not found\"}"
      exit 1
    fi
    python3 -c "
import json, sys
from datetime import datetime
with open('$FILE') as f:
    data = json.load(f)
data['current_phase'] = '$PHASE'
data['phases']['$PHASE']['status'] = 'in_progress'
data['phases']['$PHASE']['started_at'] = '$(now)'
data['updated_at'] = '$(now)'
with open('$FILE', 'w') as f:
    json.dump(data, f, indent=2)
print(json.dumps(data, indent=2))
"
    ;;

  complete)
    FILE="$STATE_DIR/$2.json"
    PHASE="$3"
    if [ ! -f "$FILE" ]; then
      echo "{\"error\": \"Job $2 not found\"}"
      exit 1
    fi
    python3 -c "
import json, sys
from datetime import datetime
with open('$FILE') as f:
    data = json.load(f)
event_key = '$2:$PHASE:complete'
if event_key in data.get('processed_events', []):
    print(json.dumps({'warning': 'Duplicate event', 'event': event_key}))
    sys.exit(0)
data['phases']['$PHASE']['status'] = 'complete'
data['phases']['$PHASE']['completed_at'] = '$(now)'
data.setdefault('processed_events', []).append(event_key)
data['updated_at'] = '$(now)'
with open('$FILE', 'w') as f:
    json.dump(data, f, indent=2)
print(json.dumps(data, indent=2))
"
    ;;

  fail)
    FILE="$STATE_DIR/$2.json"
    PHASE="$3"
    if [ ! -f "$FILE" ]; then
      echo "{\"error\": \"Job $2 not found\"}"
      exit 1
    fi
    python3 -c "
import json
with open('$FILE') as f:
    data = json.load(f)
data['phases']['$PHASE']['status'] = 'failed'
data['retry_count'] = data.get('retry_count', 0) + 1
data['updated_at'] = '$(now)'
with open('$FILE', 'w') as f:
    json.dump(data, f, indent=2)
print(json.dumps(data, indent=2))
"
    ;;

  abort)
    FILE="$STATE_DIR/$2.json"
    REASON="$3"
    if [ ! -f "$FILE" ]; then
      echo "{\"error\": \"Job $2 not found\"}"
      exit 1
    fi
    python3 -c "
import json
with open('$FILE') as f:
    data = json.load(f)
data['current_phase'] = 'aborted'
data['abort_reason'] = '$REASON'
data['updated_at'] = '$(now)'
with open('$FILE', 'w') as f:
    json.dump(data, f, indent=2)
print(json.dumps(data, indent=2))
"
    ;;

  check-event)
    FILE="$STATE_DIR/$2.json"
    PHASE="$3"
    if [ ! -f "$FILE" ]; then
      echo "{\"exists\": false}"
      exit 0
    fi
    python3 -c "
import json
with open('$FILE') as f:
    data = json.load(f)
event_key = '$2:$PHASE:complete'
if event_key in data.get('processed_events', []):
    print(json.dumps({'exists': True, 'event': event_key, 'duplicate': True}))
else:
    print(json.dumps({'exists': False, 'event': event_key, 'duplicate': False}))
"
    ;;

  list)
    ensure_dir
    ls "$STATE_DIR"/*.json 2>/dev/null | grep -v _template | while read f; do
      python3 -c "
import json
with open('$f') as fh:
    d = json.load(fh)
print(f\"{d['job_id']}  {d['current_phase']}  {d['phases'].get(d['current_phase'],{}).get('status','?')}  {d['topic'][:50]}\")
"
    done
    ;;

  *)
    echo "Usage: job-state.sh {create|get|transition|complete|fail|abort|check-event|list} [args]"
    ;;
esac
