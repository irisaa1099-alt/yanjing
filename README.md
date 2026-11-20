# 研镜

研镜是本地运行的文献研究工作台，支持论文检索、PDF 阅读和批注、语义筛选、文献对比与证据回看。这个仓库保存 2026 年 11 月 20 日的完整发行包，包含当时的论文库、附件与历史任务、运行环境、Qwen3 4B 本地模型、项目报告和演示视频。

## 下载

登录有访问权限的 GitHub 账号，打开[完整发行包](https://github.com/irisaa1099-alt/yanjing/releases/tag/2026.11.20)，从 Assets 下载所用平台的全部分卷和合并脚本，放在同一个文件夹中。

| 平台 | 所需分卷 | 合并方法 | 解压后的启动入口 |
| --- | --- | --- | --- |
| Windows 10/11，Intel 或 AMD x64 | Yanjing-Windows-x64.zip.001 至 .009 | 双击 Yanjing-Windows-x64-merge.cmd | 在本地 NTFS 磁盘完整解压，双击「启动研镜.bat」 |
| Apple 芯片 Mac | Yanjing-macOS-arm64.zip.001 至 .006 | 在下载目录打开终端，执行 `bash Yanjing-macOS-arm64-merge.command` | 完整解压，双击「启动研镜.command」 |

合并脚本会生成 ZIP 并自动验证 SHA-256。Windows ZIP 为 4.37 GB，解压后约 5.11 GB。Mac ZIP 为 3.04 GB，解压后约 3.75 GB。保留分卷、合并出的 ZIP 和解压目录时，请为三份文件预留空间。应用首次启动会恢复数据库并打开浏览器，默认地址为 `http://127.0.0.1:18765`。

已安装并登录 GitHub CLI 的用户也可以在空目录运行对应命令，一次下载所用平台的全部文件。

**Windows**

```sh
gh release download 2026.11.20 --repo irisaa1099-alt/yanjing --pattern "Yanjing-Windows-x64*"
```

**macOS**

```sh
gh release download 2026.11.20 --repo irisaa1099-alt/yanjing --pattern "Yanjing-macOS-arm64*"
```

## 发行内容

两个平台使用相同的数据快照，含 2 个论文库、2,180 条当前题录、7 个语料版本、6 份 PDF、28 次语义查询和 6 个对比任务。本地模型可离线使用，云端模型需自行配置 API Key。压缩包内另附使用说明。
