#!/usr/bin/env python3
"""
KaiBoard / Excalidraw 图表生成器
=================================
从一份结构化的「图描述」生成合法的 .excalidraw 文件，供 KaiBoard（或 Excalidraw）导入。

设计原则：
- Agent 负责「想」——把用户的自然语言想法翻译成 boxes/arrows 的结构（id + 标签 + 网格位置）。
- 本脚本负责「画」——把结构渲染成合法的 Excalidraw JSON（元素 schema、绑定、appState 全合规）。
- 输出文件可直接用 KaiBoard 文件夹右键「导入画板」收进来。

用法：
  python gen_excalidraw.py --spec spec.py --out diagram.excalidraw
  python gen_excalidraw.py --selftest                 # 自测：生成样例并校验
  python gen_excalidraw.py --list-libs                # 列出已加载素材库的全部图标名
  python gen_excalidraw.py --spec spec.py --out d.excalidraw --load-lib extra/foo.excalidrawlib

素材库（libraries.excalidraw.com）：
  用 `--load-lib` 加载任意 .excalidrawlib（可多次传入）；若本地存在素材目录 `libs/`，
  其中的 .excalidrawlib 会被自动加载（由 `lib_resolver.py --ensure` 按需下载而来）。
  spec 里用 {"lib":"图标名", ...} 即可把现成图标嵌入图里。
  本仓不随仓分发任何素材库实体文件（第三方资产，各有其许可）。

spec.py 约定：
  scene = {
      "title": "可选标题",
      "boxes": [
          {"id":"a", "label":"开始", "col":0, "row":0, "role":"input"},     # 普通矩形（网格自动布局 + 语义配色）
          {"id":"b", "label":"处理很长的中文标签也不会溢出", "col":1, "row":0, "role":"process"},  # 自动撑大
          {"id":"c", "label":"输出", "col":2, "row":0, "role":"output"},
          {"id":"d", "label":"风险点", "col":1, "row":1, "role":"danger"},
          {"id":"e", "label":"显式坐标", "x":300, "y":0},                 # 或显式坐标
          {"id":"lb","lib":"ServiceCluster","col":0,"row":1,             # 素材库图标节点
           "label":"服务集群"},                                          #   label 显示在图标下方
      ],
      "arrows": [
          {"from":"a", "to":"b", "label":"下一步"},        # 默认深灰正交箭头
          {"from":"b", "to":"d", "role":"danger"},         # 危险连线用红色强调
      ],
  }
  语义角色 role 取值（见 PALETTE）：default/input/process/output/store/external/decision/danger/accent
  箭头同样可用 role（仅 danger 会染红），其余保持中性深灰。
  lib 取值：库内图标名（如 "ServiceCluster"）；若重名可用 "库文件名:图标名"（不含扩展名）。
"""
import argparse
import copy
import glob
import json
import os
import random
import time
import uuid

# ---- 默认视觉参数 ----
FONT_FAMILY = 1          # 1 = Virgil（手写体），契合 KaiBoard 手写字体主题
BOX_W, BOX_H = 200, 80   # 最小尺寸；实际会按标签自动撑大
GAP_X, GAP_Y = 140, 100  # 留白节奏：宁大勿小。挤在一起是"看着乱"的头号原因
STROKE = "#1e1e1e"
BG = "transparent"
ARROW_COLOR = "#343a40"  # 箭头默认深灰 —— 红色是语义色（异常/告警），不该当默认
ACCENT = "#e03131"       # 仅用于真正需要强调的地方
TITLE_SIZE = 28
BODY_SIZE = 20
NOTE_SIZE = 14
# 素材库图标节点用的轻量外框（透明底 + 浅灰虚线），既是可视容器也可被箭头绑定
NODE_STROKE = "#ced4da"

