"""Unit tests for VDR Ingestion modules."""

import unittest
from apex_vdr_swarm.ingestion.corpus_loader import VdrCorpusLoader
from apex_vdr_swarm.ingestion.ledger_reconciler import LedgerReconciler
from apex_vdr_swarm.ingestion.code_auditor import CodebaseAuditor


class TestVdrIngestion(unittest.TestCase):
    def test_corpus_loader(self):
        loader = VdrCorpusLoader(demo_mode=True)
        docs = loader.load_documents()
        self.assertEqual(len(docs), 66)

        flagged = loader.get_flagged_documents()
        self.assertGreaterEqual(len(flagged), 8)

        categories = {d.category for d in docs}
        self.assertIn("Financial", categories)
        self.assertIn("IP_Tech", categories)
        self.assertIn("Infrastructure", categories)
        self.assertIn("Security", categories)

    def test_ledger_reconciler(self):
        reconciler = LedgerReconciler(demo_mode=True)
        summary = reconciler.reconcile_ledger()
        self.assertEqual(summary.total_ledger_rows, 107_358)
        self.assertEqual(summary.reported_arr_usd, 180_000_000.0)
        self.assertEqual(summary.services_misclassified_usd, 22_000_000.0)
        self.assertEqual(summary.verified_arr_usd, 158_000_000.0)
        self.assertAlmostEqual(summary.top3_concentration_pct, 38.2, places=1)
        self.assertFalse(summary.is_reconciled)

    def test_codebase_auditor(self):
        auditor = CodebaseAuditor(demo_mode=True)
        summary = auditor.audit_codebase()
        self.assertEqual(summary.repo_name, "core-inference-engine")
        self.assertIn("AGPL-3.0 (data-pipeline-worker)", summary.viral_licenses)
        self.assertGreater(len(summary.missing_ip_deeds), 0)
        self.assertEqual(summary.critical_cves_count, 3)
        self.assertEqual(summary.estimated_cve_remediation_debt_usd, 139_000.0)


if __name__ == "__main__":
    unittest.main()
