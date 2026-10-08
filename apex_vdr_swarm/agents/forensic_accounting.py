"""
Forensic Accounting Diligence Agent.
Audits general ledger reconciliation, ARR vs GAAP ASC 606 recognition, and customer concentration.
"""

from __future__ import annotations

from typing import List
from apex_vdr_swarm.agents.base import BaseDiligenceAgent, DiligenceFinding, FindingSeverity
from apex_vdr_swarm.ingestion.ledger_reconciler import LedgerReconciler, LedgerSummary


class ForensicAccountingAgent(BaseDiligenceAgent):
    """
    Audits accounting ledger lines and customer billing streams.
    Unearths one-off professional services disguised as recurring SaaS ARR.
    """

    def __init__(self, reconciler: LedgerReconciler):
        super().__init__("ForensicAccountingAgent")
        self.reconciler = reconciler

    def audit(self) -> List[DiligenceFinding]:
        summary: LedgerSummary = self.reconciler.reconcile_ledger()
        findings: List[DiligenceFinding] = []

        # 1. $22M Services ARR Misclassification (ASC 606)
        if summary.services_misclassified_usd > 0:
            # Recurring EBITDA haircut: $22M * (1 - 0.35 services margin) = $14.3M
            ebitda_haircut = summary.services_misclassified_usd * 0.65
            findings.append(
                DiligenceFinding(
                    id="FIND-FIN-01",
                    category="FIN",
                    title="GAAP ASC 606 Revenue Misclassification ($22M Services in ARR)",
                    severity=FindingSeverity.CRITICAL,
                    ebitda_haircut_usd=ebitda_haircut,
                    multiple_discount=0.50,  # 0.5x valuation multiple haircut for accounting quality
                    description=(
                        f"${summary.services_misclassified_usd:,.0f} of one-off custom implementation services "
                        f"and pilot contracts were improperly recognized as recurring subscription ARR. "
                        f"Adjusting to GAAP ASC 606 reduces baseline ARR from ${summary.reported_arr_usd:,.0f} "
                        f"to ${summary.verified_arr_usd:,.0f}."
                    ),
                    source_docs=["VDR-FIN-01", "VDR-FIN-02"],
                )
            )

        # 2. Customer Concentration Hazard (>35% Top 3)
        if summary.top3_concentration_pct > 35.0:
            findings.append(
                DiligenceFinding(
                    id="FIND-COMM-01",
                    category="COMMERCIAL",
                    title=f"Excessive Customer Concentration (Top 3 = {summary.top3_concentration_pct:.1f}%)",
                    severity=FindingSeverity.HIGH,
                    multiple_discount=0.75,  # 0.75x multiple discount for revenue fragility
                    description=(
                        f"Top 3 customers account for {summary.top3_concentration_pct:.1f}% of recognized revenue "
                        f"(exceeds 35.0% institutional ceiling). Top customer contract contains 90-day "
                        f"termination for convenience clause."
                    ),
                    source_docs=["VDR-COMM-01", "VDR-COMM-02"],
                )
            )

        # 3. Negative Contribution Margin Tenant
        if summary.negative_margin_tenants_count > 0:
            findings.append(
                DiligenceFinding(
                    id="FIND-FIN-02",
                    category="FIN",
                    title="Negative Gross Margin Tenant (C-084 Compute Drain)",
                    severity=FindingSeverity.MEDIUM,
                    direct_liability_usd=summary.negative_margin_drain_usd,
                    description=(
                        f"Tenant C-084 operates at -14% gross margin due to unmetered GPU cluster access. "
                        f"Cumulative contract deficit represents ${summary.negative_margin_drain_usd:,.0f} direct drain."
                    ),
                    source_docs=["VDR-FIN-03"],
                )
            )

        return findings
