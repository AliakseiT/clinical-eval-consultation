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

The engine is being renamed from `harness` to `validrig` (CLI `rig`); the Python helper scripts still import the `harness` package until that rename lands.

## Runs & records

Run outputs (`runs/`) are immutable, content-hash-pinned artifacts. Historic runs and promoted V&V records produced before the 2026-08-30 relabel (when this pack was labeled "MedBench") embed the old case ids and were deliberately **not** carried into this repository; they remain in the superseded `clinical-eval-medbench` repo and will be regenerated under the new labels. `runs/` is gitignored here.
