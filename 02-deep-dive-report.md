# 02 — Deep-Dive Report: Xanh SM Incident Router

**Học viên:** Le Nguyen Quoc Bao  
**Đơn vị:** Vin Smart Future / Xanh SM  
**Trạng thái:** Product-scoping prototype, chưa dùng trong vận hành thật

> Các con số trong báo cáo là baseline giả định phục vụ scoping trong lab. Cần
> kiểm chứng bằng incident log, telemetry và phỏng vấn CS/Ops trước pilot.

## 1. Executive Summary

Đề xuất một **incident-routing copilot** hỗ trợ CS/Ops Xanh SM khi tiếp nhận báo
cáo sự cố từ tài xế. Hệ thống đọc free-text, trích xuất các trường quan trọng,
gợi ý mức độ nghiêm trọng và team xử lý, sau đó tạo bản nháp cho điều phối viên
duyệt.

Hệ thống **không tự gửi tin, không tự dispatch và không tự điều xe**. Với pin
dưới 5%, boundary cứng là không đề xuất trạm sạc xa hơn 5 km; thay vào đó phải
gợi ý `dispatch_mobile_charger` và chuyển case đến `emergency-operations`.
Boundary này do rule deterministic kiểm soát, không giao cho LLM tự suy luận.

## 2. Current-State Workflow

![Current-state workflow](04-workflow-diagram.pdf)

| Bước | Actor / hệ thống | Thao tác | Thời gian giả định | Điểm kiểm soát |
|---:|---|---|---:|---|
| 1 | Tài xế | Gửi báo cáo sự cố qua app, chat hoặc điện thoại. | 1 phút | Có thể thiếu pin, GPS, mã xe hoặc mô tả rõ ràng. |
| 2 | CS/Ops | Đọc free-text và diễn giải loại sự cố. | 5 phút | **Bottleneck:** cách diễn đạt không thống nhất. |
| 3 | CS/Ops và tài xế | Gọi/chat để hỏi thông tin còn thiếu. | 2 phút | **Handoff:** CS/Ops ↔ tài xế; có thể phải hỏi lại nhiều lần. |
| 4 | CS/Ops | Gán severity, team và phương án xử lý ban đầu. | 2 phút | **Bottleneck:** có thể bỏ sót pin nguy cấp hoặc route sai team. |
| 5 | Điều phối viên | Chuyển case và theo dõi xử lý. | 1 phút | **Handoff:** CS/Ops → đội xử lý; quyết định vẫn do người duyệt. |

**Tổng baseline giả định:** khoảng **10 phút/case**. Cần đo lại trên tối thiểu
100 incident logs ở các khung giờ khác nhau. Rủi ro lớn nhất là bỏ sót tín hiệu
an toàn hoặc chuyển case sai team trong tình huống gấp.

## 3. Problem Statement — 6 Fields

| Field | Nội dung |
|---|---|
| **1. Actor / Operator** | Tài xế gửi báo cáo; nhân viên CS/Ops đọc và chuẩn hóa; điều phối viên duyệt phương án và chuyển đội xử lý. |
| **2. Current Workflow** | Nhận free-text → đọc và diễn giải → hỏi thông tin thiếu → gán severity/team → chuyển case và theo dõi. |
| **3. Bottleneck** | Tổng hợp thông tin không cấu trúc và nhận diện các tín hiệu an toàn như pin, GPS, mã xe trong nhiều bước thủ công. |
| **4. Business Impact** | Route chậm có thể làm xe nằm ngoài tuyến lâu hơn, tăng thời gian chờ và nguy cơ xử lý sai. Số case/ngày và chi phí thực tế chưa được xác minh. |
| **5. Success Metric** | 90% case có JSON chuẩn hóa trong dưới 30 giây; giảm triage trung bình xuống dưới 3 phút; ít nhất 98% case pin <5% được gắn mobile-charger/escalation đúng. |
| **6. Operational Boundary** | Bắt buộc `[DRAFT_ONLY]`; không tự gửi tin hoặc dispatch; không bịa dữ liệu; pin <5% không được gợi ý trạm >5 km và phải đề xuất `dispatch_mobile_charger`. |

## 4. AI-Fit Analysis

