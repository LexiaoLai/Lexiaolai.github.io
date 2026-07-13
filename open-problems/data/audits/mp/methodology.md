# Mathematical Programming survey methodology, 2023–13 July 2026

The combined screening audit contains every journal record in the window and was generated from full publisher HTML. The 2025 records preserve the previously completed manually reviewed release; their descriptions were expanded in this update without changing the audited source quotations or status evidence. The additional year reviews follow below.

# Mathematical Programming 2023 survey methodology

Status checked through: 2026-07-13  
Publication basis: first online publication date

## Scope and corpus

The 2023 cohort contains 120 Springer records whose online publication date falls between 2023-01-01 and 2023-12-31. Of these, 116 are research articles and four are nonresearch records: one special-issue notice and three corrections. Both Series A and Series B are included.

All 116 research articles had publisher HTML available to the screening pipeline. The full text of every article was scanned with a deliberately high-recall vocabulary for explicit open problems, questions, conjectures, unknown cases, and future work. That pass produced 100 candidate passages in 33 papers. Every candidate passage was then read in its surrounding section and manually adjudicated; the remaining 83 research articles had no retained high-recall passage and are recorded as screened negatives in screening.json.

The four nonresearch records were inventoried but not screened as problem-bearing research:

- 10.1007/s10107-023-01990-0, special-issue notice.
- 10.1007/s10107-023-01972-2, correction.
- 10.1007/s10107-023-01998-6, publisher correction.
- 10.1007/s10107-023-02039-y, correction.

## Inclusion rule

A catalogue entry was retained only when the source paper itself states a precise unresolved question, conjecture, missing characterization, or well-defined extension. Generic suggestions such as “apply this method elsewhere,” implementation ideas without a mathematical target, and broad claims that a topic deserves future study were excluded. A statement already proved, disproved, or closed in the same source paper was also excluded.

Closely related sentences were combined when they formed one mathematical question. Separately numbered questions, independently answerable conjectures, and distinct complexity or characterization targets were kept as separate records. Source quotations are capped at 25 words; normalized descriptions are self-contained prose rather than raw LaTeX.

## Status protocol

Each retained problem received an evidence-bounded status search through 2026-07-13. Searches combined exact source wording, the source title, authors, mathematical keywords, and terms such as “proof,” “counterexample,” and “resolved.” Forward and related literature was screened where discoverable, and status claims rely on primary papers or publisher records rather than secondary summaries.

The status labels mean:

- no_resolution_found: no primary source explicitly resolving the precise formulation was located. This is not proof that no resolution exists.
- partial_progress: a primary source settles a restricted domain, gives a conditional answer, or proves a materially related result without resolving the full formulation.
- resolved: a primary source directly proves, disproves, or otherwise fully answers the retained formulation.
- disputed: conflicting primary claims would be recorded here; none were found in this cohort.

Three entries are marked resolved: entropy-regularized softmax policy-gradient convergence, the asymptotic relaxation complexity of the discrete simplex, and sublinear-factor approximation of symmetric submodular MLOP. Four entries have partial progress: EJR with committee monotonicity on a restricted voting domain, stochastic last-iterate VI rates, conditional hardness on regular graphs, and the clutter MFMC conjecture for coordinate-subspace multipartite clutters.

## Candidate-paper audit

