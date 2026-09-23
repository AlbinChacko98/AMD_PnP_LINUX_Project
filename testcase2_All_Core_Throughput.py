import json
from test_utility import command_exists, log_output, run_cmd

def main():
    result = {}
    result["threads"] = run_cmd("nproc")
    result["tools"] = {tool: command_exists(tool) for tool in ("sysbench", "stress-ng", "amdrun")}
    if result["tools"]["sysbench"]:
        result["sysbench"] = run_cmd("sysbench cpu --cpu-max-prime=50000 --threads=$(nproc) run")
    if result["tools"]["stress-ng"]:
        result["stress_ng"] = run_cmd("stress-ng --cpu 0 --timeout 30 --metrics-brief")
    if result["tools"]["amdrun"]:
        result["amdrun"] = run_cmd("amdrun --config cpu_perf.xml")

    log_output("cpu_throughput", json.dumps(result, indent=4))

if __name__ == "__main__":
    main()