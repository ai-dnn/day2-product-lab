# Kết quả kiểm tra - 11/09/2026

| Bằng chứng | Kết quả | Cách hiểu |
|---|---|---|
| [pytest.txt](pytest.txt) | 38 passed | Kiểm tra chương trình và adapter SDK bằng mock; không gọi Gemini. |
| [pytest-groq.txt](pytest-groq.txt) | 47 passed | Kết quả mới sau khi thêm Groq; HTTP/adapter được mock trong unit tests. |
| [groq-auth-check.json](groq-auth-check.json) | HTTP 401, hai lần | Groq từ chối giá trị key đọc từ ảnh. Chưa có phản hồi suy luận; không lưu key trong bằng chứng này. |
| [offline-demo.json](offline-demo.json) | 4/4 fixture qua validator | `mode=offline_fixture`, `llm_was_called=false`. Không đo khả năng chống prompt injection của mô hình. |
| [autograder.txt](autograder.txt) | 8/10, exit code 1 | Đủ 4 file + 3 tiêu chí code tĩnh. Code tiêu chí 4-5 chưa đạt vì chế độ live trả exit code 2 khi thiếu API key. |
| PDF | 1 trang A3 ngang | Đã render bằng Poppler và kiểm tra trực quan: tiếng Việt hiển thị đúng, không tràn/chồng chữ. |
| Git | `git diff --check` thành công | Nhánh `codex/lab02-draft`; repo đích `ai-dnn/day2-product-lab` đã được người dùng xác nhận. Lịch sử thay đổi nằm trong Git. |

8/10 là kết quả kỹ thuật của autograder đi kèm repo, **không phải điểm bài lab cuối cùng**. Bộ chấm này kiểm tra sự tồn tại file, dấu hiệu code và đầu ra script; không xác nhận chất lượng báo cáo hay dữ liệu nghiệp vụ.

Chưa có `live-results.json`. Sau khi có key, chạy lệnh trong `00-BAT-DAU.md`, đọc nội dung phản hồi và bổ sung bằng chứng mới. Giữ các kết quả offline được ghi nhãn rõ.

Chưa có `live-groq-results.json` vì kiểm tra xác thực thất bại. Log autograder 8/10 là lần chạy Gemini trước khi bổ sung Groq; chưa chạy lại autograder với Groq. Kết quả từ provider khác không tự đáp ứng yêu cầu Gemini của worksheet.
