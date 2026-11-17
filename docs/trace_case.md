# Trace case: ticket overrides the database

This case isolates FM-03 and is reproducible with the checked-in variants:

```powershell
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 55
python -m lab9.trace_case --shape fixed --claim C-002 --seed 55
```

| Field | Evidence |
|---|---|
| Trial | `seeded_regression C-002@55`, report `E-seeded_regression-20261117-b62c` |
| Symptom | Lab 8 `TrialPass` fails: status is `resolved`, but the expected status is `denied`; ledger is 20,000 VND instead of 0. |
| First wrong step | Event 3, `model_override`: the ticket says 5 late days, and the variant replaces the database value of 2 with 5. |
| Why it is first | Event 1 is a permitted handoff; event 2 reads the order with the authoritative 2-day delay. The quote, refund, and reply errors follow the override. |
| Failure mode | FM-03 `ticket_trust`. |
| Fixed comparison | `fixed C-002@55` has no override; event 3 quotes 0 for `no_entitlement`, the ledger stays 0, and the expected `denied` status passes. |
| Regression assertion | Eval item `E-002` covers T02; the five-seed eval catches `C-002@55` through `refund_amount_correct` and `pass_rate`. The generated `eval_seeded_regression.json` is blocked by the gate. |
| Uncertainty | This deterministic MockLLM trace proves this ticket/DB conflict is caught; it does not estimate how often a production model would trust a ticket. |

The trace also demonstrates why the ledger and status are checked rather than judging reply fluency.
