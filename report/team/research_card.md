# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R2 · Failure taxonomy |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Cemri, Pan, Yang et al., *Why Do Multi-Agent LLM Systems Fail?*, 2025 (NeurIPS 2025 theo slide lab; trang arXiv không ghi venue), https://arxiv.org/abs/2503.13657 (v3). Loại bằng chứng: phân tích trace có chú thích của người (taxonomy MAST) cộng benchmark |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Lỗi của hệ multi-agent gom được thành 3 nhóm, 14 failure mode: FC1 System Design Issues, FC2 Inter-Agent Misalignment, FC3 Task Verification. Phần lớn lỗi đến từ thiết kế hệ thống và phối hợp, không chỉ do năng lực model; khâu kiểm chứng thường chỉ kiểm hời hợt |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | 7 framework MAS mã nguồn mở (ChatDev, MetaGPT, HyperAgent, AppWorld, AG2, Magentic-One, OpenManus), task code, toán và agent tổng quát; model GPT-4o, GPT-4, Claude 3.7 Sonnet, Qwen2.5-Coder, CodeLlama; khoảng 1600 trace, chú thích bởi chuyên gia (kappa 0.88) và LLM judge o1 (kappa 0.77). Không có task tài chính hay hoàn tiền; kết luận về tỉ lệ từng mode không chuyển thẳng sang lab này |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Lần trượt của swarm ở seed 55 (C-002) thuộc FC3, mode FM-3.2 No or incomplete verification: số ngày trễ do peer đọc từ ticket được dùng mà không đối chiếu cột delay_days. Nếu tắt đúng đường đó thì pass rate swarm 0.986 → 1.000, pass^5 0.929 → 1.000, variance → 0; số model call giữ nguyên nên cost/success chỉ giảm nhẹ khoảng 1–2% (thêm 1 success trên cùng tổng chi phí) |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ cố định: MockLLM, tool manifest 1.1, seed 11,22,33,44,55, 14 claim public, pricing.yaml, evaluator `trial_pass` của `lab8.benchmark`, file `swarm_reference.py` không sửa. Biến duy nhất được thay đổi: trong lúc chạy, `parse_delay_days` của swarm trả `None`, tức peer vẫn được gọi (cùng số model call) nhưng số ngày đọc từ ticket không còn vào được quyết định |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: refund 20000 cho claim lẽ ra bị từ chối (status resolved thay vì denied ở R-swarm-C-002-s55). Đo bằng pass rate, pass^5, seed min và seed variance của swarm, cộng cost/success để chắc thay đổi không đổi lấy chi phí |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn, trong `src/`): `python -c "import lab8.shapes.swarm_reference as s; s.parse_delay_days = lambda t: None; from lab8.benchmark import main; raise SystemExit(main(['--shapes', 'swarm', '--cases', 'data/public_claims.jsonl', '--seeds', '11,22,33,44,55', '--out', 'reports/ablation_r2_swarm_no_ticket_delay.json']))"`
- Run id / file report: `src/reports/ablation_r2_swarm_no_ticket_delay.json` (R-swarm-C-002-s55 chuyển từ fail sang pass); baseline `src/reports/benchmark.json`
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **Đúng.** Swarm pass 0.986 → 1.000, pass^5 0.929 → 1.000, seed min 0.929 → 1.000, variance 0.000816 → 0. Cost/success 49.57 → 48.72 VND (−1.7%); tổng chi phí 3420.12 → 3410.10 vì nhánh tính lại quote (1 tool call) cũng không còn chạy. Model call trung bình giữ 3.0. Kết luận: lỗi nằm ở khâu kiểm chứng (FC3), không phải ở topology swarm nói chung; nhưng swarm sau khi vá vẫn đắt hơn workflow 69% (48.72 so với 28.79)
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`. Điểm yếu của swarm do người soạn lab cài sẵn theo `seed % 5`, nên ablation chỉ xác nhận đúng cơ chế đã biết, không ước lượng được tỉ lệ lỗi FC3 của một LLM thật. Chỉ 1 trial thay đổi trên 70, cỡ mẫu nhỏ. Giả thuyết được viết từ việc đọc khối `REFERENCE_WEAKNESS` trước khi chạy.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
