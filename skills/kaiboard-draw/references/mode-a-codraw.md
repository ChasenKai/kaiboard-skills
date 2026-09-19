# Mode A · 实时共绘

> 本文件是 `kaiboard-draw` 的 Mode A 详细指引（经本地中继 + MCP 实时驱动已打开的 KaiBoard 画布）。路由总览见主 SKILL.md。

# kaiboard-draw · Mode A

KaiBoard 的 **Mode A 实时共绘桥**。让外部 Agent 在用户开着的 KaiBoard 画布上直接增删元素，无需导出/导入的轮转。

## 架构（为什么需要中继）

IndexedDB 按 origin 隔离，Agent（桌面端）**不能直接写**用户 KaiBoard 页。链路是：

```
Agent (kaiboard-mcp --relay · MCP server)
   │  stdio JSON-RPC（本机）
   ▼
kaiboard-mcp 内建本机中继  ← 仅 127.0.0.1，令牌校验
   │  HTTP (本机)
   ▼
KaiBoard 内建轮询客户端  ← 校验 origin+令牌，经 Excalidraw API 改画布
```

- **KaiBoard 侧** = 页面内的 `postMessage` 监听 + 强类型「工具协议」（随 KaiBoard 一同部署）。
- **MCP 包** `@kaibuddy/kaiboard-mcp`（`kaiboard-mcp`）= 上述协议的对外一半：以 `--relay` 模式启动时，进程内同时运行 MCP server 与本地中继，把工具协议暴露成 MCP tools（`kbfs_*`）。

## 指令协议

消息体：`{ type:"kaiboard-agent-cmd", token, cmd, id?, ...命令字段 }`

**读**

| cmd | MCP 工具 | 含义 | 关键字段 |
|---|---|---|---|
| `getBoard` | `kbfs_get_board` | 读画板元素 | `boardId?` |
| `getScreenshot` | `kbfs_get_screenshot` | 读画板 **PNG 截图**（base64 data URL） | `boardId?`、`opts{maxWidthOrHeight,background,darkMode}` |
| `listBoards` | `kbfs_list_boards` | 列文件树（文件夹 + 画板 id/名/父级） | 无 |

**写**

| cmd | MCP 工具 | 含义 | 关键字段 |
|---|---|---|---|
| `addElement` | `kbfs_add_element` | 追加元素（**默认、非破坏**） | `elements`、`boardId?`、`source?` |
| `patchElement` | `kbfs_patch_element` | 按 id **局部改**属性（只合并给出的字段） | `patches:[{id,...}]`、`boardId?` |
| `deleteElement` | `kbfs_delete_element` | 按 id 删元素 | `ids`、`boardId?` |
| `replaceBoard` | `kbfs_replace_board` | 整板替换（**破坏性，需用户明确授权**） | `elements`、`boardId?`、`source?` |
| `createBoard` | `kbfs_create_board` | 新建画板，返回 `boardId` | `name?`、`parentId?`、`elements?` |
| `fromMermaid` | `kbfs_from_mermaid` | Mermaid 源码 → **原生可编辑图元**并落板 | `mermaid`、`boardId?`、`opts{replace,fontSize}` |

响应：`{ type:"kaiboard-agent-resp", id, ok, ... }`（`elements` / `ids` / `dataUrl` / `boardId` / `nodes` 视命令而定）
- `addElement` / `fromMermaid` / `createBoard` 成功时返回 `ids`（本次新建元素的稳定 id），请记录以便后续 patch/delete 引用。
- **自动布局**：当前画板非空时，新增元素会被整体下移到底边之下防重叠；agent 不必自己算避让坐标。
- **可撤销**：作用于**当前打开画板**的 agent 动作都进入 Excalidraw 历史，用户可 Ctrl+Z 撤销。

### 寻址：boardId 可选

所有画板级命令都接受可选 `boardId`：
- **缺省 / 等于当前画板** → 走 Excalidraw 实时 API：即时重绘、可 Ctrl+Z 撤销。
- **指向其它画板** → 直接读写本地库，**不切换用户的画布**（规避 canvas 竞态），写完自动刷新左侧文件树。此路径**不进 Excalidraw 历史**，无法 Ctrl+Z——改别的画板前请先确认。

