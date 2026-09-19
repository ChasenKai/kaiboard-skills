---
name: Bug report
about: 报告一个可复现的问题 / Report a reproducible issue
title: "[Bug] "
labels: bug
assignees: ''
---

**描述 / Description**
简明描述你遇到的问题。
Briefly describe the problem you encountered.

**复现步骤 / Steps to reproduce**
1.
2.
3.

**期望行为 / Expected behavior**
应该发生什么。
What should happen.

**实际行为 / Actual behavior**
实际发生了什么（如有报错文本 / 截图请一并贴上）。
What actually happened (attach error text / screenshots if available).

**环境 / Environment**
- 你使用的客户端 / Your client（WorkBuddy / Claude Code / Codex / Cursor / 其他 · other）:
- Skill 版本 / Skill version（本仓 tag 或 commit · this repo's tag or commit）:
- Python 版本 / Python version（`python --version`）:
- Node.js 版本 / Node.js version（`node -v`，仅预览相关 · preview only）:
- 是否已安装 roughjs / Is `roughjs` installed（`npm i roughjs`）:
- 操作系统 / OS:

**模式 / Mode**
- [ ] **Mode A · 实时共绘** / Live co-draw —— 请附：KaiBoard 页面是否打开且已启用「Agent 共绘」？
      Is the KaiBoard page open with "Agent co-draw" enabled?
- [ ] **Mode B · 文件** / File output —— 出的是 `.excalidraw`，未连画布 / produced a `.excalidraw` file, no board connection

**诊断信息 / Diagnostics**

若为「落板后元素位置不对 / 箭头穿框」，请附 `geometry_check.py` 的输出：
If elements land in the wrong place or arrows cross boxes, paste the output of `geometry_check.py`:

```bash
python skills/kaiboard-draw/scripts/geometry_check.py <你的图>.excalidraw
```

若为「画面与预览不一致」，请同时附上 `.excalidraw` 与渲染出的 `.svg`。
If the board looks different from the preview, attach both the `.excalidraw` and the rendered `.svg`.
