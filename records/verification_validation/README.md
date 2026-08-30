# Verification & Validation Records — clinical-eval-consultation

Retained, controlled V&V records for this project — stored **exactly as they would be in a real clinical deployment**. Transient run outputs live in `runs/` (gitignored); a record is *promoted* here after clinical review and signed as QMS evidence.

| Record | Target | Description |
|---|---|---|
| [`vvr-gemini-2.5-flash.md`](vvr-gemini-2.5-flash.md) | Gemini 2.5 Flash | Baseline consultation validation dossier (`.html` = printable) |
| [`vvr-gemini-3.5-flash.md`](vvr-gemini-3.5-flash.md) | Gemini 3.5 Flash | Model upgrade validation dossier & RegressionDiff |
| [`vvr-gemini-3.7-flash.md`](vvr-gemini-3.7-flash.md) | Gemini 3.7 Flash | Next-gen model validation dossier & RegressionDiff |

Open the `.md` files to read on GitHub/IDE; open the `.html` in a browser to print (Cmd/Ctrl-P). The `.json` is the underlying structured QMS record.

All records were generated 2026-08-30 from runs on the current `CONSULT_###` casebank (`rig dossier`, battery `gemini_compare_all`, seed 1, judge `gemini-flash-lite-latest`, reference-aware). The V&V records produced before the 2026-08-30 relabel (pack was then labeled "MedBench") embedded the old case ids and were deliberately not carried over; they remain only in the superseded `clinical-eval-medbench` repo. All records here are **DRAFT / unsigned** pending clinical review.
