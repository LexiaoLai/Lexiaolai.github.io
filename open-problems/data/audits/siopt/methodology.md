# SIAM Journal on Optimization, 2023–2026: survey methodology

## Scope and corpus

This survey covers items in *SIAM Journal on Optimization* (SIOPT) with a Crossref `published-online` date from 2023-01-01 through 2026-07-13, inclusive. The inventory was retrieved from the Crossref journal endpoint for online ISSN 1095-7189 with the filter `from-online-pub-date:2023-01-01,until-online-pub-date:2026-07-13` and `rows=1000`. The raw response is preserved as `raw/crossref-online.json`; each inventory record retains its DOI and publisher links.

Crossref returned 407 items: 116 dated 2023, 138 dated 2024, 101 dated 2025, and 52 dated 2026 through the cutoff. Title-based document-type review classified 405 as research articles and two as corrigenda/corrections. The two nonresearch items remain in `inventory.json` and `screening.json` but were excluded from open-problem screening.

## Full-text discovery and coverage

Every research article was matched by DOI against Semantic Scholar and OpenAlex. Candidate full texts were accepted only when the DOI matched directly or when title and authors matched exactly. The usable corpus contains 266 extracted full texts: 230 DOI-matched arXiv copies found through Semantic Scholar, 21 other Semantic Scholar open-access copies, 11 OpenAlex open-access copies, and four exact-title-and-author arXiv matches recovered separately.

For 139 research articles, no DOI/title/author-matched open full text was located. A publisher-page check exposed metadata and an abstract but a **Get Access** barrier for the full article. These records are labeled `full_text_not_screened`; they are not treated as papers with no open problem. This distinction is preserved record by record in `screening.json`.

## High-recall screening and manual adjudication

The 266 extracted texts were searched with deliberately broad phrases, including variants of `open problem`, `open question`, `remains open`, `it is unknown`, `conjecture`, `future work`, `natural question`, `whether there exists`, and statements that a result or bound is not known. The raw hits are preserved in `raw/open-keyword-hits.txt`, stronger phrase hits in `raw/strong-hits-lines.txt`, and surrounding contexts in `raw/candidate-contexts.md`.

Every candidate context was manually adjudicated. A record was included only when the source explicitly posed a mathematically precise unresolved question, conjecture, unknown complexity boundary, or similarly crisp task. Generic research directions, informal suggestions, limitations without a well-defined task, questions already resolved later in the same paper, and literature-review descriptions of somebody else's problem were excluded. `screening.json` records 58 screened papers with at least one confirmed problem and 208 screened papers in which no source-explicit problem was confirmed.

Each public problem record contains a source quote of at most 25 words and its location in the extracted text. The normalized description is three sentences (within the required two-to-four-sentence range): it defines the setting and relevant objects, states the result or boundary established by the source paper, and states the unresolved task. The quote, normalized description, and later status evidence are deliberately separate fields.

## Status review

Statuses were checked through 2026-07-13. For each confirmed problem, the review combined an exact-quote query, a source-title-plus-keywords query, and screening of later primary works recorded as citing the source in Semantic Scholar. Candidate status evidence was accepted only when a direct DOI or arXiv primary-literature page was available and the later work explicitly addressed the same mathematical task.

The status vocabulary is:

- `resolved`: a later primary source proves the requested result or gives a counterexample that settles it.
- `partial_progress`: a later primary source settles a meaningful special case, extends the framework, or advances the problem without resolving the full source formulation.
- `disputed`: primary sources make materially conflicting resolution claims.
- `no_resolution_found`: no explicit resolution was located by the recorded search through the cutoff. This is an evidence-bounded search result, not proof that the question remains open.

The resulting catalogue contains 72 confirmed problems from 58 source papers: 65 with `no_resolution_found`, four with `partial_progress`, three `resolved`, and none `disputed`. Direct later-primary evidence for every nonnegative status is embedded in `problems.json`.

## Reproducibility and limitations

The discovery inputs and derived artifacts are preserved under this directory. `inventory.json` defines the complete publication corpus; `screening.json` gives the disposition of every item; `problems.json` contains only confirmed problems and their status evidence; `raw/problem-validation.json` records quote-word and description-sentence validation. The principal machine-readable discovery sources were:

- Crossref: `https://api.crossref.org/journals/1095-7189/works`
- Semantic Scholar Graph API batch lookups by `DOI:<doi>` and forward-citation metadata
- OpenAlex works filtered to SIOPT and the publication window
- arXiv DOI matches and exact title/author fallbacks

This is an exhaustive inventory of Crossref-online-dated SIOPT items in the stated window, but it is not an absolute exhaustive full-text survey because 139 paywalled articles could not be screened. SIAM PDF requests were also blocked by Cloudflare in the command-line retrieval path, and broad arXiv title-query recovery encountered HTTP 429 rate limits. The coverage gap is therefore visible in the data and must remain visible in any downstream website or aggregate statistic.
