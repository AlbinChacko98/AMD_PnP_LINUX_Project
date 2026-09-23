import json
from test_utility import command_exists, log_output, run_cmd

def main():
    workload = "sysbench cpu --threads=1 run"
    result = {}
    result["tools"] = {tool: command_exists(tool) for tool in ("perf", "sysbench", "AMDuProfCLI")}
    if result["tools"]["perf"] and result["tools"]["sysbench"]:
        result["perf_stat"] = run_cmd(f"perf stat -e instructions,cycles,branch-misses,cache-misses {workload}")
    if result["tools"]["AMDuProfCLI"]:
        result["uprof_hint"] = "AMDuProfCLI is available; run the workload-specific IPC collection separately."

    log_output("ipc_test", json.dumps(result, indent=4))

if __name__ == "__main__":
    main()