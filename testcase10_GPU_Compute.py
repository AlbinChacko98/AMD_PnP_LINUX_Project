import json
from test_utility import command_exists, log_output, run_cmd

def run():
    result = {
        "tools": {tool: command_exists(tool) for tool in ("clinfo", "clpeak", "rocm-bandwidth-test", "hashcat")}
    }
    if result["tools"]["clinfo"]:
        result["clinfo"] = run_cmd("clinfo | grep -E 'Platform|Device|Compute Units|MAX_COMPUTE'")
    if result["tools"]["clpeak"]:
        result["clpeak"] = run_cmd("clpeak")
    if result["tools"]["rocm-bandwidth-test"]:
        result["rocm_bandwidth"] = run_cmd("rocm-bandwidth-test -t 3")
    if result["tools"]["hashcat"]:
        result["hashcat"] = run_cmd("hashcat -b -D 2")

    log_output("gpu_compute", json.dumps(result, indent=4))

if __name__ == "__main__":
    run()