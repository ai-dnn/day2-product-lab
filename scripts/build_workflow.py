"""Generate the lab diagram. Requires reportlab; Arial defaults to Windows fonts."""
import os
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A3, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = Path(os.getenv("WORKFLOW_FONT_DIR", "C:/Windows/Fonts"))
pdfmetrics.registerFont(TTFont("ArialVN", str(FONT_DIR / "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArialVN-Bold", str(FONT_DIR / "arialbd.ttf")))
pdfmetrics.registerFontFamily("ArialVN", normal="ArialVN", bold="ArialVN-Bold")
W, H = landscape(A3)
c = Canvas(str(ROOT / "04-workflow-diagram.pdf"), pagesize=(W, H))
c.setTitle("Lab 02 - Xanh SM - Current-State Workflow (giả định)")
c.setAuthor("Lab 02 - Bản nháp có AI hỗ trợ")
NAVY = colors.HexColor("#11253D")
INK = colors.HexColor("#21354A")
MUTED = colors.HexColor("#536B80")
TEAL = colors.HexColor("#057A79")
RED = colors.HexColor("#BA3E40")
BG = colors.HexColor("#F3F6FA")


def text(x, y, value, size=12, color=INK, bold=False):
    c.setFillColor(color)
    c.setFont("ArialVN-Bold" if bold else "ArialVN", size)
    c.drawString(x, y, value)


def paragraph(x, top, width, value, size=12, color=INK, leading=None):
    style = ParagraphStyle("body", fontName="ArialVN", fontSize=size,
                           leading=leading or size * 1.45, textColor=color,
                           alignment=TA_LEFT, spaceAfter=0)
    p = Paragraph(value, style)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, top - height)
    return height


c.setFillColor(BG)
c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(NAVY)
c.rect(0, H - 186, W, 186, stroke=0, fill=1)
text(42, H - 44, "LAB 02  /  AI PRODUCT SCOPING", 12, colors.HexColor("#91DCD4"), True)
text(42, H - 91, "Xanh SM: xử lý yêu cầu hỗ trợ pin yếu", 29, colors.white, True)
text(42, H - 122, "Quy trình hiện tại - mô hình giả định phục vụ bài lab", 16, colors.HexColor("#D2E0EB"))
text(42, H - 153, "Chưa khảo sát thực địa. Các mốc thời gian cần được đo và xác nhận lại.", 12, colors.HexColor("#D2E0EB"))

text(42, 613, "5 BƯỚC XỬ LÝ", 12, TEAL, True)
text(W - 316, 608, "13 phút thao tác / lượt", 20, NAVY, True)
text(42, 585, "Bắt đầu: mở ticket  |  Kết thúc: đề xuất được duyệt  |  Chưa gồm xếp hàng, chờ trả lời và hỗ trợ hiện trường", 11.5, MUTED)

