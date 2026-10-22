# RTX 4060 Laptop 8 GB：安装与工作流排错记录

记录日期：2026-10-22。以下来自一次实际部署；只证明该配置的一次生成成功，不构成通用最低配置或性能承诺。未公开用户提示词、原始日志、模型权重或生成媒体。

## 环境与验证范围

| 项目 | 实际值 |
|---|---|
| 系统 | Windows 11 64 位，10.0.26100 |
| 显卡 | RTX 4060 Laptop，nvidia-smi 报告 8188 MiB 显存 |
| 系统内存 | 约 16 GB |
| NVIDIA 驱动 | 566.26 |
| ComfyUI | 0.42.1，提交 63be2f9b82ad0dac88a7ceaa28a9cf3154125a18 |
| 发行包 | ComfyUI_windows_portable_nvidia_cu126.7z |
| 实际解释器 | 便携版自带 Python 3.12.10 |
| PyTorch / CUDA runtime | 2.14.0+cu126 / 12.6 |
| comfy-kitchen | 0.2.39 |
| 工作流起点 | 本项目 workflows/t2v-standard.json |

系统另装的 Python 3.15 没有参与 ComfyUI 运行。nvidia-smi 的 CUDA Version 是驱动所支持的版本信息，不代表 PyTorch 实际使用的 CUDA runtime。Windows Win32_VideoController 在本机报告了不准确的 4 GB 显存，应交叉核对 nvidia-smi 的 memory.total。

主模型为 `minimax_h3_fl2va_pruned_int8_convrot.safetensors`；视频 VAE 为 `minimax_h3_video_vae_fp16.safetensors`，音频 VAE 为 `minimax_h3_audio_vae_fp32.safetensors`。

文本编码器是用户自行下载的 `qwen3vl_32b_heretic_minimax_h3_nvfp4.safetensors`，大小为 15,683,129,587 字节。该文件的来源、许可和权威校验值未在本次记录中验证；仅检查了 safetensors 文件头与数据区长度，并观察到本机加载和生成成功。不能用此文件名或大小为其他下载提供完整性认证，也不据此推荐第三方变体。

## 可复现的工作流配置错误

错误流程将 H3 UNET 接入 `ModelSamplingAuraFlow`，使用 `EmptySD3LatentImage`、普通图像采样/保存流程，并把 H3 音频 VAE 用作图像解码；CLIPLoader 类型仍为 `lumina2`。

本机执行时在 KSampler 中出现：

```text
AttributeError: 'ModelSamplingAdvanced' object has no attribute 'audio_scale'
```

相关调用位置为 `comfy/model_base.py` 的 `extra_conds` -> `audio_scale`，最终访问 `self.model_sampling.audio_scale`。本次错误流程和 traceback 已由执行历史及日志确认，没有为复现而再次提交同一失败任务。

此组合中的问题应整体处理，不能仅给对象补一个属性，也不能仅将 CLIPLoader 改成 minimax 后继续沿用 SD3 图像工作流。

处理步骤：

1. 导入本项目的 `workflows/t2v-standard.json`，保留 H3 专用 latent、采样、音视频解码与保存连接，去掉手工拼接的 AuraFlow/SD3 图像流程。
2. 把文本编码器放入实际已配置的 `models/text_encoders`，CLIPLoader 类型设为 `minimax`。仅改文件名不会自动更改类型。
3. 分别选择视频 VAE 和音频 VAE；用 CreateVideo / SaveVideo 输出视频。
4. 本次起始参数为 16:9、0.2 百万像素、multiple=32，即 608×352；duration=2 秒；标准模式 20 步，turbo_mode=false，batch=1。Turbo LoRA 虽存在，但该次标准模式没有启用它。
5. 如模板含子图，应同时检查顶层暴露的 clip_name 和内部 CLIPLoader；子图 UUID 不能直接当作缺失的后端节点。

模板节点显示 Image to Video 并不要求必须输入图片；此模板的 first_frame 和 last_frame 是可选输入，留空可进行文生视频。

## 已确认的结果与限制

- `/system_stats` 可用，Python/PyTorch CUDA 张量运算测试通过；`/object_info` 能列出所选模型与所需节点。
- ComfyUI 历史记录有一次 `status_str=success`、`completed=true`；从 execution_start 到 execution_success 约 432.6 秒（约 7.2 分钟）。这只是该次墙钟耗时，包含缓存状态等影响，不能作为通用速度基准。
- MP4 大小为 479,023 字节；容器报告约 2.333 秒，视频为 H.264、608×352，音频为 AAC。
- 使用便携环境中的 PyAV 对整个容器解码，得到 56 个视频帧、73 个音频帧，未发生解码错误。音频帧数不是音频采样数。
- 尚未进行画面、声音质量评价；未验证更高分辨率、更长时长或持续多次生成的稳定性。

请求的 2 秒与实际输出时长有差异：模板会按 H3 的有效帧数网格取整。应以最终媒体时长为准。

启动时还有 CUDA 优化操作需要 cu130 或更高版本的提示。本次 cu126 环境仍能完成上述生成；这不表示所有量化格式或优化后端都可用，也不能只因提示就替用户升级系统驱动。16 GB 系统内存需要承担大模型卸载压力，应保留充足磁盘空间并逐次观测耗时和内存。

## 下载与目录经验

- 使用便携发行包可避免与系统 Python 混用。本次 CUDA 12.6 包的 GPU 运算已实际验证；不应笼统地要求所有用户安装同一 CUDA 版本。
- 通过 `extra_model_paths.yaml` 引用共享模型目录，避免把几十 GB 权重再复制一份。使用绝对 base_path，并配置 diffusion_models、text_encoders、vae、loras 四类。
- 同一 NTFS 卷上的现有模型可使用硬链接，但两个路径指向同一数据，不能把其中一个当独立备份；不适用时再选择复制或受控移动。
- curl 断点续传使用 `.part` 文件，成功后先校验大小和可信 SHA-256，再改为最终文件名。本次主模型、两份 VAE、LoRA 及便携包均通过其下载元数据中的 SHA-256 校验。第三方编码器不包含在此校验结论中。
- 官方下载站连接失败属于网络问题。若使用镜像，应明确其第三方性质；发布包校验值与模型 LFS SHA-256 应从可信上游核对。不要把下载成功视为运行成功。
- GitHub 发布页连接超时但 API 可用时，可以使用官方 release asset API，带 `Accept: application/octet-stream`，并跟随重定向；应核对响应不是 JSON/HTML，再验证发行包哈希。

## 排错结论

本例的关键修复是选用正确的 H3 工作流，而非改动 ComfyUI 核心代码或补装随机依赖。硬件结论必须分级：下载完成、GPU 运算通过、工作流加载、生成完成、媒体解码通过、质量评价是不同阶段。
