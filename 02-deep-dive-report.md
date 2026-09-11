# 02 — Deep-Dive Report: Xanh SM Incident Router

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
