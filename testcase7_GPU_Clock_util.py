import json
import os
import subprocess
import time
from test_utility import command_exists, log_output, run_cmd

def main():
    result = {}
    result["tools"] = {tool: command_exists(tool) for tool in ("lspci", "radeontop", "glmark2", "rocm-smi")}
    result["gpu_info"] = run_cmd("lspci | grep -iE 'vga|display|3d'")
    clock_path = "/sys/class/drm/card0/device/pp_dpm_sclk"
    result["idle_clock"] = run_cmd(f"cat {clock_path}")

    load_process = None
    try:
        if result["tools"]["glmark2"]:
            load_process = subprocess.Popen(
                ["glmark2", "--off-screen", "--run-forever"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(5)
        result["load_clock"] = run_cmd(f"cat {clock_path}")
        if result["tools"]["radeontop"]:
            result["utilization"] = run_cmd("radeontop -d - -l 1")
        if result["tools"]["rocm-smi"]:
            result["rocm_smi"] = run_cmd("rocm-smi --showclocks --showuse")
    finally:
        if load_process is not None:
            load_process.terminate()
            load_process.wait(timeout=5)

    log_output("gpu_monitor", json.dumps(result, indent=4))

if __name__ == "__main__":
    main()