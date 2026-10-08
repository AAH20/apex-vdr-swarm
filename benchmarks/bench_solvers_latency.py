"""
Microsecond Latency Benchmark for apex-vdr-swarm Solvers & Full Audit Pipeline.
Evaluates PCST, PIVOT, Causal DP, Submodular Pruner, and end-to-end deal valuation latency.
"""

from __future__ import annotations

import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from apex_vdr_swarm.graph.deal_hypergraph import DealHypergraph
from apex_vdr_swarm.solvers.pcst_extractor import PcstEvidenceExtractor
from apex_vdr_swarm.solvers.pivot_multicut import PivotEntityResolver
from apex_vdr_swarm.solvers.causal_dp import CausalPathValidator
from apex_vdr_swarm.solvers.submodular_pruner import SubmodularContextPruner
from apex_vdr_swarm.tui.app import VdrSwarmTuiApp


def run_benchmarks(iterations: int = 1000) -> None:
    print("=" * 85)
    print(" apex-vdr-swarm (`a2z-atlas-vdr`): Microsecond Latency Benchmark Suite")
    print(" Apex Growth Systems LLC | a2zsoc.com | NVIDIA Inception Program Partner")
    print("=" * 85)

    graph = DealHypergraph()
    graph.build_atlas_hypergraph()
    pcst = PcstEvidenceExtractor(graph)
    pivot = PivotEntityResolver()
    causal = CausalPathValidator()
    submod = SubmodularContextPruner()

    # 1. Benchmark PCST (Primal-Dual Goemans-Williamson)
    prizes = {"ledger:asc606": 100.0, "vuln:cve_auth": 90.0}
    start = time.perf_counter()
    for _ in range(iterations):
        _ = pcst.extract_evidence_subgraph("comp:atlas", prizes)
    elapsed = time.perf_counter() - start
    avg_pcst_us = (elapsed / iterations) * 1_000_000.0
    print(f"\n[1] Prize-Collecting Steiner Tree (PCST): {avg_pcst_us:6.2f} µs / query (Primal-Dual GW 2-Approx)")

    # 2. Benchmark PIVOT Correlation Clustering (Multicut)
    mentions = ["Acme Corp LLC", "Acme Holdings", "Acme UK Ltd", "Beta Systems Inc", "Beta Cloud Co"]
    pos = {("Acme Corp LLC", "Acme Holdings"), ("Acme Holdings", "Acme UK Ltd"), ("Beta Systems Inc", "Beta Cloud Co")}
    neg = {("Acme Corp LLC", "Beta Systems Inc"), ("Acme Holdings", "Beta Cloud Co")}
    start = time.perf_counter()
    for _ in range(iterations):
        _ = pivot.resolve_entities(mentions, pos, neg)
    elapsed = time.perf_counter() - start
    avg_pivot_us = (elapsed / iterations) * 1_000_000.0
    print(f"[2] PIVOT Entity Resolution Multicut:   {avg_pivot_us:6.2f} µs / resolution (3-Approx Bound)")

    # 3. Benchmark Constrained Causal Path DP
    chain = [
        ("Contract-101", "CONTRACT_SIGNED", 10.0),
        ("Revenue-Q4", "REVENUE_RECOGNIZED", 25.0),
        ("SOW-Milestone", "MILESTONE_DELIVERED", 45.0),
    ]
    start = time.perf_counter()
    for _ in range(iterations):
        _ = causal.validate_causal_chain(chain)
    elapsed = time.perf_counter() - start
    avg_causal_us = (elapsed / iterations) * 1_000_000.0
    print(f"[3] Constrained Causal Path DP:         {avg_causal_us:6.2f} µs / chain (Pareto Label-Setting)")

    # 4. Benchmark Submodular Context Window Pruner
    snippets = [
        {"id": "doc_1", "tokens": 500, "covered_entities": {"revenue", "asc606", "ebitda"}},
        {"id": "doc_2", "tokens": 800, "covered_entities": {"revenue", "h100", "compute"}},
        {"id": "doc_3", "tokens": 300, "covered_entities": {"cve", "auth_bypass", "soc2"}},
        {"id": "doc_4", "tokens": 400, "covered_entities": {"agpl", "piia_deed"}},
    ]
    start = time.perf_counter()
    for _ in range(iterations):
        _ = submod.prune_disclosures(snippets, token_budget=1500)
    elapsed = time.perf_counter() - start
    avg_submod_us = (elapsed / iterations) * 1_000_000.0
    print(f"[4] Submodular Context Pruner:          {avg_submod_us:6.2f} µs / optimization (1 - 1/e Bound)")

    # 5. Benchmark End-to-End Swarm Audit + Haircut Valuation
    start = time.perf_counter()
    for _ in range(iterations):
        app = VdrSwarmTuiApp(demo_mode=True)
        _ = app.valuation
    elapsed = time.perf_counter() - start
    avg_audit_ms = (elapsed / iterations) * 1000.0
    print(f"\n[5] Full Deal Room Audit & Haircut SLA: {avg_audit_ms:6.3f} ms / complete deal (66 docs + 107k lines)")

    print("\n" + "=" * 85)
    print(" BENCHMARK SLA VERIFICATION:")
    assert avg_pcst_us < 50.0, "PCST SLA violated (> 50µs)"
    assert avg_pivot_us < 50.0, "PIVOT SLA violated (> 50µs)"
    assert avg_causal_us < 50.0, "Causal DP SLA violated (> 50µs)"
    assert avg_submod_us < 50.0, "Submodular SLA violated (> 50µs)"
    assert avg_audit_ms < 100.0, "Full Audit SLA violated (> 100ms)"
    print(" [✓] Sub-50µs Graph Solver Kernel SLA: PASSED")
    print(" [✓] Sub-100ms Full Deal Valuation SLA: PASSED")
    print("=" * 85)


if __name__ == "__main__":
    run_benchmarks()
