# South Carolina Elections 2026 Wiki

A Quartz-powered public site for an independent, source-first research wiki covering South Carolina's 2026 elections, with particular attention to Anderson County and Pendleton-area races.

**Live site:** https://bobafett235.github.io/elections-2026-wiki/

## Publication model

The canonical research workspace is a private Obsidian vault. This repository is a filtered public mirror. Only reviewed Markdown content belongs under `content/`.

The public site is not an official election website. Candidate status, ballot information, election results, and campaign-finance figures should be checked against the linked official records, including SC Votes, county election offices, the Federal Election Commission, and the South Carolina Ethics Commission.

## Source hierarchy

1. Official election and government records
2. Official candidate and campaign statements, clearly attributed
3. Reputable journalism
4. Secondary databases and election analysis

The site preserves uncertainty markers such as `[disputed]`, `[unverified]`, and `[needs-source]`. Volatile figures should carry a reporting period or access date.

## Local development

Requirements:

- Node.js 22 or newer
- npm 10.9.2 or newer

Install dependencies and build:

```bash
npm ci
npx quartz plugin install --from-config
npx quartz build
```

Preview locally:

```bash
npx quartz build --serve
```

The local preview is served at `http://localhost:8080`.

## Content boundary

The public build will intentionally exclude the private Obsidian configuration, internal instructions, raw research files, temporary drafts, and personal metadata. A controlled publisher will copy only approved files from the private vault into `content/`.

## Validation and CI

Before a public change is committed, run the publisher, public-content validator, and Quartz build. The validator checks the publication manifest, frontmatter, source counts, internal links, private-content patterns, accidental transcripts, and preserved uncertainty markers.

```bash
python3 tools/validate_public_content.py content
npx quartz build
```

GitHub Actions repeats those validation and build checks on pushes, pull requests, and manual dispatches. The Pages workflow deploys only from `main` after the same checks pass.

## Status

The public repository is initialized at [github.com/bobafett235/elections-2026-wiki](https://github.com/bobafett235/elections-2026-wiki). Reviewed election content, the controlled publisher, public-content validation, and GitHub Pages workflows are present. The private Obsidian vault remains canonical.
