#!/usr/bin/env node
/**
 * render_preview.cjs — 把 .excalidraw 渲染成「真实手绘风」SVG 预览
 * ================================================================
 * 为什么需要它：Agent 自动生成的 .excalidraw 文件，用户若不导入 KaiBoard 就看不到
 * 真实手绘效果（之前只能给一张「结构示意」SVG，看着很业余）。本脚本用 roughjs
 * （Excalidraw 内部同一套手绘渲染引擎）直接把元素画成 SVG，效果与 KaiBoard 内一致。
 *
 * 用法：
 *   node render_preview.cjs input.excalidraw -o out.svg
 *   node render_preview.cjs *.excalidraw                      # 每个生成同名 .svg
 *
 * 不依赖浏览器 / jsdom：roughjs generator() 纯算 path，我们手动把 op 集转成 SVG <path>。
 */
const fs = require("fs");
const path = require("path");

// 可移植加载 roughjs（不要写死本机绝对路径）：
// 1) 常规解析  2) 显式 bundled 子路径  3) 脚本目录下的 node_modules
const rough = (() => {
  for (const t of ["roughjs", "roughjs/bundled/rough.cjs.js"]) {
    try { return require(t); } catch (_) {}
  }
  try {
    return require(path.join(__dirname, "node_modules", "roughjs", "bundled", "rough.cjs.js"));
  } catch (_) {}
  console.error(
    "render_preview.cjs: 需要 roughjs 才能渲染预览。请先安装：\n" +
    "  npm i roughjs\n" +
    "（或在已安装 roughjs 的目录下运行本脚本）"
  );
  process.exit(2);
})();
const RC = rough.generator();

// roughjs op 集 → SVG path d 字符串（roughjs 的 op 是字符串："move"/"lineTo"/"bcurveTo"）
function opsToPath(ops) {
  let d = "";
  for (const op of ops) {
    const a = op.data;
    switch (op.op) {
      case "move": d += `M${a[0]} ${a[1]} `; break;
      case "lineTo": d += `L${a[0]} ${a[1]} `; break;
      case "bcurveTo": d += `C${a[0]} ${a[1]}, ${a[2]} ${a[3]}, ${a[4]} ${a[5]} `; break;
      default: break;
    }
  }
  return d.trim();
}

function elOptions(el) {
  const o = {
    roughness: el.roughness ?? 1,
    stroke: el.strokeColor || "#1e1e1e",
    strokeWidth: el.strokeWidth ?? 1,
    seed: el.seed ?? 1,
    preserveVertices: true,
    bowing: 1,
  };
  const bg = el.backgroundColor;
  if (bg && bg !== "transparent") {
    o.fill = bg;
    o.fillStyle = el.fillStyle || "hachure";
    o.hachureGap = el.hachureGap ?? 8;
    o.fillWeight = el.fillWeight ?? 1.5;
  }
  if (el.strokeStyle === "dashed") o.strokeLineDash = [9, 7];
  else if (el.strokeStyle === "dotted") o.strokeLineDash = [2, 7];
  return o;
}

function shapeFor(el) {
  const opt = elOptions(el);
  const x = el.x, y = el.y, w = el.width, h = el.height;
  switch (el.type) {
    case "rectangle":
      return RC.rectangle(x, y, w, h, opt);
    case "ellipse":
      return RC.ellipse(x + w / 2, y + h / 2, w, h, opt); // roughjs 椭圆用中心
    case "diamond":
      return RC.polygon(
        [[x + w / 2, y], [x + w, y + h / 2], [x + w / 2, y + h], [x, y + h / 2]],
        opt
      );
    default:
      return null;
  }
}

// 直线 / 箭头：Excalidraw 的 points 是相对元素 (x,y) 的偏移
function lineFor(el) {
  const opt = elOptions(el);
  const pts = (el.points || [[0, 0]]).map(([px, py]) => [el.x + px, el.y + py]);
  if (pts.length < 2) return [];
  if (pts.length === 2) return [RC.line(pts[0][0], pts[0][1], pts[1][0], pts[1][1], opt)];
  return [RC.linearPath(pts, opt)];
}

// 箭头头部（手工两支短线）
function arrowHead(el) {
  const pts = (el.points || [[0, 0], [1, 1]]).map(([px, py]) => [el.x + px, el.y + py]);
  const n = pts.length;
  const [ex, ey] = pts[n - 1];
  const [px, py] = pts[n - 2];
  const ang = Math.atan2(ey - py, ex - px);
  const size = 14;
  const a1 = ang + Math.PI - Math.PI / 7;
  const a2 = ang + Math.PI + Math.PI / 7;
  const headOpt = { stroke: el.strokeColor || "#343a40", strokeWidth: el.strokeWidth ?? 2, seed: el.seed ?? 1, roughness: 1 };
  return [
    RC.line(ex, ey, ex + size * Math.cos(a1), ey + size * Math.sin(a1), headOpt),
    RC.line(ex, ey, ex + size * Math.cos(a2), ey + size * Math.sin(a2), headOpt),
  ];
}