先用 `listBoards` 拿 id，再带 `boardId` 操作。

### 源随图走（写类命令的 `source`）

写类命令可带 `source`，如 `{ "kind": "mermaid", "text": "graph TD; A-->B;" }`，会落到每个新元素的 `customData.__kbSource`，`getBoard` 读回时原样返回。

**为什么必须带**：贴图/生成图的真实代价是「Agent 读不回」——下次要改只能看着结果猜。带上源，下次可以**按源重生成**而不是猜图。`fromMermaid` 会自动把 mermaid 源记进去；手工 `addElement` 时请**主动带上** `source`（生成它的 mermaid / DSL / 用户原话）。

## 现成素材库图标（混合模式，Mode A 也能用现成矢量）

架构/系统设计图优先用现成矢量图标（AWS / K8s / C4 / UML / IT Logos / 网络 / 安全…），**不要手搓矩形写标签**。流程（详见 SKILL.md「素材感知构图」）：

1. 本地素材目录（`libs/`）已缓存的库直接取；没有的走在线检索取件：
   ```bash
   python lib_resolver.py --search "kafka"     # 跨源检索，返回候选库 + 命中组件
   python lib_resolver.py --ensure "IT Logos"  # 命中库下载并缓存到本地
   ```
2. 取组件为画板元素：`python lib_resolver.py --components libs/<库>.excalidrawlib Kafka Docker` → 输出 `{"elements":[...],"files":{...}}`。
3. 交给 Mode A：把 `elements` 数组（注意是数组，不是 `.excalidraw` 包装对象，见 §MCP file 格式）经 `kbfs_add_element` 追加，或用 `kbfs_replace_board` 整板替换（破坏性，需用户授权）。`files` 非空时一并带上，避免 image 元素缺依赖渲染为空。

> 取件后该库即被 `gen_excalidraw` 自动识别——Mode B 直接用 `{"lib":"<图标名>"}` 嵌，无需手写元素。

## Agent 使用策略（意图 → 命令，必读）

1. **改已有内容用 patchElement，别整板替换**：改颜色/改文字/挪位置 → `patchElement`；删几个 → `deleteElement`。只有用户**显式**说"替换整块/覆盖当前画板/重做"才用 `replaceBoard`。
2. **覆盖前先确认**：拿不准是"增量补充"还是"整板替换"时**先问用户**。replaceBoard 会抹掉画板全部现有内容（自动快照只是兜底，用户未必希望被覆盖）。
3. **流程图/时序图首选 fromMermaid**：写 Mermaid 比手搓元素坐标可靠得多，且产出是**原生可编辑图元**（用户能继续手改），不是贴图。
4. **画完存疑就 getScreenshot 看一眼**：元素 JSON 看不出重叠/错位/文字溢出，截图能。改完复杂布局后建议视觉自检一次。
5. **记录 ids**：写类命令返回的 `ids` 请保存；后续按 id 引用。
6. **元素形状**：`elements` 须是合法 Excalidraw 元素（至少含 `type`/`x`/`y`/`width`/`height`；建议带 `id`）。推荐用 `kaiboard-draw` 生成，避免手搓畸形元素导致画布白屏。
7. **坐标约定**：原点左上，x 向右、y 向下；矩形/文本 x/y 为左上角，line x/y 为起点。坐标大致合理即可，落板时的自动下移会处理避让。
8. **错误处理**：未识别工具名返回 `-32602` 并列出可用工具（绝不静默回落到 replaceBoard）；遇令牌/网络错误先确认中继与开关状态，勿盲目重试。

## 更新策略与确认纪律

共绘迭代常卡在两个问题："更新是覆盖还是另存？""模糊指令要不要先问？"本段把纪律钉死，避免反复返工。

### 0) 落板目标画板：默认当前画板，新建须显式

