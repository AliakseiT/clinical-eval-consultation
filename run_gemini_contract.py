#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Extract the input contract from a REAL model (gemini-2.5-flash) on the consultation casebank.

Runs the `gemini_contract` battery (ablation + format) to characterize which
clinical inputs drive model performance. Grading is done by the judge the pack
declares in `pack/judge.yaml` (pinned, reference-aware) — this script only
orchestrates, so the judge each run pins is the judge that graded it.
Automatically loads GEMINI_API_KEY from ~/.env or environment.
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from validrig.execute import run_battery
from validrig.packio.loader import load_pack
from validrig.store.runstore import RunStore

ROOT = Path(__file__).parent


def _load_env():
    """Load GEMINI_API_KEY from ~/.env or local .env if not already set in environment."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    candidates = [
        Path.cwd() / ".env",
        ROOT / ".env",
        Path.home() / ".env",
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
    battery = sys.argv[1] if len(sys.argv) > 1 else "gemini_contract"
    judge_spec = pack.judge_for(battery)
    now = lambda: datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    print(f"Running {battery} (ablation, judge={judge_spec.id} / "
          f"{judge_spec.binding.get('model_id')}, declared in pack/judge.yaml) ...")
    r = run_battery(pack, battery, store, seed=1, now=now)[0]
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
