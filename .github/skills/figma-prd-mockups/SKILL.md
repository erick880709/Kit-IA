---
name: figma-prd-mockups
description: "Convert a functional PRD/requirements document into visual mockups and wireframes (one per screen, using the ui-ux-pro-max design system for colors/typography/style) as a mandatory design phase BEFORE any development/build skill starts writing code. Consumes the outputs of janus (functional requirements RF in resources/functional/requests/, non-functional RNF/RT in resources/architecture/definitions/, design info RD in resources/design/models/) and desglosador (user stories broken down from epics) as its primary inputs. Generates mockups in Figma (preferred, when Figma MCP is connected) or Excalidraw (built-in MCP, always available). Use this whenever the user shares a PRD, functional spec, or list of screens/user stories and asks for mockups, wireframes, prototypes, screen designs, 'diseña las pantallas', 'mockups en Figma', 'wireframes en Excalidraw', 'dibuja las pantallas', or 'antes de desarrollar' — even if they don't name a tool explicitly, as long as visual screen designs are the deliverable. Do NOT use this for pure code implementation, backend/API design, or when the user already has final visuals and only wants code."
---

# PRD to Mockups (Figma + Excalidraw)

Turns a functional PRD into visual wireframes/mockups — one per screen — grounded in a real design system, so a development skill (the "skill builder") has finished visuals and a design system to implement against instead of guessing.

This skill produces **design artifacts (Figma or Excalidraw)**, not code. It sits between requirements analysis and implementation in the full pipeline:

```
RFP / documento del cliente
        ↓
    [janus]
        ↓
resources/functional/requests/   (RF — requerimientos funcionales)
resources/architecture/definitions/ (RNF/RT — no funcionales + técnicos)
resources/design/models/         (RD — información de diseño)
        ↓
    [desglosador]  ←  (desglose de épicas Jira en historias de usuario)
        ↓
    [figma-prd-mockups]  ←  THIS SKILL
        ↓
Figma file O Excalidraw views (screens + design system)
        ↓
    [builder]  /  [genesis]
        ↓
      código
```

**Key upstream dependencies:**
- `janus` extracts structured requirements from RFPs/documents. If the project has `resources/functional/requests/` with `RF-*.md` files, read them as the primary source of truth for what screens and features exist.
- `desglosador` breaks Jira epics into granular user stories. If `desglosador` has already run, its output contains concrete user flows and acceptance criteria that map directly to screens.
- If neither has run yet, this skill can still work from a raw PRD or user-provided screen list — but the result will be only as good as the input. Consider suggesting `janus` first for ambiguous/large documents.

**Key output location:**

All design artifacts produced by this skill MUST be saved to `.github/resources/diseno/` at the project root. If the directory doesn't exist, create it before writing the first artifact.

| Artifact | File | Description |
|----------|------|-------------|
| Screen inventory | `.github/resources/diseno/inventario-pantallas.md` | Full screen list from Step 1, with purposes, entities, navigation, and states |
| Design system reference | `.github/resources/diseno/design-system.md` | Copy or summary of `MASTER.md` (palette, typography, spacing). If `MASTER.md` was generated elsewhere, link to it instead. |
| Handoff summary | `.github/resources/diseno/handoff-mockups.md` | Step 4 deliverable: tool used, screen→frame mapping, Figma link (if Path A), deferred items, open questions |
| Excalidraw exports | `.github/resources/diseno/excalidraw/` | (Path B only) One `.md` file per screen with the Excalidraw JSON or a reference to the rendered view |

This ensures `builder` and `genesis` know exactly where to find finished visuals before writing code. The `handoff-mockups.md` file is the single entry point that downstream skills should read first.

**Tool selection logic:**
- If **Figma MCP** is connected → use Figma (professional, shareable, click-through prototypes).
- If Figma MCP is **not available** → use **Excalidraw MCP** (`mcp_excalidraw_create_view`, `mcp_excalidraw_read_me`). Excalidraw produces hand-drawn-style wireframes that are perfect for early-stage mockups and design reviews.
- If neither is available → configure Excalidraw MCP first (it has no auth requirements — just add the server URL). See `## Troubleshooting`.

Never skip straight to code generation when this skill triggers — the point is to force a design checkpoint first.

## When to apply

