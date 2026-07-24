#!/usr/bin/env python3
"""Bounded CAD subprocess runner (round-5 H3 stall-prevention harness).

Runs one CAD/measurement script as an isolated subprocess with a wall-clock timeout
and an RSS memory cap, after saving the exact source it ran. Kills the whole process
tree on breach so a non-converging or runaway build can never silently occupy the
session. Interpreter-agnostic: point --interp at the build123d venv python for
authoring, or the system python for measurement/gates.

Usage:
  python cad_runner.py --interp <python.exe> --script model.py \
      --timeout 120 --mem-mb 4000 [--label build] [--workdir DIR] [-- ARGS...]

Exit code = child's exit code, or 124 (timeout), 137 (memory kill), 2 (harness error).
Writes <label>.run.json next to the script with source hash, elapsed, peak RSS, outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

try:
    import psutil
except Exception:  # pragma: no cover
    psutil = None


def tree_rss_mb(proc: "psutil.Process") -> float:
    total = 0
    try:
        procs = [proc] + proc.children(recursive=True)
    except Exception:
        procs = [proc]
    for p in procs:
        try:
            total += p.memory_info().rss
        except Exception:
            pass
    return total / (1024 * 1024)


def kill_tree(proc: "psutil.Process") -> None:
    try:
        victims = proc.children(recursive=True) + [proc]
    except Exception:
        victims = [proc]
    for p in victims:
        try:
            p.kill()
        except Exception:
            pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--interp", required=True, help="python interpreter to run the script")
    ap.add_argument("--script", required=True, type=Path)
    ap.add_argument("--timeout", type=float, default=120.0, help="wall-clock seconds")
    ap.add_argument("--mem-mb", type=float, default=4000.0, help="RSS cap (MB) across tree")
    ap.add_argument("--label", default="run")
    ap.add_argument("--workdir", type=Path, default=None)
    ap.add_argument("rest", nargs=argparse.REMAINDER, help="args after -- passed to the script")
    args = ap.parse_args()

    script = args.script.resolve()
    if not script.is_file():
        sys.stderr.write(f"cad_runner: no such script {script}\n")
        return 2
    workdir = (args.workdir or script.parent).resolve()
    src = script.read_bytes()
    src_sha = hashlib.sha256(src).hexdigest()
    passthrough = [a for a in args.rest if a != "--"]

    start = time.time()
    proc = subprocess.Popen(
        [args.interp, str(script), *passthrough],
        cwd=str(workdir),
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    ps = psutil.Process(proc.pid) if psutil else None
    peak = 0.0
    reason = "ok"
    while True:
        rc = proc.poll()
        if rc is not None:
            break
        if ps is not None:
            peak = max(peak, tree_rss_mb(ps))
            if peak > args.mem_mb:
                reason = "memory"
                kill_tree(ps)
                proc.wait()
                rc = 137
                break
        if time.time() - start > args.timeout:
            reason = "timeout"
            if ps is not None:
                kill_tree(ps)
            else:
                proc.kill()
            proc.wait()
            rc = 124
            break
        time.sleep(0.2)

    elapsed = round(time.time() - start, 3)
    if rc is None:
        rc = proc.returncode if proc.returncode is not None else 2
    receipt = {
        "label": args.label,
        "script": str(script.name),
        "script_sha256": src_sha,
        "interp": args.interp,
        "args": passthrough,
        "exit_code": rc,
        "elapsed_s": elapsed,
        "peak_rss_mb": round(peak, 1),
        "timeout_s": args.timeout,
        "mem_cap_mb": args.mem_mb,
        "outcome": reason if reason != "ok" else ("ok" if rc == 0 else "nonzero_exit"),
        "psutil": psutil is not None,
    }
    (workdir / f"{args.label}.run.json").write_text(
        json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
    )
    sys.stderr.write(
        f"cad_runner[{args.label}]: exit={rc} elapsed={elapsed}s peak={peak:.0f}MB reason={reason}\n"
    )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
