# Team

## Thông tin nhóm

- Tên nhóm: LamNgayHomNay
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-LamNgayHomNay-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/hhuydaugg/K5-L3A-DAY08-LamNgayHomNay-FromWorkflowsToAgents, `main`, commit chốt: (điền sau khi cả nhóm commit)

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Hoàng Huy | 2A202603410 |   hhuynguyen2803@gmail.com    | hhuydaugg | TV1 — workflow + integration (nhóm trưởng) |
|   2 |        |      |       |        | TV2 — single agent |
|   3 |    Hồ Xuân Vũ    | 2A202603406     |  vuqtpro1592002@gmail.com   | him2k2  | TV3 — orchestrator + handoff |
|   4 |        |      |       |        | TV4 — ledger/crash + evaluation |

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Nguyễn Hoàng Huy (TV1, hhuydaugg) | Workflow + integration | `f52f3c9` feat(workflow): implement shape A deterministic workflow | `src/tests/test_team_workflow.py` |
| TV2 | Single agent | chưa commit (`src/lab8/shapes/single.py`) | `src/tests/test_team_single.py` (chưa commit) |
| TV3 | Orchestrator + handoff | chưa commit (`src/lab8/shapes/orchestrator.py`) | `src/tests/test_team_orchestrator.py` (chưa commit) |
| TV4 | Ledger/crash + evaluation | chưa commit (`src/reports/*.json`, `report/team/decision_adr.md`, `research_card.md`) | `src/tests/test_team_crash.py` (chưa commit) |

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

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
