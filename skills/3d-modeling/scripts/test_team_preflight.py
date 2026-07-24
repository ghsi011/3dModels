from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import trimesh

import team_preflight


class TeamPreflightTest(unittest.TestCase):
    def write_plan(self, directory: Path) -> Path:
        plan = {
            "schema_version": 4,
            "candidate_predicate_revision": 1,
            "edges": [
                {
                    "id": "E-01",
                    "min_radius_mm": 0.4,
                    "max_radius_mm": 0.8,
                    "samples_required": 3,
                },
                {
                    "id": "E-02",
                    "allowed_sharp": True,
                    "allowed_sharp_reason": "hidden datum edge",
                    "samples_required": 3,
                },
            ],
            "support_rules": [
                {
                    "id": "S-01",
                    "disposition": "SELF_SUPPORT_REQUIRED",
                    "model_to_printer_matrix": [
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 1],
                        [0, 0, 0, 1],
                    ],
                    "bed_z_mm": 0,
                    "bed_tolerance_mm": 0.001,
                    "downward_normal_z_max": -0.7,
                    "max_out_of_limit_area_mm2": 0.0,
                }
            ],
        }
        path = directory / "print_plan_checks.json"
        path.write_text(json.dumps(plan), encoding="utf-8")
        return path

    def test_box_on_bed_has_zero_out_of_limit_area(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)

            result, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            self.assertEqual(result["result"], "PASS")
            self.assertAlmostEqual(result["out_of_limit_area_mm2"], 0.0, places=6)

    def test_elevated_plate_fails_support_audit(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "overhang.stl"
            base = trimesh.creation.box(extents=(1, 1, 2))
            plate = trimesh.creation.box(extents=(4, 4, 0.2))
            plate.apply_translation((0, 0, 2))
            trimesh.util.concatenate((base, plate)).export(stl_path)
            plan_path = self.write_plan(directory)

            result, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            self.assertEqual(result["result"], "FAIL")
            self.assertGreater(result["out_of_limit_area_mm2"], 10.0)

    def test_receipt_validator_rejects_missing_edge(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)
            audit, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            audit_path = directory / "support_audit.json"
            audit_path.write_text(json.dumps(audit), encoding="utf-8")
            readiness = {
                "schema_version": 4,
                "candidate_stl_sha256": team_preflight.sha256_file(stl_path),
                "print_plan_checks_sha256": team_preflight.sha256_file(plan_path),
                "edges": [
                    {
                        "id": "E-01",
                        "samples_mm": [0.5, 0.5, 0.5],
                        "method": "section fit",
                        "evidence": "edge.png",
                    }
                ],
                "support_rules": [
                    {
                        "id": "S-01",
                        "audit_path": audit_path.name,
                        "forbidden_faces_checked": True,
                    }
                ],
            }
            readiness_path = directory / "candidate_preflight.json"
            readiness_path.write_text(json.dumps(readiness), encoding="utf-8")

            result = team_preflight.validate_receipts(
                stl_path=stl_path,
                plan_path=plan_path,
                readiness_path=readiness_path,
            )
            self.assertEqual(result["result"], "FAIL")
            self.assertTrue(
                any("edge ID set mismatch" in error for error in result["errors"])
            )

    def test_receipt_validator_accepts_complete_rows(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)
            audit, _ = team_preflight.support_audit(
                stl_path=stl_path,
                plan_path=plan_path,
                rule_id="S-01",
            )
            audit_path = directory / "support_audit.json"
            audit_path.write_text(json.dumps(audit), encoding="utf-8")
            readiness = {
                "schema_version": 4,
                "candidate_stl_sha256": team_preflight.sha256_file(stl_path),
                "print_plan_checks_sha256": team_preflight.sha256_file(plan_path),
                "edges": [
                    {
                        "id": "E-01",
                        "samples_mm": [0.5, 0.6, 0.7],
                        "method": "section fit",
                        "evidence": "edge.png",
                    },
                    {
                        "id": "E-02",
                        "samples_mm": [0.0, 0.0, 0.0],
                        "method": "declared sharp",
                        "evidence": "hidden edge",
                    },
                ],
                "support_rules": [
                    {
                        "id": "S-01",
                        "audit_path": audit_path.name,
                        "forbidden_faces_checked": True,
                    }
                ],
            }
            readiness_path = directory / "candidate_preflight.json"
            readiness_path.write_text(json.dumps(readiness), encoding="utf-8")

            result = team_preflight.validate_receipts(
                stl_path=stl_path,
                plan_path=plan_path,
                readiness_path=readiness_path,
            )
            self.assertEqual(result["result"], "PASS", result["errors"])

    def test_support_audit_cli(self) -> None:
        with tempfile.TemporaryDirectory() as raw_directory:
            directory = Path(raw_directory)
            stl_path = directory / "box.stl"
            trimesh.creation.box(extents=(2, 2, 2)).export(stl_path)
            plan_path = self.write_plan(directory)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(Path(team_preflight.__file__)),
                    "support-audit",
                    "--stl",
                    str(stl_path),
                    "--plan",
                    str(plan_path),
                    "--rule-id",
                    "S-01",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
