# AMD PnP Linux Project

Python automation scripts for Linux CPU, GPU, video, camera, ISP, and NPU
validation. Each testcase checks its required tools and hardware, runs system
commands, and appends results to `Logs/`.

## Framework flow

```text
Run testcase -> check tools and hardware -> run benchmark -> capture output
-> build result -> write timestamped result to Logs/
```

Common helpers are in `test_utility.py`:

- `run_cmd()` executes commands with a 300-second timeout.
- `command_exists()` checks whether a command is installed.
- `log_output()` appends results to `Logs/<test>_log.txt`.

## Testcase index

| ID | Script                                   | Area      | Main measurement |
|---:|---                                       |---        |---               |
| 1 | `testcase1_PstateScaling.py`              | CPU P-state | Frequency, governors, EPP, boost, and sysbench |
| 2 | `testcase2_All_Core_Throughput.py`        | CPU | All-core throughput |
| 3 | `testcase3_IPC_Microarch _Efficiency.py`  | CPU microarchitecture | IPC and efficiency |
| 4 | `testcase4_Cache_Hit_Rate_Latency.py`     | CPU cache | Cache hit rate and latency |
| 5 | `testcase5_Scheduler_Latency.py`          | Linux scheduler | Scheduler latency |
| 6 | `testcase6_CPU_Power_Energy.py`           | CPU power | Package power and energy |
| 7 | `testcase7_GPU_Clock_util.py`             | GPU | GPU clock and utilization |
| 8 | `testcase8_OpenGL_Perf.py`                | OpenGL | OpenGL rendering performance |
| 9 | `testcase9_Vulan_perf.py`                 | Vulkan | Vulkan capability and vkmark score |
| 10 | `testcase10_GPU_Compute.py`              | GPU compute | OpenCL, clpeak, ROCm bandwidth, and Hashcat |
| 11 | `testcase11_H264_HW_Encode.py`           | Video encode | H.264 VA-API encoding |
| 12 | `testcase12_H265_HEVC_Encode.py`         | Video encode | HEVC VA-API encoding |
| 13 | `testcase13_AV1_Encode.py`               | Video encode | AV1 VA-API capability |
| 14 | `testcase14_Video_Decode_test.py`        | Video decode | H.264 720p, HEVC 4K, and AV1 4K |
| 15 | `testcase15_USB_Camera_Capture.py`       | Camera/UVC | V4L2 formats, resolutions, and capture FPS |
| 16 | `testcase16_AMD_ISP_Pipeline.py`         | AMD ISP | Media topology, controls, and capture |
| 17 | `testcase17_Camera_VAAPI_Pipeline.py`    | Camera/video | Camera-to-VA-API H.264 pipeline |
| 18 | `testcase18_NPU_TOPS.py`                 | NPU/XDNA | ONNX/XDNA TOPS benchmark hook |
| 19 | `testcase19_NPU_Inference.py`            | NPU/XDNA | ONNX latency and throughput |
| 20 | `testcase20_NPU_Power_Efficiency.py`     | NPU/XDNA | Inference power and GOPS/W collection |
| 21 | `testcase21_DRAM_Read_Bandwidth.py`     | DDR5/LPDDR5 | STREAM, MBW, and sysbench read bandwidth |
| 22 | `testcase22_DRAM_Write_Copy.py`         | DDR5/LPDDR5 | Write/copy bandwidth and NUMA information |
| 23 | `testcase23_DRAM_Access_Latency.py`    | DDR5/LPDDR5 | Pointer-chase and memory access latency |

## Running tests

Run from the project directory:

```bash
cd ~/Documents/AMD-Linux/AMD_PnP_LINUX_Project
python3 testcase10_GPU_Compute.py
python3 testcase11_H264_HW_Encode.py
python3 testcase12_H265_HEVC_Encode.py
python3 testcase13_AV1_Encode.py
python3 testcase14_Video_Decode_test.py
python3 testcase15_USB_Camera_Capture.py
python3 testcase16_AMD_ISP_Pipeline.py
python3 testcase17_Camera_VAAPI_Pipeline.py
python3 testcase18_NPU_TOPS.py
python3 testcase19_NPU_Inference.py
python3 testcase20_NPU_Power_Efficiency.py
python3 testcase21_DRAM_Read_Bandwidth.py
python3 testcase22_DRAM_Write_Copy.py
python3 testcase23_DRAM_Access_Latency.py
```

CPU frequency and power tests may require elevated privileges:

```bash
sudo python3 testcase1_PstateScaling.py
sudo python3 testcase6_CPU_Power_Energy.py
```

Inspect results with:

```bash
ls Logs/
less Logs/video_decode_log.txt
```

Logs are append-only. Each run has a timestamped section containing command
output, errors, and nonzero exit codes.

## Camera configuration

```bash
CAMERA_DEVICE=/dev/video0
CAMERA_FORMATS=mjpeg,yuyv422
CAMERA_RESOLUTIONS=640x480,1280x720,1920x1080
MEDIA_DEVICE=/dev/media0
ISP_DEVICE=/dev/video2
VAAPI_DEVICE=/dev/dri/renderD128
```

Example:

```bash
CAMERA_DEVICE=/dev/video0 \
CAMERA_RESOLUTIONS=1280x720,1920x1080 \
python3 testcase15_USB_Camera_Capture.py
```

## NPU configuration

NPU tests require a local ONNX model and an installed execution provider. They
do not invent TOPS, latency, or power values when hardware or models are
missing.

```bash
export NPU_MODEL=/path/to/model.onnx
export NPU_PROVIDER=AmdMIGraphXExecutionProvider
export NPU_BENCHMARK=benchmark_npu.py

python3 testcase18_NPU_TOPS.py
python3 testcase19_NPU_Inference.py
python3 testcase20_NPU_Power_Efficiency.py
```

## Dependencies

Common tools include Python 3, `cpupower`, `sysbench`, `turbostat`,
`vulkaninfo`, `vkmark`, `vainfo`, `ffmpeg`, VA-API drivers, `v4l2-ctl`,
`media-ctl`, `libcamera-still`, a UVC camera, ONNX Runtime, and an AMD
execution provider. Install only the tools required by the tests you run.

Hardware support depends on the kernel, firmware, drivers, camera, model, and
execution provider. Missing capabilities are logged as unavailable or pending
rather than reported as successful measurements.

## Memory benchmark configuration

Build STREAM separately with an array size at least three times larger than
the last-level cache, then point the tests to the executable:

```bash
gcc -O3 -fopenmp stream.c -o stream_c.exe
STREAM_BINARY=./stream_c.exe python3 testcase21_DRAM_Read_Bandwidth.py
STREAM_BINARY=./stream_c.exe python3 testcase22_DRAM_Write_Copy.py
LAT_MEM_RD=/path/to/lat_mem_rd python3 testcase23_DRAM_Access_Latency.py
```

Optional variables include `MBW_SIZE_MB`, `SYSBENCH_MEMORY_SIZE`,
`LAT_MEM_RD`, and `STREAM_BINARY`. The scripts do not infer dual-channel mode
or fabricate bandwidth/latency values when the benchmark or firmware topology
data is unavailable.