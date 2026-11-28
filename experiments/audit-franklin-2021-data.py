"""Audit aggregate claims using the two public Figshare CSVs; never emit records.

Usage: python3 experiments/audit-franklin-2021-data.py STUDY1.csv STUDY2.csv
Uses independently written NumPy/SciPy calculations, not author analysis code.
Raw participant data and free text must remain outside this repository.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def fit(y, x):
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    return float(np.sum((y - x @ beta) ** 2)), int(np.linalg.matrix_rank(x))


def nested(y, small, large):
    ss0, r0 = fit(y, small)
    ss1, r1 = fit(y, large)
    df1, df2 = r1 - r0, len(y) - r1
    f = max(0.0, (ss0 - ss1) / df1 / (ss1 / df2))
    return {'F': f, 'df': [df1, df2], 'p': float(stats.f.sf(f, df1, df2))}


def anovas(y, driver, situation):
    one = np.ones((len(y), 1))
    d = pd.get_dummies(driver, drop_first=True).to_numpy(dtype=float)
    s = pd.get_dummies(situation, drop_first=True).to_numpy(dtype=float)
    additive = np.column_stack((one, d, s))
    cell = pd.get_dummies(list(zip(driver, situation))).to_numpy(dtype=float)
    # Sum contrasts permit standard Type III tests in a model with interaction.
    def sum_contrasts(values):
        levels = np.unique(values)
        return np.column_stack([np.where(values == level, 1., np.where(values == levels[-1], -1., 0.))
                                for level in levels[:-1]])
    dc, sc = sum_contrasts(np.asarray(driver)), sum_contrasts(np.asarray(situation))
    interaction = np.column_stack([dc[:, i] * sc[:, j] for i in range(dc.shape[1]) for j in range(sc.shape[1])])
    full = np.column_stack((one, dc, sc, interaction))
    return {
        'one_way_driver': nested(y, one, np.column_stack((one, d))),
        'one_way_situation': nested(y, one, np.column_stack((one, s))),
        'additive_driver_adjusting_situation': nested(y, np.column_stack((one, s)), additive),
        'additive_situation_adjusting_driver': nested(y, np.column_stack((one, d)), additive),
        'interaction_vs_additive': nested(y, additive, cell),
        'full_interaction_type_iii_driver': nested(y, np.column_stack((one, sc, interaction)), full),
        'full_interaction_type_iii_situation': nested(y, np.column_stack((one, dc, interaction)), full),
        'note': 'Additive tests use their own residual MS; not asserted to be the authors\' exact model. One row is one participant, totals are repeated-item sums.'}


def descriptives(frame, groups, columns):
    out = []
    for key, part in frame.groupby(groups, observed=True):
        key = key if isinstance(key, tuple) else (key,)
        out.append({'group': [int(v) for v in key], 'n': len(part),
                    'outcomes': {c: {'mean': float(part[c].mean()),
                                     'sd': float(part[c].std(ddof=1))} for c in columns}})
    return out


def regression(x, y):
    r = stats.linregress(x, y)
    return {'n': len(x), 'slope': float(r.slope), 'r_squared': float(r.rvalue ** 2),
            'F': float((r.slope / r.stderr) ** 2), 'df': [1, len(x)-2], 'p': float(r.pvalue)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('study1', type=Path)
    parser.add_argument('study2', type=Path)
    args = parser.parse_args()
    first = pd.read_csv(args.study1, encoding='cp1252')
    second = pd.read_csv(args.study2, encoding='utf-8-sig')
    group1 = first.iloc[:, 1].to_numpy()
    first['driver'] = np.where(np.isin(group1, [1, 3]), 1, 2)
    first['situation'] = np.where(np.isin(group1, [1, 2]), 1, 2)
    assert set(group1) == {1, 2, 3, 4}
    for outcome in ['cause', 'blame']:
        first[outcome] = first[[f'Q{i}{outcome}' for i in range(1, 7)]].sum(axis=1)
    driver2, situation2 = 'Human or AI (1,2)', 'Mistake (S1, N2, C3)'
    assert set(second[driver2]) == {1, 2}
    assert set(second[situation2]) == {1, 2, 3}
    outcomes = ['Total Cause', 'Total Blame', 'Total Novelty', 'Total Difficulty']
    sum_checks = {}
    for total, suffix in zip(outcomes, ['Cause', 'Blame', 'Novel', 'Difficult']):
        cols = [f'Q{i} {suffix}' if not (i == 4 and suffix == 'Difficult') else 'Q4Difficult'
                for i in range(1, 6)]
        sum_checks[total] = bool((second[cols].sum(axis=1) == second[total]).all())
    out = {'method': 'Independent aggregate reanalysis, public cleaned data; no free text, demographics, identifiers or participant rows emitted.',
           'files': [{'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                      'md5': hashlib.md5(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
                     for p in [args.study1, args.study2]],
           'study1': {'n': len(first), 'cell_summary': descriptives(first, ['driver', 'situation'], ['cause', 'blame']),
                      'anova': {c: anovas(first[c].to_numpy(), first.driver, first.situation) for c in ['cause', 'blame']}},
           'study2': {'n': len(second), 'sum_checks': sum_checks,
                      'cell_summary': descriptives(second, [driver2, situation2], outcomes),
                      'situation_summary': descriptives(second, [situation2], outcomes),
                      'anova': {c: anovas(second[c].to_numpy(), second[driver2], second[situation2]) for c in outcomes}}}
    out['study2']['individual_items_one_way_driver'] = {
        f'Q{i} {suffix}': anovas(second[f'Q{i} {suffix}'].to_numpy(), second[driver2], second[situation2])['one_way_driver']
        for i in range(1, 6) for suffix in ['Cause', 'Blame']}
    trust, expected = 'I trust other drivers/SDC', 'Knew that a mistake was about to happen'
    out['study2']['post_outcome_regressions'] = {}
    for g in [1, 2]:
        sub = second[second[driver2] == g]
        out['study2']['post_outcome_regressions'][str(g)] = {
            c: regression(sub[trust], sub[c]) for c in ['Total Cause', 'Total Blame']}
    out['study2']['post_outcome_regressions']['pooled_expected'] = {
        c: regression(second[expected], second[c]) for c in ['Total Cause', 'Total Blame']}
    out['study2']['expected_mistake_summary'] = descriptives(second, [driver2], [expected])
    a, b = (second.loc[second[driver2] == g, expected].to_numpy() for g in [1, 2])
    pooled_sd = np.sqrt(((len(a)-1)*np.var(a, ddof=1)+(len(b)-1)*np.var(b, ddof=1))/(len(a)+len(b)-2))
    t, p = stats.ttest_ind(a, b, equal_var=True)
    out['study2']['expected_mistake_test'] = {'t': float(t), 'df': len(a)+len(b)-2, 'p_two_sided': float(p),
                                             'cohen_d_human_minus_ai': float((a.mean()-b.mean())/pooled_sd)}
    out['study2']['within_driver_tukey_hsd'] = {}
    for g in [1, 2]:
        for c in ['Total Novelty', 'Total Difficulty']:
            arrays = [second.loc[(second[driver2] == g) & (second[situation2] == s), c].to_numpy() for s in [1, 2, 3]]
            result = stats.tukey_hsd(*arrays)
            ci = result.confidence_interval()
            out['study2']['within_driver_tukey_hsd'][f'driver{g}:{c}'] = [
                {'contrast': f'{a+1} minus {b+1}', 'difference': float(result.statistic[a, b]),
                 'p': float(result.pvalue[a, b]), 'ci95': [float(ci.low[a, b]), float(ci.high[a, b])]}
                for a, b in [(0, 1), (0, 2), (1, 2)]]
    print(json.dumps(out, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
