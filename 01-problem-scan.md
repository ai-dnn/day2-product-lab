# 01 — Problem Scan & Quick Problem Cards

**Học viên:** Le Nguyen Quoc Bao  
**Vai trò giả định:** AI Product Engineer, Vin Smart Future  
**Phạm vi được chọn:** Xanh SM Incident Router

## Phase 1 — SCAN

Mục tiêu của bước scan là tìm các quy trình có đầu vào không cấu trúc, có thao
tác lặp lại hoặc tốn thời gian, có điểm chuyển giao rõ và có thể đo được kết quả.
Các cơ hội dưới đây được giữ ở mức scoping; chưa giả định rằng AI được phép tự
thực hiện hành động vận hành.

| # | Công ty | Lens | Bài toán vận hành quan sát được | Actor chịu ảnh hưởng | Dữ liệu cần xác minh | Cơ hội AI |
|---|---|---|---|---|---|---|
| 1 | Xanh SM | Stakeholder pain + time-consuming | Khi tài xế báo sự cố bằng free-text, CS/Ops phải đọc, hỏi lại thông tin thiếu, gán mức độ và chuyển đúng team. | Tài xế, CS/Ops, điều phối viên, hành khách | Incident text, pin, GPS, mã xe, lịch sử case, nhãn severity/team | Chuẩn hóa incident, trích xuất field, gợi ý severity và routing có người duyệt. |
| 2 | VinFast | Repetitive + time-consuming | Nhân viên đọc mô tả lỗi xe không đồng nhất, xác định nhóm lỗi và hỏi lại triệu chứng còn thiếu. | Nhân viên tiếp nhận, kỹ thuật viên, chủ xe | Nội dung ticket, mã lỗi, model xe, lịch sử sửa chữa, nhãn kỹ thuật | Chuẩn hóa symptom, phân loại ticket và tạo câu hỏi intake; không tự chẩn đoán. |
| 3 | Vinhomes | Repetitive + AI-upgrade | CSKH đọc phản ánh cư dân, xác định category, mức khẩn cấp, bộ phận xử lý và soạn phản hồi ban đầu. | CSKH, ban quản lý, cư dân | Ticket đa kênh, tòa/căn hộ, SLA, category, lịch sử phản hồi | Phân loại, trích xuất thông tin, phát hiện mức khẩn cấp và draft phản hồi. |
| 4 | Vinpearl | Time-consuming | Yêu cầu đổi/hủy vé, booking hoặc hỏi dịch vụ phải tra nhiều chính sách trong mùa cao điểm. | CSKH, khách du lịch, quản lý dịch vụ | Booking, loại vé, chính sách hiệu lực, lịch sử hội thoại | Nhận diện intent, tra policy và tạo draft; trường hợp ngoại lệ cần escalation. |
| 5 | Xanh SM | Repetitive + AI-upgrade | Điều phối xe đến điểm đón phải cân nhắc ETA, pin, ùn tắc và nhu cầu theo khu vực. | Điều phối viên, tài xế, khách hàng | GPS, ETA, pin, traffic, nhu cầu lịch sử, log phân bổ | Dự báo/ranking ứng viên và cảnh báo xe không đủ pin; quyết định cuối vẫn theo rule/operator. |

### Tiêu chí sàng lọc

- **Giá trị vận hành:** Có thể giảm thời gian triage hoặc giảm chuyển sai team.
- **Khả năng làm prototype:** Có thể mô phỏng bằng text input, field extraction và rule.
- **Rủi ro:** Có thể kiểm soát bằng safety gate, thiếu dữ liệu và human-in-the-loop.
- **Khả năng đo:** Có baseline thời gian, routing accuracy và tỷ lệ escalation.

## So sánh và lựa chọn

Chấm theo thang 1–5, trong đó 5 là mức thuận lợi/giá trị cao hơn.

| Tiêu chí | Xanh SM Incident Router | VinFast Service Assistant | Vinhomes Ticket Assistant |
|---|---:|---:|---:|
| Giá trị vận hành | 5 | 4 | 4 |
| Dữ liệu có khả năng sẵn có | 4 | 4 | 3 |
| Scope prototype trong lab | 5 | 4 | 4 |
| Rủi ro kiểm soát bằng rule/HITL | 4 | 3 | 3 |
| Khả năng đo metric | 5 | 4 | 4 |
| **Tổng** | **23** | **19** | **18** |

### Lựa chọn để deep-dive