# ---- 语义调色板（取自 Excalidraw 官方色板，浅底 + 同色系深描边，保证手绘风协调）----
# 用「角色」而不是「颜色」来写 spec：语义化 → 全图配色自动一致，也便于统一换肤。
PALETTE = {
    "default":  {"bg": "#ffffff", "stroke": "#1e1e1e"},
    "input":    {"bg": "#d0ebff", "stroke": "#1971c2"},  # 蓝 · 输入 / 用户 / 来源
    "process":  {"bg": "#e9ecef", "stroke": "#495057"},  # 灰 · 处理 / 中间步骤
    "output":   {"bg": "#d3f9d8", "stroke": "#2f9e44"},  # 绿 · 输出 / 成功 / 结果
    "store":    {"bg": "#fff3bf", "stroke": "#f08c00"},  # 黄 · 存储 / 数据 / 状态
    "external": {"bg": "#f3f0ff", "stroke": "#6741d9"},  # 紫 · 外部系统 / 第三方
    "decision": {"bg": "#ffe8cc", "stroke": "#e8590c"},  # 橙 · 判断 / 分支
    "danger":   {"bg": "#ffc9c9", "stroke": "#c92a2a"},  # 红 · 风险 / 异常 / 禁止
    "accent":   {"bg": "#ffec99", "stroke": "#e67700"},  # 高亮 · 本图重点
}
GROUP_BG = "#f8f9fa"      # 分组容器底色（极浅，只做区域暗示，不抢主体）
GROUP_STROKE = "#adb5bd"


def _is_cjk(ch):
    return "\u2e80" <= ch <= "\u9fff" or "\uff00" <= ch <= "\uffef" or "\u3000" <= ch <= "\u303f"


def text_size(label, size=BODY_SIZE):
    """估算多行文本的像素宽高。中文按 1.0em、西文按 0.56em 计（Virgil 实测近似值）。

    生成器不做真实字体度量，但**必须**有这个估算 —— 否则中文标签一长就溢出框外，
    这是自动生成图"看起来很业余"的最主要原因。
    """
    lines = str(label).split("\n")
    widest = 0.0
    for ln in lines:
        w = sum(size * (1.0 if _is_cjk(c) else 0.56) for c in ln)
        widest = max(widest, w)
    return widest, len(lines) * size * 1.25


def wrap_label(label, max_em=11):
    """按「视觉字宽」折行（中文 1、西文 0.56）。已含换行符的按用户意图不动。"""
    if "\n" in str(label):
        return label
    out, cur, acc = [], "", 0.0
    for ch in str(label):
        w = 1.0 if _is_cjk(ch) else 0.56
        if acc + w > max_em and cur:
            out.append(cur)
            cur, acc = "", 0.0
        cur += ch
        acc += w
    if cur:
        out.append(cur)
    return "\n".join(out)


def _uid():
    return uuid.uuid4().hex[:12]


def make_batch_marker(theme, now=None, batch_no=1, x=0, y=0, size=18, color="#1971c2"):
    """生成「批次标记」分隔文本框——Mode A 每批必带（见 SKILL.md 铁律 #5）。

    固定格式：'━━━ YYYY-MM-DD HH:MM · 批次N · 主题 ━━━'
    作为本批第一个元素、置于顶部，天然把本轮新内容与其余画板内容分隔，并作传递记录
    （谁画、何时画、画了啥），便于日后回溯 / 多模态模型读回。

    - theme : 一句话主题，如「微服务架构图（汇报升级版·干净版）」
    - now   : 缺省取本机当前时间（本地时区），格式 YYYY-MM-DD HH:MM
    - x, y  : 左上角坐标（左对齐）
    生成器在落板前必须调用本函数把标记作为 elements[0] 加进去；不要手搓、不要漏。
    """
    if now is None:
        now = time.strftime("%Y-%m-%d %H:%M")
    text = f"━━━ {now} · 批次{batch_no} · {theme} ━━━"
    w, _ = text_size(text, size)
    t = make_text(text, x + w / 2, y, w, size=size, color=color)
    t["x"] = x
    t["textAlign"] = "left"
    t["version"] = 1
    return t


def _now():
    return int(time.time() * 1000)


