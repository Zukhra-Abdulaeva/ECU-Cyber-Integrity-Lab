# EV-P4-VER

Create the corresponding Evidence Record, then validate and associate that record with the test execution, observation, and result.

The JSON field types and enum representations match the supplied `a_framework/evidence.py` model.

Artifact SHA-256: `be5c7c2a77651d7dbb2df36d92841b653019bc5a0572bffa08bd3c43016c9b08`
Artifact size: `2598` bytes
https://openfiletools.com/tools
https://openfiletools.com/guides/how-to-verify-a-file-checksum


Important:
- Record lifecycle remains `CREATED`.
- Associations are represented as references, but they have not yet been validated or transitioned through the repository lifecycle.
- `timestamp` remains null because the supplied terminal output does not contain an execution timestamp.
- The local EvidenceValidator has not been executed by this package. Run it from the repository checkout after copying the files into the paths shown.
- Confirm the repository's actual evidence root before copying; the supplied code's default is `c_evidence/records`.

Test Execution:
Command: source .venv/bin/activate
Command: pip install --upgrade python-can
Command: python -m pytest -q a_framework/test_evidence.py
Command: python -m pytest -q
Execution context: LOCAL

Test Verification: 
mkdir -p c_evidence/verification
python -m pytest -q a_framework/test_evidence.py \ 2>&1 | tee c_evidence/verification/EV-P4-VER-001_test_execution.txt
sha256sum c_evidence/verification/EV-P4-VER-001_test_execution.txt