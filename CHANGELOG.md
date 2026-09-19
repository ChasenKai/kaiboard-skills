# Changelog

> 对外版本记录 / Public version history.
> 格式遵循 [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)；版本号遵循 [语义化版本](https://semver.org/spec/v2.0.0.html)。

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
