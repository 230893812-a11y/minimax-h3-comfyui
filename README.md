# MiniMax H3 ComfyUI 部署与诊断 Skill

让 Codex 按可复用的流程协助你检查 MiniMax H3 环境、核对模型文件、选择工作流，并排查生成失败的问题。适合本地部署新手，也适合帮助别人排错的维护者。

项目包含操作说明、Python/PowerShell 检查脚本和工作流 JSON，不包含模型权重、账号凭据或私人日志。安装 Skill 只复制项目文件，不会自动安装 ComfyUI、下载模型或配置显卡驱动。

## 功能概览

| 场景 | 当前能力 |
| --- | --- |
| 不知道模型放在哪里 | 模型目录说明和文件清单 |
| 不确定文件是否完整 | 检查文件存在性、大小和清单中配置的 SHA-256 |
| ComfyUI 启动报错 | 日志排查流程，包括 comfy-kitchen 依赖问题 |
| 不知道选什么工作流 | T2V、I2V、R2V、视频续接模板和说明 |
| 想整理环境信息 | 报告操作系统、脚本 Python、磁盘空间、NVIDIA GPU 和显存 |
| 想检查生成结果 | 读取视频时长、分辨率、帧率和音视频流信息 |

这些工具以检查和报告为主，不会自动修复所有错误。环境检查暂不核对全部驱动、PyTorch、CUDA/ROCm 或 ComfyUI 依赖版本。

## 快速安装

### 1. 下载并进入项目目录

在 GitHub 页面点击 **Code → Download ZIP**，解压后进入包含 README.md 和 SKILL.md 的文件夹。熟悉 Git 的用户可以运行：

~~~powershell
git clone https://github.com/230893812-a11y/minimax-h3-comfyui.git
cd minimax-h3-comfyui
~~~

### 2. 安装 Skill（Windows）

在项目文件夹中打开 PowerShell：

~~~powershell
.\install.ps1
~~~

设置 CODEX_HOME 时，安装位置为该目录下的 skills/minimax-h3-comfyui；否则为当前用户目录下的 .codex/skills/minimax-h3-comfyui。已有安装中的同名文件会被覆盖更新，请先保存自定义修改。

如果执行策略阻止脚本运行，可以手动复制项目到上述位置。目标文件夹应命名为 minimax-h3-comfyui，SKILL.md 直接位于其根目录，不要再多套一层文件夹。

### 3. 检查文件并调用

以下命令检查当前项目目录的必要文件是否齐全，不检查 Codex 是否已加载 Skill：

~~~powershell
.\verify-install.ps1
~~~

安装后重新打开 Codex 或开始新聊天，输入：

~~~text
使用 $minimax-h3-comfyui 检查我的 MiniMax H3 部署环境。
先读取现有配置，列出缺失项，再执行必要的修复。
~~~

更多使用示例：

~~~text
使用 $minimax-h3-comfyui 检查模型是否完整，已有正确文件不要重复下载。
~~~

~~~text
使用 $minimax-h3-comfyui 排查 ComfyUI 启动时报 comfy_kitchen 缺少属性的问题。
~~~

~~~text
使用 $minimax-h3-comfyui 帮我选择图生视频工作流，并核对输入素材和模型配置。
~~~

## 单独运行脚本

不安装 Skill 也可以使用脚本。建议 Python 3.12（项目当前测试环境），先运行 python --version 确认解释器。脚本使用 Python 标准库；视频检查还需要安装 FFmpeg，并使 ffprobe 位于 PATH。

以下命令均在项目根目录执行，路径是示例，请替换为自己的路径。

### 环境检查

~~~powershell
python scripts/check_environment.py --comfyui "D:/ComfyUI" --json
~~~

输出操作系统、当前脚本的 Python、指定目录、磁盘剩余空间，以及 nvidia-smi 返回的 NVIDIA GPU 名称和显存。脚本 Python 不一定是 ComfyUI 使用的 Python。使用 AMD 或缺少 NVIDIA 工具时，字段可能显示 unavailable，不能据此断定 GPU 不可用。

### 模型完整性检查

~~~powershell
python scripts/check_models.py --root "D:/ComfyUI-Shared" --manifest examples/models.comfy-org-minimax-h3.json
~~~

--root 是包含 models 文件夹的目录，不是 models 文件夹本身。脚本相对于它查找清单中的 models/vae/example.safetensors 等路径。

| 状态 | 含义 |
| --- | --- |
| OK | 通过清单实际配置的检查项 |
| MISSING | 文件不存在 |
| SIZE_MISMATCH | 文件大小不符 |
| HASH_MISMATCH | SHA-256 不符 |
| RESULT PASS / FAIL | 整体结果；失败退出码为 1 |