def _base(el_type, x, y, w, h, roundness=None):
    return {
        "id": _uid(),
        "type": el_type,
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0,
        "strokeColor": STROKE,
        "backgroundColor": BG,
        "fillStyle": "hachure",   # 手绘风关键：草图斜线填充，而非死板实底
        "hachureGap": 7,          # 斜线间距（越小越密）
        "fillWeight": 1.5,        # 斜线粗细
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1.2,         # 1.2 略带抖动，比 1 更像人手绘
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": roundness,
        "seed": random.randint(1, 2**31),
        "versionNonce": random.randint(1, 2**31),
        "isDeleted": False,
        "boundElements": [],
        "updated": _now(),
        "link": None,
        "locked": False,
    }


def make_text(label, cx, top, width, size=16, color=STROKE):
    return {
        "id": _uid(),
        "type": "text",
        "x": cx - width / 2, "y": top, "width": width, "height": size * 1.25,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": random.randint(1, 2**31),
        "versionNonce": random.randint(1, 2**31),
        "isDeleted": False,
        "boundElements": [],
        "updated": _now(),
        "link": None,
        "locked": False,
        "text": label,
        "fontSize": size,
        "fontFamily": FONT_FAMILY,
        "textAlign": "center",
        "verticalAlign": "middle",
        "containerId": None,
        "originalText": label,
        "lineHeight": 1.25,
        "baseline": size,
    }


def box_dims(label, role=None, size=BODY_SIZE, w=None, h=None):
    """仅估算盒子尺寸（不创建元素），供网格自适应布局使用。"""
    wrapped = wrap_label(label)
    tw, th = text_size(wrapped, size)
    bw = w if w is not None else max(BOX_W, int(tw) + 44)
    bh = h if h is not None else max(BOX_H, int(th) + 28)
    return bw, bh, wrapped


def make_box(label, x, y, w=None, h=None, fill=None, role=None, size=BODY_SIZE):
    """生成「自动适配标签」的矩形 + 居中绑定文本。

    - role: 语义角色（见 PALETTE），决定底色 + 描边 + 文字色，全图配色一致。
    - fill: 显式底色，与 role 二选一（role 优先）。
    - 不传 w/h 时按标签视觉宽度自动撑大，杜绝中文溢出框外。
    """
    if role and role in PALETTE:
        bg, stroke = PALETTE[role]["bg"], PALETTE[role]["stroke"]
    else:
        bg = fill if fill is not None else PALETTE["default"]["bg"]
        stroke = PALETTE["default"]["stroke"]

    wrapped = wrap_label(label)
    tw, th = text_size(wrapped, size)
    bw = w if w is not None else max(BOX_W, int(tw) + 44)
    bh = h if h is not None else max(BOX_H, int(th) + 28)

    el = _base("rectangle", x, y, bw, bh, roundness={"type": 3})
    el["backgroundColor"] = bg
    el["strokeColor"] = stroke
    txt = make_text(wrapped, x + bw / 2, y, bw, size=size, color=stroke)
    txt["verticalAlign"] = "middle"
    txt["y"] = y
    txt["height"] = bh
    txt["containerId"] = el["id"]
    el["boundElements"] = [{"type": "text", "id": txt["id"]}]
    return el, txt


def _regen_ids(els):
    """深拷贝后重映射所有内部 id/引用，并统一成一个新 group，避免与图里其它元素冲突。"""
    idmap = {}
    for e in els:
        idmap[e["id"]] = _uid()
    group = _uid()
    for e in els:
        e["id"] = idmap[e["id"]]
        if e.get("containerId") and e["containerId"] in idmap:
            e["containerId"] = idmap[e["containerId"]]
        if e.get("frameId") and e["frameId"] in idmap:
            e["frameId"] = idmap[e["frameId"]]
        if e.get("boundElements"):
            for be in e["boundElements"]:
                if be.get("id") in idmap:
                    be["id"] = idmap[be["id"]]
        if e.get("startBinding") and e["startBinding"].get("elementId") in idmap:
            e["startBinding"]["elementId"] = idmap[e["startBinding"]["elementId"]]
        if e.get("endBinding") and e["endBinding"].get("elementId") in idmap:
            e["endBinding"]["elementId"] = idmap[e["endBinding"]["elementId"]]
        e["groupIds"] = [group]
        e["seed"] = random.randint(1, 2**31)
        e["versionNonce"] = random.randint(1, 2**31)
        e.pop("index", None)
        e["version"] = e.get("version", 1)
    return els


