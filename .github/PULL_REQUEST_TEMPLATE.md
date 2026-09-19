## 变更说明 / What changed

简要描述本 PR 做了什么、为什么。
Briefly describe what this PR does and why.

## 关联 / Related

- 关闭 / Closes #（issue 编号 · issue number）

## 检查清单 / Checklist

- [ ] 若改了 `references/` 下内容，**文内交叉引用仍成立**（路径、文件名未悬空）
      If `references/` changed, in-file cross-references still resolve (no dangling paths or filenames).
- [ ] 若改了 `SKILL.md` 的 **frontmatter**：`name` 仍匹配目录名、`description` ≤1024 字符、`agent_created: true` 保留、未引入规范外键
      If `SKILL.md` frontmatter changed: `name` still matches the folder, `description` ≤1024 chars, `agent_created: true` kept, no out-of-spec keys.
- [ ] 若动了 `scripts/`：Python 脚本通过 `python -m py_compile`、`.cjs` 通过 `node --check`，并实跑过一次
      If `scripts/` changed: `.py` passes `py_compile`, `.cjs` passes `node --check`, and the script was actually run.
- [ ] 若新增**外部依赖**：已在 `README` 的「运行要求」与对应 `references/*.md` 中写明安装方式
      If a new external dependency is introduced: install steps are documented in the README Requirements and the relevant `references/*.md`.
- [ ] 若改了**对外文案**：无夸大表述、无内部代号 / 内部路径、无未经验证的客户端承诺
      If public-facing copy changed: no overstatement, no internal codenames or paths, no unverified client claims.
- [ ] 若涉及**版本相关**改动：`CHANGELOG.md` 与 `plugin.json` 的版本一致
      If version-related: `CHANGELOG.md` and `plugin.json` versions agree.
- [ ] 已按 [Keep a Changelog](https://keepachangelog.com/1.1.0/) 惯例更新 `CHANGELOG.md`（如适用）
      `CHANGELOG.md` updated following Keep a Changelog (if applicable).

## 备注 / Notes

设计决策、兼容性影响、后续计划等。
Design decisions, compatibility impact, follow-up plans, etc.
