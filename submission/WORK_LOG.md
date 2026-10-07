# Tiến độ thực hiện Lab 21

Đây là nhật ký thực hiện, chưa phải báo cáo nộp bài. Không dùng các số đo dưới đây
để thay cho NB2–NB5.

## Đã hoàn thành trên máy hiện tại

- Môi trường: Windows, RTX 4060 8 GB; `.env` chọn `LAPTOP`, base
  `Qwen/Qwen3.5-2B`, `MASK_MODE=assistant-only`, `EPOCHS=2`.
- NB1 đã chạy thật với corpus mặc định: 250 mẫu, split seed 42 thành 225 train
  và 25 validation.
- Mask proof: 37/94 token được tính loss (0,3936); câu trả lời được tính loss,
  câu hỏi bị che. Chat template giữ khối `<think>`.
- `check_mask_agreement.py` cho thấy mask tự động của tokenizer bằng 0 token vì
  template không có `{% generation %}`. NB3 dùng dataset đã gắn `labels` theo mask
  được chứng minh ở NB1, nên không dựa vào mask tự động này.
- Độ dài token: p95 = 98, max = 101, gợi ý `max_length=256`. Tier hiện đặt 1024;
  đây là giới hạn chung của tier và cần giải thích trong báo cáo nếu giữ nguyên.
- Kiểm tra mã: 120 test qua. `verify.py` xác nhận dữ liệu gốc và ba artefact NB1.
- Đã sửa `verify.py` để checksum JSONL không báo sai khi Git checkout CRLF trên
  Windows; test vẫn phát hiện khi nội dung nhãn bị đổi.

Artefact đã sinh: `results/mask_proof.json`, `results/template_check.json`,
`results/token_stats.json`, `data/split/train.jsonl`, `data/split/val.jsonl`.

## Chưa thể đo tại máy này

NB2–NB5 cần PyTorch CUDA và trọng số model. Python hiện cài `torch 2.9.1+cpu`.
Wheel CUDA chính thức nặng 1,86 GB; pip tải khoảng 0,3 GB rồi timeout. Thử tải
chia phần cũng chỉ đạt vài trăm KB/s tổng. Không có điểm baseline, loss, VRAM,
verdict hay adapter thật để điền trung thực vào `REPORT.md`.

`python scripts/verify.py` hiện còn 5 FAIL dự kiến: thiếu
`baselines_frozen.json`, `runs.csv`, `verdict.json`, `autopsy.json`, và báo cáo
vẫn là mẫu. Không nộp bài ở trạng thái này.

## Tiếp tục trên Colab T4

Mở `colab/Lab21_RUN_ALL.ipynb` từ repo, chọn GPU T4, chạy các ô theo thứ tự.
Notebook sẽ chạy NB1–NB5 trên model mặc định của tier T4. Vì base model khác
máy hiện tại, dùng toàn bộ artefact mới từ cùng một lượt Colab khi viết report;
không trộn số của hai tier. Sau khi pipeline xong, tải `results/` và ít nhất
`adapters/correct/` về workspace này, rồi viết `submission/REPORT.md` từ số đo
thật và chạy lại `python scripts/verify.py`.

## Lượt Colab T4 do người dùng gửi ngày 2026-10-07

Người dùng đã chạy hết NB1–NB5 trên `unsloth/Qwen3.5-4B`, Tesla T4, fp16,
`EPOCHS=2`, nhưng đặt `EVAL_LIMIT=8`. Đây là lượt thử nhanh, không phải kết quả
nộp bài. Log cho thấy:

- NB1: mask đúng, 39/94 token được tính loss (0,4149); p95 = 98.
- NB2: (a) target 0,000; (b) target 0,6875, format 1,000. Regression (a)
  và (b) đều 0,750.
- NB3: `correct` r=16, 32.464.896 tham số trainable, 30 step, train loss
  0,6271, peak VRAM 8,78 GB.
- NB4: `attn_only` r=283, 32.456.704 tham số, loss 0,5379;
  `wrong_lr` loss 1,5702; `qlora` loss 0,7058, VRAM 3,86 GB. Tất cả 30 step.
- NB5 trên 8 mẫu: fine-tune target 0,9375, regression 0,625, format 1,000;
  verdict FAILED vì regression giảm 0,125 so với (b). `attn_only` hoà
  `correct` trên target 0,9375; `qlora` 0,8438; `wrong_lr` 0,000.

Log Colab cho thấy `verify.py` còn hai FAIL: báo cáo vẫn là mẫu và tập eval
chỉ có 8 mẫu. Nếu runtime cùng artefact còn mở, gỡ `EVAL_LIMIT` rồi **chỉ chạy
lại NB2 và NB5** để đo đủ 50 target, 15 regression; giữ nguyên NB3/NB4. Sau đó
tải `results/` về workspace. Nếu runtime đã mất, cần khôi phục cả bốn adapter
đã train trước khi chạy NB5 hoặc chạy lại pipeline.
