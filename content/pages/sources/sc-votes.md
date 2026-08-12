---
tags: [source]
aliases: [South Carolina State Election Commission, SC Votes]
status: evergreen
last_updated: 2026-08-11
source_count: 8
confidence: high
sources:
  - "https://scvotes.gov/"
  - "https://vrems.scvotes.sc.gov/Candidate/SelectElection"
  - "https://scvotes.gov/candidates/"
  - "https://scvotes.gov/elections-statistics/election-results/"
  - "https://scvotes.gov/candidate-name-added-to-ballot-in-u-s-senate-special-republican-primary/"
  - "https://scvotes.gov/sec-addresses-ballot-question/"
  - "https://scdailygazette.com/2026/07/29/sc-gop-bars-3-candidates-from-primary-ballot-leaving-9-to-compete-for-us-senate/"
  - "https://apnews.com/live/election-primary-08-11-2026"
modified: 2026-08-11
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

## 2026 Senate special-primary timeline reconciliation

The August 4 Candidate Tracking snapshot reflected the final 10-candidate ballot, after a ballot challenge that altered the earlier certification status:

- Twelve people initially filed for the August 11 special Republican primary.
- The South Carolina Republican Party decertified Danny Ford II, Darius Mitchell, and Clark Neilson on July 28, leaving nine candidates.
- On August 4, a court order required Ford's name to be added to the ballot. The State Election Commission confirmed the order, so the August 11 ballot had ten candidates.
- The August 11 primary produced an August 25 runoff between Darline Graham and Ralph Norman, according to Associated Press reporting. The official SC Votes results landing page links to the canonical ENR record, which returned HTTP 403 from this research environment. Do not replace this access limitation with unverified totals.

## General-election multiple-office rule

On July 15, the State Election Commission stated that a candidate may appear on a general-election ballot for more than one office. A candidate's Senate-primary participation therefore does not by itself establish that the candidate vacated, or cannot appear on the ballot for, a U.S. House seat.

## Integration rules

- Use SC Votes first for current candidate status, filing deadlines, special-election mechanics, and official results.
- Use the election-specific Candidate Tracking page when a roster matters. The generic landing page is stable, but the detailed election search is dynamic and may stop exposing completed contests.
- Keep local candidate gaps explicit. Anderson County and school-board pages may require county or district records because SC Votes does not list every local election.
- If the linked ENR result endpoint cannot be fetched, retain a `[needs-source]` or `[disputed]` marker rather than treating Ballotpedia as the official result.

## Source list

- [SC Votes home](https://scvotes.gov/)
- [Candidate Tracking](https://vrems.scvotes.sc.gov/Candidate/SelectElection)
- [Candidate information](https://scvotes.gov/candidates/)
- [Election results](https://scvotes.gov/elections-statistics/election-results/)
- [Ford ballot-addition notice](https://scvotes.gov/candidate-name-added-to-ballot-in-u-s-senate-special-republican-primary/)
- [Multiple-office ballot statement](https://scvotes.gov/sec-addresses-ballot-question/)
- [SC Daily Gazette ballot-certification report](https://scdailygazette.com/2026/07/29/sc-gop-bars-3-candidates-from-primary-ballot-leaving-9-to-compete-for-us-senate/)
- [Associated Press Aug. 11 runoff call](https://apnews.com/live/election-primary-08-11-2026)