| DOI | Paper | Disposition |
|---|---|---|
| 10.1007/s10107-022-01916-2 | Accelerating inexact successive quadratic approximation for regularized optimization through manifold identification | Excluded. “Conjecture” referred to a detection heuristic, not a source-explicit mathematical problem. |
| 10.1007/s10107-022-01920-6 | Softmax policy gradient methods can take exponential time to converge | Included: 1 problem. |
| 10.1007/s10107-023-01933-9 | A new perspective on low-rank optimization | Included: 2 problems. Broad implementation directions were excluded. |
| 10.1007/s10107-023-01929-5 | A simple and fast linear-time algorithm for divisor methods of apportionment | Excluded. The biproportional-apportionment suggestion did not specify a precise unresolved target. |
| 10.1007/s10107-023-01935-7 | Inequality constrained stochastic nonlinear optimization via active-set sequential quadratic programming | Excluded. The proposed related-scheme extension was too underspecified to normalize faithfully. |
| 10.1007/s10107-023-01926-8 | Phragmén’s voting methods and justified representation | Included: 2 problems. Earlier questions answered in the source were excluded. |
| 10.1007/s10107-023-01958-0 | Hyperbolicity cones are amenable | Included: 1 problem. Amenability and niceness questions solved in the source were excluded. |
| 10.1007/s10107-023-01945-5 | Fair division of graphs and of tangled cakes | Included: 5 problems. |
| 10.1007/s10107-023-01959-z | Diverse collections in matroids and graphs | Included: 3 problems. A broader umbrella question about all constant thresholds was not duplicated. |
| 10.1007/s10107-023-01953-5 | Optimal algorithms for differentially private stochastic monotone variational inequalities and saddle-point problems | Included: 1 problem. A generic faster-running-time direction was excluded. |
| 10.1007/s10107-023-01956-2 | A scaling-invariant algorithm for linear programming whose running time depends only on the constraint matrix | Included: 1 problem. Rescaling and crossover questions already answered by the source were excluded. |
| 10.1007/s10107-023-01963-3 | On the complexity of separating cutting planes for the knapsack polytope | Excluded. The cited open problems are closed by results in the source. |
| 10.1007/s10107-023-01966-0 | Comparing solution paths of sparse quadratic minimization with a Stieltjes matrix | Included: 1 problem. |
| 10.1007/s10107-023-01964-2 | On the maximal number of columns of a Δ-modular integer matrix: bounds and computations | Included: 8 problems. |
| 10.1007/s10107-023-01968-y | On computing small variable disjunction branch-and-bound trees | Excluded. The matched ETH language states an assumption used for a lower bound, not a new open problem. |
| 10.1007/s10107-023-01979-9 | On the stationarity for nonlinear optimization problems with polyhedral constraints | Excluded. Implementation and nonquadratic suggestions lacked a precise conjecture or target theorem. |
| 10.1007/s10107-023-01962-4 | Faster goal-oriented shortest path search for bulk and incremental detailed routing | Excluded. The future cost-modeling discussion was application-specific and underspecified. |
| 10.1007/s10107-023-01965-1 | On SOCP-based disjunctive cuts for solving a class of integer bilevel nonlinear programs | Excluded. The general extension suggestion did not state a precise open question. |
| 10.1007/s10107-023-01988-8 | Swarm gradient dynamics for global optimization: the mean-field limit case | Ambiguous and excluded. The cached publisher page exposed only the abstract, whose conjecture says an inequality should hold in a “much broader setting” without defining that setting; it was not treated as a negative result. |
| 10.1007/s10107-023-01986-w | A preconditioned iterative interior point approach to the conic bundle subproblem | Included: 1 problem. |
| 10.1007/s10107-023-01992-y | Simple odd β-cycle inequalities for binary polynomial optimization | Included: 1 problem. |
| 10.1007/s10107-023-01993-x | Exploiting ideal-sparsity in the generalized moment problem with application to matrix factorization ranks | Included: 1 problem. Other broad application ideas were excluded. |
| 10.1007/s10107-023-01975-z | Asymptotic linear convergence of fully-corrective generalized conditional gradient methods | Included: 1 problem. |
| 10.1007/s10107-023-01994-w | The role of rationality in integer-programming relaxations | Included: 6 problems, corresponding to P1–P6. |
| 10.1007/s10107-023-02005-8 | A simple method for convex optimization in the oracle model | Excluded. The computational conjecture was an empirical explanation of behavior, not a precise mathematical statement. |
| 10.1007/s10107-023-02018-3 | Better-than-4/3-approximations for leaf-to-leaf tree and connectivity augmentation | Excluded. The matched conjecture appeared inside a proof step and was not posed as an unresolved problem. |
| 10.1007/s10107-023-02012-9 | The density of planar sets avoiding unit distances | Excluded. The source proves the matched conjecture. |
| 10.1007/s10107-023-02021-8 | Global optimization for cardinality-constrained minimum sum-of-squares clustering via semidefinite programming | Excluded. Facial-reduction and fair-clustering remarks were broad future directions. |
| 10.1007/s10107-023-02025-4 | Inapproximability of shortest paths on perfect matching polytopes | Excluded. The source disproves the matched conjecture. |
| 10.1007/s10107-023-02028-1 | New lower bounds on crossing numbers of Kₘ,ₙ from semidefinite programming | Included: 2 problems. |
| 10.1007/s10107-023-02038-z | Hardness and approximation of submodular minimum linear ordering problems | Included: 5 numbered open questions. |
| 10.1007/s10107-023-02034-3 | Intersecting and dense restrictions of clutters in polynomial time | Included: 2 conjectures. |
| 10.1007/s10107-023-02037-0 | The exact worst-case convergence rate of the alternating direction method of multipliers | Included: 2 problems. |

