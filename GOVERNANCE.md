# GOVERNANCE.md – Integrity Proofs for Audit Documents

## Scope
This document governs the creation, maintenance, and verification of cryptographic integrity proofs for audit reports in the ws-documents repository (e.g. AIO-*-1.0 series).

## Roles & Responsibilities

| Role | Responsibilities |
|------|------------------|
| **Audit Author / Owner** | Provides raw chapter texts or pre-computed sentence hashes; approves final proofs before commit |
| **Integrity Engineer** | Runs build scripts, validates Merkle proofs, maintains scripts and structure |
| **Reviewer / Approver** | Independent review of proof generation process and verification logs |
| **Repository Maintainer** | Manages Git history, branch protection, release tags for proof sets |

## Process for Adding/Updating Proofs (AIO-2506-1.0 example)

1. **Content Freeze**: Chapter texts are finalized and versioned (no further edits without new proof cycle).
2. **Sentence Extraction**: Define clear rules for splitting into "Sätze" (sentences). Recommended: split on sentence-ending punctuation while preserving context (use NLP-aware splitter if available, or manual review for German abbreviations like "z. B.", "etc.").
3. **Hash Computation**: SHA-256 over exact UTF-8 bytes of each sentence string (no extra normalization beyond what is in the source document; preserve whitespace, line breaks if present in original).
4. **Proof Generation**: Use `build_integrity.py` (preferred for batch) or merkle.html. Set `document_id`, `chapter`, `created` (current UTC ISO8601), adjust `key` fields to `AIO-2506-1.0_<chapter-id>_satzN`.
5. **Storage**: Save as `docs/integrity/AIO-2506-1.0_chapterX_integrity.json`.
6. **Verification**: Run `scripts/verify_audit.py`. All must pass.
7. **Documentation**: Update operational guide if procedures changed. Add entry to this GOVERNANCE if process evolves.
8. **Commit**: Use conventional commit `feat: Add/update integrity proofs for AIO-2506-1.0 chapters X,Y`. Include verification output in PR description.
9. **Approval**: At least one reviewer signs off before merge to main.

## Edge Cases & Policies

- **Minor text edits** (typos, formatting): Require full re-proof of affected chapter. No "patch" proofs.
- **New chapters added**: Create new JSON; update any index if exists.
- **Chapter removal**: Archive old JSON (do not delete from Git history); note in README.
- **Large chapters** (>500 sentences): Consider performance; Merkle tree depth is log2(N), still efficient. Split into sub-chapters if needed for usability.
- **Unicode / Special chars**: Fully supported (Python `hashlib.sha256` handles UTF-8).
- **Empty chapters**: Allowed but discouraged; JSON with `num_sentences: 0`, empty `sentences` array, root = hash of empty or special marker.
- **Reproducibility**: Proofs must be reproducible from the exact source text. Store source texts alongside if possible (or reference to immutable location).
- **Retention**: Proof JSONs are kept indefinitely in Git. Do not force-push or rewrite history.
- **Export / External Verification**: JSON format is self-contained; third parties can implement verifier using the same Merkle algorithm.

## Algorithm Specification (for implementers)

- Leaf: `sha256( sentence_text.encode('utf-8') )`
- Internal node: `sha256( left_child + right_child )` (concatenation of 32-byte digests)
- For odd number of nodes at a level: duplicate the last leaf/hash (common Merkle practice for balanced tree).
- Proof for a leaf: ordered list of sibling hashes + direction (left/right) or implicit by position in path.
- Verification: iteratively hash leaf with proof siblings in correct order/direction until root.

See `scripts/build_integrity.py` and `verify_audit.py` for canonical implementation.

## Change Log

- Initial setup for AIO-2506-1.0 mirroring AIO-2511-1.0 (2026-06-26)
- ...

## Approval

This governance is approved by the Integrity Working Group. Changes require consensus or documented exception.