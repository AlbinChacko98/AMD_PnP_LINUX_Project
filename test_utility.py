import subprocess
import os
from datetime import datetime

LOGS_DIR = os.path.join(os.path.dirname(__file__), "Logs")
os.makedirs(LOGS_DIR, exist_ok=True)

def run_cmd(cmd):
    """Run a shell command and return stdout plus stderr for diagnostics."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode != 0:
            return f"exit_code={result.returncode}\n{output}".strip()
        return output
    except subprocess.TimeoutExpired:
        return "ERROR: command timed out after 300 seconds"
    except Exception as e:
        return f"ERROR: {e}"

def command_exists(command):
    return subprocess.run(
        f"command -v {command}",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0

def log_path(filename):
    os.makedirs(LOGS_DIR, exist_ok=True)
    return os.path.join(LOGS_DIR, filename)

def log_output(test_name, output):
    with open(log_path(f"{test_name}_log.txt"), "a") as f:
        f.write(f"\n===== {test_name.upper()} | {datetime.now().isoformat(timespec='seconds')} =====\n")
        f.write(f"{output}\n")