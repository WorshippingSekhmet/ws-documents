# ws-documents

Zentrale Sammlung kryptographischer **Integritäts-Proofs** für Audit-Berichte der AIO-Serie.

## Integrity Proofs

Hier werden für jeden Audit-Bericht die Integritäts-Proofs (Merkle-Patricia-Tree Schema) hinterlegt. 
Zukünftige Berichte können einfach ergänzt werden, ohne das Haupt-README zu überladen.

### Verfügbare Berichte

| Bericht       | Link                                      | Status      | Beschreibung                     |
|---------------|-------------------------------------------|-------------|----------------------------------|
| AIO-2506-1.0 | [ws-documents/](ws-documents/)           | Templates   | Aktueller Bericht (8 Kapitel)   |
| AIO-2511-1.0 | [ws-documents/](ws-documents/)           | Referenz    | Referenz-Implementierung        |

> **Hinweis:** Die detaillierte Struktur, Skripte und Proof-JSONs befinden sich im Unterordner `ws-documents/`.

## Struktur des Repositories

```
ws-documents/
├── README.md                     ← Detaillierte Projektbeschreibung
├── GOVERNANCE.md
├── docs/
│   ├── integrity/               ← JSON-Proofs pro Kapitel
│   └── operations/
├── scripts/
│   ├── build_integrity.py
│   └── verify_audit.py
└── ...
```

## Nächste Schritte

- Weitere AIO-Berichte werden hier ergänzt
- Echte Satz-Texte/Hashes für AIO-2506-1.0 einspielen
- Bei Bedarf individuelle Merkle-Proofs pro Satz erweitern

Siehe [ws-documents/README.md](ws-documents/README.md) für die vollständige technische Dokumentation und den Workflow.