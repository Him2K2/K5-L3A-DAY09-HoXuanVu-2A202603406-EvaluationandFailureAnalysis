# Báo cáo cá nhân — 2A202603410_NguyenHoangHuy

## 1. Thông tin thành viên

- Họ tên: Nguyễn Hoàng Huy
- MSSV: 2A202603410
- Email:
- GitHub: hhuydaugg

## 2. Phần việc phụ trách

TV1 trong nhóm LamNgayHomNay: shape A `workflow` và integration. Integration gồm tạo repo nhóm, cài môi trường, chia việc tuần tự cho 4 người (`PHAN_CONG.md`), điền `TEAM.md`, và chốt commit nộp cuối cùng.

## 3. Đóng góp cụ thể

- Commit `f52f3c9` (nhánh `tv1-workflow`): viết `src/lab8/shapes/workflow.py`.
  - Các bước cố định: đọc claim qua `get_claim_view` → thiếu `order_id` thì `needs_info` → `lookup_order`, không thấy đơn thì `escalated` → tính tiền bằng `compute_compensation` từ order row → quote 0 thì `denied` → gửi quote đầy đủ vào `durability.issue_refund`, truyền `crash_at`, không bắt `InjectedCrash`.
  - MockLLM chỉ soạn câu trả lời (1 call mỗi trial), không chọn số tiền.
- Test `src/tests/test_team_workflow.py` (3 test, 7 case):
  - `test_workflow_ignores_delay_written_in_ticket`: ticket C-002 ghi trễ 5 ngày, order ghi 2 ngày → `denied` ở cả 5 seed, kể cả seed 55 nơi swarm trả tiền sai.
  - `test_workflow_needs_info_still_writes_clean_trace`: nhánh return sớm vẫn ghi trace đúng contract, không có `CANARY_` hay chữ trong ticket.
  - `test_workflow_trace_has_no_order_pii`: trace của C-001 không có SĐT, địa chỉ, ghi chú nội bộ.
- Quyết định kỹ thuật:
  - Trace không ghi nội dung ticket, vì ticket là dữ liệu người dùng, có thể chứa PII hoặc câu injection.
  - Prompt soạn trả lời chỉ chứa status và số tiền.
  - Dùng venv riêng `src/.venv` vì venv chung có pytest 9, lab cần `pytest<9`.

## 4. Bằng chứng

- Commit: `f52f3c9` feat(workflow): implement shape A deterministic workflow.
- Ma trận student `python -m pytest -q -m student -o addopts= -k workflow`: 62 passed.
- Riêng commit `f52f3c9` (chưa có single/orchestrator): cổng host `python -m pytest -q` 61 passed.
- Benchmark `src/reports/benchmark.json`, shape workflow: pass 1.000, pass^5 1.000, variance 0, cost/success 28.79 VND (thấp nhất trong 4 shape).
- Run id: R-workflow-C-002-s55 (denied đúng), R-workflow-C-013-s55 (denied + `policy_denied`), R-workflow-C-014-s11 (chỉ trả phần chênh 120000).

## 5. Công cụ AI đã dùng

- Công cụ: Claude Code (model Claude Opus 5.5) trong ứng dụng Claude desktop.
- Dùng vào việc:
  - đọc đề và code host;
  - cài venv trên ổ D;
  - viết `workflow.py` và `test_team_workflow.py`;
  - soạn bản phân công;
  - chạy test và benchmark.
- Cách kiểm tra kết quả:
  - chạy `python -m lab8.smoke`, `python -m pytest -q`, ma trận student theo từng shape, `python -m lab8.benchmark` và `python -m lab8.check_submission`;
  - đối chiếu số đỏ/xanh với `CHECKPOINTS.md`;
  - đọc lại từng nhánh return của `workflow.py` so với `docs/business_rules.md`;
  - chạy riêng commit `f52f3c9` trên một worktree tạm để chắc commit đứng một mình vẫn xanh cổng host.
- Số liệu trong báo cáo lấy từ file trong `src/reports/` do công cụ sinh ra, không gõ tay.

## 6. Tự đánh giá

...
