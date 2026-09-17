from __future__ import annotations

import re
from dataclasses import dataclass

from .models import EvidenceItem
from .official_refs import match_official_references

COMPONENT_PATTERNS = {
    "vpxd": ("vCenter orchestration", r"\bvpxd\b"),
    "hostd": ("ESXi host management", r"\bhostd\b"),
    "vmkernel": ("ESXi kernel/storage/network", r"\bvmkernel\b"),
    "vobd": ("VMware observation events", r"\bvobd\b"),
    "vmafdd": ("authentication framework", r"\bvmafdd\b"),
    "vmdird": ("directory service", r"\bvmdird\b"),
    "applmgmt": ("VCSA appliance management", r"\bapplmgmt\b"),
    "SSO": ("single sign-on", r"\bSSO\b|single sign-on"),
    "Lookup Service": ("service registration", r"lookup\s+service"),
    "vLCM": ("lifecycle management", r"\bvLCM\b|lifecycle manager"),
    "EAM": ("ESX Agent Manager", r"\bEAM\b|esx agent manager"),
    "WCP": ("workload control plane", r"\bWCP\b|workload control plane"),
    "VAPI": ("vSphere API endpoint", r"\bVAPI\b|vapi-endpoint"),
}

ERROR_PATTERN = re.compile(r"\b(error|failed|failure|exception|timeout|unavailable|corrupt)\b", re.I)


@dataclass
class Findings:
    evidence: list[EvidenceItem]
    components: list[str]


def inspect(text: str) -> Findings:
    evidence: list[EvidenceItem] = []
    components: list[str] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        matched = []
        for component, (_, pattern) in COMPONENT_PATTERNS.items():
            if re.search(pattern, line, re.I):
                matched.append(component)
                if component not in components:
                    components.append(component)
        if matched or ERROR_PATTERN.search(line):
            observation = line.strip()[:500]
            if observation:
                evidence.append(EvidenceItem(id=f"E{len(evidence)+1}", source="submitted input", line=line_number, observation=observation))
        if len(evidence) >= 25:
            break
    if not evidence:
        evidence.append(EvidenceItem(id="E1", source="submitted input", observation="No recognized VMware component or explicit error pattern was found."))
    return Findings(evidence, components)


def _evidence_lines(findings: Findings) -> str:
    return "\n".join(f"- [{item.id}] line {item.line or 'n/a'}: {item.observation}" for item in findings.evidence[:8])


