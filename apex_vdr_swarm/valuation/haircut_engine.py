"""
EBITDA Valuation Haircut & Balance Sheet Liability Engine.
Implements mathematically defensible M&A valuation adjustments and Reps & Warranties escrow sizing.
Derived from project-atlas-due-diligence and ma_vdr_diligence_os models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Any

from apex_vdr_swarm.agents.base import DiligenceFinding, FindingSeverity


@dataclass
class ValuationSummary:
    """Comprehensive mathematical valuation adjustment summary."""
    reported_ebitda_usd: float
    recurring_ebitda_haircut_usd: float
    adjusted_ebitda_usd: float
    ebitda_reduction_pct: float
    base_multiple: float
    total_multiple_discount: float
    adjusted_multiple: float
    reported_ev_usd: float
    total_direct_liabilities_usd: float
    adjusted_ev_usd: float
    net_valuation_haircut_usd: float
    net_haircut_pct: float
    recommended_escrow_holdback_usd: float
    deal_recommendation: str
    findings_count: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reported_ebitda_usd": self.reported_ebitda_usd,
            "recurring_ebitda_haircut_usd": self.recurring_ebitda_haircut_usd,
            "adjusted_ebitda_usd": self.adjusted_ebitda_usd,
            "ebitda_reduction_pct": round(self.ebitda_reduction_pct, 1),
            "base_multiple": self.base_multiple,
            "total_multiple_discount": round(self.total_multiple_discount, 2),
            "adjusted_multiple": round(self.adjusted_multiple, 2),
            "reported_ev_usd": self.reported_ev_usd,
            "total_direct_liabilities_usd": self.total_direct_liabilities_usd,
            "adjusted_ev_usd": self.adjusted_ev_usd,
            "net_valuation_haircut_usd": self.net_valuation_haircut_usd,
            "net_haircut_pct": round(self.net_haircut_pct, 1),
            "recommended_escrow_holdback_usd": self.recommended_escrow_holdback_usd,
            "deal_recommendation": self.deal_recommendation,
            "findings_count": self.findings_count,
        }


class EbitdaHaircutEngine:
    """
    Computes statistically defensible Enterprise Value haircuts:
    Adjusted EV = (Reported EBITDA - Delta_Recurring) * (Multiple - Sum(delta_Risk)) - Sum(Direct Liabilities)
    """

    def __init__(self, base_multiple: float = 14.0):
        self.base_multiple = base_multiple

    def calculate_valuation(
        self,
        reported_ebitda: float,
        findings: List[DiligenceFinding],
    ) -> ValuationSummary:
        """Calculate complete M&A haircut waterfall across all material findings."""
        # 1. Aggregate recurring EBITDA haircut (ASC 606 services misclassification + unabsorbed GPU drag)
        recurring_haircut = sum(f.ebitda_haircut_usd for f in findings)
        adjusted_ebitda = max(0.0, reported_ebitda - recurring_haircut)
        ebitda_pct = (recurring_haircut / reported_ebitda) * 100.0 if reported_ebitda > 0 else 0.0

        # 2. Aggregate multiple discounts (concentration + SOC 2 + bus factor + accounting quality)
        multiple_discount = sum(f.multiple_discount for f in findings)
        adjusted_multiple = max(1.0, self.base_multiple - multiple_discount)

        # 3. Aggregate direct cash liabilities (CVE debt + unabsorbed lease debt + negative tenant drain)
        direct_liabilities = sum(f.direct_liability_usd for f in findings)

        # 4. Compute Enterprise Values
        reported_ev = reported_ebitda * self.base_multiple
        operating_ev = adjusted_ebitda * adjusted_multiple
        adjusted_ev = max(0.0, operating_ev - direct_liabilities)

        net_haircut = reported_ev - adjusted_ev
        haircut_pct = (net_haircut / reported_ev) * 100.0 if reported_ev > 0 else 0.0

        # 5. Reps & Warranties Special Indemnity Escrow Sizing
        # Base escrow = 5% of adjusted EV + specific legal escrow holdbacks (e.g. $3.5M IP deed holdback)
        special_escrow_holds = sum(f.escrow_hold_usd for f in findings)
        base_indemnity_escrow = adjusted_ev * 0.05
        recommended_escrow = base_indemnity_escrow + special_escrow_holds

        # 6. Deal Recommendation
        if haircut_pct > 40.0 or any(f.severity == FindingSeverity.CRITICAL for f in findings):
            recommendation = "RENEGOTIATE_LOI_WITH_MATERIAL_HAIRCUT"
        elif haircut_pct > 20.0:
            recommendation = "PROCEED_WITH_PRICE_ADJUSTMENT"
        else:
            recommendation = "PROCEED_AS_STRUCTURED"

        return ValuationSummary(
            reported_ebitda_usd=reported_ebitda,
            recurring_ebitda_haircut_usd=recurring_haircut,
            adjusted_ebitda_usd=adjusted_ebitda,
            ebitda_reduction_pct=ebitda_pct,
            base_multiple=self.base_multiple,
            total_multiple_discount=multiple_discount,
            adjusted_multiple=adjusted_multiple,
            reported_ev_usd=reported_ev,
            total_direct_liabilities_usd=direct_liabilities,
            adjusted_ev_usd=adjusted_ev,
            net_valuation_haircut_usd=net_haircut,
            net_haircut_pct=haircut_pct,
            recommended_escrow_holdback_usd=recommended_escrow,
            deal_recommendation=recommendation,
            findings_count=len(findings),
        )
