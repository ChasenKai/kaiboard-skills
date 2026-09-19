#!/usr/bin/env python3
"""KaiBoard 画图「自检 Loop」核心工具（程序化自检，不依赖看图）。

对标「绝不接受交叉箭头」+「缩到 50% 自检构图」两条成熟实践：
落板前/后跑一遍，确定性地揪出 4 类缺陷——
  1) 重复元素 id（会导致渲染错乱）
  2) 箭头悬空绑定（引用了不存在的 elementId）
  3) 矩形部分重叠（非分组的疑似穿叠）
  4) 箭头穿无关内容框（最致命，肉眼难发现）

用法：
  python geometry_check.py diag.json            # 裸数组 或 .excalidraw 包装都认
  python geometry_check.py diag.json --min-zone-w 1000
退出码：0 = PASS，1 = NEEDS FIX（可接进 CI / 自动化 Loop）。
"""
import sys, json

def load(path):
    d = json.load(open(path, encoding="utf-8"))
    return d if isinstance(d, list) else d.get("elements", [])

def bb(e):
    return (e["x"], e["y"], e["x"] + e.get("width", 0), e["y"] + e.get("height", 0))

def segs_of(a):
    pts = a.get("points", [[0, 0]])
    ox, oy = a["x"], a["y"]
    P = [(ox + p[0], oy + p[1]) for p in pts]
    return [(P[k], P[k + 1]) for k in range(len(P) - 1)]

def seg_hits_rect(s, r, inset=4):
    (ax, ay), (bx, by) = s
    x0, y0, x1, y1 = bb(r)
    x0 += inset; y0 += inset; x1 -= inset; y1 -= inset
    if max(ax, bx) < x0 or min(ax, bx) > x1 or max(ay, by) < y0 or min(ay, by) > y1:
        return False
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) - (B[1] - A[1]) * (C[0] - A[0])
    for e in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
              ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
        if (ccw(s[0], s[1], e[0]) * ccw(s[0], s[1], e[1]) <= 0) and \
           (ccw(e[0], e[1], s[0]) * ccw(e[0], e[1], s[1]) <= 0):
            return True
    return False

def contains(o, i):
    ox0, oy0, ox1, oy1 = bb(o)
    ix0, iy0, ix1, iy1 = bb(i)
    return ix0 >= ox0 and iy0 >= oy0 and ix1 <= ox1 and iy1 <= oy1

def check(els, min_zone_w=1000):
    by_id = {e["id"]: e for e in els}
    texts = {e["id"]: e for e in els if e["type"] == "text"}
    rects = [e for e in els if e["type"] == "rectangle"]
    arrows = [e for e in els if e["type"] == "arrow"]
    zone_bg = {r["id"] for r in rects
               if r.get("width", 0) >= min_zone_w and not r.get("boundElements")}
    content = [r for r in rects
               if r["id"] not in zone_bg and not r.get("kaiIconChild")]

    def lbl(b):
        for x in b.get("boundElements", []):
            if x["type"] == "text" and x["id"] in texts:
                return texts[x["id"]].get("text", "")[:10]
        return "?"

    problems = []

    # 1) 重复 id
    ids = [e["id"] for e in els]
    if len(ids) != len(set(ids)):
        problems.append(("dup_id", f"重复 id 数={len(ids)-len(set(ids))}"))

    # 2) 悬空绑定
    for a in arrows:
        for k in ("startBinding", "endBinding"):
            b = a.get(k)
            if b and b.get("elementId") and b["elementId"] not in by_id:
                problems.append(("dangling", f"箭头 {a['id'][:8]} {k} 悬空 -> {b['elementId'][:8]}"))

    # 3) 矩形部分重叠（排除包含=分组）
    for i in range(len(content)):
        for j in range(i + 1, len(content)):
            ax0, ay0, ax1, ay1 = bb(content[i])
            bx0, by0, bx1, by1 = bb(content[j])
            if ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1:
                if not (contains(content[i], content[j]) or contains(content[j], content[i])):
                    problems.append(("overlap", f"{lbl(content[i])} ✕ {lbl(content[j])}"))

    # 4) 箭头穿无关内容框
    for a in arrows:
        sb = a.get("startBinding") or {}
        eb = a.get("endBinding") or {}
        bound = {sb.get("elementId"), eb.get("elementId")}
        for s in segs_of(a):
            for r in content:
                if r["id"] in bound:
                    continue
                if seg_hits_rect(s, r):
                    problems.append(("cross", f"箭头 {a['id'][:8]} 穿 {lbl(r)}"))

    return problems

def main():
    if len(sys.argv) < 2:
        print("usage: geometry_check.py <file.json> [--min-zone-w N]")
        sys.exit(2)
    path = sys.argv[1]
    mzw = 1000
    if "--min-zone-w" in sys.argv:
        mzw = int(sys.argv and sys.argv[sys.argv.index("--min-zone-w") + 1])
    els = load(path)
    problems = check(els, mzw)
    print(f"[geometry_check] 元素 {len(els)} · 缺陷 {len(problems)}")
    for kind, msg in problems:
        print(f"  ❌ {kind}: {msg}")
    if problems:
        print("SELF-CHECK: NEEDS FIX")
        sys.exit(1)
    print("SELF-CHECK: PASS ✅")
    sys.exit(0)

if __name__ == "__main__":
    main()
