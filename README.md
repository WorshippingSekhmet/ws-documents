# ws-documents

Zentrale Sammlung kryptographischer **Integritäts-Proofs** für Audit-Berichte (AIO-Serie).

## Integrity Proofs

Hier sind die kryptographischen Integritäts-Proofs (Merkle-Patricia-Tree) für die einzelnen Audit-Berichte hinterlegt.

### Verfügbare Berichte

| Bericht        | Link zu den Proofs                          | Kapitel | Status     |
|----------------|---------------------------------------------|---------|------------|
| **AIO-2506-1.0** | [docs/integrity/](docs/integrity/)         | 8       | Templates  |
| AIO-2511-1.0     | Referenz-Implementierung                    | -       | Referenz   |

**AIO-2506-1.0 Kapitel-Proofs:**
- [1. Audit Titel](docs/integrity/AIO-2506-1.0_chapter1_integrity.json)
- [2. Einleitung](docs/integrity/AIO-2506-1.0_chapter2_integrity.json)
- [3. Umfang des Audits](docs/integrity/AIO-2506-1.0_chapter3_integrity.json)
- [4. Executive Summary](docs/integrity/AIO-2506-1.0_chapter4_integrity.json)
- [5. Beurteilung der Lage](docs/integrity/AIO-2506-1.0_chapter5_integrity.json)
- [5.1 Destabilisierung des Ordnungssystems](docs/integrity/AIO-2506-1.0_chapter5_1_integrity.json)
- [5.2 Integrität von CMD und CTRL](docs/integrity/AIO-2506-1.0_chapter5_2_integrity.json)
- [5.3 Strategisches gegenseitiges Vertrauen (SMT)](docs/integrity/AIO-2506-1.0_chapter5_3_integrity.json)

> Weitere AIO-Berichte werden hier sukzessive ergänzt.

## Repository-Struktur

```
docs/integrity/          # Alle JSON-Proofs (pro Kapitel)
scripts/
  ├── build_integrity.py   # JSONs aus Hashes/Texten erzeugen
  └── verify_audit.py    # Alle Proofs validieren
GOVERNANCE.md
README.md                # Diese Datei (Index)
```

## Verwendung

1. `python3 scripts/verify_audit.py` – Alle Proofs prüfen
2. Bei neuen Daten: `python3 scripts/build_integrity.py` nutzen
3. Commit & Push

Die detaillierte technische Dokumentation und der Workflow befinden sich in dieser README (siehe oben).