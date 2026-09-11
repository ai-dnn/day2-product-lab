# Lab 02 - Problem Scan & Quick Cards

**Bối cảnh:** Vin Smart Future theo tình huống học tập của đề bài.

**Người làm / nhóm:** chưa được cung cấp; cần điền trước khi nộp.

**Trạng thái:** bản nháp có AI hỗ trợ, ngày 11/09/2026.

> Các quy trình và số liệu dưới đây là giả thuyết phục vụ scoping, không phải kết quả khảo sát doanh nghiệp. Chưa phỏng vấn nhân viên, chưa truy cập logs nội bộ. Mỗi metric là mục tiêu thử nghiệm cần kiểm chứng. Tên đơn vị được dùng theo phạm vi trong worksheet.

## Phase 1 - SCAN qua 4 lenses

| # | Đơn vị | Lens | Bài toán / người chịu ảnh hưởng | Dữ liệu cần xác minh |
|---|---|---|---|---|
| 1 | Xanh SM | Tốn thời gian | Điều phối viên đọc tin báo pin yếu, đối chiếu thông tin và soạn nháp hỗ trợ; tài xế chờ phản hồi. | Tin nhắn đã ẩn danh, thời điểm nhận/duyệt, pin xác minh. |
| 2 | Vinhomes | AI-upgrade | Nhân viên phân loại phản ánh cư dân viết bằng ngôn ngữ tự nhiên, chuyển đúng đội xử lý. | Ticket và nhãn bộ phận do nhân viên xác nhận. |
| 3 | VinFast | Lặp lại | Nhân viên đối chiếu dòng hóa đơn sạc với giao dịch; ngoại lệ cần kiểm tra thủ công. | Bảng giao dịch và hóa đơn đã loại bỏ định danh. |
| 4 | Vinpearl / VinWonders | Pain từ người khác | Nhân viên nhận yêu cầu khách thiếu ngày, địa điểm hoặc loại dịch vụ, phải hỏi lại nhiều lần. | Hội thoại đã ẩn danh, danh mục thông tin bắt buộc. |
| 5 | Xanh SM | Lặp lại | Nhân viên tổng hợp lý do hủy chuyến từ ghi chú để lập báo cáo vận hành. | Ghi chú, nhãn lý do, số lần nhân viên sửa phân loại. |
| 6 | Vinmec | Tốn thời gian | Nhân viên hành chính kiểm tra hồ sơ đặt lịch thiếu giấy tờ trước khi tiếp nhận. | Danh mục giấy tờ và dữ liệu mô phỏng, không dùng bệnh án thật. |

Chọn #1, #2 và #3 để so sánh một bài toán soạn nháp, một bài toán phân loại và một bài toán có khả năng chỉ cần rule.

## Phase 2 - QUICK-ASSESS

### Card 1 - Xanh SM: nháp hỗ trợ sự cố pin yếu

| Trường | Nội dung |
|---|---|
| Bài toán | Rút ngắn thời gian điều phối viên chuẩn bị phản hồi cho tài xế báo pin yếu, giữ người duyệt mọi hành động. |
| Actor | Điều phối viên là người dùng trực tiếp; tài xế chịu thời gian chờ. |
| Workflow hiện tại, giả định | 1. Nhận báo cáo → 2. Xác minh pin/vị trí → 3. Tra phương án hỗ trợ → 4. Soạn và kiểm tra tin → 5. Chuyển đề xuất cho người có thẩm quyền. |
| Bottleneck | Bước 3-4 giả định chiếm 8 phút trong tổng 13 phút thao tác/lượt. |
| AI hỗ trợ | Tóm tắt lý do từ tin nhắn cho người duyệt; tạo đề xuất JSON. Rule kiểm tra ngưỡng pin và mẫu nháp. |
| Metric | Mục tiêu median thời gian soạn/kiểm tra từ 4 xuống ≤2 phút, tính cả lượt phải sửa hoặc fallback; 0 hành động tự gửi. |
| Kiến trúc | Rule + LLM Feature; không Agent. Ngưỡng pin không cần LLM quyết định. |
| Dữ liệu thiếu | Baseline thực đo, pin xác minh, quy trình duyệt, tính khả dụng của hỗ trợ hiện trường. |
| Ranh giới | `dispatch_mobile_charger` chỉ là đề xuất theo bài lab; không chứng minh doanh nghiệp có dịch vụ này tại mọi nơi. |

