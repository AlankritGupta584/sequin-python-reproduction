import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from grid_model import load_case
from search_methods import exact_simultaneous, exact_sequential, greedy_impact, guided_search

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, 'data')
RESULTS = os.path.join(HERE, 'results')
PLOTS = os.path.join(HERE, 'plots')
os.makedirs(RESULTS, exist_ok=True)
os.makedirs(PLOTS, exist_ok=True)

rows = []

case14 = load_case(os.path.join(DATA, 'pglib_opf_case14_ieee__api.m'))
sim = exact_simultaneous(case14, k=2, ramp=0.1)
seq = exact_sequential(case14, k=2, ramp=0.1)
guided14 = guided_search(case14, k=2, ramp=0.1, top_n=10)

for method, item in [('simultaneous exact', sim), ('sequential exact', seq), ('guided', guided14)]:
    rows.append(['case14', 2, 0.1, method, item[0], str(item[1]), 'independent'])

plt.figure(figsize=(6.2, 4.0))
plt.bar(['Simultaneous\nexact', 'Sequential\nexact', 'Guided\nsearch'], [sim[0], seq[0], guided14[0]])
plt.ylabel('Final load shed (p.u.)')
plt.title('Case 14: independent student implementation')
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, '01_case14_core_reproduction.png'), dpi=180)
plt.close()

case39 = load_case(os.path.join(DATA, 'pglib_opf_case39_epri__api.m'))
author = pd.read_csv(os.path.join(DATA, 'author_case39_exp1.csv'))
compare = []

for k in [2, 3, 4]:
    ours_g = greedy_impact(case39, k=k, ramp=0.1)
    ours_s = guided_search(case39, k=k, ramp=0.1, top_n=10)
    a_g = author[(author.k == k) & (author.problem == 'greedy_impt')].load_shed.max()
    a_s = author[(author.k == k) & (author.problem == 'sequin')].load_shed.max()
    compare.append([k, 'greedy impact', ours_g[0], a_g, 100 * (ours_g[0] - a_g) / a_g])
    compare.append([k, 'guided', ours_s[0], a_s, 100 * (ours_s[0] - a_s) / a_s])
    rows.append(['case39', k, 0.1, 'greedy impact', ours_g[0], str(ours_g[1]), 'independent'])
    rows.append(['case39', k, 0.1, 'guided', ours_s[0], str(ours_s[1]), 'independent'])

pd.DataFrame(compare, columns=['k','method','our_load_shed','author_reference','difference_percent']).to_csv(
    os.path.join(RESULTS, 'case39_author_comparison.csv'), index=False)

cmp = pd.DataFrame(compare, columns=['k','method','our','author','diff'])
fig, ax = plt.subplots(figsize=(7.0, 4.2))
x = range(len(cmp))
ax.bar([i - 0.18 for i in x], cmp['our'], width=0.36, label='Our Python')
ax.bar([i + 0.18 for i in x], cmp['author'], width=0.36, label='Author reference')
ax.set_xticks(list(x))
ax.set_xticklabels([f"k={r.k}\n{r.method}" for r in cmp.itertuples()], fontsize=8)
ax.set_ylabel('Load shed (p.u.)')
ax.set_title('Case 39: independent Python vs author reference')
ax.legend()
fig.tight_layout()
fig.savefig(os.path.join(PLOTS, '02_case39_reference_comparison.png'), dpi=180)
plt.close(fig)

author_ramp = pd.read_csv(os.path.join(DATA, 'author_case39_ramp_k3.csv'))
ramp_rows = []
for ramp in [1.0, 0.5, 0.25, 0.1, 0.0]:
    ours = greedy_impact(case39, k=3, ramp=ramp, simple_ramp=True)
    ref = author_ramp[(author_ramp.percent_change == ramp) & (author_ramp.problem == 'greedy_impt')].load_shed.max()
    ramp_rows.append([ramp, ours[0], ref])
    rows.append(['case39', 3, ramp, 'simple ramp greedy impact', ours[0], str(ours[1]), 'partial independent'])

ramp_df = pd.DataFrame(ramp_rows, columns=['ramp','our_simple_model','author_reference'])
ramp_df.to_csv(os.path.join(RESULTS, 'ramp_partial_reproduction.csv'), index=False)

plt.figure(figsize=(6.5, 4.1))
plt.plot(ramp_df['ramp'], ramp_df['our_simple_model'], marker='o', label='Simple Python model')
plt.plot(ramp_df['ramp'], ramp_df['author_reference'], marker='o', label='Author reference')
plt.gca().invert_xaxis()
plt.xlabel('Generator ramp fraction (more restrictive →)')
plt.ylabel('Load shed (p.u.)')
plt.title('Case 39 ramping: partial reproduction')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(PLOTS, '03_case39_partial_ramp_reproduction.png'), dpi=180)
plt.close()

with open(os.path.join(RESULTS, 'all_results.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['case','k','ramp','method','load_shed','sequence','evidence'])
    w.writerows(rows)

print('\nCASE 14')
print('simultaneous exact:', sim)
print('sequential exact  :', seq)
print('guided search     :', guided14)
print('\nCASE 39 comparison')
print(pd.DataFrame(compare, columns=['k','method','our','author','difference_%']).to_string(index=False))
print('\nPARTIAL ramp reproduction')
print(ramp_df.to_string(index=False))
print('\nWrote results/ and plots/.')
