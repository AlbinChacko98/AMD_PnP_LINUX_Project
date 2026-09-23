import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    model = os.environ.get("NPU_MODEL")
    provider = os.environ.get("NPU_PROVIDER", "AmdMIGraphXExecutionProvider")
    benchmark = os.environ.get("NPU_BENCHMARK", "benchmark_npu.py")
    result = {
        "model": model,
        "provider": provider,
        "tools": {"turbostat": command_exists("turbostat"), "python3": command_exists("python3")},
    }
    if not result["tools"]["turbostat"]:
        result["status"] = "turbostat unavailable; power efficiency not measured"
    elif not model or not os.path.exists(model) or not os.path.exists(benchmark):
        result["status"] = "Set NPU_MODEL and NPU_BENCHMARK before running"
    else:
        result["idle_power"] = run_cmd("turbostat --quiet --interval 1 --num_iterations 2")
        result["inference"] = run_cmd(f"python3 {benchmark} --model {model} --provider {provider}")
        result["load_power"] = run_cmd("turbostat --quiet --interval 1 --num_iterations 5")
        result["status"] = "Pending GOPS/W calculation from inference operations and load-minus-idle power"
    log_output("npu_power_efficiency", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()