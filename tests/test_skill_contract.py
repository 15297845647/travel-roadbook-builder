from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_trigger_description_is_condition_only(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        description = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
        self.assertIsNotNone(description)
        self.assertTrue(description.group(1).startswith("Use when"))
        self.assertLess(len(description.group(1)), 500)

    def test_skill_defines_quick_and_roadbook_modes(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Quick mode", text)
        self.assertIn("Roadbook mode", text)
        self.assertIn("references/maps-and-transport.md", text)
        self.assertIn("references/plan-data-model.md", text)

    def test_map_workflow_requires_exact_leg_reconciliation(self) -> None:
        text = (ROOT / "references" / "maps-and-transport.md").read_text(encoding="utf-8")
        self.assertIn("exactly match the chronological travel block", text)
        self.assertIn("mixed modes", text)

    def test_template_has_map_slot_and_trip_timezone(self) -> None:
        text = (ROOT / "assets" / "roadbook-template.html").read_text(encoding="utf-8")
        self.assertIn("{{MAP_CONTENT}}", text)
        self.assertIn("{{MASTER_ROUTE_ROWS}}", text)
        self.assertIn("data-trip-timezone=", text)

    def test_countdown_uses_local_date_prefix_without_viewer_timezone_shift(self) -> None:
        text = (ROOT / "assets" / "roadbook-template.html").read_text(encoding="utf-8")
        self.assertIn(r"(?:T.*)?$/.exec(startEl.dataset.tripStart)", text)

    def test_provenance_record_exists(self) -> None:
        text = (ROOT / "references" / "provenance.md").read_text(encoding="utf-8")
        self.assertIn("independently authored", text)
        self.assertIn("No substantial expressive source code, prose, examples, or assets were copied", text)
        self.assertIn("Reviewed on: 2026-09-07", text)

    def test_documented_plan_example_passes_the_validator(self) -> None:
        text = (ROOT / "references" / "plan-data-model.md").read_text(encoding="utf-8")
        example = re.search(r"```json\n(.*?)\n```", text, re.DOTALL)
        self.assertIsNotNone(example)
        with tempfile.TemporaryDirectory() as directory:
            plan = Path(directory) / "plan.json"
            plan.write_text(example.group(1), encoding="utf-8")
            completed = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "validate_roadbook.py"), "--plan", str(plan)],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_delivery_spec_preserves_the_ready_gate(self) -> None:
        text = (ROOT / "references" / "deliverable-spec.md").read_text(encoding="utf-8")
        self.assertIn("## Delivery states", text)
        self.assertIn("## Final artifact choices", text)
        self.assertIn("does not bypass material-fact resolution or itinerary acceptance", text)
        self.assertIn("clearly labeled draft links", text)
        self.assertIn("Do not generate files merely because the plan is complete", text)

    def test_artifact_generation_requires_an_accepted_itinerary(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        planning = skill.index("**Planning**")
        ready = skill.index("**Ready**")
        generating = skill.index("**Generating**")
        self.assertLess(planning, ready)
        self.assertLess(ready, generating)
        self.assertIn("user has accepted the itinerary", skill)
        self.assertIn("never removes the need to settle material facts or obtain itinerary acceptance", skill)
        self.assertIn("without repeating the product-choice question", skill)

        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("只有行程事实一致并获确认后才制作最终文件", readme)
        self.assertIn("等待你确认完整行程后再生成文件", readme)

        agent_prompt = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("先核验并确认行程", agent_prompt)
        self.assertIn("若我已指定产物，只跳过重复选择", agent_prompt)

    def test_referenced_skill_files_exist(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        paths = set(re.findall(r"`((?:references|scripts|assets)/[^`]+)`", text))
        self.assertTrue(paths)
        self.assertEqual([], [path for path in sorted(paths) if not (ROOT / path).is_file()])


if __name__ == "__main__":
    unittest.main()
