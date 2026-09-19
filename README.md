# KaiBoard Skills

**English** | [简体中文](./README.zh-CN.md)

Official skills for [KaiBoard](https://kaiboard.kaibuddy.com) — a local-first, open-source whiteboard built on Excalidraw.

These skills teach an AI agent **how to draw on your KaiBoard whiteboard**: which of the two collaboration paths to take, how to compose a diagram well, and how to land elements safely on your canvas.

> ⚠️ **Status — please read first**
> - **Goal**: work with any client that supports Agent Skills and MCP.
> - **What's actually verified**: so far, chiefly on **WorkBuddy**. **On other clients, please verify and tune it yourself** — tool exposure and connection behaviour differ between clients, and that is expected.
> - **Stage**: early / preview. Interfaces and content may change; not recommended for critical workflows yet.
> - **Feedback**: issues and suggestions are welcome. We will not describe an unverified client as "supported".

## What's inside

| Skill | What it does |
|---|---|
| [`kaiboard-draw`](./skills/kaiboard-draw/) | Draw on KaiBoard. **Live co-draw** (drives the board you already have open) or **file output** (generate an editable `.excalidraw` to import later). |

## Install

### Option A — copy the skill folder

Any agent that reads the [Agent Skills](https://agentskills.io) spec can load it. Clone and drop the skill folder where your agent looks for skills:

```bash
git clone https://github.com/ChasenKai/kaiboard-skills.git
cp -r kaiboard-skills/skills/kaiboard-draw ~/.claude/skills/     # path varies per client
```

### Option B — as an Agent Plugin

This repo is also an [Agent Plugin](https://agent-plugins.org): it ships a `plugin.json` manifest plus an `mcp.json`. Clients implementing that format discover **both the skill and its companion MCP server** from this one repository.

The companion MCP server is [`@kaibuddy/kaiboard-mcp`](https://www.npmjs.com/package/@kaibuddy/kaiboard-mcp) — it talks straight to a KaiBoard board you have open in your browser.

## Configure

Live co-drawing needs a token, which KaiBoard generates for you:

1. Open KaiBoard in your browser and open the board you want to work on.
2. Open settings and turn on **Agent co-draw**.
3. Copy the token shown there.

Then set it in `mcp.json` (replace the placeholder):

```json
"env": { "KAIBOARD_TOKEN": "<your token here>" }
```

> **Credentials are not shipped with this repo.** The placeholder is intentional — the token is personal to your machine and your KaiBoard session. Don't commit it or share it.

> 📄 Step-by-step setup and troubleshooting live in [`skills/kaiboard-draw/SETUP.md`](./skills/kaiboard-draw/SETUP.md).

## Requirements

- **Live co-draw**: KaiBoard open in a browser with _Agent co-draw_ enabled, plus the MCP server configured. The agent and the browser must be on the same machine.
- **File output**: no KaiBoard connection needed — you get a `.excalidraw` file to import whenever you like.
- **Python 3** for the bundled helper scripts.
- **Node.js** + [`roughjs`](https://www.npmjs.com/package/roughjs) (`npm i roughjs`) — needed only for the hand-drawn SVG preview. That preview is the mandatory checkpoint before anything lands on a board, so treat it as a real requirement, not an optional extra. See [`skills/kaiboard-draw/SETUP.md`](./skills/kaiboard-draw/SETUP.md).

## Contributing & maintenance

- New findings are validated on a working branch first; once stable they are proposed as a PR and released following this repo's [semantic versioning](./CHANGELOG.md).
- When editing anything under `skills/`, re-check that cross-references inside `references/` still hold.

## Credits

This repo stands on the work of others — the Excalidraw element schema and its community icon libraries, the roughjs hand-drawn rendering engine, and the public Agent Skills / Agent Plugins specifications. See [CREDITS.md](./CREDITS.md) for the full list.

## License

[MIT](./LICENSE). Community icon libraries fetched on demand are third-party works under their own licenses; this repo does **not** redistribute them.
