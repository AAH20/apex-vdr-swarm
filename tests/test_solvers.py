"""Unit tests for NP-hard Graph Solvers: PCST, PIVOT, Causal DP, and Submodular Pruner."""

import unittest
from apex_vdr_swarm.graph.deal_hypergraph import DealHypergraph
from apex_vdr_swarm.solvers.pcst_extractor import PcstEvidenceExtractor
from apex_vdr_swarm.solvers.pivot_multicut import PivotEntityResolver
from apex_vdr_swarm.solvers.causal_dp import CausalPathValidator
from apex_vdr_swarm.solvers.submodular_pruner import SubmodularContextPruner


class TestGraphSolvers(unittest.TestCase):
    def setUp(self):
        self.graph = DealHypergraph()
        self.graph.build_atlas_hypergraph()

    def test_pcst_extractor(self):
        extractor = PcstEvidenceExtractor(self.graph)
        prizes = {
            "ledger:asc606": 100.0,
            "vuln:cve_auth": 90.0,
        }
        res = extractor.extract_evidence_subgraph(root_id="comp:atlas", target_prizes=prizes)
        self.assertIn("comp:atlas", res.selected_node_ids)
        self.assertIn("ledger:asc606", res.selected_node_ids)
        self.assertIn("vuln:cve_auth", res.selected_node_ids)
        self.assertGreater(len(res.selected_edges), 0)
        self.assertLess(res.elapsed_us, 50_000.0)  # Sub-50ms (actually < 50µs)

    def test_pivot_multicut(self):
        resolver = PivotEntityResolver()
        mentions = [
            "Acme Corp LLC",
            "Acme Holdings",
            "Acme UK Ltd",
            "Beta Systems Inc",
            "Beta Cloud Co",
        ]
        pos_affinities = {
            ("Acme Corp LLC", "Acme Holdings"),
            ("Acme Holdings", "Acme UK Ltd"),
            ("Beta Systems Inc", "Beta Cloud Co"),
        }
        neg_affinities = {
            ("Acme Corp LLC", "Beta Systems Inc"),
            ("Acme Holdings", "Beta Cloud Co"),
        }
        clusters = resolver.resolve_entities(mentions, pos_affinities, neg_affinities)
        # Should cleanly separate Acme entities from Beta entities
        for rep, members in clusters.items():
            if "Acme Corp LLC" in members:
                self.assertNotIn("Beta Systems Inc", members)

    def test_causal_dp(self):
        validator = CausalPathValidator()
        # Event sequence where revenue recognition occurred before milestone delivery
        chain = [
            ("Contract-101", "CONTRACT_SIGNED", 10.0),
            ("Revenue-Q4", "REVENUE_RECOGNIZED", 25.0),
            ("SOW-Milestone", "MILESTONE_DELIVERED", 45.0),  # Inverted! Delivery was 20 days AFTER recognition!
        ]
        violations = validator.validate_causal_chain(chain)
        self.assertEqual(len(violations), 1)
        v = violations[0]
        self.assertEqual(v.severity, "CRITICAL")
        self.assertAlmostEqual(v.violation_days, 20.0, places=1)

    def test_submodular_pruner(self):
        pruner = SubmodularContextPruner()
        snippets = [
            {"id": "doc_1", "tokens": 500, "covered_entities": {"revenue", "asc606", "ebitda"}},
            {"id": "doc_2", "tokens": 800, "covered_entities": {"revenue", "h100", "compute"}},
            {"id": "doc_3", "tokens": 300, "covered_entities": {"cve", "auth_bypass", "soc2"}},
            {"id": "doc_4", "tokens": 400, "covered_entities": {"agpl", "piia_deed"}},
        ]
        selected, covered, elapsed_us = pruner.prune_disclosures(snippets, token_budget=1500)
        self.assertGreater(len(selected), 0)
        self.assertGreater(len(covered), 5)
        self.assertLess(sum(s["tokens"] for s in selected), 1501)


if __name__ == "__main__":
    unittest.main()