### Card 2 - Vinhomes: phân loại yêu cầu cư dân

| Trường | Nội dung |
|---|---|
| Bài toán | Hỗ trợ nhân viên nhận diện chủ đề ticket và gợi ý đội phụ trách. |
| Actor | Nhân viên CSKH và đội vận hành tiếp nhận ticket. |
| Workflow hiện tại, giả định | 1. Nhận ticket → 2. Đọc nội dung → 3. Chọn nhãn → 4. Chuyển đội → 5. Theo dõi và chuyển lại nếu sai. |
| Bottleneck | Đọc và chọn nhãn giả định 3 phút/ticket; thông tin nhiều chủ đề dễ bị chuyển sai. |
| AI hỗ trợ | Gợi ý nhãn từ danh mục đóng và lý do ngắn; nhân viên xác nhận. |
| Metric | Mục tiêu median phân loại từ 3 xuống ≤1 phút; macro-F1 ≥0,90 trên 100 ticket giữ riêng, có nhãn chuyên viên; báo riêng tỷ lệ chuyển lại. |
| Kiến trúc | Thử rule từ khóa làm baseline; chỉ bổ sung LLM nếu giảm lỗi ở câu mơ hồ. |
| Ranh giới | Không phán quyết tranh chấp, không sửa phí và không tự hứa thời hạn xử lý. |

### Card 3 - VinFast: đối chiếu hóa đơn sạc

| Trường | Nội dung |
|---|---|
| Bài toán | Phát hiện giao dịch không khớp giữa bảng kê và hóa đơn để nhân viên kiểm tra. |
| Actor | Nhân viên đối soát. |
| Workflow hiện tại, giả định | 1. Xuất bảng kê → 2. Chuẩn hóa mã/thời gian → 3. Ghép giao dịch → 4. Đánh dấu lệch → 5. Nhân viên xác nhận. |
| Bottleneck | Ghép và kiểm tra thủ công giả định 30 phút/100 dòng. |
| AI hỗ trợ | Chưa cần LLM nếu đầu vào đã có cấu trúc. Dùng join, ngưỡng sai số và danh sách ngoại lệ. |
| Metric | Mục tiêu ≤5 phút/100 dòng gồm kiểm tra ngoại lệ; phát hiện 100% chênh lệch được cài sẵn trong 20 ca mô phỏng. |
| Kiến trúc | Rule / script Python. Chỉ xem xét OCR nếu hóa đơn là ảnh và phát sinh nhu cầu thật. |
| Ranh giới | Không tự sửa sổ hoặc thực hiện thanh toán. |

## Quyết định chọn bài toán

Chọn **Card 1 - Xanh SM** cho phần deep-dive vì có actor, điểm duyệt và ranh giới rõ; đồng thời khớp các quy tắc pin và nhãn nháp trong starter code/bộ chấm. Đây là quyết định xây dựng bản nháp của phiên làm việc này, chưa phải biên bản thống nhất nhóm.

Card 2 cần danh mục nhãn và dữ liệu đúng của vận hành. Card 3 nên bắt đầu bằng rule; thêm LLM ở bước đối chiếu số không có lợi ích rõ. Ngay với Card 1, LLM chỉ đáng dùng nếu giúp tóm tắt tin nhắn tốt hơn mẫu nháp cố định; thử nghiệm phải so sánh với phương án rule + template.

## Kiểm chứng tiếp theo

1. Nhờ đại diện vận hành xác nhận 5 bước và người có quyền duyệt.
2. Đo 30 lượt xử lý để thay toàn bộ baseline giả định.
3. Chuẩn bị tập tin nhắn được phép sử dụng, loại bỏ biển số, số điện thoại và vị trí chính xác.
4. Chạy đối chứng rule + template trước khi kết luận cần LLM.

**Nguồn yêu cầu:** [worksheet](01-worksheet.md), [starter code](starter-code/prompt_prototype.py), [quy định nộp bài](README.md).
