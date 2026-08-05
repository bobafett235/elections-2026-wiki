---
tags: [meta]
aliases: [Public changelog]
status: evergreen
last_updated: 2026-08-04
source_count: 0
confidence: high
sources: []
modified: 2026-08-04
---
# Public changelog

## 2026-08-04: Public-content validation added

- Added a repeatable validation gate for the reviewed public Markdown export.
- The gate checks publication counts, frontmatter, source counts, internal links, private-content patterns, accidental transcripts, and preserved uncertainty markers before a Quartz build.
- Added GitHub Actions validation for pushes, pull requests, and manual runs. This workflow validates and builds but does not deploy the site.

## 2026-08-04: Markdown compatibility pass

- Replaced Obsidian wikilinks with aliases inside Markdown table cells with standard relative Markdown links where Quartz would otherwise interpret the alias separator as a table column.
- Verified the corrected County Council, Anderson SD4, and U.S. House overview tables in the rendered site.
- Checked 131 internal references across the 70-page public export: 126 Obsidian wikilinks and 5 relative Markdown links; no broken targets remained.

## 2026-08-04: Public publication layer initialized

- Created the Quartz 5 website scaffold for the South Carolina Elections 2026 Wiki.
- Added the public source hierarchy and uncertainty policy.
- Defined a private-vault to public-repository publication boundary.
- Election race and candidate pages will be added only after the controlled publisher and public-content validation are in place.

The public site is a work in progress. It should not yet be treated as a complete election reference.
