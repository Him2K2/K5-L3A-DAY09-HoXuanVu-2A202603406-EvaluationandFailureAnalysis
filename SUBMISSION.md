# Submission

## Loại bài

**Nhóm.** Nhóm push bài lên GitHub; mỗi thành viên tự nộp cùng link repo nhóm trên LMS bằng tài khoản cá nhân. Ai không nộp link thì không có điểm, dù nhóm đã nộp.

## Tên repo và biến tên

- `Kn`: số khóa. Khóa này dùng `K5`.
- Level/lớp: `L3A`.

### Repo bài nộp nhóm

```text
K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents
```

`TenNhom` viết không dấu, không khoảng trắng. Repo phải public, hoặc đã mời giảng viên vào.

### Tạo repo nhóm

Nhóm trưởng Fork repo đề bài rồi đổi tên theo mẫu trên. Nếu không Fork được, clone repo đề bài, đổi `origin` sang repo nhóm rỗng và push `main`:

```bash
git clone https://github.com/VinUni-AI20k/K5-Day8-From-Workflows-to-Agents.git <TEN_REPO_NHOM>
cd <TEN_REPO_NHOM>
git remote rename origin upstream
git remote add origin <URL_REPO_NHOM>
git push -u origin main
```

## Cấu trúc và deliverable phải nộp (đặt tên và cấu trúc)

### Báo cáo và thông tin nhóm (ở gốc repo)

| File | Nội dung |
|---|---|
| `TEAM.md` | Thông tin nhóm, thành viên, phân công và **bảng đóng góp** (mỗi người một dòng) |
| `report/team/group_report.md` | Báo cáo nhóm, tối đa 5 trang ngoài phụ lục |
| `report/team/decision_adr.md` | Shape chọn, commit hash, run id, số liệu. Giữ nguyên các dòng nhãn |
| `report/team/research_card.md` | Phiếu nghiên cứu R1–R4 và kết quả ablation. Cột "Nhóm điền" không để trống |
| `report/team/MSSV_HoTen.md` | Mỗi thành viên một file, copy từ mẫu và đổi tên, ví dụ `report/team/20241234_NguyenVanAn.md` |
| `report/team/bonus_report.md` | Chỉ khi làm bonus. Tiêu đề `# Bonus report: B1` … `B6` |

### Code và bằng chứng (trong `src/`)

| Phần | File |
|---|---|
| Ba shape | `src/lab8/shapes/workflow.py`, `single.py`, `orchestrator.py` |
| Test nhóm thêm | `src/tests/` |
| Benchmark | `src/reports/benchmark.json` do `lab8.benchmark` tạo: đủ 4 shape, seed `11,22,33,44,55`, ≥ 10 claim |
| Crash suite | `src/reports/crash.json`: `crash_safety` = `20/20` |
| Tự kiểm hidden (tùy chọn) | `src/reports/hidden_selfcheck.json` |
| Bonus (nếu làm) | `src/bonus/`, `src/tests/test_bonus_*.py`, `src/reports/bonus_*.json` |

Không sửa tay file JSON trong `src/reports/`. Không commit `traces/`, `*.sqlite`, `student_drop/`, `src/eval/instructor/`, `.venv/` hay `.env`.

### Thứ tự nộp

Chạy trong `src/`:

1. `python -m pytest -q` xanh.
2. Chạy benchmark và crash test ([src/reports/README.md](src/reports/README.md)) để tạo `reports/benchmark.json`, `reports/crash.json`.
3. Commit, rồi chạy `git rev-parse --short HEAD`. Ghi hash và run id vào `report/team/decision_adr.md`, rồi commit tiếp.
4. `python -m lab8.check_submission` ra `0 FAIL`, rồi push.

## Nộp Lab 9 bổ sung trong repo Day 8

Lab 9 là **overlay trong repo nhóm Day 8**. Repo nộp duy nhất vẫn là
`K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents`; `lab9-starter` chỉ dùng làm nguồn hướng dẫn/code,
không phải repo nộp. Không chạy `git init` ở thư mục cha `day9`, không commit/push `lab9-starter`
hay repo Day 9 riêng.