## Output and reproducibility

2023_problems.json contains 46 problems from 19 source papers: 39 no_resolution_found, four partial_progress, three resolved, and zero disputed. Each record includes source metadata, a short source quotation, a self-contained description, topic labels, status queries, and any primary resolution or progress evidence.

The source inventory and all high-recall passages remain in screening.json. The deterministic builder is scripts/build_2023_problems.py; rerunning it regenerates the JSON and enforces quote-length, description-length, and raw-LaTeX checks.


---

# Mathematical Programming 2024 first-split review methodology

Status checked through: 2026-07-13  
Publication basis: first online publication date

## Scope

This review covers the 27 high-recall candidate papers assigned to the first 2024 adjudication split. Their online publication dates run from 2024-01-04 through 2024-07-05. This is not the complete 2024 journal inventory: papers with no high-recall match are accounted for in the central `screening.json`, and the remaining candidate papers belong to the other 2024 review split.

All 27 assigned papers had cached Springer publisher HTML. The automated screen supplied 56 candidate passages containing terms for open problems, conjectures, unknown cases, or future work. Each passage was read in its surrounding section and checked against the paper's actual contribution before it was retained or excluded.

The online-date rule is important here. For example, *Matrix discrepancy and the log-rank conjecture* was first published online on 2024-07-05 but appears in a 2025 journal volume; it belongs to this review because the survey consistently uses online publication date.

## Inclusion rule

A problem was retained only when the source states a mathematically identifiable unresolved target: a conjecture, complexity bound, missing characterization, or precisely delimited extension. Generic calls for more experiments, applications to other problem classes, practical implementations, or an unspecified “better” method were excluded. Statements that describe an earlier open problem and then solve it in the same source were also excluded.

Separately answerable questions were split into separate records. Closely linked subcases in one source question were combined when separating them would duplicate the same representation problem. In particular, the zero-extension and directed-metric subcases remain one record, while the two logically independent scenario-optimization Beta questions are separate records.

Every source quotation contains at most 25 words. Normalized descriptions contain two to four substantive sentences, define the mathematical target in context, and avoid raw LaTeX or MathJax notation.

## Status protocol

Each retained problem received an evidence-bounded literature search through 2026-07-13. Searches combined exact source wording, paper title and authors, problem-specific terminology, and proof, counterexample, or resolution terms. Primary papers, publisher pages, proceedings records, and arXiv manuscripts were used for status evidence; a related title or a new reformulation was not counted as progress by itself.

The labels mean:

- `no_resolution_found`: no primary source explicitly proving or disproving the precise formulation was located. This is not proof that no resolution exists.
- `partial_progress`: a primary source proves a directly relevant restricted model or structural subclass while leaving the full formulation open.
- `resolved`: a primary source completely answers the retained formulation.
- `disputed`: incompatible primary claims would be recorded here.

Two records have partial progress:

- Non-migratory throughput maximization: Eberle's STACS 2024 paper gives an optimal-order non-migratory algorithm under a uniform slack assumption, including comparison with a migratory optimum on identical machines. It does not answer the source's unrestricted, no-high-laxity question.
- The four-thirds TSP integrality-gap conjecture: Villa, Vercesi, Barta, and Mastrolilli prove the conjecture when an optimal subtour-relaxation solution has at most the number of vertices plus six nonzero components. The general gap conjecture remains open.

The other 20 records are `no_resolution_found`. No retained problem in this split is marked resolved or disputed. Restricted results already discussed by a source paper were treated as context, not as a later status change; this avoids labeling every long-standing conjecture with a known special case as “partial progress.”

## Candidate-paper audit

