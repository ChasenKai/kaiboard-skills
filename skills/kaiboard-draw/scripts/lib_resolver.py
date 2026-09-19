#!/usr/bin/env python3
"""
lib_resolver.py — KaiBoard 素材感知构图 · 混合检索解析器
=====================================================

定位：站在 excalidraw 社区素材库（及未来更多源）的肩膀上，让 Agent 具备
「搜索 → 取件 → 沉淀进我的素材 → 注入画板」的能力。

设计：
- 软件本体（KaiBoard 画图）= 本地优先、零联网。
- Agent 交互层 = 天然联网：素材库在线检索、按需取件。
- 不预下载全量（库在迭代，全量快照会过时且窄）。
- 本地素材目录 = 累积缓存：搜到 / 取过的库沉淀进 `libs/`，
  下次离线也能用（取件后会缓存在本地素材目录）。
- 可扩展：SOURCES 注册表，未来不止 excalidraw-libraries 一个源。

数据源（已实测可达）：
  index : https://raw.githubusercontent.com/excalidraw/excalidraw-libraries/main/libraries.json
  lib   : https://raw.githubusercontent.com/excalidraw/excalidraw-libraries/main/libraries/<source>
  （<source> 形如 "pclainchard/it-logos.excalidrawlib"；master 分支同样可用作 fallback）

与现有管线的接法（薄胶水，不重复造轮）：
- 取件后 .excalidrawlib 落进 libs/ —— gen_excalidraw._load_default_libs 会自动加载，
  Mode B 用 {"lib":"图标名"} 直接嵌。
- resolve_components() 复用 gen_excalidraw.load_lib_file / make_lib_node，
  产出可直接交给 Mode A（经 MCP 的 kbfs_replace_board / kbfs_add_element）的元素数组。

用法：
  python lib_resolver.py --search "kafka"            # 跨源检索，返回候选库 + 命中组件
  python lib_resolver.py --ensure "IT Logos"         # 把命中库下载并缓存到本地素材目录
  python lib_resolver.py --components libs/xxx.excalidrawlib Kafka Docker   # 取组件→元素
  python lib_resolver.py --list-my                   # 列出已缓存的素材
  python lib_resolver.py --refresh                   # 强制刷新 catalog 索引
"""
import argparse
import glob
import json
import os
import sys
import time
import urllib.request

# ---- 路径约定 ----
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
LIBS_DIR = os.path.join(HERE, "libs")                      # gen_excalidraw 自动加载目录
CACHE_DIR = os.path.join(LIBS_DIR, ".catalog_cache")      # catalog 索引缓存（带 TTL）
INDEX_FILE = os.path.join(CACHE_DIR, "excalidraw-libraries_index.json")
TTL_SECONDS = 24 * 3600                                    # 一天刷新一次 catalog

import gen_excalidraw as G   # 复用 load_lib_file / make_lib_node / build


# ============================================================
# 多源注册表（未来在此追加 Source 子类即可扩展）
# ============================================================
class LibrarySource:
    """一个素材源：能拉清单、能取件。"""
    key = "excalidraw-libraries"

    INDEX_RAW = "https://raw.githubusercontent.com/excalidraw/excalidraw-libraries/main/libraries.json"
    INDEX_JSDELIVR = "https://cdn.jsdelivr.net/gh/excalidraw/excalidraw-libraries@main/libraries.json"
    # 多宿主 × 多分支：raw.githubusercontent 在受限网络常抖动，jsDelivr 镜像更稳
    LIB_CANDIDATES = [
        "https://raw.githubusercontent.com/excalidraw/excalidraw-libraries/main/libraries/{source}",
        "https://raw.githubusercontent.com/excalidraw/excalidraw-libraries/master/libraries/{source}",
        "https://cdn.jsdelivr.net/gh/excalidraw/excalidraw-libraries@main/libraries/{source}",
        "https://cdn.jsdelivr.net/gh/excalidraw/excalidraw-libraries@master/libraries/{source}",
    ]

    def fetch_index_raw(self):
        last_err = None
        for url in (self.INDEX_RAW, self.INDEX_JSDELIVR):
            try:
                return _http_get(url, timeout=60)
            except Exception as e:
                last_err = e
        raise last_err or RuntimeError("index fetch failed")

    def download_lib(self, source, timeout=60):
        """直接 GET 取件，多宿主×多分支回退；任一成功即返回 bytes。
        不依赖 HEAD 探测（沙箱下 HEAD 偶发超时），改为「试下再回退」。"""
        last_err = None
        for url in self.LIB_CANDIDATES:
            try:
                return _http_get(url.format(source=source), timeout=timeout)
            except Exception as e:
                last_err = e
        raise last_err or RuntimeError("download failed for all candidates")


