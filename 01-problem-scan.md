# 01 — Problem Scan & Quick Problem Cards

## Phase 1: SCAN

Các ý tưởng dưới đây được tham khảo từ bảng pain point đã cung cấp. Mình ưu tiên
các tác vụ có dữ liệu đầu vào là free-text, có handoff rõ và có thể đo được thời
gian xử lý.

| # | Công ty | Lens | Bài toán vận hành | Cơ hội AI |
|---|---|---|---|---|
| 1 | Vinhomes | Time-consuming + AI-upgrade | CSKH đọc ticket cư dân, xác định loại vấn đề, ưu tiên, bộ phận xử lý và soạn phản hồi. | Phân loại ticket, trích xuất thông tin, đề xuất route, draft phản hồi. |
| 2 | VinFast | Repetitive + Time-consuming | Nhân viên đọc mô tả lỗi xe tự do, xác định nhóm lỗi và thông tin còn thiếu. | Chuẩn hóa mô tả, phân loại lỗi, hỏi bổ sung thông tin. |
| 3 | Xanh SM | Stakeholder Pain + Time-consuming | Báo cáo sự cố từ tài xế là free-text, CS/Ops phải đọc và chuyển đúng team. | Chuẩn hóa incident report, gợi ý severity và routing. |
| 4 | Vinpearl | AI-upgrade | Tin nhắn về booking, hoàn/hủy, giờ hoạt động và dịch vụ được diễn đạt không thống nhất. | Intent classification và draft trả lời theo policy. |
| 5 | Vinhomes | Repetitive | Yêu cầu sửa chữa có thể bị trùng hoặc sai category. | Phát hiện duplicate và phân loại plumbing/electric/elevator. |


## Lựa chọn để deep-dive

Chọn **#3 — Chuẩn hóa báo cáo sự cố tài xế Xanh SM**. Đây là bài toán có pain trực
tiếp từ stakeholder, dữ liệu free-text phù hợp với LLM feature, nhưng hành động
cuối cùng vẫn cần điều phối viên phê duyệt. Prototype tập trung vào nhánh sự cố
pin thấp để kiểm tra operational boundary.

## Phase 2: QUICK PROBLEM CARDS

### Card #1 — Xanh SM Incident Router

- **Bài toán:** Tài xế gửi báo cáo sự cố bằng ngôn ngữ tự do, khiến CS/Ops mất thời gian đọc, chuẩn hóa và chuyển đúng team.
- **Actor:** Tài xế, nhân viên CS và điều phối viên vận hành.
- **Workflow:** Nhận tin nhắn → đọc và hiểu sự cố → hỏi thông tin thiếu → gán severity/team → chuyển case.
- **Bottleneck:** Đọc và chuẩn hóa free-text, khoảng 8–12 phút/lượt.
- **AI step:** Extract trường dữ liệu, phân loại incident, gợi ý severity và routing.
- **Metric:** 90% case được chuẩn hóa trong dưới 30 giây; giảm thời gian triage trung bình từ 10 xuống dưới 3 phút.
- **Architecture:** LLM feature + rule-based safety gate + HITL.

### Card #2 — VinFast Service Description Assistant

- **Bài toán:** Mô tả lỗi xe bằng tiếng Việt không đồng nhất, khiến nhân viên service phải hỏi lại nhiều lần.
- **Actor:** Nhân viên tiếp nhận và kỹ thuật viên service.
- **Workflow:** Nhận mô tả → đọc triệu chứng → xác định nhóm lỗi → hỏi thông tin thiếu → chuyển xưởng.
- **Bottleneck:** Xác định nhóm lỗi và thông tin thiếu, khoảng 6–10 phút/lượt.
- **AI step:** Chuẩn hóa symptom, extract component và sinh câu hỏi bổ sung.
- **Metric:** 85% case có đủ trường cần thiết sau một lượt hỏi; giảm thời gian intake xuống dưới 3 phút.
- **Architecture:** LLM feature, không tự chẩn đoán hay chỉ dẫn sửa chữa.

### Card #3 — Vinhomes Resident Ticket Assistant

- **Bài toán:** Ticket cư dân cần được phân loại, ưu tiên, route và draft phản hồi.
- **Actor:** CSKH và ban quản lý tòa nhà.
- **Workflow:** Nhận ticket → đọc nội dung → tìm category → route → soạn phản hồi → duyệt và gửi.
- **Bottleneck:** Đọc ticket và soạn phản hồi, khoảng 10–15 phút/lượt.
- **AI step:** Extract căn hộ/vấn đề, gợi ý priority/team và draft theo policy.
- **Metric:** 90% ticket được route đúng; giảm thời gian draft từ 10 xuống dưới 2 phút.
- **Architecture:** LLM feature + policy retrieval + HITL; tranh chấp phí/pháp lý luôn escalation.