哈希为空时不会计算 SHA-256，所以 OK 不一定代表通过哈希校验。大模型检查需读取完整文件，可能耗时较长。当前脚本不会扫描或清理下载残留。

### 视频信息检查

~~~powershell
python scripts/check_output.py "D:/ComfyUI-Shared/output/video/example.mp4"
~~~

输出时长、分辨率、帧率和音视频流。ffprobe 缺失时退出码为 2，探测失败时为 1。它不会评价画面和声音质量，也不能替代完整播放或逐帧解码。

### 综合诊断

~~~powershell
python scripts/diagnose.py --comfyui "D:/ComfyUI" --models "D:/ComfyUI-Shared" --manifest examples/models.comfy-org-minimax-h3.json --output "D:/ComfyUI-Shared/output" --json
~~~

报告打印到终端，包含环境、模型和输出目录信息。当前媒体文件按路径排序选择，并非按修改时间寻找最新文件；检查指定成片时请直接使用 check_output.py。

报告可能保留完整目录路径，目前没有自动脱敏。公开分享前先检查用户名、私人路径等内容。综合诊断退出码主要反映模型检查结果，不能代表所有环境和媒体检查成功。

## 模型清单与目录

~~~text
ComfyUI-Shared/
└─ models/
   ├─ diffusion_models/  主扩散模型
   ├─ text_encoders/     文本编码器
   ├─ vae/               音频和视频 VAE
   └─ loras/             可选 LoRA
~~~

| 清单 | 用途 |
| --- | --- |
| [Comfy-Org H3 清单](examples/models.comfy-org-minimax-h3.json) | 文件名、大小、来源和部分哈希；包含 Turbo LoRA，按所选工作流调整检查项 |
| [自定义模板](examples/models.template.json) | 为其他版本填写路径、大小和可信哈希 |
| [社区 Heretic 示例](examples/models.community-heretic.json) | 未验证编码器示例，没有可靠大小和哈希，不能作为完整性认证 |

正式清单前四个文件配置了 SHA-256，Turbo LoRA 目前仅配置大小。清单提供来源信息，不会自动下载模型。不要仅凭大小相近认定两个模型版本相同。

## 工作流选择

| 类型 | 用途 | 文件 |
| --- | --- | --- |
| T2V | 根据文字描述生成视频 | [t2v-standard.json](workflows/t2v-standard.json) |
| I2V | 从输入图片生成运动画面 | [i2v-standard.json](workflows/i2v-standard.json) |
| R2V | 使用参考素材生成视频 | [r2v-standard.json](workflows/r2v-standard.json) |
| 视频续接 | 延续已有内容 | [i2v-continuation.json](workflows/i2v-continuation.json) |

在 ComfyUI 中打开 JSON，处理缺失节点和模型提示，选择本机模型，再配置提示词与输入素材。模板不是针对所有显卡优化的低显存配置，也未在本项目逐一完成生成测试。来源见 [工作流说明](workflows/README.md)。

## 硬件与验证范围

项目记录了一次 Windows 11、RTX 5060 Laptop 8 GB 的实测：864 × 480、约 5 秒、20 步、带音轨。它是参考案例，不代表所有 8 GB 显卡都能稳定运行，也不代表模型最长只能生成 5 秒。

更长时长、更高分辨率和不同量化格式可能显著增加显存与系统内存需求。AMD/ROCm 尚未在本项目实测，不应直接套用 NVIDIA CUDA/NVFP4 配置。

详见 [兼容记录](COMPATIBILITY.md)、[硬件参考](references/hardware-matrix.md)和[工作流选择](references/workflows.md)。

## 遇到问题

先阅读 [常见错误排查](references/troubleshooting.md)。提交 Issue 时建议提供：

- 操作系统、GPU、显存和系统内存。
- ComfyUI 版本或提交号、实际 Python 环境。
- 工作流、分辨率、时长和步数。
- 复现步骤、报错结尾和检查脚本结果。

公开前先脱敏，不上传模型权重、Token、密码或完整私人日志。不能只凭“跑到一半停了”判断显存不足，应结合实际报错定位。

## 更新与卸载

获取新版本后可再次运行安装脚本更新同名文件。卸载只删除目标 Skill 文件夹，不删除 ComfyUI 或模型；先保存安装目录里自行添加的内容。

~~~powershell
.\uninstall.ps1
~~~

## 开源与许可

本项目自己的代码和文档按 [LICENSE](LICENSE) 提供。模型和复制的第三方工作流受各自上游许可约束，不能因本项目采用 MIT 就推定它们也采用 MIT。工作流来源与许可核实记录仍需补齐。

贡献前阅读 [CONTRIBUTING.md](CONTRIBUTING.md)，版本变化见 [CHANGELOG.md](CHANGELOG.md)。欢迎提供可复现的问题报告和附带环境记录的硬件实测结果。