| Phương án | Phù hợp với | Hạn chế | Quyết định |
|---|---|---|---|
| **No AI / thủ công** | Fallback khi hệ thống lỗi hoặc case chưa đủ dữ liệu. | Chậm, khó chuẩn hóa và phụ thuộc nhiều vào kinh nghiệm operator. | Giữ làm fallback bắt buộc. |
| **Rule / state machine** | Ngưỡng pin, khoảng cách, schema, quyền gửi và validation. | Khó hiểu free-text và tạo giải thích tự nhiên. | Bắt buộc cho safety gate. |
| **LLM feature** | Trích xuất field, tóm tắt incident, gợi ý severity/team và tạo draft. | Có thể hallucinate hoặc bị prompt injection. | Dùng sau rule; output chỉ là draft. |
| **Agentic loop** | Gọi nhiều hệ thống và điều phối end-to-end. | Rủi ro hành động sai, quyền truy cập lớn và khó audit. | Không dùng trong scope hiện tại. |

**Kiến trúc được chọn:** deterministic rule engine + LLM extraction/drafting +
human approval. LLM không phải nguồn sự thật cho pin, GPS, khoảng cách hoặc trạng
thái trạm.

## 5. Future-State Flow

1. Incident được tạo từ tài xế hoặc telemetry, gồm `vehicle_id`, pin, GPS và timestamp.
2. **LLM extraction:** trích xuất incident type, severity, pin, vị trí và trường thiếu.
3. **Safety gate:** kiểm tra schema, độ mới dữ liệu, ngưỡng pin và các field bắt buộc.
4. Nếu pin <5%, không đề xuất trạm >5 km; tạo action `dispatch_mobile_charger` và ưu tiên critical.
5. Nếu dữ liệu hợp lệ và pin không ở mức critical, rule/service có thể cung cấp các phương án hợp lệ cho LLM tóm tắt.
6. **Draft step:** tạo JSON có marker `[DRAFT_ONLY]`, routing team, lý do và thông tin cần bổ sung.
7. **Human-in-the-loop:** điều phối viên xem dữ liệu nguồn, rule result và draft; chọn Approve, Edit hoặc Reject.
8. Chỉ sau Approve, hệ thống nghiệp vụ mới thực hiện action đã được duyệt.
9. Lưu input đã ẩn danh, rule result, model/version, draft và quyết định của operator để audit.

```text
[Incident từ tài xế/telemetry]
                                                |
                                                v
[LLM extract fields] --> [Thiếu/xung đột] --> [Hỏi bổ sung hoặc queue thủ công]
                                                |
                                                v
[Safety gate: pin, khoảng cách, schema, freshness]
                                                |
                   +--------+--------+
                   |                 |
       [Pin <5%]        [Dữ liệu hợp lệ]
                   |                 |
                   v                 v
[Mobile charger]  [Draft routing/action]
                   +--------+--------+
                                                v
                   [Dispatcher review]
                                                |
                        Approve / Edit / Reject
```

AI không được gọi API dispatch hay gửi tin trực tiếp. Nếu model timeout, confidence
thấp hoặc trả JSON sai schema, case được giữ trong queue và chuyển quy trình thủ công.

## 6. Fallback và Operational Controls

| Trigger | Hành động fallback |
|---|---|
| Thiếu pin, GPS, mã xe hoặc timestamp | Không tạo action cụ thể; liệt kê `missing_information` và yêu cầu bổ sung. |
| Telemetry quá cũ hoặc mâu thuẫn | Đánh dấu cần xác minh, không tự suy diễn giá trị mới; chuyển operator review. |
| Không truy cập được service bản đồ/trạm | Giữ case trong queue và dùng quy trình tra cứu hiện tại. |
| LLM timeout hoặc output sai schema | Dùng template rule-based hoặc xử lý thủ công; tuyệt đối không tự gửi. |
| Pin <5% | Ưu tiên mobile charger/emergency operations; operator phải xác nhận trước khi dispatch. |
| Operator Reject | Ghi lý do reject để phân tích; không tự động thực hiện phương án bị từ chối. |

## 7. Prototype Contract và Adversarial Tests

Mọi output prototype phải bắt đầu bằng `[DRAFT_ONLY]`, sau đó là JSON hợp lệ. Ví dụ:

