"""Audit public supplementary aggregates without emitting participant records.

Usage: python3 experiments/audit-kallioinen-2019-data.py Data_Sheet_1.CSV Data_Sheet_2.CSV
No author code, mixed-model refit or causal mechanism replication is implied.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.special import expit


def chi(table):
    value, p, df, expected = stats.chi2_contingency(table, correction=False)
    return {'counts': np.asarray(table).astype(int).tolist(), 'n': int(np.sum(table)),
            'chi_squared': float(value), 'df': int(df), 'p': float(p),
            'minimum_expected': float(expected.min())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('study1', type=Path)
    parser.add_argument('study2', type=Path)
    args = parser.parse_args()
    frames = [pd.read_csv(p) for p in [args.study1, args.study2]]
    result = {'scope': 'Independent descriptive and contingency checks only; raw rows, identifiers and demographics not emitted.',
              'files': [{'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                        for p in [args.study1, args.study2]], 'studies': []}
    for frame in frames:
        # Labels describe assigned scenarios/roles, not individual responses.
        stable = ['motorist', 'identification']
        assert all(frame.groupby('participant')[c].nunique().max() == 1 for c in stable)
        participants = frame.drop_duplicates('participant')
        count = frame.groupby('participant').size().value_counts().sort_index()
        entry = {'rows': len(frame), 'participants': len(participants),
                 'trial_count_distribution': {str(k): int(v) for k, v in count.items()},
                 'task_labels': {c: sorted(str(v) for v in frame[c].dropna().unique())
                                 for c in ['perspective', 'motorist', 'scenario', 'judgement']},
                 'scenario_summary': []}
        for scenario, sub in frame.groupby('scenario'):
            entry['scenario_summary'].append({'scenario': str(scenario), 'participants': int(sub.participant.nunique()),
                                               'trials': len(sub), 'judgement_counts': {str(k): int(v) for k, v in sub.judgement.value_counts().items()}})
        # Each participant contributes once, rather than once per repeated trial.
        role = participants['perspective'].str.lower().map(
            lambda v: 'pedestrian' if 'pedestrian' in v else 'passenger' if v in {'car', 'car occupant', 'passenger'} else v)
        table = pd.crosstab(role, participants.identification)
        entry['collapsed_role_identification'] = {'row_labels': list(table.index), 'column_labels': list(table.columns), **chi(table.to_numpy())}
        if 'age_group' in participants:
            specific = participants.perspective.replace({'pedestrian_fwd': 'pedestrian_front'})
            table = pd.crosstab(specific, participants.identification)
            entry['four_role_identification'] = {'row_labels': list(table.index), 'column_labels': list(table.columns), **chi(table.to_numpy())}
        if 'age_group' in participants:
            entry['missing_age_group_participants'] = int(participants.age_group.isna().sum())
        result['studies'].append(entry)
    result['printed_manipulation_tables'] = {
        'S2': chi(np.array([[31, 10, 5], [8, 35, 3], [33, 3, 56]])),
        'S13': chi(np.array([[73, 28], [53, 42], [21, 65], [23, 63]]))}
    result['printed_table4_checks'] = {
        'road_type': {'chi_squared': 9.87, 'df': 1, 'p_asymptotic': float(stats.chi2.sf(9.87, 1))},
        'three_way_pedestrians': {'chi_squared': 20.47, 'df': 9, 'p_asymptotic': float(stats.chi2.sf(20.47, 9))},
        'three_way_occupants': {'chi_squared': 14.07, 'df': 6, 'p_asymptotic': float(stats.chi2.sf(14.07, 6))}}
    result['printed_supplement_scale_checks'] = {
        'S16_log_odds_to_probability': [float(expit(x)) for x in [2.0196, 1.1519]],
        'S15_exponentiated_log_odds_contrast': float(np.exp(.8677)),
        'S15_two_sided_wald_p': float(2*stats.norm.sf(3.369)),
        'S19_1v1_vs_2v1_odds_ratio': float((.1170/(1-.1170))/(.8653/(1-.8653))),
        'S30_vs_S31_example_reciprocal_product': float(8.2638*.1210),
        'note': 'Probabilities, log odds, odds ratios and multiplicity families differ; these conversions do not recover original mixed-model output.'}
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
