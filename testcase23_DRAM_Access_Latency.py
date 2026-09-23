import json
import os
import shutil
from test_utility import command_exists, log_output, run_cmd


def find_lat_mem_rd():
    configured = os.environ.get("LAT_MEM_RD")
    if configured:
        return configured
    discovered = shutil.which("lat_mem_rd")
    if discovered:
        return discovered
    packaged = "/usr/lib/lmbench/bin/x86_64-linux-gnu/lat_mem_rd"
    if os.path.isfile(packaged) and os.access(packaged, os.X_OK):
        return packaged
    return "lat_mem_rd"


def run():
    lat_mem_rd = find_lat_mem_rd()
    result = {
        "tools": {tool: command_exists(tool) for tool in ("perf", "mlc", "numactl")},
        "lat_mem_rd": lat_mem_rd,
    }
    if command_exists(lat_mem_rd):
        result["latency_scan"] = run_cmd(f"{lat_mem_rd} -P 1 -t 512m")
    else:
        result["latency_scan"] = "lmbench lat_mem_rd unavailable; install lmbench or set LAT_MEM_RD"
    if result["tools"]["perf"]:
        result["perf_memory"] = run_cmd("perf bench mem memcpy -s 4MB")
    if result["tools"]["mlc"]:
        result["mlc_latency"] = run_cmd("mlc --latency_matrix")
    if result["tools"]["numactl"]:
        result["numa_topology"] = run_cmd("numactl --hardware")
    result["status"] = "Latency plateaus require lmbench output analysis"
    log_output("dram_access_latency", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()