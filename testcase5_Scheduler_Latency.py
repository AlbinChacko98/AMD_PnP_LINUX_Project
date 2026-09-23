import json
import os
from test_utility import command_exists, log_output, run_cmd

def main():
    result = {}
    cyclic_duration = os.environ.get("CYCLICTEST_DURATION", "10")
    result["tools"] = {tool: command_exists(tool) for tool in ("cyclictest", "perf", "vmstat")}
    if result["tools"]["cyclictest"]:
        result["cyclictest"] = run_cmd(
            f"sudo cyclictest -p 99 -t1 -n -i 1000 -D {cyclic_duration}"
        )
    if result["tools"]["perf"]:
        result["context_switch"] = run_cmd("perf stat -e context-switches -a sleep 5")
    if result["tools"]["vmstat"]:
        result["vmstat"] = run_cmd("vmstat 1 5")

    log_output("scheduler_test", json.dumps(result, indent=4))

if __name__ == "__main__":
    main()