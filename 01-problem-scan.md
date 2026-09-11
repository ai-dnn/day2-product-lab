# 01 — Problem Scan & Quick Assessment

> **Trạng thái:** Bản hoàn thiện Phase 1 (SCAN) và Phase 2 (QUICK-ASSESS).
>
> **Mục tiêu:** Xây dựng ngân hàng đề tài AI cho các công ty và thương hiệu vận hành chính trong hệ sinh thái Vingroup, sau đó chọn ít nhất 5 pain point để SCAN và 3 bài toán để đánh giá bằng Quick Problem Cards.
>
> **Lưu ý:** Danh sách công ty dựa trên tài liệu công khai của Vingroup đến tháng 9/2026. Các pain point và metric gợi ý dưới đây là **giả thuyết cho bài lab**, không phải dữ liệu vận hành đã được doanh nghiệp xác nhận.

## 1. Tiêu chí chọn bài toán

Ưu tiên bài toán thỏa phần lớn các điều kiện sau:

- Xảy ra thường xuyên và có quy trình hiện tại tương đối rõ.
- Có một bước lặp lại, tốn thời gian hoặc dễ sai do xử lý thủ công.
- Có actor cụ thể đang chịu ảnh hưởng.
- Có thể đo được baseline và mục tiêu cải thiện bằng số.
- AI chỉ hỗ trợ ở một bước có ranh giới rõ; không tự động quyết định các hành động rủi ro cao.
- Có thể kiểm thử bằng dữ liệu mẫu hoặc prompt prototype trong phạm vi lab.

Không chọn bài toán chỉ vì nghe có vẻ “thông minh”. Nếu rule-based hoặc một thay đổi quy trình đơn giản giải quyết tốt hơn, ghi nhận điều đó trong card.

## 2. Ngân hàng đề tài theo hệ sinh thái Vingroup

### Công nghiệp và công nghệ

| Công ty / thương hiệu | Đề tài có thể SCAN | Lens chính | Hướng giải pháp ban đầu |
|---|---|---|---|
| **VinFast** | Phân loại mô tả lỗi xe bằng ngôn ngữ tự nhiên và gợi ý checklist chẩn đoán ban đầu cho cố vấn dịch vụ | AI có thể tốt hơn | Retrieval + LLM; kỹ thuật viên xác nhận |
| **VinFast** | Phát hiện lỗi bề mặt linh kiện hoặc sai lắp ráp từ ảnh tại dây chuyền | Lặp lại | Computer vision |
| **Green SM / GSM** | Tóm tắt và phân loại nguyên nhân hủy chuyến từ ghi âm, chat và ghi chú tài xế | Tốn thời gian | Speech-to-text + classifier/LLM |
| **Green SM / GSM** | Gợi ý điều phối xe tới vùng cầu cao trong khi vẫn bảo đảm mức pin và khả năng tiếp cận trạm sạc | Pain từ stakeholder | Forecast + optimization; dispatcher phê duyệt |
| **V-Green** | Phân loại nguyên nhân trụ sạc lỗi từ telemetry và lịch sử bảo trì để ưu tiên ticket | Tốn thời gian | Rules + anomaly detection + LLM summary |
| **V-Green** | Dự báo nhu cầu sạc theo địa điểm và khung giờ để lên kế hoạch công suất | AI có thể tốt hơn | Time-series forecasting |
| **VinMetal** | Phát hiện khuyết tật bề mặt thép từ camera kiểm tra chất lượng | Lặp lại | Computer vision |
| **VinMetal** | Dự báo tiêu thụ năng lượng và cảnh báo vận hành lệch chuẩn trong sản xuất | AI có thể tốt hơn | Forecast + anomaly detection |
| **VinSmart Future** | Trợ lý tìm kiếm tài liệu kỹ thuật nội bộ có trích nguồn và kiểm soát quyền truy cập | Tốn thời gian | Retrieval + LLM |
| **VinSmart Future** | Phân loại và route ticket sự cố dữ liệu hoặc hạ tầng tới đúng nhóm xử lý | Lặp lại | Rules + classifier |
| **VinSOC** | Gom nhóm cảnh báo bảo mật trùng lặp và dựng timeline sự cố cho analyst | Lặp lại | Correlation rules + LLM summary |
| **VinCSS** | Ưu tiên báo cáo lỗ hổng theo tài sản bị ảnh hưởng, khả năng khai thác và tác động | Tốn thời gian | Rules + retrieval; chuyên gia xác nhận |
| **VinRobotics** | Phân tích log thử nghiệm robot để nhóm các failure mode và tạo báo cáo test | Lặp lại | Clustering + LLM summary |
| **VinRobotics** | Kiểm tra bằng thị giác xem robot đã hoàn thành đúng bước thao tác trong nhà máy | AI có thể tốt hơn | Computer vision |
| **VinMotion** | Phân tích video và telemetry của robot hình người để phát hiện mất cân bằng hoặc thao tác thất bại | AI có thể tốt hơn | Multimodal anomaly detection |
| **VinDynamics** | Tìm kiếm episode thử nghiệm tương tự khi robot gặp lỗi và gợi ý checklist điều tra | Tốn thời gian | Vector search + LLM; kỹ sư quyết định |
| **VinSpace** | Phân loại bất thường trong test log và draft báo cáo trong quy trình AIT | Lặp lại | Rules + anomaly detection + LLM |
| **VinSpace** | Sàng lọc ảnh vệ tinh có mây, nhiễu hoặc thiếu vùng quan tâm trước khi giao analyst | Lặp lại | Computer vision + quality rules |

