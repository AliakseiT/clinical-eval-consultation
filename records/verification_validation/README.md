# Verification & Validation Records — clinical-eval-consultation

Retained, controlled V&V records for this project — stored **exactly as they would be in a real clinical deployment**. Transient run outputs live in `runs/` (gitignored); a record is *promoted* here after clinical review and signed as QMS evidence.

| Record | Target | Description |
|---|---|---|
| [`vvr-gemini-2.5-flash.md`](vvr-gemini-2.5-flash.md) | Gemini 2.5 Flash | Baseline consultation validation dossier (`.html` = printable) |
| [`vvr-gemini-3.5-flash.md`](vvr-gemini-3.5-flash.md) | Gemini 3.5 Flash | Model upgrade validation dossier & RegressionDiff |
| [`vvr-gemini-3.7-flash.md`](vvr-gemini-3.7-flash.md) | Gemini 3.7 Flash | Next-gen model validation dossier & RegressionDiff |
| [`vvr-gemini-2.5-flash-contract.md`](vvr-gemini-2.5-flash-contract.md) | Gemini 2.5 Flash | Input-contract dossier — **`not_approved_for_release`**: critical-omission rate 0.067 exceeds the 0.05 limit on the baseline (intended-input) condition |

Open the `.md` files to read on GitHub/IDE; open the `.html` in a browser to print (Cmd/Ctrl-P). The `.json` is the underlying structured QMS record.

All records were regenerated 2026-08-30 from runs on the current `CONSULT_###` casebank (`rig dossier`, seed 1, pack_hash `58e1058bc0b4b9f1…`): battery `gemini_compare_all` → runs `63eec9c7d2ca0c08` (2.5-flash), `a8ccc6fac866e8d3` (3.5-flash), `84ef279cb7a91160` (3.7-flash); battery `gemini_contract` → run `ac16501e75930ce7` (2.5-flash). The contract record is retained precisely **because** it failed: a record set that keeps only its passing runs is not evidence. The V&V records produced before the 2026-08-30 relabel (pack was then labeled "MedBench") embedded the old case ids and were deliberately not carried over; they remain only in the superseded `clinical-eval-medbench` repo. All records here are **DRAFT / unsigned** pending clinical review.

The judge is now declared in the pack (`pack/judge.yaml`), so each record pins `judge_id: geval-gemini-flash-lite` — the reference-aware `gemini-flash-lite-latest` G-Eval judge that actually graded these runs. Records promoted before that change pinned `judge_id: fake-judge` while a real judge graded them, because the run scripts constructed the judge outside the pack; those records are superseded by these. Note that `gemini-flash-lite-latest` is a floating provider alias — the pin records the alias, not a resolved model build.