Trigger on: a PRD, functional spec, backlog of user stories, or a plain list of screens — including the structured outputs of `janus` (`resources/functional/requests/RF-*.md`, `resources/architecture/definitions/RNF-*.md`/`RT-*.md`, `resources/design/models/RD-*.md`) and the user-story breakdown from `desglosador` — paired with a request for mockups/wireframes/prototypes/"diseño de pantallas"/"antes de que el builder desarrolle". Also trigger proactively if the user's *dev/build skill* (e.g. `arquitecto-software-senior`, `builder`, a codegen skill) is about to start implementing UI and no mockups exist yet for the screens involved — pause and offer to run this skill first.

Skip it when: the user only wants a code component from an existing design, wants copy/content only, or explicitly says they want raw HTML/React/CSS mockups instead of a design-tool artifact (that's `ui-ux-pro-max` alone, not this skill).

## Prerequisites

### Required (always)

1. **`ui-ux-pro-max` design system** — bundled in `references/ui-ux-pro-max-skill-main/`. This provides the color palette, typography scale, spacing, and style decisions. See Step 2 for usage.
   - If the bundled scripts fail (Python not available, etc.), fall back to reading the CSV data files directly from `references/ui-ux-pro-max-skill-main/src/ui-ux-pro-max/data/` and asking the user for style direction with 2-3 concrete options.

### For Figma path (preferred)

2. **Figma MCP connector**, connected with write access (Design + Dev Mode scopes). This skill uses Figma's own agent tools (`create_new_file`, `use_figma`, `get_screenshot`, `get_metadata`).
   - Figma also ships prerequisite agent skills that MUST be loaded before calling its tools: `figma-create-new-file` before `create_new_file`, and `figma-use` (+ `figma-generate-design` for full screens, `figma-use-figjam` for FigJam) before `use_figma`. Load whichever Figma provides via its skill/resource discovery before the corresponding tool call.
   - If Figma MCP is not connected, **do not block** — fall back to the Excalidraw path below.

### For Excalidraw path (fallback, always available)

3. **Excalidraw MCP** (`excalidraw-remoto`). This is a free, no-auth MCP server. Tools: `mcp_excalidraw_read_me` (read the element format reference first), `mcp_excalidraw_create_view` (render diagrams).
   - If the tools aren't visible, configure the MCP server in the user's `mcp.json`:
     ```json
     { "servers": { "excalidraw-remoto": { "url": "https://mcp.excalidraw.com/mcp" } } }
     ```
   - The user must reload the VS Code window after adding the server for tools to appear.
   - While waiting, continue with Steps 1-2 (screen inventory + design system) so no time is lost.

## Workflow

### Step 1 — Gather inputs and extract screens

**First, check for upstream artifacts.** Before parsing the PRD from scratch, look for structured inputs that `janus` and `desglosador` may have already produced:

1. **From `janus`**: Check `resources/functional/requests/` for `RF-*.md` files (functional requirements). Each RF describes a capability the system must support — many map 1:1 to screens. Also check `resources/architecture/definitions/` for `RNF-*.md` (non-functional: performance, security, UX constraints) and `RT-*.md` (technical requirements: stack, APIs, auth) — these constrain *how* screens are built. Check `resources/design/models/` for `RD-*.md` (design info: branding, existing style guides, domain entities) — these inform the visual direction.
2. **From `desglosador`**: If Jira epics have been broken down, each user story typically describes a user flow that translates to one or more screens. Look for story descriptions with acceptance criteria — these define exactly what each screen must let the user do.
3. **Fallback**: If neither `janus` nor `desglosador` has run, work from the raw PRD/document the user provided.

**Then, build a screen inventory.** Read all available sources and build a **screen inventory** before touching any design tool. For each screen capture:
- Screen name + purpose (one line)
- Primary user goal / job-to-be-done on that screen
- Key entities and actions present (list, form, table, detail view, dashboard, etc.)
- Navigation: what screen(s) it links to/from
- States worth designing: empty, loading, error, success (only include ones that matter for that screen — don't pad the list)

Write this inventory out explicitly (as markdown, in your response or a scratch file) before Step 2. If the PRD is ambiguous about how many distinct screens exist, infer a reasonable minimal set from the user flows described rather than asking — but flag any screen you inferred rather than found explicit text for.

See `references/screen-extraction.md` for extraction heuristics and a worked example.

### Step 2 — Get the design system

Derive the product type, industry, and style keywords from the PRD (e.g. "internal analytics SaaS", "consumer marketplace", "healthcare portal"), then call `ui-ux-pro-max` from the **bundled local copy**:

```bash
python "<skill-root>/references/ui-ux-pro-max-skill-main/src/ui-ux-pro-max/scripts/search.py" "<product_type> <industry> <keywords>" --design-system --persist -p "<Project Name>" --output-dir "<project-root>"
```

Where `<skill-root>` is `.github/skills/figma-prd-mockups` (resolve the absolute path at runtime — use `$PWD/.github/skills/figma-prd-mockups` or the equivalent).

This is REQUIRED before creating any frame — don't invent colors/fonts ad hoc. Use `--variance`, `--motion`, `--density` dials if the PRD signals a specific product feel (e.g. dense internal dashboard → `--density 8`).

If Python is not available or the script fails, read the design data directly from the CSV files in `references/ui-ux-pro-max-skill-main/src/ui-ux-pro-max/data/` (especially `colors.csv`, `typography.csv`, `styles.csv`, `ux-guidelines.csv`) and select an appropriate combination. If even that fails, ask the user for style direction with 2-3 concrete options (don't silently default) before proceeding.

Read the resulting `MASTER.md` (or your CSV-derived selection) — palette, type scale, spacing scale, and the named UI style — this is what every frame in Step 3 must follow, regardless of whether you use Figma or Excalidraw.

### Step 3 — Build the mockups

Choose the path based on tool availability (checked in Prerequisites):

#### Path A: Figma (when Figma MCP is connected)

1. Create one new Figma **Design** file for the project (via `figma-create-new-file` → `create_new_file`). Name it after the project.
2. For each screen in the inventory, build a frame at a standard breakpoint (state which one — e.g. 1440px desktop or 390px mobile, based on what the PRD implies) using `use_figma`, applying:
   - The color palette and typography from `MASTER.md` as real Figma styles/variables, not one-off hex values per layer.
   - The layout pattern and component choices implied by the screen's purpose (list, form, dashboard, etc.) — reference `ui-ux-pro-max`'s `product`/`ux` domains for the specific pattern if unsure.
   - Real, plausible placeholder content — not "Lorem ipsum" or "Button 1" — so the mockup reads like the actual product.
3. Wire simple navigation between frames where the PRD describes a flow (e.g. list → detail), so the file is click-through, not just static screens.
4. After each frame, call `get_screenshot` to visually verify it before moving to the next screen — don't batch all screens blind and check at the end.
5. Keep frame and layer names meaningful (`Login / Default`, `Dashboard / Empty state`) — the dev skill will read these names later.

#### Path B: Excalidraw (when Figma MCP is NOT connected — always available)

1. Call `mcp_excalidraw_read_me` first to get the Excalidraw element format reference (colors, shapes, element types). Do this once before building any screen.
2. For each screen in the inventory, build one Excalidraw view via `mcp_excalidraw_create_view`, applying:
   - The color palette from `MASTER.md` mapped to the closest Excalidraw palette colors (use the stroke/fill properties).
   - Typography indicated via text elements with the font family and size from the design system.
   - Layout using Excalidraw rectangles, diamonds (for decision points), arrows (for navigation/flows), and text labels — keep the hand-drawn wireframe aesthetic.
   - Real, plausible placeholder content — same standard as Figma: no "Lorem ipsum", use realistic sample data.
3. For navigation flows between screens, use arrows connecting labeled boxes that represent each screen (a simple user-flow diagram supplementing the per-screen wireframes).
4. Excalidraw views render incrementally with draw-on animation — verify each screen visually after creation.
5. Name each view clearly in your response so the user can identify which screen is which.

#### Common rules for both paths

- Build screens in priority order: core/primary flow first, secondary and edge-state screens after.
- If the PRD implies more than ~8-10 screens, confirm scope with the user rather than silently designing all of them.
- For each screen, design the states that matter (empty, loading, error, success) — not all states apply to every screen, use judgment.

### Step 4 — Save artifacts and produce handoff

**First, ensure the output directory exists.** Create `.github/resources/diseno/` at the project root if it doesn't already exist. For Excalidraw Path B, also create `.github/resources/diseno/excalidraw/`.

**Save the screen inventory** from Step 1 as `.github/resources/diseno/inventario-pantallas.md`. This is the canonical list of screens — downstream skills will reference it.

**Save the design system reference** as `.github/resources/diseno/design-system.md`. If `ui-ux-pro-max` generated a `MASTER.md` elsewhere, copy or summarize the key decisions (palette name, font pair, spacing scale, UI style) into this file so the design context stays with the mockups.

**Save the handoff summary** as `.github/resources/diseno/handoff-mockups.md`. This is the single entry point for downstream skills. It must contain:
- **Tool used:** Figma file link (if Path A) or confirmation that Excalidraw views were rendered (if Path B)
- **Screen → frame/view name mapping**
- **Design system source** (path to `MASTER.md` or note that CSV data was used directly)
- **Paths to all saved artifacts** (inventory, design system, Excalidraw exports if any)
- **Anything explicitly deferred** (states not designed, screens inferred rather than specified, open questions for the user)

**For Excalidraw Path B**, also save each screen's Excalidraw JSON or a descriptive reference as `.github/resources/diseno/excalidraw/<nombre-pantalla>.md` so the views are traceable to files.

This handoff is what the dev/build skill should read before writing code — say so explicitly to the user so they carry it into that next step. Do not start implementation code yourself in this same pass; the checkpoint is the point.

## Gotchas

- **Never** use "Lorem ipsum" or generic placeholder labels like "Button 1" — every text element must use realistic sample data that reads like the actual product. Generic placeholders make mockups useless for stakeholder review.
- **Never** invent colors, fonts, or spacing ad-hoc. Always derive them from `ui-ux-pro-max` (Step 2). If that fails, ask the user — don't silently default to system fonts and browser-default blues.
- **Never** reproduce a competitor's or real brand's proprietary UI pixel-for-pixel from a screenshot they provide — use it as style reference only, not for copying copyrighted assets.
- **Excalidraw element format is strict JSON** — no comments, no trailing commas. Always call `mcp_excalidraw_read_me` before building the first screen to confirm the exact schema.
- **Figma prerequisite skills must be loaded first** — calling `create_new_file` without loading `figma-create-new-file` first will fail. Figma enforces this; it's not optional.
- If the user pushes to skip straight to code ("just build it, skip the mockups"), that's their call — don't insist, but say plainly what's being skipped (no visual sign-off before implementation).

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Figma MCP tools not found | Fall back to **Path B (Excalidraw)**. Do not block the workflow — Excalidraw wireframes are a valid deliverable. |
| Excalidraw MCP tools not found | Configure the server in `mcp.json`: add `"excalidraw-remoto"` with URL `https://mcp.excalidraw.com/mcp`. User must reload VS Code. Continue with Steps 1-2 while waiting. |
| `ui-ux-pro-max` Python script fails | Read CSV files directly from `references/ui-ux-pro-max-skill-main/src/ui-ux-pro-max/data/`. Match product type → pick a style from `styles.csv`, palette from `colors.csv`, fonts from `typography.csv`. |
| Python not installed at all | Read the CSV data files with the file reader tool and manually select design tokens. Ask user for confirmation on the chosen palette + font pairing. |
| Excalidraw JSON parse error | Check for trailing commas, comments (`//` or `/* */`), or unquoted keys. The format is strict JSON. Validate with a JSON linter mentally before calling `create_view`. |
| Excalidraw render looks wrong (overlapping, off-screen) | Adjust element `x`/`y` coordinates — Excalidraw uses a canvas coordinate system. Keep elements spaced at least 100px apart. Use `boundElements` for arrows connecting boxes. |
| User wants Figma but can't connect | Explain the Figma MCP setup briefly (they need a Figma account + connector). Offer to proceed with Excalidraw in the meantime — the design system and screen inventory are reusable regardless of tool. |

## References

Bundled with this skill:

| File | Purpose | When to read |
|------|---------|--------------|
| `references/screen-extraction.md` | Heuristics and worked example for extracting a screen inventory from a PRD | Step 1 — before listing screens |
| `references/ui-ux-pro-max-skill-main/` | Full `ui-ux-pro-max` design system (scripts, CSV data, templates). Use `src/ui-ux-pro-max/scripts/search.py` to generate a `MASTER.md`, or read `src/ui-ux-pro-max/data/` CSVs directly as fallback. | Step 2 — before designing any frame |

External references:
- [Excalidraw MCP documentation](https://mcp.excalidraw.com/mcp) — element format and API reference
- [ui-ux-pro-max CLI docs](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) — full usage of the design system tool
