# Four-journal survey methodology

## Scope

The corpus contains 1,542 journal records dated from 1 January 2023 through 13 July 2026 across *Mathematical Programming*, *SIAM Journal on Optimization*, *Foundations of Computational Mathematics*, and *Mathematics of Operations Research*. Document-type review retained 1,507 research articles; corrections, notices, editorials, prefaces, and tributes remain in the audit but were excluded from problem screening.

## Access and screening

Publisher full text or a DOI/title/author-matched manuscript was screened for most of the 1,040 research articles with usable text. For a documented MOR subset, the evidence source is a DOI/title/author-matched paper-text extract from the prior catalogue rather than a directly accessed manuscript. Usable text could not be obtained for 467 articles. Every access gap remains visible in the per-journal screening audit and is never interpreted as a paper with no open problem. The MOR audit includes 175 direct full texts or matched extracts and distinguishes those routes record by record.

High-recall phrase searches were followed by manual context review. A problem was retained only when the source explicitly stated a precise conjecture, unresolved mathematical question, unknown complexity classification or constant, or sharply delimited missing theorem/counterexample. Generic future-work suggestions and limitations without a crisp mathematical task were excluded.

## Problem records

The combined catalogue contains 484 problems from 357 source papers. Every record has a contiguous source excerpt of at most 25 words and a two-to-four-sentence description that defines the setting, gives the relevant known boundary, and states the unresolved task. The excerpt preserves local source evidence; the normalized description is the independently readable statement. Source claims, normalized descriptions, and later-status evidence are stored separately.

## Status review

Statuses were checked through 13 July 2026 with exact-statement, title/keyword, and forward-literature searches. A record is marked **resolved** only when a matched primary source proves, refutes, or otherwise fully settles the stated task. **Partial progress** requires a matched primary source to establish an explicit theorem, bound, counterexample, or special case that directly advances the task. The evidence may be later or contemporaneous with the source article; a related-paper title alone is not evidence. **No resolution found** is a bounded negative search result, not proof that a problem remains open.

Status totals: 446 no resolution found, 25 partial progress, 13 resolved, and 0 disputed.

## Reproducibility

The public bundle includes the byte-identical combined JSON at `data/catalogue.json` and each journal's inventory, screening audit, and methodology under `data/audits/`. Publication dates use the journal deposit's online date when available; the MOR audit records its documented DOI-matched fallback for deposits without an online date.
