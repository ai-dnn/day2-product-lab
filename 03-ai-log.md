# 03 — AI Log & Reflection

## AI đã hỗ trợ gì?

Mình dùng AI như một thought-partner để brainstorm pain point theo bốn lens,
so sánh các ý tưởng trong bảng được cung cấp, rút gọn phạm vi và chuyển một
quy trình free-text thành các field có thể đo. AI cũng giúp tạo các tình huống
adversarial như tài xế thúc giục bỏ qua bước duyệt hoặc yêu cầu đi tới trạm sạc
quá xa khi pin còn 2%.

## AI có thể sai ở đâu?

Các con số về số case mỗi ngày, thời gian xử lý và doanh thu trong bản nháp chỉ
là giả định để lập scope, không phải số liệu công bố của doanh nghiệp. AI cũng có
thể nhầm giữa “gợi ý hành động” và “thực hiện hành động”, hoặc tự điền vị trí,
loại xe và trạm sạc khi input không có dữ liệu.

## Cách mình sửa prompt và ranh giới

1. Gắn `[DRAFT_ONLY]` ở đầu mọi output và bắt buộc human review.
2. Tách LLM extraction khỏi safety gate bằng rule: pin dưới 5% thì dùng
   `dispatch_mobile_charger`, không đề xuất trạm trên 5km.
3. Yêu cầu JSON có field `missing_information`, cấm bịa dữ liệu và chuyển case
   sang `needs_human_review` khi thiếu field hoặc model không chắc chắn.
4. Không cho model trả lời tư vấn y khoa, pháp lý hoặc hướng dẫn sửa xe; các vấn
   đề đó phải chuyển người có thẩm quyền.

## Kết quả kiểm thử

Prototype có hai test chính: yêu cầu bỏ qua `[DRAFT_ONLY]` và yêu cầu pin 2% đi
đến trạm cách 8km. Fallback cục bộ cũng giữ đúng hai ranh giới khi chưa có API
key. Khi triển khai thật, cần log input/output đã ẩn danh, đo precision/recall
theo từng loại sự cố và review các case model không chắc chắn.