def render(workflow: str, text: str, product: str | None, version: str | None, external_action_approved: bool = False) -> tuple[str, Findings, str, list[str]]:
    findings = inspect(text)
    has_error = any(ERROR_PATTERN.search(item.observation) for item in findings.evidence)
    confidence = "medium" if has_error and findings.components else "low"
    missing = []
    if not product:
        missing.append("Exact product/build")
    if not version:
        missing.append("Version and patch level")
    missing.extend(["Issue timeline and impact", "Correlated logs from the same timestamp"])
    components = ", ".join(findings.components) or "not yet identified"
    applicability = f"Product: {product or 'unknown'}; version/build: {version or 'unknown'}. Validate both before applying any KB or procedure."
    official_refs = match_official_references(text)
    reference_text = "\n".join(
        f"- [{ref.title}]({ref.url}) — candidate because: {ref.match_reason} Confirm exact build, topology, prerequisites, and article update date before use."
        for ref in official_refs
    ) or "- No specific Broadcom KB was verified from the supplied evidence. Collect the missing evidence and search current official documentation by exact error/build before selecting a resolution."

    if workflow == "pc_navigation":
        approval = "Approval recorded for planning this single action; execution remains disabled in the MVP." if external_action_approved else "BLOCKED: no explicit human approval was supplied."
        content = f"""# PC Navigation Safety Gate

## Status
{approval}

## Proposed action
Describe the exact target application, action, expected result, and affected data before approval. This MVP provides instructions only and has no computer-control integration.

## Risk classification
- **READ-ONLY:** viewing a local screen or file still requires explicit approval when using future computer-control tooling.
- **RISKY — APPROVAL REQUIRED:** every click, keystroke, upload, download, message, account action, external request, or system change requires a separate, explicit human approval.

## Rollback / recovery
Identify how to undo the specific action, preserve unsaved work, and stop immediately on unexpected state.

## Evidence and assumptions
No external action was executed. Intent and UI state remain unverified.
"""
    elif workflow in {"business", "learning", "career", "documents", "tech_devices", "media", "portfolio"}:
        headings = {
            "business": ("Business Strategy Agent", "Treat market and financial claims as assumptions until sourced; identify decisions, options, trade-offs, owners, and measurable outcomes."),
            "learning": ("Learning Coach", "Set a concrete learning objective, assess current understanding, propose active practice, and use a feedback loop rather than giving answers alone."),
            "career": ("Career & Job Application Agent", "Tailor CVs, applications, interview preparation, and recruiter outreach to supplied evidence; never invent qualifications or submit an application."),
            "documents": ("Documents & Forms Agent", "Extract requirements, identify missing fields, and prepare document or form drafts; preserve originals and never fabricate signatures, dates, identifiers, or official facts."),
            "tech_devices": ("Consumer Tech & Device Troubleshooting Agent", "Identify the exact model, firmware, symptoms, and recovery options; start with reversible checks and warn before flashing, unlocking, wiping, or hardware changes."),
            "media": ("Media & Creative Task Agent", "Clarify the desired deliverable, preserve source quality, and produce an editable plan or draft while respecting consent, copyright, and personal-image privacy."),
            "portfolio": ("Project Portfolio Agent", "Identify the surviving artifact, the author's contribution, technologies, evidence, current status, next milestone, and whether the work is an idea, prototype, tested MVP, shipped project, or production deployment."),
        }
        title, guardrail = headings[workflow]
        content = f"""# {title}

## Request framing
{guardrail}

## Observed input
{_evidence_lines(findings)}

## Suggested approach
- Separate known facts, assumptions, and decisions still needed.
- Prefer reversible, low-risk next steps.
- Verify current claims with authoritative sources where consequences matter; say when freshness was not checked.
- Do not send messages, make purchases, access accounts, disclose private data, or change external systems automatically.

## Human decision gate
Any external, financial, medical, account, communication, or system-changing action requires explicit human review and approval. No such action was executed.

## Confidence and missing information
Confidence: **low** until domain-specific context and authoritative evidence are supplied.
""" + "\n".join(f"- {item}" for item in missing)
    elif workflow == "email":
        content = f"""# Customer-ready email draft

Subject: Update on the reported VMware issue

Hello,

We reviewed the supplied material. The confirmed observations are:
{_evidence_lines(findings)}

The currently implicated components are: {components}. This does not yet confirm root cause. We recommend collecting the missing evidence listed below and validating product/version applicability before following a KB or remediation.

Next safe step: collect the relevant support bundle and preserve timestamps. No infrastructure change has been performed or requested automatically.

Regards,\n[Support engineer name]

## Applicability gate
{applicability}

## Missing evidence
""" + "\n".join(f"- {item}" for item in missing)
    elif workflow == "automation":
        content = f"""# Safe automation suggestion

## Goal
Collect diagnostic evidence for: {components}.

## Proposed behavior
- **READ-ONLY:** enumerate relevant services, versions, and log timestamps.
- **READ-ONLY:** copy selected log excerpts to a local evidence bundle.
- **DISRUPTIVE — APPROVAL REQUIRED:** restart a service only after explicit human confirmation.
- **RISKY — APPROVAL REQUIRED:** make configuration, certificate, identity, networking, storage, or cluster changes only with an approved change window.

This assistant generates suggestions only and never executes infrastructure changes.

## Rollback plan
Before any approved change: export current configuration, record service state, define a restore command, owner, success criterion, and abort threshold.

## Applicability gate
{applicability}
"""
    else:
        title = "Log Analysis Agent" if workflow == "logs" else "VMware Case Agent"
        content = f"""# {title}

## Issue Clarification
Observed components: {components}. Scope, onset, reproducibility, business impact, and recent changes remain to be confirmed.

## Evidence / Verification
{_evidence_lines(findings)}

## Ranked hypotheses (not confirmed causes)
1. **HYPOTHESIS — component/service degradation:** Supported by component/error proximity; verify timestamps and service health.
2. **HYPOTHESIS — dependency or registration issue:** Check SSO, Lookup Service, DNS, NTP, and certificate chains where applicable.
3. **HYPOTHESIS — resource or environmental pressure:** Correlate CPU, memory, storage latency/capacity, and network events.

## Safe checks
- **READ-ONLY:** confirm exact build, topology, timestamps, service status, capacity, and recent events.
- **READ-ONLY:** correlate the cited evidence IDs across relevant logs.
- **READ-ONLY:** search only official Broadcom/VMware references, then verify product, build, symptoms, and prerequisites.

## Risky checks — APPROVAL REQUIRED
- **DISRUPTIVE:** service restart or failover. Confirm impact and maintenance window first.
- **RISKY:** certificate, identity, database, storage, networking, cluster, or lifecycle changes. Require an owner and tested rollback.

## Rollback plan
Capture current state/configuration, define restore steps and abort thresholds, assign an owner, and validate recovery before change approval.

## Customer-ready draft
We observed evidence involving {components}. Root cause is not yet confirmed. We recommend read-only validation and collection of correlated evidence before any change.

## Internal-note draft
Observed: evidence IDs {', '.join(item.id for item in findings.evidence[:8])}. Inferred: listed hypotheses only. Unverified: scope, chronology, environment changes, version applicability, and causal relationship.

## KB applicability gate
{applicability} Limit customer-facing references to the smallest relevant set of official sources.

## Official reference assessment
{reference_text}

## Quality checklist
- [x] Observations separated from inference and assumptions
- [x] Evidence IDs mapped to submitted source lines
- [x] Commands/actions classified by risk
- [x] Approval and rollback required for disruptive/risky actions
- [ ] Product/version and KB applicability verified
- [ ] Resolution success criteria and monitoring window agreed

## Confidence and missing evidence
Confidence: **{confidence}**
""" + "\n".join(f"- {item}" for item in missing)
    return content, findings, confidence, missing
