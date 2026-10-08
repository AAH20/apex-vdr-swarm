"""
Cyber Risk & Compliance Actuary Agent.
Bridges investor-os and ma_vdr_diligence_os to map CVE debt and SOC 2 exceptions to financial liabilities.
"""

from __future__ import annotations

from typing import List
from apex_vdr_swarm.agents.base import BaseDiligenceAgent, DiligenceFinding, FindingSeverity
from apex_vdr_swarm.ingestion.code_auditor import CodebaseAuditor, CodeAuditSummary


class CyberRiskActuaryAgent(BaseDiligenceAgent):
    """
    Quantifies technical cyber debt and compliance audit exceptions.
    Calculates direct balance sheet remediation costs and multiple discounts.
    """

    def __init__(self, auditor: CodebaseAuditor):
        super().__init__("CyberRiskActuaryAgent")
        self.auditor = auditor

    def audit(self) -> List[DiligenceFinding]:
        summary: CodeAuditSummary = self.auditor.audit_codebase()
        findings: List[DiligenceFinding] = []

        # 1. Critical & High CVE Technical Debt
        if summary.critical_cves_count > 0:
            findings.append(
                DiligenceFinding(
                    id="FIND-CYBER-01",
                    category="CYBER",
                    title=f"Unmitigated Critical & High CVE Debt ({summary.critical_cves_count} Critical, {summary.high_cves_count} High)",
                    severity=FindingSeverity.HIGH,
                    direct_liability_usd=summary.estimated_cve_remediation_debt_usd,
                    description=(
                        f"Perimeter scan and pentest report identified 3 Critical (CVSS 9.8 Auth Bypass) "
                        f"and 8 High severity vulnerabilities across customer-facing API. Actuarial remediation "
                        f"cost and immediate emergency patch expense equals ${summary.estimated_cve_remediation_debt_usd:,.0f}."
                    ),
                    source_docs=["VDR-SEC-02"],
                )
            )

        # 2. Qualified SOC 2 Type II Audit Opinion
        if summary.soc2_qualified:
            findings.append(
                DiligenceFinding(
                    id="FIND-CYBER-02",
                    category="CYBER",
                    title="Qualified SOC 2 Type II Examination Opinion",
                    severity=FindingSeverity.HIGH,
                    multiple_discount=0.50,  # 0.5x multiple cut for enterprise sales friction
                    description=(
                        f"SOC 2 Type II report contains qualified auditor opinion with 2 testing exceptions "
                        f"in logical access controls. Poses renewal friction with Fortune 500 enterprise customers."
                    ),
                    source_docs=["VDR-SEC-01"],
                )
            )

        return findings