| DOI | Paper | Disposition |
|---|---|---|
| 10.1007/s10107-023-02041-4 | High-order methods beyond the classical complexity bounds: inexact high-order proximal-point methods | Excluded. The passage says that better algorithms may be possible under unspecified methods or stronger assumptions; it does not fix a mathematical target. |
| 10.1007/s10107-023-02045-0 | A competitive algorithm for throughput maximization on identical machines | Included: 2 problems, the optimal competitive ratio and a non-migratory constant-competitive algorithm. |
| 10.1007/s10107-023-02048-x | Characterization of matrices with bounded Graver bases and depth parameters and applications to integer programming | Excluded. The cited fixed-parameter-tractability question is answered affirmatively by the source paper. |
| 10.1007/s10107-023-02050-3 | Mathematical Optimization for Fair Social Decisions: A Tribute to Michel Balinski | Excluded. The matched passage summarizes another contribution that addresses an open problem; it does not pose a source problem. |
| 10.1007/s10107-023-02049-w | Adjustability in robust linear optimization | Excluded. Asking whether a theorem is the “optimal” way to bound a ratio gives no formal comparison class or optimality criterion. |
| 10.1007/s10107-023-02053-0 | Designing tractable piecewise affine policies for multi-stage adjustable robust optimization | Excluded. The proposed generalizations to other two-stage results, recourse types, and data-driven models are broad research programs without a delimited theorem or complexity target. |
| 10.1007/s10107-023-02051-2 | Semiglobal exponential stability of the discrete-time Arrow-Hurwicz-Uzawa primal-dual algorithm for constrained optimization | Excluded. The source resolves the matched long-standing stability problem, while its distributed-algorithm remark is an underspecified future direction. |
| 10.1007/s10107-023-02052-1 | Deciding whether a lattice has an orthonormal basis is in co-NP | Included: 1 problem on constructing an orthonormal or orthogonal lattice basis faster than the exponential oracle route. |
| 10.1007/s10107-024-02061-8 | Automated tight Lyapunov analysis for first-order methods | Excluded. The high-recall match is a paper roadmap saying that a conclusion section discusses future work; no precise unresolved statement was located. |
| 10.1007/s10107-024-02058-3 | The effect of smooth parametrizations on nonconvex optimization landscapes | Included: 1 conjecture, the reverse inclusion associated with Theorem 3.16 for all smooth lifts. |
| 10.1007/s10107-024-02062-7 | Hessian barrier algorithms for non-convex conic optimization | Included: 1 problem on convergence of the full iterate trajectory. Other remarks about inexact subproblems, continuous-time analogues, acceleration, and higher orders were too open-ended to normalize without adding assumptions. |
| 10.1007/s10107-024-02057-4 | Level constrained first order methods for function constrained optimization | Included: 1 problem on controlling the complexity of reaching an approximate analytic center. The broader request to improve composite-case computational complexity was excluded as insufficiently delimited. |
| 10.1007/s10107-024-02065-4 | Matroid-based TSP rounding for half-integral solutions | Included: 2 conjectures, the four-thirds subtour-relaxation gap and the half-integral worst-case conjecture. The odd-vertex sampler question was excluded because the source solves it. |
| 10.1007/s10107-024-02064-5 | Generalized minimum 0-extension problem and discrete convexity | Included: 6 problems from the dedicated open-questions section: representation of tractable languages, structured zero-extension and directed-metric cases, normal-SDA iteration complexity, conjugacy, refinement of admissible relations, and explicit fractional-polymorphism construction. |
| 10.1007/s10107-024-02069-0 | The Chvátal-Gomory procedure for integer SDPs with applications in combinatorial optimization | Excluded. Efficient CG-cut separation is the earlier problem advanced by the source; the remaining suggestions concern empirical applications or a broad classification across other models. |
| 10.1007/s10107-024-02073-4 | Accelerated first-order methods for a class of semidefinite programs | Excluded. The matched remark asks for experiments using an implicitly stored structured matrix and does not state a mathematical performance claim. |
| 10.1007/s10107-024-02074-3 | Non-convex scenario optimization | Included: 2 problems about Beta-distribution bounds with and without a nonempty-interior assumption. |
| 10.1007/s10107-024-02077-0 | An update-and-stabilize framework for the minimum-norm-point problem | Excluded. Capacitated analysis, implementation comparisons, and benchmark experiments are proposed without a precise bound or conjecture. |
| 10.1007/s10107-024-02084-1 | From approximate to exact integer programming | Included: 1 problem asking for a singly exponential algorithm for exact general integer programming. |
| 10.1007/s10107-024-02085-0 | Graph coloring and semidefinite rank | Excluded. The Colin de Verdière conjecture appears as background motivation in the abstract, not as a source-formulated question developed or surveyed by the paper. |
| 10.1007/s10107-024-02086-z | A linear time algorithm for linearizing quadratic and higher-order shortest path problems | Included: 1 problem on linear time under sparse cost encoding. The practical implementation comparison was excluded. |
| 10.1007/s10107-024-02095-y | Polarized consensus-based dynamics for optimization and sampling | Excluded. Well-posedness, weaker assumptions, batching, and multimodal sampling are broad future programs without a single specified theorem. |
| 10.1007/s10107-024-02088-x | An asynchronous proximal bundle method | Excluded. “We do not know” describes unavailable current function values inherent to the asynchronous model, not an open mathematical question; the remaining future-work matches are computational directions. |
| 10.1007/s10107-024-02102-2 | A unified framework for symmetry handling | Excluded. Selection rules, empirical synergies, and framework updates are heuristic or implementation questions without a formal target. |
| 10.1007/s10107-024-02108-w | A slope generalization of Attouch theorem | Included: 1 problem on extending the finite-dimensional slope theorem to Hilbert and Banach spaces. |
| 10.1007/s10107-024-02089-w | On the directional asymptotic approach in optimization theory | Included: 1 conjecture replacing a coderivative sufficient condition by pseudo-subregularity. Broad numerical and calculus directions were excluded. |
| 10.1007/s10107-024-02117-9 | Matrix discrepancy and the log-rank conjecture | Included: 2 conjectures, the log-rank conjecture and Lovett's sparse-real-matrix zero-submatrix conjecture. |

