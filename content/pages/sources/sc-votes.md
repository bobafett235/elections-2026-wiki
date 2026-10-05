---
tags: [source]
aliases: [South Carolina State Election Commission, SC Votes]
status: evergreen
last_updated: 2026-10-05
sources_checked: 2026-10-05
source_count: 17
confidence: high
sources:
  - "https://scvotes.gov/"
  - "https://vrems.scvotes.sc.gov/Candidate/SelectElection"
  - "https://scvotes.gov/candidates/"
  - "https://scvotes.gov/elections-statistics/election-results/"
  - "https://www.enr-scvotes.org/SC/127017/"
  - "https://www.enr-scvotes.org/SC/127179/"
  - "https://vrems.scvotes.sc.gov/Candidate/CandidateSearch?electionId=22596"
  - "https://scvotes.gov/candidates/2026-candidate-information/"
  - "https://scvotes.gov/voters/early-voting/"
  - "https://scvotes.gov/voters/2026prep/"
  - "https://scvotes.gov/hand-count-audits-for-2026-u-s-senate-special-republican-primary-runoff/"
  - "https://scvotes.gov/national-voter-registration-day-highlights-south-carolinas-upcoming-voter-registration-deadline/"
  - "https://scvotes.gov/elections-statistics/election-database/"
  - "https://scvotes.gov/candidate-name-added-to-ballot-in-u-s-senate-special-republican-primary/"
  - "https://scvotes.gov/sec-addresses-ballot-question/"
  - "https://scdailygazette.com/2026/07/29/sc-gop-bars-3-candidates-from-primary-ballot-leaving-9-to-compete-for-us-senate/"
  - "https://apnews.com/live/election-primary-08-11-2026"
modified: 2026-10-05
---
# South Carolina Election Commission / SC Votes

## Role

Primary source for South Carolina election administration, filing rules, candidate tracking, election dates, voter information, and official results.

## Verified scope

- The Candidate Tracking tool reports filed candidates by election and allows filtering by office, candidate status, party, and filing location.
- The tool warns that statewide primary views show candidates appearing on the primary ballot and that some local elections may not be available.
- The Candidates page explains partisan filing, special-election timing, write-in rules, party conventions, and the relationship between election filings and State Ethics Commission disclosures.
- The Results page links to statewide primary, runoff, recount, special-election, and historical result databases.
- The Election Database page provides the State Election Commission's historical election-data search and is distinct from the live ENR reporting site.

## 2026 Senate special-primary check

On August 4, 2026, the Candidate Tracking listing for the August 11 U.S. Senate Special Republican Primary returned 12 filed records:

- 10 records marked **Active**: Duke Buckner, Danny Ford II, Russell Fry, Darline Graham, Mark Lynch, Mark McBride, Ralph Norman, Glenda Gail Parker, Mark Sanford, and Sam Shepherd.
- 2 records marked **Not Certified for Primary**: Darius Mitchell and Clark Neilson.

The wiki should describe the active ballot field as ten candidates and retain the two non-certified filings only as a status note.

## 2026 Senate special-primary timeline reconciliation