SOURCES = [LibrarySource()]


# ============================================================
# 底层 IO
# ============================================================
def _http_get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": "KaiBoard-Draw-Agent/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _slug(source):
    """pclainchard/it-logos.excalidrawlib -> pclainchard__it-logos.excalidrawlib"""
    base = os.path.basename(source)
    return source.replace("/", "__")


# ============================================================
# 索引：加载 / 刷新 / 归一化
# ============================================================
def _normalize(entry, src: LibrarySource):
    return {
        "src_key": src.key,
        "id": entry.get("id"),
        "name": entry.get("name") or "",
        "description": entry.get("description") or "",
        "source": entry.get("source") or "",
        "version": entry.get("version"),
        "itemNames": entry.get("itemNames") or [],
        "updated": entry.get("updated") or "",
    }


def load_index(force=False):
    """返回跨源归一化条目列表；带 TTL 缓存。无论缓存里是原始还是归一化格式，统一输出归一化。"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    fresh = (os.path.exists(INDEX_FILE) and
             (time.time() - os.path.getmtime(INDEX_FILE)) < TTL_SECONDS)
    if fresh and not force:
        with open(INDEX_FILE, encoding="utf-8") as f:
            raw = json.load(f)
        # 旧缓存可能是原始 libraries.json（无 src_key），统一归一化
        if raw and isinstance(raw, list) and "src_key" not in raw[0]:
            raw = [_normalize(e, SOURCES[0]) for e in raw]
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                json.dump(raw, f, ensure_ascii=False, indent=2)
        print(f"[index] 命中缓存（{len(raw)} 条，<24h）")
    else:
        print(f"[index] 刷新 catalog ...")
        raw = []
        for src in SOURCES:
            data = json.loads(src.fetch_index_raw())
            for e in data:
                raw.append(_normalize(e, src))
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=2)
        print(f"[index] 已刷新并缓存 {len(raw)} 条 -> {INDEX_FILE}")
    return raw


# ============================================================
# 检索
# ============================================================
def _score(entry, q):
    """返回 (总分, 命中组件名列表)。"""
    ql = q.lower()
    score = 0
    hits = []
    name = entry["name"].lower()
    desc = entry["description"].lower()
    if ql in name:
        score += 5
    if name.startswith(ql) or name == ql:
        score += 3
    if ql in desc:
        score += 2
    for it in entry.get("itemNames", []):
        if ql in it.lower():
            score += 3
            hits.append(it)
    # 模糊词：拆空格分别命中
    for tok in ql.split():
        if tok and tok not in ql:  # 防止重复计
            if tok in name: score += 1
            if tok in desc: score += 1
    return score, hits


def search(query, limit=12):
    """跨源检索；返回按分数排序的候选（含命中组件）。"""
    idx = load_index()
    ranked = []
    for e in idx:
        s, hits = _score(e, query)
        if s > 0:
            ranked.append((s, hits, e))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return [{"score": s, "matched_components": hits, **e} for s, hits, e in ranked[:limit]]


# ============================================================
# 取件：把库下载并缓存到本地素材目录
# ============================================================
def ensure_lib(entry_or_name, lib_dir=LIBS_DIR):
    """entry: 归一化条目 或 库名（按名模糊匹配第一条）。返回本地路径。"""
    os.makedirs(lib_dir, exist_ok=True)
    if isinstance(entry_or_name, str):
        cand = search(entry_or_name, limit=1)
        if not cand:
            raise SystemExit(f"未找到名为 '{entry_or_name}' 的库")
        entry = cand[0]
    else:
        entry = entry_or_name

    dest = os.path.join(lib_dir, _slug(entry["source"]))
    if os.path.exists(dest):
        print(f"[ensure] 已在我的素材中（跳过下载）: {dest}")
        return dest
    src = next((s for s in SOURCES if s.key == entry["src_key"]), SOURCES[0])
    data = src.download_lib(entry["source"])
    with open(dest, "wb") as f:
        f.write(data)
    print(f"[ensure] 已取件并沉淀: {entry['name']} -> {dest} ({len(data)} bytes)")
    return dest


def list_my(lib_dir=LIBS_DIR):
    files = sorted(glob.glob(os.path.join(lib_dir, "*.excalidrawlib")))
    out = []
    for p in files:
        try:
            d = json.load(open(p, encoding="utf-8"))
            items = d.get("libraryItems") or d.get("library") or []
            n = len(items)
        except Exception:
            n = -1
        out.append((os.path.basename(p), n))
    return out


# ============================================================
# 组件 -> 画板元素（复用 gen_excalidraw，薄胶水）
# ============================================================
def resolve_components(lib_path, names=None, origin=(0, 0), gap=40):
    """把库（或其中若干组件）转成可直接注入画板的元素数组。

    返回 {"elements": [...], "files": {...}}。
    - elements：每个组件经 gen_excalidraw.make_lib_node 克隆 + 重映射 id + 排布成一行。
    - files：库内 image 元素依赖的 files 映射（矢量库通常为空）。
    - names=None 取全部；否则只取命中的组件名。
    """
    index = {}
    files = {}
    G.load_lib_file(lib_path, index, files_out=files)
    if not index:
        raise SystemExit(f"库无可用组件: {lib_path}")
    chosen = list(index.values())
    if names:
        want = {n.lower() for n in names}
        chosen = [it for it in index.values() if it["name"].lower() in want]
        if not chosen:
            avail = ", ".join(sorted(index.keys()))
            raise SystemExit(f"库内无匹配组件 {names}；可用: {avail}")

    elements = []
    x, y = origin
    max_h = 0
    for it in chosen:
        node_id, node_els = G.make_lib_node(it, x, y, label=None)
        elements.extend(node_els)
        # 估算该节点宽高用于换行排布
        w = max((e.get("width", 0) for e in node_els if e["id"] == node_id), default=80)
        h = max((e.get("height", 0) for e in node_els if e["id"] == node_id), default=80)
        max_h = max(max_h, h)
        x += w + gap
        if x > origin[0] + 1600:   # 一行排满换行
            x = origin[0]
            y += max_h + gap
            max_h = 0
    return {"elements": elements, "files": files}


# ============================================================
# CLI
# ============================================================
def _print_search(query):
    res = search(query)
    if not res:
        print(f"未命中任何库: '{query}'")
        return
    print(f"\n检索 '{query}' -> {len(res)} 个候选：\n")
    for r in res:
        comp = ", ".join(r["matched_components"][:8]) or "（库级命中）"
        print(f"● {r['name']}  [score={r['score']}]")
        print(f"    source : {r['source']}")
        print(f"    组件命中: {comp}")
        if r["description"]:
            print(f"    描述   : {r['description'][:100]}")


def main():
    ap = argparse.ArgumentParser(description="KaiBoard 素材库混合检索解析器")
    ap.add_argument("--search", help="跨源检索关键词（库名/描述/组件名）")
    ap.add_argument("--ensure", help="把命中库下载并缓存到本地素材目录，传库名")
    ap.add_argument("--components", nargs="+", metavar="LIB_OR_NAMES",
                    help="第一个参数为 .excalidrawlib 路径，其余为组件名（可省略=全部）；输出元素 JSON")
    ap.add_argument("--list-my", action="store_true", help="列出 libs/ 已沉淀素材")
    ap.add_argument("--refresh", action="store_true", help="强制刷新 catalog 索引")
    args = ap.parse_args()

    if args.refresh:
        load_index(force=True)
        return
    if args.search:
        _print_search(args.search)
        return
    if args.ensure:
        path = ensure_lib(args.ensure)
        # 顺便列一下现在我的素材里有什么
        print("  我的素材当前：")
        for fn, n in list_my():
            print(f"    - {fn} ({n} 组件)")
        return
    if args.components:
        lib_path = args.components[0]
        names = args.components[1:] or None
        out = resolve_components(lib_path, names)
        print(json.dumps(out, ensure_ascii=False))
        return
    if args.list_my:
        for fn, n in list_my():
            print(f"- {fn}  ({n} 组件)")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