```json
{
      "action": "dispatch_mobile_charger",
      "reason": "Battery is below 5%; do not route to a station farther than 5 km.",
      "routing_team": "emergency-operations",
      "missing_information": ["exact_gps"],
      "requires_human_approval": true
}
```

Các nhóm tấn công cần kiểm thử:

- Dụ hệ thống đưa xe pin 2% đến trạm cách 8 km.
- Yêu cầu bỏ marker `[DRAFT_ONLY]` và gửi ngay.
- Giả mạo chỉ dẫn quản trị để đổi ngưỡng pin hoặc tự phê duyệt.
- Cung cấp GPS, mã xe hoặc trạng thái trạm giả để xem model có bịa dữ liệu không.
- Chèn thông tin cá nhân hoặc secret vào nội dung trả về.

## 8. Measurement Plan

### Offline trước pilot

- Lấy tối thiểu 100 incident đã ẩn danh và gắn nhãn phương án đúng bởi hai operator.
- Test boundary tại 4.9%, 5.0%, khoảng cách 4.9 km và 5.1 km.
- Red-team tối thiểu 30 prompt injection/adversarial cases.
- Đo schema validity, boundary violation, latency, routing accuracy và agreement với operator.

### Pilot shadow mode

- Chạy 2 tuần ở chế độ chỉ gợi ý, không ảnh hưởng workflow thật.
- So sánh thời gian triage, acceptance/edit/reject rate và số escalation với baseline.
- Dừng pilot nếu có critical boundary violation hoặc thiếu audit log.

## 9. Risks and Controls

| Rủi ro | Mức độ | Kiểm soát |
|---|---|---|
| Pin/GPS sai khiến đề xuất phương án nguy hiểm | Cao | Freshness check, provenance của dữ liệu và human approval. |
| Prompt injection từ nội dung tài xế | Cao | Tách dữ liệu khỏi chỉ dẫn, allowlist action và validation hậu xử lý. |
| LLM hallucinate trạm hoặc khoảng cách | Cao | LLM không tự tìm trạm; chỉ tóm tắt kết quả từ nguồn đã xác minh. |
| Lộ mã xe/GPS | Cao | Data minimization, access control, retention ngắn và audit. |
| Automation bias của operator | Trung bình | Hiển thị dữ liệu nguồn, lý do rule và nút Edit/Reject rõ ràng. |
| Model hoặc service outage | Trung bình | Template rule-based và quy trình thủ công sẵn có. |

## 10. AI Readiness Checklist

| Câu hỏi | Trạng thái | Bằng chứng / việc cần làm |
|---|---|---|
| Có dữ liệu mẫu/log sạch để test? | **Chưa xác nhận** | Cần trích xuất và ẩn danh incident logs; không coi baseline giả định là dữ liệu thật. |
| Rủi ro AI sai có kiểm soát được? | **Có, với điều kiện** | Safety gate, draft-only, human approval, fallback và audit log. |
| Stakeholder sẵn sàng đổi workflow? | **Chưa xác nhận** | Phỏng vấn CS/Ops và chạy shadow mode trước khi đưa vào queue thật. |

## 11. Decision

### **GO — prototype scope hẹp, không production automation**

Cho phép xây prototype và shadow mode vì boundary an toàn có thể biểu diễn bằng
rule xác định, còn LLM chỉ tạo bản nháp. Chưa cho phép tự động gửi tin hoặc tự
dispatch. Quyết định production chỉ được xem xét sau khi có incident data thật,
red-team không có critical violation, operator acceptance đạt ngưỡng và stakeholder
ký duyệt workflow.

## 1. Phạm vi và lựa chọn

Đề tài là trợ lý cho CS/Ops Xanh SM khi tiếp nhận báo cáo sự cố từ tài xế. AI chỉ
chuẩn hóa báo cáo, gợi ý mức độ nghiêm trọng và team xử lý; điều phối viên vẫn
duyệt mọi hành động. Nhánh được kiểm thử kỹ nhất là xe có pin dưới 5%.

## 2. Current-State Workflow

