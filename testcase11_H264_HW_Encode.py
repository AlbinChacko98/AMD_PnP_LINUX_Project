# tests/h264_encode.py
import json
from datetime import datetime
from test_utility import LOGS_DIR, command_exists, log_output, run_cmd
import os

def run():
    result = {"tools": {tool: command_exists(tool) for tool in ("vainfo", "ffmpeg")}}
    device = os.environ.get("VAAPI_DEVICE", "/dev/dri/renderD128")
    if not os.path.exists(device) or not result["tools"]["vainfo"] or not result["tools"]["ffmpeg"]:
        result["status"] = "VAAPI or required tool unavailable"
        log_output("h264_encode", json.dumps(result, indent=4))
        return

    check = run_cmd(f"vainfo --display drm --device {device} | grep -i H264")
    output_file = os.path.join(LOGS_DIR, f"h264_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4")
    
    encode = run_cmd(f"""
    ffmpeg -y -benchmark -hwaccel vaapi -hwaccel_device {device} \
    -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 \
    -vf 'format=nv12,hwupload' \
    -c:v h264_vaapi -b:v 5M {output_file}
    """)

    log_output("h264_encode", json.dumps({"vaapi_check": check, "encode": encode, "output": output_file}, indent=4))

if __name__ == "__main__":
    run()