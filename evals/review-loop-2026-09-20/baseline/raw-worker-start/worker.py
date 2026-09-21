import json
import os
import sys
from policy import normalize_text


def main():
    request = json.load(sys.stdin)
    try:
        result = {"value": normalize_text(request["text"])}
    except ValueError as exc:
        result = {"error": str(exc)}
    # Names only: integration diagnostics never expose environment values.
    result["environment_names"] = sorted(os.environ)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