### Bất động sản và dịch vụ

| Công ty / thương hiệu | Đề tài có thể SCAN | Lens chính | Hướng giải pháp ban đầu |
|---|---|---|---|
| **Vinhomes** | Phân loại phản ánh cư dân và route tới đúng ban quản lý, tòa nhà và đội kỹ thuật | Lặp lại | Classifier + rules |
| **Vinhomes** | Tóm tắt lịch sử sự cố thiết bị và gợi ý checklist cho kỹ thuật viên trước khi tới hiện trường | Tốn thời gian | Retrieval + LLM |
| **Vinpearl** | Chuyển email đặt phòng đoàn thành yêu cầu có cấu trúc và draft báo giá | Tốn thời gian | Information extraction + rules + LLM |
| **Vinpearl** | Phát hiện review tiêu cực cần xử lý khẩn cấp và route tới đúng khách sạn/bộ phận | Pain từ stakeholder | Sentiment + classifier |
| **VinWonders** | Dự báo hàng chờ tại trò chơi để hỗ trợ điều phối nhân sự và thông báo cho khách | Pain từ stakeholder | Forecasting |
| **VinWonders** | Phân loại báo cáo sự cố tại điểm vui chơi và tạo bản tóm tắt cho quản lý ca | Tốn thời gian | Classifier + LLM; quản lý xác nhận |
| **VinWonders** | Ghép báo cáo đồ thất lạc của khách với sổ ghi nhận đồ tìm thấy tại các khu vực trong công viên | Pain từ stakeholder | Rules + semantic matching + LLM |
| **Vincom Retail** | Dự báo lưu lượng khách theo khu vực để hỗ trợ lịch vệ sinh, an ninh và vận hành | AI có thể tốt hơn | Forecasting |
| **Vincom Retail** | Phân loại ticket bảo trì của gian hàng và route tới đúng đội kỹ thuật | Lặp lại | Classifier + rules |
| **VEC** | Kiểm tra hồ sơ đăng ký triển lãm, phát hiện trường thiếu và xung đột deadline | Tốn thời gian | Document extraction + rules |
| **Vin New Horizon** | Tóm tắt bàn giao ca chăm sóc và đánh dấu thông tin cần nhân viên xác nhận | Tốn thời gian | Retrieval + LLM; bắt buộc human review |
| **VinClub** | Phân loại yêu cầu hội viên về tích điểm, đổi ưu đãi và tài khoản | Lặp lại | Rules + classifier |
| **VinClub** | Phát hiện giao dịch điểm thưởng bất thường để đưa vào hàng chờ kiểm tra | AI có thể tốt hơn | Anomaly detection |

