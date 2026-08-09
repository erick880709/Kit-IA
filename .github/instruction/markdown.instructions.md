---
description: 'Unified Markdown authoring and review standard for every skill in this kit — syntax (CommonMark + GFM), document structure, and accessibility. Consolidates markdown.instructions.md, markdown-gfm.instructions.md, markdown-content-creation.instructions.md and markdown-accessibility.instructions.md into one baseline all skills follow when writing or reviewing .md deliverables.'
applyTo: '**/*.md'
---

# Markdown Authoring Standard

This file is the single source of truth for how **any skill in this kit** writes
or reviews a `.md` file — architecture documents, RF/RNF/RT/RD, ADRs, historias
de usuario, planes de prueba, resúmenes ejecutivos, mockup specs, etc. It
replaces the need for each skill to redefine markdown formatting rules on its
own: `janus`, `refinador`, `archi`, `genesis`, `desglosador`, `figma-prd-mockups`,
`builder`, `qa` (and any skill added later, including the review/security
skills planned next) all produce markdown under `resources/`, and all of it
must meet this same bar. This is a **baseline, not a ceiling** — a skill may
add its own template/frontmatter fields on top of this file, but it may not
violate what's defined here.

Source references consolidated here: CommonMark spec 0.31.2, the GFM spec,
GitHub's accessible-documentation guidance, and general content-creation
formatting rules. Specs are for reference only — do not fetch or download
them at runtime.

---

## 1. Scope and precedence

- Applies to every `.md` file this kit generates or edits, regardless of
  which skill produced it or which `resources/<subfolder>/` it lives in.
- If a skill's own template conflicts with this file on **syntax or
  accessibility**, this file wins. If it conflicts on **domain content**
  (e.g. which sections an ADR must contain), the skill's template wins —
  this file governs *how* content is written, not *what* content a
  document must contain.
- One deliberate adaptation vs. the original blog-oriented source: our
  documents are not CMS posts with an externally generated title, so
  **every document must have exactly one H1**, used as its title (see §3).
  Do not follow a "no H1, it's auto-generated" rule here — that only
  applied to the blog-publishing context the original guidance came from.

## 2. Core syntax (CommonMark + GFM)

Every skill writes valid, unambiguous Markdown — not "close enough" text
that happens to render right in one previewer.

- **Headings**: ATX style only (`#` … `######`), 1–6 `#` followed by a
  space. Never Setext (`===`/`---` underlines). Never skip a level
  (`##` → `####` is a violation) — go one level at a time.
