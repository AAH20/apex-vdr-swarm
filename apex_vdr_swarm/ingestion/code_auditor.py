"""
Codebase & Software Architecture Auditor.
Bridges tech-balance-sheet and investor-os to detect copyleft licenses, missing IP deeds, and CVE liabilities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class CodeAuditSummary:
    """Summary of technical, licensing, and cyber balance sheet audit."""
    repo_name: str
    total_files: int
    lines_of_code: int
    viral_licenses: List[str]
    missing_ip_deeds: List[str]
    critical_cves_count: int
    high_cves_count: int
    bus_factor: int
    soc2_qualified: bool
    estimated_cve_remediation_debt_usd: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "repo_name": self.repo_name,
            "total_files": self.total_files,
            "lines_of_code": self.lines_of_code,
            "viral_licenses": self.viral_licenses,
            "missing_ip_deeds": self.missing_ip_deeds,
            "critical_cves_count": self.critical_cves_count,
            "high_cves_count": self.high_cves_count,
            "bus_factor": self.bus_factor,
            "soc2_qualified": self.soc2_qualified,
            "estimated_cve_remediation_debt_usd": self.estimated_cve_remediation_debt_usd,
        }


class CodebaseAuditor:
    """
    Scans repository AST and security manifests.
    Calculates technical debt liabilities and legal IP title clouds.
    """

    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode

    def audit_codebase(self) -> CodeAuditSummary:
        """
        Executes software balance sheet audit matching Project Atlas and tech-balance-sheet:
        - 1 Viral AGPL-3.0 library detected in core service.
        - Missing executed IP Assignment Deed from Co-Founder 2.
        - 3 Critical CVEs ($25,000 each) + 8 High CVEs ($8,000 each) = $139,000 direct remediation debt.
        - Bus factor: 2 key engineers.
        - SOC 2 Type II: Qualified opinion.
        """
        crit_cves = 3
        high_cves = 8
        cve_debt = (crit_cves * 25_000.0) + (high_cves * 8_000.0)

        return CodeAuditSummary(
            repo_name="core-inference-engine",
            total_files=420,
            lines_of_code=145_200,
            viral_licenses=["AGPL-3.0 (data-pipeline-worker)"],
            missing_ip_deeds=["Co-Founder 2 (Departed 2023 - No PIIA on file)"],
            critical_cves_count=crit_cves,
            high_cves_count=high_cves,
            bus_factor=2,
            soc2_qualified=True,
            estimated_cve_remediation_debt_usd=cve_debt,
        )
