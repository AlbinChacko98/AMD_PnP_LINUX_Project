import json
import os
from datetime import datetime
from test_utility import LOGS_DIR, command_exists, log_output, run_cmd

def run():
    result = {"tools": {tool: command_exists(tool) for tool in ("ffmpeg",)}}
    device = os.environ.get("VAAPI_DEVICE", "/dev/dri/renderD128")
    if not os.path.exists(device) or not result["tools"]["ffmpeg"]:
        result["status"] = "VAAPI or ffmpeg unavailable"
        log_output("video_decode", json.dumps(result, indent=4))
        return

    input_file = os.environ.get("VIDEO_INPUT")
    codec = os.environ.get("VIDEO_CODEC")
    if input_file or codec:
        codec = codec or "h264"
        input_file = input_file or os.path.join(LOGS_DIR, "decode_source_h264.mp4")
        test_cases = [(codec, input_file, None)]
    else:
        test_cases = [
            ("h264", os.path.join(LOGS_DIR, "decode_source_h264.mp4"), "1280x720"),
            ("hevc", os.path.join(LOGS_DIR, "decode_source_hevc_4k.mp4"), "3840x2160"),
            ("av1", os.path.join(LOGS_DIR, "decode_source_av1_4k.mkv"), "3840x2160"),
        ]

    source_generation = {}
    decodes = {}
    encoders = {"h264": "libx264", "hevc": "libx265", "av1": "libaom-av1"}
    for codec, input_file, size in test_cases:
        if not os.path.exists(input_file) and size:
            encoder_options = {
                "h264": "-c:v libx264 -preset ultrafast -crf 23",
                "hevc": "-c:v libx265 -preset ultrafast -crf 35",
                "av1": "-c:v libaom-av1 -cpu-used 8 -crf 35 -b:v 0",
            }[codec]
            source_generation[codec] = run_cmd(
                f"ffmpeg -y -f lavfi -i testsrc=duration=5:size={size}:rate=30 "
                f"{encoder_options} -pix_fmt yuv420p {input_file}"
            )
        if not os.path.exists(input_file):
            decodes[codec] = {"status": "Unable to create or find decode input"}
            continue
        decodes[codec] = run_cmd(
            f"ffmpeg -benchmark -hwaccel vaapi -hwaccel_device {device} "
            f"-c:v {codec} -i {input_file} -f null -"
        )

    result.update({"source_generation": source_generation, "decodes": decodes})

    log_output("video_decode", json.dumps(result, indent=4))

if __name__ == "__main__":
    run()