- **Emphasis**: `*text*` / `**text**` for italics/bold. Use `_` only at
  word boundaries, never mid-word. Don't rely on emphasis alone to convey
  critical meaning (see §4 — screen readers often don't announce it).
- **Code**: inline code in single backticks. Fenced blocks with triple
  backticks, **always with a language identifier**
  (` ```typescript `, ` ```bash `, ` ```json `, ` ```mermaid `, etc.) —
  never an unlabeled fence for real code or config.
- **Lists**: `-` for bullets (consistent within a document — don't mix
  `-`, `*`, `+` in the same list). `1.` for ordered lists. Nested lists
  indented to the parent's content column (2 spaces after `-`). Use
  `- [ ]` / `- [x]` (GFM task lists) for actionable checklists like
  acceptance criteria — never emoji or plain-text bullets standing in
  for real list syntax (see §4).
- **Links**: `[descriptive text](url)`. Never a bare URL in prose — wrap
  it. Never open in a new tab/window (no `target="_blank"` in raw HTML
  inside markdown).
- **Images**: `![alt text](path "optional title")`. Alt text is
  mandatory — see §4.2.
- **Tables** (GFM extension): header row + delimiter row (`---`, `:---:`,
  `---:` for alignment) + data rows, matching column counts. Tables are
  for **tabular data only** — never for page/document layout. Avoid
  nested tables and avoid tables so complex they can't be represented
  accessibly in plain markdown (split them instead).
- **Strikethrough** (GFM extension): exactly `~~text~~` — two tildes,
  never three or more.
- **Line endings**: a single trailing newline breaks a line softly
  (renders as a space); two-or-more trailing spaces or a trailing `\`
  force a hard break. Don't rely on invisible trailing whitespace for
  intentional line breaks — prefer restructuring into separate
  paragraphs or a list.
- **Raw HTML**: allowed only when Markdown genuinely can't express the
  need (e.g. a `<details>` block for a long image description, see
  §4.2). Never use disallowed/dangerous raw tags (`<script>`, `<style>`,
  `<iframe>`, `<title>`, `<textarea>`, `<xmp>`, `<noembed>`,
  `<noframes>`, `<plaintext>`).

## 3. Document structure

- **One H1 per document**, used as the document's title, first line of
  real content (after frontmatter). Everything else starts at H2.
- **Frontmatter**: every generated `.md` deliverable starts with YAML
  frontmatter. Exact fields depend on the producing skill's own template
  (e.g. `archi` includes proyecto/escenario/fecha; `janus` includes
  tipo/ID/origen-RFP), but at minimum every frontmatter block includes:
  `title`, `skill` (which skill produced it), and `date`. Don't invent
  blog-specific fields (`post_slug`, `microsoft_alias`, `categories`)
  that don't apply to this kit's documents.
- **Heading hierarchy**: logical and sequential, never skips a level.
  Never use **bold text** as a stand-in for a missing heading level.
- **Paragraphs**: short. Prefer breaking a long, dense paragraph into
  bullets or shorter paragraphs over one wall of text.
- **Whitespace**: one blank line between blocks (headings, paragraphs,
  lists, code fences). No multiple consecutive blank lines.
- **Line length**: soft-wrap prose around 80–100 characters per line for
  diffability in git; never a hard technical limit that breaks a link,
  a table row, or a code line — those stay on one line regardless of
  length.

## 4. Accessibility (mandatory, not optional polish)

Every skill that writes a `.md` deliverable is responsible for these —
not just `front`/`figma-prd-mockups`. A requirements document or an ADR
is read by people too, some of them using assistive technology.

### 4.1 Descriptive links
- Never "click here", "here", "this", "read more", or a bare link as the
  only text. Link text must make sense read out of context — screen
  readers can list all links on a page in isolation.
- Never reuse identical link text for two links pointing to different
  destinations in the same document.

### 4.2 Image alt text
- Never an empty `![]()` unless the image is genuinely decorative.
- Never a filename or generic placeholder (`img_01.png`, `screenshot`,
  `diagram`) as alt text.
- Alt text is succinct but describes what's actually in the image,
  including visible text. Use "screenshot of…" where relevant; don't
  prefix with "image of…" (screen readers already announce that).
- For complex images this kit produces a lot of — C4 diagrams, sequence
  diagrams, deployment diagrams, cost charts — summarize the key
  takeaway in the alt text, and put the full breakdown in the
  surrounding prose or a `<details>` block, not only in the image.
- Alt text is a **recommendation the author/skill proposes**, not a
  silent auto-fill — flag it for review rather than asserting it's
  final, since it requires visual judgment.

### 4.3 Plain language
- Prefer short sentences, common words, active voice over
  jargon-heavy phrasing — including in architecture and requirements
  documents, where dense language is the norm but isn't a virtue.
- When documenting a UI navigation path (common in `figma-prd-mockups`
  and `builder` deliverables), write it as plain sequential steps first
  ("abre Configuración, luego selecciona Preferencias"), not as an icon
  name or a breadcrumb symbol. A parenthetical visual cue can follow
  ("(ícono de engranaje > Preferencias)") but never stand alone as the
  only description.
- Treat plain-language rewrites as recommendations for the author to
  confirm, same as alt text — tone and audience are judgment calls.

### 4.4 Lists and emoji
- Sequential items always use real list syntax (`-`, `1.`), never emoji
  or symbols standing in for bullets, and never plain-text sentences
  that are actually a list in disguise.
- No consecutive strings of emoji (each is read aloud in full by a
  screen reader). If emoji are used at all, use them sparingly and
  never as the sole carrier of meaning — pair with text.

### 4.5 Multimedia
- Any embedded video/audio needs captions or a transcript.
- No autoplay. Animated content should not auto-play on load.

## 5. Review priority

When a skill or a human reviews an existing `.md` file against this
standard, fix issues in this order:

1. Missing/empty/placeholder image alt text
2. Skipped heading levels or broken heading hierarchy (including
   missing/duplicate H1)
3. Non-descriptive link text or bare URLs
4. Emoji or plain text used as list markers instead of real list syntax
5. GFM table malformation (mismatched columns, tables used for layout)
6. Plain-language / jargon simplification opportunities
7. Multimedia captioning
8. Everything else in the validation checklist (§6)

## 6. Validation checklist

- [ ] Exactly one H1, used as the document title; no skipped heading
      levels anywhere below it.
- [ ] Every fenced code block declares a language.
- [ ] Every link uses descriptive text; no bare URLs in prose; no two
      links with identical text pointing elsewhere.
- [ ] Every image has real alt text (not empty, not a filename, not a
      generic placeholder).
- [ ] Lists use `-`/`1.`/`- [ ]` syntax — never emoji or prose standing
      in for a list.
- [ ] Tables have matching header/delimiter/data column counts and are
      used only for tabular data, not layout.
- [ ] No bold text used as a substitute for a real heading.
- [ ] No disallowed raw HTML tags.
- [ ] Frontmatter present with at minimum `title`, `skill`, `date`.
- [ ] No links set to open in a new tab/window.

## 7. How skills apply this file

- Any skill whose output includes a `.md` file (this is nearly all of
  them) treats this file as a shared dependency, the same way `builder`
  treats `archi`'s architecture document as a dependency — read it once
  per session before generating markdown, not on every single file.
- If your editor/agent runtime honors the `applyTo` glob in this file's
  frontmatter (e.g. GitHub Copilot custom instructions in VS Code), it
  is applied automatically to every `.md` file without any change to
  the individual `SKILL.md` files. When running skills through an agent
  that does **not** auto-load `.github/instruction/*.instructions.md` by
  glob, each skill should explicitly reference this file (one line is
  enough, e.g. "sigue `.github/instruction/markdown.instructions.md`
  para el formato del entregable") so the persona knows to load and
  follow it before writing.
- This file does not replace per-skill output templates (e.g.
  `archi/references/plantilla-documento-arquitectura.md`). It sits
  underneath them: the template says *what sections* a document needs;
  this file says *how* every section, link, list, image, and heading in
  that template must be written.
