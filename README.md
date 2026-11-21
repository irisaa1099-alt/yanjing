# 研镜

研镜是本地运行的文献研究工作台，支持论文检索、PDF 阅读和批注、语义筛选、文献对比与证据回看。发行包使用 2026 年 11 月 20 日的快照，包含当时的论文库、附件与历史任务、运行环境、Qwen3 4B 本地模型、项目报告和演示视频。

## 下载

打开下表中对应平台的发行页，从 Assets 下载全部分卷和同页的合并脚本，放在同一个新文件夹中。

| 平台 | 所需分卷 | 合并方法 | 解压后的启动入口 |
| --- | --- | --- | --- |
| [Windows x64 · 原生权限修复版](https://github.com/irisaa1099-alt/yanjing/releases/latest) | Yanjing-Windows-x64.zip.001 至 .009 | 双击 Yanjing-Windows-x64-merge.cmd | 在可写的本地 NTFS 中文或英文目录完整解压，双击「启动研镜.bat」 |
| [Apple 芯片 Mac · 稳定性修复版](https://github.com/irisaa1099-alt/yanjing/releases/latest) | Yanjing-macOS-arm64.zip.001 至 .006 | 在下载目录打开终端，执行 `bash Yanjing-macOS-arm64-merge.command` | 完整解压，双击「启动研镜.command」 |

合并脚本会生成 ZIP 并自动验证 SHA-256。Windows ZIP 为 4.37 GB，解压后约 5.11 GB。Mac ZIP 为 3.04 GB，解压后约 3.75 GB。保留分卷、合并出的 ZIP 和解压目录时，请为三份文件预留空间。应用首次启动会恢复数据库并打开浏览器，默认地址为 `http://127.0.0.1:18765`。

已安装并登录 GitHub CLI 的用户也可以在空目录运行对应命令，一次下载所用平台的全部文件。

**Windows**

```sh
gh release download 2026.11.21-stable --repo irisaa1099-alt/yanjing --pattern "Yanjing-Windows-x64*"
```

**macOS**

```sh
gh release download 2026.11.21-stable --repo irisaa1099-alt/yanjing --pattern "Yanjing-macOS-arm64*"
```

## 启动与已有数据

首次建库中断后，从原目录双击启动文件即可重试。正常退出请在启动窗口按 Ctrl+C，待数据库关闭后再移动整个目录。Windows 支持含中文及空格的可写本地 NTFS 目录。已有个人论文库时，请先备份整个旧目录，将新版解压到另一处。Windows 原生权限修复版已在 Windows Server 2022 x64 的管理员和普通用户环境验证。测试覆盖首次建库、中断后重试、本地模型筛选、文献对比与退出后重启。升级请使用完整包。仓库的 `windows/` 目录记录的是早期中文路径补丁。

## 发行内容

两个平台使用相同的数据快照，含 2 个论文库、2,180 条当前题录、7 个语料版本、6 份 PDF、28 次语义查询和 6 个对比任务。本地模型可离线使用，云端模型需自行配置 API Key。压缩包内另附使用说明。
