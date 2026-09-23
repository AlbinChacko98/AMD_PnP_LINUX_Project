import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    device = os.environ.get("CAMERA_DEVICE", "/dev/video0")
    result = {
        "device": device,
        "tools": {tool: command_exists(tool) for tool in ("v4l2-ctl", "ffmpeg")},
        "measurements": {},
    }
    if not os.path.exists(device):
        result["status"] = "Camera device unavailable"
        log_output("camera_capture", json.dumps(result, indent=4))
        return
    if not all(result["tools"].values()):
        result["status"] = "v4l2-ctl and ffmpeg are required"
        log_output("camera_capture", json.dumps(result, indent=4))
        return

    result["formats"] = run_cmd(f"v4l2-ctl --device {device} --list-formats-ext")
    formats = os.environ.get("CAMERA_FORMATS", "mjpeg,yuyv422").split(",")
    resolutions = os.environ.get("CAMERA_RESOLUTIONS", "640x480,1280x720,1920x1080").split(",")
    for pixel_format in formats:
        for resolution in resolutions:
            width, height = resolution.split("x", 1)
            command = (
                f"ffmpeg -hide_banner -benchmark -f v4l2 -input_format {pixel_format} "
                f"-video_size {width}x{height} -framerate 30 -i {device} "
                f"-t 5 -f null -"
            )
            result["measurements"][f"{pixel_format}_{resolution}"] = run_cmd(command)

    log_output("camera_capture", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()