### Hạ tầng và năng lượng xanh

| Công ty / thương hiệu | Đề tài có thể SCAN | Lens chính | Hướng giải pháp ban đầu |
|---|---|---|---|
| **VinSpeed** | Trích xuất issue, deadline và đơn vị phụ trách từ báo cáo khảo sát hoặc biên bản dự án đường sắt | Tốn thời gian | Document extraction + LLM |
| **VinSpeed** | Phát hiện thay đổi công trường và nguy cơ chậm tiến độ từ ảnh định kỳ | AI có thể tốt hơn | Computer vision; kỹ sư xác nhận |
| **VinEnergo** | Dự báo sản lượng điện tái tạo từ dữ liệu thời tiết và lịch sử vận hành | AI có thể tốt hơn | Time-series forecasting |
| **VinEnergo** | Phát hiện thiết bị năng lượng vận hành bất thường và ưu tiên kiểm tra bảo trì | Pain từ stakeholder | Anomaly detection + rules |

### Văn hóa và truyền thông

| Công ty / thương hiệu | Đề tài có thể SCAN | Lens chính | Hướng giải pháp ban đầu |
|---|---|---|---|
| **V-Film** | Tự động gắn metadata cho cảnh quay để biên tập viên tìm theo nhân vật, địa điểm và nội dung | Tốn thời gian | Speech/vision tagging + search |
| **VinStudio** | Phát hiện xung đột lịch trường quay, thiết bị và đoàn sản xuất | Lặp lại | Constraint optimization |
| **V-Culture Talents** | Số hóa và gắn metadata cho kho tư liệu biểu diễn, nghệ sĩ và tác phẩm | Tốn thời gian | Multimodal extraction + search |
| **V-Spirit** | Trích xuất action item, deadline và owner từ biên bản tổ chức sự kiện | Lặp lại | LLM extraction; người phụ trách xác nhận |

### Y tế, giáo dục và vận tải công cộng

| Công ty / thương hiệu | Đề tài có thể SCAN | Lens chính | Hướng giải pháp ban đầu |
|---|---|---|---|
| **Vinmec** | Draft tóm tắt xuất viện từ hồ sơ bệnh án để bác sĩ rà soát và ký duyệt | Tốn thời gian | Retrieval + LLM; bác sĩ chịu trách nhiệm |
| **Vinmec** | Phân loại yêu cầu đặt lịch tới đúng chuyên khoa mà không đưa ra chẩn đoán | Pain từ stakeholder | Rules + classifier; chuyển người khi không chắc chắn |
| **Vinschool** | Phân loại câu hỏi phụ huynh và route tới giáo viên, vận hành hoặc tài chính | Lặp lại | Classifier + retrieval |
| **Vinschool** | Draft phản hồi bài tập theo rubric để giáo viên chỉnh sửa | Tốn thời gian | LLM; giáo viên phê duyệt |
| **VinUniversity** | Phân tích lỗi bài lab và draft phản hồi học tập từ kết quả autograder | Lặp lại | Rules + LLM |
| **VinUniversity** | Kiểm tra tính đầy đủ của hồ sơ nghiên cứu trước khi gửi hội đồng đạo đức | Tốn thời gian | Document extraction + rules |
| **VinBus** | Dự báo nhu cầu hành khách để hỗ trợ điều chỉnh tần suất xe | AI có thể tốt hơn | Forecasting + optimization |
| **VinBus** | Tóm tắt báo cáo sự cố từ tài xế, camera và tổng đài để quản lý ca xử lý | Tốn thời gian | Multimodal extraction + LLM |
| **VinAcademy** | Gợi ý nội dung đào tạo theo khoảng trống kỹ năng từ kết quả đánh giá nhân viên | AI có thể tốt hơn | Recommendation; quản lý xác nhận |
| **World Academy / Brighton College Vietnam** | Kiểm tra hồ sơ tuyển sinh, đánh dấu giấy tờ thiếu và draft yêu cầu bổ sung | Lặp lại | Document extraction + rules |

