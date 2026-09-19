# Credits / 致谢

**English** | [简体中文](#简体中文)

---

## English

This repository stands on the work of others. Our thanks to everyone below.

### Ecosystem & specifications

| Project | What we use it for |
|---|---|
| [Excalidraw](https://github.com/excalidraw/excalidraw) (MIT) | Element schema and `.excalidraw` file format — the contract both collaboration modes converge on. We implement against the schema; we are not a fork. |
| [excalidraw-libraries](https://github.com/excalidraw/excalidraw-libraries) (MIT) | The official community icon-library index. Asset-aware composition searches and fetches from here on demand. |
| [roughjs](https://github.com/rough-stuff/rough) (MIT) | Hand-drawn rendering engine — the same one Excalidraw uses. Powers true-to-canvas SVG previews. |
| [Agent Skills](https://agentskills.io) specification | The `SKILL.md` + progressive-disclosure format this skill follows. |
| [Agent Plugins](https://agent-plugins.org) specification | The `plugin.json` + `mcp.json` manifest format that lets one repo ship a skill and its companion MCP server together. |
| [Model Context Protocol](https://modelcontextprotocol.io) | The tool protocol the companion MCP server implements. |

### Diagramming methodology

Our drawing methodology distils publicly available Excalidraw drawing skills and tutorials. We learned from:

| Source | What we adopted |
|---|---|
| [robonuggets/excalidraw-skill](https://github.com/robonuggets/excalidraw-skill) | Ten visual techniques, screenshot self-review, quality checklist, arrow binding / `fixedPoint` / `focus` |
| `authoring-excalidraw-files` (indiosmo/skills) | Multi-arrow stagger formula, `fixedPoint` reference table, common-mistake table |
| `acking-you/excalidraw` | Cross-over risk decision tree, per-arrow walkthrough before finishing |
| `excalidraw-3` / `skill4agent` | Loop and hub layouts (triangle / diamond / 2×2), container binding, background sizing |
| [neversight feed-excalidraw-skill](https://lobehub.com/skills/neversight-skills_feed-excalidraw) | Route-mode selection (straight / L / U / curve / elbow), "never accept crossing arrows", screenshot self-review loop |
| `toxigon` Excalidraw tips | `sloppiness` tiers, stroke matching arrowheads, 2–3 colour discipline, 50%-zoom composition check |
| `ai-bar` Excalidraw guide | Component grouping and reuse, annotation text boxes |
| [C4 model](https://c4model.com) (Simon Brown) | Layering architecture diagrams by audience (Context / Container / Component / Code) |

> Entries without a link are public articles or skill-directory pages we drew on at the time; linked entries are directly traceable. If you are the author of any entry here and would prefer different attribution, please open an Issue.

### Third-party assets

Community icon libraries are the property of their respective authors and carry their own licences. **This repository does not redistribute them** — they are fetched on demand from the upstream official index.

---

## 简体中文

本仓站在他人工作之上。感谢以下每一位。

### 生态与规范

| 项目 | 我们用它做什么 |
|---|---|
| [Excalidraw](https://github.com/excalidraw/excalidraw)（MIT） | 元素 schema 与 `.excalidraw` 文件格式 —— 两种协作模式共同收敛的契约。我们按其 schema 实现，并非 fork。 |
| [excalidraw-libraries](https://github.com/excalidraw/excalidraw-libraries)（MIT） | 官方社区图标库索引。素材感知构图从这里按需检索与取件。 |
| [roughjs](https://github.com/rough-stuff/rough)（MIT） | 手绘渲染引擎 —— Excalidraw 内部同一套。用于生成与画布一致的 SVG 预览。 |
| [Agent Skills](https://agentskills.io) 规范 | 本 skill 遵循的 `SKILL.md` + 渐进披露格式。 |
| [Agent Plugins](https://agent-plugins.org) 规范 | `plugin.json` + `mcp.json` 清单格式，让一个仓库同时交付 skill 与配套 MCP 服务端。 |
| [Model Context Protocol](https://modelcontextprotocol.io) | 配套 MCP 服务端实现的工具协议。 |

### 画图方法论

本仓的画图方法论提炼自公开的 Excalidraw 画图 skill 与教程，借鉴来源：

| 来源 | 借鉴内容 |
|---|---|
| [robonuggets/excalidraw-skill](https://github.com/robonuggets/excalidraw-skill) | 十条视觉技法、截图自纠、质量清单、箭头 `binding` / `fixedPoint` / `focus` |
| `authoring-excalidraw-files`（indiosmo/skills） | 同边多箭头 stagger 公式、`fixedPoint` 取值表、常见错误表 |
| `acking-you/excalidraw` | 交叉风险预判决策树、收尾前逐箭头走查 |
| `excalidraw-3` / `skill4agent` | 回环与枢纽布局（三角 / 菱形 / 2×2）、容器绑定、背景尺寸 |
| [neversight feed-excalidraw-skill](https://lobehub.com/skills/neversight-skills_feed-excalidraw) | 路由模式选型（直行 / L / U / 曲线 / 肘线）、「绝不接受交叉箭头」、截图自纠闭环 |
| `toxigon` Excalidraw 技巧 | `sloppiness` 档位、描边匹配箭头、2–3 主色纪律、缩到 50% 自检构图 |
| `ai-bar` Excalidraw 指南 | 组件分组复用、标注文本框 |
| [C4 模型](https://c4model.com)（Simon Brown） | 架构图按受众分层（Context / Container / Component / Code） |

> 上表中未能给出链接的条目，是我们接触时依据的公开文章或 skill 目录页；有链接者可直接溯源。若你是其中某条目的作者并希望调整署名方式，欢迎提 Issue。

### 第三方资产

社区图标库属各自作者所有、各有其许可。**本仓不重新分发**这些文件 —— 一律按需从上游官方索引获取。