def make_lib_node(item, x, y, label=None):
    """把一个素材库条目克隆为一个图中节点：浅灰虚线外框(可绑定) + 图标元素 + 可选标签。"""
    els = copy.deepcopy(item["elements"])
    xs = [e["x"] for e in els]
    ys = [e["y"] for e in els]
    ws = [e.get("width", 0) for e in els]
    hs = [e.get("height", 0) for e in els]
    minx, miny = min(xs), min(ys)
    maxx = max(x + w for x, w in zip(xs, ws))
    maxy = max(y + h for y, h in zip(ys, hs))
    w, h = maxx - minx, maxy - miny

    _regen_ids(els)
    for e in els:
        e["x"] = e["x"] - minx + x
        e["y"] = e["y"] - miny + y

    node_id = _uid()
    label_h = 30 if label else 0
    rect = _base("rectangle", x, y, w, h + label_h, roundness={"type": 3})
    rect["id"] = node_id
    rect["backgroundColor"] = "transparent"
    rect["strokeColor"] = NODE_STROKE
    rect["strokeStyle"] = "dashed"
    rect["strokeWidth"] = 1
    out = [rect]
    out.extend(els)
    if label:
        out.append(make_text(label, x + w / 2, y + h + 4, max(w, 80), size=NOTE_SIZE))
    return node_id, out


def make_arrow(frm, to, label=None, color=None):
    fx, fy, fw, fh = frm["x"], frm["y"], frm["width"], frm["height"]
    tx, ty, tw, th = to["x"], to["y"], to["width"], to["height"]
    fc = (fx + fw / 2, fy + fh / 2)
    tc = (tx + tw / 2, ty + th / 2)
    if tc[0] >= fc[0]:
        sx, sy = fx + fw, fy + fh / 2
        ex, ey = tx, ty + th / 2
    else:
        sx, sy = fx, fy + fh / 2
        ex, ey = tx + tw, ty + th / 2

    acolor = color or ARROW_COLOR
    arrow = _base("arrow", sx, sy, abs(ex - sx), max(1, abs(ey - sy)))
    arrow["points"] = [[0, 0], [ex - sx, ey - sy]]
    arrow["strokeColor"] = acolor
    arrow["elbowed"] = True          # 正交折线：比斜线更像工程图，节点多时不打架
    arrow["startBinding"] = {"elementId": frm["id"], "focus": 0, "gap": 4}
    arrow["endBinding"] = {"elementId": to["id"], "focus": 0, "gap": 4}
    arrow["startArrowhead"] = None
    arrow["endArrowhead"] = "arrow"
    arrow.pop("roundness", None)

    frm.setdefault("boundElements", []).append({"type": "arrow", "id": arrow["id"]})
    to.setdefault("boundElements", []).append({"type": "arrow", "id": arrow["id"]})

    out = [arrow]
    if label:
        wrapped = wrap_label(label, max_em=14)
        tw, th = text_size(wrapped, NOTE_SIZE)
        lx = (sx + ex) / 2 - tw / 2
        ly = (sy + ey) / 2 - th / 2
        lbl = make_text(wrapped, lx + tw / 2, ly, tw, size=NOTE_SIZE, color=acolor)
        lbl["y"] = ly
        lbl["height"] = th
        lbl["containerId"] = arrow["id"]   # 修正：标签必须挂到真实箭头 id
        arrow["boundElements"] = [{"type": "text", "id": lbl["id"]}]
        out.append(lbl)
    return out


def _derive_name(els):
    """v1 库没有 name 字段，用项内最长文字元素推断一个可读名。"""
    best = ""
    for e in els:
        if e.get("type") == "text" and e.get("text"):
            if len(e["text"]) > len(best):
                best = e["text"]
    return best.strip()


