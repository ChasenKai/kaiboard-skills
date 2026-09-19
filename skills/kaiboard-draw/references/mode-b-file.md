# Mode B · 文件生成

> 本文件是 `kaiboard-draw` 的 Mode B 详细指引（从自然语言想法生成合法 `.excalidraw` 文件）。路由总览见主 SKILL.md。
> **广义画图方法论（风格档位 / 箭头路由 / 标注 / 构图 / 图类型→技法映射）见 `references/drawing-methodology.md`**——本文件只讲 Mode B 工作流，技法请以方法论总纲为准，两者互补。

# kaiboard-draw · Mode B

把用户的自然语言想法，生成一份**合法、可直接导入 KaiBoard**（也可在 Excalidraw 打开）的 `.excalidraw` 文件 —— Agent 出文件、你导入查看与继续编辑。

> 本 skill 的画图范围**不限于框架图**：草图、手绘插画、标注图解、线框、思维导图、视觉笔记都能生成。不同图型用不同技法（见方法论总纲第七节「图类型→技法映射」）。

## 什么时候用
- 用户要"画个草图 / 手绘 / 框图 / 流程图 / 架构图 / 标注插画 / 思维导图 / 概念图 / 把某结构或想法可视化"
- 用户要在 KaiBoard 里看一张图（Agent 出文件、用户导入看）
- 任何需要"想法 → Excalidraw 文件"的场景（结构图、教学图解、低保真线框、头脑风暴都算）

## 不用这个 skill 的情况
- 用户已在 KaiBoard 网页里手动画（无需生成文件）
- 需要的是 LaTeX / PPT / 网页原型（用别的 skill）
- 需要的是**文章配图 / 位图插画**（属专门插画工具的范畴，不是本 skill）

## 与其他作图产物的区别（避免混淆）
本 skill 产出的是**可编辑的矢量图表文件（.excalidraw）**，进白板后能继续改；**不是**位图插画。

| 你要的 | 该用什么 |
|---|---|
| 白板里能继续改的图（框图 / 流程 / 架构 / 草图 / 思维导图） | **本 skill** |
| 文章 / 帖子配图、位图插画、角色资产、故事板 | 专门的插画工具（产出 PNG，不可编辑） |
| HTML 原型 / 幻灯片 / 动画 | 专门的原型或设计工具 |

> 简记：**要「白板里能继续改的图」→ 用本 skill；要「配图 / 位图插画」→ 用专门的插画工具。**

## 工作流

### 第 0 步（强制）：先渲染「真实手绘预览」，人确认后再落板
**不要直接生成文件甩给用户，也不要给一张扁平的「结构示意」SVG。** 必须用 `render_preview.cjs` 把 `.excalidraw` 渲染成**真实手绘风 SVG**（roughjs = Excalidraw 同款手绘引擎，效果与画布内一致），连同 `.excalidraw` 一起在对话里给用户看，改到满意再落板。

```
node <skill_dir>/render_preview.cjs <图>.excalidraw          # 生成同名 .svg（手绘风，可预览）
```

