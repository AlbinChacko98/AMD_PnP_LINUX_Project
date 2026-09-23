import json
from test_utility import command_exists, log_output, run_cmd

def main():
    result = {}
    result["tools"] = {tool: command_exists(tool) for tool in ("perf", "valgrind", "lmbench")}
    if result["tools"]["perf"]:
        result["perf_cache"] = run_cmd(
            "perf stat -e L1-dcache-load-misses,LLC-loads,LLC-load-misses ls"
        )
    if result["tools"]["valgrind"]:
        result["cachegrind"] = run_cmd("valgrind --tool=cachegrind ls")
    if result["tools"]["lmbench"]:
        result["lat_mem_rd"] = run_cmd("lat_mem_rd 4 512")

    log_output("cache_test", json.dumps(result, indent=4))

if __name__ == "__main__":
    main()