cards = [
    ("01", "Tiếp nhận", "1 phút", "Điều phối viên", "Tin tài xế → hồ sơ sự cố", "H1: Tài xế chuyển thông tin cho điều phối viên.", False),
    ("02", "Xác minh", "2 phút", "Điều phối viên", "Hồ sơ → pin / vị trí xác minh", "H2: Thông tin hệ thống xe chuyển tới người xử lý.", False),
    ("03", "Tra phương án", "4 phút", "Điều phối viên", "Pin / vị trí → phương án", "Chuyển công cụ, kiểm tra nguồn hỗ trợ phù hợp.", True),
    ("04", "Soạn và kiểm tra", "4 phút", "Điều phối viên", "Phương án → bản nháp", "Lọc tin tự do, soạn nháp và kiểm tra ranh giới.", True),
    ("05", "Chuyển duyệt", "2 phút", "Người có thẩm quyền", "Bản nháp → duyệt / sửa", "H3: Điều phối viên chuyển đề xuất cho người duyệt.", False),
]
gap = 18
card_w = (W - 84 - gap * 4) / 5
y, card_h = 292, 263
for i, (number, title, duration, actor, io, note, bottleneck) in enumerate(cards):
    x = 42 + i * (card_w + gap)
    accent = RED if bottleneck else TEAL
    c.setFillColor(colors.white)
    c.setStrokeColor(colors.HexColor("#DDE4EC"))
    c.roundRect(x, y, card_w, card_h, 10, stroke=1, fill=1)
    c.setFillColor(accent)
    c.roundRect(x + 15, y + card_h - 44, 34, 27, 5, stroke=0, fill=1)
    text(x + 23, y + card_h - 35, number, 12, colors.white, True)
    text(x + 15, y + card_h - 77, title, 17, NAVY, True)
    text(x + 15, y + card_h - 108, duration, 23, accent, True)
    paragraph(x + 15, y + card_h - 124, card_w - 30, actor, 10.5, MUTED)
    paragraph(x + 15, y + card_h - 154, card_w - 30, io, 11.5, INK)
    paragraph(x + 15, y + 61, card_w - 30, note, 10.5, MUTED)
    if bottleneck:
        text(x + 63, y + card_h - 35, "ĐIỂM NGHẼN", 9.3, RED, True)
    if i < 4:
        mid = y + card_h / 2
        c.setStrokeColor(MUTED)
        c.setLineWidth(1.3)
        c.line(x + card_w + 3, mid, x + card_w + gap - 3, mid)
        c.line(x + card_w + gap - 7, mid + 4, x + card_w + gap - 3, mid)
        c.line(x + card_w + gap - 7, mid - 4, x + card_w + gap - 3, mid)

panel_y, panel_h = 91, 166
panel_w = (W - 104) / 2
for x in [42, 62 + panel_w]:
    c.setFillColor(colors.white)
    c.roundRect(x, panel_y, panel_w, panel_h, 10, stroke=0, fill=1)
text(60, panel_y + panel_h - 30, "CHUYỂN GIAO VÀ NGOẠI LỆ", 12, TEAL, True)
paragraph(60, panel_y + panel_h - 46, panel_w - 36,
          "<b>H1 / H2 / H3:</b> điểm chuyển giao giữa tài xế, hệ thống và người duyệt.<br/>"
          "<b>Thiếu pin hoặc vị trí:</b> hỏi lại và quay về bước 2. Đo riêng thời gian chờ.<br/>"
          "<b>Cần sửa đề xuất:</b> người duyệt trả về bước 3 hoặc 4.<br/>"
          "<b>Điểm nghẽn 3 + 4:</b> 8/13 phút thao tác giả định.", 11.5)
rx = 80 + panel_w
text(rx, panel_y + panel_h - 30, "PHẠM VI CẢI TIẾN CỦA PROTOTYPE", 12, TEAL, True)
paragraph(rx, panel_y + panel_h - 46, panel_w - 36,
          "Chỉ hỗ trợ <b>bước 4</b>: AI tóm tắt cho người duyệt, rule kiểm tra nháp.<br/>"
          "Mục tiêu giả định: bước 4 từ <b>4 → 2 phút</b>; tổng từ <b>13 → 11 phút</b>.<br/>"
          "Mọi hành động chờ người duyệt. Không tự gửi tin hoặc điều xe.<br/>"
          "<b>Trạng thái: NOT YET</b> - cần baseline và thử nghiệm Gemini thật.", 11.5)
c.setStrokeColor(colors.HexColor("#D6DEE8"))
c.line(42, 65, W - 42, 65)
text(42, 43, "Nguồn thiết kế: 01-worksheet.md và starter code  |  Chi tiết: 02-deep-dive-report.md", 10, MUTED)
text(W - 269, 43, "BẢN NHÁP  •  11/09/2026  •  1/1", 10, MUTED)
c.showPage()
c.save()
print(ROOT / "04-workflow-diagram.pdf")
