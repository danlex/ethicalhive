#!/usr/bin/env python3
"""Compatibility entry point: research content now lives in the main catalogue."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/'check-unified-catalogue.py'), run_name='__main__')
