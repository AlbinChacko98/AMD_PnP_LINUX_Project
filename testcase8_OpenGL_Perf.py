import subprocess
import re
import json
import csv
import os
from datetime import datetime
from test_utility import LOGS_DIR, log_output

# ==============================
# CONFIGURATION
# ==============================
RESOLUTIONS = [
    ("1280x720", "720p"),
    ("1920x1080", "1080p"),
    ("2560x1440", "1440p"),
    ("3840x2160", "4K")
]

OUTPUT_PREFIX = "opengl_perf"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# ==============================
# UTILITY FUNCTIONS
# ==============================

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        output = (result.stdout + result.stderr).strip()
        return output if result.returncode == 0 else f"exit_code={result.returncode}\n{output}"
    except subprocess.TimeoutExpired:
        return "ERROR: command timed out after 300 seconds"
    except Exception as e:
        return f"ERROR: {str(e)}"


def check_tool(tool):
    return subprocess.call(f"which {tool}", shell=True,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


# ==============================
# SYSTEM INFO COLLECTION
# ==============================

def get_opengl_info():
    output = run_command("glxinfo | grep 'OpenGL'")
    return output


def get_gpu_info():
    return run_command("lspci | grep -i vga")


# ==============================
# GLMARK2 EXECUTION + PARSING
# ==============================

def run_glmark2(resolution):
    cmd = f"glmark2 --off-screen --size {resolution}"
    print(f"Running: {cmd}")
    output = run_command(cmd)
    return output


def parse_glmark2(output):
    results = {}

    # Extract final score
    score_match = re.search(r"glmark2 Score:\s*(\d+)", output)
    if score_match:
        results["score"] = int(score_match.group(1))
    else:
        results["score"] = None

    # Extract scene FPS
    scenes = {}
    for line in output.splitlines():
        match = re.search(r"\[\s*(.*?)\s*\].*?FPS:\s*([\d\.]+)", line)
        if match:
            scene = match.group(1)
            fps = float(match.group(2))
            scenes[scene] = fps

    results["scenes"] = scenes
    return results


# ==============================
# MAIN EXECUTION
# ==============================

def main():

    print("===== OpenGL Performance Automation =====")

    # Tool validation
    required_tools = ["glmark2", "glxinfo"]
    for tool in required_tools:
        if not check_tool(tool):
            print(f"ERROR: {tool} not installed. Install using apt.")
            return

    # Collect system info
    system_info = {
        "gpu": get_gpu_info(),
        "opengl": get_opengl_info()
    }

    print("System Info Collected")

    final_results = []

    # Run benchmarks
    for res, label in RESOLUTIONS:
        raw_output = run_glmark2(res)
        parsed = parse_glmark2(raw_output)

        entry = {
            "resolution": label,
            "raw_resolution": res,
            "score": parsed.get("score"),
            "scene_fps": parsed.get("scenes")
        }

        final_results.append(entry)

    # ==============================
    # SAVE RESULTS
    # ==============================

    json_file = f"{OUTPUT_PREFIX}_{TIMESTAMP}.json"
    csv_file = f"{OUTPUT_PREFIX}_{TIMESTAMP}.csv"
    os.makedirs(LOGS_DIR, exist_ok=True)
    json_file = os.path.join(LOGS_DIR, json_file)
    csv_file = os.path.join(LOGS_DIR, csv_file)

    # Save JSON
    with open(json_file, "w") as f:
        json.dump({
            "system_info": system_info,
            "results": final_results
        }, f, indent=4)

    # Save CSV (flattened)
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Resolution", "Score"])

        for r in final_results:
            writer.writerow([r["resolution"], r["score"]])

    print(f"\nResults saved:")
    print(f"JSON: {json_file}")
    print(f"CSV : {csv_file}")
    log_output("opengl_perf", json.dumps({
        "system_info": system_info,
        "results": final_results
    }, indent=4))


if __name__ == "__main__":
    main()