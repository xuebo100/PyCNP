"""Find header files in a directory (cross-platform)."""

import glob
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("")
    sys.exit(0)

search_dir = Path(sys.argv[1])
if not search_dir.exists():
    print("")
    sys.exit(0)

# Use forward slashes for consistency (works on all platforms)
headers = glob.glob(str(search_dir / "**" / "*.h"), recursive=True)
# Convert to forward slashes for meson compatibility
headers = [h.replace("\\", "/") for h in headers]
print(" ".join(headers))
