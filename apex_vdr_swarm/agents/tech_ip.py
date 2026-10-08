"""
Intellectual Property & Codebase Diligence Agent.
Bridges tech-balance-sheet to audit viral copyleft licenses, IP title clouds, and bus factor.
"""

from __future__ import annotations

from typing import List
from apex_vdr_swarm.agents.base import BaseDiligenceAgent, DiligenceFinding, FindingSeverity
from apex_vdr_swarm.ingestion.code_auditor import CodebaseAuditor, CodeAuditSummary


class TechIpAuditAgent(BaseDiligenceAgent):
    """
    Audits codebase AST, license manifests, and founder IP assignment agreements.
    Identifies viral copyleft exposure and legal title clouds.
    """

    def __init__(self, auditor: CodebaseAuditor):
        super().__init__("TechIpAuditAgent")
        self.auditor = auditor

    def audit(self) -> List[DiligenceFinding]:
        summary: CodeAuditSummary = self.auditor.audit_codebase()
        findings: List[DiligenceFinding] = []

        # 1. Missing IP Assignment Deed from Co-Founder 2
        if summary.missing_ip_deeds:
            findings.append(
                DiligenceFinding(
                    id="FIND-IP-01",
                    category="IP",
                    title="Missing Founder IP Assignment Deed (Co-Founder 2 Cloud on Title)",
                    severity=FindingSeverity.HIGH,
                    escrow_hold_usd=3_500_000.0,  # $3.5M special indemnity escrow holdback
                    description=(
                        f"Co-Founder 2 departed in 2023 without an executed Proprietary Information & "
                        f"Inventions Agreement (PIIA). Poses material risk of copyright ownership dispute "
                        f"over foundational model orchestration algorithms. Requires $3.5M special escrow holdback."
                    ),
                    source_docs=["VDR-IP-03", "VDR-CORP-02"],
                )
            )

        # 2. Viral AGPL-3.0 License Contamination
        if summary.viral_licenses:
            findings.append(
                DiligenceFinding(
                    id="FIND-IP-02",
                    category="IP",
                    title="Viral AGPL-3.0 Copyleft License Contamination",
                    severity=FindingSeverity.MEDIUM,
                    direct_liability_usd=350_000.0,  # Engineering re-platforming cost
                    description=(
                        f"Detected AGPL-3.0 library compiled directly into backend data worker pipeline. "
                        f"Requires complete clean-room rewrite to eliminate viral reciprocal disclosure obligations."
                    ),
                    source_docs=["VDR-IP-02"],
                )
            )

        # 3. Key-Person Bus Factor Risk
        if summary.bus_factor <= 2:
            findings.append(
                DiligenceFinding(
                    id="FIND-TECH-01",
                    category="IP",
                    title=f"Key-Person Bus Factor Risk (Bus Factor = {summary.bus_factor})",
                    severity=FindingSeverity.MEDIUM,
                    multiple_discount=0.25,  # 0.25x multiple cut for key-person dependency
                    description=(
                        f"Over 74% of core inference codebase commits authored by only 2 individuals. "
                        f"Requires post-close key employee retention bonus pool."
                    ),
                    source_docs=["VDR-IP-01"],
                )
            )

        return findings
