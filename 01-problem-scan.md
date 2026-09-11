# SCAN

| # | Subsidiary | Lens | Mô tả ngắn bài toán |
|---|---|---|---|
| 1 | Xanh SM | Lặp lại | Nhân viên phải đọc, phân loại và chuyển hàng nghìn yêu cầu như lỗi app, thanh toán, chuyến đi, khách hủy chuyến, lost & found. |
| 2 | Vinfast | Lặp lại |Phân loại yêu cầu bảo hành như tự động phân loại các yêu cầu theo lỗi pin hay sạc. |
| 3 | Vinhomes | Resident AI Assistant để trả lời câu hỏi về phí dịch vụ, tiện ích, quy định và giờ hoạt động.|
| 4 | Xanh SM | Pain từ người khác | Tài xế gặp khó khăn khi điểm đón do khách nhập không rõ, GPS sai hoặc vị trí thực tế khác vị trí trên app.|
| 5 | Vinmec | Pain từ người khác | Điều phối lịch khám để phát hiện lịch trùng hoặc đề xuất slot phù hợp.|

# QUICK-ASSESS
Top 3 ý tưởng từ danh sách SCAN: #1 Xanh SM, #2 VinFast, và #3 Vinhomes.

```
┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #01                                     │
│                                                             │
│ Bài toán (1 câu): AI tự động phân loại và tóm tắt yêu cầu  │
│ hỗ trợ từ tài xế Xanh SM.                                  │
│                                                             │
│ Công ty thành viên: [ ] VinFast  [x] Xanh SM  [ ] Vinhomes │
│                      [ ] Vinmec                            │
│                                                             │
│ Ai đang đau (Actor)? Tài xế và nhân viên CSKH/Support      │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                     │
│ 1. Nhận yêu cầu → 2. Đọc nội dung → 3. Phân loại →         │
│ 4. Chuyển bộ phận xử lý → 5. Phản hồi tài xế              │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Phân loại & chuyển ticket │
│ (⏱ ~3 phút/lượt)                                           │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│ Phân loại, tóm tắt và đề xuất bộ phận xử lý.               │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian xử lý ticket từ ~3 phút → dưới 30 giây;     │
│ classification accuracy >90%.                              │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #02                                     │
│                                                             │
│ Bài toán (1 câu): AI tự động phân loại yêu cầu bảo hành    │
│ xe VinFast theo loại lỗi như pin, sạc hoặc phần mềm.      │
│                                                             │
│ Công ty thành viên: [x] VinFast  [ ] Xanh SM [ ] Vinhomes │
│                      [ ] Vinmec                            │
│                                                             │
│ Ai đang đau (Actor)? Nhân viên bảo hành và khách hàng      │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                     │
│ 1. Nhận yêu cầu → 2. Đọc mô tả lỗi → 3. Xác định loại lỗi │
│ → 4. Chuyển bộ phận → 5. Liên hệ khách hàng               │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Xác định loại lỗi         │
│ (⏱ ~5 phút/lượt)                                           │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│ Extract thông tin lỗi và phân loại yêu cầu bảo hành.       │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian phân loại từ ~5 phút → dưới 1 phút;         │
│ classification F1 >90%.                                    │
│                                                             │
│ Quick Architecture: [ ] No AI  [x] Rule + LLM [ ] Agent   │
└─────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│ QUICK PROBLEM CARD #03                                     │
│                                                             │
│ Bài toán (1 câu): AI trợ lý trả lời tự động các câu hỏi    │
│ thường gặp của cư dân Vinhomes.                            │
│                                                             │
│ Công ty thành viên: [ ] VinFast  [ ] Xanh SM [x] Vinhomes │
│                      [ ] Vinmec                            │
│                                                             │
│ Ai đang đau (Actor)? Cư dân và nhân viên CSKH              │
│                                                             │
│ Workflow thủ công hiện tại (3-5 bước):                     │
│ 1. Cư dân gửi câu hỏi → 2. Nhân viên đọc → 3. Tìm thông   │
│ tin → 4. Soạn phản hồi → 5. Gửi cư dân                    │
│                                                             │
│ Bước nào tốn thời gian/lỗi nhất? Tìm thông tin & soạn      │
│ phản hồi (⏱ ~5 phút/lượt)                                  │
│                                                             │
│ AI có thể nhảy vào hỗ trợ ở bước nào?                       │
│ Hiểu câu hỏi và tạo câu trả lời dựa trên policy có sẵn.   │
│                                                             │
│ Đo thành công bằng gì (Metric có số)?                       │
│ Giảm thời gian phản hồi từ ~5 phút → dưới 1 phút;          │
│ answer accuracy >90%.                                      │
│                                                             │
│ Quick Architecture: [ ] No AI  [ ] Rule  [x] LLM  [ ] Agent│
└─────────────────────────────────────────────────────────────┘
```