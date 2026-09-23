import json
import os
import time
from test_utility import command_exists, log_output, run_cmd

def check_pstate():
    return run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver")

def set_governor(mode):
    return run_cmd(f"cpupower frequency-set -g {mode}")

def get_freq():
    return run_cmd("cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_cur_freq")

def read_sysfs(path):
    return run_cmd(f"cat {path}")

def main():
    result = {}
    result["tools"] = {tool: command_exists(tool) for tool in ("cpupower", "sysbench", "turbostat --interval 1")}
    result["driver"] = check_pstate()
    result["governor_before"] = read_sysfs("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    result["epp"] = read_sysfs("/sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference")
    result["idle_freq_khz"] = get_freq()

    result["performance_governor"] = set_governor("performance")
    result["performance_freq_khz"] = get_freq()
    if command_exists("sysbench"):
        result["sysbench"] = run_cmd("sysbench cpu --threads=$(nproc) --time=10 run")
        time.sleep(1)
        result["boost_freq_khz"] = get_freq()

    result["powersave_governor"] = set_governor("powersave")
    time.sleep(1)
    result["powersave_freq_khz"] = get_freq()

    log_output("pstate_test", json.dumps(result, indent=4))

if __name__ == "__main__":
    main()