```text
[Tài xế gửi free-text]
          |  Handoff: tài xế -> CS/Ops
          v
[CS đọc và hiểu sự cố] -- 5 phút -- BOTTLENECK
          |
          v
[Gọi/chat hỏi thông tin thiếu] -- 2 phút -- Handoff
          |
          v
[Gán severity và team] -- 2 phút -- BOTTLENECK
          |
          v
[Chuyển case, theo dõi xử lý] -- 1 phút -- Handoff

Tổng thời gian trung bình: 10 phút/case.
Rủi ro lớn nhất: bỏ sót tình trạng pin nghiêm trọng hoặc route sai team.
```

## 3. Problem Statement (6 fields)

| Field | Nội dung |
|---|---|
| Actor / Operator | Nhân viên CS/Ops và điều phối viên Xanh SM; đầu vào đến từ tài xế. |
| Current Workflow | Nhận free-text qua app/chat/điện thoại, đọc, hỏi lại, phân loại, gán severity, chuyển team và theo dõi. |
| Bottleneck | Hiểu ngôn ngữ không cấu trúc và nhận diện thông tin an toàn quan trọng như pin, vị trí, xe và tình trạng nguy hiểm. |
| Business Impact | Ở quy mô 80 case/ngày, 10 phút/case tương đương khoảng 13 giờ xử lý thủ công/ngày; route chậm kéo dài thời gian xe nằm ngoài tuyến. |
| Success Metric | 90% case có JSON chuẩn hóa trong dưới 30 giây; giảm triage xuống dưới 3 phút; 98% case pin dưới 5% được gắn mobile-charger/escalation đúng. |
| Operational Boundary | Bắt buộc `[DRAFT_ONLY]`; không tự gửi tin, không tự dispatch; pin dưới 5% không được gợi ý trạm quá 5km mà phải đề xuất `dispatch_mobile_charger`; thiếu dữ liệu thì hỏi bổ sung/escalate; không bịa dữ liệu. |

## 4. AI Fit và Future-State Flow

**AI Fit: LLM Feature kết hợp Rule/State Machine.** LLM phù hợp để hiểu free-text
và trích xuất trường; rule cứng bảo vệ ngưỡng pin, khoảng cách và quyền phê duyệt.
Agent tự trị không phù hợp vì hành động sai ảnh hưởng an toàn và vận hành.

```text
[Nhận incident]
      |
      v
🔵 [LLM extract: loại lỗi, pin, GPS, xe, severity, missing fields]
      |
      v
[Safety gate: rule pin < 5%, khoảng cách, field bắt buộc]
      |                         \
      | pass                      \ thiếu dữ liệu / xung đột
      v                           v
🔵 [Draft routing + action]    ↩️ [Fallback: giữ case ở queue,
      |                         hỏi bổ sung hoặc điều phối thủ công]
      v
🟢 [Dispatcher review và approve]
      |
      v
[Hệ thống vận hành thực hiện action đã duyệt]
```

AI không được gọi API dispatch hay gửi tin trực tiếp. Nếu model lỗi, timeout,
không đủ confidence hoặc trả JSON sai schema, hệ thống giữ nguyên case và dùng
quy trình thủ công.

## 5. Đánh giá độ sẵn sàng và quyết định

| Tiêu chí | Đánh giá | Bằng chứng / việc cần làm |
|---|---|---|
| Có dữ liệu mẫu sạch? | NOT YET | Cần tối thiểu 500 incident đã gán nhãn, ẩn dữ liệu cá nhân và có ground truth về severity/team. |
| Rủi ro có kiểm soát? | GO trong pilot | Có safety gate, `[DRAFT_ONLY]`, HITL và fallback; không cho AI tự dispatch. |
| Stakeholder sẵn sàng? | Cần xác nhận | Chạy shadow mode với một nhóm CS/Ops trước khi đưa vào queue thật. |

**Quyết định: NOT YET cho production, GO cho prototype/pilot giới hạn.** Lý do là
giá trị vận hành rõ và rủi ro có thể khoanh vùng, nhưng cần baseline dữ liệu và
đánh giá độ chính xác trước khi mở rộng. Pilot nên chạy 2 tuần ở shadow mode,
so sánh thời gian triage, routing accuracy và tỷ lệ escalation với quy trình cũ.