The August 4 Candidate Tracking snapshot reflected the final 10-candidate ballot, after a ballot challenge that altered the earlier certification status. The August 11 primary produced an August 25 runoff between Darline Graham and Ralph Norman. The certified primary ENR record shows Graham 109,881 (32.75%), Norman 82,627 (24.62%), Fry 65,955 (19.66%), Sanford 50,136 (14.94%), Lynch 19,892 (5.93%), and five single-digit-share candidates; 335,555 votes cast and 11.12% turnout ([primary ENR](https://www.enr-scvotes.org/SC/127017/)). The runoff ENR record now reports Graham defeating Norman, 193,486 (52.45%) to 175,412 (47.55%), and the SEC published a hand-count audit notice ([runoff ENR](https://www.enr-scvotes.org/SC/127179/); [audit notice](https://scvotes.gov/hand-count-audits-for-2026-u-s-senate-special-republican-primary-runoff/)).

## General-election multiple-office rule

On July 15, the State Election Commission stated that a candidate may appear on a general-election ballot for more than one office. A candidate's Senate-primary participation therefore does not by itself establish that the candidate vacated, or cannot appear on the ballot for, a U.S. House seat.

## General-election record check (Oct. 5, 2026)

The Candidate Tracking listing for the November 3 Statewide General Election (election 22596) was re-pulled via the candidate-search endpoint on Oct. 5, 2026. It returned 14 U.S. Senate rows, with four Active records: Darline Graham (Republican), Annie Andrews (Democratic), Kasie Whitener (Libertarian), and Mark Hackett (Constitution). Lindsey Graham remains in the record with status "Deceased After Primary." Ballotpedia's five Independent Senate candidates (Jack Ellison, Cindy Glaser, Paul Sedletsky, Edward Strunge, Reece Wright-McDonald) do not appear anywhere in the record, so their November ballot status is [unverified]. The record does list petition candidates that failed to qualify, so an absent name means no filed record as of the pull. Anderson County Council D2 (Davis/Hayes), D4 (Shalaby), D7 (Alexander Active, M. Cindy Wilson Defeated In Primary), SD4 Areas 2/4/5, HD-8, and all seven House fields were re-confirmed unchanged.

The SEC's current voter-preparation page lists Oct. 2 as the in-person registration deadline, Oct. 4 at 11:59 p.m. for online or email/fax applications, and Oct. 5 as the mail postmark deadline. General-election early voting is Oct. 19-31, 8:30 a.m. to 6:00 p.m., Monday through Saturday, closed Sunday, Oct. 25. Absentee ballots must arrive by 7:00 p.m. on Nov. 3.

## Integration rules

- Use SC Votes first for current candidate status, filing deadlines, special-election mechanics, and official results.
- Use the election-specific Candidate Tracking page when a roster matters. The generic landing page is stable, but the detailed election search is dynamic and may stop exposing completed contests.
- Keep local candidate gaps explicit. Anderson County and school-board pages may require county or district records because SC Votes does not list every local election.
- If the linked ENR result endpoint cannot be fetched, retain a `[needs-source]` or `[disputed]` marker rather than treating Ballotpedia as the official result.

## Source list

- [SC Votes home](https://scvotes.gov/)
- [Candidate Tracking](https://vrems.scvotes.sc.gov/Candidate/SelectElection)
- [Candidate search, November 2026](https://vrems.scvotes.sc.gov/Candidate/CandidateSearch?electionId=22596)
- [Candidate information](https://scvotes.gov/candidates/2026-candidate-information/)
- [Election results](https://scvotes.gov/elections-statistics/election-results/)
- [Election Database](https://scvotes.gov/elections-statistics/election-database/)
- [Primary ENR](https://www.enr-scvotes.org/SC/127017/)
- [Runoff ENR](https://www.enr-scvotes.org/SC/127179/)
- [Early voting](https://scvotes.gov/voters/early-voting/)
- [2026 voter preparation](https://scvotes.gov/voters/2026prep/)
- [Runoff hand-count audit notice](https://scvotes.gov/hand-count-audits-for-2026-u-s-senate-special-republican-primary-runoff/)
- [Registration deadline reminder](https://scvotes.gov/national-voter-registration-day-highlights-south-carolinas-upcoming-voter-registration-deadline/)
- [Ford ballot-addition notice](https://scvotes.gov/candidate-name-added-to-ballot-in-u-s-senate-special-republican-primary/)
- [Multiple-office ballot statement](https://scvotes.gov/sec-addresses-ballot-question/)
- [SC Daily Gazette ballot-certification report](https://scdailygazette.com/2026/07/29/sc-gop-bars-3-candidates-from-primary-ballot-leaving-9-to-compete-for-us-senate/)
- [Associated Press Aug. 11 runoff call](https://apnews.com/live/election-primary-08-11-2026)
