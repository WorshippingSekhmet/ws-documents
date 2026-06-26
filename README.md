# ws-documents – Audit Integrity Proofs Repository

This repository maintains tamper-evident integrity proofs for audit reports using per-sentence SHA-256 hashing and Merkle tree-based proofs.

## Purpose

To provide cryptographic proof that the content of audit reports (specifically chapters/sections) has not been altered since the proofs were generated. This is critical for:

- Regulatory compliance and auditability
- Demonstrating document integrity over time
- Enabling third-party verification without revealing full content (if proofs are shared selectively)
- Chain of custody for AI-generated or sensitive operational documents (e.g., Valkyrie guides)

## Structure

```
ws-documents/
├── docs/
│   ├── integrity/                    # JSON Merkle proofs per chapter
│   │   ├── AIO-2506-1.0_chapter1_integrity.json
│   │   │   ...
│   └── operations/                   # Human-readable operational docs
│       └── operational-valkyrie-guide-AIO-2506-1.0.md
├── scripts/
│   ├── verify_audit.py               # Verification script (document-ID agnostic)
│   └── build_integrity.py            # Builder for generating JSON proofs from sentence hashes
├── README.md
├── GOVERNANCE.md
└── LICENSE
```

## Supported Documents

- **AIO-2511-1.0** (reference implementation)
- **AIO-2506-1.0** (current target – proofs to be added)

## Workflow

1. Prepare sentence hashes for each chapter (exact text → SHA-256).
2. Use `build_integrity.py` or the HTML Merkle calculator to generate proofs.
3. Store JSONs in `docs/integrity/`.
4. Run `python3 scripts/verify_audit.py` to validate all proofs.
5. Commit and push for immutable record.

## Verification

```bash
python3 scripts/verify_audit.py
```

Expected: All chapters report ✅ valid sentences and overall success.

## Security Notes

- Uses SHA-256 (collision resistant for this purpose).
- Merkle trees allow efficient inclusion proofs and root verification.
- Any change to even one character in a sentence invalidates its proof and the chapter root.
- Timestamps in JSONs are UTC; roots are deterministic from content.

## Contributing / Updating Proofs

When a report is updated:
- Recompute hashes for changed chapters only.
- Regenerate affected JSONs.
- Update `created` timestamp.
- Re-verify and commit with clear message.

## License

See LICENSE file.

## Contact / Governance

See GOVERNANCE.md for roles, approval process for new proofs, and retention policy.