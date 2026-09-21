# Changelog

> 对外版本记录 / Public version history.
> 格式遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)；版本号遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

---

## [0.2.0] - 2026-09-21 · 命令面扩充与边界说明

跟进 `kaiboard-mcp` `0.3.0`：补齐文件树管理命令的文档，并把"写死的清单"改为可自省的引用。

Follows `kaiboard-mcp` `0.3.0`: documents the new file-tree management commands, and replaces hard-coded lists with self-describing references.

### Added / 新增

- **命令表补齐至 14 个**：新增 `createFolder` / `renameBoard` / `renameFolder`，并补上此前缺失的 `deleteBoard` / `setMetadata`。
- **新增共同铁律：画板与文件夹的删除、新建边界** —— `deleteBoard` 不能删除"当前打开着的画板"（属设计约束，不是故障）；`createBoard` / `createFolder` 的父级必须是已存在的文件夹。并写明**遇到这类"预期内的拒绝"时如何向用户说明并给出下一步**。

  **New common rule on delete/create boundaries** — `deleteBoard` cannot remove the board that is currently open (a deliberate constraint, not a failure); parents must be existing folders. It also spells out how to explain such expected refusals to the user and offer a next step.

- **排错**：补充 `NO_BACKEND` 的成因与处置（既没起中继也没绑文件夹时会命中）。

### Changed / 变更

- **不再写死工具数量与清单**：改为"以 `kbfs_list_capabilities` 返回的 `commands` 为准" —— 命令集会随版本增减，写死必然漂移。
- **接入提醒的措辞**：改为先说清"是什么情况"，再给出两个可选做法（用户自己操作 / 让 Agent 代做）。

---
## [0.1.0] - 2026-09-18 · 首个公开发布版 / First public release

首个公开发布版本。`0.x` 表示 API 与内容在次版本之间仍可能变化。

First public release. `0.x` means the API and content may still change between minor versions.

### Added / 新增

- **`kaiboard-draw`** —— 在 KaiBoard 白板上作图：两条协作路径（实时共绘 / 生成可编辑 `.excalidraw`），共用同一份「合法 Excalidraw 元素」契约。

  **`kaiboard-draw`** — Draw on KaiBoard whiteboards: two paths (live co-draw / editable `.excalidraw` output) sharing one "valid Excalidraw element" contract.

- 广义画图方法论：构图、风格档位、箭头路由、标注、图类型→技法映射。

  A general diagramming methodology: composition, style tiers, arrow routing, annotation, diagram-type → technique mapping.

- 素材感知构图：在线检索社区素材库、按需取件，用现成矢量图标代替手搓矩形。

  Asset-aware composition: search community libraries online and fetch on demand, using ready-made vector icons instead of hand-drawn rectangles.

- 落板自检与几何校验工具，以及真实手绘风预览渲染。

  Landing self-check and geometry validation tooling, plus true hand-drawn-style preview rendering.

- 手绘风预览的前置依赖（Node.js + `roughjs`）现已写明 —— 该预览是落板前的强制检查点，属必备而非可选。

  The hand-drawn preview's prerequisites (Node.js + `roughjs`) are now documented — that preview is a mandatory checkpoint before landing, so it is a requirement rather than an optional extra.

- **Agent Plugins 清单**（`plugin.json` + `mcp.json`）：支持该格式的客户端可一次发现 skill 与配套 MCP 服务端。

  **Agent Plugins manifest** (`plugin.json` + `mcp.json`): clients implementing that format discover the skill and its companion MCP server in one go.

- **致谢清单**（`CREDITS.md`）：生态依赖、规范，以及画图方法论的公开借鉴来源。

  **Credits** (`CREDITS.md`): ecosystem dependencies, specifications, and the public sources our diagramming methodology draws on.

[0.1.0]: https://github.com/ChasenKai/kaiboard-skills/releases/tag/v0.1.0
