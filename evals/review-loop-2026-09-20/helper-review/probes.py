"""Replay the corrected fsmonitor regression using the shared disposable probe."""
from pathlib import Path
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('verify_round2.py')), run_name='__main__')
