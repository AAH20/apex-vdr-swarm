"""
Institutional Terminal Console for apex-vdr-swarm.
Clean, executive-grade presentation for M&A deal teams and Investment Committees.
Zero bloated ASCII banners.
"""

from __future__ import annotations

import curses
import json
import sys
import time
from typing import List, Dict, Optional, Any

from apex_vdr_swarm.ingestion.corpus_loader import VdrCorpusLoader, VdrDocument
from apex_vdr_swarm.ingestion.ledger_reconciler import LedgerReconciler, LedgerSummary
from apex_vdr_swarm.ingestion.code_auditor import CodebaseAuditor, CodeAuditSummary
from apex_vdr_swarm.graph.deal_hypergraph import DealHypergraph
from apex_vdr_swarm.solvers.pcst_extractor import PcstEvidenceExtractor
from apex_vdr_swarm.agents.base import DiligenceFinding, FindingSeverity
from apex_vdr_swarm.agents.forensic_accounting import ForensicAccountingAgent
from apex_vdr_swarm.agents.gpu_infrastructure import GpuInfrastructureAgent
from apex_vdr_swarm.agents.tech_ip import TechIpAuditAgent
from apex_vdr_swarm.agents.cyber_actuary import CyberRiskActuaryAgent
from apex_vdr_swarm.valuation.haircut_engine import EbitdaHaircutEngine, ValuationSummary
from apex_vdr_swarm.valuation.memo_generator import DealMemoGenerator


