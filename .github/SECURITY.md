# Security Policy / 安全政策

## 支持的版本 / Supported versions

| 版本 / Version | 是否支持 / Supported |
|---|---|
| 最新的 `0.x` / latest `0.x` | ✅ |
| 更早版本 / Earlier versions | ❌ 请先升级到最新版 / please upgrade first |

## 报告漏洞 / Reporting a vulnerability

**请不要通过公开 issue 报告安全问题。**
**Please do not report security issues through a public issue.**

请使用 GitHub 的私密漏洞报告功能 / Use GitHub's private vulnerability reporting:

1. 打开本仓的 **Security** 标签页 / Open this repo's **Security** tab
2. 点击 **Report a vulnerability** / Click **Report a vulnerability**
3. 填写复现步骤与影响说明 / Describe reproduction steps and impact

若无法使用该功能，也可以开一个**不含任何敏感细节**的 issue，说明希望建立私密联系渠道。
If you cannot use that feature, open an issue **without any sensitive detail** asking for a private channel.

## 我们会怎么做 / What we will do

- 收到报告后尽快确认并给出初步判断 / Acknowledge and give an initial assessment as soon as possible
- 修复发布前与你同步进展 / Keep you updated before a fix ships
- 修复发布后，如你同意，在发布说明中致谢 / Credit you in the release notes if you agree

## 范围说明 / Scope

本仓是一组 **Agent Skill（提示词 + 本地辅助脚本）**，不含服务端、不上传任何数据。主要攻击面：

This repo is a set of **Agent Skills (prompts + local helper scripts)**. It has no server and uploads no data. Main attack surfaces:

| 面 / Surface | 说明 / Notes |
|---|---|
| **本地辅助脚本** / Local helper scripts | `scripts/` 下的脚本会在你本机以你的权限运行 / run locally with your privileges |
| **MCP 令牌** / MCP token | 实时共绘需要令牌，令牌泄露等同于该会话被接管 / live co-draw needs a token; a leaked token means that session can be driven |
| **网络行为** / Network behaviour | 仅「素材库在线检索」会访问网络；画布数据始终留在本机 / only the asset-library lookup goes online; canvas data never leaves your machine |
| **第三方素材库** / Third-party libraries | 按需获取的社区图标库是第三方作品，各有其许可 / community icon libraries are third-party works under their own licenses |

不在范围内 / Out of scope：上游依赖自身的漏洞（请向对应项目报告，我们会在收到通知后跟进升级）。
Vulnerabilities in upstream dependencies (report to the respective project; we will follow up on upgrades).

## 相关 / See also

- 安全边界要点见 [`skills/kaiboard-draw/SKILL.md`](../skills/kaiboard-draw/SKILL.md) §安全边界
- 完整依赖与许可清单见 [`CREDITS.md`](../CREDITS.md)