function drawableToSvg(d, opt) {
  let s = "";
  for (const set of d.sets) {
    const dd = opsToPath(set.ops);
    if (!dd) continue;
    if (set.type === "fillPath") {
      s += `<path d="${dd}" fill="${opt.fill || "none"}" stroke="none"/>`;
    } else if (set.type === "fillSketch") {
      s += `<path d="${dd}" fill="none" stroke="${opt.fill || "#000"}" stroke-width="${opt.fillWeight || 1.2}" stroke-linecap="round"/>`;
    } else {
      const dash = opt.dash ? ` stroke-dasharray="${opt.dash.join(",")}"` : "";
      s += `<path d="${dd}" fill="none" stroke="${opt.stroke}" stroke-width="${opt.sw || 1.5}" stroke-linecap="round" stroke-linejoin="round"${dash}/>`;
    }
  }
  return s;
}

function esc(t) {
  return String(t).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function textSvg(el) {
  const size = el.fontSize || 16;
  const lines = String(el.text || "").split("\n");
  const cx = el.x + el.width / 2;
  const lineH = size * 1.25;
  const totalH = lines.length * lineH;
  const startY = el.y + el.height / 2 - totalH / 2 + lineH * 0.38;
  const color = el.strokeColor || "#1e1e1e";
  // 近似 Virgil 手写体：能加载就用 Comic Sans/Comic Neue，否则走 cursive 兜底
  const ff = "'Comic Sans MS','Comic Neue',Virgil,cursive";
  const tspans = lines
    .map((ln, i) => `<tspan x="${cx}" y="${(startY + i * lineH).toFixed(1)}">${esc(ln)}</tspan>`)
    .join("");
  return `<text x="${cx}" y="${startY.toFixed(1)}" font-family="${ff}" font-size="${size}" fill="${color}" text-anchor="middle">${tspans}</text>`;
}

function render(excalidrawPath) {
  const data = JSON.parse(fs.readFileSync(excalidrawPath, "utf-8"));
  const els = data.elements || [];
  let body = "";
  for (const el of els) {
    if (el.isDeleted) continue;
    if (el.type === "text") {
      body += textSvg(el);
    } else if (el.type === "arrow" || el.type === "line") {
      for (const d of lineFor(el)) body += drawableToSvg(d, { stroke: el.strokeColor, sw: el.strokeWidth, fill: el.backgroundColor, fillWeight: el.fillWeight, dash: elOptions(el).strokeLineDash });
      if (el.type === "arrow" && el.endArrowhead) for (const d of arrowHead(el)) body += drawableToSvg(d, { stroke: el.strokeColor, sw: el.strokeWidth });
    } else {
      const d = shapeFor(el);
      if (d) body += drawableToSvg(d, { stroke: el.strokeColor, sw: el.strokeWidth, fill: el.backgroundColor, fillWeight: el.fillWeight });
    }
  }

  // 计算包围盒
  let minx = Infinity, miny = Infinity, maxx = -Infinity, maxy = -Infinity;
  for (const el of els) {
    if (el.isDeleted) continue;
    const x2 = el.x + (el.width || 0), y2 = el.y + (el.height || 0);
    minx = Math.min(minx, el.x); miny = Math.min(miny, el.y);
    maxx = Math.max(maxx, x2); maxy = Math.max(maxy, y2);
  }
  if (!isFinite(minx)) { minx = 0; miny = 0; maxx = 800; maxy = 600; }
  const pad = 48;
  minx -= pad; miny -= pad; maxx += pad; maxy += pad;
  const W = maxx - minx, H = maxy - miny;
  const bg = (data.appState && data.appState.viewBackgroundColor) || "#ffffff";

  const svg =
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${minx.toFixed(0)} ${miny.toFixed(0)} ${W.toFixed(0)} ${H.toFixed(0)}" width="${W.toFixed(0)}" height="${H.toFixed(0)}">` +
    `<rect x="${minx.toFixed(0)}" y="${miny.toFixed(0)}" width="${W.toFixed(0)}" height="${H.toFixed(0)}" fill="${bg}"/>` +
    body +
    `</svg>`;
  return svg;
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) { console.error("usage: node render_preview.cjs file.excalidraw [-o out.svg]"); process.exit(1); }
  let out = null;
  const files = [];
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "-o") out = args[++i];
    else files.push(args[i]);
  }
  if (out && files.length === 1) {
    fs.writeFileSync(out, render(files[0]), "utf-8");
    console.log(`[ok] ${out}`);
  } else {
    for (const f of files) {
      const o = f.replace(/\.excalidraw$/, ".svg");
      fs.writeFileSync(o, render(f), "utf-8");
      console.log(`[ok] ${o}`);
    }
  }
}
main();
