# Mathematics of Operations Research survey methodology

## Scope and cutoff

This audit covers *Mathematics of Operations Research* (MOR; ISSN 0364-765X / 1526-5471) from 1 January 2023 through 13 July 2026. The status cutoff is 13 July 2026.

The completeness frame is the 515 unique DOI records returned by the Crossref journal query for `0364-765X`, type `journal-article`, with the broad Crossref publication-date filter `from-pub-date:2023-01-01,until-pub-date:2026-07-13`. A broad date filter is necessary because INFORMS deposits frequently omit `published-online` for older articles even when the publisher page gives an Articles-in-Advance date.

For each DOI, the canonical survey date is:

1. Crossref `published-online`, when present;
2. otherwise, the publication date on the DOI-matched OpenAlex MOR record;
3. otherwise, Crossref print/issued date.

This supplies an online date for 444 records and leaves 71 with only a print/issued date. All 515 canonical dates fall inside the requested window. The resulting inventory is:

| Canonical year | All items | Research articles | Nonresearch |
| --- | ---: | ---: | ---: |
| 2023 | 189 | 186 | 3 |
| 2024 | 125 | 120 | 5 |
| 2025 | 128 | 124 | 4 |
| 2026 through July 13 | 73 | 71 | 2 |
| **Total** | **515** | **501** | **14** |

The 14 nonresearch records are 13 “Editorial Board” items and one erratum. They remain in `inventory.json` and are excluded from problem screening.

## Access and full-text screening

Every research DOI received an access check through its INFORMS DOI page, Crossref links, DOI-matched OpenAlex locations, and title/author matching to an open preprint or repository copy. Publisher-only abstract pages were not treated as full text.

- OpenAlex returned 445 MOR work records (443 distinct matched DOIs) in the window.
- It exposed 67 direct PDF routes. Fifty-nine downloaded as valid PDFs and were text-extracted; eight routes failed or returned non-PDF content.
- The 59 PDFs received a page-level high-recall search. Forty-five contained at least one trigger phrase; references and passages that only used words such as “unknown” descriptively were rejected manually.
- The public `open-problems-in-or` corpus supplied 132 MOR candidate extracts from 132 source papers. These were used only as leads. Every lead was matched back to this audit by DOI, title, and author list, and every retained quote is source-explicit and has a paper location. Sixteen of those source papers were independently rechecked in the downloaded OA PDFs.
- The independent PDF pass found 12 additional explicit problems in 10 source papers that were absent from the public candidate catalogue.
- Of the 142 source papers with confirmed problems, 26 were directly screened from locally extracted OA full text and 116 use the DOI/title/author-matched primary-text extract route. The latter route is disclosed per record; it is weaker than direct local PDF re-verification.
- Another 33 OA PDFs were fully screened and yielded no confirmed source-explicit problem.
- The remaining 326 research papers are marked `inaccessible`. They are not counted as negative screens, and no claim is made that they contain no open problem.

The high-recall phrase set included `open problem`, `open question`, `remain(s) open`, `left open`, `unknown`, `not known`, `do not know`, `unresolved`, `conjecture`, and `remains to be proved/shown/determined/settled/established/understood`. Matches in bibliographies, descriptions of unknown model parameters, problems solved later in the same paper, and generic future-work aspirations were rejected.

## Inclusion rule

A record appears in `problems.json` only when the source paper itself states a precise unresolved mathematical or algorithmic task. Included forms are:

- a named conjecture;
- an explicit open question;
- a precise unknown complexity classification or optimal constant;
- a sharply delimited missing case, convergence theorem, existence result, or counterexample request.

Generic “interesting directions,” calls for applications, numerical experiments, or broad model extensions were excluded unless the source also specified the exact property to prove or compute.

Each problem contains:

- an exact contiguous source fragment of at most 25 words and its location;
- a self-contained 2–4 sentence description that defines the essential objects and nonstandard acronyms, states the known boundary, and identifies the unresolved task;
- topic and keywords;
- source DOI, title, authors, dates, issue metadata, and the full-text access route;
- a conservative status with later-primary-literature evidence.

The final catalogue contains 144 problems from 142 source papers. Two papers contribute more than one independently stated problem.

Descriptions are written for the site's plain-text renderer rather than MathJax: raw LaTeX delimiters and commands are removed, short formulas use Unicode or compact ASCII notation, and formula-heavy source definitions are paraphrased. A final record-by-record pass removed title-only boilerplate and checked that every description contains substantive setting, boundary, and task information.

## Status review

Status searches used the exact source title, DOI, distinctive noun phrases from the question, forward citations, and searches combining the source authors with terms such as `conjecture`, `open problem`, `resolved`, `counterexample`, or the relevant bound/algorithm name. Public-catalogue forward-citation summaries and related-paper titles were treated as leads only. An item was labeled partial or resolved only when a later primary paper supplied a manually checked statement of the theorem, bound, counterexample, or case it established; a thematically related paper was not itself evidence of progress.

The status enum is exactly:

- `no_resolution_found`: targeted searches found no later primary paper claiming a complete answer;
- `partial_progress`: later primary work directly advances the stated question but leaves part of it open;
- `resolved`: later primary work proves, refutes, or otherwise fully settles the normalized question;
- `disputed`: incompatible resolution claims exist and could not be reconciled.

At the cutoff the counts are 139 `no_resolution_found`, 1 `partial_progress`, 4 `resolved`, and 0 `disputed`. The four resolved records concern best-core improvement in housing markets, complete EFX under general monotone valuations (resolved negatively), the minimax exponent in distribution-free contextual dynamic pricing, and unsmoothed Riemannian ADMM. The diffusion-model question is the sole `partial_progress` record: total-variation adaptivity has been established, but the Wasserstein part remains open. Forty-two provisional partial labels were conservatively demoted because their retained evidence merely restated the open question or named a related paper without identifying a proved advance.

“No resolution found” is bounded negative search evidence, never a proof that a problem remains open. Each such record states this limitation and the date through which the search was checked.

## Reproducibility and files

- `inventory.json`: all 515 records, dates, types, URLs, access routes, and dispositions.
- `screening.json`: per-item screening/access status and short candidate evidence without reproducing long source passages.
- `problems.json`: the 144 normalized problem records and status evidence.
- `../mor_crossref.json`: the 515-record broad-date Crossref completeness frame; `source/crossref.json`: the 142-record online-date-only diagnostic that exposed the deposit gap.
- `source/openalex_1.json` through `source/openalex_3.json`: OpenAlex source snapshots.
- `source/oa_phrase_screen.json`: OA-PDF download and page-level high-recall screening audit.
- `manual_additions.json`: independently reviewed additions found by the OA pass.
- `build_deliverables.py`: deterministic builder for the three public JSON outputs.

The public reference catalogue remains in `source/open-problems-in-or-main/` solely as an auditable candidate input. Its own `unverified` labels are not imported as status claims.
