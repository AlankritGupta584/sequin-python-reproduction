from itertools import combinations, permutations
from grid_model import initial_state, defend, shed_pu


def run_sequence(case, sequence, ramp=0.1, simple_ramp=False):
    state = initial_state(case)
    failed = []
    history = []
    for line in sequence:
        failed.append(int(line))
        state = defend(case, failed, state, ramp, simple_ramp=simple_ramp)
        if state is None:
            return None
        history.append(shed_pu(case, state))
    return history[-1], history


def exact_simultaneous(case, k=2, ramp=0.1):
    """Small-case only: try every k-line set and let defender react once."""
    start = initial_state(case)
    best = (-1, None)
    for lines in combinations(range(1, len(case['branch']) + 1), k):
        state = defend(case, list(lines), start, ramp)
        if state is None:
            continue
        score = shed_pu(case, state)
        if score > best[0]:
            best = (score, lines)
    return best


def exact_sequential(case, k=2, ramp=0.1):
    """Small-case only: try every ordered sequence."""
    best = (-1, None, None)
    for seq in permutations(range(1, len(case['branch']) + 1), k):
        out = run_sequence(case, seq, ramp)
        if out is None:
            continue
        score, hist = out
        if score > best[0]:
            best = (score, seq, hist)
    return best


def greedy_impact(case, k, ramp=0.1, simple_ramp=False):
    """At each step, fail the line that gives the largest immediate load shed."""
    state = initial_state(case)
    failed = []
    hist = []
    for _ in range(k):
        best = (-1, None, None)
        for line in range(1, len(case['branch']) + 1):
            if line in failed:
                continue
            cand = defend(case, failed + [line], state, ramp, simple_ramp=simple_ramp)
            if cand is None:
                continue
            score = shed_pu(case, cand)
            if score > best[0] + 1e-10 or (abs(score - best[0]) <= 1e-10 and (best[1] is None or line < best[1])):
                best = (score, line, cand)
        failed.append(best[1])
        state = best[2]
        hist.append(best[0])
    return hist[-1], tuple(failed), hist


def guided_search(case, k, ramp=0.1, top_n=10):
    """Small student version of SEQUIN's idea.

    Start from a few high-flow lines. After each failure, keep only the next
    top_n lines by current |flow|, test those with the defender, and continue
    using the one with highest immediate load shed.
    """
    start = initial_state(case)
    first = sorted(start['flows'], key=lambda i: -abs(start['flows'][i]))[:top_n]
    overall = (-1, None, None)

    for first_line in first:
        failed = [first_line]
        state = defend(case, failed, start, ramp)
        if state is None:
            continue
        hist = [shed_pu(case, state)]

        while len(failed) < k:
            candidates = [i for i in sorted(state['flows'], key=lambda i: -abs(state['flows'][i]))
                          if i not in failed][:top_n]
            best = (-1, None, None)
            for line in candidates:
                cand = defend(case, failed + [line], state, ramp)
                if cand is None:
                    continue
                score = shed_pu(case, cand)
                if score > best[0] + 1e-10 or (abs(score - best[0]) <= 1e-10 and (best[1] is None or line < best[1])):
                    best = (score, line, cand)
            if best[1] is None:
                break
            failed.append(best[1])
            state = best[2]
            hist.append(best[0])

        if len(failed) == k and hist[-1] > overall[0]:
            overall = (hist[-1], tuple(failed), hist)

    return overall
