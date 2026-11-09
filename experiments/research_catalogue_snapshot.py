#!/usr/bin/env python3
"""Inspect the immutable catalogue release used by the historical resource study."""
import hashlib
import json
from pathlib import Path
import subprocess

import yaml

ROOT = Path(__file__).resolve().parents[1]
STUDY_COMMIT = '8798134'


def snapshot():
    commit = subprocess.check_output(['git','rev-parse',STUDY_COMMIT+'^{commit}'],cwd=ROOT,text=True).strip()
    source = subprocess.check_output(['git','show',commit+':ontology/ethical-ai.yaml'],cwd=ROOT)
    ontology = yaml.safe_load(source)
    modes = ontology['modes']
    return {
        'commit':commit,
        'url':f'https://github.com/danlex/ethicalhive/blob/{commit}/ontology/ethical-ai.yaml',
        'sha256':hashlib.sha256(source).hexdigest(),
        'version':ontology['meta']['version'],
        'records':len(modes),
        'categories':len({m['category'] for m in modes}),
        'ai_native':sum(bool(m.get('ai_native')) for m in modes),
        'human_parallel':sum(bool(m.get('human_parallel')) for m in modes),
        'worked_example_audit_eligible':sum(len(m.get('examples') or [])>=3 for m in modes),
        'eligibility_rule':'The historical verify-sample.py selects records with at least three examples; eligibility alone does not establish source support.',
    }


if __name__=='__main__':
    print(json.dumps(snapshot(),indent=2))
