# Report về Vinfast #1

## Current-State Workflow Mapping
1. Khách hàng gửi yêu cầu bảo hành
2. Khách hàng gửi yêu cầu bảo hành
3. Đọc và hiểu mô tả lỗi
4. Xác định loại lỗi (Pin / Sạc / Phần mềm / Khác)
5. Chuyển yêu cầu đến bộ phận phù hợp
6. Nhân viên kỹ thuật tiếp nhận
7. Xử lý/phản hồi khách hàng

Thời gian dự kiến: ~7 phút/lượt
- Bottleneck: Đọc mô tả lỗi và xác định loại lỗi, đặc biệt khi khách hàng mô tả vấn đề bằng ngôn ngữ tự nhiên hoặc không dùng thuật ngữ kỹ thuật.
- Handoff: Nhân viên CSKH → Bộ phận kỹ thuật/bảo hành.

## Problem Statement (6-field) & Metrics
Nhân viên CSKH VinFast mất thời gian đọc và phân loại thủ công các yêu cầu bảo hành, đặc biệt khi khách hàng mô tả lỗi bằng ngôn ngữ tự nhiên. AI có thể hỗ trợ tự động phân loại và tóm tắt yêu cầu để giảm thời gian xử lý, trong khi quyết định kỹ thuật và bảo hành vẫn thuộc về nhân viên chuyên trách.

| Field | Nội dung chi tiết |
|---|---|
| **1. Actor / Operator** | Nhân viên CSKH / nhân viên tiếp nhận yêu cầu bảo hành. |
| **2. Current Workflow** | Nhân viên nhận yêu cầu → đọc mô tả lỗi → xác định loại lỗi → chuyển đến bộ phận phù hợp → phản hồi khách hàng. |
| **3. Bottleneck** | Đọc và phân loại mô tả lỗi thủ công. Khách hàng có thể mô tả cùng một vấn đề bằng nhiều cách khác nhau, gây chậm hoặc phân loại sai. |
| **4. Business Impact** | Giả sử 1.000 yêu cầu/ngày × 5 phút cho đọc + phân loại = ~83 giờ nhân sự/ngày. Phân loại sai cũng có thể gây thêm một vòng chuyển ticket. |
| **5. Success Metric** |≥90% classification accuracy/F1 và giảm thời gian đọc + phân loại từ ~5 phút → <1 phút/ticket. |
| **6. Operational Boundary** | AI được phép phân loại, extract triệu chứng và tóm tắt yêu cầu. AI không được phép tự xác nhận lỗi kỹ thuật, quyết định bảo hành, cam kết chi phí hoặc hướng dẫn sửa chữa nguy hiểm. Case không rõ hoặc confidence thấp → Human Review/Fallback. |

## Future-State Flow & AI Fit
* **AI fit**: LLM Feature
* **Future-State Flow**:
Khách hàng gửi yêu cầu
        ↓
🔵 AI: Extract thông tin lỗi
        ↓
🔵 AI: Classify
(Pin / Sạc / Phần mềm / Khác)
        ↓
🔵 AI: Tóm tắt vấn đề
        ↓
Confidence Check
        ↓
   ┌───────────────┐
   │               │
High confidence   Low confidence /
   │               │ unclear
   ↓               ↓
Tự động tạo      ↩️ Fallback
ticket draft       ↓
   │           🟢 Human Review
   ↓
🔄 Chuyển bộ phận
bảo hành phù hợp
        ↓
🟢 Nhân viên xử lý
quyết định cuối cùng

## Operational Boundary
AI được phép:
* Phân loại loại lỗi
* Extract thông tin từ mô tả
* Tóm tắt yêu cầu
* Gợi ý bộ phận tiếp nhận

AI không được phép:
* Tự chẩn đoán lỗi kỹ thuật
* Tự xác nhận điều kiện bảo hành
* Tự quyết định từ chối/chấp nhận bảo hành
* Hướng dẫn khách hàng thực hiện thao tác nguy hiểm với pin/xe

## AI Readiness Checklist:
1. [ YES ] Chúng tôi có sẵn dữ liệu mẫu/logs sạch để test?
2. [ YES ] Rủi ro khi AI sai có nằm trong tầm kiểm soát (qua HITL hoặc Fallback)?
3. [ YES ] Stakeholders sẵn sàng thay đổi quy trình làm việc cũ?

## Quyết định cuối cùng
NO-GO