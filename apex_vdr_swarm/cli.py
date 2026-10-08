"""
Command Line Interface for apex-vdr-swarm (vdr-swarm / vdr-top).
"""

from __future__ import annotations

import argparse
import sys
import json

from apex_vdr_swarm import __version__
from apex_vdr_swarm.tui.app import VdrSwarmTuiApp
from apex_vdr_swarm.valuation.memo_generator import DealMemoGenerator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vdr-swarm",
        description="apex-vdr-swarm (`a2z-atlas-vdr`): Autonomous M&A Deal Room & Private Equity Due Diligence Swarm.",
        epilog="Apex Growth Systems LLC | a2zsoc.com | NVIDIA Inception Program Partner",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run non-interactively without curses (for CI/CD due diligence checks).",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format when running in --headless mode (default: text).",
    )
    parser.add_argument(
        "--deal",
        type=str,
        default="Project Atlas ($180M ARR)",
        help="Target company deal name.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Operational subcommands")

    audit_p = subparsers.add_parser("audit", help="Execute complete forensic audit")
    audit_p.add_argument("path", nargs="?", default=".", help="Path to VDR corpus directory")

    memo_p = subparsers.add_parser("memo", help="Generate Investment Committee Deal Memo")
    memo_p.add_argument("-o", "--output", help="Optional output file path")

    snap_p = subparsers.add_parser("snapshot", help="Output raw JSON telemetry snapshot")

    return parser


def main(args: list[str] | None = None) -> int:
    parser = build_parser()
    parsed = parser.parse_args(args)

    app = VdrSwarmTuiApp(deal_name=parsed.deal, demo_mode=True)

    if parsed.command == "memo":
        memo_md = DealMemoGenerator.generate_markdown_memo(
            parsed.deal, app.valuation, app.ledger_summary, app.findings
        )
        if parsed.output:
            with open(parsed.output, "w") as f:
                f.write(memo_md)
            print(f"[OK] Deal Memo saved to {parsed.output}")
        else:
            print(memo_md)
        return 0

    elif parsed.command == "snapshot":
        snap = app.get_snapshot()
        print(json.dumps(snap, indent=2))
        return 0

    # Main Audit / TUI runner
    if parsed.headless:
        app.run_headless(output_format=parsed.format, iterations=1)
    else:
        try:
            app.run_curses()
        except KeyboardInterrupt:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
