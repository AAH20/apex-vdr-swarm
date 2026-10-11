# `apex-vdr-swarm` (`a2z-atlas-vdr`)
### *The Autonomous M&A Deal Room & Private Equity Due Diligence Swarm*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Zero External Dependencies](https://img.shields.io/badge/dependencies-0%20(stdlib%20only)-success.svg)](https://github.com/AAH20/apex-vdr-swarm)
[![Apex Growth Systems LLC](https://img.shields.io/badge/Apex-Growth%20Systems%20LLC-emerald.svg)](https://a2zsoc.com)
[![NVIDIA Inception](https://img.shields.io/badge/NVIDIA%20Inception-Partner-76B900.svg)](https://www.nvidia.com/en-us/deep-learning-ai/startups/)

---

## 1. Overview & Problem Domain

In Private Equity (PE) buyouts, growth equity, and corporate M&A, acquiring an enterprise requires exhaustive technical, financial, and legal verification across the target company's **Virtual Data Room (VDR)**.

Today, this process remains fundamentally broken:
1. **Prohibitive Time & Cost**: PE firms (Blackstone, KKR, Thoma Bravo, Vista Equity) pay advisory firms (Big 4, Alvarez & Marsal, West Monroe, Crosslake) **$75,000 to $150,000 per deal** for 4 to 6 weeks of manual document reviews and subjective checklists.
2. **Hidden Balance Sheet Liabilities**:
   - **Revenue Classification Discrepancies**: Non-recurring professional services and pilot projects routinely disguised as recurring SaaS ARR to artificially inflate valuation multiples.
   - **Unabsorbed GPU / Compute Leases**: Targets entering multi-year, non-cancelable cloud commitments (e.g. 1,024 NVIDIA H100s) where tenant churn creates massive unabsorbed operational drag.
   - **Intellectual Property Contamination**: Undisclosed viral open-source licenses (AGPL-3.0/GPL-2.0) and missing founder IP assignment agreements that jeopardize software ownership.
   - **Cyber & Compliance Debt**: Unpatched critical CVEs, unhedged breach liability, and missing or qualified SOC 2 Type II audit opinions.

`apex-vdr-swarm` (`a2z-atlas-vdr`) is a self-contained GraphRAG multi-agent diligence engine: it ingests a VDR corpus and general-ledger data, runs specialist diligence agents, applies an EBITDA-haircut / valuation engine, and emits a Markdown Investment Committee deal memo. **In v1.0.0 the engine runs against a built-in synthetic "Project Atlas" benchmark (`demo_mode=True`); ingestion of real VDR/ledger inputs and integration with the `AAH20` sibling projects (`project-atlas-due-diligence`, `investor-os`, `ma_vdr_diligence_os`, `tech-balance-sheet`, `ApexGraphSwarm`, `graph-rag-np-hard-kernel`) is roadmap, not yet implemented.**

---

## 2. Archify Layered System Architecture

```mermaid
flowchart TB
    %% ==========================================
    %% apex-vdr-swarm ARCHIFY SYSTEM ARCHITECTURE
    %% Designed with diagram-design standards
    %% ==========================================

    subgraph L1_VDR ["LAYER 1: VDR FORENSIC INGESTION ENCLAVE"]
        direction TB
        VDR_CORPUS["Virtual Data Room Corpus (project-atlas-due-diligence)<br/>66 Versioned Documents | Corporate, Commercial, Finance, IP, Legal"]
        LEDGER_INGEST["Double-Entry General Ledger Ingestion<br/>107,358 Journal Rows | GAAP ASC 606 Revenue Recognition"]
        CODE_SCAN["Codebase AST & Git Forensics (tech-balance-sheet)<br/>License Scanner (AGPL/GPL) | Commit Churn | Bus Factor Risk"]
        VDR_CORPUS --- LEDGER_INGEST
        VDR_CORPUS --- CODE_SCAN
    end

    subgraph L2_KERNEL ["LAYER 2: GRAPHRAG HEURISTIC SOLVER CORE"]
        direction TB
        PCST_SOLVER["1. Evidence Subgraph Extractor (PCST-style)<br/>Greedy Dijkstra shortest-path connection of high-prize targets<br/>Extracts Minimal Evidence Subgraph Without Edge Explosion"]
        PIVOT_MULTICUT["2. Entity Correlation Clustering (PIVOT)<br/>Deterministic PIVOT greedy clustering<br/>Resolves Cross-Doc Entities (Subsidiaries, Shells, Customers)"]
        CAUSAL_DP["3. Causal Chain Validator<br/>Pairwise temporal-order comparison (not dynamic programming)<br/>Detects Revenue Front-Loading & Backdated Contracts"]
        SUBMOD_KNAP["4. Submodular Context Pruner<br/>Density-scaled greedy coverage selection"]
    end

    subgraph L3_SWARM ["LAYER 3: SPECIALIST DILIGENCE AGENT SWARM"]
        direction TB
        FIN_AGENT["Forensic Accounting Agent<br/>Reconciles ARR vs GAAP ASC 606 ($22M Services Misclassification)"]
        GPU_AGENT["GPU Infrastructure Agent<br/>Audits 1024 Leased H100s vs Utilization & Unabsorbed Drag"]
        IP_AGENT["IP & Software Architecture Agent<br/>Audits Copyleft Contamination & Missing Assignment Deeds"]
        CYBER_AGENT["Cyber Risk Actuary Agent (investor-os)<br/>Maps CVE Debt & SOC 2 Type II Exceptions to Dollar Liabilities"]
        CHAIR_AGENT["Investment Committee Chair Agent<br/>Synthesizes Defensible IC Memo & Reps/Warranties Escrow"]
    end

    subgraph L4_VALUATION ["LAYER 4: STATISTICALLY DEFENSIBLE VALUATION ENGINE"]
        direction TB
        EBITDA_HAIRCUT["EBITDA Valuation Haircut Calculator (ma_vdr_diligence_os)<br/>Adjusted EV = (Reported EBITDA - Drag) * Multiple - Liabilities"]
        ESCROW_MODEL["Reps & Warranties Escrow Sizing Model<br/>Calculates Indemnity Escrow Holdback for LOI Negotiation"]
        DEAL_MEMO["IC Deal Memo Generator<br/>Markdown memo only (`generate_markdown_memo`); PDF/JSON export is roadmap"]
        EBITDA_HAIRCUT --> ESCROW_MODEL
        ESCROW_MODEL --> DEAL_MEMO
    end

    subgraph L5_CONSOLE ["LAYER 5: INSTITUTIONAL CONSOLE & AUDIT RUNTIME"]
        direction TB
        VDR_TUI["Interactive Institutional Console (vdr-swarm)<br/>TUI Deal Room Monitor | Live Haircut Meter | Hotkey Navigation"]
        HEADLESS_STREAM["Headless CLI Output<br/>`--headless --format text|json` to stdout (no JSON-RPC / REST server)"]
        VDR_TUI --- HEADLESS_STREAM
    end

    %% Cross-Layer Interconnections
    L1_VDR ==>|"Deal Hypergraph Construction"| L2_KERNEL
    L2_KERNEL ==>|"High-SNR Knowledge Primitives"| L3_SWARM
    L3_SWARM ==>|"Material Findings & Risk Quantifications"| L4_VALUATION
    L4_VALUATION ==>|"Executive Memo & Balance Sheet"| L5_CONSOLE

    %% Diagram-Design High-Contrast Accessible Styling
    classDef vdrStyle fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef kernStyle fill:#1e1b4b,stroke:#818cf8,stroke-width:2px,color:#f8fafc;
    classDef swarmStyle fill:#14532d,stroke:#4ade80,stroke-width:2px,color:#f8fafc;
    classDef valStyle fill:#450a0a,stroke:#f87171,stroke-width:2px,color:#f8fafc;
    classDef conStyle fill:#1c1917,stroke:#fbbf24,stroke-width:2px,color:#f8fafc;

    class VDR_CORPUS,LEDGER_INGEST,CODE_SCAN vdrStyle;
    class PCST_SOLVER,PIVOT_MULTICUT,CAUSAL_DP,SUBMOD_KNAP kernStyle;
    class FIN_AGENT,GPU_AGENT,IP_AGENT,CYBER_AGENT,CHAIR_AGENT swarmStyle;
    class EBITDA_HAIRCUT,ESCROW_MODEL,DEAL_MEMO valStyle;
    class VDR_TUI,HEADLESS_STREAM conStyle;
```

---

## 3. Cross-Portfolio Integration Bus (`AAH20` Ecosystem)

> **Roadmap — not implemented in v1.0.0.** The ingestion modules in this repo return hardcoded `demo_mode=True` benchmark constants rather than parsing real VDR, ledger, or sibling-project inputs. There is no cross-repo integration bus, no external solver kernel, and no cryptographic audit trail in the code. The diagram below describes the intended target architecture.

```mermaid
flowchart LR
    %% ==========================================
    %% AAH20 PORTFOLIO INTEGRATION BUS
    %% ==========================================

    subgraph Diligence_Data ["VDR Datasets & Models"]
        direction TB
        ATLAS_VDR["project-atlas-due-diligence<br/>66 Docs | 107k Ledger Lines<br/>$180M ARR Benchmark"]
        INVESTOR_OS["investor-os & ma_vdr_diligence_os<br/>EBITDA Haircuts & Cyber Debt"]
        TECH_BS["tech-balance-sheet<br/>Code AST, Licenses & Bus Factor"]
    end

    subgraph Core_Engine ["apex-vdr-swarm Engine"]
        direction TB
        VDR_HUB["Diligence Swarm Orchestrator<br/>AAH20/apex-vdr-swarm"]
        HYPERGRAPH["Deal Room Hypergraph Store<br/>Cross-Modal Entity Relational Graph"]
        VDR_HUB --- HYPERGRAPH
    end

    subgraph Graph_Solvers ["Graph Intelligence & Kernels"]
        direction TB
        APEX_GRAPH["ApexGraphSwarm<br/>Multi-Agent GraphRAG Orchestration"]
        NP_KERNELS["graph-rag-np-hard-kernel<br/>External sibling project (roadmap)"]
    end

    subgraph Deliverables ["Institutional Outputs"]
        direction TB
        IC_MEMO["Investment Committee Deal Memo<br/>Adjusted EV, Haircuts & Escrow"]
        AUDIT_TRAIL["Deterministic CLI Output<br/>(no RFC 8785 / cryptographic receipt implemented)"]
    end

    ATLAS_VDR -->|"VDR Documents & Journal Lines"| VDR_HUB
    INVESTOR_OS -->|"EBITDA Haircut Actuarial Models"| VDR_HUB
    TECH_BS -->|"Software Balance Sheet Metrics"| VDR_HUB

    VDR_HUB <-->|"Graph Traversal & Subgraph Pruning"| APEX_GRAPH
    VDR_HUB <-->|"PCST, PIVOT, Causal DP & Submodular Pruning"| NP_KERNELS

    VDR_HUB ==>|"Generate Executable Diligence Pack"| IC_MEMO
    VDR_HUB ==>|"Emit Verifiable Audit Receipt"| AUDIT_TRAIL

    classDef dataStyle fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f0fdf4;
    classDef hubStyle fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc;
    classDef graphStyle fill:#312e81,stroke:#a5b4fc,stroke-width:2px,color:#e0e7ff;
    classDef outStyle fill:#451a03,stroke:#fcd34d,stroke-width:2px,color:#fffbeb;

    class ATLAS_VDR,INVESTOR_OS,TECH_BS dataStyle;
    class VDR_HUB,HYPERGRAPH hubStyle;
    class APEX_GRAPH,NP_KERNELS graphStyle;
    class IC_MEMO,AUDIT_TRAIL outStyle;
```

---

## 4. Autonomous Diligence Audit Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Partner as PE Deal Partner
    participant VDR as VDR Ingestion Layer
    participant Kernel as NP-Hard Graph Kernel
    participant Swarm as Diligence Agent Swarm
    participant Memo as Valuation & IC Memo Engine

    Partner->>VDR: Trigger Audit: audit_vdr(corpus_path)
    VDR->>VDR: Ingest 66 Docs + 107k Ledger Rows
    VDR->>Kernel: Construct Deal Hypergraph
    
    activate Kernel
    Kernel->>Kernel: Run PIVOT Multicut (Resolve 500 Customer Entities)
    Kernel->>Kernel: Run PCST (Extract 14 High-Prize Finding Subgraphs)
    Kernel->>Kernel: Run Causal DP (Detect Backdated Revenue Recognition)
    Kernel-->>Swarm: Emit Pruned, High-SNR Knowledge Subgraphs
    deactivate Kernel

    activate Swarm
    Swarm->>Swarm: ForensicAccountingAgent: Flag $22M Services ARR Discrepancy
    Swarm->>Swarm: GpuInfrastructureAgent: Flag 1024 Leased H100 Unabsorbed Drag
    Swarm->>Swarm: TechIpAgent: Flag Missing Founder IP Assignment Deed
    Swarm-->>Memo: Return Quantified Findings & Risk Deductions
    deactivate Swarm

    activate Memo
    Memo->>Memo: Calculate EBITDA Haircut: $42.0M to $28.4M (-32.4%)
    Memo->>Memo: Size Reps & Warranties Escrow: $12.5M Holdback
    Memo-->>Partner: Deliver Defensible IC Deal Memo & Valuation Table
    deactivate Memo
```

---

## 5. Mathematical Valuation Methodology Derived from Project Atlas

$$\text{Adjusted EV} = \left(\text{Reported EBITDA} - \Delta_{\text{Recurring}}\right) \times \left(\text{Base Multiple} - \sum \delta_{\text{Risk}}\right) - \sum \text{Direct Liabilities}$$

| Valuation Component | Atlas Diligence Reality | Mathematical Deduction Formula | Valuation Impact |
| :--- | :--- | :--- | :---: |
| **Recurring EBITDA Haircut ($\Delta_{\text{Recurring}}$)** | \$22M one-time implementation services disguised as recurring software ARR. | $\Delta_{\text{Recurring}} = \$22.0\text{M} \times (1 - 0.35) + \$1.8\text{M (GPU Drag)}$ | **-\$16.1M EBITDA reduction** |
| **Multiple Risk Discount ($\sum \delta_{\text{Risk}}$)** | Customer concentration $>35\%$ (Top 3 = 38.2%), missing SOC 2 Type II audit. | $\sum \delta = 0.75\times (\text{Concentration}) + 0.50\times (\text{SOC 2}) = 1.25\times$ | **Base $14.0\times \to 12.75\times$** |
| **Direct Balance Sheet Liabilities** | 1,024 leased H100s with unabsorbed tenant drain, unpatched critical CVEs. | $\text{Liabilities} = \text{CVE Remediation} + \text{Tenant Deficit} + \text{IP Holdback}$ | **-\$18.2M Direct Cash Deduction** |
| **Net Enterprise Value Adjustment** | Baseline \$588M Reported EV (at $14\times$ on \$42M EBITDA). | **Adjusted EV = $(\$42\text{M} - \$16.1\text{M}) \times 12.75 - \$18.2\text{M} = \$312.0\text{M}$** | **-\$276.0M Net Haircut (-46.9%)** |
| **Reps & Warranties Indemnity Escrow** | Missing IP assignment deed from Co-Founder 2 and patent indemnification risks. | $\text{Escrow} = \text{IP Holdback} (\$3.5\text{M}) + 5\%\text{ Deal Value } (\$15.6\text{M})$ | **\$19.1M Special Escrow Hold** |

---

## 6. Quickstart & Installation

### Zero-Dependency Instant Run (Python 3.10+)
`apex-vdr-swarm` runs directly with the Python standard library:

```bash
# Clone the repository
git clone https://github.com/AAH20/apex-vdr-swarm.git
cd apex-vdr-swarm

# Launch the interactive institutional console
python3 -m apex_vdr_swarm.cli

# Or generate the Investment Committee Deal Memo directly:
python3 -m apex_vdr_swarm.cli memo -o deal_memo.md
```

### Install CLI Globally
```bash
pip install -e .

# Launch using either command alias:
vdr-swarm
vdr-top
```

### Headless & CI/CD Streaming
```bash
# Output complete structured JSON due diligence snapshot
vdr-swarm --headless --format json | jq .valuation

# Plain text audit output
vdr-swarm --headless --format text
```

---

## 7. Performance Benchmarks

> **Illustrative sample output — not a committed or CI-verified benchmark result.** The figures below are sample values printed by `benchmarks/bench_solvers_latency.py` (run `make bench`); actual latencies vary by machine. The solver labels emitted by that script retain aspirational names; the descriptions in Section 2 reflect what the code actually does.

Sample run on macOS Darwin / Apple Silicon / Linux x86_64:

```text
=====================================================================================
 apex-vdr-swarm (`a2z-atlas-vdr`): Solver Latency Benchmark (sample output)
 Apex Growth Systems LLC | a2zsoc.com | NVIDIA Inception Program Partner
=====================================================================================

[1] Evidence Subgraph Extractor (PCST-style): 12.59 µs / query (greedy shortest-path)
[2] PIVOT Entity Resolution Multicut:          1.94 µs / resolution (greedy PIVOT clustering)
[3] Causal Chain Validator:                    1.24 µs / chain (pairwise temporal comparison)
[4] Submodular Context Pruner:                 3.26 µs / optimization (density-scaled greedy)

[5] Full Deal Room Audit & Haircut:           0.123 ms / complete deal (synthetic 66-doc benchmark)

=====================================================================================
 BENCHMARK SLA VERIFICATION:
 [✓] Sub-50µs Solver SLA: PASSED
 [✓] Sub-100ms Full Deal Valuation SLA: PASSED
=====================================================================================
```

---

## 8. License & Commercial Contact

Distributed under the **MIT License**.

- **Organization:** Apex Growth Systems LLC
- **Flagship Platform:** [a2zsoc.com](https://a2zsoc.com)
- **Founder & Managing Member:** Ahmed Hassan (`aah@a2zsoc.com`)
- **NVIDIA Inception Program Partner**
