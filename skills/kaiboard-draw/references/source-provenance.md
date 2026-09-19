# Provenance / 溯源

| 项 | 内容 |
|---|---|
| 交付物 | `kaiboard-draw`（本仓官方 skill） |
| 类别 | 自研 + 引用上游 |
| 上游 / 来源 | 生成逻辑基于 Excalidraw 的元素 schema（自研实现）；预览渲染使用 roughjs（Excalidraw 同款手绘引擎）；素材检索对接 excalidraw 官方社区库 `excalidraw-libraries`。 |
| 上游地址 | Excalidraw — https://github.com/excalidraw/excalidraw ｜ roughjs — https://github.com/rough-stuff/rough ｜ 社区素材库 — https://github.com/excalidraw/excalidraw-libraries |
| 许可 | 本仓 MIT；上游均为宽松开源许可（MIT/Apache 类）。 |
| 核对方式 | 上游地址与许可在每次涉及相关改动时复核 |

> 说明：本仓**不重新分发**任何第三方素材库文件；素材按需从上游官方库获取。
