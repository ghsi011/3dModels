#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import trimesh

SCHEMA_VERSION = 4
TOOL_VERSION = "1.0"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def load_single_mesh(path: Path) -> trimesh.Trimesh:
    loaded = trimesh.load(path, force="mesh", process=True)
    if not isinstance(loaded, trimesh.Trimesh):
        raise ValueError(f"{path}: did not load as one mesh")
    return loaded


def indexed_rows(
    rows: Any,
    *,
    label: str,
) -> dict[str, dict[str, Any]]:
    if not isinstance(rows, list):
        raise ValueError(f"{label}: expected a list")
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str):
            raise ValueError(f"{label}: every row needs a string id")
        row_id = row["id"]
        if row_id in indexed:
            raise ValueError(f"{label}: duplicate id {row_id}")
        indexed[row_id] = row
    return indexed


def support_audit(
    *,
    stl_path: Path,
    plan_path: Path,
    rule_id: str,
) -> tuple[dict[str, Any], float]:
    plan = load_json(plan_path)
    rules = indexed_rows(plan.get("support_rules"), label="support_rules")
    if rule_id not in rules:
        raise ValueError(f"support_rules: missing id {rule_id}")
    rule = rules[rule_id]

    matrix = np.asarray(rule.get("model_to_printer_matrix"), dtype=float)
    if matrix.shape != (4, 4):
        raise ValueError(f"{rule_id}: model_to_printer_matrix must be 4x4")
    bed_z = float(rule.get("bed_z_mm"))
    bed_tolerance = float(rule.get("bed_tolerance_mm"))
    downward_normal_z_max = float(rule.get("downward_normal_z_max"))
    maximum_area = float(rule.get("max_out_of_limit_area_mm2"))

    mesh = load_single_mesh(stl_path)
    vertices = trimesh.transform_points(mesh.vertices, matrix)
    triangles = vertices[mesh.faces]
    edges_a = triangles[:, 1] - triangles[:, 0]
    edges_b = triangles[:, 2] - triangles[:, 0]
    crosses = np.cross(edges_a, edges_b)
    double_areas = np.linalg.norm(crosses, axis=1)
    valid = double_areas > 1e-12
    normals = np.zeros_like(crosses)
    normals[valid] = crosses[valid] / double_areas[valid, None]
    areas = double_areas * 0.5

    bed_contact = (
        np.max(np.abs(triangles[:, :, 2] - bed_z), axis=1) <= bed_tolerance
    )
    downward = normals[:, 2] <= downward_normal_z_max
    out_of_limit = valid & downward & ~bed_contact
    out_of_limit_area = float(areas[out_of_limit].sum())

    result = {
        "schema_version": SCHEMA_VERSION,
        "tool": "team_preflight.py",
        "tool_version": TOOL_VERSION,
        "kind": "support-audit",
        "stl_path": stl_path.name,
        "stl_sha256": sha256_file(stl_path),
        "plan_checks_sha256": sha256_file(plan_path),
        "rule_id": rule_id,
        "matrix_sha256": canonical_sha256(rule["model_to_printer_matrix"]),
        "disposition": rule.get("disposition"),
        "bed_z_mm": bed_z,
        "bed_tolerance_mm": bed_tolerance,
        "downward_normal_z_max": downward_normal_z_max,
        "bed_contact_area_mm2": float(areas[valid & bed_contact].sum()),
        "out_of_limit_faces": int(np.count_nonzero(out_of_limit)),
        "out_of_limit_area_mm2": out_of_limit_area,
        "max_out_of_limit_area_mm2": maximum_area,
        "result": "PASS" if out_of_limit_area <= maximum_area + 1e-9 else "FAIL",
    }
    return result, maximum_area


