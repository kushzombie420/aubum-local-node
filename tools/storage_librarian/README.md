# Storage Librarian

Current tested baseline for the Aubum storage-management helper.

## Stable components

- `storage_librarian.py` - Phase 1 read-only scanner used by later phases.
- `storage_librarian_v0_3_6.py` - recommendation/planning baseline with real D:/E: routing and failed-download detection.
- `storage_librarian_v0_4b.py` - read-only SHA256 source/destination verification.
- `storage_librarian_v0_4c.py` - missing-destination COPY + SHA256 verify. Requires exact `COPY` approval. Never overwrites and contains no delete operation.
- `storage_librarian_v0_4d.py` - verified archive-source cleanup. Only ARCHIVE TO E items whose destination SHA256 matches can be deleted. Requires exact `DELETE` approval for each source. BACKUP TO D sources are never delete candidates.
- `storage_librarian_v0_4e_3.py` - safe refresh of DIFFERENT existing D:\Aubum Recovery backups. Uses a short D: scratch path and Windows long-path handling. Requires exact `REFRESH` approval. C: sources are never deleted.

## Proven behavior

Live tests completed successfully:

- Matching recovery backups are detected and skipped.
- Different recovery backup is detected.
- Missing E: archive targets are copied and SHA256 verified.
- Existing different destinations are refused by Phase 4C.
- Failed-download stubs such as a 9-byte `Not Found` ZIP are flagged and skipped.
- Archive-source deletion occurs only after exact destination SHA256 match plus explicit per-item `DELETE`.
- Recovery-source deletion is blocked.
- Long nested paths are handled by Phase 4E.3 using a short D: scratch path.
- Existing D: recovery backup refresh was completed and SHA256 verified successfully.

## Safety rules

1. No automatic source deletion.
2. D: recovery sources on C: are never deleted by the Librarian.
3. Archive deletion requires an existing SHA256-identical E: destination and exact `DELETE` approval.
4. Missing-destination copy requires exact `COPY` approval.
5. Existing D: backup refresh requires exact `REFRESH` approval.
6. Phase 4C never overwrites an existing destination.
7. Phase 4E.3 verifies the temporary copy before swapping the existing recovery backup.

## Current status

Functional build complete as of 2026-10-04.

The canonical refresh implementation is `storage_librarian_v0_4e_3.py`. Earlier 4E prototypes were removed from the current tree after failed long-path/syntax tests; their history remains available in Git.
