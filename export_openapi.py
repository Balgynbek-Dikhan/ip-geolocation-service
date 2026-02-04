import json
from pathlib import Path

import yaml

from app.main import app


def main() -> None:
    output_path = Path("openapi/openapi.yaml")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    spec = app.openapi()
    output_path.write_text(yaml.safe_dump(spec, sort_keys=False), encoding="utf-8")

    json_path = Path("openapi/openapi.json")
    json_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
