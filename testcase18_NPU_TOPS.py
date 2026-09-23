import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    model = os.environ.get("NPU_MODEL")
    provider = os.environ.get("NPU_PROVIDER", "AmdMIGraphXExecutionProvider")
    result = {
        "model": model,
        "provider": provider,
        "tools": {tool: command_exists(tool) for tool in ("python3", "xrt-smi")},
    }
    if result["tools"]["xrt-smi"]:
        result["npu_visibility"] = run_cmd("xrt-smi examine")
    else:
        result["npu_visibility"] = "xrt-smi unavailable"
    if not model or not os.path.exists(model):
        result["status"] = "Set NPU_MODEL to an ONNX model; no TOPS measured"
        log_output("npu_tops", json.dumps(result, indent=4))
        return

    benchmark = os.environ.get("NPU_BENCHMARK", "benchmark_npu.py")
    if os.path.exists(benchmark):
        result["benchmark"] = run_cmd(f"python3 {benchmark} --model {model} --provider {provider}")
    else:
        result["status"] = "NPU benchmark script unavailable"
    result["status"] = result.get("status", "Pending effective TOPS calculation from model FLOPs")
    log_output("npu_tops", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()