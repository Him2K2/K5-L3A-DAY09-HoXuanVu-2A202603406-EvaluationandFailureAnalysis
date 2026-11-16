# Team

## Thông tin nhóm

- Tên nhóm: LamNgayHomNay
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-LamNgayHomNay-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/hhuydaugg/K5-L3A-DAY08-LamNgayHomNay-FromWorkflowsToAgents, `main`, commit chốt: (điền sau khi cả nhóm commit)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Hoàng Huy | 2A202603410 | hhuynguyen2803@gmail.com | hhuydaugg | TV1 — workflow + integration (nhóm trưởng) |
|   2 | Nguyễn Thế Văn | 2A202603474 | zanngyn@gmail.com | zannngyn | TV2 — single agent |
|   3 | Hồ Xuân Vũ | 2A202603406 | vuqtpro1592002@gmail.com | Him2K2 | TV3 — orchestrator + handoff |
|   4 | Trần Văn Tài | 2A202603506 | tail110402@gmail.com | iat-123 | TV4 — ledger/crash + evaluation |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Hoàng Huy (TV1, hhuydaugg) | Workflow + integration | `f52f3c9` feat(workflow): implement shape A deterministic workflow | `src/tests/test_team_workflow.py` |
| Nguyễn Thế Văn (TV2) | Single agent | `84dcc5c` feat(shapes): implement single shape workflow | `src/tests/test_team_single.py` |
| Hồ Xuân Vũ (TV3) | Orchestrator + handoff | `964f11b` feat(orchestrator): implement run_claim function and add tests for handoff behavior | `src/tests/test_team_orchestrator.py` |
| Trần Văn Tài (TV4) | Ledger/crash + evaluation | `fd7148f` feat(eval): add crash tests, benchmark reports and team ADR | `src/tests/test_team_crash.py` |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## 2A202603410_NguyenHoangHuy

### Phần việc phụ trách

- TV1: shape A `workflow` và integration (chia việc trong `PHAN_CONG.md`, điền `TEAM.md`, chốt commit nộp).

### Đóng góp cụ thể

- Commit `f52f3c9`: viết `src/lab8/shapes/workflow.py` theo 8 bước của docstring.
- Test `src/tests/test_team_workflow.py`: 3 test, 7 case.

### Bằng chứng

- 62/62 test student của workflow; benchmark public pass 1.000, pass^5 1.000 (`src/reports/benchmark.json`).
- Báo cáo chi tiết: `report/team/2A202603410_NguyenHoangHuy.md`.

## 2A202603506_TranVanTai

### Phần việc phụ trách

- TV4: ledger/crash + evaluation (crash test, benchmark, ADR, research card).

### Đóng góp cụ thể

- Commit `fd7148f`: thêm `src/tests/test_team_crash.py`, các report `src/reports/benchmark.json`, `src/reports/crash.json`, `src/reports/ablation_r2_swarm_no_ticket_delay.json`; điền `report/team/decision_adr.md` và `report/team/research_card.md`.
- Test `src/tests/test_team_crash.py`: 9/9 cho workflow, single, orchestrator ở 3 điểm crash.

### Bằng chứng

- Crash safety 20/20 (`src/reports/crash.json`).
- Benchmark 14 claim × 5 seed (`src/reports/benchmark.json`); ablation R2 swarm pass 0.986 → 1.000 (`src/reports/ablation_r2_swarm_no_ticket_delay.json`).

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