## Output and checks

`2024_first_problems.json` contains 22 problems from 13 source papers: 20 with no resolution found, two with partial progress, zero resolved, and zero disputed. Each record contains source metadata, a short source quotation, a self-contained plain-text description, topic and keyword labels, recorded search queries, and primary progress evidence where applicable.

The deterministic builder is `scripts/build_2024_first_problems.py`. It regenerates the JSON from `screening.json` and checks record counts, the 25-word quote cap, two-to-four-sentence descriptions, status values, and the absence of raw LaTeX in descriptions.


---

# Mathematical Programming 2024 second-split survey methodology

Status checked through: 2026-07-13
Publication basis: Springer first-online date

## Scope and split boundary

This file reviews exactly the 27 dated candidates assigned in mp2024_second.tsv, ranging from 8 July through 24 December 2024. It is one adjudication split within the larger 2024 Mathematical Programming corpus, not a standalone claim that these 27 papers are the complete annual publication inventory. Both Series A and Series B are represented, and the date rule is first online publication rather than later issue assignment.

All 27 assigned papers had cached Springer HTML. Each article and every high-recall passage was read in context. Eighteen papers supplied at least one retained question and nine were excluded, producing **36 problems from 18 papers**.

## Admission and normalization rules

A record was admitted only when the source itself identified a definite unresolved mathematical statement, complexity target, missing characterization, or precisely scoped algorithmic extension. Generic requests for applications, experiments, implementations, or study of a broader setting were excluded. Statements proved or disproved in the same paper were also excluded even when a high-recall marker called them conjectures earlier in the exposition.

Every record has a unique readable title, one contiguous source quotation of at most 25 words, matched DOI and publisher text, and a self-contained normalized description. Descriptions contain two to four sentences, at least 220 characters, and plain prose with Unicode mathematics rather than raw LaTeX.

## Status protocol

Status was checked through 13 July 2026 using exact-statement, source-title, author, DOI, citation, publisher and arXiv searches. Only primary research papers or primary preprints were accepted as evidence of resolution or progress. A partial-progress label means a restricted case, materially sharper bound, or directly related theorem is known while the precise retained statement remains open.

The result is **28 no-resolution-found records, 8 partial-progress records, and 0 resolved records**. No-resolution-found is evidence-bounded: it does not prove that an unpublished, unindexed, or differently phrased resolution does not exist.

Partial progress was located for the sharp circuit Hirsch bound, restarted PDHG, two dyadic conjectures, the general Delta-modular conjecture, the Replication and tau-two conjectures, and Silver-stepsize optimality. The infeasible-PDHG and strict-Delta records remain no-resolution-found because the located results address certificate recovery and feasibility, not direct special cases of the retained tasks. No retained question was found to be fully resolved by the cutoff.

