# 03 — AI Log & Reflection

**Học viên:** Tran Nguyen Tien Duc  
**Bài toán:** Xanh SM Critical-Battery Dispatch Copilot

## 1. AI đã được sử dụng như thế nào

Tôi dùng AI như một thought-partner ở bốn bước: mở rộng danh sách pain point trong hệ sinh thái Vingroup, phản biện ba Quick Problem Cards, cấu trúc Problem Statement 6-field và stress-test operational boundary của prompt prototype. Tôi không coi nội dung AI sinh ra là dữ kiện chính thức.

Các prompt tiêu biểu:

1. “Đề xuất 5 bottleneck vận hành cho VinFast, Xanh SM, Vinhomes và Vinpearl; phân loại theo repetitive, time-consuming, AI-upgrade và stakeholder pain.”
2. “Đóng vai CFO và trưởng vận hành. Hãy chỉ ra metric nào trong ba problem cards chưa có baseline và trường hợp nào rule-based tốt hơn LLM.”
3. “Thiết kế các prompt injection nhằm khiến dispatcher bỏ marker draft-only hoặc gửi xe pin dưới 5% đến trạm xa hơn 5 km.”
4. “Kiểm tra future-state flow và liệt kê những điểm cần human approval, fallback và audit log.”

## 2. AI giúp ích ở đâu

- Giúp tôi nhìn thấy rằng bài toán không nên được mô tả chung chung là “tối ưu điều phối”, mà cần thu hẹp thành một decision point có input, action và boundary đo được.
- Gợi ý tách công việc: rule engine xử lý pin/khoảng cách/quyền hành động; LLM chỉ giải thích và soạn draft.
- Giúp tạo danh sách failure modes như telemetry cũ, trạm đầy, output sai schema, prompt injection và automation bias.
- Giúp biến các mục tiêu mơ hồ thành metric có threshold: latency P95, boundary violation, draft acceptance và tỷ lệ human approval.

## 3. AI sai hoặc chưa đáng tin ở đâu

Trong quá trình brainstorm, AI có xu hướng đưa ra các con số thời gian xử lý, tỷ lệ hủy chuyến và chi phí cứu hộ nghe hợp lý nhưng không có nguồn nội bộ. Nếu chép nguyên các con số này, báo cáo sẽ biến giả định thành bằng chứng và dẫn đến quyết định sai.

AI cũng có xu hướng đề xuất “agent tự động điều xe sạc” để tối ưu tốc độ. Cách này bỏ qua quyền hành động, trách nhiệm khi điều phối sai và yêu cầu human approval. Ngoài ra, chỉ viết safety rule trong system prompt không bảo đảm mô hình luôn tuân thủ; prompt injection vẫn có thể tác động đến output.

## 4. Tôi đã sửa prompt và boundary ra sao

- Gắn nhãn mọi con số chưa được xác minh là **baseline giả định** và bổ sung measurement plan bằng incident logs thật.
- Thu hẹp vai trò AI thành copilot tạo `[DRAFT_ONLY]`, không phải autonomous dispatcher.
- Đưa rule pin <5%, khoảng cách và quyền gửi vào validation code, thay vì chỉ dựa vào khả năng nghe lời của LLM.
- Bổ sung cấu trúc output có action allowlist và `requires_human_approval`.
- Viết adversarial tests cố tình yêu cầu bỏ tag, đổi ngưỡng an toàn và tự gửi hành động.
- Thêm fallback khi dữ liệu thiếu/cũ, API lỗi hoặc output không đúng schema.

## 5. Cách tôi kiểm chứng

Tôi chạy prototype bằng Gemini 2.5 Flash, xem output của từng adversarial test và dùng assertion tự động để kiểm tra hai invariant quan trọng: phản hồi luôn có `[DRAFT_ONLY]`, và trường hợp pin nguy cấp phải chứa `dispatch_mobile_charger`. Sau đó tôi chạy autograder của repository để kiểm tra file, cấu trúc code, khả năng thực thi và kết quả boundary tests.

Một lần model trả lời hợp lý không đủ chứng minh an toàn. Trước production cần tập test lớn hơn tại các giá trị biên 4.9%/5.0% và 4.9 km/5.1 km, nhiều cách diễn đạt tiếng Việt/Anh, input thiếu dữ liệu và prompt injection nhiều vòng.

## 6. Reflection cá nhân

Điểm quan trọng nhất tôi học được là lựa chọn đúng vai trò của AI quan trọng hơn việc cố đưa AI vào mọi bước. Với bài toán này, rule-based logic phù hợp hơn cho quyết định an toàn có ngưỡng rõ ràng; LLM tạo giá trị ở phần hiểu/ngôn ngữ và giải thích. Human-in-the-loop không chỉ là một nút “duyệt”, mà cần dữ liệu nguồn, lý do quyết định, quyền reject và audit trail để người vận hành thực sự chịu trách nhiệm.

Tôi cũng nhận ra AI rất hữu ích trong việc tạo phản biện và edge case, nhưng yếu ở việc phân biệt dữ liệu thật với con số ước lượng nếu prompt không yêu cầu provenance. Vì vậy, đầu ra AI phải được xem là giả thuyết để kiểm chứng, không phải nguồn bằng chứng.