def load_lib_file(path, index, files_out=None):
    """加载一个 .excalidrawlib，把组件名 -> {name, elements} 写进 index。

    files_out: 若传入 dict，会把库内顶层的 files（image 元素依赖的 dataURL 映射）合并进去，
    供 Mode A 注入时一并带上，避免图片元素因缺 files 而渲染为空。矢量库通常为空。
    """
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    fname = os.path.splitext(os.path.basename(path))[0]
    # 兼容两种格式：
    #  v2 -> libraryItems: [{status,elements,id,name,...}]
    #  v1 -> library: [[元素,...], [元素,...], ...]（无 name）
    items = d.get("libraryItems") or d.get("library") or []
    if files_out is not None and isinstance(d.get("files"), dict):
        files_out.update(d["files"])
    for i, it in enumerate(items):
        if isinstance(it, dict):
            nm = it.get("name") or _derive_name(it.get("elements", []))
            els = it.get("elements", [])
        else:
            nm = _derive_name(it)
            els = it
        if not nm:
            nm = f"{fname}#{i + 1}"
        index[nm] = {"name": nm, "elements": els}            # 裸名（重名后者覆盖）
        index[f"{fname}:{nm}"] = {"name": nm, "elements": els}  # 带库名限定，永不冲突
    return [k for k in index if not k.startswith(fname + ":")]


def build(scene, out_path, lib_index=None):
    lib_index = lib_index or {}
    elements = []
    boxes = {}

    # ---- 第一遍：先量每个普通 box 的尺寸，做「自适应网格」布局 ----
    # 传统固定列宽会让长中文标签溢出；这里按每列/每行最大实际宽度排布，互不重叠。
    col_maxw, row_maxh = {}, {}
    dims = {}
    for b in scene.get("boxes", []):
        if b.get("lib"):
            continue
        bw, bh, _ = box_dims(b["label"], role=b.get("role"), size=b.get("size", BODY_SIZE),
                             w=b.get("width"), h=b.get("height"))
        dims[b["id"]] = (bw, bh)
        if "x" not in b and "y" not in b:
            c = b.get("col", 0); r = b.get("row", 0)
            col_maxw[c] = max(col_maxw.get(c, 0), bw)
            row_maxh[r] = max(row_maxh.get(r, 0), bh)

    def _col_x(c):
        x = 0
        for i in range(c):
            x += col_maxw.get(i, BOX_W) + GAP_X
        return x

    def _row_y(r):
        y = 0
        for i in range(r):
            y += row_maxh.get(i, BOX_H) + GAP_Y
        return y

    # ---- 第二遍：放置节点 ----
    for b in scene.get("boxes", []):
        if "x" in b and "y" in b:
            x, y = b["x"], b["y"]
        else:
            x, y = _col_x(b.get("col", 0)), _row_y(b.get("row", 0))

        if b.get("lib"):
            ref = b["lib"]
            if ":" in ref:
                fname, iname = ref.split(":", 1)
                item = None
                for k, it in lib_index.items():
                    if k == iname:
                        item = it
                        break
                if item is None:
                    item = lib_index.get(iname)
            else:
                item = lib_index.get(ref)
            if item is None:
                raise ValueError(f"box '{b['id']}' 引用了不存在的素材库图标: {ref}")
            node_id, node_els = make_lib_node(item, x, y, b.get("label"))
            boxes[b["id"]] = next(e for e in node_els if e["id"] == node_id)
            elements.extend(node_els)
        else:
            bw, bh = dims[b["id"]]
            el, txt = make_box(b["label"], x, y, w=bw, h=bh,
                               fill=b.get("fill"), role=b.get("role"),
                               size=b.get("size", BODY_SIZE))
            boxes[b["id"]] = el
            elements.append(el)
            elements.append(txt)

    if scene.get("title"):
        elements.append(make_text(scene["title"], 300, -BOX_H - 30, 600, size=TITLE_SIZE))

    for a in scene.get("arrows", []):
        frm = boxes.get(a["from"])
        to = boxes.get(a["to"])
        if not frm or not to:
            raise ValueError(f"arrow 引用了不存在的 box: {a}")
        acolor = ACCENT if a.get("role") == "danger" else None
        elements.extend(make_arrow(frm, to, a.get("label"), color=acolor))

    payload = {
        "type": "excalidraw",
        "version": 2,
        "source": "kaiboard-draw",
        "elements": elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": "#ffffff",
            "zoom": {"value": 1},
        },
        "files": {},
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out_path, len(elements)