### Kiểm tra repo trước khi tạo branch hoặc commit (PowerShell)

```powershell
$repo = 'C:\path\to\K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents'
Set-Location $repo
git rev-parse --show-toplevel
git status --short
git remote -v
```

`git rev-parse --show-toplevel` phải trỏ đúng vào thư mục repo Day 8. `origin` phải là URL repo
nhóm **Day 8** trước khi push; nếu URL có `DAY09` hoặc là repo khác, dừng lại, không push. Không
đổi remote sang URL đoán được; hỏi nhóm trưởng để lấy URL đúng.

Nếu đã được nhóm trưởng xác nhận URL Day 8, có thể sửa `origin` rồi kiểm tra lại:

```powershell
git remote set-url origin <URL_REPO_NHOM_DAY08>
git remote -v
```

Tạo branch làm Lab 9 từ repo Day 8:

```powershell
git switch -c starter/d09
```

Nếu branch đã tồn tại thì dùng `git switch starter/d09`. Mọi lệnh `git add` bên dưới chạy từ root
Day 8; chỉ stage đường dẫn `src/`, `docs/` và `.github/` được liệt kê. Không dùng `git add -A`
khi chưa kiểm tra root và `git status`.

### Các mốc commit nên có

1. **Sau M0 — overlay:** commit phần Lab 9 được chép vào repo Day 8. Không chép đè README,
   `CHECKPOINTS.md`, `RUBRIC.md`, `SUBMISSION.md` hay `.gitignore` ở root. Nội dung gồm
   `src/lab9/`, `src/requirements-lab9.txt`, `src/tests/test_lab9_*.py`, config và fixture Lab 9,
   tài liệu Lab 9 trong `docs/`, `src/harness_map.yaml` và riêng
   `.github/workflows/eval-gate.yml` (giữ workflow Lab 8).
   Commit gợi ý: `chore: add lab9 overlay`.
   Nếu `git log` đã có commit này thì M0 đã xong; không tạo commit overlay trùng lặp, chuyển sang M1–M3.
2. **Sau M1–M3 — Core implementation:** commit code hoàn chỉnh trong `src/lab9/`, test,
   `src/config/metric_spec.yaml`, eval set v1/labels và tài liệu đã điền:
   `docs/failure_taxonomy.md`, `docs/trace_case.md`, `docs/judge_audit.md`, `docs/eval_card.md`,
   `docs/PRD_v1.1.md`. Không đưa `src/lab8/` vào commit.
   Commit gợi ý: `feat: implement lab9 core evaluation`.
3. **Sau M4 — baseline v1:** chạy evaluator trên `swarm`, sau đó stage report do script tạo:

   ```powershell
   Set-Location (Join-Path $repo 'src')
   python -m lab9.eval --shape swarm --spec config/metric_spec.yaml --out reports/baseline_v1.json
   python -m lab9.eval --shape fixed --spec config/metric_spec.yaml --out reports/eval_fixed.json
   python -m lab9.eval --shape seeded_regression --spec config/metric_spec.yaml --out reports/eval_seeded_regression.json
   Set-Location $repo
   git add -f src/reports/baseline_v1.json src/reports/eval_fixed.json src/reports/eval_seeded_regression.json
   git diff --cached --name-only
   git commit -m "chore: add eval baseline v1"
   ```

   `baseline_v1.json` phải là kết quả `swarm`, không sửa tay. Gate phải cho qua baseline và `fixed`,
   đồng thời chặn `seeded_regression`; lưu output `exit 1` vào phần mô tả PR.
