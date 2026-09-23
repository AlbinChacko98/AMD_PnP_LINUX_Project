import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    stream_binary = os.environ.get("STREAM_BINARY", "./stream_c.exe")
    mbw_size = os.environ.get("MBW_SIZE_MB", "1024")
    result = {
        "tools": {tool: command_exists(tool) for tool in ("mbw", "numactl", "radeontop")},
        "stream_binary": stream_binary,
        "mbw_size_mb": mbw_size,
    }
    if os.path.exists(stream_binary) and os.access(stream_binary, os.X_OK):
        result["stream_copy_scale"] = run_cmd(stream_binary)
    else:
        result["stream_copy_scale"] = "STREAM binary unavailable; set STREAM_BINARY to a built executable"
    if result["tools"]["mbw"]:
        result["mbw_write_copy"] = run_cmd(f"mbw -t 2 -n 100 {mbw_size}")
    if result["tools"]["numactl"] and result["tools"]["mbw"]:
        result["numa_mbw"] = run_cmd(f"numactl --physcpubind=0 mbw -n 100 {mbw_size}")
        result["numa_topology"] = run_cmd("numactl --hardware")
    if result["tools"]["radeontop"]:
        result["gpu_monitor_note"] = "Run radeontop separately during this test for iGPU contention"
    result["status"] = "Pending measured bandwidth drop under simultaneous iGPU load"
    log_output("dram_write_copy", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()