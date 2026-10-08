"""Unit tests for TUI Console and CLI entry points."""

import unittest
import json
from apex_vdr_swarm.tui.app import VdrSwarmTuiApp
from apex_vdr_swarm.cli import main, build_parser


class TestTuiAndCli(unittest.TestCase):
    def setUp(self):
        self.app = VdrSwarmTuiApp(deal_name="Project Atlas Test", demo_mode=True)

    def test_app_snapshot(self):
        snap = self.app.get_snapshot()
        self.assertEqual(snap["deal_name"], "Project Atlas Test")
        self.assertIn("vdr_documents_count", snap)
        self.assertEqual(snap["vdr_documents_count"], 66)
        self.assertIn("valuation", snap)
        self.assertIn("findings", snap)
        self.assertGreaterEqual(len(snap["findings"]), 5)

    def test_render_all_tabs(self):
        for tab in ["DASHBOARD", "MEMO", "GRAPH", "LEDGER"]:
            self.app.active_tab = tab
            frame = self.app.render_text_frame(width=100)
            self.assertIn("apex-vdr-swarm", frame)
            self.assertIn("Project Atlas Test", frame)
            self.assertIn("STATUS:", frame)
            self.assertIn("HOTKEYS:", frame)

    def test_cli_parser(self):
        parser = build_parser()
        args = parser.parse_args(["--headless", "--format", "json"])
        self.assertTrue(args.headless)
        self.assertEqual(args.format, "json")

    def test_cli_snapshot_command(self):
        ret = main(["snapshot"])
        self.assertEqual(ret, 0)

    def test_cli_memo_command(self):
        ret = main(["memo"])
        self.assertEqual(ret, 0)

    def test_cli_headless_text(self):
        ret = main(["--headless", "--format", "text"])
        self.assertEqual(ret, 0)


if __name__ == "__main__":
    unittest.main()
