"""Conservative, evidence-only PRAI applicability routing.

This classifier does not override a mandatory PRAI requirement or grant transition,
merge, deployment, production, or release authority. It is a proposal for
separate protected governance adoption, not an active gate replacement.
"""

from __future__ import annotations

from dataclasses import dataclass

from .prai import ALLOWED_RISK_CHARACTERISTICS, DEEP_RISK_CHARACTERISTICS


DISPOSITIONS = ("SKIP", "ADVISORY", "REQUIRED")
GATE_STATES = ("MANDATORY", "OPTIONAL", "UNKNOWN")
IMPACTS = ("NONE", "LOW", "MEDIUM", "HIGH", "CRITICAL")
ACTIONS = ("TASK", "MERGE", "RELEASE", "PRODUCTION", "POLICY_CHANGE", "SECURITY_EXCEPTION")
REQUIRED_RISKS = frozenset(DEEP_RISK_CHARACTERISTICS).union(
    {
        "LEGAL", "PRIVACY", "COMPLIANCE", "IP", "POLICY",
        "PERSISTENCE", "TRANSACTION", "DURABILITY", "DATA_OWNERSHIP",
        "SCOPE_EXPANSION",
    }
)
PROTECTED_PATH_PREFIXES = (
    ".github/workflows/",
    "docs/architecture/",
    "docs/governance/",
    "docs/releases/",
    "machine/",
    "scripts/validation/",
    "orchestra_runtime/domain/adaptive/prai",
)
PROTECTED_PATH_EXACT = frozenset(
    {"AGENTS.md", "plugin.json", "PROJECT_STATE.md", "PROJECT_CONTEXT.md"}
)


@dataclass(frozen=True, slots=True)
class PraiApplicabilityDecision:
    disposition: str
    reasons: tuple[str, ...]
    may_continue_without_prai: bool
    authority_granted: bool = False


def evaluate_prai_applicability(
    *,
    changed_paths: tuple[str, ...],
    logical_impact: str,
    security_impact: str,
    risk_characteristics: tuple[str, ...],
    phase: str,
    action: str,
    existing_prai_gate: str,
) -> PraiApplicabilityDecision:
    """Classify only post-run PRAI applicability, never overall transition readiness.

    An upstream reviewer must explicitly verify the current active gate. UNKNOWN
    fails closed; evidence missing for other mandatory controls is never a skip.
    """
    if not isinstance(changed_paths, tuple) or not isinstance(risk_characteristics, tuple):
        raise TypeError("changed_paths and risk_characteristics must be tuples")
    if not isinstance(logical_impact, str) or not isinstance(security_impact, str):
        raise TypeError("impact classifications must be strings")
    if not isinstance(phase, str) or not isinstance(action, str) or not isinstance(existing_prai_gate, str):
        raise TypeError("phase, action and gate classifications must be strings")

    unknown_path = not changed_paths or any(
        not isinstance(path, str)
        or not path
        or path.startswith(("/", "\\"))
        or "\\" in path
        or any(part in ("", ".", "..") for part in path.split("/"))
        for path in changed_paths
    )
    unknown_risks = any(
        not isinstance(risk, str) or risk not in ALLOWED_RISK_CHARACTERISTICS
        for risk in risk_characteristics
    )
    invalid_classification = (
        logical_impact not in IMPACTS
        or security_impact not in IMPACTS
        or existing_prai_gate not in GATE_STATES
        or action not in ACTIONS
        or not phase
        or unknown_path
        or unknown_risks
    )
    if invalid_classification or existing_prai_gate == "UNKNOWN":
        return PraiApplicabilityDecision("REQUIRED", ("UNKNOWN_OR_UNVERIFIED_POLICY_OR_RISK",), False)
    if existing_prai_gate == "MANDATORY":
        return PraiApplicabilityDecision("REQUIRED", ("EXISTING_MANDATORY_GATE",), False)
    if action != "TASK" or phase != "GENERAL":
        return PraiApplicabilityDecision("REQUIRED", ("PROTECTED_ACTION_OR_PHASE",), False)
    if logical_impact in ("HIGH", "CRITICAL") or security_impact in ("MEDIUM", "HIGH", "CRITICAL"):
        return PraiApplicabilityDecision("REQUIRED", ("MATERIAL_LOGICAL_OR_SECURITY_IMPACT",), False)
    if REQUIRED_RISKS.intersection(risk_characteristics):
        return PraiApplicabilityDecision("REQUIRED", ("PROTECTED_RISK_CHARACTERISTIC",), False)
    if any(
        path in PROTECTED_PATH_EXACT or path.startswith(PROTECTED_PATH_PREFIXES)
        for path in changed_paths
    ):
        return PraiApplicabilityDecision("REQUIRED", ("PROTECTED_SOURCE_PATH",), False)

    harmless_reference_docs = (
        logical_impact in ("NONE", "LOW")
        and security_impact == "NONE"
        and not risk_characteristics
        and all(path.startswith("docs/reference/") and path.endswith(".md") for path in changed_paths)
    )
    if harmless_reference_docs:
        return PraiApplicabilityDecision("SKIP", ("HARMLESS_REFERENCE_DOCUMENTATION",), True)
    return PraiApplicabilityDecision("ADVISORY", ("BOUNDED_NONPROTECTED_WORK",), True)
