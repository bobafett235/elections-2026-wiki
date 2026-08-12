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

## 2026-08-12: Frontrunner profile refresh

- Refreshed the five top-of-ticket profiles with current-cycle sources: Alan Wilson (income tax elimination, human trafficking record, seven-AG endorsements), Jermaine Johnson (affordable housing and labor council proposals), Annie Andrews (over $10M raised per FEC, measles and Medicaid platform), Mark Sanford (concession sourced), and Kasie Whitener (full academic and party record).
- Every profile now cites campaign sites plus reputable news, with campaign claims attributed and uncertainty markers preserved.

## 2026-08-12: Verified-source expansion across candidate profiles

- Expanded 21 candidate pages with verified background and platform material from campaign sites, official state office pages, local news, and candidate surveys. Standouts: Catherine Fleming Bruce (Senate write-in, author and preservationist), Sam Skardon (ex-John Lewis aide running for lieutenant governor), Eunice Lehmacher (SC-3 Democratic platform from her voter survey), and the statewide Democratic challengers (Belton, Boozer, Coe).
- Updated the U.S. House statewide overview with verified November fields: SC-1 is an open seat (Honeycutt, Lacore, Reeside), SC-7 is competitive (Fry vs Vincent, campaign poll at 37-41), SC-6 is Clyburn vs Peterson; SC-5 remains unconfirmed.
- Corrected primary outcomes: Glenda Gail Parker and Sam Shepherd lost the Aug. 11 Senate special primary; Don Chapman's June 23 HD-8 runoff win is now directly sourced.
- All updates preserved uncertainty markers and campaign-claim attribution; profiles with no public information still say so.

## 2026-08-12: Table-cell link repair on race pages

- Repaired 12 broken candidate links inside the County Council and Anderson SD4 race tables. Quartz resolves links in table cells against the content root, so the previously used `../entities/...` form emitted 404 hrefs.
- Replaced them with content-root relative links (`pages/entities/...`), which render correctly at any page depth.
- Strengthened the validation gate with a table-cell link rule and regression tests, so a future export with this pattern fails before deployment.

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
