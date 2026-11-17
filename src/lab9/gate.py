"""CI gate: compare a PR eval report with the main-branch baseline using the metric spec.

    python -m lab9.gate --pr reports/eval_workflow.json --baseline reports/baseline_v1.json

exit 0 = merge, exit 1 = blocked. Safety metrics: max 0, no averaging away.
Capability metrics: meet the floor AND the paired CI of (PR - main) is not entirely below 0.
Thresholds may only get stricter on the same eval-set version (ratchet).
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from lab8.console import utf8_stdio
from lab9 import stats
from lab9.eval import SPEC, load_spec, per_item
from lab9.graders import GRADERS


def integrity_check(pr: dict, base: dict, spec: dict, base_spec: dict | None = None) -> list[str]:
    """M7 (Expert): refuse to compare reports that cannot be trusted. Return a list of problems
    (empty = trustworthy). A gate that passes a broken report is worse than no gate.
    Must catch at least:
      - any metric value in pr["metrics"] that is NaN or inf
      - len(pr["rows"]) != manifest items x len(manifest seeds)   (dropped / duplicated rows)
      - the (item_id, seed) set of PR differs from the baseline's (cherry-picked seeds/items)
      - pr["evaluator_failures"] non-empty, or a row whose value for a graded spec metric is
        None (a crashed grader silently scores as "missing" and drops out of the mean)
      - base_spec given and a threshold in spec is LOOSER than in base_spec for the same
        eval-set version (ratchet: max may not rise, min may not fall, a blocking metric may
        not become non-blocking, a metric may not disappear; the same for spec["slices"],
        including dropping no_significant_drop)
      - an item's slice tags in PR rows differ from the baseline's (relabelling an item out of a
        slice hides its regression from the slice gate)"""
    problems: list[str] = []
    metrics = pr.get("metrics")
    if not isinstance(metrics, dict):
        problems.append("metrics is missing or not an object")
    else:
        for metric, value in metrics.items():
            if isinstance(value, (int, float)) and not math.isfinite(value):
                problems.append(f"metric {metric} is not finite")

    manifest = pr.get("manifest")
    if not isinstance(manifest, dict):
        problems.append("manifest is missing or not an object")
        manifest = {}
    if not isinstance(base.get("manifest"), dict):
        problems.append("baseline manifest is missing or not an object")
    rows = pr.get("rows")
    base_rows = base.get("rows")
    if not isinstance(rows, list) or not isinstance(base_rows, list):
        problems.append("rows is missing or not a list")
        rows = rows if isinstance(rows, list) else []
        base_rows = base_rows if isinstance(base_rows, list) else []

    seeds = manifest.get("seeds")
    item_count = manifest.get("items")
    if not isinstance(seeds, list) or isinstance(item_count, bool) or not isinstance(item_count, int) or item_count < 0:
        problems.append("manifest items or seeds is invalid")
    else:
        if any(isinstance(seed, bool) or not isinstance(seed, int) for seed in seeds):
            problems.append("manifest seeds must be integers")
        elif len(set(seeds)) != len(seeds):
            problems.append("manifest seeds contain duplicates")
        expected_count = item_count * len(seeds)
        if len(rows) != expected_count:
            problems.append(f"row count {len(rows)} != manifest {item_count} items x {len(seeds)} seeds")

    def row_keys(report_rows: list) -> tuple[set[tuple], bool]:
        keys = []
        valid = True
        for row in report_rows:
            if (not isinstance(row, dict) or not isinstance(row.get("item_id"), str)
                    or isinstance(row.get("seed"), bool) or not isinstance(row.get("seed"), int)):
                valid = False
                continue
            keys.append((row["item_id"], row["seed"]))
        return set(keys), valid and len(keys) == len(set(keys))

    pr_keys, pr_unique = row_keys(rows)
    base_keys, base_unique = row_keys(base_rows)
    if not pr_unique:
        problems.append("PR rows have invalid or duplicate (item_id, seed) keys")
    if not base_unique:
        problems.append("baseline rows have invalid or duplicate (item_id, seed) keys")
    if pr_keys != base_keys:
        problems.append("PR (item_id, seed) set differs from baseline")
    if isinstance(seeds, list) and all(isinstance(seed, int) and not isinstance(seed, bool) for seed in seeds):
        if {seed for _, seed in pr_keys} != set(seeds):
            problems.append("PR row seeds differ from manifest")
        if isinstance(item_count, int) and len({item_id for item_id, _ in pr_keys}) != item_count:
            problems.append("PR row item count differs from manifest")

    if pr.get("evaluator_failures"):
        problems.append("evaluator_failures is non-empty")
    metric_ids = {m.get("id") for m in spec.get("metrics", []) if m.get("id")}
    graded_ids = metric_ids & GRADERS.keys()
    for metric in metric_ids:
        if not isinstance(metrics, dict) or metric not in metrics:
            problems.append(f"metric {metric} is missing")
    for metric in graded_ids:
        if any(not isinstance(row, dict) or row.get(metric) is None for row in rows):
            problems.append(f"row metric {metric} is missing or None")

    def slices_by_item(report_rows: list, report_name: str) -> dict:
        by_item: dict[Any, tuple] = {}
        for row in report_rows:
            if not isinstance(row, dict) or row.get("item_id") is None:
                continue
            tags = row.get("slices") or []
            if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
                problems.append(f"{report_name} item {row['item_id']} has invalid slice tags")
                tags = []
            current = tuple(sorted(set(tags)))
            item_id = row["item_id"]
            if item_id in by_item and by_item[item_id] != current:
                problems.append(f"{report_name} item {item_id} has inconsistent slice tags across seeds")
            by_item[item_id] = current
        return by_item

    pr_slices = slices_by_item(rows, "PR")
    base_slices = slices_by_item(base_rows, "baseline")
    if pr_slices != base_slices:
        problems.append("item slice tags differ from baseline")

    if base_spec and spec.get("eval_set_version") == base_spec.get("eval_set_version"):
        current_metrics = {m.get("id"): m for m in spec.get("metrics", []) if m.get("id")}
        for old in base_spec.get("metrics", []):
            metric_id = old.get("id")
            new = current_metrics.get(metric_id)
            if new is None:
                problems.append(f"ratchet removed metric {metric_id}")
                continue
            old_threshold = old.get("threshold") or {}
            new_threshold = new.get("threshold") or {}
            for key, old_value in old_threshold.items():
                if key not in new_threshold:
                    if key != "no_significant_drop" or old_value:
                        problems.append(f"ratchet removed {key} threshold from {metric_id}")
                elif key == "max" and new_threshold[key] > old_value:
                    problems.append(f"ratchet loosened {metric_id} max threshold")
                elif key in ("min", "max_increase") and new_threshold[key] < old_value:
                    problems.append(f"ratchet loosened {metric_id} {key} threshold")
                elif key == "no_significant_drop" and old_value and not new_threshold[key]:
                    problems.append(f"ratchet removed no_significant_drop from {metric_id}")
            if old.get("blocking") and not new.get("blocking"):
                problems.append(f"ratchet made {metric_id} non-blocking")

        current_slices = {(s.get("name"), s.get("metric")): s for s in spec.get("slices", [])}
        for old in base_spec.get("slices", []):
            key = (old.get("name"), old.get("metric"))
            new = current_slices.get(key)
            if new is None:
                problems.append(f"ratchet removed slice {key[0]}/{key[1]}")
                continue
            for threshold in ("min", "max"):
                if threshold in old:
                    if threshold not in new:
                        problems.append(f"ratchet removed {threshold} threshold from slice {key[0]}/{key[1]}")
                    elif threshold == "min" and new[threshold] < old[threshold]:
                        problems.append(f"ratchet loosened slice {key[0]}/{key[1]} min threshold")
                    elif threshold == "max" and new[threshold] > old[threshold]:
                        problems.append(f"ratchet loosened slice {key[0]}/{key[1]} max threshold")
            if old.get("no_significant_drop") and not new.get("no_significant_drop"):
                problems.append(f"ratchet removed no_significant_drop from slice {key[0]}/{key[1]}")
            if old.get("blocking") and not new.get("blocking"):
                problems.append(f"ratchet made slice {key[0]}/{key[1]} non-blocking")
    return problems


def slice_check(pr: dict, base: dict, spec: dict) -> tuple[list[str], list[str]]:
    """Block floor or paired-CI regressions on important item slices."""
    blocked, lines = [], []
    bootstrap = spec.get("bootstrap", {})
    for item in spec.get("slices", []):
        name, metric = item["name"], item["metric"]
        current = per_item(pr, metric, slice_name=name)
        baseline = per_item(base, metric, slice_name=name)
        keys = sorted(set(current) & set(baseline))
        value = sum(current.values()) / len(current) if current else None
        verdict, note = "ok", ""
        if not keys:
            verdict = "missing"
        elif "min" in item and (value is None or value < item["min"]):
            verdict = "fail"
        if item.get("no_significant_drop") and keys:
            delta, lo, hi = stats.paired_bootstrap(
                [current[k] for k in keys], [baseline[k] for k in keys],
                n_resamples=bootstrap.get("n_resamples", 1000), rng=bootstrap.get("rng", 2027),
                confidence=bootstrap.get("confidence", 0.95),
            )
            note = f"Δ {delta:+.3f} CI [{lo:+.3f}, {hi:+.3f}]"
            if hi < 0:
                verdict = "fail"
        if verdict != "ok" and item.get("blocking"):
            blocked.append(f"slice:{name}/{metric}")
        label = "ok" if verdict == "ok" else ("MISSING" if verdict == "missing" else
                                                   "BLOCK" if item.get("blocking") else "warn")
        lines.append(f"  slice:{name}/{metric:<16} {value!s:<8} {note:<28} {label}")
    return blocked, lines


def check(pr: dict, base: dict, spec: dict, base_spec: dict | None = None) -> tuple[list[str], list[str]]:
    pr_manifest = pr.get("manifest")
    base_manifest = base.get("manifest")
    if not isinstance(pr_manifest, dict) or not isinstance(base_manifest, dict):
        return ["integrity"], ["  INTEGRITY report manifest is missing or invalid"]
    if not pr_manifest.get("eval_set_sha") or not base_manifest.get("eval_set_sha"):
        return ["integrity"], ["  INTEGRITY eval_set_sha is missing"]
    if pr_manifest["eval_set_sha"] != base_manifest["eval_set_sha"]:
        return ["eval_set_sha"], ["  EVAL SET differs from the baseline's: re-run the baseline on the same eval set"]
    problems = integrity_check(pr, base, spec, base_spec)
    if problems:
        return ["integrity"], [f"  INTEGRITY {p}" for p in problems]
    blocked, lines = [], []
    bs = spec.get("bootstrap", {})
    for m in spec["metrics"]:
        mid, th, val = m["id"], m.get("threshold", {}), pr["metrics"].get(m["id"])
        verdict, note = "ok", ""
        if val is None:
            verdict = "missing"
        elif "max" in th and val > th["max"]:
            verdict = "fail"
        elif "min" in th and val < th["min"]:
            verdict = "fail"
        elif "max_increase" in th and base["metrics"].get(mid):
            if val > base["metrics"][mid] * (1 + th["max_increase"]):
                verdict = "fail"
        if th.get("no_significant_drop") and val is not None:
            a, b = per_item(pr, mid), per_item(base, mid)
            keys = sorted(set(a) & set(b))
            d, lo, hi = stats.paired_bootstrap([a[k] for k in keys], [b[k] for k in keys],
                                               n_resamples=bs.get("n_resamples", 1000), rng=bs.get("rng", 2027))
            note = f"Δ {d:+.3f} CI [{lo:+.3f}, {hi:+.3f}]"
            if hi < 0:
                verdict = "fail"
        if verdict != "ok" and m.get("blocking"):
            blocked.append(mid)
        label = {"ok": "ok", "missing": "MISSING"}.get(verdict, "BLOCK" if m.get("blocking") else "warn")
        lines.append(f"  {mid:<22} {val!s:<8} {json.dumps(th):<40} {note:<28} {label}")
    if spec.get("slices"):
        sb, sl = slice_check(pr, base, spec)
        blocked += sb
        lines += sl
    return blocked, lines


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(prog="lab9.gate")
    ap.add_argument("--pr", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--spec", default=str(SPEC))
    ap.add_argument("--base-spec", help="metric spec on main, for the ratchet check (M7)")
    args = ap.parse_args(argv)
    pr = json.loads(Path(args.pr).read_text(encoding="utf-8"))
    base = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    base_spec = load_spec(Path(args.base_spec)) if args.base_spec else None
    blocked, lines = check(pr, base, load_spec(Path(args.spec)), base_spec)
    pr_manifest = pr.get("manifest") or {}
    print(f"gate: PR {pr.get('run_id', '<unknown>')} vs main {base.get('run_id', '<unknown>')} "
          f"· eval set {pr_manifest.get('eval_set_sha', '<missing>')}")
    print("\n".join(lines))
    if blocked:
        print(f"exit 1 — blocked: {', '.join(blocked)}")
        return 1
    print("exit 0 — merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