- **默认推到用户「当前打开的画板」**（MCP 不传 `boardId` 即作用于 active board，即 `kbfs_list_boards` 返回的 `activeBoardId`）。两种落法：
  - **往当前图下方追加**新内容（最常用、非破坏）：`kbfs_add_element`（`file`=裸元素数组）→ 画板非空时 KaiBoard 自动整批下移避让，呈现"往下画"。
  - **原地重做同一张图**（同图新版本）：`kbfs_replace_board` 整块替换当前画板（自动快照 + Ctrl+Z 可撤销）。
- **只有用户显式说「新建一张 / 新画板 / new board」时才用 `kbfs_create_board`**。绝不在"推个图看看"时默认开新板 —— 那会造成"到底看哪张"的混乱（见 §1 原地迭代纪律）。
- 前置：本机中继在跑（127.0.0.1:8787）+ KaiBoard 页面开 + Agent 共绘 ON；`file` 参数必须是**裸 Excalidraw 元素数组 JSON**（不是 `.excalidraw` 包装对象）。
- **反例**："推送到我画板上看一下"若被 Agent 理解成 `create_board` 开了新板，用户当前画板反而收不到内容 —— 即便新建本身是非破坏操作，也是错解意图。根因 = 缺这条默认规则。结论 =**「推个图」= 落到当前画板**，新建必须点名。

### 0-附) 批量落板：优先 `replaceBoard` 整板写入

- **批量 / 多图内容落板，优先用 `kbfs_replace_board`** —— 它是「set 整板」，**幂等**：无论被应用几次，写入的始终是同一份 elements，结果一致、零重复。
  - **关键做法**：replaceBoard 会抹掉整板，故必须先把「**当前画板全量 + 本批新内容**」组装成一份完整 elements（顺序堆叠、新内容排在已有内容底边 + 120px 之下、带批次标记），再一次性 replaceBoard，从而**不丢现有内容**。
  - **适用**：批量 / 多图内容落板。单点小改仍可用 `addElement`。
- **多图顺序落板**：多张图一次性 push 会**重叠**。必须**先后堆叠**（banner 在上、flow 在下，留 120px 间距），靠自动下移天然分隔；不要"两张一块到画板上"。

### 1) 覆盖 vs 另存：画布原地迭代，但每版留快照

- **画布（board）原地迭代**：同一张图的多轮优化，**直接更新同一块画布**（`patchElement` 局部改 / `replaceBoard` 整块重做），**不要每轮都新建一张画板**。画板是工作资产，反复堆新板只会造成"到底看哪张"的混乱 —— 常见诱因是板内标题没带版本号，浏览器缓存旧内容时无从分辨。
- **板内标题带版本号**：每次 replace 时把图的标题文本写成含版本的形式（如 `微服务架构图 · v2.1 优化版`），即便浏览器缓存旧内容，用户也能凭标题分辨当前是第几版。

### 2) 确认 vs 直接执行：模糊先问，清楚就做

- **直接执行（不必问）**：指令清晰、对象明确、自检已 PASS 的确定性操作 —— 如"把箭头 A 颜色改成红""删除批次标记""推 v2.1 上去""跨区箭头强制正交"。这类命令语义无歧义，执行后结果可预期。
- **先确认再执行**：指令**模糊/缺对象**时——如"优化一下""整理一下""弄好看点""再调调"，必须先反问"优化哪方面？是增量补充还是整块替换？"再动手；或当安全默认不明确、可能动到别的画板时。
- **破坏性操作铁律**：`replaceBoard` / `deleteElement` / 动其它画板，除非用户**同一句话里点名该操作**（"替换整块""覆盖当前画板""删掉这些"），否则**一律先确认**。replaceBoard 会抹掉画板全部现有内容，自动快照只是兜底。
- **自检闸门不豁免**：即便是"清楚"的指令，推送前仍须过 `geometry_check` PASS 闸门（推送前必须过闸门）。确认纪律管"该不该做"，自检纪律管"做出来对不对"。