def validate_receipts(
    *,
    stl_path: Path,
    plan_path: Path,
    readiness_path: Path,
) -> dict[str, Any]:
    plan = load_json(plan_path)
    readiness = load_json(readiness_path)
    errors: list[str] = []

    if plan.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"plan schema_version must be {SCHEMA_VERSION}")
    if readiness.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"readiness schema_version must be {SCHEMA_VERSION}")

    stl_sha = sha256_file(stl_path)
    plan_sha = sha256_file(plan_path)
    if readiness.get("candidate_stl_sha256") != stl_sha:
        errors.append("candidate_stl_sha256 does not match the exported STL")
    if readiness.get("print_plan_checks_sha256") != plan_sha:
        errors.append("print_plan_checks_sha256 does not match the plan checks file")

    plan_edges = indexed_rows(plan.get("edges"), label="plan edges")
    ready_edges = indexed_rows(readiness.get("edges"), label="readiness edges")
    if set(plan_edges) != set(ready_edges):
        errors.append(
            "edge ID set mismatch: "
            f"missing={sorted(set(plan_edges) - set(ready_edges))}, "
            f"extra={sorted(set(ready_edges) - set(plan_edges))}"
        )
    for edge_id in sorted(set(plan_edges) & set(ready_edges)):
        expected = plan_edges[edge_id]
        observed = ready_edges[edge_id]
        samples = observed.get("samples_mm")
        if not isinstance(samples, list) or not all(
            isinstance(value, (int, float)) for value in samples
        ):
            errors.append(f"{edge_id}: samples_mm must be a numeric list")
            continue
        required_samples = int(expected.get("samples_required", 3))
        if len(samples) < required_samples:
            errors.append(
                f"{edge_id}: needs {required_samples} samples, found {len(samples)}"
            )
            continue
        if expected.get("allowed_sharp") is True:
            if not expected.get("allowed_sharp_reason"):
                errors.append(f"{edge_id}: allowed sharp edge needs a plan reason")
            continue
        minimum = float(expected.get("min_radius_mm"))
        maximum_value = expected.get("max_radius_mm")
        observed_min = min(float(value) for value in samples)
        observed_max = max(float(value) for value in samples)
        if observed_min + 1e-9 < minimum:
            errors.append(
                f"{edge_id}: radius {observed_min:.6f} below {minimum:.6f} mm"
            )
        if maximum_value is not None and observed_max - 1e-9 > float(maximum_value):
            errors.append(
                f"{edge_id}: radius {observed_max:.6f} above "
                f"{float(maximum_value):.6f} mm"
            )
        if not observed.get("method") or not observed.get("evidence"):
            errors.append(f"{edge_id}: method and evidence are required")

    plan_support = indexed_rows(plan.get("support_rules"), label="plan support_rules")
    ready_support = indexed_rows(
        readiness.get("support_rules"), label="readiness support_rules"
    )
    if set(plan_support) != set(ready_support):
        errors.append(
            "support-rule ID set mismatch: "
            f"missing={sorted(set(plan_support) - set(ready_support))}, "
            f"extra={sorted(set(ready_support) - set(plan_support))}"
        )
    for rule_id in sorted(set(plan_support) & set(ready_support)):
        expected = plan_support[rule_id]
        observed = ready_support[rule_id]
        audit_value = observed.get("audit_path")
        if not isinstance(audit_value, str):
            errors.append(f"{rule_id}: audit_path is required")
            continue
        audit_path = (readiness_path.parent / audit_value).resolve()
        if not audit_path.is_file():
            errors.append(f"{rule_id}: missing audit file {audit_value}")
            continue
        audit = load_json(audit_path)
        if audit.get("tool") != "team_preflight.py":
            errors.append(f"{rule_id}: audit must come from team_preflight.py")
        if audit.get("stl_sha256") != stl_sha:
            errors.append(f"{rule_id}: audit STL hash mismatch")
        if audit.get("plan_checks_sha256") != plan_sha:
            errors.append(f"{rule_id}: audit plan hash mismatch")
        if audit.get("rule_id") != rule_id:
            errors.append(f"{rule_id}: audit rule ID mismatch")
        if audit.get("matrix_sha256") != canonical_sha256(
            expected.get("model_to_printer_matrix")
        ):
            errors.append(f"{rule_id}: transform hash mismatch")
        observed_area = float(audit.get("out_of_limit_area_mm2", float("inf")))
        maximum_area = float(expected.get("max_out_of_limit_area_mm2"))
        if expected.get("disposition") == "SELF_SUPPORT_REQUIRED":
            if observed_area > maximum_area + 1e-9:
                errors.append(
                    f"{rule_id}: {observed_area:.6f} mm2 exceeds "
                    f"{maximum_area:.6f} mm2"
                )
        elif expected.get("disposition") == "SUPPORT_ALLOWED":
            if not expected.get("allowed_contact_class"):
                errors.append(f"{rule_id}: SUPPORT_ALLOWED needs allowed_contact_class")
            if observed.get("forbidden_faces_checked") is not True:
                errors.append(f"{rule_id}: forbidden faces were not checked")
        else:
            errors.append(f"{rule_id}: unknown disposition")

    return {
        "schema_version": SCHEMA_VERSION,
        "tool": "team_preflight.py",
        "tool_version": TOOL_VERSION,
        "kind": "receipt-validation",
        "candidate_stl_sha256": stl_sha,
        "print_plan_checks_sha256": plan_sha,
        "edge_ids": sorted(plan_edges),
        "support_rule_ids": sorted(plan_support),
        "errors": errors,
        "result": "PASS" if not errors else "FAIL",
    }


def write_result(result: dict[str, Any], output: Path | None) -> None:
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output is None:
        sys.stdout.write(payload)
    else:
        output.write_text(payload, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run deterministic team-pipeline non-acceptance gates."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    support = subparsers.add_parser(
        "support-audit",
        help="Measure transformed non-bed downward area on a re-imported STL.",
    )
    support.add_argument("--stl", required=True, type=Path)
    support.add_argument("--plan", required=True, type=Path)
    support.add_argument("--rule-id", required=True)
    support.add_argument("--output", type=Path)

    validate = subparsers.add_parser(
        "validate-receipts",
        help="Validate hashes and complete edge/support ID coverage.",
    )
    validate.add_argument("--stl", required=True, type=Path)
    validate.add_argument("--plan", required=True, type=Path)
    validate.add_argument("--readiness", required=True, type=Path)
    validate.add_argument("--output", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "support-audit":
            result, _ = support_audit(
                stl_path=args.stl.resolve(),
                plan_path=args.plan.resolve(),
                rule_id=args.rule_id,
            )
        else:
            result = validate_receipts(
                stl_path=args.stl.resolve(),
                plan_path=args.plan.resolve(),
                readiness_path=args.readiness.resolve(),
            )
        write_result(result, args.output.resolve() if args.output else None)
        return 0 if result["result"] == "PASS" else 1
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as error:
        sys.stderr.write(f"team_preflight: {error}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
