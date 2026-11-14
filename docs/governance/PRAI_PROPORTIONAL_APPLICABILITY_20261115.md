# PRAI Proportional Applicability Proposal

**Status:** proposed protected governance amendment; **not yet active**.

**Owner direction (November 15, 2026):** retain PRAI within full autonomous work when useful and applicable. Avoid repeatedly blocking routine work on nonessential assurance. Continue providing concise verified progress, risks, and decisions for owner oversight.

## Scope

This proposal introduces a conservative **pre-PRAI routing decision**. It does not change the independent PRAI validator, qualified-receipt criteria, required CI, security tests, Arbiter authority, or protected merge/release approvals. A routing decision cannot convert PRAI BLOCKED into PRAI PASS or grant authority.

The separate, deterministic prototype lives in `orchestra_runtime/domain/adaptive/prai_applicability.py`; its cases live in `tests/runtime/test_prai_applicability.py`. It requires upstream Conductor to read the *effective* policy and explicitly classify the existing PRAI gate. No speculative default to OPTIONAL is permitted.

## Routing outcomes

| Result | Allowed use | Effect |
| --- | --- | --- |
| `SKIP` | Isolated Markdown in `docs/reference/` with no declared security, logical, or other risk; no protected action/phase; effective PRAI gate verified OPTIONAL | Record `HARMLESS_REFERENCE_DOCUMENTATION`. Run applicable documentation/structure tests. Do not invent a PRAI review or PASS. |
| `ADVISORY` | Bounded nonprotected work, an explicitly OPTIONAL PRAI gate, no material security or protected risk trigger | Request a focused review when useful. A timeout or missing optional review may be recorded and work may continue **only if** other applicable controls are satisfied. No independent-review claim is inferred. |
| `REQUIRED` | Mandatory or unverifiable existing gate; protected phase/action or source path; security, data, policy, legal, or high-impact risk | Run existing independent PRAI and preserve fail-closed status. If unavailable or BLOCKED, escalate; never silently downgrade. |

Unknown paths, unknown risk characteristics, missing source changes, noncanonical classifications, and an unread/unknown effective policy yield `REQUIRED`. Impact triggers and protected paths are enumerated in the prototype and tested.

## Required protected boundaries

- Existing AQ6 and AQ8 PRAI requirements, protected assurance campaigns and release rules remain unchanged **until a separate approved policy revision**. The prototype deliberately returns REQUIRED for all nongeneral phases and protected actions.
- No same-run modification to the policy/validator that blocked the original candidate.
- The full autonomous profile never grants independent policy exception, security bypass, whitelist edit, merge or release rights.
- A failed mandatory PRAI review remains a blocker. A failed *optional* advisory may be recorded as such only after verifying the task is not covered by a mandatory gate.
- Reviewer identity and source-bound evidence are not manufactured from model names or green CI.

## Bounded autonomous workflow after independent adoption

1. Observe active repository state, exact head, active policy, changed paths, impact and protected operations.
2. Evaluate the proposed risk classifier using verified input, preserving outcome, reason code, exact candidate and policy reference.
3. Run only applicable assurance and existing required tests/CI/security checks.
4. For optional review timeouts, stop redundant retries and record INCONCLUSIVE/UNAVAILABLE; do not use those outputs as qualified PRAI evidence.
5. Route transitions through existing Arbiter and applicable owner approval boundaries.
6. Provide the owner a short status covering completion, evidence, residual risks and next protected decision.

## Current release treatment

PR #1009 at `b770a58fef3898feb6437500423d512a51baf116` is a separate blocked release candidate. This new branch does **not** waive that failure, retroactively authorize the release, or alter its source. To consider a release-specific exception or a policy change with wider reach, perform a separately authorized human-governance decision and an independent readback before requalification.

## Qualification and activation

A dedicated branch and independent review must validate the change and relevant negative tests. Integration into host routing requires a separate approved change and checks showing the classifier cannot bypass a required gate. This document and prototype are evidence for human assessment only until merged and formally adopted through the protected governance process.
