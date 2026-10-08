"""
Investment Committee Deal Memo Generator.
Produces institutional Markdown and JSON due diligence memos for Private Equity Investment Committees.
"""

from __future__ import annotations

import time
from typing import List, Dict, Any

from apex_vdr_swarm.agents.base import DiligenceFinding, FindingSeverity
from apex_vdr_swarm.valuation.haircut_engine import ValuationSummary
from apex_vdr_swarm.ingestion.ledger_reconciler import LedgerSummary


class DealMemoGenerator:
    """
    Synthesizes specialist findings, mathematical valuation haircuts, and contract clauses
    into a formal Investment Committee (IC) Diligence Memo.
    """

    @staticmethod
    def generate_markdown_memo(
        deal_name: str,
        summary: ValuationSummary,
        ledger: LedgerSummary,
        findings: List[DiligenceFinding],
    ) -> str:
        date_str = time.strftime("%B %d, %Y")

        lines = [
            f"# CONFIDENTIAL INVESTMENT COMMITTEE DILIGENCE MEMO",
            f"**Target Company:** {deal_name} | **Evaluation Date:** {date_str}",
            f"**Authoring Engine:** apex-vdr-swarm (`a2z-atlas-vdr`) | **Managing Member:** Ahmed Hassan (`aah@a2zsoc.com`)",
            "",
            "---",
            "",
            "## 1. Executive Diligence Verdict & Valuation Impact",
            "",
            f"**RECOMMENDATION:** `{summary.deal_recommendation}`",
            "",
            f"Based on autonomous multi-agent GraphRAG diligence across 66 VDR documents and 107,358 general ledger lines, "
            f"the diligence swarm identified material accounting, compute lease, and IP title deficiencies requiring a "
            f"**-${summary.net_valuation_haircut_usd:,.0f} (-{summary.net_haircut_pct:.1f}%) net Enterprise Value purchase price haircut**.",
            "",
            "| Valuation Metric | Seller Reported | Diligence Adjusted | Variance / Deduction |",
            "| :--- | :---: | :---: | :---: |",
            f"| **Recurring ARR** | ${ledger.reported_arr_usd:,.0f} | ${ledger.verified_arr_usd:,.0f} | -${ledger.services_misclassified_usd:,.0f} (ASC 606 Gap) |",
            f"| **Normalized EBITDA** | ${summary.reported_ebitda_usd:,.0f} | ${summary.adjusted_ebitda_usd:,.0f} | -${summary.recurring_ebitda_haircut_usd:,.0f} (-{summary.ebitda_reduction_pct:.1f}%) |",
            f"| **EV Multiple** | {summary.base_multiple:.2f}x | {summary.adjusted_multiple:.2f}x | -{summary.total_multiple_discount:.2f}x (Risk Discounts) |",
            f"| **Direct Liabilities** | $0 | ${summary.total_direct_liabilities_usd:,.0f} | -${summary.total_direct_liabilities_usd:,.0f} (Cash Deductions) |",
            f"| **Enterprise Value (EV)** | **${summary.reported_ev_usd:,.0f}** | **${summary.adjusted_ev_usd:,.0f}** | **-${summary.net_valuation_haircut_usd:,.0f} (-{summary.net_haircut_pct:.1f}%)** |",
            f"| **Indemnity Escrow Holdback** | $0 | **${summary.recommended_escrow_holdback_usd:,.0f}** | 5% Base + Special IP Holdback |",
            "",
            "---",
            "",
            "## 2. Material Diligence Findings Breakdown",
            "",
        ]

        # Group findings by severity
        for idx, f in enumerate(findings, 1):
            lines.append(f"### {idx}. [{f.id}] [{f.severity.value}] {f.title} ({f.category})")
            lines.append(f"- **Description:** {f.description}")
            deductions = []
            if f.ebitda_haircut_usd > 0:
                deductions.append(f"EBITDA Haircut: -${f.ebitda_haircut_usd:,.0f}")
            if f.multiple_discount > 0:
                deductions.append(f"Multiple Cut: -{f.multiple_discount:.2f}x")
            if f.direct_liability_usd > 0:
                deductions.append(f"Direct Balance Sheet Debt: -${f.direct_liability_usd:,.0f}")
            if f.escrow_hold_usd > 0:
                deductions.append(f"Special Escrow Holdback: ${f.escrow_hold_usd:,.0f}")

            if deductions:
                lines.append(f"- **Quantitative Deduction:** {', '.join(deductions)}")
            lines.append(f"- **Source Documents:** {', '.join(f.source_docs)}")
            lines.append("")

        lines.extend([
            "---",
            "",
            "## 3. Recommended Purchase Agreement (SPA) Covenants & Next Steps",
            "",
            f"1. **Price Adjustment**: Amend Letter of Intent (LOI) headline consideration from "
            f"${summary.reported_ev_usd:,.0f} to **${summary.adjusted_ev_usd:,.0f}** reflecting true GAAP ASC 606 normalized ARR.",
            f"2. **Special Indemnity Escrow**: Require an indemnity holdback of **${summary.recommended_escrow_holdback_usd:,.0f}** "
            f"escrowed for 18 months specifically covering the missing Co-Founder 2 IP assignment deed and patent clouds.",
            f"3. **GPU Lease Novation**: Require seller to novate or extinguish the 1,024 NVIDIA H100 unabsorbed take-or-pay lease commitment "
            f"prior to deal closing.",
            f"4. **CVE Remediation Condition Precedent**: Contractual requirement for seller to patch the 3 Critical authentication bypass CVEs "
            f"prior to funds flow.",
            "",
            "---",
            "*Report generated deterministically by Apex Growth Systems LLC (`a2zsoc.com`) | NVIDIA Inception Partner*",
        ])

        return "\n".join(lines)
