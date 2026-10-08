"""
apex-vdr-swarm (`a2z-atlas-vdr`): Autonomous M&A Deal Room & Private Equity Due Diligence Swarm.
GraphRAG Multi-Agent Swarm with Deterministic NP-Hard Graph Solvers.

Apex Growth Systems LLC | a2zsoc.com | NVIDIA Inception Program Partner
Managing Member: Ahmed Hassan (aah@a2zsoc.com)
"""

__version__ = "1.0.0"
__author__ = "Ahmed Hassan <aah@a2zsoc.com>"
__license__ = "MIT"

from apex_vdr_swarm.ingestion.corpus_loader import VdrCorpusLoader, VdrDocument
from apex_vdr_swarm.ingestion.ledger_reconciler import LedgerReconciler, LedgerSummary
from apex_vdr_swarm.ingestion.code_auditor import CodebaseAuditor, CodeAuditSummary
from apex_vdr_swarm.graph.deal_hypergraph import DealHypergraph, HyperNode, HyperEdge
from apex_vdr_swarm.solvers.pcst_extractor import PcstEvidenceExtractor, PcstResult
from apex_vdr_swarm.solvers.pivot_multicut import PivotEntityResolver
from apex_vdr_swarm.solvers.causal_dp import CausalPathValidator, CausalViolation
from apex_vdr_swarm.solvers.submodular_pruner import SubmodularContextPruner
from apex_vdr_swarm.agents.base import DiligenceFinding, FindingSeverity
from apex_vdr_swarm.valuation.haircut_engine import EbitdaHaircutEngine, ValuationSummary
from apex_vdr_swarm.valuation.memo_generator import DealMemoGenerator

__all__ = [
    "VdrCorpusLoader",
    "VdrDocument",
    "LedgerReconciler",
    "LedgerSummary",
    "CodebaseAuditor",
    "CodeAuditSummary",
    "DealHypergraph",
    "HyperNode",
    "HyperEdge",
    "PcstEvidenceExtractor",
    "PcstResult",
    "PivotEntityResolver",
    "CausalPathValidator",
    "CausalViolation",
    "SubmodularContextPruner",
    "DiligenceFinding",
    "FindingSeverity",
    "EbitdaHaircutEngine",
    "ValuationSummary",
    "DealMemoGenerator",
]
