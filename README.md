# clinical-eval-consultation

An evaluation pack for LLM-based **telemedicine consultation** workflows, built for the **validrig** engine (CLI: `rig`; formerly "Harness Factory").

## Provenance

The 10 cases (`CONSULT_001`–`CONSULT_010`) are **original, independently authored synthetic consultation cases**, hardcoded in `ingest_consultation.py`. Their design follows the D.O.T.S. specification published in [arXiv:2603.25821](https://arxiv.org/abs/2603.25821) (Doctorina MedBench), cited here as design provenance only: **no Doctorina data is included** — the Doctorina MedBench dataset was never publicly released. The cases are not physician-authored; clinical adjudication by HCP experts is a planned, separate step.

## Intended Use

Evaluates multi-domain clinical decision workflows across:
1. **Diagnosis**: Primary clinical identification
2. **Differential**: Retrieval of plausible clinical alternatives
3. **Investigations / Workup**: Appropriate diagnostic tests and procedures
4. **Treatment & Safety**: Guideline-concordant therapy without contraindicated actions
5. **Red Flags & Escalation**: Recognition of safety-critical emergency conditions

For demonstration / discussion with clinicians — not a clinical device.

## Build & Run

```bash
# 0. (Re)generate the casebank + adjudication files from source
python ingest_consultation.py

# 1. Lint the evaluation pack
rig lint pack

# 2. Run offline smoke battery (deterministic fake model + fake judge)
rig run pack --battery smoke --out ./runs --seed 1

# 3. Run Gemini multi-model comparison (2.5-flash vs 3.5-flash vs 3.7-flash)
GEMINI_API_KEY=... python run_gemini_eval.py

# 4. Measure input contract on real data
GEMINI_API_KEY=... python run_gemini_contract.py
```

The judge is declared in `pack/judge.yaml`, not constructed by the scripts: the `smoke` battery selects the offline fake judge, every Gemini battery uses the pinned `gemini-flash-lite-latest` G-Eval judge. So the `judge_id` a run pins is the judge that actually graded it, and swapping the judge changes `pack_hash` → `run_id` — a revalidation event by construction. The helper scripts only orchestrate batteries and load `GEMINI_API_KEY` (env-var name only; no key is ever stored in the pack).

## Runs & records

Run outputs (`runs/`) are immutable, content-hash-pinned artifacts. Historic runs and promoted V&V records produced before the 2026-08-30 relabel (when this pack was labeled "MedBench") embed the old case ids and were deliberately **not** carried into this repository; they remain in the superseded `clinical-eval-medbench` repo and will be regenerated under the new labels. `runs/` is gitignored here.

## Licensing

- **Code** (`ingest_consultation.py`, run scripts, and everything not listed
  below): **AGPL-3.0-or-later**, same license as the
  [validrig](https://github.com/AliakseiT/validrig) engine — full text in
  [`LICENSE`](LICENSE).
- **Pack content** (cases, rubric, adjudication expectations, authored pack
  prose): **CC BY 4.0** — fully original work, no third-party data; notice and
  covered files in [`LICENSE-CONTENT`](LICENSE-CONTENT).

License files live outside the parsed pack model, so adding or editing them
does not change the `pack_hash` or invalidate pinned runs.
