import importlib
import json
from pathlib import Path


def run_registered(value):
    spec = json.loads((Path(__file__).parent / "deployment" / "registry.json").read_text())
    module = importlib.import_module(spec["module"])
    handler = getattr(module, "_".join(spec["symbol_parts"]))
    return handler(value)
