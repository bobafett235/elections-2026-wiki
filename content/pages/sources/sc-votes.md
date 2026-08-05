---
tags: [source]
aliases: [South Carolina State Election Commission, SC Votes]
status: evergreen
last_updated: 2026-08-04
source_count: 4
confidence: high
sources:
  - "https://scvotes.gov/"
  - "https://vrems.scvotes.sc.gov/Candidate/SelectElection"
  - "https://scvotes.gov/candidates/"
  - "https://scvotes.gov/elections-statistics/election-results/"
modified: 2026-08-04
---
# South Carolina Election Commission / SC Votes

## Role

Primary source for South Carolina election administration, filing rules, candidate tracking, election dates, voter information, and official results.

## Verified scope

- The Candidate Tracking tool reports filed candidates by election and allows filtering by office, candidate status, party, and filing location.
- The tool warns that statewide primary views show candidates appearing on the primary ballot and that some local elections may not be available.
- The Candidates page explains partisan filing, special-election timing, write-in rules, party conventions, and the relationship between election filings and State Ethics Commission disclosures.
- The Results page links to statewide primary, runoff, recount, special-election, and historical result databases.

## 2026 Senate special-primary check

On August 4, 2026, the Candidate Tracking listing for the August 11 U.S. Senate Special Republican Primary returned 12 filed records:

- 10 records marked **Active**: Duke Buckner, Danny Ford II, Russell Fry, Darline Graham, Mark Lynch, Mark McBride, Ralph Norman, Glenda Gail Parker, Mark Sanford, and Sam Shepherd.
- 2 records marked **Not Certified for Primary**: Darius Mitchell and Clark Neilson.

The wiki should describe the active ballot field as ten candidates and retain the two non-certified filings only as a status note.

## Integration rules

- Use SC Votes first for current candidate status, filing deadlines, special-election mechanics, and official results.
- Cite the election-specific Candidate Tracking page when a roster matters. The generic landing page is stable, but the detailed election search is dynamic.
- Keep local candidate gaps explicit. Anderson County and school-board pages may require county or district records because SC Votes does not list every local election.
- If the linked ENR result endpoint cannot be fetched, retain a `[needs-source]` or `[disputed]` marker rather than treating Ballotpedia as the official result.

## Source list

- [SC Votes home](https://scvotes.gov/)
- [Candidate Tracking](https://vrems.scvotes.sc.gov/Candidate/SelectElection)
- [Candidate information](https://scvotes.gov/candidates/)
- [Election results](https://scvotes.gov/elections-statistics/election-results/)