**前置依赖**：本脚本需要 Node.js 与 [`roughjs`](https://www.npmjs.com/package/roughjs)。若报「需要 roughjs 才能渲染预览」，先安装：

```bash
npm i roughjs        # 在 skill 目录下安装，脚本会自动就近解析
```

理由：Agent **看不见**自己画的东西（画布无视觉回读），盲画质量不可控；而且**扁平结构 SVG 会严重误导判断**——用户以为"图就这样丑"，其实只是预览引擎没用手绘风。用 roughjs 渲染后，预览 = 画布内真实观感，坏图在进画布前就被拦掉。
> 原则：**能在对话里否决的，绝不带进画布。** 画布是资产，对话是草稿区。

⚠️ 预览只对「信息结构 + 手绘观感」负责，仍不对「像素级排版」负责（落板后由布局器/手绘抖动微调）。用户确认的是"该有哪些框、怎么连、谁重要、手绘风对不对"。

### 第 0.5 步（视觉技法）：对照通用方法论

**生成前先对照 `references/drawing-methodology.md` §视觉技法（10 条）** —— 那是**两种模式共用的通用画法**
（hachure 填充 / 绑定箭头 / 语义配色 / 字体层级 / 形状混合 / 线型语义 / 分组着色 / 留白 / 中文不溢出 / 截图自纠），
`scripts/gen_excalidraw.py` 已内置其中大部分。

### 第 1–3 步：生成
1. **Agent 想结构**：从用户描述里提炼 `boxes`（节点）和 `arrows`（连线）。每个 box 给一个 `id`、一个 `label`、以及一个网格位置（`col`/`row`）或显式 `x`/`y`。
2. **写 spec 文件**：把结构写成一个 Python 文件，定义 `scene` 字典（见下）。
3. **跑生成器**：
   ```
   python <skill_dir>/gen_excalidraw.py --spec <你的spec.py> --out <输出>.excalidraw
   ```

### 第 4 步：先选**表达通道**，再选**落板路径**（两个正交维度，别混为一谈）

**4a. 选通道——唯一判据是「这张图之后主要由谁改」**

| 之后谁改 | 选什么 | 理由 |
|---|---|---|
| **主要由 Agent 改**（用户只看） | **SVG 贴图** ✅ 完全够用 | 编辑权本就在对话里，"不可编辑"不构成问题 |
| **主要由用户手改 / 要融进手绘** | **Excalidraw JSON**（本 skill 主路径）或 **Mermaid** | 必须是原生图元才能双击改、绑箭头、同风格 |
| **不再改，只归档展示** | **SVG 贴图**（最优） | 样式 100% 可控、与预览像素一致、可出正式风 |

| | **SVG** | **Excalidraw JSON** | **Mermaid** |
|---|---|---|---|
| 落板后 | `image` 贴图 | 原生图元 | 原生图元 |
| 用户可双击改 | ❌ | ✅ | ✅ |
| **Agent 能读回内容** | ❌ **黑箱** | ✅ | ✅ |
| 手绘风 | ❌ | ✅ | ✅ |
| 样式掌控 | **100%，可出正式风** | 中 | 算法决定 |
| Token 成本 | 高 | 高 | **最低** |
| 适合 | 汇报/归档/正式图 | 精细结构图 | 流程图、时序图 |

**4b. 选路径**：① 复制粘贴（零配置）② 生成 `.excalidraw` → 右键「导入画板」③ 桥接 `addElement`（需中继+MCP）。
通道与路径可自由组合，例如 Mermaid 转出的元素既能存文件导入，也能经桥直接落板。

**5 秒自测**：双击图里的方框——能编辑文字 = 原生图元；整块被选中 = 贴图。

⚠️ **走 SVG 通道时必做**：贴图后 Agent **再也读不回图里的内容**（`getBoard` 只见 `image` 元素）。所以要么会话内保留源，要么按「源随图走」约定，**在贴图旁附一个文本元素存 Mermaid 源码/关键提示词**（零成本，防会话结束后成死资产）。

## spec 格式
```python
scene = {
    "title": "可选：图的标题",
    "boxes": [
        {"id": "a", "label": "开始", "col": 0, "row": 0, "role": "input"},   # 网格自动布局 + 语义配色
        {"id": "b", "label": "处理很长的中文标签也不会溢出", "col": 1, "row": 0, "role": "process"},  # 自动撑大
        {"id": "c", "label": "输出", "col": 2, "row": 0, "role": "output"},
        {"id": "e", "label": "显式坐标", "x": 320, "y": 0},                  # 或显式坐标（像素）
        {"id": "f", "label": "重点", "col": 1, "row": 1, "fill": "#fff3bf"}, # fill 可显式覆盖底色
    ],
    "arrows": [
        {"from": "a", "to": "b", "label": "下一步"},          # 默认深灰正交箭头（elbowed）
        {"from": "c", "to": "e", "role": "danger"},           # 危险连线染红
    ],
}
```

### box 字段
| 字段 | 含义 |
|------|------|
| `id` | 唯一标识，arrow 用 `from`/`to` 引用 |
| `label` | 框内文字（自动按视觉字宽折行、并撑大框，中文不再溢出） |
| `col`/`row` | **自适应网格**坐标：每列/每行按实际最大宽度排布，互不重叠 |
| `x`/`y` | 显式像素坐标（跳过网格，直接定位） |
| `role` | 语义角色，**决定底色+描边+文字色，全图配色自动一致**（见下表） |
| `fill` | 显式底色（与 `role` 二选一；`role` 优先） |
| `size` | 文字大小（默认 `BODY_SIZE=20`） |
| `width`/`height` | 显式锁定尺寸（不传则按 label 自动撑大） |
| `lib` | 引用素材库图标（见「Excalidraw 素材库」小节） |

### 语义角色 PALETTE（用「角色」而非「颜色」写图 → 配色永远协调）
| role | 色 | 适用 |
|------|----|------|
| `default` | 白底黑描边 | 普通节点 |
| `input` | 蓝 | 输入 / 用户 / 来源 |
| `process` | 灰 | 处理 / 中间步骤 |
| `output` | 绿 | 输出 / 成功 / 结果 |
| `store` | 黄 | 存储 / 数据 / 状态 |
| `external` | 紫 | 外部系统 / 第三方 |
| `decision` | 橙 | 判断 / 分支 |
| `danger` | 红 | 风险 / 异常 / 禁止 |
| `accent` | 高亮黄 | 本图重点 |

### arrow 字段
- `from`/`to`：box 的 `id`。
- `label`：线上文字（可选，自动折行、挂到箭头 id、随箭头移动）。
- `role`：仅 `danger` 会染红；其余保持**中性深灰**（`ARROW_COLOR`）——红色是语义色，不该当默认。
- 所有箭头默认 **`elbowed`（正交折线）**，节点多时比斜线更不易打架；双向绑定 box，移动 box 箭头跟随。

### 通用约定
- 网格：`col`/`row` 自动算坐标（自适应间距，留白节奏宁大勿小）；混用显式坐标也行。
- 字体用 Virgil 手写体（fontFamily=1），契合 KaiBoard 手写主题。
- 文字容器用**标准绑定**（`rectangle` 的 `boundElements` + `text` 的 `containerId`），不是 Excalidraw 骨架 API 的 `label` 属性——后者仅供 Skeleton 程序化生成，原始 JSON 不认。

## 自测
```
python <skill_dir>/gen_excalidraw.py --selftest          # 校验生成器 schema/语义/不溢出
node   <skill_dir>/render_preview.cjs <图>.excalidraw     # 渲染真实手绘风 .svg 预览（需 roughjs）
```
`gen_excalidraw.py` 校验 schema（type/version、appState.zoom 为 {value} 对象、元素含 id/type、`role` 落到底色/描边、危险箭头染红且 `elbowed`、矩形不溢出文字）。`render_preview.cjs` 用 roughjs（Excalidraw 同款手绘引擎）把文件渲染成可在对话里直接预览的手绘 SVG，**无须浏览器 / jsdom**。

## 工具清单
| 文件 | 作用 |
|------|------|
| `gen_excalidraw.py` | spec → 合法 `.excalidraw`（hachure 手绘填充 + 语义配色 + 绑定箭头 + 自适应尺寸） |
| `render_preview.cjs` | `.excalidraw` → 真实手绘风 `.svg` 预览（roughjs，无浏览器依赖） |
| `lib_resolver.py` | 素材库在线检索 → 按需取件 → 取组件转为画板元素 |
| `geometry_check.py` | 落板自检：穿框 / 重叠 / 悬空绑定 / 重复 id 四项确定性检测 |

## 快速上手示例
`python gen_excalidraw.py --selftest` 会生成一张覆盖全部语义角色（input/process/output/store/decision/external/danger）、自适应尺寸、正交箭头的完整数据流图 —— 可直接作为 spec 的写法参考，也可导入 KaiBoard 看效果。查看生成的 spec 结构，照它改写即可。

## 重要约束（避免导入白屏）
- `appState.zoom` **必须是 `{value: number}` 对象**，绝不能是纯数字（Excalidraw 0.18.1 按 `zoom.value` 取值，纯数字会崩溃）。
- 元素必须含 `id` / `type` / `x` / `y` / `width` / `height` 等基础字段；本脚本已内置合规默认值。
- 不要带 `width/height=0` 的 appState 或临时 UI 态（selectedElementIds 等）——会触发 KaiBoard 的白屏兜底。

## Excalidraw 素材库（libraries.excalidraw.com）

`https://libraries.excalidraw.com/` 是社区共享的**形状素材库**（软件架构 / UML&ER / 云图标 / 流程图符号等，格式 `.excalidrawlib`）。按需取件后，生成图时可直接引用里面的现成图标。

> **本仓不随仓分发任何素材库实体文件** —— 素材是第三方作者的资产、各有其许可。本仓只提供**在线检索与按需取件**能力，以及一份可检索的清单概览（`references/asset-catalog.md`）。

- **取件**：`python lib_resolver.py --ensure "<库名>"`（命中库下载并缓存到本地素材目录 `libs/`，生成器会自动加载）。也可直接 `--load-lib <路径>` 临时加载。
- **库有 v1 / v2 两种格式**：v2 带 `name` 索引；v1 只有元素列表、无名字。加载器两种都兼容；**v1 项用 `库名:#N` 引用**（如 `uml-er#2`），也可用 `库名:推导名`（取项内最长文字）。列出全部可用名：`python gen_excalidraw.py --list-libs`。
- **在 spec 里引用图标**：box 加 `"lib": "图标名"` 即可，生成器会把该图标克隆为图中节点（浅灰虚线外框可绑定箭头 + 可选标签）。
  ```python
  {"id": "svc", "lib": "systemdesign-icons:ServiceCluster", "x": 560, "y": 150, "label": "订单服务"}
  ```
  重名时用 `"库名:图标名"`（不含扩展名）区分。**同一图标可多次引用**：配不同 `label` 即变成不同语义节点（如 ServiceCluster 复用为「订单服务」「用户服务」）。
- **扩更多库**：`--load-lib` 指定任意 `.excalidrawlib` 即可。超大整库（AWS/GCP/Azure 全量）不建议长期加载，按需用 `--load-lib` 临时取。
- **用户侧另法**：KaiBoard 里也能手动「导入素材库」把社区图标拖进画板手绘。
