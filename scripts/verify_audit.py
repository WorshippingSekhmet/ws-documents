#!/usr/bin/env python3
"""
verify_audit.py – Verify all integrity proof JSONs in the new Merkle-Patricia-Tree schema.

Scans docs/integrity/ for *_integrity.json and checks:
- Structure matches the target schema
- All entry values are valid 64-char hex
- Recomputed Merkle root from all "value" fields matches merkle_tree.root
- Outputs the expected ✅ / ❌ and overall result

Run from ws-documents root:
    python3 scripts/verify_audit.py
"""

import json
import hashlib
import sys
from pathlib import Path

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def compute_merkle_root(leaf_values: list[str]) -> str:
    if not leaf_values:
        return sha256_hex(b"")
    level = [bytes.fromhex(h) for h in leaf_values]
    while len(level) > 1:
        next_level = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            parent = hashlib.sha256(left + right).digest()
            next_level.append(parent)
        level = next_level
    return level[0].hex()

def verify_json_file(json_path: Path) -> tuple[bool, str, int]:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Failed to load/parse JSON: {e}", 0

    # Check required top-level keys for new schema
    required = ["document_id", "chapter", "merkle_tree", "entries"]
    missing = [k for k in required if k not in data]
    if missing:
        return False, f"Missing top-level keys: {missing}", 0

    merkle_info = data.get("merkle_tree", {})
    if not isinstance(merkle_info, dict) or "root" not in merkle_info:
        return False, "merkle_tree.root missing or invalid", 0

    entries = data.get("entries", [])
    if not isinstance(entries, list):
        return False, "'entries' must be a list", 0

    if len(entries) == 0:
        return True, "No entries (empty chapter) – considered valid", 0

    values = []
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            return False, f"Entry {idx} is not an object", 0
        val = entry.get("value", "")
        if not isinstance(val, str) or len(val) != 64 or not all(c in "0123456789abcdefABCDEF" for c in val):
            return False, f"Invalid 'value' hash in entry {idx} (key={entry.get('key', '?')})", 0
        values.append(val.lower())

    try:
        recomputed = compute_merkle_root(values)
    except Exception as e:
        return False, f"Error computing Merkle root: {e}", len(values)

    stored_root = merkle_info.get("root", "").lower()
    if recomputed != stored_root:
        return False, f"Merkle root mismatch!\n  Stored:   {stored_root}\n  Computed: {recomputed}", len(values)

    return True, "OK", len(values)

def main():
    integrity_dir = Path("docs/integrity")
    if not integrity_dir.exists():
        print(f"❌ Directory {integrity_dir} not found. Run from ws-documents root.")
        sys.exit(1)

    json_files = sorted(integrity_dir.glob("*_integrity.json"))
    if not json_files:
        json_files = sorted(integrity_dir.glob("*.json"))

    if not json_files:
        print("⚠️ No integrity JSON files found.")
        sys.exit(0)

    print("🔍 Starting Audit Verification (Merkle-Patricia-Tree schema)...\n")

    all_passed = True
    total_chapters = 0
    total_entries = 0

    for jf in json_files:
        total_chapters += 1
        print(f"📄 {jf}")
        success, msg, num = verify_json_file(jf)
        total_entries += num
        if success:
            print(f"   ✅ All {num} entries valid (root matches)")
        else:
            print(f"   ❌ FAILED: {msg}")
            all_passed = False
        print()

    print("─" * 60)
    if all_passed:
        print(f"🎉 OVERALL RESULT: ALL CHAPTERS PASSED! ({total_chapters} chapters, {total_entries} entries verified)")
        sys.exit(0)
    else:
        print(f"💥 OVERALL RESULT: SOME CHAPTERS FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()