## 落板后自检 Loop（必做，双轨）
每批图落板后，先跑一轮自检—修正，再交付给人看——这是「持续学习、自我修正」的闭环：
- **通道 A · 程序化自检（确定性，Agent 自身可跑）**：用 `geometry_check.py <diag.json>` 检测 4 类缺陷——重复 id / 箭头悬空绑定 / 矩形部分重叠 / **箭头穿无关内容框**（最致命，肉眼难发现）。返回非 0 即 FAIL，按报告修（`patchElement` 或改 `gen_excalidraw.py` 路由助手重生成）后**再跑直到 PASS**。
  - 注意：即便模型支持读图，程序化硬校验仍是 Agent 唯一的**确定性**修正依据，不能只靠「Agent 看图」——视觉自看对中文小字幻觉、细线穿框等仍可能漏判。
- **通道 B · 截图肉眼复核（给人 / 多模态）**：`getScreenshot` 回看溢出/压框/构图拥挤；截图交给用户，或交给支持图像输入的模型二遍眼检。
  - **边界（重要 · 审图 ≠ 出图）**：通道 B 的「Agent 读截图自检」只是**审图**（判断重叠 / 错位 / 乱码 / 水印），**不等于**「产出成品图」。审图能力可对成品图做自动初审，但不能替代「真实画板为源头」的产出链路。
- **反哺**：Loop 里反复出现的缺陷模式（如跨列斜箭头穿中间框、同排水平箭头穿过中间框），要立刻加进 `gen_excalidraw.py` 的路由助手（如 `orthogonal_route` 走分区 gutter 绕开、同排被挡则拱过）或本文件 §三 纪律，让下次生成阶段就不犯。

## 批次标记（Batch marker，Mode A 默认行为）

**每次 Mode A 新增内容（fromMermaid / addElement 带真实图元），默认在本批里带一个「批次标记」文本框**，作为这一轮绘制的**传递记录**：它标明"这一批什么时候画的、第几轮、画了什么主题"，并天然把本轮新内容和画板里**已有**的内容隔开。

> **命名统一**：「批次标记 / 分隔 / 分隔符」指**同一事物**，统一叫「批次标记」。`fromMermaid` 路径在 mermaid 源码首行写 `BATCH["━━━ … 批次 … ━━━"]`；`gen_excalidraw` 路径（生成器路径）必须调用 `gen_excalidraw.make_batch_marker(theme)` 把标记作为 `elements[0]` 加入 —— **不要手搓、不要漏**。该标记为 **SKILL.md 铁律第 5 条**，推送前必须校验其存在（除非用户明确要求不加）。

### 为什么是模型做、不是中继做
中继无状态、不知道批次边界，硬加会错位。改由**模型在生成时自带**：模型知道当前时间、也知道自己画了什么，天然契合"谁画谁标注"。

### 规则（默认开启，用户说不跳过）

1. **取当前时间**：用 `date "+%Y-%m-%d %H:%M"` 取本机时间，格式 `YYYY-MM-DD HH:MM`（本地时区）。
2. **主方法：在 mermaid 里直接写批次框（推荐，单次原子落板、最省性能）**
   把标记作为一个**断开节点**（无箭头连接）放进同一次 mermaid 源码第一行，内容含：分隔符 + 时间戳 + 批次号 + 一句话主题：
   ```text
   graph TB
     BATCH["━━━ 2025-01-01 09:30 · 批次1 · 微服务架构图 ━━━"]
     Client[客户端 Web + App] --> GW[API Gateway 网关]
     ...
   ```
   - `BATCH` 与主图无连接，仅作文字标记；mermaid 布局通常把它排在本批元素上方。
   - **用单个文本框当分隔**，不要拆成"真线 line + 时间戳 text 两个元素"—— 后者在 mermaid 布局里不可控，且若改用 `addElement` 后补会被自动下移拖到内容下面，达不到"在图形上方"的效果。
   - 每次生成都带上**一句话主题**（如"微服务架构图"），让每批内容自带标题，便于回溯。
   - `fromMermaid` 自动把 mermaid 源写进每个元素的 `customData.__kbSource`（含 BATCH 行），无需额外操作。
3. **空板处理**：`getBoard` 顺带取 `prevBottom`（画板现有元素最大 `y+height`；无内容则 `0`）。`prevBottom=0`（空板）时 `GAP_ABOVE` 取 `0`，批次框直接贴顶当标题；非空时按下方「间距规则」拉开。一次 `getBoard` 顺带完成，不额外往返。
4. **source 必带**：mermaid 法由 `fromMermaid` 自动记录源；手工 `addElement` 时请主动带上 `source`。
5. **关闭条件**：用户明确说"不要批次标记 / 别加时间戳 / 别加分隔 / 别加主题"时跳过；其余情况默认开启。