def _default_lib_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "libs")


def _load_default_libs(extra=None):
    index = {}
    lib_dir = _default_lib_dir()
    files = sorted(glob.glob(os.path.join(lib_dir, "*.excalidrawlib"))) if os.path.isdir(lib_dir) else []
    for p in files:
        load_lib_file(p, index)
    for p in (extra or []):
        load_lib_file(p, index)
    return index


def _selftest():
    # 普通节点 + 语义角色 + 自适应尺寸
    scene = {
        "title": "自测图：从想法到白板",
        "boxes": [
            {"id": "a", "label": "用户想法", "col": 0, "row": 0, "role": "input"},
            {"id": "b", "label": "Agent 生成很长的中文标签也不会溢出", "col": 1, "row": 0, "role": "process"},
            {"id": "c", "label": "KaiBoard 导入查看", "col": 2, "row": 0, "role": "output"},
            {"id": "d", "label": "实时共绘", "col": 1, "row": 1, "role": "accent"},
        ],
        "arrows": [
            {"from": "a", "to": "b", "label": "描述"},
            {"from": "b", "to": "c", "label": "导入"},
            {"from": "c", "to": "d", "label": "升级", "role": "danger"},
        ],
    }
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_selftest.excalidraw")
    p, n = build(scene, out)
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    assert d["type"] == "excalidraw"
    assert isinstance(d["appState"]["zoom"], dict) and "value" in d["appState"]["zoom"]
    assert all("id" in e and "type" in e for e in d["elements"])
    # 校验：语义角色确实落到底色/描边；危险箭头染红
    rects = {e["id"]: e for e in d["elements"] if e["type"] == "rectangle"}
    assert rects[next(k for k, v in rects.items() if v.get("backgroundColor") == PALETTE["input"]["bg"])]
    danger_arrow = next(e for e in d["elements"] if e["type"] == "arrow" and e["strokeColor"] == ACCENT)
    assert danger_arrow["elbowed"] is True
    # 校验：每个矩形都能容纳其绑定文字（不溢出）
    for e in d["elements"]:
        if e["type"] == "rectangle":
            txt = next((t for t in d["elements"] if t.get("containerId") == e["id"]), None)
            if txt:
                tw, _ = text_size(txt["text"], BODY_SIZE)
                assert tw <= e["width"], f"文字溢出: {txt['text']}"
    print(f"[selftest] 普通节点 OK -> {p} ({n} elements, 含语义角色+自适应尺寸)")

    # 素材库图标节点（若 libs 可用）
    try:
        idx = _load_default_libs()
        if idx:
            demo_item = next((nm for nm in ("ServiceCluster", "cacheLayer", "MapReduce") if nm in idx), None)
            if demo_item:
                scene2 = {
                    "title": "自测图：素材库图标节点",
                    "boxes": [
                        {"id": "s", "lib": demo_item, "col": 0, "row": 0, "label": "来自素材库"},
                        {"id": "k", "label": "普通框", "col": 1, "row": 0},
                    ],
                    "arrows": [{"from": "s", "to": "k", "label": "连到"}],
                }
                p2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_selftest_lib.excalidraw")
                p2, n2 = build(scene2, p2, lib_index=idx)
                with open(p2, encoding="utf-8") as f:
                    d2 = json.load(f)
                assert all("id" in e and "type" in e for e in d2["elements"])
                print(f"[selftest] 素材库节点 OK -> {p2} ({n2} elements, 图标={demo_item})")
    except Exception as e:
        print(f"[selftest] 素材库节点跳过（libs 不可用）: {e}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", help="Python 文件，定义 scene 字典")
    ap.add_argument("--out", default="diagram.excalidraw", help="输出 .excalidraw 路径")
    ap.add_argument("--load-lib", action="append", default=[], help="额外加载的 .excalidrawlib（可重复）")
    ap.add_argument("--list-libs", action="store_true", help="列出已加载素材库的图标名后退出")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.list_libs:
        idx = _load_default_libs(args.load_lib)
        names = sorted(idx.keys())
        print(f"已加载 {len(names)} 个图标：")
        for nm in names:
            print("  -", nm)
        return

    if args.selftest:
        _selftest()
        return

    if not args.spec:
        ap.error("需要 --spec / --selftest / --list-libs")

    lib_index = _load_default_libs(args.load_lib)
    ns = {}
    with open(args.spec, encoding="utf-8") as f:
        exec(compile(f.read(), args.spec, "exec"), ns)
    scene = ns.get("scene")
    if not scene:
        raise SystemExit("spec 文件未定义 scene 变量")
    p, n = build(scene, args.out, lib_index=lib_index)
    print(f"[ok] {p} ({n} elements)")


