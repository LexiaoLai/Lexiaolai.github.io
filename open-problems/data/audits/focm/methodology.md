# Foundations of Computational Mathematics survey methodology

## Scope and inventory

The inventory covers every Crossref record for *Foundations of Computational Mathematics* with an online-publication date from 1 January 2023 through 13 July 2026, inclusive. It contains **151 records**: **147 research articles** and **4 excluded nonresearch records** (two corrections, one preface, and one tribute). The online-year counts are {'2023': 35, '2024': 51, '2025': 45, '2026': 20}.

## Full-text screening

Every research article was taken through a high-recall title, abstract, and phrase screen and then manually reviewed in full wherever a matching full text could be located. Full text was available for **145 of 147 research articles** through Springer full HTML, a title-and-author-matched arXiv preprint, an author manuscript, or an institutional-repository copy. The two inaccessible research articles are:

- 10.1007/s10208-023-09610-1, “Further ∃R-Complete Problems with PSD Matrix Factorizations”.
- 10.1007/s10208-024-09644-z, “Analysis of a Modified Regularity-Preserving Euler Scheme for Parabolic Semilinear SPDEs with Multiplicative Noise”.

For each inaccessible article, exact-title, DOI, author, Springer, arXiv, OpenAlex, Semantic Scholar, and general web searches were performed. Neither article was silently treated as a negative screen.

## Retention rule

A record was retained only when the source paper itself explicitly framed an unresolved conjecture, problem, question, unknown, or clearly delimited open-problem item and the issue could be normalized into a self-contained research statement. Quotations are short evidence snippets of no more than 25 words; the normalized descriptions preserve the source scope but are not quotations. Vague aspirations, routine implementation plans, unavailable numerical inputs, historical problems the paper reports solving, and broad “future work” without a precise mathematical target were excluded.

This process retained **82 problems** from **53 source articles**. Counts by source online year are {'2023': 9, '2024': 28, '2025': 30, '2026': 15}.

## Status checking

Statuses were checked through **2026-07-13**. For each retained item, the search combined source-DOI and exact-title searches, distinctive statement-keyword searches, arXiv, Crossref, OpenAlex, Semantic Scholar citation metadata, and general web discovery. A later work was counted as a resolution or partial advance only when a primary paper directly addressed the same mathematical claim; surveys, snippets, and secondary summaries were used only for discovery.

The status totals are {'no_resolution_found': 80, 'partial_progress': 1, 'resolved': 1}. “No resolution found” is an evidence-bounded literature-search result, not a proof that no resolution exists. One problem is marked resolved by 10.1093/pnasnexus/pgag131, and one is marked partial progress by 10.1137/24M1689053; both records include the later primary evidence and a scope comparison.

## Artifact map and limitations

- inventory.json: all 151 journal records, classification, and full-text route or access failure.
- screening.json: one screening disposition per inventory record, high-recall phrase counts, and retained-problem counts.
- problems.json: normalized problem records with source evidence and status evidence.
- methodology.md: this audit description.

The principal limitation is the two inaccessible research articles. Automated phrase counts were used only for recall support and never as the final inclusion decision. Publisher pagination and preprint pagination can differ, so evidence locations prioritize stable section, problem, conjecture, theorem, or remark labels.
