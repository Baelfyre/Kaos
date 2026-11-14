"""Negative and applicability fixtures for the proposed PRAI routing classifier."""

from __future__ import annotations

import pytest

from orchestra_runtime.domain.adaptive.prai_applicability import evaluate_prai_applicability


DEFAULTS = {
    "changed_paths": ("docs/reference/formatting.md",),
    "logical_impact": "NONE",
    "security_impact": "NONE",
    "risk_characteristics": (),
    "phase": "GENERAL",
    "action": "TASK",
    "existing_prai_gate": "OPTIONAL",
}


def classify(**overrides):
    return evaluate_prai_applicability(**(DEFAULTS | overrides))


def test_harmless_reference_documentation_can_skip():
    result = classify()
    assert result.disposition == "SKIP"
    assert result.reasons == ("HARMLESS_REFERENCE_DOCUMENTATION",)
    assert not result.authority_granted


@pytest.mark.parametrize(
    "changes",
    [
        ("docs/reference/formatting.md", "docs/reference/naming.md"),
        ("docs/reference/deep/naming.md",),
    ],
)
def test_reference_documentation_only_is_allowed_to_skip(changes):
    assert classify(changed_paths=changes).disposition == "SKIP"


@pytest.mark.parametrize(
    "changes",
    [
        ("docs/governance/PROTECTED_GOVERNANCE_ESCALATION_PROTOCOL.md",),
        ("machine/adaptive/prai-post-run-assurance.v1.json",),
        ("orchestra_runtime/domain/adaptive/prai.py",),
        ("scripts/validation/validate_prai.py",),
        ("AGENTS.md",),
        (".github/workflows/prai.yml",),
        ("PROJECT_STATE.md",),
        ("SECURITY.md",),
        ("ROUTING_MAP.md",),
        ("scripts/governance_check.py",),
        ("scripts/dagger_guardrail.py",),
        ("scripts/validate_governance_protocol_consistency.py",),
        ("orchestra_runtime/domain/adaptive/gate_coverage.py",),
        ("orchestra_runtime/domain/adaptive/high_risk_assurance.py",),
        (".claude-plugin/plugin.json",),
        (".codex-plugin/plugin.json",),
        (".antigravity-plugin/plugin.json",),
        ("adapters/codex/README.md",),
        ("DOCS/GOVERNANCE/PROTECTED_GOVERNANCE_ESCALATION_PROTOCOL.md",),
        ("SECURITY.MD",),
    ],
)
def test_protected_source_always_requires_prai(changes):
    assert classify(changed_paths=changes).disposition == "REQUIRED"


@pytest.mark.parametrize("phase", ["AQ6", "AQ7", "AQ8", "RELEASE", "UNKNOWN"])
def test_phase_is_not_a_skip(phase):
    assert classify(phase=phase).disposition == "REQUIRED"


@pytest.mark.parametrize("action", ["MERGE", "RELEASE", "PRODUCTION", "POLICY_CHANGE", "SECURITY_EXCEPTION"])
def test_protected_actions_must_not_skip(action):
    assert classify(action=action).disposition == "REQUIRED"


@pytest.mark.parametrize("gate", ["MANDATORY", "UNKNOWN", "INVALID"])
def test_active_or_unknown_mandatory_requirement_fails_closed(gate):
    result = classify(existing_prai_gate=gate)
    assert result.disposition == "REQUIRED"


@pytest.mark.parametrize(
    "risks",
    [
        ("AUTHENTICATION",),
        ("AUTHORIZATION",),
        ("PRIVACY",),
        ("CONCURRENCY",),
        ("STATE_MACHINE",),
        ("IP",),
        ("POLICY",),
        ("DATA_OWNERSHIP",),
        ("SENSITIVE_PROVENANCE",),
        ("NOT_A_VALID_RISK",),
    ],
)
def test_sensitive_or_unrecognized_risks_are_required(risks):
    assert classify(risk_characteristics=risks).disposition == "REQUIRED"


@pytest.mark.parametrize("impact", ["MEDIUM", "HIGH", "CRITICAL", "UNKNOWN"])
def test_security_impact_is_required(impact):
    assert classify(security_impact=impact).disposition == "REQUIRED"


@pytest.mark.parametrize("impact", ["HIGH", "CRITICAL", "UNKNOWN"])
def test_high_or_unknown_logical_impact_is_required(impact):
    assert classify(logical_impact=impact).disposition == "REQUIRED"


@pytest.mark.parametrize(
    "changes",
    [
        (),
        ("/absolute/path.md",),
        ("../docs/reference/something.md",),
        ("docs//reference/a.md",),
        ("docs/reference/../governance/x.md",),
        (r"docs\\reference\\x.md",),
        ("docs/reference/x.md", "machine/policy.json"),
        ("C:docs/reference/x.md",),
        ("docs/reference/file:name.md",),
    ],
)
def test_ambiguous_path_or_mixed_protected_paths_never_skip(changes):
    assert classify(changed_paths=changes).disposition == "REQUIRED"


def test_bounded_code_work_is_advisory_not_mandatory_by_default():
    result = classify(
        changed_paths=("tests/runtime/test_task_profile.py",),
        logical_impact="MEDIUM",
        security_impact="LOW",
        risk_characteristics=("UI",),
    )
    assert result.disposition == "ADVISORY"
    assert not result.authority_granted


def test_documentation_outside_narrow_allowlist_is_advisory():
    result = classify(changed_paths=("docs/setup/how-to.md",))
    assert result.disposition == "ADVISORY"


def test_skip_does_not_authorize_a_transition():
    for changes in (("docs/reference/formatting.md",), ("docs/setup/how-to.md",)):
        assert not classify(changed_paths=changes).authority_granted


def test_missing_declarations_fail_closed():
    with pytest.raises(TypeError):
        classify(changed_paths=["docs/reference/formatting.md"])
    with pytest.raises(TypeError):
        classify(risk_characteristics=["UI"])