# ============================================================
# 广义画图方法论 · 落地代码助手（详见 references/drawing-methodology.md）
# 借鉴公开实践：fixedPoint/binding 精准停靠、stagger 同边分散、路由模式选型、风格档位。
# 均为纯增量函数，不改动 build()。
# ============================================================

def style_tier(tier="technical"):
    """风格档位预设：sketch(草图/手绘, 高 roughness) ↔ technical(技术图, 低 roughness)。
    返回可直接展开进 _base() 的样式键值。"""
    if tier == "sketch":
        return {"roughness": 2.2, "strokeWidth": 1.6, "fillStyle": "hachure", "hachureGap": 9}
    # technical：干净、对齐、精确
    return {"roughness": 0.8, "strokeWidth": 1.8, "fillStyle": "hachure", "hachureGap": 6}


def _edge_point(box, fp):
    """fixedPoint → 绝对坐标。fp=[x,y] 为框内相对位置（0..1）。"""
    return (box["x"] + fp[0] * box["width"], box["y"] + fp[1] * box["height"])


def dock_arrow(frm, to, fp_from=(0.5, 1), fp_to=(0.5, 0),
               color=None, dashed=False, label=None, focus=0, gap=4):
    """精准停靠箭头：用 fixedPoint 决定从框的哪条边出/入，避免线穿框。
    - 纵向流：fp_from=(0.5,1)底 → fp_to=(0.5,0)顶
    - 横向流：fp_from=(0,0.5)左 → fp_to=(1,0.5)右
    返回 [arrow, (可选 label)] 列表，调用方 extend 进 elements。"""
    sx, sy = _edge_point(frm, fp_from)
    ex, ey = _edge_point(to, fp_to)
    acolor = color or ARROW_COLOR
    dx, dy = ex - sx, ey - sy
    arrow = _base("arrow", sx, sy, abs(dx) or 1, abs(dy) or 1)
    arrow["points"] = [[0, 0], [dx, dy]]
    arrow["strokeColor"] = acolor
    arrow["strokeWidth"] = 1.8
    arrow["roughness"] = 0.8
    arrow["elbowed"] = False
    arrow["startBinding"] = {"elementId": frm["id"], "focus": focus, "gap": gap, "fixedPoint": list(fp_from)}
    arrow["endBinding"] = {"elementId": to["id"], "focus": focus, "gap": gap, "fixedPoint": list(fp_to)}
    arrow["startArrowhead"] = None
    arrow["endArrowhead"] = "arrow"
    if dashed:
        arrow["strokeStyle"] = "dashed"
    arrow.pop("roundness", None)
    frm.setdefault("boundElements", []).append({"type": "arrow", "id": arrow["id"]})
    to.setdefault("boundElements", []).append({"type": "arrow", "id": arrow["id"]})
    out = [arrow]
    if label:
        wrapped = wrap_label(label, max_em=14)
        tw, th = text_size(wrapped, NOTE_SIZE)
        mx, my = (sx + ex) / 2 - tw / 2, (sy + ey) / 2 - th / 2
        lbl = make_text(wrapped, mx + tw / 2, my, tw, size=NOTE_SIZE, color=acolor)
        lbl["y"] = my
        lbl["height"] = th
        lbl["containerId"] = arrow["id"]
        arrow["boundElements"] = [{"type": "text", "id": lbl["id"]}]
        out.append(lbl)
    return out