Chọn **Xanh SM Incident Router — chuẩn hóa báo cáo sự cố tài xế**. Bài toán có
pain trực tiếp từ stakeholder, đầu vào free-text phù hợp với LLM feature và có
handoff rõ giữa tài xế, CS/Ops và điều phối viên. Prototype tập trung vào nhánh
xe có pin dưới 5% để kiểm tra boundary: không hướng xe đến trạm quá 5 km,
không tự gửi tin hoặc tự dispatch, và luôn giữ `[DRAFT_ONLY]` cho người duyệt.

## Phase 2 — QUICK PROBLEM CARDS

### Quick Problem Card 1 — Xanh SM Incident Router (được chọn)

| Thuộc tính | Nội dung |
|---|---|
| **Bài toán** | Tài xế gửi báo cáo sự cố bằng ngôn ngữ tự do, khiến CS/Ops mất thời gian đọc, chuẩn hóa và chuyển đúng team. |
| **Actor / operator** | Tài xế là người gửi; CS/Ops và điều phối viên là operator; hành khách có thể chịu tác động gián tiếp. |
| **Workflow hiện tại** | Nhận tin nhắn → đọc và diễn giải → hỏi thông tin thiếu → gán severity/team → chuyển case và theo dõi. |
| **Bottleneck** | Đọc free-text, phát hiện tín hiệu an toàn như pin/GPS và chuyển đúng team; baseline giả định 8–12 phút/case. |
| **AI hỗ trợ** | Extract `incident_type`, `severity`, `vehicle_id`, `location`, `battery_percent`, `missing_information`; gợi ý action và routing. |
| **Metric** | 90% case có JSON chuẩn hóa trong dưới 30 giây; giảm triage trung bình xuống dưới 3 phút; 100% case pin <5% không gợi ý trạm >5 km. |
| **Quick architecture** | LLM feature + safety rule/state machine + human-in-the-loop; fallback về queue thủ công khi thiếu dữ liệu hoặc model lỗi. |
| **Rủi ro / boundary** | Không bịa GPS, xe hoặc trạm; không gửi tin/dispatch trực tiếp; pin <5% phải đề xuất mobile charger và chuyển emergency operations. |

### Quick Problem Card 2 — VinFast Service Description Assistant

| Thuộc tính | Nội dung |
|---|---|
| **Bài toán** | Mô tả lỗi xe bằng tiếng Việt không đồng nhất khiến nhân viên service phải hỏi lại nhiều lần. |
| **Actor / operator** | Nhân viên tiếp nhận là operator; kỹ thuật viên và chủ xe là các bên chịu tác động. |
| **Workflow hiện tại** | Nhận mô tả → đọc triệu chứng → xác định nhóm lỗi → hỏi thông tin thiếu → chuyển xưởng. |
| **Bottleneck** | Xác định component/triệu chứng và trường còn thiếu; baseline giả định 6–10 phút/case. |
| **AI hỗ trợ** | Chuẩn hóa symptom, trích xuất component và sinh câu hỏi bổ sung theo template. |
| **Metric** | 85% case có đủ trường intake sau một lượt hỏi; giảm thời gian tiếp nhận xuống dưới 3 phút. |
| **Quick architecture** | LLM feature + schema validation + human review; không tự chẩn đoán hoặc hướng dẫn sửa chữa. |
| **Rủi ro chính** | Model suy diễn nguyên nhân hỏng hoặc bỏ sót lỗi an toàn; mọi chẩn đoán vẫn thuộc kỹ thuật viên. |

### Quick Problem Card 3 — Vinhomes Resident Ticket Assistant

| Thuộc tính | Nội dung |
|---|---|
| **Bài toán** | Ticket cư dân cần được phân loại, ưu tiên, chuyển đúng bộ phận và soạn phản hồi ban đầu. |
| **Actor / operator** | CSKH và ban quản lý là operator; cư dân là người gửi và nhận phản hồi. |
| **Workflow hiện tại** | Nhận ticket → đọc nội dung → xác định category/priority → route → soạn phản hồi → duyệt và gửi. |
| **Bottleneck** | Đọc ticket đa kênh và soạn phản hồi phù hợp; baseline giả định 10–15 phút/ticket. |
| **AI hỗ trợ** | Trích xuất tòa/căn hộ/vấn đề, gợi ý priority/team và tạo draft theo policy hiện hành. |
| **Metric** | 90% ticket được route đúng; giảm thời gian draft từ khoảng 10 phút xuống dưới 2 phút. |
| **Quick architecture** | LLM feature + policy retrieval + human review; các case phí, pháp lý, an ninh hoặc khẩn cấp phải escalation. |
| **Rủi ro chính** | Lộ dữ liệu cư dân, bỏ sót tình huống khẩn cấp hoặc gửi phản hồi ngoài policy. |
