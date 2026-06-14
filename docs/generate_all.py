#!/usr/bin/env python3
"""
Central orchestrator for all WS Framework documents.
All generator scripts must follow the same template structure.
"""

import subprocess
import sys
from pathlib import Path

# =============================================================================
# DOCUMENT REGISTRY - Explicit and ordered list
# =============================================================================
DOCUMENTS = [
    # === Core Normative Layer ===
    "generate_ws_vic_001.py",
    "generate_ws_framework_charter.py",

    # === Accreditation ===
    "generate_vas_v87.py",

    # === Monetary Authority ===
    # "generate_vma_strategy_phased_model.py",

    # === Health Authority (VHA) ===
    # "generate_vha_integrity_governance.py",
]

def run_generator(script_name: str) -> bool:
    script_path = Path("docs") / script_name
    if not script_path.exists():
        print(f"⚠️  Skipping (not found): {script_name}")
        return False

    print(f"\n{'='*60}")
    print(f"Generating: {script_name}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ Done: {script_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {script_name}")
        print(e.stdout)
        print(e.stderr)
        return False


def main():
    print("WS Framework Document Generator (Central Orchestrator)")
    print(f"Total documents: {len(DOCUMENTS)}\n")

    success = 0
    for script in DOCUMENTS:
        if run_generator(script):
            success += 1

    print(f"\n{'='*60}")
    print(f"Finished: {success}/{len(DOCUMENTS)} documents generated successfully.")
    print("Output: artifacts/")


if __name__ == "__main__":
    main()