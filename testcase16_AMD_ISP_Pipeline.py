import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    media_device = os.environ.get("MEDIA_DEVICE", "/dev/media0")
    capture_device = os.environ.get("ISP_DEVICE", "/dev/video2")
    result = {
        "media_device": media_device,
        "capture_device": capture_device,
        "tools": {tool: command_exists(tool) for tool in ("media-ctl", "v4l2-ctl", "libcamera-still")},
    }
    if os.path.exists(media_device) and result["tools"]["media-ctl"]:
        result["pipeline_topology"] = run_cmd(f"media-ctl -d {media_device} -p")
    else:
        result["pipeline_topology"] = "AMD ISP media node or media-ctl unavailable"
    if os.path.exists(capture_device) and result["tools"]["v4l2-ctl"]:
        result["capture_formats"] = run_cmd(f"v4l2-ctl -d {capture_device} --list-formats-ext")
        result["capture_controls"] = run_cmd(f"v4l2-ctl -d {capture_device} --list-ctrls")
    else:
        result["capture_status"] = "ISP video node or v4l2-ctl unavailable"
    if result["tools"]["libcamera-still"]:
        output = os.environ.get("ISP_FRAME", "Logs/isp_frame.jpg")
        result["libcamera_capture"] = run_cmd(f"libcamera-still -n -o {output} --timeout 1000")
    else:
        result["libcamera_capture"] = "libcamera-still unavailable"
    result["status"] = "Pending measured sensor-to-frame latency and 3A validation"
    log_output("amd_isp_pipeline", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()