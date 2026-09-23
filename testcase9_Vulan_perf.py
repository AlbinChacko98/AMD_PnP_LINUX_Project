import json
from test_utility import command_exists, log_output, run_cmd

def run():
    result = {
        "tools": {tool: command_exists(tool) for tool in ("vulkaninfo", "vkmark")}
    }
    if result["tools"]["vulkaninfo"]:
        result["vulkan_info"] = run_cmd("vulkaninfo | grep -E 'apiVersion|driverVersion'")
    if result["tools"]["vkmark"]:
        result["vkmark"] = run_cmd("vkmark -s 1920x1080")

    log_output("vulkan_test", json.dumps(result, indent=4))

if __name__ == "__main__":
    run()