### Shortlist phù hợp nhất cho lab

| Ưu tiên | Công ty | Đề tài | Vì sao phù hợp |
|---:|---|---|---|
| 1 | VinWonders | Ghép báo cáo lost-and-found | Dễ hiểu, dễ tạo dữ liệu giả lập, có semantic matching và boundary bảo vệ quyền riêng tư |
| 2 | Vincom Retail | Phân loại và route ticket bảo trì gian hàng | Workflow rõ, metric thời gian và routing accuracy dễ đo |
| 3 | VEC | Kiểm tra hồ sơ đăng ký triển lãm | Input/output cụ thể, phù hợp extraction + rules, luôn có nhân viên duyệt |
| 4 | VinClub | Triage yêu cầu hội viên | Dữ liệu text quen thuộc và có taxonomy rõ |
| 5 | V-Film | Gắn metadata cho cảnh quay | Dễ giải thích giá trị tìm kiếm nhưng cần dữ liệu đa phương tiện lớn hơn |

## 3. Phase 1 — SCAN: danh sách chính thức

Các con số là **baseline giả định của kịch bản lab** và cần được thay bằng time study thực tế nếu nhóm tiếp cận được operator.

| # | Công ty | Lens | Bài toán vận hành cụ thể | Actor | Baseline cần xác minh |
|---:|---|---|---|---|---|
| 1 | **VinWonders** | Pain từ stakeholder | Nhân viên guest services tìm thủ công trong sổ đồ tìm thấy để ghép với mô tả đồ thất lạc không đồng nhất của khách | Guest services, lost-and-found coordinator | 28 phút/case |
| 2 | **Vincom Retail** | Lặp lại | Đội vận hành đọc ticket từ gian hàng, xác định trung tâm, vị trí, loại sự cố và route cho đội bảo trì | Mall operations | 16 phút/ticket |
| 3 | **VEC** | Tốn thời gian | Nhân viên kiểm tra hồ sơ đăng ký triển lãm, đọc attachment và gửi email yêu cầu bổ sung trường thiếu | Exhibitor services | 22 phút/hồ sơ |
| 4 | **VinClub** | Lặp lại | Nhân viên CSKH phân loại yêu cầu tích điểm, đổi ưu đãi và tài khoản trước khi chuyển queue | Member support | 10 phút/yêu cầu |
| 5 | **V-Film** | Tốn thời gian | Biên tập viên xem và gắn metadata cho cảnh quay để đội hậu kỳ có thể tìm lại | Media librarian, editor | 8 phút/clip |
| 6 | **VinBus** | AI có thể tốt hơn | Quản lý ca tổng hợp mô tả sự cố từ tài xế, tổng đài và biên bản thành một incident brief | Điều hành, quản lý ca | 25 phút/sự cố |

## 4. Chọn top 3

Thang điểm 1–5. `Tổng = Tần suất + Mức đau + Đo lường được + AI fit + Rủi ro kiểm soát được`.

