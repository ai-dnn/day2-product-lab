# 01 — Problem Scan & Quick Assessment

**Học viên:** Tran Nguyen Tien Duc  
**Vai trò giả định:** AI Product Engineer, Vin Smart Future  
**Ngày thực hiện:** 11/09/2026

> Các con số trong tài liệu là baseline giả định phục vụ scoping trong lab, không phải số liệu vận hành chính thức của Vingroup. Trước khi triển khai cần kiểm chứng bằng ticket, telemetry và phỏng vấn stakeholder.

## Phase 1 — SCAN

| # | Công ty | Lens | Bài toán vận hành quan sát được | Actor chịu ảnh hưởng | Dữ liệu cần xác minh |
|---:|---|---|---|---|---|
| 1 | Xanh SM | Stakeholder pain, time-consuming | Khi xe báo pin yếu, điều phối viên phải đối chiếu thủ công vị trí xe, mức pin, khoảng cách trạm và khả năng tiếp nhận trước khi hướng dẫn tài xế. | Tài xế, điều phối viên, hành khách | Telemetry pin/GPS, danh sách trạm, trạng thái trụ sạc, log điều phối |
| 2 | Xanh SM | Repetitive, AI-upgrade | Phân bổ tài xế đến điểm đón chưa xét đầy đủ ETA, pin còn lại, ùn tắc và nhu cầu theo khu vực. | Điều phối viên, tài xế, khách hàng | GPS, ETA, pin, nhu cầu lịch sử, traffic |
| 3 | VinFast | Time-consuming, repetitive | Ticket bảo hành được đọc và phân loại thủ công, dễ chuyển sai nhóm kỹ thuật hoặc thiếu dữ liệu cần thiết. | Nhân viên CSKH, cố vấn dịch vụ | Nội dung ticket, mã lỗi xe, lịch sử sửa chữa, nhãn xử lý |
| 4 | Vinhomes | Repetitive, AI-upgrade | Phản ánh cư dân đến từ nhiều kênh, cần phân loại, phát hiện mức khẩn cấp và soạn phản hồi ban đầu. | Ban quản lý, CSKH, cư dân | Ticket đa kênh, SLA, danh mục sự cố, lịch sử phản hồi |
| 5 | Vinpearl | Time-consuming, stakeholder pain | Yêu cầu đổi/hoàn vé và thay đổi đặt phòng phải tra nhiều chính sách, làm thời gian phản hồi kéo dài vào mùa cao điểm. | Nhân viên CSKH, khách du lịch | Booking, loại vé, chính sách hiện hành, lịch sử hội thoại |

## Phase 2 — QUICK-ASSESS

### Quick Problem Card 1 — Điều phối xe pin nguy cấp

| Thuộc tính | Nội dung |
|---|---|
| **Bài toán** | Giảm thời gian và rủi ro khi xử lý xe Xanh SM có mức pin nguy cấp trong lúc vận hành. |
| **Công ty** | Xanh SM |
| **Actor** | Điều phối viên là operator chính; tài xế và hành khách là người chịu tác động. |
| **Workflow hiện tại** | (1) Tài xế báo pin yếu → (2) điều phối đọc pin/GPS → (3) tra trạm và khoảng cách → (4) gọi xác nhận hoặc chọn phương án → (5) gửi hướng dẫn. |
| **Bottleneck** | Đối chiếu pin, khoảng cách và khả năng sạc trên nhiều màn hình; baseline giả định **8 phút/lượt**. |
| **AI hỗ trợ** | Tổng hợp ngữ cảnh, áp rule an toàn và tạo bản nháp phương án cho điều phối viên duyệt. |
| **Metric** | P95 thời gian tạo phương án ≤ **30 giây**; **100%** trường hợp pin <5% không đề xuất trạm >5 km; 100% hành động gửi ra ngoài có người duyệt. |
| **Quick Architecture** | **Rule + LLM feature + Human-in-the-loop**; không dùng agent tự gửi lệnh. |
| **Rủi ro chính** | Telemetry cũ, trạm đã đầy, LLM làm sai rule hoặc tự suy diễn khoảng cách. |

### Quick Problem Card 2 — Gợi ý điểm đón và phân bổ tài xế

| Thuộc tính | Nội dung |
|---|---|
| **Bài toán** | Giảm chuyến nhận cuốc có ETA dài hoặc không phù hợp với mức pin hiện tại của xe. |
| **Công ty** | Xanh SM |
| **Actor** | Điều phối viên, tài xế và khách đặt xe. |
| **Workflow hiện tại** | (1) Nhận yêu cầu → (2) lọc xe gần → (3) tài xế nhận/từ chối → (4) phân bổ lại nếu thất bại. |
| **Bottleneck** | Phân bổ lại nhiều vòng trong giờ cao điểm; baseline giả định **3 phút/cuốc lỗi**. |
| **AI hỗ trợ** | Mô hình dự báo ETA/nhu cầu xếp hạng ứng viên; rule loại xe không đủ pin. |
| **Metric** | Giảm tỷ lệ phân bổ lại từ baseline giả định 12% xuống < **7%**; ETA đón P90 < **8 phút**. |
| **Quick Architecture** | **ML prediction + Rule**; LLM không phải thành phần quyết định chính. |
| **Rủi ro chính** | Bias theo khu vực, dữ liệu traffic trễ, tối ưu ETA làm giảm công bằng cho tài xế. |

### Quick Problem Card 3 — Phân loại phản ánh cư dân

| Thuộc tính | Nội dung |
|---|---|
| **Bài toán** | Rút ngắn thời gian phân loại và phản hồi bước đầu cho phản ánh của cư dân Vinhomes. |
| **Công ty** | Vinhomes |
| **Actor** | Nhân viên CSKH, ban quản lý tòa nhà và cư dân. |
| **Workflow hiện tại** | (1) Nhận tin đa kênh → (2) đọc và phân loại → (3) kiểm tra tòa/căn hộ → (4) chuyển bộ phận → (5) soạn phản hồi. |
| **Bottleneck** | Đọc nội dung tự do và chuyển đúng nhóm; baseline giả định **10 phút/ticket**. |
| **AI hỗ trợ** | LLM trích xuất trường dữ liệu, phân loại và soạn bản nháp; rule ưu tiên cháy, thang máy, an ninh. |
| **Metric** | ≥ **85%** ticket được gợi ý đúng nhóm trong <10 giây; giảm thời gian xử lý bước đầu xuống < **3 phút**. |
| **Quick Architecture** | **LLM feature + Rule + Human review**. |
| **Rủi ro chính** | Bỏ sót tình huống khẩn cấp, lộ dữ liệu cư dân, phản hồi thiếu đồng cảm. |

## So sánh và lựa chọn

| Tiêu chí (1–5) | Pin nguy cấp | Phân bổ tài xế | Phản ánh cư dân |
|---|---:|---:|---:|
| Giá trị vận hành | 5 | 5 | 4 |
| Dữ liệu có khả năng sẵn có | 4 | 3 | 4 |
| Scope prototype trong lab | 5 | 2 | 4 |
| Rủi ro có thể kiểm soát bằng rule/HITL | 4 | 3 | 4 |
| Khả năng đo metric | 5 | 4 | 4 |
| **Tổng** | **23** | **17** | **20** |

**Bài toán được chọn:** Điều phối xe Xanh SM có pin nguy cấp. Scope hẹp, có thể biểu diễn boundary rõ ràng và kiểm thử adversarial trong thời gian lab.

