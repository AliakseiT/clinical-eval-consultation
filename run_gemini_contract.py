#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Extract the input contract from a REAL model (gemini-2.5-flash) on the consultation casebank.

Runs the `gemini_contract` battery (ablation + format) with a pinned,
reference-aware lite judge to characterize which clinical inputs drive model performance.
Automatically loads GEMINI_API_KEY from ~/.env or environment.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from harness.execute import run_battery
from harness.judge.llm import GradingConfig, LLMJudge
from harness.models.sut import SUTBinding
from harness.packio.loader import load_pack
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


def main() -> int:
    _load_env()
    if not os.environ.get("GEMINI_API_KEY"):
        print("Set GEMINI_API_KEY in ~/.env or environment.")
        return 1
    pack = load_pack(ROOT / "pack")
    store = RunStore(ROOT / "runs")
    judge = LLMJudge(
        SUTBinding(model_id=JUDGE_MODEL, model_version=JUDGE_MODEL,
                   endpoint=GEMINI_ENDPOINT, api_key_env="GEMINI_API_KEY"),
        GradingConfig(include_document=True, include_reference=True),
    )
    battery = sys.argv[1] if len(sys.argv) > 1 else "gemini_contract"
    now = lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    print(f"Running {battery} (ablation) ...")
    r = run_battery(pack, battery, store, seed=1, now=now, judge=judge)[0]
    print(f"\nrun={r.run_id} sut={r.sut_id} units={r.n_units} acceptance="
          f"{'PASS' if r.report['acceptance']['overall_pass'] else 'FAIL'}")
    print(f"\n=== INPUT CONTRACT on {r.sut_id} (clinical-eval-consultation) ===")
    for e in r.contract["elements"]:
        iv = e["information_value"]
        print(f"  {e['name']:30} measured={e['measured']!s:5} "
              f"information_value={'—' if iv is None else round(iv, 3)}")
    print("  minimal sufficient set:", r.contract["minimal_sufficient_set_candidate"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
