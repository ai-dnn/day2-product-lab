# Lab 02 - AI Log & Reflection

**Trạng thái:** nhật ký do trợ lý ghi theo phiên làm việc thực tế ngày 11/09/2026. Người học cần đọc, sửa và bổ sung phản ánh cá nhân trước khi nộp. Không coi phần này là lời tự thuật đã được người học xác nhận.

## 1. Tương tác đã xảy ra

| Mốc | Yêu cầu / hành động thật | Kết quả và giới hạn |
|---|---|---|
| 1 | Người học gửi link `ai-dnn/day2-product-lab` và hỏi “giờ tôi cần làm gì”. | Trợ lý đọc README, kiểm tra thư mục máy và giải thích các file cần nộp. |
| 2 | Người học yêu cầu “Làm đi”. | Trợ lý tải repo, tạo nhánh `codex/lab02-draft`, tạo `.venv`, cài requirements. |
| 3 | Trợ lý hỏi tùy chọn lĩnh vực và thông tin cá nhân/nhóm. | Chưa có câu trả lời lúc soạn bản nháp; không tự điền tên, mã sinh viên hoặc repo nhóm. |
| 4 | Trợ lý đọc worksheet, ví dụ, starter code và autograder. | Phát hiện code và bộ chấm có quy tắc riêng của Xanh SM, nên chọn use case pin yếu và thông báo lại. |
| 5 | Trợ lý viết báo cáo và prototype. | Có system prompt, JSON contract, bốn ca tấn công, validator, fallback và pytest. |
| 6 | Trợ lý chạy kiểm thử tại máy. | 38 tests vượt qua; adapter Gemini được mock trong test. Autograder báo 8/10, còn hai tiêu chí live chưa đạt vì thiếu Gemini API key. |
| 7 | Người học gửi ảnh API key và yêu cầu sử dụng. | Ảnh là trang Groq. Trợ lý thêm chế độ Groq riêng và 9 kiểm thử bổ sung, tổng 47 tests đạt. |
| 8 | Trợ lý đọc key trong ảnh bằng OCR tại máy, thử endpoint danh sách model. | Hai lần Groq trả HTTP 401, kể cả sau tăng kích thước ảnh trong bộ nhớ để nhận dạng. Chưa gọi suy luận; không đưa key vào code/báo cáo và không ghi kết quả live thành công. |
| 9 | Người học hỏi khả năng push và xác nhận link repo `ai-dnn/day2-product-lab`. | Dùng repo này làm đích của nhánh bản nháp `codex/lab02-draft`; giữ ghi nhận rõ các kiểm thử API chưa hoàn tất. |

Không có cuộc phỏng vấn nhân viên, cuộc họp nhóm, lần chạy Gemini thật hoặc kết quả chấm của giảng viên nào được thực hiện trong nhật ký này.

Lỗi xác thực Groq không phải hallucination của mô hình và không chứng minh mô hình thất bại ở các ca tấn công. Cần key được nhập chính xác để tiếp tục kiểm thử live. Trợ lý không gửi key Groq tới Gemini.

## 2. AI đã giúp gì?

AI giúp phân rã đề bài thành deliverables, tìm ràng buộc ẩn trong starter code, xây dựng bản so sánh Rule/LLM/Agent và viết code kiểm tra phản hồi. Báo cáo tách thời gian soạn nháp khỏi thời gian toàn quy trình để tránh tuyên bố giảm 13 phút xuống 2 phút khi chỉ cải tiến một bước.

AI hỗ trợ dựng test âm: mất nhãn đầu dòng, giả mạo vai trò quản lý, tin nhắn sửa pin, JSON trùng key, giá trị `"true"` thay cho boolean và phản hồi rỗng. Người học có thể dùng các ca này để giải thích vì sao kiểm tra chuỗi đơn giản chưa đủ.

## 3. Sai sót, giới hạn và cách sửa đã xảy ra

**Chọn hướng quá sớm:** trợ lý ban đầu gợi ý Vinpearl/VinFast/Vinhomes khi mới đọc README. Đọc starter code sau đó cho thấy bộ chấm gắn với Xanh SM và ngưỡng pin. Đã sửa hướng bằng cách dùng bài toán Xanh SM nhất quán giữa báo cáo, code và sơ đồ. Bài học: phải đối chiếu worksheet, code và cách chấm trước khi chốt đề tài.

**Truy cập tài liệu:** một số trang file GitHub không tải được qua trình duyệt công cụ. Trợ lý tải repo rồi đọc bản local; không suy diễn nội dung file từ thông báo lỗi.

**Giới hạn bằng chứng:** số liệu thời gian chưa có nguồn thực địa. Bản nháp ghi rõ “giả định” và xây kế hoạch đo; không dựng lời kể “đã khảo sát”. Chưa quan sát hallucination của Gemini vì chưa gọi mô hình. Các ví dụ trả lời sai trong tests là fixture do người viết test tạo để kiểm tra validator, không phải câu trả lời Gemini đã tạo.

## 4. Ranh giới đã đưa vào prompt và code

- Tách `system_instruction` khỏi tin nhắn tài xế, coi tin nhắn là dữ liệu không đáng tin.
- Tách pin xác minh mô phỏng khỏi số pin mà tài xế tự viết; không tự động tin dữ liệu trong câu tấn công.
- Yêu cầu `[DRAFT_ONLY]` ở đầu, boolean duyệt và một JSON object không có trường lạ.
- Đối chiếu pin bằng rule tại máy; dùng mẫu cố định cho phần nháp hướng tới tài xế.
- Giữ `reason` cho người duyệt kiểm tra nghĩa; không tuyên bố validator có thể phát hiện mọi thông tin bịa.
- Tách demo offline và live test, giữ exit code lỗi khi chưa có key hoặc khi phản hồi bị chặn.

Đây là mô tả thiết kế/hiện thực của trợ lý trong phiên này, không phải chuỗi nhiều lần tinh chỉnh prompt đã thử trên Gemini.

## 5. Phần người học cần bổ sung sau khi chạy thật

1. Điền họ tên/mã sinh viên và phần việc cá nhân đã trực tiếp đọc, sửa hoặc chạy.
2. Chạy prototype với Gemini, lưu `verification/live-results.json`, đọc từng `raw_output` và ghi nội dung sai nếu có.
3. Nếu sửa prompt, lưu trích đoạn trước/sau và chạy lại cùng ca để có so sánh thật.
4. Viết nhận xét cá nhân về việc AI giúp/không giúp, nêu một quyết định mà người học tự đưa ra sau khi kiểm chứng.

Không thay các bước chưa làm bằng trải nghiệm tưởng tượng. Việc hoàn thành reflection cá nhân cần sự tham gia của người học.
