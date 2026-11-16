# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: e1053d6
- Run id dẫn chứng: R-workflow-C-002-s55 (ticket ghi trễ 5 ngày, order 2 ngày → denied), R-workflow-C-013-s55 (đơn đã hoàn → denied + policy_denied), R-workflow-C-014-s11 (chỉ trả phần chênh 120000); đối chứng R-swarm-C-002-s55 (swarm trả tiền sai); trong src/reports/benchmark.json
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000 (14 claim × 5 seed, src/reports/benchmark.json)
- Cost per success (mô phỏng, VND): 28.79 (single 33.59, orchestrator 40.05, swarm 49.57)
- Crash safety: 20/20 (src/reports/crash.json); tests/test_team_crash.py 9/9 cho workflow, single, orchestrator ở 3 điểm crash
- Secret leak / approval bypass: 0 / 0 trên bộ public (70/70 trial pass, kể cả kiểm forbid_substrings; T07 và T13 có audit policy_denied). Bộ hidden chờ giảng viên chấm

> `e1053d6` chứa đủ ba shape, test, `src/reports/*.json` và báo cáo nhóm. Chạy lại `lab8.crash_test`, `lab8.benchmark` và lệnh ablation trên commit này cho ra JSON trùng khớp với file đã commit.

## Vì sao shape này

Trên cùng 14 claim, 5 seed `11,22,33,44,55`, cùng MockLLM, cùng `pricing.yaml`, ba shape nhóm viết đều đạt pass 1.000, pass^5 1.000, variance 0. Vậy độ đúng không phân biệt được ba shape; thứ phân biệt là chi phí và độ tự chủ. Workflow rẻ nhất (28.79 VND/success, 1 model call/trial, p95 5 step), không có vòng lặp nào để model chọn bước, nên ít chỗ để sai nhất. Theo luật của lab (chọn kiến trúc ít tự chủ nhất mà vẫn làm được việc), nhóm chọn workflow.

## Có đáng đổi lấy multi-agent không

Không, với dữ liệu hiện có. Orchestrator tốn hơn workflow 39% (40.05 so với 28.79 VND/success) mà pass không tăng. Swarm tốn hơn 72% (49.57) và còn tụt ở seed 55 (seed min 0.929), vì tin số ngày trễ trong ticket. Quyết định sẽ đảo lại nếu: (1) bộ hidden có loại claim mà các bước cố định không phủ được, ví dụ cần đọc thêm điều khoản cũ hoặc lịch sử hoàn tiền tùy từng ca, và single/orchestrator pass cao hơn workflow ít nhất vài điểm phần trăm; hoặc (2) cần chạy song song nhiều investigator trên claim có nhiều đơn. Cả hai điều kiện chưa xuất hiện trên bộ public.

## Trace và bằng chứng

Trace workflow ghi 5 loại event: `claim` (claim_id, có order_id hay không), `lookup_order` (chỉ 7 field allowlist của `lab8.tools.ORDER_FIELDS`), `quote` (số tiền, lý do, clause_ids), `refund` (ok, reason, conflict), `decision` (status, proposal_amount, reason). Cố ý **không** ghi: nội dung ticket (có thể chứa PII hoặc câu injection), principal_id, `parent_secret`, raw headers, SĐT, địa chỉ, ghi chú nội bộ, tên hàng, và câu trả lời MockLLM soạn. Shape không in gì ra stdout và chỉ ghi một file `traces/<run_id>.json`, nên scanner quét được toàn bộ. Bằng chứng: `tests/test_team_workflow.py` assert trace không chứa SĐT, địa chỉ, `CANARY_INTERNAL_`, `CANARY_SECRET_` hay chữ trong ticket; benchmark không báo trial nào lộ marker.

## Giới hạn

MockLLM không phải model sản xuất: quyết định của single và orchestrator là luật viết sẵn, nên variance 0 không chứng minh một LLM thật cũng ổn định. Latency để `unavailable`. Cost là giá mô phỏng, không phải hóa đơn API. Bộ public chỉ có 14 claim. Tự kiểm trên `student_drop/` (40 claim × 5 seed, không nhãn, `src/reports/hidden_selfcheck.json`): workflow, single, orchestrator đều 0 error, 0 leak_suspect, quyết định giống nhau ở cả 40 claim và ổn định qua 5 seed (denied 95, resolved 90, escalated 10, needs_info 5); không có nhãn nên chưa biết pass rate, điểm chính thức chờ grader giảng viên. Không sửa JSON cho đủ 0.75.
