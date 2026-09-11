# Lab 02 — Deep-Dive Report

## Dự án được chọn

**Vinhomes — Phân loại và điều hướng phản ánh cư dân.**

## 1. Current-State Workflow

1. Cư dân gửi phản ánh tự do qua ứng dụng hoặc tổng đài. *(~1 phút)*
2. CSKH mở ticket, đọc nội dung và kiểm tra tòa nhà/căn hộ. **🔴 Bottleneck** *(~4 phút)*
3. CSKH xác định loại vấn đề và mức ưu tiên. **🔴 Bottleneck** *(~2 phút)*
4. CSKH chuyển ticket cho ban quản lý/đội kỹ thuật. **🔄 Handoff** *(~1 phút)*
5. Ban quản lý phân công người xử lý. **🔄 Handoff** *(~2 phút)*
6. Bộ phận phụ trách cập nhật kết quả; CSKH phản hồi cư dân. *(~5 phút)*

**Tổng thời gian xử lý ban đầu trước khi phân công: khoảng 10 phút/ticket.**

## 2. Problem Statement — 6 Fields

| Field | Nội dung |
|---|---|
| 1. Actor / Operator | Nhân viên CSKH, ban quản lý tòa nhà và đội kỹ thuật. |
| 2. Current Workflow | CSKH đọc ticket tự do, kiểm tra thông tin, phân loại, chọn nơi xử lý và chuyển ticket. |
| 3. Bottleneck | Mô tả không đồng nhất/thiếu thông tin; nhiều loại vấn đề; dễ chuyển sai hoặc đặt sai mức ưu tiên. |
| 4. Business Impact | Chậm SLA phản hồi, tăng thời gian thao tác của CSKH, làm cư dân phải chờ lâu và dễ hài lòng thấp. |
| 5. Success Metric | ≥85% ticket được đề xuất đúng category/đội phụ trách; phản hồi phân loại dưới 10 giây; giảm xử lý ban đầu từ 10 phút xuống dưới 3 phút. |
| 6. Operational Boundary | AI chỉ phân loại, trích xuất, đề xuất và tạo nháp. AI không tự chuyển/đóng ticket, không cam kết xử lý hay tiết lộ dữ liệu. Case cháy nổ, rò điện, an ninh hoặc y tế phải chuyển người trực khẩn cấp. |

## 3. AI Fit & Future-State Flow

**AI Fit: LLM Feature.** Lý do: ticket là ngôn ngữ tự do, cần hiểu ngữ cảnh và chuẩn hóa thành các trường có cấu trúc. Quyết định vận hành vẫn thuộc về nhân viên; không cần Agentic Loop.

1. Cư dân gửi phản ánh.
2. **🔵 AI Step:** LLM phân loại category, priority, đội phụ trách; tạo bản tóm tắt và phản hồi nháp dạng JSON.
3. **🟢 Human-in-the-loop:** CSKH kiểm tra/sửa/duyệt đề xuất.
4. CSKH chuyển ticket đã duyệt đến đúng bộ phận. **🔄 Handoff**
5. Ban quản lý phân công và cập nhật tiến độ. **🔄 Handoff**
6. CSKH gửi phản hồi đã duyệt cho cư dân.

**↩️ Fallback:** Nếu JSON không hợp lệ, mô hình thiếu tự tin, ticket thiếu thông tin hoặc phát hiện từ khóa khẩn cấp, đưa ticket vào hàng đợi thủ công; hiển thị cảnh báo cho người trực trong các case nguy hiểm.

## 4. Evaluate — AI Readiness Checklist

| Câu hỏi | Đánh giá | Bằng chứng / việc cần làm |
|---|---|---|
| Có dữ liệu mẫu/logs sạch để test? | Chưa đầy đủ | Cần lấy ticket lịch sử đã ẩn danh, gán nhãn category/priority/đội phụ trách trước khi test. |
| Rủi ro AI sai có kiểm soát được? | Có | CSKH duyệt toàn bộ đề xuất; case khẩn cấp đi theo fallback thủ công. |
| Stakeholders sẵn sàng đổi quy trình? | Có điều kiện | Cần pilot với một tòa nhà và đào tạo CSKH sử dụng màn hình duyệt. |

## 5. Quyết định

**NOT YET — Cần tích lũy dữ liệu và xác lập baseline trước khi triển khai thật.**

Nhóm nên xây prompt prototype với dữ liệu giả lập/đã ẩn danh ngay bây giờ, nhưng chưa triển khai vận hành. Trước khi GO, cần ít nhất một tập ticket đã gán nhãn để đo accuracy, baseline thời gian xử lý hiện tại và quy trình escalation rõ ràng cho sự cố khẩn cấp.
