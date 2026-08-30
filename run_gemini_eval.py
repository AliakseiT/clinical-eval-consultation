#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Real-model evaluation: validate + compare Gemini 2.5, 3.5, and 3.7 on the consultation casebank.

Runs `gemini_compare_all` (gemini-2.5-flash vs gemini-3.5-flash vs gemini-3.7-flash)
via Google's OpenAI-compatible endpoint, grades the clinical output with a pinned
reference-aware LLM judge, and produces:
  1. per-model validation scores and acceptance pass/fail status,
  2. RegressionDiff across model transitions (2.5 -> 3.5 and 3.5 -> 3.7),
  3. QMS change requests for each model upgrade event,
  4. safety monitoring projections for clinical governance.

Automatically loads GEMINI_API_KEY from ~/.env or environment.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from harness.diff import diff_runs
from harness.execute import run_battery
from harness.judge.llm import GradingConfig, LLMJudge
from harness.models.sut import SUTBinding
from harness.packio.loader import load_pack
from harness.qms.mappers import build_change_request
from harness.store.runstore import RunStore

ROOT = Path(__file__).parent
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
JUDGE_MODEL = "gemini-flash-lite-latest"


def _load_env():
    """Load GEMINI_API_KEY from ~/.env or local .env if not already set in environment."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    candidates = [
        Path.cwd() / ".env",
        ROOT / ".env",
        Path.home() / ".env",
        Path("/Users/aliaksei/.env"),
    ]
    for cand in candidates:
        if cand.exists():
            try:
                for line in cand.read_text().splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, v = line.split("=", 1)
                    k = k.strip().removeprefix("export ").strip()
                    v = v.strip().strip("'\"")
                    if k == "GEMINI_API_KEY" and v:
                        os.environ["GEMINI_API_KEY"] = v
                        return
            except Exception:
                pass


def _clock():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    _load_env()
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not set. Add GEMINI_API_KEY to ~/.env or export it in your shell.")
        return 1

    pack = load_pack(ROOT / "pack")
    store = RunStore(ROOT / "runs")

    judge = LLMJudge(
        SUTBinding(model_id=JUDGE_MODEL, model_version=JUDGE_MODEL,
                   endpoint=GEMINI_ENDPOINT, api_key_env="GEMINI_API_KEY"),
        GradingConfig(include_document=True, include_reference=True),
    )

    print(f"Running gemini_compare_all (judge={JUDGE_MODEL}, reference-aware) ...")
    results = run_battery(pack, "gemini_compare_all", store, seed=1, now=_clock, judge=judge)
    by_sut = {r.sut_id: r for r in results}

    print("\n=== PER-MODEL VALIDATION (Consultation Cohort) ===")
    for sut_id in ["gemini-2.5-flash", "gemini-3.5-flash", "gemini-3.7-flash"]:
        if sut_id in by_sut:
            r = by_sut[sut_id]
            ms = r.report["summary"]["mean_score"]["mean"]
            errs = r.report["summary"].get("judge_errors", 0)
            print(f"  {sut_id:24} mean_score={ms:.3f}  judge_errors={errs}  "
                  f"acceptance={'PASS' if r.report['acceptance']['overall_pass'] else 'FAIL'}")

    qms_dir = store.root / "qms"
    qms_dir.mkdir(parents=True, exist_ok=True)

    # 1. RegressionDiff: 2.5-flash -> 3.5-flash
    if "gemini-2.5-flash" in by_sut and "gemini-3.5-flash" in by_sut:
        m25, m35 = by_sut["gemini-2.5-flash"], by_sut["gemini-3.5-flash"]
        diff1 = diff_runs(store, m25.run_id, m35.run_id)
        agg1 = diff1["aggregate"]
        print("\n=== RegressionDiff: gemini-2.5-flash -> gemini-3.5-flash ===")
        print(f"  mean score {agg1['mean_score_baseline']:.3f} -> {agg1['mean_score_candidate']:.3f} "
              f"(delta {agg1['delta']:+.3f}, {'significant' if agg1['significant'] else 'not significant'})")
        print(f"  item regressions={diff1['n_regressions']} improvements={diff1['n_improvements']}")
        change1 = build_change_request(diff1)
        (qms_dir / "change_request_2.5_to_3.5.json").write_text(json.dumps(change1, indent=2, sort_keys=True))

    # 2. RegressionDiff: 3.5-flash -> 3.7-flash
    if "gemini-3.5-flash" in by_sut and "gemini-3.7-flash" in by_sut:
        m35, m37 = by_sut["gemini-3.5-flash"], by_sut["gemini-3.7-flash"]
        diff2 = diff_runs(store, m35.run_id, m37.run_id)
        agg2 = diff2["aggregate"]
        print("\n=== RegressionDiff: gemini-3.5-flash -> gemini-3.7-flash ===")
        print(f"  mean score {agg2['mean_score_baseline']:.3f} -> {agg2['mean_score_candidate']:.3f} "
              f"(delta {agg2['delta']:+.3f}, {'significant' if agg2['significant'] else 'not significant'})")
        print(f"  item regressions={diff2['n_regressions']} improvements={diff2['n_improvements']}")
        change2 = build_change_request(diff2)
        (qms_dir / "change_request_3.5_to_3.7.json").write_text(json.dumps(change2, indent=2, sort_keys=True))

    print(f"\n  QMS change requests written to {qms_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
