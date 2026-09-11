# Bài lab đã chuẩn bị - bắt đầu tại đây

**Thư mục:** `F:\AIbai2`

**Nhánh hiện tại:** `codex/lab02-draft`

**Đề tài:** Xanh SM - trợ lý soạn nháp hỗ trợ tài xế báo pin yếu.

**Cập nhật Groq:** đã thêm `--provider groq`, 47 kiểm thử tại máy đạt. Hai lần kiểm tra key đọc từ ảnh đều nhận HTTP 401 từ Groq; chưa xác thực thành công và chưa chạy suy luận với Groq. Cần nhập lại key bằng thao tác Copy của Groq để loại trừ nhầm ký tự trong ảnh.

Đây là bản nháp có AI hỗ trợ để bạn đọc, kiểm tra và hoàn thiện trước khi nộp. Người dùng đã xác nhận [ai-dnn/day2-product-lab](https://github.com/ai-dnn/day2-product-lab) là repo nhận bài; `origin` trỏ tới repo này. Nhánh bài làm là `codex/lab02-draft`. Thông tin tên/mã sinh viên và tên nhóm trong báo cáo vẫn cần người học xác nhận.

## Đọc bài làm

1. [Quét 6 bài toán và 3 Quick Cards](01-problem-scan.md).
2. [Báo cáo phân tích sâu](02-deep-dive-report.md).
3. [Nhật ký dùng AI trung thực](03-ai-log.md).
4. [Sơ đồ quy trình PDF](04-workflow-diagram.pdf).
5. [Prototype Python](starter-code/prompt_prototype.py).

Số liệu vận hành được ghi rõ là giả định; cần thay bằng số thực đo nếu bạn có dữ liệu. Reflection cá nhân cần bạn đọc, sửa và bổ sung trải nghiệm thật.

## Chạy tại máy Windows

Môi trường `.venv` đã được tạo với Python 3.12.14 từ runtime đi kèm; đã cài `requirements.txt`. Không cần activate nếu dùng đường dẫn Python bên dưới. `.venv` chỉ dùng trên máy này; khi chuyển máy hãy tạo lại bằng Python 3.10+.

Mở PowerShell tại `F:\AIbai2`:

```powershell
# Kiểm thử tại máy, không gọi Gemini
.\.venv\Scripts\python.exe -m pytest -q

# Demo bằng dữ liệu mô phỏng, KHÔNG phải phản hồi Gemini
.\.venv\Scripts\python.exe starter-code/prompt_prototype.py --offline-demo --report verification/offline-demo.json

# Bộ chấm kiểm tra sự có mặt của các file báo cáo
.\.venv\Scripts\python.exe autograder/autograder.py --section-a
```

## Dùng Groq theo yêu cầu bổ sung

Key Groq dùng biến `GROQ_API_KEY`, không đặt vào `GEMINI_API_KEY`. Nhập key trực tiếp trên máy bằng PowerShell, ký tự sẽ được che:

```powershell
$labGroqKey = Read-Host 'Dan key vua Copy tu Groq' -AsSecureString
$env:GROQ_API_KEY = [System.Net.NetworkCredential]::new('', $labGroqKey).Password
Remove-Variable labGroqKey

.\.venv\Scripts\python.exe starter-code/prompt_prototype.py --provider groq --report verification/live-groq-results.json
```

Model mặc định cho Groq là `llama-3.3-70b-versatile`; có thể chọn model khác bằng `GROQ_MODEL`. Nếu phản hồi bị chặn/lỗi, chương trình báo thất bại và chuyển fallback; không tự chuyển sang provider khác. Kết quả ghi rõ `provider=groq` và `mode=live_groq`.

Đề bài gốc yêu cầu Gemini 2.5 Flash. Kết quả Groq không thay thế bằng chứng đã chạy Gemini; cần ghi rõ khác biệt này khi nộp. Mặc định của code vẫn là Gemini. Tham khảo [hướng dẫn chính thức Groq](https://console.groq.com/docs/quickstart).

Khi dùng xong, gỡ key khỏi phiên:

```powershell
Remove-Item Env:GROQ_API_KEY
```

## Phần còn cần làm để có kết quả Gemini thật

Chưa có API key trong phiên chuẩn bị. Nhập key **trực tiếp tại PowerShell của bạn**, không gửi vào cuộc trò chuyện hoặc lưu trong code. Ví dụ sau che ký tự khi nhập và không đặt key trong lịch sử lệnh:

```powershell
$labGeminiKey = Read-Host 'Gemini API key' -AsSecureString
$env:GEMINI_API_KEY = [System.Net.NetworkCredential]::new('', $labGeminiKey).Password
Remove-Variable labGeminiKey

.\.venv\Scripts\python.exe starter-code/prompt_prototype.py --report verification/live-results.json
```

Lệnh trên gọi `gemini-2.5-flash` cho 4 ca tổng hợp, có thể dùng quota/chi phí API của bạn. Nếu model không còn dùng được cho tài khoản, xem model hiện có rồi đặt `$env:GEMINI_MODEL`; ghi lại model đã dùng trong bài.

Đọc `raw_output` trong báo cáo live để đánh giá nội dung `reason`. Dòng `Passed structural checks` chỉ chứng minh nhãn/JSON/rule hợp lệ; không thay thế kiểm tra nghĩa bằng người. Nếu cần sửa prompt, chạy lại và ghi kết quả thật vào AI log.

Chạy toàn bộ autograder khi đã có key:

```powershell
.\.venv\Scripts\python.exe autograder/autograder.py
```

Autograder giới hạn subprocess 30 giây cho cả lượt chạy. Nếu API chậm, chạy prototype trực tiếp để phân biệt timeout của bộ chấm với lỗi ranh giới. Không đổi output hoặc sửa bộ chấm để che lỗi. Khi xong có thể gỡ key khỏi phiên PowerShell:

```powershell
Remove-Item Env:GEMINI_API_KEY
```

## Trạng thái xác minh

- 47 kiểm thử pytest tại máy đã đạt sau khi thêm Groq; kết quả ở [verification/pytest-groq.txt](verification/pytest-groq.txt). Log 38 tests trước đó vẫn giữ để đối chiếu.
- Demo offline có 4 fixture được gắn nhãn; không gọi Gemini.
- Autograder hiện báo **8/10, exit code 1**: đủ file và đạt 3 kiểm tra code tĩnh; 2 kiểm tra chạy Gemini chưa đạt vì thiếu API key. Xem [log gốc](verification/autograder.txt). Đây không phải điểm bài lab cuối cùng.
- Chưa xác nhận kết quả Gemini, chất lượng nghiệp vụ hay điểm giảng viên. Bộ chấm kiểm tra file hiện diện không chấm chất lượng báo cáo.

## Trước khi nộp

1. Điền tên/mã sinh viên và tên nhóm; đổi nhánh theo tên cá nhân nếu cần.
2. Repo đích đã được người dùng xác nhận là `ai-dnn/day2-product-lab`; kiểm tra bài trên nhánh `codex/lab02-draft`.
3. Bổ sung lần chạy Gemini và reflection của chính bạn.
4. Với mỗi lần cập nhật tiếp theo, commit và push lên nhánh cá nhân. Chỉ trưởng nhóm chọn các báo cáo `.md` và sơ đồ đưa vào `main`; code `.py` vẫn ở nhánh cá nhân.
5. Trưởng nhóm điền form nộp bài theo README của lớp.

Lịch sử commit/push được theo dõi trên [nhánh bài làm](https://github.com/ai-dnn/day2-product-lab/tree/codex/lab02-draft). Push bản nháp không đồng nghĩa đã hoàn tất kiểm thử API hoặc nộp form; form chưa được nộp trong phiên làm việc này.
