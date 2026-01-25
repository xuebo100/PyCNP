"""Extract version from pyproject.toml."""

import re
from pathlib import Path

pyproject = Path(__file__).parent.parent / "pyproject.toml"
match = re.search(r'version\s*=\s*"([^"]+)"', pyproject.read_text())
if match:
    print(match.group(1))
else:
    print("0.0.0")