### 间距规则（默认开启，回应"离上一张图太近"）

批次标记、实际内容、以及新批次与画板已有内容之间的间距，默认按以下规则拉开（避免新图贴着旧图）：

1. **与已有内容的间距（GAP_ABOVE）**：`fromMermaid` 后整批会被下移到底边下，但默认间距偏小。默认把整批再下移到 `prevBottom + 120px`（≈ KaiBoard 默认间距的 **2 倍**；可调，想要更大就调大 `GAP_ABOVE`）。空板（`prevBottom=0`）时取 `0`。
2. **批次框 ↔ 内容间距（CONTENT_GAP）**：组合文本框（批次标记）与下方实际生成内容之间留 `50px` 空，不让文字贴着图。
3. **整批左对齐（ALIGN_LEFT，默认开启）**：整批（批次框 + 内容）的左边缘统一对齐到 `targetLeftX`，避免新图相对旧图"偏"：
   - 画板非空时 `targetLeftX = 画板现有元素的**最小 `x`**`（与已有内容左缘一致）；
   - 画板为空时 `targetLeftX = LEFT_MARGIN`（默认 `0`，可调）。
   - 计算 `deltaX = targetLeftX - min(本批所有元素的 x)`，把**整批每个元素**的 `x` 都加 `deltaX`（批次框与内容同步左移，保持彼此相对位置不变）。

**实施流程（一次 `fromMermaid` + 一次 `getBoard` + 一次 `patchElement`，属一次性批量操作、不持续占主线程）**：
1. `getBoard` 取 `prevBottom`（现有元素最大 `y+height`，无内容则 `0`）与 `prevLeftX`（现有元素最小 `x`）。
2. `fromMermaid` 把 `BATCH` 节点 + 主图一次性落板（自动先把整批挪到 `prevBottom` 下方）。
3. 再 `getBoard` 按 `customData.__kbSource` 认出本批元素；分出 `batchMarker` 与 `diagramNodes`，按上面规则算：`newBatchTop = prevBottom + GAP_ABOVE`、`diagramTopTarget`、`shiftY`、`targetLeftX`（非空取 `prevLeftX`，空板取 `LEFT_MARGIN`）、`deltaX`。
4. `patchElement` 一次性把整批坐标改成目标值：批次框 `{x: targetLeftX, y: newBatchTop}`；每个内容节点 `{x: x+deltaX, y: y+shiftY}`（整批左对齐到 `targetLeftX`、整体下移 `CONTENT_GAP`）。

> 真正会"卡"的是 `fromMermaid` 被框架盲目重试导致的**重复渲染**——见下方去重。间距这套只是多一次读 + 一次写，开销可忽略。

> 批次标记会随整批一起被自动下移避让；用户后续 Ctrl+Z 撤销整批时，标记一并撤销。批号 N 仅在单次会话内递增，跨会话重开从 1 计（或按时间戳区分即可）。

### 性能与去重（重要，回应"卡"的担心）
- 共绘链路是 `127.0.0.1` 本机异步 + KaiBoard 增量渲染，正常不阻塞用户其它操作；用户说一句后可先去忙，回头看即可。
- **命令去重（在 `kaiboard-mcp` 进程内生效）**：以命令体内容做指纹 + **60s TTL**，若 MCP 客户端 / 框架对慢命令（如大图 `fromMermaid` / 大数组 `addElement`）超时后盲目重试，重复命令**不会二次发往画布**，而是复用首次结果——**同一批图只渲染一次**，立省一半开销，也避免重复落图。实际生效点在 `kaiboard-mcp`（MCP server 进程，已在 `--relay` 模式下内建中继），改完后需在客户端里**重启该 MCP** 才生效（与轮换令牌同一步骤）。

## 安装与使用（统一 MCP 包 `kaiboard-mcp --relay`）

