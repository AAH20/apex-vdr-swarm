"""
VDR Corpus Loader & Document Manifest Ingestion.
Parses versioned Virtual Data Room documents based on the project-atlas-due-diligence standard.
"""

from __future__ import annotations

import os
import hashlib
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any


@dataclass
class VdrDocument:
    """An individual audited Virtual Data Room document."""
    id: str
    category: str  # Corporate, Commercial, Financial, IP_Tech, Infrastructure, Security, Legal
    title: str
    stage: str  # T0 (Initial IOI), T1 (Confirmatory), T2 (Closing Escrow)
    word_count: int
    content_summary: str
    sha256_hash: str
    flags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "category": self.category,
            "title": self.title,
            "stage": self.stage,
            "word_count": self.word_count,
            "content_summary": self.content_summary,
            "sha256_hash": self.sha256_hash,
            "flags": self.flags,
        }


class VdrCorpusLoader:
    """
    Ingests VDR folder structures. Defaults to high-fidelity Project Atlas benchmark:
    66 versioned documents spanning 7 core diligence categories.
    """

    CATEGORIES = [
        "Corporate",
        "Commercial",
        "Financial",
        "IP_Tech",
        "Infrastructure",
        "Security",
        "Legal",
    ]

    def __init__(self, demo_mode: bool = True):
        self.demo_mode = demo_mode
        self._documents: List[VdrDocument] = []
        if self.demo_mode:
            self._seed_atlas_benchmark()

    def _seed_atlas_benchmark(self) -> None:
        """Seed representative 66-document Project Atlas VDR benchmark."""
        docs_def = [
            ("VDR-CORP-01", "Corporate", "Articles of Incorporation & Entity Structure", "T0", 1450,
             "Delaware C-Corp with 6 international operating subsidiaries. Cross-border IP licensing agreements.", ["Cross-Border Tax"]),
            ("VDR-CORP-02", "Corporate", "Cap Table & Shareholder Option Grants", "T0", 920,
             "Common stock, Series A/B preferred. 1,200,000 unvested options. Co-Founder 2 left in 2023.", ["Unvested Drag"]),
            ("VDR-COMM-01", "Commercial", "Master Services Agreement (MSA) - Tier 1 Enterprise", "T0", 3800,
             "Top customer contract ($28M ARR). Contains strict 90-day termination for convenience clause.", ["Termination For Convenience", "High Concentration"]),
            ("VDR-COMM-02", "Commercial", "Top 10 Customer Schedule & Net Revenue Retention", "T1", 2100,
             "Top 3 customers account for 38.2% of total recognized revenue. NRR stated as 118%.", ["Customer Concentration > 35%"]),
            ("VDR-FIN-01", "Financial", "Audited Financial Statements (TTM & 3-Year Historical)", "T0", 6400,
             "Reported ARR: $180M. Recognized TTM Revenue: $202M. EBITDA reported at $42.0M.", ["Revenue Discrepancy"]),
            ("VDR-FIN-02", "Financial", "ASC 606 Revenue Recognition & Services SOW Ledgers", "T1", 4500,
             "Detailed breakdown: $22M one-time implementation services recognized as recurring software ARR.", ["ASC 606 Violation", "Critical Haircut"]),
            ("VDR-FIN-03", "Financial", "Customer Margin & Unit Economics Matrix", "T1", 3200,
             "Customer C-084 displays negative gross margin (-14%) due to unmetered GPU compute access.", ["Negative Contribution Margin"]),
            ("VDR-IP-01", "IP_Tech", "Proprietary Software Architecture & Repositories", "T0", 2900,
             "Core ML inference engine and orchestration pipeline. Monorepo architecture.", []),
            ("VDR-IP-02", "IP_Tech", "Third-Party & Open Source Software License Audit", "T1", 3100,
             "Scanning detected AGPL-3.0 copyleft dependency in backend data processing microservice.", ["Viral AGPL Contamination"]),
            ("VDR-IP-03", "IP_Tech", "Employee & Contractor IP Assignment Deeds", "T1", 1800,
             "Missing executed Proprietary Information & Inventions Agreement (PIIA) from Co-Founder 2.", ["Missing IP Assignment", "Title Cloud"]),
            ("VDR-INFRA-01", "Infrastructure", "Cloud Infrastructure & GPU Compute Lease Master Agreement", "T0", 4200,
             "3-Year non-cancelable reservation for 1,024 NVIDIA H100 SXM5 GPUs ($18.4M annual commitment).", ["Take-or-Pay Lease"]),
            ("VDR-INFRA-02", "Infrastructure", "GPU Cluster Telemetry & Active Tenant Utilization", "T1", 2600,
             "Telemetry shows actual average cluster utilization is 58.4%. Unabsorbed capacity drag: $1.8M/yr.", ["Unabsorbed GPU Drag"]),
            ("VDR-SEC-01", "Security", "SOC 2 Type II Examination Report", "T1", 5100,
             "Auditor opinion qualified due to 2 exceptions in change management and user deprovisioning.", ["Qualified SOC 2"]),
            ("VDR-SEC-02", "Security", "Third-Party Penetration Test & CVE Vulnerability Scan", "T1", 2400,
             "Identified 3 Critical CVEs (CVSS 9.8 Auth Bypass) and 8 High CVEs in customer portal.", ["Critical CVEs", "Direct Cyber Debt"]),
            ("VDR-LEG-01", "Legal", "Material Litigation, Regulatory Inquiries & Disclosures", "T0", 1900,
             "No ongoing federal litigation. Minor pending customer billing dispute in arbitration ($450k).", []),
            ("VDR-LEG-02", "Legal", "Proposed Reps & Warranties Indemnity Escrow Terms", "T2", 3400,
             "Seller proposes 5% indemnity escrow cap ($15.6M) with 12-month survival period.", ["Escrow Negotiation"]),
        ]

        # Expand to 66 documents across subcategories
        for i, (doc_id, cat, title, stage, words, summary, flags) in enumerate(docs_def):
            sha = hashlib.sha256(f"{doc_id}-{title}-{stage}".encode()).hexdigest()
            self._documents.append(
                VdrDocument(
                    id=doc_id,
                    category=cat,
                    title=title,
                    stage=stage,
                    word_count=words,
                    content_summary=summary,
                    sha256_hash=f"sha256:{sha}",
                    flags=flags,
                )
            )

        # Pad remaining documents to complete 66-doc institutional corpus
        current_count = len(self._documents)
        for idx in range(current_count + 1, 67):
            cat = self.CATEGORIES[idx % len(self.CATEGORIES)]
            doc_id = f"VDR-{cat[:4].upper()}-{idx:02d}"
            title = f"{cat} Operational Schedule & Supporting Annex #{idx}"
            sha = hashlib.sha256(f"{doc_id}-{title}".encode()).hexdigest()
            self._documents.append(
                VdrDocument(
                    id=doc_id,
                    category=cat,
                    title=title,
                    stage="T1" if idx % 2 == 0 else "T0",
                    word_count=1200 + (idx * 35),
                    content_summary=f"Supplemental operational diligence schedule for {cat} sub-process #{idx}.",
                    sha256_hash=f"sha256:{sha}",
                    flags=[],
                )
            )

    def load_documents(self) -> List[VdrDocument]:
        return list(self._documents)

    def get_flagged_documents(self) -> List[VdrDocument]:
        return [d for d in self._documents if d.flags]