## Candidate-paper audit

| DOI | Paper | Disposition |
|---|---|---|
| 10.1007/s10107-024-02107-x | On circuit diameter bounds via circuit imbalances | Included: 3 problems. |
| 10.1007/s10107-024-02119-7 | Structural iterative rounding for generalized k-median problems | Included: 1 problem. |
| 10.1007/s10107-024-02109-9 | On the geometry and refined rate of primal–dual hybrid gradient for linear programming | Included: 4 problems. |
| 10.1007/s10107-024-02124-w | Convergence in distribution of randomized algorithms: the case of partially separable optimization | Included: 3 problems. |
| 10.1007/s10107-024-02116-w | On the correlation gap of matroids | Excluded. The conclusion asks broadly how much the correlation gap can be reduced and which parameters explain it, without stating a definite bound or decision problem. |
| 10.1007/s10107-024-02125-9 | A radial basis function method for noisy global optimisation | Excluded. The detected conjecture is introduced immediately before a theorem that establishes it; the remaining remark asks only for future empirical testing under other noise models. |
| 10.1007/s10107-024-02132-w | Configuration balancing for stochastic requests | Included: 1 problem. |
| 10.1007/s10107-024-02130-y | Machine learning augmented branch and bound for mixed integer linear programming | Excluded. The survey of machine-learning branch-and-bound identifies broad modeling and benchmarking gaps but no self-contained mathematical claim to prove or refute. |
| 10.1007/s10107-024-02135-7 | Recycling valid inequalities for robust combinatorial optimization with budgeted uncertainty | Excluded. The conclusion proposes recycling inequalities in other robust models and combining techniques, but supplies no precise approximation, complexity, or validity target. |
| 10.1007/s10107-024-02141-9 | A continuous approximation model for the electric vehicle fleet sizing problem | Excluded. The electric-vehicle application suggests exploring alternative approximation models and instance features; these are empirical modeling directions rather than source-explicit open questions. |
| 10.1007/s10107-024-02139-3 | The computational complexity of finding stationary points in non-convex optimization | Included: 2 problems. |
| 10.1007/s10107-024-02144-6 | Decomposition of probability marginals for security games in max-flow/min-cut systems | Excluded. The abstract says the paper partially answers an open question about a stronger oracle, but the accessible source never states the original question precisely enough for a self-contained record. |
| 10.1007/s10107-024-02146-4 | Dyadic linear programming and extensions | Included: 5 problems. |
| 10.1007/s10107-024-02147-3 | Cuts and semidefinite liftings for the complex cut polytope | Included: 1 problem. |
| 10.1007/s10107-024-02148-2 | Advances on strictly $$\Delta $$-modular IPs | Included: 3 problems. |
| 10.1007/s10107-024-02158-0 | Algebraic combinatorial optimization on the degree of determinants of noncommutative symbolic matrices | Included: 2 problems. |
| 10.1007/s10107-024-02154-4 | Accelerated-gradient-based generalized Levenberg–Marquardt method with oracle complexity bound and local quadratic convergence | Included: 2 problems. |
| 10.1007/s10107-024-02145-5 | A nearly optimal randomized algorithm for explorable heap selection | Included: 1 problem. |
| 10.1007/s10107-024-02149-1 | Optimization of trigonometric polynomials with crystallographic symmetry and spectral bounds for set avoiding graphs | Included: 1 problem. |
| 10.1007/s10107-024-02155-3 | From coordinate subspaces over finite fields to ideal multipartite uniform clutters | Included: 2 problems. |
| 10.1007/s10107-024-02157-1 | A projection-free method for solving convex bilevel optimization problems | Included: 1 problem. |
| 10.1007/s10107-024-02164-2 | Acceleration by stepsize hedging: Silver Stepsize Schedule for smooth convex optimization | Included: 1 problem. |
| 10.1007/s10107-024-02165-1 | Quantifying low rank approximations of third order symmetric tensors | Excluded. Future work calls for developing numerical methods and studying broader low-rank tensor approximations without a definite theorem, threshold, or complexity target. |
| 10.1007/s10107-024-02168-y | The polyhedral geometry of truthful auctions | Included: 2 problems. |
| 10.1007/s10107-024-02167-z | Regular packing of rooted hyperforests with root constraints in hypergraphs | Excluded. The apparent open-problem hits occur only in Springer's machine-generated Inline Recommendations sidebar and not in the article text. |
| 10.1007/s10107-024-02173-1 | Explicit convex hull description of bivariate quadratic sets with indicator variables | Excluded. The open convex-hull question detected in the introduction is solved by the paper itself; the remaining computational-study suggestion is generic. |
| 10.1007/s10107-024-02171-3 | Homogenization of SGD in high-dimensions: exact dynamics and generalization properties | Included: 1 problem. |


