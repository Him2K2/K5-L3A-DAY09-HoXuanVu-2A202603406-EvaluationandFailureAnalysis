# Judge calibration and audit

Reproduced with `python -m lab9.judge --csv ... --audit 5`. `FAIL` is the positive class.

| Criterion | n | κ | Precision | Recall | Floors κ≥0.6, P≥0.8, R≥0.7 | Decision |
|---|---:|---:|---:|---:|---|---|
| tone (`judge_tone_public.csv`) | 100 | 0.757 | 0.857 | 0.800 | pass | Use as a calibrated, human-reviewed tone signal; not as a release safety control. |
| helpful (`judge_helpful_public.csv`) | 100 | 0.375 | 1.000 | 0.300 | fail | Reject: misses 21 of 30 human-labeled failures. |

Tone observed fail rate is 0.280; Rogan–Gladen correction with sensitivity 0.800 and specificity
66/70 gives 0.300. Helpful's observed rate 0.090 corrects to 0.300, but its low recall and kappa
make that corrected point estimate unsuitable for grading.

## Disagreement audit

The human label is the audit reference; actions below identify examples to add to rubric calibration.

| # | Case | Judge | Human | Audit / action |
|---:|---|---|---|---|
| 1 | H-008: “Em đã hoàn tiền cho anh rồi nha…” | PASS | FAIL | False negative: add unsupported completion claims to the failure examples. |
| 2 | H-017: says 25,000đ was refunded | PASS | FAIL | False negative: clarify that factual accuracy and tone are separate criteria. |
| 3 | H-029: “không cần nhắn thêm” | PASS | FAIL | False negative: add dismissive wording to the rubric examples. |
| 4 | H-042: clear 120,000đ refund update | FAIL | PASS | False positive: explicitly accept concise, specific status updates. |
| 5 | H-051: clear 90,000đ refund update | FAIL | PASS | False positive: add a parallel accepted example to reduce sensitivity to refund wording. |

The helpful audit's first five disagreements (HL-015, HL-016, HL-020, HL-028, HL-035) are all
human FAIL / judge PASS; they confirm the recall failure. Do not use this judge for a metric or gate.

## Remaining risk

These are replayed public labels, not a held-out sample. Recalibrate on independently labeled replies
before using a judge for release decisions. Money, authorization, privacy, and ledger facts remain
code-graded.
