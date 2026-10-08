"""Unit tests for Valuation Haircut Engine and Deal Memo Generator."""

import unittest
from apex_vdr_swarm.valuation.haircut_engine import EbitdaHaircutEngine, ValuationSummary
from apex_vdr_swarm.valuation.memo_generator import DealMemoGenerator
from apex_vdr_swarm.ingestion.ledger_reconciler import LedgerReconciler
from apex_vdr_swarm.agents.forensic_accounting import ForensicAccountingAgent
from apex_vdr_swarm.agents.gpu_infrastructure import GpuInfrastructureAgent
from apex_vdr_swarm.agents.tech_ip import TechIpAuditAgent
from apex_vdr_swarm.agents.cyber_actuary import CyberRiskActuaryAgent
from apex_vdr_swarm.ingestion.code_auditor import CodebaseAuditor


class TestValuationEngine(unittest.TestCase):
    def setUp(self):
        reconciler = LedgerReconciler(demo_mode=True)
        auditor = CodebaseAuditor(demo_mode=True)
        self.ledger_summary = reconciler.reconcile_ledger()

        # Collect findings
        self.findings = []
        self.findings.extend(ForensicAccountingAgent(reconciler).audit())
        self.findings.extend(GpuInfrastructureAgent().audit())
        self.findings.extend(TechIpAuditAgent(auditor).audit())
        self.findings.extend(CyberRiskActuaryAgent(auditor).audit())

        self.engine = EbitdaHaircutEngine(base_multiple=14.0)

    def test_calculate_valuation(self):
        val = self.engine.calculate_valuation(
            reported_ebitda=self.ledger_summary.reported_ebitda_usd,
            findings=self.findings,
        )
        self.assertEqual(val.reported_ebitda_usd, 42_000_000.0)
        self.assertGreater(val.recurring_ebitda_haircut_usd, 15_000_000.0)
        self.assertLess(val.adjusted_ebitda_usd, 27_000_000.0)
        self.assertGreater(val.total_multiple_discount, 1.5)
        self.assertLess(val.adjusted_multiple, 13.0)
        self.assertGreater(val.net_valuation_haircut_usd, 200_000_000.0)
        self.assertGreater(val.net_haircut_pct, 40.0)
        self.assertGreater(val.recommended_escrow_holdback_usd, 10_000_000.0)
        self.assertEqual(val.deal_recommendation, "RENEGOTIATE_LOI_WITH_MATERIAL_HAIRCUT")

    def test_memo_generator(self):
        val = self.engine.calculate_valuation(
            reported_ebitda=self.ledger_summary.reported_ebitda_usd,
            findings=self.findings,
        )
        memo = DealMemoGenerator.generate_markdown_memo(
            deal_name="Project Atlas",
            summary=val,
            ledger=self.ledger_summary,
            findings=self.findings,
        )
        self.assertIn("CONFIDENTIAL INVESTMENT COMMITTEE DILIGENCE MEMO", memo)
        self.assertIn("Project Atlas", memo)
        self.assertIn("RENEGOTIATE_LOI_WITH_MATERIAL_HAIRCUT", memo)
        self.assertIn("FIND-FIN-01", memo)
        self.assertIn("FIND-GPU-01", memo)


if __name__ == "__main__":
    unittest.main()