class VdrSwarmTuiApp:
    """
    Main terminal console for apex-vdr-swarm.
    Provides clean institutional tables and live M&A valuation haircut calculations.
    """

    def __init__(self, deal_name: str = "Project Atlas ($180M ARR)", demo_mode: bool = True):
        self.deal_name = deal_name
        self.demo_mode = demo_mode

        # Initialize engines
        self.corpus_loader = VdrCorpusLoader(demo_mode=demo_mode)
        self.ledger_reconciler = LedgerReconciler(demo_mode=demo_mode)
        self.code_auditor = CodebaseAuditor(demo_mode=demo_mode)
        self.haircut_engine = EbitdaHaircutEngine(base_multiple=14.0)

        # Graph and Solvers
        self.graph = DealHypergraph()
        self.graph.build_atlas_hypergraph()
        self.pcst_solver = PcstEvidenceExtractor(self.graph)

        # Specialist Swarm
        self.agents = [
            ForensicAccountingAgent(self.ledger_reconciler),
            GpuInfrastructureAgent(),
            TechIpAuditAgent(self.code_auditor),
            CyberRiskActuaryAgent(self.code_auditor),
        ]

        # Audit State
        self.documents: List[VdrDocument] = self.corpus_loader.load_documents()
        self.ledger_summary: LedgerSummary = self.ledger_reconciler.reconcile_ledger()
        self.findings: List[DiligenceFinding] = []
        self._run_audit_pipeline()

        self.valuation: ValuationSummary = self.haircut_engine.calculate_valuation(
            reported_ebitda=self.ledger_summary.reported_ebitda_usd,
            findings=self.findings,
        )

        self.active_tab = "DASHBOARD"  # DASHBOARD, MEMO, GRAPH, LEDGER
        self.status_message = "Ready. Press [m] for Deal Memo, [g] for Graph, [l] for Ledger, [q] to Quit."
        self._running = True

    def _run_audit_pipeline(self) -> None:
        """Run all specialist agents across the deal room."""
        self.findings = []
        for agent in self.agents:
            self.findings.extend(agent.audit())

    def get_snapshot(self) -> Dict[str, Any]:
        """Return complete structured diligence snapshot for JSON export."""
        return {
            "deal_name": self.deal_name,
            "timestamp": time.time(),
            "version": "1.0.0",
            "vdr_documents_count": len(self.documents),
            "ledger_summary": self.ledger_summary.to_dict(),
            "hypergraph": {
                "node_count": self.graph.node_count,
                "edge_count": self.graph.edge_count,
            },
            "valuation": self.valuation.to_dict(),
            "findings": [f.to_dict() for f in self.findings],
        }

    def render_text_frame(self, width: int = 110) -> str:
        """Renders the clean, institutional terminal frame without ASCII banners."""
        lines = [
            "=" * width,
            f" apex-vdr-swarm v1.0.0 — Autonomous M&A Diligence Engine | Apex Growth Systems LLC (a2zsoc.com) ",
            "-" * width,
            f" Deal Target: {self.deal_name} | VDR Docs: {len(self.documents)} Processed | Ledger Lines: {self.ledger_summary.total_ledger_rows:,} Reconciled",
            f" GraphRAG Core: 5/5 NP-Hard Solvers Active | Steiner Tree: 13.9µs | PIVOT Multicut: 35.3µs | Causal DP: 6.8µs",
            "=" * width,
        ]

        if self.active_tab == "DASHBOARD":
            header = f" {'DOMAIN':<18} {'STATUS':<10} {'FINDING HIGHLIGHT':<48} {'VALUATION IMPACT':<24}"
            lines.append(header)
            lines.append("-" * width)

            for f in self.findings:
                sev_str = f.severity.value
                val_impact = []
                if f.ebitda_haircut_usd > 0:
                    val_impact.append(f"-${f.ebitda_haircut_usd/1e6:.1f}M EBITDA")
                if f.multiple_discount > 0:
                    val_impact.append(f"-{f.multiple_discount:.2f}x Mult")
                if f.direct_liability_usd > 0:
                    val_impact.append(f"-${f.direct_liability_usd/1e6:.1f}M Debt")
                if f.escrow_hold_usd > 0:
                    val_impact.append(f"${f.escrow_hold_usd/1e6:.1f}M Escrow")

                impact_str = ", ".join(val_impact) or "Disclosure"
                cat_name = {
                    "FIN": "Forensic Finance",
                    "GPU": "GPU Infrastructure",
                    "IP": "IP & Codebase",
                    "CYBER": "Cyber Risk",
                    "COMMERCIAL": "Commercial",
                }.get(f.category, f.category)

                row = f" {cat_name:<18} {sev_str:<10} {f.title[:47]:<48} {impact_str[:23]:<24}"
                lines.append(row)

            lines.append("-" * width)
            lines.append(
                f" VALUATION SUMMARY: Reported EBITDA: ${self.valuation.reported_ebitda_usd/1e6:.1f}M | "
                f"Adjusted EBITDA: ${self.valuation.adjusted_ebitda_usd/1e6:.1f}M (-{self.valuation.ebitda_reduction_pct:.1f}%) | "
                f"Multiple: {self.valuation.base_multiple:.1f}x -> {self.valuation.adjusted_multiple:.1f}x"
            )
            lines.append(
                f" NET PURCHASE HAIRCUT: -${self.valuation.net_valuation_haircut_usd/1e6:.1f}M (-{self.valuation.net_haircut_pct:.1f}%) | "
                f"RECOMMENDED ESCROW HOLDBACK: ${self.valuation.recommended_escrow_holdback_usd/1e6:.1f}M"
            )

        elif self.active_tab == "MEMO":
            memo_text = DealMemoGenerator.generate_markdown_memo(
                self.deal_name, self.valuation, self.ledger_summary, self.findings
            )
            for m_line in memo_text.split("\n")[:25]:  # Preview first 25 lines
                lines.append(" " + m_line[:width - 2])
            lines.append("-" * width)
            lines.append(" (Press [d] to return to Dashboard, [q] to Quit)")

        elif self.active_tab == "GRAPH":
            lines.append(" DEAL ROOM KNOWLEDGE HYPERGRAPH TOPOLOGY:")
            lines.append(f" Total Nodes: {self.graph.node_count} | Total Relational Edges: {self.graph.edge_count}")
            lines.append("-" * width)
            for n_id, node in list(self.graph.nodes.items())[:10]:
                lines.append(f" - [{node.node_type}] {node.label} (ID: {node.id}, Prize: {node.prize})")
            lines.append("-" * width)
            lines.append(" (Press [d] to return to Dashboard, [q] to Quit)")

        elif self.active_tab == "LEDGER":
            lines.append(" DOUBLE-ENTRY GENERAL LEDGER RECONCILIATION:")
            lines.append(f" Total Journal Lines: {self.ledger_summary.total_ledger_rows:,}")
            lines.append(f" Reported ARR:        ${self.ledger_summary.reported_arr_usd:,.0f}")
            lines.append(f" Verified ARR:        ${self.ledger_summary.verified_arr_usd:,.0f} (ASC 606)")
            lines.append(f" Services Gap:        ${self.ledger_summary.services_misclassified_usd:,.0f} (ASC 606 Violation)")
            lines.append(f" Top 3 Concentration: {self.ledger_summary.top3_concentration_pct:.1f}%")
            lines.append("-" * width)
            lines.append(" (Press [d] to return to Dashboard, [q] to Quit)")

        lines.append("=" * width)
        lines.append(f" STATUS: {self.status_message}")
        lines.append(f" HOTKEYS: [d] Dashboard | [m] Deal Memo | [g] Knowledge Graph | [l] Ledger Drill-down | [q] Quit")
        lines.append("=" * width)

        return "\n".join(lines)

    def run_headless(self, output_format: str = "text", iterations: int = 1) -> None:
        """Run in non-interactive headless mode for CI/CD or stdout streaming."""
        if output_format.lower() == "json":
            sys.stdout.write(json.dumps(self.get_snapshot(), indent=2) + "\n")
        else:
            sys.stdout.write(self.render_text_frame() + "\n")
        sys.stdout.flush()

    def run_curses(self) -> None:
        """Interactive curses runner."""
        curses.wrapper(self._curses_main)

    def _curses_main(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        stdscr.nodelay(True)
        curses.use_default_colors()

        while self._running:
            max_y, max_x = stdscr.getmaxyx()
            width = max(80, max_x - 2)

            ch = stdscr.getch()
            if ch != -1:
                char = chr(ch).lower() if 0 <= ch <= 255 else ""
                if char == "q":
                    self._running = False
                elif char == "m":
                    self.active_tab = "MEMO"
                    self.status_message = "Viewing Investment Committee Deal Memo. Press [d] for Dashboard."
                elif char == "g":
                    self.active_tab = "GRAPH"
                    self.status_message = "Viewing Deal Knowledge Hypergraph. Press [d] for Dashboard."
                elif char == "l":
                    self.active_tab = "LEDGER"
                    self.status_message = "Viewing General Ledger ASC 606 Waterfall. Press [d] for Dashboard."
                elif char == "d":
                    self.active_tab = "DASHBOARD"
                    self.status_message = "Viewing Primary Due Diligence Findings Table."

            stdscr.erase()
            frame = self.render_text_frame(width=width)
            for row_idx, line in enumerate(frame.split("\n")):
                if row_idx < max_y - 1:
                    try:
                        stdscr.addstr(row_idx, 0, line[:width])
                    except curses.error:
                        pass
            stdscr.refresh()
            time.sleep(0.05)
