import json
import hashlib
import glob

def sha256_pair(left_hex: str, right_hex: str) -> str:
    """Berechnet SHA-256 über die Verkettung zweier Hex-Strings."""
    return hashlib.sha256(bytes.fromhex(left_hex + right_hex)).hexdigest()

def verify_merkle_proof(leaf: str, proof: list, index: int, root: str) -> bool:
    """
    Verifiziert einen Merkle-Proof.
    - leaf: Hash des Blattes
    - proof: Liste der Geschwister-Hashes (von unten nach oben)
    - index: Position des Blattes im ursprünglichen Array (0-basiert)
    - root: Erwarteter Root-Hash
    """
    current = leaf
    for sibling in proof:
        if index % 2 == 0:
            current = sha256_pair(current, sibling)
        else:
            current = sha256_pair(sibling, current)
        index //= 2
    return current == root

def verify_chapter(filepath: str) -> tuple[bool, str]:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return False, f"Fehler beim Lesen: {e}"

    root = data.get("merkle_tree", {}).get("root")
    entries = data.get("entries", [])

    if not root:
        return False, "Kein Root-Hash gefunden."
    if not entries:
        return True, "Keine Einträge (leeres Kapitel) – übersprungen."

    all_valid = True
    for entry in entries:
        key = entry.get("key", "")
        try:
            index = int(key.split("_satz")[-1]) - 1
        except (ValueError, IndexError):
            return False, f"Ungültiger Key: {key}"

        leaf = entry.get("value")
        proof = entry.get("proofs", {}).get("merkle", {}).get("proof", [])

        if not verify_merkle_proof(leaf, proof, index, root):
            print(f"  ❌ Ungültiger Proof für {key}")
            all_valid = False

    if all_valid:
        return True, f"✅ Alle {len(entries)} Sätze gültig"
    else:
        return False, f"❌ Fehlerhafte Proofs gefunden"

def main():
    print("🔍 Starte Audit-Verifikation...\n")
    pattern = ".audit/AIO-2511-1.0_chapter*_integrity.json"
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"❌ Keine Dateien gefunden unter: {pattern}")
        return

    all_passed = True
    for filepath in files:
        print(f"📄 {filepath}")
        passed, message = verify_chapter(filepath)
        print(f"   {message}\n")
        if not passed:
            all_passed = False

    if all_passed:
        print("🎉 GESAMTERGEBNIS: ALLE KAPITEL BESTANDEN!")
    else:
        print("❌ GESAMTERGEBNIS: FEHLER BEI MINDESTENS EINEM KAPITEL.")

if __name__ == "__main__":
    main()