> Mode A 的完整自服务设置（令牌复制、mcp.json 注册、常见问题）见 skill 根目录 `SETUP.md`。此处只给要点与排错。

### 1) 注册并启动 MCP

**首选方式**：

```json
{
  "mcpServers": {
    "kaiboard": {
      "command": "npx",
      "args": ["-y", "@kaibuddy/kaiboard-mcp", "--relay"],
      "env": { "KAIBOARD_TOKEN": "<粘贴 KaiBoard「Agent 共绘」面板生成的令牌>" },
      "disabled": false
    }
  }
}
```

> Windows 下 `command` 用 `npx.cmd` 的全路径（如 `…\binaries\node\versions\<ver>\npx.cmd`），或直接由客户端解析。

**仅本地开发 / 改源码**时才用仓库内产物：

```json
{ "command": "npx", "args": ["-y", "@kaibuddy/kaiboard-mcp", "--relay"] }
```

注册后在连接器管理页面对该 server 点「信任」并**重启该 MCP**（改过 `mcp.json` 就必须重启才生效）。KaiBoard 页面打开 + 「Agent 共绘」开关 ON + 令牌一致，即连上。

> ⚠️ **改过 `mcp.json`（含换令牌）后，必须重启 MCP 才会加载新配置**；若页面开着但连不上，见下方「排错」。

### 1-附) 排错：中继连不上

**三步诊断，按顺序做**：

| 步骤 | 命令 | 判读 |
|---|---|---|
| 1 | `list_capabilities` | 看 `relayAvailable`（中继进程活否）/ **`pageConnected`**（页面接入否）。`serverInfo.version` 可确认跑的是哪个包版本 |
| 2 | `list_boards` | 返回 **`RELAY_FAILED: relay response timeout`** = 中继活着但**没有页面应答** → 问题在页面侧 |
| 3 | `netstat -ano -p TCP \| grep 8787` | 应有 `LISTENING`；`ESTABLISHED` 才说明真有连接 |

**已知现象与处置**：

- 🔴 **中继重启后，页面不会自动重连 → 需硬刷 KaiBoard 页面**（保持「Agent 共绘」ON）。现象：重启 MCP 后 `pageConnected:false` + `list_boards` 超时；**硬刷页面后即恢复 `pageConnected:true`、读写真通**。
  → 用户重启 Agent 客户端是常见操作，遇到「明明开着页面却超时」先让他**硬刷**，别急着查令牌。
- ✅ **`EADDRINUSE: 127.0.0.1:8787` 是正常设计**，不是故障 —— **一台机器只跑一个中继**。再起一个进程必然撞端口；看到它说明**中继已在跑**。
- **令牌不匹配**：症状通常是页面显示不匹配；让用户在面板点「更新令牌并重新复制」，改完 `mcp.json` **记得重启 MCP**。

**`get_screenshot` 返回过大**：结果是 base64 dataUrl（可达 8 万字符），直接读会超限。取 `result.dataUrl` → 剥掉 `data:image/png;base64,` → base64 解码存 PNG 再看。（与 `--dir` 不同：**relay 模式下截图可用**，`--dir` 下非空板会显式降级。）


### 2) 发指令（Agent 侧）

直接用 MCP 工具（**`kbfs_` 前缀**：`kbfs_get_board` / `kbfs_add_element` / `kbfs_replace_board` / `kbfs_from_mermaid` / `kbfs_list_capabilities` / …见上方指令协议表）。

> 🔴 **工具前缀统一为 `kbfs_`** —— 工具名绑定「KaiBoard 文件系统」语义，与产品名解耦。全部 12 个：`kbfs_get_board` / `kbfs_get_screenshot` / `kbfs_list_boards` / `kbfs_add_element` / `kbfs_patch_element` / `kbfs_delete_element` / `kbfs_replace_board` / `kbfs_create_board` / `kbfs_delete_board` / `kbfs_from_mermaid` / `kbfs_set_metadata` / `kbfs_list_capabilities`。

### 3) MCP 接入（供任意 MCP 客户端）
统一 MCP 包 `@kaibuddy/kaiboard-mcp`（`--relay`）把共绘动作暴露成 **`kbfs_*` 工具**（对应上表全部命令）。

