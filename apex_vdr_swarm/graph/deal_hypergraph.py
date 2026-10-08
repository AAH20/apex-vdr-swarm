"""
Deal Room Knowledge Hypergraph Store.
Builds the integrated cross-modal graph linking companies, customer contracts, invoices, ledger entries, and code assets.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any


@dataclass
class HyperNode:
    """An individual entity node in the deal graph."""
    id: str
    label: str
    node_type: str  # Company, Customer, Contract, Invoice, LedgerLine, GpuCluster, RepoFile, Vulnerability
    properties: Dict[str, Any] = field(default_factory=dict)
    prize: float = 1.0  # Used by Prize-Collecting Steiner Tree solver

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "node_type": self.node_type,
            "properties": self.properties,
            "prize": round(self.prize, 2),
        }


@dataclass
class HyperEdge:
    """A directed relational edge in the deal graph."""
    source_id: str
    target_id: str
    relation_type: str  # SIGNS, BILLS_TO, POSTED_IN, EXECUTES_ON, CONTAINS, VIOLATES
    cost: float = 1.0  # Edge traversal cost for Steiner Tree
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type,
            "cost": round(self.cost, 2),
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }


class DealHypergraph:
    """
    In-memory cross-modal deal hypergraph.
    Connects financial double-entry records, customer contracts, GPU leases, and code AST.
    """

    def __init__(self):
        self.nodes: Dict[str, HyperNode] = {}
        self.edges: List[HyperEdge] = []
        self._adj: Dict[str, List[HyperEdge]] = {}

    def add_node(self, node: HyperNode) -> None:
        self.nodes[node.id] = node
        if node.id not in self._adj:
            self._adj[node.id] = []

    def add_edge(self, edge: HyperEdge) -> None:
        self.edges.append(edge)
        if edge.source_id not in self._adj:
            self._adj[edge.source_id] = []
        self._adj[edge.source_id].append(edge)

    def get_neighbors(self, node_id: str) -> List[str]:
        return [e.target_id for e in self._adj.get(node_id, [])]

    def get_edges_from(self, node_id: str) -> List[HyperEdge]:
        return self._adj.get(node_id, [])

    @property
    def node_count(self) -> int:
        return len(self.nodes)

    @property
    def edge_count(self) -> int:
        return len(self.edges)

    def build_atlas_hypergraph(self) -> None:
        """Seed representative deal hypergraph for Project Atlas."""
        # 1. Company Core
        self.add_node(HyperNode("comp:atlas", "Project Atlas Parent", "Company", {"revenue": 202_000_000}, prize=100.0))

        # 2. Key Customers
        self.add_node(HyperNode("cust:c001", "Enterprise Tier 1 (C-001)", "Customer", {"arr": 28_000_000}, prize=80.0))
        self.add_node(HyperNode("cust:c084", "Drain Tenant (C-084)", "Customer", {"gross_margin": -0.14}, prize=95.0))
        self.add_node(HyperNode("cust:c012", "Growth Account (C-012)", "Customer", {"arr": 14_000_000}, prize=50.0))

        # 3. Customer Contracts
        self.add_node(HyperNode("contract:msa_01", "MSA-Tier1-90DayTerm", "Contract", {"term_convenience": True}, prize=70.0))
        self.add_node(HyperNode("contract:drain_084", "MSA-UnmeteredGPU", "Contract", {"capped": False}, prize=90.0))

        # 4. Invoices & ASC 606 Ledgers
        self.add_node(HyperNode("inv:q4_services", "Q4 SOW Services Invoices ($22M)", "Invoice", {"amount": 22_000_000}, prize=100.0))
        self.add_node(HyperNode("ledger:asc606", "ASC 606 Journal Account #4100", "LedgerLine", {"misclassified": True}, prize=100.0))

        # 5. Infrastructure & GPUs
        self.add_node(HyperNode("gpu:cluster_1024", "1024x NVIDIA H100 Lease", "GpuCluster", {"utilization": 0.584, "cost": 18_400_000}, prize=85.0))

        # 6. Repositories & Vulnerabilities
        self.add_node(HyperNode("repo:inference", "core-inference-engine", "RepoFile", {"viral_gpl": True}, prize=75.0))
        self.add_node(HyperNode("vuln:cve_auth", "CVE-2024-AuthBypass (CVSS 9.8)", "Vulnerability", {"severity": "CRITICAL"}, prize=90.0))
        self.add_node(HyperNode("legal:ip_deed", "Missing PIIA Deed (Founder 2)", "Legal", {"title_cloud": True}, prize=95.0))

        # Connect with relational edges
        self.add_edge(HyperEdge("comp:atlas", "cust:c001", "BILLS_TO", cost=1.0))
        self.add_edge(HyperEdge("comp:atlas", "cust:c084", "BILLS_TO", cost=1.0))
        self.add_edge(HyperEdge("cust:c001", "contract:msa_01", "SIGNS", cost=1.0))
        self.add_edge(HyperEdge("cust:c084", "contract:drain_084", "SIGNS", cost=1.0))
        self.add_edge(HyperEdge("contract:msa_01", "inv:q4_services", "BILLS_TO", cost=1.2))
        self.add_edge(HyperEdge("inv:q4_services", "ledger:asc606", "POSTED_IN", cost=1.5))
        self.add_edge(HyperEdge("contract:drain_084", "gpu:cluster_1024", "EXECUTES_ON", cost=2.0))
        self.add_edge(HyperEdge("comp:atlas", "repo:inference", "CONTAINS", cost=1.0))
        self.add_edge(HyperEdge("repo:inference", "vuln:cve_auth", "CONTAINS", cost=1.5))
        self.add_edge(HyperEdge("comp:atlas", "legal:ip_deed", "VIOLATES", cost=1.0))
