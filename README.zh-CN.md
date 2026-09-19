# KaiBoard Skills

[English](./README.md) | **简体中文**

[KaiBoard](https://kaiboard.kaibuddy.com) 的官方技能集合 —— KaiBoard 是一个基于 Excalidraw 的**本地优先**开源白板。

这些技能教会 AI Agent **如何在你的 KaiBoard 白板上作图**：两条协作路径该走哪条、图怎么画得好、元素如何安全落板。

> ⚠️ **使用现状（请先读）**
> - **目标**：任何支持 Agent Skills 与 MCP 的客户端都能用。
> - **实际验证情况**：目前主要在 **WorkBuddy** 上验证过。**其他客户端请自行验证与调教** —— 不同客户端的工具暴露方式、连接方式可能不同，属正常。
> - **阶段**：属**早期 / 预览版**，接口与内容可能变化，暂不建议用于关键流程。
> - **问题与建议**：欢迎提 Issue。我们**不会**把尚未验证的客户端说成"已支持"。

## 包含什么

| 技能 | 作用 |
|---|---|
| [`kaiboard-draw`](./skills/kaiboard-draw/) | 在 KaiBoard 上作图。**实时共绘**（直接驱动你已经打开的画布）或**出文件**（生成可编辑的 `.excalidraw`，稍后导入）。 |

## 安装

### 方式 A —— 复制技能目录

任何支持 [Agent Skills](https://agentskills.io) 规范的 Agent 都能加载。克隆后把技能目录放到你的 Agent 查找技能的位置：

```bash
git clone https://github.com/ChasenKai/kaiboard-skills.git
cp -r kaiboard-skills/skills/kaiboard-draw ~/.claude/skills/     # 路径随客户端而异
```

### 方式 B —— 作为 Agent Plugin

本仓同时是一个 [Agent Plugin](https://agent-plugins.org)：根目录带 `plugin.json` 清单与 `mcp.json`。支持该格式的客户端，可以从**这一个仓库**同时发现**技能本身**和**配套的 MCP 服务端**。

配套 MCP 服务端是 [`@kaibuddy/kaiboard-mcp`](https://www.npmjs.com/package/@kaibuddy/kaiboard-mcp) —— 它直接与你在浏览器里打开的 KaiBoard 画板通信。

## 配置

实时共绘需要一个令牌，由 KaiBoard 为你生成：

1. 在浏览器中打开 KaiBoard，并打开你要操作的画板。
2. 打开设置，开启 **Agent 共绘**。
3. 复制面板上显示的令牌。

然后在 `mcp.json` 里填入（替换占位符）：

```json
"env": { "KAIBOARD_TOKEN": "<你的令牌>" }
```

> **凭据不随本仓分发。** 占位符是刻意的 —— 令牌属于你自己的机器与 KaiBoard 会话，不要写进公开文件或分享给他人。

> 📄 更细的分步设置与常见问题见 [`skills/kaiboard-draw/SETUP.md`](./skills/kaiboard-draw/SETUP.md)。

## 运行要求

- **实时共绘**：浏览器中打开 KaiBoard 并开启「Agent 共绘」，且配置好 MCP 服务端。Agent 与浏览器须在**同一台机器**上。
- **出文件**：无需连接 KaiBoard —— 你会得到一个 `.excalidraw` 文件，随时导入即可。
- 随附的辅助脚本需要 **Python 3**。
- **Node.js** + [`roughjs`](https://www.npmjs.com/package/roughjs)（`npm i roughjs`）—— 仅手绘风 SVG 预览需要。该预览是落板前的**强制**检查点，因此请按真实依赖对待，而非可选项。详见 [`skills/kaiboard-draw/SETUP.md`](./skills/kaiboard-draw/SETUP.md)。

## 贡献与维护

- 新发现先在工作分支验证；稳定后再提 PR，并按本仓 [语义化版本](./CHANGELOG.md) 发布。
- 修改 `skills/` 下的内容时，请同步检查 `references/` 内的相互引用是否仍然成立。

## 致谢

本仓站在他人工作之上 —— Excalidraw 的元素 schema 与社区素材库、roughjs 手绘渲染引擎，以及公开的 Agent Skills / Agent Plugins 规范。完整清单见 [CREDITS.md](./CREDITS.md)。

## 许可

[MIT](./LICENSE)。按需获取的社区图标库属第三方作品、各有其许可；本仓**不分发**它们的实体文件。