典型链路示例：
```
kbfs_list_boards → 拿到目标画板 id
kbfs_from_mermaid { mermaid:"graph TD; 需求-->设计-->开发", boardId:"xxx" }
kbfs_get_screenshot { boardId:"xxx" }        ← 看一眼真实渲染
kbfs_patch_element  { patches:[{id:"kb_a", strokeColor:"#e03131"}] }   ← 只改一个框的颜色
```

### MCP `file` 参数格式（重要）

MCP 工具 `kbfs_add_element` / `kbfs_replace_board` 的 `file` 参数，要求文件内容是**合法的 Excalidraw 元素数组**（JSON array `[...]`），而不是 `.excalidraw` 文件那样的包装对象：

- ✅ 正确：`[{"id":"a","type":"rectangle",...}, ...]`
- ❌ 错误：`{"type":"excalidraw", "elements":[...], "appState":{...}}`

因为 MCP server（`kaiboard-mcp`）会执行 `elements = JSON.parse(fs.readFileSync(file))`，然后把整个解析结果赋给命令的 `elements` 字段。如果传了包装对象，`replaceBoard` 收到的是对象而非数组，页面会把它当作空元素处理，**导致整板被清空为 0 个元素**。Mode B 生成的 `.excalidraw` 文件是包装对象，直接作为 `file` 推送前必须先取 `.elements` 数组另存一份。

**显式令牌模型**：服务端读取环境变量 `KAIBOARD_TOKEN`，其值等于 KaiBoard 设置里显示的「中继令牌」。**授权完全由用户把令牌复制给 Agent 来完成** —— 没有你的授权，任何 Agent 都连不上。

注册示例（MCP 客户端的 `mcp.json`）：
```json
{
  "mcpServers": {
    "kaiboard": {
      "command": "npx",
      "args": ["-y", "@kaibuddy/kaiboard-mcp", "--relay"],
      "env": {
        "KAIBOARD_TOKEN": "在此粘贴 KaiBoard 设置里的「中继令牌」"
      }
    }
  }
}
```
> 💡 **更省事的做法**：KaiBoard 的「Agent 共绘」面板里有「复制给 Agent」按钮，一键给出可直接粘贴的配置（含令牌）—— 见 `SETUP.md`。
未配置 `KAIBOARD_TOKEN` 时，工具调用会返回清晰错误，提示去 KaiBoard 设置复制令牌。改完 `mcp.json` 后需在连接器管理页面对 `kaiboard-mcp` 点「信任」并重启该 MCP 使其生效（与轮换令牌同一步骤）。

### 4) 叠加 `--dir` 文件模式（kbfs_* 工具，零云、无中继）

`--dir` 是**可选的叠加能力**，不是第二个 server：在**同一个** `kaiboard-mcp` 条目上追加 `--dir <文件夹>` 即可（与 `--relay` 共存、互不互斥）。它对应 `kbfs_*` 工具集（`@kaibuddy/kaiboard-mcp` 统一包），让 Agent 直写本机文件夹、无需开页面。把 `--dir` 指向 **KaiBoard 浏览器所选的同一文件夹**：

```json
{
  "mcpServers": {
    "kaiboard": {
      "command": "npx",
      "args": [
        "-y", "@kaibuddy/kaiboard-mcp",
        "--relay",
        "--dir", "<你的 KaiBoard 文件夹绝对路径>"
      ]
    }
  }
}
```

- 命令行形态：`kaiboard-mcp --dir <文件夹> [--relay]`；`--dir` 缺省会打印用法并退出。
- **关键**：`--dir` 的值必须与 KaiBoard 设置里「文件夹存储」所选目录**完全一致**。两者不一致 → Agent 读写不到同一份数据。
- 改完 `mcp.json` 后需**重启 / 重载该 MCP** 使 `--dir` 生效（与轮换令牌同一步骤）。

## 自测
- 端到端需：`kaiboard-mcp` 以 `--relay` 运行（中继内建）+ KaiBoard 开「Agent 共绘」并复制令牌到 Agent MCP（`KAIBOARD_TOKEN`）+ KaiBoard 页面打开。
- 连通验证：用 `kbfs_list_boards` 拿画板 id，再 `kbfs_from_mermaid` / `kbfs_get_screenshot` 走一轮（详见上方「Agent 使用策略」）。

