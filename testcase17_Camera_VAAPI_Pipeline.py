import json
import os
from test_utility import command_exists, log_output, run_cmd


def run():
    device = os.environ.get("CAMERA_DEVICE", "/dev/video0")
    vaapi_device = os.environ.get("VAAPI_DEVICE", "/dev/dri/renderD128")
    output_file = os.environ.get("CAMERA_ENCODE_OUTPUT", "Logs/camera_vaapi_output.mp4")
    result = {
        "camera_device": device,
        "vaapi_device": vaapi_device,
        "tools": {tool: command_exists(tool) for tool in ("ffmpeg", "vainfo")},
    }
    if not os.path.exists(device) or not os.path.exists(vaapi_device):
        result["status"] = "Camera or VA-API device unavailable"
        log_output("camera_vaapi_pipeline", json.dumps(result, indent=4))
        return
    if not all(result["tools"].values()):
        result["status"] = "ffmpeg and vainfo are required"
        log_output("camera_vaapi_pipeline", json.dumps(result, indent=4))
        return

    result["vaapi_check"] = run_cmd(f"vainfo --display drm --device {vaapi_device} | grep -i H264")
    result["pipeline"] = run_cmd(
        f"ffmpeg -y -hide_banner -benchmark -f v4l2 -input_format mjpeg "
        f"-framerate 30 -video_size 1920x1080 -i {device} -t 5 "
        f"-vf 'format=nv12,hwupload' -c:v h264_vaapi -b:v 4M {output_file}"
    )
    result["output"] = output_file
    log_output("camera_vaapi_pipeline", json.dumps(result, indent=4))


if __name__ == "__main__":
    run()