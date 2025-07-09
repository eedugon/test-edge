#!/usr/bin/env python3
"""
Generate a single change fragment in .release/outgoing/
Filename format: YYYY-MM-DD_<type>_<service>_pr<PR>.yaml
"""

import os
import re
import yaml
from datetime import date
from pathlib import Path

# --------------------------------------------------------------------------- #
# 1. Gather inputs (env vars or hard-coded defaults for local testing)
# --------------------------------------------------------------------------- #

SERVICE   = os.getenv("SERVICE",   "microservice1")
TYPE      = os.getenv("TYPE",      "enhancement").lower()          # enhancement | fix | ...
SUMMARY   = os.getenv("SUMMARY",   "Improve login flow for SSO users")
PR_URL    = os.getenv("PR_URL",    "https://github.com/eedugon/test-edge/pull/12345")
AUTHOR    = os.getenv("AUTHOR",    "@userdefault")
PRODUCTS  = os.getenv("PRODUCTS",  "cloud-hosted").split(",")

# --------------------------------------------------------------------------- #
# 2. Extract PR number (mandatory int) from the URL or string
# --------------------------------------------------------------------------- #

pr_match = re.search(r"(?:/pull/|^)(\\d+)$", PR_URL.strip())
if not pr_match:
    raise SystemExit(f"[ERROR] Cannot extract PR number from '{PR_URL}'")
PR_NUMBER = int(pr_match.group(1))

# --------------------------------------------------------------------------- #
# 3. Build YAML payload (mandatory + optional fields)
# --------------------------------------------------------------------------- #

release_note = {
    "date": date.today().isoformat(),     # mandatory
    "type": TYPE,                         # mandatory
    "service": SERVICE,                   # mandatory
    "pr": PR_NUMBER,                      # mandatory (int!)
    "summary": SUMMARY,                   # mandatory (was 'description')
    "products": PRODUCTS,                 # optional (extra metadata)
    "author": AUTHOR,                     # optional
    "issues": [],                         # optional
    # "highlight": {                      # fully optional
    #     "title": "...",
    #     "body": "..."
    # }
}

# --------------------------------------------------------------------------- #
# 4. Compose filename: YYYY-MM-DD_<type>_<service>_pr<PR>.yaml
#    e.g. 2025-07-09-enhancement-microservice1-pr12345.yaml
# --------------------------------------------------------------------------- #

filename = f"{release_note['date']}_{TYPE}_{SERVICE}_pr{PR_NUMBER}.yaml"
out_dir  = Path(".release/outgoing")
out_dir.mkdir(parents=True, exist_ok=True)
file_path = out_dir / filename

# --------------------------------------------------------------------------- #
# 5. Write the YAML fragment
# --------------------------------------------------------------------------- #

with file_path.open("w", encoding="utf-8") as f:
    # use default_flow_style=False for multi-line readability
    yaml.safe_dump(release_note, f, sort_keys=False)

print(f"[OK] Release note written to {file_path.relative_to(Path.cwd())}")