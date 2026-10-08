"""Unit tests for specialist diligence agents."""

import unittest
from apex_vdr_swarm.ingestion.ledger_reconciler import LedgerReconciler
from apex_vdr_swarm.ingestion.code_auditor import CodebaseAuditor
from apex_vdr_swarm.agents.forensic_accounting import ForensicAccountingAgent
from apex_vdr_swarm.agents.gpu_infrastructure import GpuInfrastructureAgent
from apex_vdr_swarm.agents.tech_ip import TechIpAuditAgent
from apex_vdr_swarm.agents.cyber_actuary import CyberRiskActuaryAgent
from apex_vdr_swarm.agents.base import FindingSeverity


class TestDiligenceAgents(unittest.TestCase):
    def test_forensic_accounting_agent(self):
        agent = ForensicAccountingAgent(LedgerReconciler(demo_mode=True))
        findings = agent.audit()
        self.assertGreaterEqual(len(findings), 2)

        # Check ASC 606 critical finding
        f_asc = next(f for f in findings if f.id == "FIND-FIN-01")
        self.assertEqual(f_asc.severity, FindingSeverity.CRITICAL)
        self.assertGreater(f_asc.ebitda_haircut_usd, 10_000_000.0)
        self.assertEqual(f_asc.multiple_discount, 0.50)

    def test_gpu_infrastructure_agent(self):
        agent = GpuInfrastructureAgent()
        findings = agent.audit()
        self.assertEqual(len(findings), 1)

        f_gpu = findings[0]
        self.assertEqual(f_gpu.category, "GPU")
        self.assertGreater(f_gpu.ebitda_haircut_usd, 1_000_000.0)
        self.assertGreater(f_gpu.direct_liability_usd, 10_000_000.0)

    def test_tech_ip_agent(self):
        agent = TechIpAuditAgent(CodebaseAuditor(demo_mode=True))
        findings = agent.audit()
        self.assertGreaterEqual(len(findings), 2)

        f_ip = next(f for f in findings if f.id == "FIND-IP-01")
        self.assertEqual(f_ip.escrow_hold_usd, 3_500_000.0)

    def test_cyber_actuary_agent(self):
        agent = CyberRiskActuaryAgent(CodebaseAuditor(demo_mode=True))
        findings = agent.audit()
        self.assertEqual(len(findings), 2)

        f_cve = next(f for f in findings if f.id == "FIND-CYBER-01")
        self.assertEqual(f_cve.direct_liability_usd, 139_000.0)


if __name__ == "__main__":
    unittest.main()
