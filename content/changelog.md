---
tags: [meta]
aliases: [Public changelog]
status: evergreen
last_updated: 2026-08-12
source_count: 0
confidence: high
sources: []
modified: 2026-08-12
---
# Public changelog

## 2026-08-12: Anderson County Council candidate pages and source links

- Added seven verified candidate pages for the Anderson County Council November field (Districts 1 through 6), each citing SC Votes candidate records, county council profiles, and local reporting: Chris Sullivan, Dave Shalaby, Glenn Davis, Greg Elgin, James Hayes, Jimmy Davis, and Josh Mann.
- Completed the County Council race page with the full verified field: District 2 is the only two-candidate November contest (Glenn Davis vs James Hayes); the other six districts list one active candidate each. The District 7 correction (Collin Alexander beat M. Cindy Wilson by 38 votes) is now fully sourced.
- Rebuilt the index to 74 pages: 8 races, 54 candidates, and 12 source notes.
- Added the project source repository link (github.com/bobafett235/elections-2026-wiki) to the homepage and the About page.

## 2026-08-11: Senate special-primary result and ballot correction

- Updated the Senate race from the completed Aug. 11 special primary to the Aug. 25 runoff between Darline Graham and Ralph Norman. The Associated Press called the runoff pair; the official SC Votes ENR record remains linked but returned HTTP 403 from this research environment, so the site does not present unofficial totals as final.
- Corrected the August ballot history: the party decertified three of 12 filers, then a court order required Danny Ford II back onto the ballot, producing the 10-candidate field that voted Aug. 11.
- Removed the false SC-5/SC-7 “status conflict.” SC Votes says candidates may appear on a general-election ballot for more than one office, while complete House candidate fields remain explicitly unverified.
- Strengthened public publishing: exports now stage and pass safety checks before atomically replacing the last known-good public content, with regression tests enforced in GitHub Actions.

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