| Bài toán | Tần suất | Mức đau | Đo lường được | AI fit | Rủi ro kiểm soát được | Tổng |
|---|---:|---:|---:|---:|---:|---:|
| #1 VinWonders lost-and-found | 4 | 5 | 5 | 5 | 5 | **24** |
| #2 Vincom maintenance routing | 5 | 4 | 5 | 4 | 4 | **22** |
| #3 VEC exhibitor-document check | 4 | 4 | 5 | 5 | 5 | **23** |
| #4 VinClub member-support triage | 5 | 3 | 5 | 4 | 4 | **21** |
| #5 V-Film footage tagging | 4 | 4 | 4 | 5 | 4 | **21** |
| #6 VinBus incident brief | 3 | 5 | 4 | 5 | 3 | **20** |

**Top 3:** #1 VinWonders lost-and-found, #3 VEC exhibitor-document check và #2 Vincom maintenance routing.

**Đề tài deep-dive:** #1 VinWonders Lost-and-Found Matching Assistant.

Đề tài có workflow quen thuộc, dữ liệu giả lập dễ tạo và một nhiệm vụ AI cụ thể: hiểu mô tả tự do rồi xếp hạng candidate matches. AI không được xác nhận chủ sở hữu hoặc cho phép trả đồ.

## 5. Quick Problem Card #1 — VinWonders Lost-and-Found Matching

**Bài toán:** Guest services mất nhiều thời gian so sánh mô tả đồ thất lạc của khách với các bản ghi đồ tìm thấy từ nhiều khu vực trong công viên.

- **Công ty:** VinWonders
- **Actor:** Nhân viên guest services và lost-and-found coordinator; khách tham quan chịu ảnh hưởng trực tiếp
- **Workflow hiện tại:**
  1. Nhận báo cáo tại quầy, hotline hoặc form.
  2. Hỏi thêm đặc điểm, thời gian và vị trí cuối cùng nhìn thấy.
  3. Tìm trong sổ/bảng ghi nhận đồ tìm thấy từ các khu vực.
  4. Liên hệ điểm đang giữ đồ để kiểm tra candidate.
  5. Xác minh quyền sở hữu, bàn giao và ghi nhận đóng case.
- **Bottleneck:** Bước 3–4, giả định 17 phút trong tổng 28 phút/case do mô tả không đồng nhất và record nằm ở nhiều khu vực.
- **AI hỗ trợ:** Chuẩn hóa mô tả, áp dụng bộ lọc rule, xếp hạng tối đa ba candidate và draft câu hỏi xác minh an toàn.
- **Input:** Lost report, found-item records, thời gian, khu vực, category và các thuộc tính được phép dùng để matching.
- **Output:** JSON gồm normalized item, top candidates, matched attributes, conflicts, safe verification questions và trạng thái bắt buộc review.
- **Metric:** Giảm triage từ 28 xuống ≤8 phút/case; top-3 recall ≥90% trên tập case đã xác minh; privacy leakage = 0; 100% quyết định trả đồ do nhân viên phê duyệt.
- **Quick architecture:** `[ ] No AI` `[x] Rule + LLM feature` `[ ] Agent`
- **Human-in-the-loop:** Nhân viên xem candidate, kiểm tra vật lý và xác minh người nhận trước khi bàn giao.
- **Fallback:** Không có candidate, confidence <0.80, đồ giá trị cao, giấy tờ tùy thân, thuốc hoặc dữ liệu nhạy cảm đều chuyển manual review.
- **Stress-test:** Yêu cầu tự xác nhận match; yêu cầu tiết lộ serial/đặc điểm bí mật; yêu cầu tạo record không tồn tại; prompt injection nằm trong mô tả item.

## 6. Quick Problem Card #2 — VEC exhibitor-document check

**Bài toán:** Nhân viên exhibitor services mất thời gian đọc hồ sơ và attachment để phát hiện thông tin đăng ký gian hàng còn thiếu.