4. **Sau M5–M7 — Advanced/Expert:** commit `src/config/fm_map.yaml`,
   `src/config/metric_spec_v2.yaml`, `src/data/eval/eval_set_v2.jsonl`,
   `src/data/eval/labels_v2.json`, test, tài liệu và cập nhật workflow. Sau khi build/check eval set
   v2 sạch, tạo reports bằng script:

   ```powershell
   Set-Location (Join-Path $repo 'src')
   python -m lab9.evalset --v2 --build
   python -m lab9.eval --shape swarm --spec config/metric_spec_v2.yaml --out reports/baseline_v2.json
   python -m lab9.eval --shape slice_regression --spec config/metric_spec_v2.yaml --out reports/eval_slice_regression.json
   Set-Location $repo
   git add src/config/fm_map.yaml src/config/metric_spec_v2.yaml `
       src/data/eval/eval_set_v2.jsonl src/data/eval/labels_v2.json
   git add -f src/reports/baseline_v2.json src/reports/eval_slice_regression.json
   git diff --cached --name-only
   git commit -m "feat: add lab9 v2 slices and integrity gate"
   ```

   `reports/traps/` được tạo bởi `python -m lab9.traps`; không sửa các file này bằng tay. Dán output
   `lab9.mutation --aa`, scorecard và bốn dòng trap bị chặn vào mô tả PR. Chỉ stage reports bổ sung
   nếu nhóm muốn lưu làm bằng chứng; không stage toàn bộ `src/reports/`.

Trước **mỗi** commit, kiểm tra `git diff --cached --name-only` và `git diff --cached -- src/lab8`.
Danh sách không được có `lab9-starter`, repo Day 9 riêng, file secret, hoặc thay đổi trong `src/lab8/`.
Các commit được tạo trong repo Day 8; push branch `starter/d09` lên `origin` chỉ sau khi xác nhận
`origin` là repo Day 8 của nhóm:

```powershell
git push -u origin starter/d09
```

Mở PR `starter/d09` → `main` của **repo Day 8**. Mỗi thành viên nộp cùng link repo nhóm trên LMS.

## Deadline (GMT+7)

- Lab **sáng**: nộp trước **23h59 GMT+7** ngày lab.
- Lab **chiều** (lịch mẫu 13:30–17:30) hoặc **tối**: nộp trước **11h59 GMT+7** ngày hôm sau.
- Coach có thể gia hạn ≤ 48h nếu có lý do chính đáng; nếu gia hạn thì theo thông báo của coach.
- Các mốc giờ trong [CHECKPOINTS.md](CHECKPOINTS.md) là checkpoint tại lớp, không phải deadline.
- Sửa sau deadline phải tạo commit mới; xem [RULES.md](RULES.md).

## Checklist

- [ ] Đổi tên repo theo đúng quy ước `K5-L3A-DAY08-…`.
- [ ] Điền `TEAM.md` ở root: thông tin nhóm, thành viên, bảng đóng góp.
- [ ] Mỗi thành viên có file báo cáo đã đổi tên đúng định dạng `report/team/MSSV_HoTen.md`.
- [ ] `report/team/group_report.md`, `decision_adr.md`, `research_card.md` đã điền đủ.
- [ ] Mỗi thành viên có commit kỹ thuật và ít nhất một test trong lịch sử branch nộp bài.
- [ ] Trong `src/`: `python -m pytest -q` xanh; có `reports/benchmark.json` và `reports/crash.json` do công cụ sinh ra.
- [ ] Trong `src/`: `python -m lab8.check_submission` ra `0 FAIL`.
- [ ] Lab 9 (nếu làm trên repo Day 8): eval set v1/v2 sạch; commit baseline do script sinh; CI cho qua baseline/`fixed`, chặn `seeded_regression`.
- [ ] Lab 9 Advanced/Expert (nếu làm): `mutation` 3/3, không false alarm; traps công khai bị chặn; `docs/eval_card.md` ghi ngưỡng, kết quả và giới hạn mẫu.
- [ ] Không commit secret, password, file `.env`, trace hay file `.sqlite`.
- [ ] Đã push lên GitHub; repo mở được cho người chấm.
- [ ] Mọi thành viên đã nộp cùng link repo trên LMS trước deadline.