def stagger(n, ratios=None):
    """同边扇出 n 根箭头时，返回每根的 focus 偏移（散布在边宽上，互不重叠）。
    以 0 为中心、覆盖 ±0.45（端点留 0.05 边距），与 authoring-excalidraw-files 的
    spread 公式同源（2→[-0.45,0.45], 3→[-0.45,0,0.45], 4→[-0.45,-0.15,0.15,0.45]）。"""
    if ratios:
        return list(ratios)
    if n <= 1:
        return [0]
    span = 0.9
    return [(-span / 2 + i * span / (n - 1)) for i in range(n)]


def route_pattern(frm, to, mode="straight", color=None, dashed=False, label=None, gap=4):
    """路由模式选型（neversight）：直行 / L / U / curve / elbow。
    - straight：同列/同行直落
    - L：先下后横（或先横后下）
    - U：回环绕到上方/下方（bypass，绕开中间框）
    - curve：加 waypoint + roundness 优雅弧过
    - elbow：肘线 Z 形（必要横穿时）
    返回 [arrow,(可选label)] 列表。arrow 自动绑定两端 + 按模式设 points。"""
    acolor = color or ARROW_COLOR
    fx, fy, fw, fh = frm["x"], frm["y"], frm["width"], frm["height"]
    tx, ty, tw, th = to["x"], to["y"], to["width"], to["height"]
    # 起点取 frm 底中，终点取 to 顶中（默认纵向直落）
    sx, sy = fx + fw / 2, fy + fh
    ex, ey = tx + tw / 2, ty
    pts = [[0, 0], [ex - sx, ey - sy]]  # straight
    elbowed = False
    roundness = None
    if mode == "L":
        midx = ex
        pts = [[0, 0], [0, (ey - sy) / 2], [midx - sx, (ey - sy) / 2], [midx - sx, ey - sy]]
    elif mode == "U":
        # 回环绕到上方：先上，再横，再下到目标顶（适合 A→...→A 回环）
        up = min(sy, ty) - 60
        pts = [[0, 0], [0, up - sy], [ex - sx, up - sy], [ex - sx, ey - sy]]
    elif mode == "curve":
        roundness = {"type": 2}
        pts = [[0, 0], [(ex - sx) / 2, -30], [ex - sx, ey - sy]]
    elif mode == "elbow":
        elbowed = True
        pts = [[0, 0], [0, (ey - sy) / 2], [ex - sx, (ey - sy) / 2], [ex - sx, ey - sy]]
    arrow = _base("arrow", sx, sy, max(1, abs(ex - sx)), max(1, abs(ey - sy)))
    arrow["points"] = pts
    arrow["strokeColor"] = acolor
    arrow["strokeWidth"] = 1.8
    arrow["roughness"] = 0.8
    arrow["elbowed"] = elbowed
    if roundness:
        arrow["roundness"] = roundness
    arrow["startBinding"] = {"elementId": frm["id"], "focus": 0, "gap": gap}
    arrow["endBinding"] = {"elementId": to["id"], "focus": 0, "gap": gap}
    arrow["startArrowhead"] = None
    arrow["endArrowhead"] = "arrow"
    if dashed:
        arrow["strokeStyle"] = "dashed"
    frm.setdefault("boundElements", []).append({"type": "arrow", "id": arrow["id"]})
    to.setdefault("boundElements", []).append({"type": "arrow", "id": arrow["id"]})
    out = [arrow]
    if label:
        wrapped = wrap_label(label, max_em=14)
        tw, th = text_size(wrapped, NOTE_SIZE)
        mx, my = (sx + ex) / 2 - tw / 2, (sy + ey) / 2 - th / 2
        lbl = make_text(wrapped, mx + tw / 2, my, tw, size=NOTE_SIZE, color=acolor)
        lbl["y"] = my
        lbl["height"] = th
        lbl["containerId"] = arrow["id"]
        arrow["boundElements"] = [{"type": "text", "id": lbl["id"]}]
        out.append(lbl)
    return out


if __name__ == "__main__":
    main()
