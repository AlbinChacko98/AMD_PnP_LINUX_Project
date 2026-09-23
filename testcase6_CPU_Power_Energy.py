import glob
import json
import time
from test_utility import command_exists, log_output, run_cmd

def read_energy():
    for path in glob.glob("/sys/class/powercap/*/energy_uj"):
        try:
            with open(path) as energy_file:
                return path, int(energy_file.read().strip())
        except (OSError, ValueError):
            continue
    return None, None

def main():
    result = {}
    result["tools"] = {tool: command_exists(tool) for tool in ("stress-ng", "turbostat", "powertop")}
    energy_path, start = read_energy()
    result["energy_path"] = energy_path
    time.sleep(5)

    if result["tools"]["stress-ng"]:
        result["stress_ng"] = run_cmd("stress-ng --cpu 0 --timeout 10 --metrics-brief")

    _, end = read_energy()

    if start is not None and end is not None:
        result["energy_joules"] = (end - start) / 1e6
        result["measurement_seconds"] = 15
    else:
        result["energy_joules"] = None
        result["energy_status"] = "No readable powercap energy_uj file found"

    if result["tools"]["turbostat"]:
        result["turbostat"] = run_cmd("turbostat --interval 1 --quiet sleep 3")

    log_output("power_test", json.dumps(result, indent=4))

if __name__ == "__main__":
    main()