import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    model = os.environ.get("NPU_MODEL")
    provider = os.environ.get("NPU_PROVIDER", "AmdMIGraphXExecutionProvider")
    iterations = os.environ.get("NPU_ITERATIONS", "100")
    result = {"model": model, "provider": provider, "iterations": iterations}
    result["tools"] = {"python3": command_exists("python3")}
    if not model or not os.path.exists(model):
        result["status"] = "Set NPU_MODEL to an ONNX model; inference not run"
    else:
        result["benchmark"] = run_cmd(
            f"python3 -m onnxruntime.tools.benchmark_tool --model {model} "
            f"--execution_provider {provider} --intra_op_num_threads 1 "
            f"--iterations {iterations}"
        )
    log_output("npu_inference", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()