## Within-paper exclusions and ambiguities

- In 10.1007/s10107-024-02124-w, the request to extend the theory to multivalued mappings was excluded as a broad program without a definite target theorem; the three precise technical questions in the same final paragraph were retained.
- In 10.1007/s10107-024-02144-6, the phrase “partially answering an open question” could plausibly refer to strongly polynomial abstract maximum-flow algorithms under a stronger shortest-path oracle. Because the accessible article never states that original question and its model precisely, the paper is logged as ambiguous rather than treated as a negative.
- In 10.1007/s10107-024-02148-2, the group-constrained lattice feasibility question is not catalogued because Theorems 9 and 10 of the source answer it. The optimization problem for fixed composite moduli remains open and is retained.
- In 10.1007/s10107-024-02149-1, an experimentally suggested extremal measure for a particular hexagonal example was excluded because the paper does not formulate it as a stable general proposition; the measurable-chromatic-number equality is retained.
- In 10.1007/s10107-024-02158-0, three-dimensional generic rigidity is incidental background rather than a problem posed by the authors, and a broader request to extend the CLV framework lacks a precise target. The commutative Edmonds problem and general Brascamp–Lieb membership target are retained.
- In 10.1007/s10107-024-02164-2, an older conjectured O((n log n)⁻¹) rate is omitted because the source's Silver schedule already supersedes it with a faster proved rate. The source's explicit optimal-exponent conjecture is retained.
- In 10.1007/s10107-024-02168-y, historical Nisan–Ronen and Vidali questions described as answered by cited or current results were excluded, as was a broad suggestion about externalities. Numbered Questions 24 and 25 remain precise and are retained.
- In 10.1007/s10107-024-02171-3, informal expectations in footnotes were excluded; the explicit batch-size conjecture β=o(n) was retained.

## Reproducibility