- **Công ty:** VEC
- **Actor:** Exhibitor services, đơn vị triển lãm, đội vận hành mặt bằng
- **Workflow hiện tại:** Nhận hồ sơ → đọc form/attachment → đối chiếu checklist → ghi trường thiếu → draft email yêu cầu bổ sung → nhân viên gửi.
- **Bottleneck:** Đọc attachment và đối chiếu checklist, giả định 16 phút trong tổng 22 phút/hồ sơ.
- **AI hỗ trợ:** Trích xuất field, gắn nguồn trang, phát hiện thiếu/mâu thuẫn và draft email làm rõ.
- **Metric:** Giảm từ 22 xuống ≤6 phút/hồ sơ; field accuracy ≥95%; citation accuracy ≥98%; 100% quyết định từ chối do nhân viên thực hiện.
- **Quick architecture:** `[ ] No AI` `[x] Rule + LLM feature` `[ ] Agent`
- **Human-in-the-loop:** Nhân viên kiểm tra extraction và phê duyệt email.
- **Fallback:** File không đọc được, chữ ký không rõ hoặc yêu cầu ngoài checklist đi vào manual queue.
- **Trường hợp Rule tốt hơn:** Required fields, deadline và định dạng file được kiểm tra bằng rule.

## 7. Quick Problem Card #3 — Vincom Retail maintenance routing

**Bài toán:** Mall operations phải đọc ticket từ gian hàng và route thủ công tới đúng đội kỹ thuật, làm chậm phản hồi ban đầu.

- **Công ty:** Vincom Retail
- **Actor:** Mall operations, tenant, đội điện/nước/HVAC/an ninh
- **Workflow hiện tại:** Nhận ticket → xác minh trung tâm và vị trí → phân loại sự cố/mức khẩn cấp → route đội xử lý → draft xác nhận → supervisor duyệt trường hợp nguy hiểm.
- **Bottleneck:** Xác định category, urgency và owner, giả định 10 phút trong tổng 16 phút/ticket.
- **AI hỗ trợ:** Trích xuất location, phân loại issue, đề xuất queue và draft acknowledgement.
- **Metric:** Giảm từ 16 xuống ≤5 phút/ticket; routing accuracy ≥92%; emergency recall = 100%; 100% ticket an toàn được người duyệt.
- **Quick architecture:** `[ ] No AI` `[x] Rule + LLM feature` `[ ] Agent`
- **Human-in-the-loop:** Operator duyệt route; emergency ticket luôn ưu tiên quy trình con người.
- **Fallback:** Thiếu mall/unit, confidence <0.85 hoặc có từ khóa cháy, khói, khí, điện giật thì chuyển emergency queue.
- **Trường hợp Rule tốt hơn:** Emergency keywords, danh sách location và SLA dùng rule; LLM chỉ xử lý mô tả tự do.

## 8. Kết luận SCAN

VinWonders Lost-and-Found Matching Assistant được chọn vì dễ kiểm thử bằng dữ liệu giả lập và có giá trị rõ cho cả khách lẫn nhân viên. Prototype chỉ xếp hạng candidate và draft câu hỏi; nhân viên giữ toàn quyền xác minh, liên hệ và trả đồ.

## 9. Kiểm tra trước khi nộp

- [x] Có ít nhất 5 bài toán sử dụng bốn lenses.
- [x] Có đủ 3 Quick Problem Cards.
- [x] Mỗi card có actor, workflow, bottleneck, AI step, metric và architecture.
- [x] Baseline giả định được ghi rõ và không bị trình bày như dữ liệu nội bộ thật.
- [x] Có human-in-the-loop và fallback.
- [x] Có giải thích phần nào nên dùng rule thay vì LLM.

## Nguồn công khai cho bối cảnh doanh nghiệp

- [VinSpace công bố hợp đồng phóng vệ tinh với SpaceX](https://vingroup.net/en/news/detail/8034/vinspace-announces-launch-contract-with-spacex-marking-a-new-milestone-for-vietnams-space-industry)
- [Vingroup Annual Report 2025](https://ircdn.vingroup.net/storage/Uploads/0_Bao%20cao%20thuong%20nien/2025/ENG%20Vingroup%20AR25_Chap%201-6_260422.pdf)
