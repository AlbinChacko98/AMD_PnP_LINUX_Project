import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    stream_binary = os.environ.get("STREAM_BINARY", "./stream_c.exe")
    mbw_size = os.environ.get("MBW_SIZE_MB", "1024")
    result = {
        "tools": {tool: command_exists(tool) for tool in ("mbw", "sysbench", "dmidecode", "hwinfo")},
        "stream_binary": stream_binary,
        "mbw_size_mb": mbw_size,
    }
    if os.path.exists(stream_binary) and os.access(stream_binary, os.X_OK):
        result["stream"] = run_cmd(stream_binary)
    else:
        result["stream"] = "STREAM binary unavailable; set STREAM_BINARY to a built executable"
    if result["tools"]["mbw"]:
        result["mbw"] = run_cmd(f"mbw -n 100 {mbw_size}")
    if result["tools"]["sysbench"]:
        total_size = os.environ.get("SYSBENCH_MEMORY_SIZE", "10G")
        result["sysbench_read"] = run_cmd(
            f"sysbench memory --memory-oper=read --memory-total-size={total_size} run"
        )
    for tool, command in (("dmidecode", "dmidecode --type memory"), ("hwinfo", "hwinfo --memory")):
        if result["tools"][tool]:
            result[tool] = run_cmd(command)
    result["status"] = "Pending STREAM/MBW measurement if required tools are unavailable"
    log_output("dram_read_bandwidth", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()