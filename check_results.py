from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent

c = pd.read_csv(HERE / 'results' / 'case39_author_comparison.csv')
assert abs(c[(c.k == 2) & (c.method == 'guided')].difference_percent.iloc[0]) < 1e-6
assert abs(c[(c.k == 3) & (c.method == 'guided')].difference_percent.iloc[0]) < 1e-6
assert abs(c[(c.k == 4) & (c.method == 'guided')].difference_percent.iloc[0]) < 2.0
assert abs(c[(c.k == 4) & (c.method == 'greedy impact')].difference_percent.iloc[0]) < 2.0

r = pd.read_csv(HERE / 'results' / 'ramp_partial_reproduction.csv')
assert abs(r.iloc[0].our_simple_model - r.iloc[0].author_reference) < 1e-6
assert abs(r.iloc[-1].our_simple_model - r.iloc[-1].author_reference) > 1.0

print('PASS: selected full reproductions agree, and partial-ramp limitation is visible.')