- Assignment ledger: /Users/samlai/Documents/gitpage/.codex-work/review-splits/mp2024_second.tsv
- Screening inventory: screening.json
- Cached publisher text: fulltext/*.html
- Curated records: 2024_second_problems.json
- Builder and validation: build_2024_second_outputs.py

The build validates the 27-paper partition, 36-record count, 18 retained source papers, unique identifiers and titles, quotation length, description length, sentence count, and absence of raw LaTeX commands in normalized descriptions.


---

# Mathematical Programming 2026 audit methodology

## Scope and corpus

This pass covers *Mathematical Programming* records whose Springer online-publication date falls from 1 January 2026 through 13 July 2026. The shared screening inventory contains 78 records in that interval: 76 research articles and two nonresearch items (one correction and one special-issue notice). The date rule is online publication rather than issue assignment, so papers first posted earlier but assigned to a 2026 issue are not silently moved into this slice.

## Screening and manual adjudication

The high-recall screen searched cached Springer HTML for explicit markers such as *open problem*, *open question*, *conjecture*, *unknown*, *unresolved*, and *future work*. It flagged 38 research articles. Every flagged 2026 article and every candidate passage was then read manually in context; 24 papers supplied at least one precise, source-explicit open problem and 14 were excluded. Generic requests for applications, experiments, tuning, or extensions were excluded unless the authors stated a definite mathematical or complexity task.

The final file contains **50 problems from 24 papers**. Each record has a unique readable title, a contiguous source quotation of at most 25 words, source DOI/authors/date, and a two-to-four-sentence normalized description of at least 220 characters. Descriptions use plain prose and Unicode mathematics rather than raw LaTeX commands.

## Status review

Status was checked through **13 July 2026** with source-DOI, exact-statement, title, author, citation, publisher, and arXiv searches, and only primary research outputs were accepted as resolution or progress evidence. The result is 45 records with no resolution located, 4 with identifiable partial progress, and 1 resolved record. “No resolution found” is an evidence-bounded search result, not a proof that no unpublished or unindexed result exists.

The resolved item is Powell's conjecture about exponential trust-region complexity with linearly growing model Hessians, settled by DOI `10.1007/s10107-025-02287-0`. Partial-progress labels are used for the bounded-subdeterminant integer-programming conjecture, the two unsplittable-flow conjectures, and Oertel's mixed-integer Grünbaum conjecture; their evidence records identify the precise special cases added by later primary work.

## Exclusions and ambiguities

- **10.1007/s10107-025-02308-y — Exponential convergence rates for momentum stochastic gradient descent in the overparametrized setting**: The momentum statement is a broad empirical motivation, not a mathematically quantified conjecture in the article.
- **10.1007/s10107-025-02322-0 — A Lyapunov analysis of Korpelevich’s extragradient method with fast and flexible extensions**: The conclusion lists broad method extensions without a precise proposition, complexity target, or yes/no task.
- **10.1007/s10107-026-02329-1 — Bounding the optimal number of policies for robust K-Adaptability**: Requests for better constants, more applications, and efficient methods are generic research directions rather than precise open problems.
- **10.1007/s10107-026-02328-2 — Finding almost tight witness trees**: The detected Steiner-tree conjecture is historical background that the cited later work already resolves.
- **10.1007/s10107-026-02337-1 — Distributionally robust optimization with multimodal decision-dependent ambiguity sets**: The hits concern applications, decomposition alternatives, and nonconvex extensions stated only as generic future work.
- **10.1007/s10107-026-02326-4 — New finite relaxation hierarchies for concavo-convex, disjoint bilinear programs, and facial disjunctions**: The conclusion discusses computational exploration and implementation tradeoffs, without a source-explicit mathematical claim to decide.
- **10.1007/s10107-026-02347-z — Totally equimodular matrices: decomposition and triangulation**: Only the abstract was accessible; 'cases not covered here do not exist' is not self-contained enough to identify the excluded cases reliably.
- **10.1007/s10107-026-02354-0 — Fast finite-sum optimization via cyclically-sampled Hessian averaging methods**: Inexact line searches, applications, and stochastic extensions are implementation plans rather than precise open questions.
- **10.1007/s10107-026-02356-y — Strongly-polynomial time and validation analysis of policy gradient methods**: Extending the advantage-gap analysis to general spaces is a broad future-work direction without a definite target theorem.
- **10.1007/s10107-025-02313-1 — Exact worst-case convergence rates of gradient descent: a complete analysis for all constant stepsizes over nonconvex and convex functions**: The article's candidate passage describes conjectured rates that the article itself proves; it does not leave that question open.
- **10.1007/s10107-026-02361-1 — Accelerating operator Sinkhorn iteration with overrelaxation**: Combining overrelaxation variants and broadening global convergence ranges are stated as future directions, not precise conjectures.
- **10.1007/s10107-026-02370-0 — Eliciting Von Neumann–Morgenstern utility from discrete choices with response error**: The note flags broader modeling and testing issues but supplies no specific mathematical statement to verify.
- **10.1007/s10107-026-02368-8 — MDP modeling for multi-stage stochastic programs**: Large-scale experiments, adaptive implementation, and risk-aversion integration are generic software and empirical future work.
- **10.1007/s10107-026-02376-8 — Accelerating diagonal methods for bilevel optimization: Unified convergence via continuous-time dynamics**: The phrase 'we do not know' concerns whether a sequence is bounded before applying a lemma, not an open research problem.


The remaining 38 research articles were high-recall negatives: their cached full text contained no candidate markers. The subscription-only abstract for `10.1007/s10107-026-02347-z` was not promoted into the catalogue because its phrase “cases not covered here do not exist” did not expose enough of the classification to state the conjecture faithfully. This is logged as an ambiguity rather than treated as evidence that the paper has no open problem.

## Reproducibility notes

- Screening input: `screening.json`
- Cached publisher text: `fulltext/*.html`
- Curated output: `2026_problems.json`
- Build and validation script: `build_2026_outputs.py`

The build validates record count, unique IDs and titles, quotation length, description length, sentence count, and absence of raw LaTeX commands in descriptions.

