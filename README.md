# SEQUIN Python Reproduction

Independent Python/SciPy reproduction and analysis of selected mechanisms from:

> Andrew Chio, Russell Bent, Kaarthik Sundar, and Nalini Venkatasubramanian, **“SEQUIN: A Network Science and Physics-based Approach to Identify Sequential N-k Attacks in Electric Power Grids,”** ACM/IEEE ICCPS 2025.

Original authors' implementation: https://github.com/andrewgchio/SEQUIN

This repository is intentionally **not** a line-by-line rewrite of the Julia/PowerModels/JuMP/Gurobi artifact. It independently implements the core DC defender and sequential search mechanisms, then compares them against the authors' released experiment outputs. Good matches, partial matches, and failures are all kept visible.

## Implemented model

- MATPOWER parser for six PGLib cases used in the paper.
- DC bus balance and branch-flow equations.
- Branch thermal limits and phase-angle limits.
- Line outages and connected-island reference angles.
- Load shedding with already-shed load unavailable in later rounds.
- Generator ramp bounds.
- Binary generator on/off recourse for the fuller defender model.
- Optional deliberately simplified continuous-ramp model for ablation.
- Optional deterministic ±5% load perturbation with explicit random seed.
- Handling of negative MATPOWER loads as fixed net injections (needed for Case 162/240 fidelity).

## Search methods

- Exact simultaneous search for small cases.
- Exact ordered sequential enumeration for small cases.
- Greedy-FLOW.
- Greedy-IMPACT / immediate load shed.
- Greedy criticality variants, including an author-style state-update version.
- SEQUIN-style guided search matching the active released `ours.jl` path: top-10 current power-flow shortlist followed by cut-impact selection.
- PERM reproduction by enumerating orders of a fixed author STD line set.
- Replay of an author's exact attack sequence to isolate physical-model fidelity from search differences.

## Two levels of experiments

### Quick/core reproduction

```bash
python run_reproduction.py
python check_results.py
```

### Expanded evaluation suite

```bash
python run_extended_reproduction.py
python check_extended_results.py
python make_extended_plots.py
```

The expanded suite covers all six paper networks, Greedy-FLOW `k=2..8`, same-author-sequence replay, selected Guided / Greedy-IMPACT searches, PERM, ramp sensitivity, defender-model ablation, ±5% load perturbation sensitivity, measured runtime/solver calls, and explicit divergence diagnosis.

Large searches are deliberately selective. Full Greedy-IMPACT or exact enumeration on the largest grids would require thousands to tens of thousands of repeated MILP solves; those are recorded as computational limitations rather than silently presented as completed experiments.

## Main verified findings

- **Case 14, k=2:** exact simultaneous = `3.7500`, exact sequential = `4.3997`, guided = `4.3997`.
- **Case 14 guided search:** exact match on tested `k=2,3,4,8`.
- **Case 39 guided search:** tested `k=2,3,4,6` stay within about 1.1% of the released reference.
- **Case 162 guided k=2:** within 5%.
- **Case 240:** replaying the authors' exact SEQUIN sequence stays within about 2% at tested k values.
- **Ramp replay:** same-sequence ramp tests are particularly close for Cases 39, 162, and 240.
- **Simplified ramp ablation:** fails badly under tight ramping, showing binary generator recourse materially affects the result.
- **Load perturbation:** independent ±5% draws can substantially change both the selected sequence and final load shed; the released experiment code does not preserve RNG state.

See `results/divergence_diagnosis_fresh.csv` and `results/limitations_fresh.csv` for machine-readable mismatch analysis.

## Install

```bash
python -m venv .venv
pip install -r requirements.txt
```

The Python reproduction does **not** require a Gurobi license; SciPy's HiGHS backend is used.

## Academic scope

A safe description is:

> We independently implemented a compact DC line-outage and sequential-response model in Python/SciPy, reproduced the core small-case phenomenon exactly, reproduced selected guided-search results closely, broadened the evaluation to all six paper networks through search and same-sequence replay tests, and explicitly analyzed where differences arise from randomized inputs, search sensitivity, model simplification, and computational cost.

It should not be described as a complete replacement for PowerModels/JuMP/Gurobi or as an exact reproduction of every randomized author run.
