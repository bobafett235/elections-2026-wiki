---
tags: [source]
aliases: [Keep DC Honest, Influence Registry]
status: evergreen
last_updated: 2026-08-04
source_count: 4
confidence: medium
sources:
  - "https://www.keep-dc-honest.com/"
  - "https://github.com/yeet01520/Influence-Registry"
  - "https://github.com/yeet01520/Influence-Registry/blob/main/METHODOLOGY.md"
  - "https://github.com/yeet01520/Influence-Registry/blob/main/data/fec.json"
modified: 2026-08-04
---
# Keep DC Honest / Influence Registry

## Role

Secondary, derived federal campaign-finance source. Useful for career-level fundraising context, sector fields, and tracked outside spending. Not an election-status authority and not a primary FEC source.

## Verified limitations

- Federal congressional scope only. It does not establish South Carolina ballot status or cover county, school-board, or state-legislative races.
- The data is primarily career-cumulative, while the wiki needs current-cycle 2026 figures.
- The roster still presented Lindsey Graham as a sitting South Carolina senator after the wiki's recorded death and special-election transition.
- Published score values did not all reproduce from the repository's current raw inputs. The public profile data also contains manually written corruption scores and narratives.
- Sector totals can include individual donations classified by employer, not only corporate PAC checks.

## Integration rules

- Use official FEC figures first for current-cycle federal finance.
- Cite raw career totals, sector fields, and outside-spending fields only after checking the underlying FEC or OpenSecrets record.
- Label every figure as career context and record the source date.
- Do not import the site's risk labels, corruption scores, manually written controversies, or current officeholder claims.
- Do not treat the score as a corporate-PAC percentage. Its formula uses a residual non-grassroots bucket plus a special AIPAC field.

## Current wiki use

Keep this as a supplemental finance source for federal candidate pages. It should not drive the candidate roster or race-status blocks.

## Source list

- [Live site](https://www.keep-dc-honest.com/)
- [Public repository](https://github.com/yeet01520/Influence-Registry)
- [Methodology](https://github.com/yeet01520/Influence-Registry/blob/main/METHODOLOGY.md)
- [Raw FEC-derived data](https://github.com/yeet01520/Influence-Registry/blob/main/data/fec.json)