## 安全（必读）
- 共绘默认关闭；开启才生成令牌，令牌不匹配/来源不符一律不响应。
- **显式授权**：用户把「中继令牌」从 KaiBoard 设置复制、粘贴进 Agent 的 MCP 配置，才算授权该 Agent；Agent 不会自动发现令牌。
- 中继仅绑 127.0.0.1 + 令牌；userscript 仅把指令 postMessage 进同源页，绝不静默外发画板内容。
- 敏感动作（replaceBoard）在 KaiBoard 侧以 toast 透明提示，用户可见。

## 进阶：从 Mermaid / 自然语言生成图元

共绘协议只认「合法 Excalidraw 元素」。把 Mermaid 文本或自然语言转成元素有两条路：
桥内建的 `fromMermaid`（推荐），或 Agent 侧自行转换后 `addElement`。二者都遵循
「基础体验自研 + AI 用现成」原则 —— 转换用官方库，不自造。

### Mermaid → 原生图元（**已内建，首选**）
- KaiBoard 已直接依赖官方 `@excalidraw/mermaid-to-excalidraw@2.2.2`，桥命令 `fromMermaid`
  在页面内完成转换 → 落成**原生可编辑图元**（非贴图）。
- 用法：MCP `kbfs_from_mermaid { mermaid, boardId?, replace?, fontSize? }`。
- 自动带源：mermaid 原文会写进每个元素的 `customData.__kbSource`，下次可按源重生成。
- 坐标：库返回元素可能有重叠 / 偏移，交给 KaiBoard 自动下移避让；需精确布局自行调 x/y。

> 备选（Agent 侧转换）：若你的场景需要在推送前先程序化改写元素，可在 Agent 环境
> `npm i @excalidraw/mermaid-to-excalidraw`，调 `parseMermaidToExcalidraw(str)` 取 `elements`，
> 再走 `addElement`——此时请**手动带上** `source`，别让图变黑箱。

### 线框图 → 代码（Wireframe-to-code，外接实现）

同类产品把「画个界面草图 → 生成前端代码」做成内嵌付费 AI 功能。KaiBoard **不内嵌**——
同样的事在 Agent 侧做，且效果更好（用什么模型由用户自己定，费用自付、不加价、不锁厂商）。

标准流程：
1. 用户在画布上画界面草图（矩形当容器、文本当标签、线当分隔）。
2. Agent 调 `kbfs_get_screenshot { boardId? }` 拿 PNG —— **必须用截图，不要只读元素 JSON**：
   布局意图体现在视觉位置关系上，读 JSON 容易把「并排两栏」误解成两个孤立矩形。
3. 可选：再调 `kbfs_get_board` 拿元素文本内容，补齐截图里看不清的小字。
4. Agent 用自身多模态能力把截图翻译成 HTML/React/Vue 代码，写成本地文件交付。
5. 若用户要在画布上标注修改意见，用 `patchElement` 给对应元素加高亮色，或让用户直接用
   KaiBoard 的**元素批注**功能写文字意见，Agent 下一轮从 `customData.__kbComment` 读回。

要点：截图是「读」，代码文件是「写到磁盘」——整条链路**不需要 KaiBoard 内嵌任何模型**，
画板保持零后端、零账号。

### NL → Excalidraw 生成器（Agent 侧实现）
- 趋势：外部已有成熟的「自然语言 → 可编辑 Excalidraw 文件」能力可调用。
- 原则：KaiBoard **不做**内置 NL→图生成器（规避内嵌 AI 的维护税）；由 Agent 侧调用现成的
  NL→Excalidraw 能力产出元素，再经桥 `addElement` 上画布。
- 接入：Agent 取得 Excalidraw JSON → 校验为合法元素数组 → `addElement`；整板重做先与用户
  确认再用 `replaceBoard`。

- 无论走哪条通道（原生图元 / Mermaid / 预渲染图），最终都收敛到**「合法 Excalidraw 元素」这一契约**。

