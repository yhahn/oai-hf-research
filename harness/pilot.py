#!/usr/bin/env python3
"""sos-benchmarks pilot driver: run the arm x scenario x n matrix in parallel.

Resume-safe: skips jobs whose meta.json already exists.
"""

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).resolve().parent


def job(model, arm, scenario, i, out, max_turns, temperature, wall):
    stem = f"{scenario}-{arm}-{model}-r{i:02d}"
    if (Path(out) / f"{stem}.meta.json").exists():
        return f"skip {stem}"
    cmd = [sys.executable, str(HERE / "runner.py"), "--model", model, "--arm", arm,
           "--scenario", scenario, "--out", out, "--max-turns", str(max_turns),
           "--temperature", str(temperature), "--wall-seconds", str(wall),
           "--tag", f"r{i:02d}"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        return f"FAIL {stem}: {(r.stderr or r.stdout)[-300:]}"
    return f"ok {stem}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt-5.6-sol")
    ap.add_argument("--arms", default="A,B,D")
    ap.add_argument("--scenarios", default="S0,S1,S2,S3")
    ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default=str(HERE.parent / "runs"))
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--temperature", type=float, default=1.0)
    ap.add_argument("--wall", type=int, default=1800)
    args = ap.parse_args()

    arms = [a.strip() for a in args.arms.split(",")]
    scenarios = [s.strip() for s in args.scenarios.split(",")]
    jobs = [(args.model, arm, s, i, args.out, args.max_turns, args.temperature, args.wall)
            for arm in arms for s in scenarios for i in range(1, args.n + 1)]
    print(f"{len(jobs)} jobs, {args.workers} workers, temp={args.temperature}", flush=True)
    fails = 0
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for fut in as_completed([ex.submit(job, *j) for j in jobs]):
            line = fut.result()
            if line.startswith("FAIL"):
                fails += 1
            print(line, flush=True)
    print(f"pilot complete: {len(jobs)} jobs, {fails} failures", flush=True)


if __name__ == "__main__":
    main()
