# Public publisher

`publish_public.py` copies the reviewed subset of the private Obsidian vault into Quartz's `content/` directory. It stages and validates a complete replacement before atomically swapping it into place, so a rejected export cannot erase the last known-good public tree.

## Publish the current reviewed vault

```bash
python3 tools/publish_public.py \
  --vault "/Users/levibates/Library/Mobile Documents/iCloud~md~obsidian/Documents/Levi's Vault/Elections 2026 Wiki" \
  --output content
```

The publisher stages every export beside `content/`, runs the safety and manifest checks against that staged tree, and swaps it into place only after those checks pass. A rejected export leaves the last known-good `content/` tree untouched.

The publisher currently expects:

- 8 race pages under `pages/races/`
- 54 entity pages under `pages/entities/`
- 12 source pages under `pages/sources/`
- `index.md` at the vault root
- `publish/about.md`
- `publish/changelog.md`

It publishes 77 Markdown files in total, including the index and two public meta pages.

## Safety behavior

The publisher:

- Copies only Markdown from the approved directories
- Derives Quartz's public `modified` date from each note's canonical `last_updated` field
- Excludes `AGENTS.md`, `README.md`, `log.md`, `.obsidian/`, `raw/`, and private scratch content
- Scans copied content for local user paths, credential-like assignments, private-key material, `.env` references, and common token formats
- Enforces the counts in `publication-manifest.json`
- Exits nonzero when a required file, group, or safety check fails

After publishing, run:

```bash
python3 tools/publish_public.py --help
python3 tools/validate_public_content.py content
npx quartz build
```

`validate_public_content.py` checks the manifest counts, allowed public file types, private-path and credential scans, frontmatter fields, source counts, Obsidian wikilinks, relative Markdown links, accidental tool-transcript markers, and the Governor's required `[disputed]` marker. The same validation and build run in `.github/workflows/validate.yml` on pushes, pull requests, and manual dispatch.
