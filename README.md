# SEQUIN Python Reproduction

A compact, independent Python/SciPy reproduction of selected ideas from:

> Andrew Chio, Russell Bent, Kaarthik Sundar, and Nalini Venkatasubramanian, **“SEQUIN: A Network Science and Physics-based Approach to Identify Sequential N-k Attacks in Electric Power Grids,”** ACM/IEEE ICCPS 2025.

Original authors' implementation: https://github.com/andrewgchio/SEQUIN

It is **not** a line-by-line rewrite of the authors' Julia/PowerModels/JuMP/Gurobi code. The goal is to independently implement enough of the core sequential-attack idea to reproduce selected results and verify the model.

## What is implemented

- MATPOWER case reader for the selected benchmark inputs.
- DC grid/load-shedding defender model using SciPy optimization.
- Line-outage evaluation.
- Generator ramp limits and sequential state propagation.
- Exact simultaneous search for small cases.
- Exact ordered sequential enumeration for small cases.
- Greedy immediate-impact search.
- A compact SEQUIN-style guided search.
- Comparison against selected released author results.
- Reproduction plots and automated sanity checks.

## Repository structure

```text
.
├── grid_model.py
├── search_methods.py
├── run_reproduction.py
├── check_results.py
├── requirements.txt
├── data/
│   ├── pglib_opf_case14_ieee__api.m
│   ├── pglib_opf_case39_epri__api.m
│   ├── author_case39_exp1.csv
│   └── author_case39_ramp_k3.csv
├── results/
├── plots/
└── docs/
    └── STUDENT_REPORT_NOTES.md
```

## Reproduction experiments

### 1. Case 14 — core sequential-vs-simultaneous result

For `k=2`, the independent Python model compares exact simultaneous N-2 search, exact ordered sequential search, and guided search. The small case is useful because exact ordered enumeration provides a ground-truth check for the guided method.

### 2. Case 39 — selected author-reference cross-check

For `k=2,3,4`, the compact greedy-impact and guided methods are compared with selected released author-reference values. This is an independent numerical cross-check, not simply a rerun of the Julia repository.

### 3. Case 39 — partial ramping reproduction

A deliberately simplified continuous-ramp model is compared with the authors' full formulation. It matches the unrestricted point but diverges under tight ramping because the compact model omits some full defender recourse details, especially generator on/off behavior. This experiment is therefore labelled **partial reproduction** rather than forced into an artificial exact match.

## Install and run

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run_reproduction.py
python check_results.py
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python run_reproduction.py
python check_results.py
```

The simplified implementation does **not** require a Gurobi license; SciPy's HiGHS backend is used.

## Outputs

Running `run_reproduction.py` writes:

```text
results/all_results.csv
results/case39_author_comparison.csv
results/ramp_partial_reproduction.csv

plots/01_case14_core_reproduction.png
plots/02_case39_reference_comparison.png
plots/03_case39_partial_ramp_reproduction.png
```

## Academic scope

A safe description of this repository is:

> We independently implemented a compact DC line-outage and sequential-response model in Python/SciPy. We reproduce the central small-case sequential-vs-simultaneous phenomenon, cross-check selected Case-39 search results against released author-reference values, and separately report a simplified ramping experiment where omitted defender details lead to a partial rather than exact reproduction.

It should **not** be described as a complete reimplementation of every SEQUIN experiment or of the full PowerModels/JuMP defender formulation.

## Data provenance

The PGLib/MATPOWER benchmark inputs and selected author-reference values are included only to support reproduction and comparison. Credit for the original SEQUIN paper, implementation, benchmark sources, and released experiment data belongs to the original authors and PGLib-OPF contributors. See the original SEQUIN repository above for the authors' project and licensing information.
