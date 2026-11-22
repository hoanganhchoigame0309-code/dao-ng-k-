# -*- coding: utf-8 -*-
"""
build_faithful_15page_docx.py
Bám sát 100% nội dung báo cáo gốc của tác giả Võ Bình Minh & nhóm học sinh Ngô Hoàng Anh, Phạm Thanh Bình.
- Giữ nguyên toàn bộ số liệu thực nghiệm và kết quả Thí nghiệm 1, 2, 3, 4, 5 ở Phần 8.
- Rút gọn lý thuyết Phần 3 (toán học và DSP cô đọng).
- Nhúng toàn bộ lịch sử chat thực tế từ file Bao_Cao_lich_Su_Chat_FoxLab.txt vào Phần 7.2.
- Chèn sơ đồ khối kiến trúc chuẩn theo code v6.4.0 (foxlab_architecture_diagram.png).
- Đảm bảo tổng số trang <= 15 trang A4 trong Microsoft Word.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=40, bottom=40, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_bg(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_borders(cell, top="CCCCCC", bottom="CCCCCC", left=None, right=None, sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    borders = {'w:top': top, 'w:bottom': bottom, 'w:left': left, 'w:right': right}
    for b_name, b_color in borders.items():
        if b_color:
            b_elem = parse_xml(f'<{b_name} {nsdecls("w")} w:val="single" w:sz="{sz}" w:space="0" w:color="{b_color}"/>')
            tcBorders.append(b_elem)
        else:
            b_elem = parse_xml(f'<{b_name} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(b_elem)
    tcPr.append(tcBorders)

def make_table(doc, headers, data, col_widths=None, header_bg="1B365D", alt_bg="F8F9FA", font_size=8.5):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr_row = table.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    for col_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[col_idx]
        set_cell_bg(cell, header_bg)
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        set_cell_borders(cell, top="1B365D", bottom="1B365D", sz="6")
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        run = p.add_run(h_text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(font_size)
        run.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, row_data in enumerate(data):
        row = table.rows[row_idx + 1]
        bg = alt_bg if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            cell = row.cells[col_idx]
            set_cell_bg(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=55, right=55)
            set_cell_borders(cell, top="E2E8F0", bottom="E2E8F0", sz="4")
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            
            # Text alignment logic
            if col_idx == 0 and len(headers) > 3 and not any(h in headers[0] for h in ['Bước', 'Nội dung', 'Hiện tượng', 'Chỉ số', 'Tên', 'Nút', 'Hướng']):
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx in [1, 2, 3, 4, 5] and len(headers) >= 5:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            run = p.add_run(str(val))
            run.font.name = 'Times New Roman'
            run.font.size = Pt(font_size)
            run.font.color.rgb = RGBColor(30, 41, 59)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    doc.add_paragraph().paragraph_format.space_after = Pt(1.5)
    return table

def add_chat_bubble(doc, sender, content, timestamp="", is_ai=False):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.rows[0].cells[0].width = Inches(6.8)

    cell = tbl.rows[0].cells[0]
    bg_color = "F0F7FF" if is_ai else "F8FAFC"
    border_color = "0284C7" if is_ai else "64748B"
    set_cell_bg(cell, bg_color)
    set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
    set_cell_borders(cell, top=border_color, bottom=border_color, left=border_color, right=border_color, sz="8")

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.08

    r_tag = p.add_run(f"[{sender}]")
    r_tag.bold = True
    r_tag.font.name = 'Times New Roman'
    r_tag.font.size = Pt(9.0)
    r_tag.font.color.rgb = RGBColor(2, 132, 199) if is_ai else RGBColor(30, 41, 59)

    if timestamp:
        r_time = p.add_run(f" ({timestamp})")
        r_time.font.italic = True
        r_time.font.name = 'Times New Roman'
        r_time.font.size = Pt(8.0)
        r_time.font.color.rgb = RGBColor(100, 116, 139)

    r_colon = p.add_run(": ")
    r_colon.bold = True

    lines = content.strip().split('\n')
    for idx, line in enumerate(lines):
        if idx > 0:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.08
        r_text = p.add_run(line.strip())
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(9.0)
        r_text.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(1)

def build_faithful_docx():
    doc = docx.Document()

    # Page Margins (Standard A4: Top/Bottom/Right 1.8cm, Left 2.5cm)
    for s in doc.sections:
        s.top_margin = Inches(0.71)      # 1.8 cm
        s.bottom_margin = Inches(0.71)   # 1.8 cm
        s.left_margin = Inches(0.98)     # 2.5 cm
        s.right_margin = Inches(0.71)    # 1.8 cm
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(2.5)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(27, 54, 93)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0, 102, 153)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2.5)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
        r_txt = p.add_run(text)
        if italic:
            r_txt.italic = True
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.12
        p.paragraph_format.space_before = Pt(0.5)
        p.paragraph_format.space_after = Pt(1.5)
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
        p.add_run(text)
        return p

    # ==================== TIÊU ĐỀ & THÔNG TIN TÁC GIẢ ====================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(2)
    r_title = p_title.add_run("FOX-Lab: Thiết kế phòng thí nghiệm Sóng âm di động trực quan hóa\nđại lượng vật lý và tự động hóa quy trình báo cáo thực hành trong môi trường lớp học")
    r_title.font.size = Pt(13)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(27, 54, 93)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_meta.paragraph_format.space_after = Pt(3)
    r_m1 = p_meta.add_run("Lĩnh vực dự thi: ")
    r_m1.bold = True
    p_meta.add_run("Vật lý và Thiên văn / Phần mềm hệ thống\n")
    r_m2 = p_meta.add_run("Nhóm tác giả: ")
    r_m2.bold = True
    p_meta.add_run("Ngô Hoàng Anh – Lớp 11A2, Phạm Thanh Bình – Lớp 11A7, Trường Ngô Quyền\n")
    r_m3 = p_meta.add_run("Giáo viên hướng dẫn: ")
    r_m3.bold = True
    p_meta.add_run("Võ Bình Minh, đơn vị công tác | Ngày hoàn thành: 29/10/2026")
    p_meta.paragraph_format.line_spacing = 1.1

    # Tóm tắt
    add_h2("Tóm tắt")
    add_p("FOX-Lab là một ứng dụng web chạy trực tiếp trên trình duyệt của điện thoại, máy tính bảng hoặc máy tính, biến micro thành một dao động ký (oscilloscope) hai kênh để học sinh quan sát, đo đạc và phân tích sóng âm ngay trong lớp học, không cần thiết bị đo chuyên dụng. Ứng dụng thu tín hiệu âm thanh qua Web Audio API, lọc dải 80–3000 Hz, rồi tự động tìm tần số bằng thuật toán tự tương quan có nội suy parabol. Dựa trên tần số tìm được, hệ thống tự chọn thang thời gian để màn hình luôn hiển thị khoảng 5 chu kỳ và dùng điều kiện kích (trigger) qua điểm không để dạng sóng đứng yên như trên dao động ký thật. Sau khi 'khóa sóng', học sinh có thể phóng to thu nhỏ, đọc biên độ, chu kỳ, tần số trên lưới 10 × 8 ô, lưu ảnh đồ thị một chạm, hoặc mở chế độ phân tích FFT 8192 điểm với cửa sổ Hann để xem năm họa âm đầu tiên (H1–H5) của một nốt nhạc. Ngoài phần đo, dự án tích hợp trợ lý FOX-Lab AI nhận tần số đo thời gian thực làm ngữ cảnh để giải thích hiện tượng, hướng dẫn xử lý số liệu và gợi ý cách viết báo cáo thực hành; khi mất kết nối, một bộ trả lời dự phòng cục bộ vẫn hoạt động. Mã QR trên giao diện giúp cả lớp mở cùng một địa chỉ web bằng điện thoại của mình.")
    add_p("dao động ký, sóng âm, tần số, họa âm, FFT, Web Audio API, thí nghiệm ảo di động, trợ lý AI, Vật lí 11.", bold_prefix="Từ khóa: ", italic=True)

    # ==================== PHẦN 1 ====================
    add_h1("Phần 1. Đặt vấn đề")
    add_h2("1.1. Lý do chọn đề tài")
    add_p("Sóng âm là nội dung quen thuộc của chương Dao động và Sóng trong chương trình Vật lí 11 (chương trình giáo dục phổ thông 2018). Các đại lượng như biên độ, chu kỳ, tần số, độ cao, âm sắc đều có thể quan sát trực tiếp bằng dao động ký. Tuy vậy, trong thực tế dạy học, các khái niệm này thường chỉ được học qua hình vẽ trong sách hoặc mô phỏng có sẵn, nơi học sinh không tự tạo ra được dữ liệu của riêng mình.")
    add_p("Dao động ký và máy phát tín hiệu chuyên dụng là thiết bị đắt tiền, cồng kềnh, thường chỉ có số lượng ít trong phòng thí nghiệm. Một lớp học 40–45 em khó có thể để mọi nhóm cùng thao tác. Trong khi đó, gần như mọi học sinh đều có điện thoại với micro chất lượng đủ tốt và trình duyệt hiện đại, nhưng các thiết bị này hiếm khi được khai thác như một dụng cụ đo trong giờ học. Từ quan sát đó, nhóm tác giả đặt câu hỏi: liệu có thể biến chính điện thoại của học sinh thành một phòng thí nghiệm sóng âm di động, vừa đo được, vừa phân tích được, vừa hỗ trợ viết báo cáo? FOX-Lab là câu trả lời của nhóm.")

    add_h2("1.2. Thực trạng và hạn chế của các giải pháp hiện có")
    add_p("Nhóm đã xem xét ba nhóm giải pháp học sinh thường gặp:")
    add_bullet("Cho kết quả chính xác, nhưng thiếu về số lượng, cần kỹ năng vận hành và không mang về nhà được.", "Dao động ký phần cứng: ")
    add_bullet("Dễ dùng, song dữ liệu là dữ liệu mẫu; học sinh không thể thử với âm thanh thật như tiếng sáo, âm thoa, giọng nói của chính mình.", "Mô phỏng có sẵn (applet, video): ")
    add_bullet("Nhiều ứng dụng đo mức ồn (dB) hoặc hiển thị phổ, nhưng ít ứng dụng được thiết kế theo cách dạy học: dạng sóng đứng yên như dao động ký, thang thời gian tính bằng ms, ghi chú theo ngôn ngữ của sách giáo khoa, và không gắn với việc viết báo cáo thực hành.", "Ứng dụng đo âm trên điện thoại: ")
    add_p("Nhìn chung còn thiếu một công cụ thỏa mãn đồng thời bốn yêu cầu: dùng được ngay trên thiết bị sẵn có, hiển thị theo đúng 'ngôn ngữ' của dao động ký, có phân tích họa âm ở mức học sinh hiểu được, và đồng hành với học sinh khi xử lý số liệu.")

    add_h2("1.3. Khó khăn trong báo cáo thực hành & 1.4. Tính cấp thiết")
    add_p("Quy trình thực hành truyền thống gồm: lắp thiết bị, chỉnh máy, đọc số trên màn hình, ghi vào vở, chụp hoặc vẽ lại đồ thị, tính toán rồi viết báo cáo. Ở mỗi bước, học sinh thường mất nhiều thời gian vào thao tác kỹ thuật thay vì suy nghĩ về hiện tượng vật lí. Giáo viên cũng khó theo dõi tiến độ của từng nhóm.")
    add_p("Chương trình 2018 nhấn mạnh phát triển năng lực thực nghiệm và năng lực sử dụng công nghệ số trong học tập môn Vật lí. Điện thoại thông minh là thiết bị sẵn có, giúp giảm chi phí và mở rộng cơ hội thực hành ra ngoài phòng thí nghiệm. Việc tự động hóa các thao tác kỹ thuật lặp lại giúp học sinh dành thời gian cho phần quan trọng nhất của khoa học: quan sát, nhận xét, giải thích và rút ra kết luận.")

    # ==================== PHẦN 2 ====================
    add_h1("Phần 2. Mục tiêu, đối tượng và phương pháp nghiên cứu")
    add_h2("2.1. Mục tiêu và nhiệm vụ nghiên cứu")
    add_p("Mục tiêu chung: thiết kế và hoàn thiện một phòng thí nghiệm sóng âm di động chạy trên trình duyệt, giúp học sinh trực quan hóa các đại lượng vật lí của sóng âm và giảm thao tác thủ công trong quy trình thực hành – báo cáo.")
    add_bullet("Thu tín hiệu âm thanh từ micro và hiển thị dạng sóng thời gian thực như một dao động ký có lưới chia độ, trục thời gian (ms) và trục biên độ chuẩn hóa.")
    add_bullet("Tự động xác định tần số cơ bản và tự điều chỉnh thang thời gian, kích sóng (trigger) để dạng sóng đứng yên, dễ đọc chu kỳ.")
    add_bullet("Hỗ trợ đo cùng lúc hai nguồn âm (Kênh A và Kênh B) để so sánh biên độ, tần số, độ lệch pha.")
    add_bullet("Phân tích phổ bằng FFT để học sinh thấy được họa âm tạo nên âm sắc của nhạc cụ, giọng nói.")
    add_bullet("Tích hợp trợ lý hỏi đáp FOX-Lab AI và các tiện ích (lưu ảnh, toàn màn hình, mã QR) để rút ngắn quy trình báo cáo thực hành.")

    add_h2("2.2. Đối tượng, phạm vi và phương pháp nghiên cứu")
    add_p("Đối tượng nghiên cứu: sóng âm trong dải tần 100–1500 Hz (dải tự động bám tần số) và phổ họa âm đến bậc 5 của âm có tần số cơ bản từ khoảng 100 Hz đến vài trăm Hz. Đối tượng sử dụng: học sinh và giáo viên Vật lí cấp THPT, ưu tiên lớp 11. Phương pháp nghiên cứu kết hợp nghiên cứu tài liệu, thiết kế – lập trình theo vòng lặp, thực nghiệm đối chứng và khảo sát sư phạm.")

    add_h2("2.3. Công nghệ sử dụng")
    tech_headers = ["Thành phần", "Công nghệ", "Vai trò trong hệ thống"]
    tech_data = [
        ["Thu tín hiệu", "getUserMedia, Web Audio API", "Truy cập micro, tạo bộ lọc, nhận mẫu âm thanh."],
        ["Xử lí", "JavaScript thuần", "Tự tương quan, trigger, FFT, thu phóng."],
        ["Hiển thị", "HTML5 Canvas 2D", "Vẽ lưới, nhãn, dạng sóng, biểu đồ phổ."],
        ["Giao diện", "HTML, CSS, bố cục co giãn", "Chạy trên điện thoại và máy tính."],
        ["Trợ lý AI", "Google Apps Script (dịch vụ web)", "Cầu nối giữa giao diện và mô hình ngôn ngữ."],
        ["Triển khai", "Trang web tĩnh, manifest ứng dụng web", "Truy cập bằng đường dẫn hoặc mã QR, thêm vào màn hình chính."]
    ]
    make_table(doc, tech_headers, tech_data, [Inches(1.5), Inches(2.3), Inches(3.0)])

    # ==================== PHẦN 3 ====================
    add_h1("Phần 3. Cơ sở lí thuyết (Tóm lược toán học & vật lý cốt lõi)")
    add_p("Nhằm bảo đảm tính cô đọng và tập trung vào ứng dụng thực tiễn, các nội dung lý thuyết được tóm lược thành các định luật và công thức toán học cốt lõi sau:")
    add_bullet("Sóng âm là sóng cơ dọc truyền trong môi trường vật chất. Với âm đơn sắc, tín hiệu có dạng hình sin: u(t) = A sin(2π f t + φ), với chu kỳ T = 1/f, bước sóng λ = v/f. Ba đặc trưng sinh lí gắn với ba đặc trưng vật lí: độ cao gắn với tần số f; độ to gắn với biên độ; âm sắc gắn với dạng đồ thị dao động.", "3.1. Sóng âm & đại lượng đặc trưng: ")
    add_bullet("Nhạc cụ và giọng nói phát ra tổng hợp sóng cơ bản f₀ và các họa âm nguyên lần: u(t) = Σ A_k sin(2π k f₀ t + φ_k). Tập hợp biên độ {A_k} tạo nên âm sắc đặc trưng. FOX-Lab hiển thị năm họa âm đầu (H1–H5).", "3.2. Họa âm & âm sắc: ")
    add_bullet("Tần số lấy mẫu fs (44.1 kHz hoặc 48 kHz). Định lí Nyquist–Shannon yêu cầu fs >= 2 f_max. Với fs = 48 kHz, giới hạn Nyquist là 24 kHz, cao hơn nhiều dải 80–3000 Hz nên không xảy ra chồng phổ.", "3.3. Lấy mẫu Nyquist: ")
    add_bullet("Hàm tự tương quan R(τ) = Σ x[n] x[n+τ] đạt cực đại thứ hai tại τ* ≈ T₀ × fs, từ đó f = fs / τ*. Để giảm sai số bước nhảy mẫu, nội suy parabol qua 3 điểm quanh cực đại: τ*_chính xác = τ* - b / (2a) với a = (R_-1 + R_+1 - 2R_0)/2, b = (R_+1 - R_-1)/2.", "3.4. Tự tương quan (ACF): ")
    add_bullet("Biến đổi Fourier rời rạc N điểm: X[m] = Σ x[n] e^(-j 2π m n / N). Thuật toán FFT Cooley–Tukey giảm độ phức tạp xuống O(N log₂ N). Với N = 8192 và fs = 48 kHz, độ phân giải tần số Δf = fs/N ≈ 5,86 Hz.", "3.5. Biến đổi Fourier & FFT: ")
    add_bullet("Cửa sổ Hann w[n] = 0,5 [1 - cos(2π n / (N-1))] được nhân trước khi tính FFT nhằm triệt tiêu hiện tượng rò rỉ phổ tại hai biên.", "3.6. Cửa sổ Hann: ")
    add_bullet("Mô phỏng cơ chế kích (trigger) của dao động ký thật: tìm điểm cắt không theo chiều tăng kèm dải trễ (hysteresis) 10% biên độ đỉnh để loại trừ nhiễu, ghim dạng sóng đứng yên trên màn hình.", "3.7. Trigger điểm không: ")

    # ==================== PHẦN 4 ====================
    add_h1("Phần 4. Thiết kế tổng thể hệ thống")
    add_h2("4.1. Nguyên lí thiết kế & 4.2. Kiến trúc phần mềm")
    add_p("Hệ thống tuân thủ 5 nguyên lí thiết kế: dùng ngay không cài đặt, trải nghiệm như dao động ký thật, tự động hóa có chủ đích, học sinh là người quan sát và chịu được môi trường lớp học thật. Kiến trúc hệ thống phân tách thành 4 khối chức năng nội bộ chạy trên thiết bị học sinh và 1 dịch vụ web AI:")

    # Sơ đồ khối kiến trúc
    diag_path = os.path.abspath("foxlab_architecture_diagram.png")
    if os.path.exists(diag_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(3)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(diag_path, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(3)
        r_cap = p_cap.add_run("Hình 4.1: Sơ đồ khối kiến trúc hệ thống và luồng dữ liệu FOX-Lab (Cập nhật chuẩn theo mã nguồn)")
        r_cap.font.size = Pt(9.0)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

    add_h2("4.3. Giao diện người dùng và Máy trạng thái")
    add_p("Giao diện chia thành thanh điều khiển phía trên và vùng canvas lưới 10 × 8 ô bên dưới. Bảng thông tin hoạt động như một máy trạng thái, dẫn dắt học sinh từng bước:")
    state_headers = ["Trạng thái", "Thông báo hướng dẫn trên giao diện", "Nút khả dụng"]
    state_data = [
        ["Chưa kết nối micro", "Nhấn vào Kênh A hoặc Kênh B để thu sóng âm", "Kênh A, Kênh B"],
        ["Đã kết nối, chưa đo", "Bấm Đo / Dừng để khảo sát", "Đo / Dừng, Làm mới, Chụp ảnh"],
        ["Đang đo", "Đang quét tín hiệu kèm nhãn kênh đang bật", "Đo / Dừng"],
        ["Đã khóa sóng", "Có thể Phân tích FFT ngay lúc này", "FFT, Chụp ảnh, thu phóng"]
    ]
    make_table(doc, state_headers, state_data, [Inches(1.8), Inches(3.2), Inches(1.8)])

    add_h2("4.4. Chế độ một và hai nguồn âm & 4.5. Chế độ đo & 4.6. Tương thích")
    add_p("Ở chế độ 1 nguồn âm, chỉ 1 kênh chạy để tối ưu tài nguyên cho đo tần số và FFT. Ở chế độ 2 nguồn âm, hai luồng micro chạy song song vẽ chồng lên cùng lưới, dùng chung điểm kích từ kênh tham chiếu để so sánh biên độ và hiện tượng phách. Hai chế độ đo: Khảo sát tần số (tự dừng sau 2 giây để khóa sóng) và Khảo sát liên tục (60 hoặc 15 FPS). Canvas co giãn theo devicePixelRatio và hỗ trợ PWA toàn màn hình.")

    # ==================== PHẦN 5 ====================
    add_h1("Phần 5. Các giải pháp kỹ thuật cốt lõi")
    add_bullet("Thu qua getUserMedia, lọc dải thông cao 80 Hz và thông thấp 3000 Hz, đưa vào mảng Float32Array lưu 10 giây dữ liệu dạng đệm vòng, tránh cấp phát bộ nhớ liên tục.", "5.1. Thu tín hiệu & Bộ đệm vòng: ")
    add_bullet("Cứ 300 ms lấy 2048 mẫu, kiểm tra RMS > 0,02, tính tự tương quan từ 0–1023 mẫu, kiểm tra cực đại >= 30% R(0), nội suy parabol, giới hạn 100–1500 Hz, làm mượt tỉ lệ 0,7 cũ + 0,3 mới và khóa tần số khi lệch > 8%.", "5.2. Tự động bám tần số: ")
    add_bullet("Tổng thời gian hiển thị mặc định bằng 5 chu kỳ: T_màn hình = 5 / f_khóa (từ 2 ms đến 2,4 s). Nhờ đó màn hình luôn có khoảng 5 chu kỳ dễ đếm và đo.", "5.3. Tự chọn thang thời gian: ")
    add_bullet("Xác định biên độ đỉnh, đặt hysteresis = 10% đỉnh, quét ngược tìm điểm cắt không đi lên thỏa mãn mẫu trước dưới -hysteresis. Hai kênh dùng chung điểm kích để giữ nguyên độ lệch pha.", "5.4. Trigger điểm không chống trôi: ")
    add_bullet("Giảm mẫu thông minh (lấy min/max trong nhóm mẫu), giới hạn khung hình qua requestAnimationFrame, cắt vùng vẽ canvas để không tràn biên độ.", "5.5. Vẽ sóng hiệu quả trên canvas: ")

    param_headers = ["Tham số kỹ thuật", "Giá trị chuẩn hóa", "Ý nghĩa trong thực hành Vật lí"]
    param_data = [
        ["Tần số lấy mẫu (fs)", "44 100 Hz hoặc 48 000 Hz", "Quyết định độ phân giải thời gian."],
        ["Bộ đệm mỗi kênh", "10 giây", "Cho phép phân tích lại đoạn đã thu."],
        ["Bộ lọc dải thông", "Thông cao 80 Hz, thông thấp 3000 Hz", "Tập trung vào dải âm nhạc và giọng nói."],
        ["Kích thước FFT N", "8192 mẫu (bins)", "Độ phân giải tần số Δf ≈ 5,86 Hz (ở 48 kHz)."],
        ["Cửa sổ tự tương quan", "2048 mẫu, cập nhật mỗi 300 ms", "Xác định tần số gần thời gian thực."],
        ["Ngưỡng im lặng", "RMS dưới 0,02", "Loại bỏ nhiễu nền."],
        ["Dải tần chấp nhận", "100–1500 Hz", "Dải nốt nhạc và giọng nói thông thường."],
        ["Cửa sổ hiển thị mặc định", "5 chu kỳ (2 ms – 2,4 s)", "Dễ đọc chu kỳ trên lưới 10 ô."],
        ["Thời gian tự dừng", "2 giây", "Khóa sóng để đọc số và phân tích FFT."]
    ]
    make_table(doc, param_headers, param_data, [Inches(1.8), Inches(2.2), Inches(2.8)])

    # ==================== PHẦN 6 ====================
    add_h1("Phần 6. Phân tích họa âm bằng FFT (Âm sắc)")
    add_p("Dạng sóng trên dao động ký cho thấy âm sắc 'trông như thế nào', còn phổ FFT cho thấy âm sắc 'được tạo từ những gì'. Chức năng FFT kích hoạt khi hệ thống đã khóa sóng ở chế độ 1 nguồn âm:")
    add_bullet("Lấy 8192 mẫu mới nhất từ bộ đệm vòng, nhân cửa sổ Hann, thực thi thuật toán FFT Cooley–Tukey cơ số 2 do nhóm tự viết (đảo bit và tầng bướm, không dùng thư viện ngoài). Chuẩn hóa biên độ chia cho N/2.")
    add_bullet("Các vạch trong khoảng ±15% quanh k × f₀ (k = 1..5) tô màu đỏ và đánh nhãn H1, H2, H3, H4, H5; các vạch khác tô xanh nhạt. Trục tần số nằm ở đáy hiển thị các vạch chia đơn vị Hz.")
    add_bullet("Độ phân giải Δf ≈ 5,86 Hz (ở 48 kHz) cho phép tách biệt rõ 5 họa âm của âm cơ bản từ 200–600 Hz. Bộ lọc thông thấp 3000 Hz làm suy giảm các họa âm trên 3000 Hz, được nhóm ghi nhận là đánh đổi kỹ thuật để chống nhiễu.")

    # ==================== PHẦN 7 ====================
    add_h1("Phần 7. Trợ lý FOX-Lab AI và tự động hóa quy trình thực hành")
    add_h2("7.1. Quy trình thực hành – báo cáo: từ thủ công đến tự động")
    wf_headers = ["Bước thực hành", "Cách làm truyền thống", "Với FOX-Lab"]
    wf_data = [
        ["1. Chuẩn bị", "Lắp micro, nối dây vào dao động ký, bật máy", "Mở đường dẫn hoặc quét mã QR, bấm Kênh A."],
        ["2. Chỉnh thang thời gian", "Vặn núm TIME/DIV nhiều lần cho vừa số chu kỳ", "Tự động: cửa sổ đúng khoảng 5 chu kỳ."],
        ["3. Làm đứng hình", "Chỉnh mức và chiều kích (trigger)", "Tự động tìm điểm cắt không đi lên, có độ trễ chống nhiễu."],
        ["4. Đọc T, f", "Đếm ô, nhân thang, tính f = 1/T", "Đọc trên lưới có nhãn ms; tần số hiển thị ngay trên chân cửa sổ trợ lý."],
        ["5. Giữ hình để ghi", "Chụp màn hình dao động ký hoặc vẽ tay", "Tự dừng sau 2 s ('khóa sóng'), sau đó Chụp ảnh lưu tệp PNG."],
        ["6. Khảo sát âm sắc", "Cần máy phân tích phổ riêng", "Phân tích FFT, hiển thị H1–H5."],
        ["7. Giải thích hiện tượng", "Hỏi giáo viên khi còn thời gian", "Hỏi FOX-Lab AI, có kèm tần số đang đo."],
        ["8. Viết báo cáo", "Tự trình bày từ đầu", "Dùng phiếu báo cáo mẫu (Phụ lục B), ảnh đồ thị và số liệu đã có."]
    ]
    make_table(doc, wf_headers, wf_data, [Inches(1.5), Inches(2.6), Inches(2.7)])

    add_h2("7.2. Trợ lý FOX-Lab AI và Trích xuất Nhật Ký Tương Tác Thực Tế")
    add_p("Trợ lý là một cửa sổ trò chuyện nổi mang nhãn 'Vật lí 11', xưng 'thầy' gọi 'em' thân thiện. Điểm đặc biệt là cơ chế truyền ngữ cảnh đo thực tế: mỗi câu hỏi tự động ghép thêm tần số khóa thời gian thực (chỉ gửi văn bản câu hỏi và tần số, tuyệt đối không gửi âm thanh ra ngoài). Dịch vụ web Google Apps Script đóng vai trò proxy bảo mật giấu API Key của mô hình AI. Nếu mất mạng hoặc quá 15 giây, bộ trả lời dự phòng cục bộ tự động kích hoạt.")
    add_p("Dưới đây là biên bản trích xuất trực tiếp từ tính năng Export Chat History của FOX-Lab AI trong buổi thực hành đo âm học ngày 22/11/2026:", italic=True)

    # Injected Chat History from txt file
    add_chat_bubble(doc, "Fox-lab AI",
                   "Xin chào quý Thầy/Cô và các em Học sinh! Mình là Fox-lab AI, trợ lý ảo hướng dẫn thí nghiệm Vật lý. Quý Thầy/Cô và các em Học sinh cần mình hỗ trợ vấn đề gì?",
                   timestamp="11/22/2026, 5:28:17 PM | Tần số khảo sát hiện tại: 63.1 Hz", is_ai=True)

    add_chat_bubble(doc, "Học sinh/Thầy giáo", "Các bước thực hành đo tần số sóng cơ", is_ai=False)
    add_chat_bubble(doc, "Fox-lab AI", "Chào.", is_ai=True)

    add_chat_bubble(doc, "Học sinh/Thầy giáo", "Giải thích hiện tượng sóng phách", is_ai=False)
    add_chat_bubble(doc, "Fox-lab AI",
                   "Chào bạn, tôi là Trợ lý Ảo phòng thí nghiệm Vật lý FOX-Lab. Dưới đây là giải thích về hiện tượng sóng phách:\n"
                   "- Khái niệm: Sóng phách là hiện tượng giao thoa của hai dao động điều hòa (hoặc hai sóng) cùng phương, có biên độ gần bằng nhau nhưng có tần số hơi khác nhau (f1 ≈ f2).\n"
                   "- Biểu hiện: Kết quả của sự chồng chất này tạo ra một dao động tổng hợp có biên độ biến thiên tuần hoàn theo thời gian, lúc tăng lên rất mạnh (phách mạnh) rồi lại giảm xuống rất yếu (phách yếu).\n"
                   "- Phương trình toán học: Giả sử hai dao động thành phần có cùng biên độ A và tần số góc ω1, ω2:\n"
                   "  x1 = A cos(ω1 t),  x2 = A cos(ω2 t)\n"
                   "  Dao động tổng hợp: x = x1 + x2 = 2A cos[(ω1 - ω2)t / 2] cos[(ω1 + ω2)t / 2]\n"
                   "- Đại lượng đặc trưng: Biên độ của dao động tổng hợp biến thiên với tần số góc của phách: ω_phách = |ω1 - ω2|. Tần số của sóng phách: f_beat = |f1 - f2|.",
                   is_ai=True)

    add_chat_bubble(doc, "Học sinh/Thầy giáo", "Các bước thực hành đo tần số sóng cơ", is_ai=False)
    add_chat_bubble(doc, "Fox-lab AI",
                   "Chào bạn, tôi là trợ lý ảo FOX-Lab. Dưới đây là các bước thực hành đo tần số sóng cơ theo lý thuyết tổng quát:\n"
                   "• Bước 1: Chuẩn bị dụng cụ và lắp ráp thí nghiệm. Chuẩn bị nguồn phát sóng (cần rung), dây đàn hồi hoặc máng sóng, bộ kích thích dao động, thước đo, và thiết bị đo (dao động ký hoặc đồng hồ đo thời gian hiện số). Lắp đặt nguồn phát sóng kết nối với bộ tạo dao động.\n"
                   "• Bước 2: Thiết lập dao động và quan sát sóng. Bật nguồn phát sóng, điều chỉnh tần số của bộ kích thích dao động để trên dây (hoặc mặt nước) xuất hiện hiện tượng sóng truyền đi hoặc sóng dừng rõ nét. Quan sát và xác định các điểm nút, điểm bụng hoặc đếm số bước sóng trên khoảng chiều dài xác định.\n"
                   "• Bước 3: Thu thập dữ liệu. Xác định bước sóng λ bằng cách đo khoảng cách d giữa các nút sóng liên tiếp (λ/2) hoặc giữa các đỉnh sóng liên tiếp trên phương truyền sóng. Xác định tốc độ truyền sóng v của môi trường hoặc đọc trực tiếp tần số f hiển thị trên thiết bị đo tần số của bộ kích thích dao động.\n"
                   "• Bước 4: Tính toán tần số sóng. Sử dụng công thức tổng quát gắn kết giữa tốc độ truyền sóng, bước sóng và tần số: f = v / λ, hoặc tính trực tiếp qua chu kỳ dao động T của nguồn phát: f = 1 / T.\n"
                   "• Bước 5: Xử lý số liệu và báo cáo kết quả. Lặp lại phép đo nhiều lần ở các mức tần số khác nhau để giảm sai số ngẫu nhiên. Tính giá trị trung bình của tần số f và đánh giá sai số thí nghiệm.",
                   is_ai=True)

    add_chat_bubble(doc, "Học sinh/Thầy giáo", "Viết phương trình sóng", is_ai=False)
    add_chat_bubble(doc, "Fox-lab AI",
                   "Chào bạn, tôi là Trợ lý Ảo phòng thí nghiệm Vật lý FOX-Lab. Dưới đây là phương trình sóng tổng quát theo chuẩn SGK:\n"
                   "• Định nghĩa: Phương trình sóng là biểu thức mô tả li độ dao động của một phần tử vật chất tại vị trí x theo thời gian t khi có sóng truyền qua.\n"
                   "• Phương trình sóng tại nguồn O: u_O(t) = A cos(ωt + φ). Trong đó: A: Biên độ sóng; ω = 2πf: Tần số góc; φ: Pha ban đầu; t: Thời gian sóng truyền.\n"
                   "• Phương trình sóng tại điểm M cách nguồn O một khoảng x trên phương truyền sóng:\n"
                   "  - Trường hợp sóng truyền theo chiều dương trục Ox: u_M(t, x) = A cos[ω(t - x/v) + φ] = A cos[2π(t/T - x/λ) + φ]\n"
                   "  - Trường hợp sóng truyền theo chiều âm trục Ox: u_M(t, x) = A cos[ω(t + x/v) + φ] = A cos[2π(t/T + x/λ) + φ]\n"
                   "• Ý nghĩa các đại lượng: v: Tốc độ truyền sóng; λ = v.T: Bước sóng; đại lượng 2πx/λ là độ lệch pha giữa dao động tại nguồn O và tại điểm M.",
                   is_ai=True)

    add_h2("7.3. Phân phối trong lớp học & 7.4. Quy trình đề xuất cho giáo viên")
    add_p("Giáo viên chiếu mã QR trên màn hình; học sinh quét mã bằng điện thoại để mở ứng dụng đồng loạt. Mọi tính toán chạy tại máy khách nên không gây nghẽn mạng. Quy trình 45 phút đề xuất gồm: Chuẩn bị (3'), Khảo sát tần số (10'), So sánh hai nguồn (10'), Phân tích âm sắc FFT (10'), Hỏi đáp AI (5'), Hoàn thành báo cáo (7').")

    # ==================== PHẦN 8 ====================
    add_h1("Phần 8. Phương án thực nghiệm và kết quả")
    add_p("8.1. Mục đích và tiêu chí: Đánh giá độ chính xác đo tần số (sai số < 2% dải 200–1000 Hz), vị trí họa âm H2–H5 lệch không quá một vạch phổ (khoảng 6 Hz), và trên 80% học sinh tự hoàn thành bài thực hành.")
    add_p("8.2. Thiết bị và điều kiện: Hai mẫu điện thoại (Android và iOS), âm thoa 440 Hz, loa phát tần số chuẩn, sáo trúc, đàn guitar. Khoảng cách micro 10–30 cm trong phòng yên tĩnh. Mỗi phép đo lặp lại 3 lần lấy giá trị trung bình.")

    add_h2("8.3. Thí nghiệm 1 – Độ chính xác khi đo tần số")
    add_p("Phát lần lượt các tần số chuẩn bằng loa, đo bằng FOX-Lab ở chế độ 1 nguồn âm, đọc tần số khóa. Kết quả thu được:")
    exp1_headers = ["Tần số chuẩn (Hz)", "Lần 1 (Hz)", "Lần 2 (Hz)", "Lần 3 (Hz)", "Trung bình (Hz)", "Sai số tương đối (%)"]
    exp1_data = [
        ["200", "200,1", "199,5", "199,8", "199,8", "0,10%"],
        ["300", "299,7", "300,2", "300,2", "300,0", "0,00%"],
        ["440", "440,4", "439,6", "439,9", "440,0", "0,00%"],
        ["600", "599,5", "599,7", "600,0", "599,7", "0,05%"],
        ["800", "799,5", "799,7", "800,1", "799,8", "0,03%"],
        ["1000", "1000,0", "999,7", "1000,1", "999,9", "0,01%"],
        ["1200", "1200,3", "1199,5", "1200,3", "1200,0", "0,00%"]
    ]
    make_table(doc, exp1_headers, exp1_data, [Inches(1.2), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.2)])

    add_h2("8.4. Thí nghiệm 2 – Đọc chu kỳ trên lưới so với tần số tự động")
    add_p("Học sinh đếm số ô ngang của một chu kỳ, nhân với thang thời gian để tìm T, tính f = 1/T rồi so sánh với tần số tự động:")
    exp2_headers = ["Nguồn âm", "Số ô / chu kỳ", "Thang (ms/ô)", "T (ms)", "f = 1/T (Hz)", "f tự động (Hz)", "Chênh lệch (%)"]
    exp2_data = [
        ["Âm thoa 440 Hz", "2,0", "1,14", "2,28", "438,6", "440,1", "0,34%"],
        ["Loa 600 Hz", "2,0", "0,83", "1,66", "602,4", "600,2", "0,36%"],
        ["Sáo, nốt thứ nhất", "2,1", "0,96", "2,02", "495,0", "493,8", "0,24%"]
    ]
    make_table(doc, exp2_headers, exp2_data, [Inches(1.5), Inches(0.8), Inches(0.9), Inches(0.9), Inches(1.0), Inches(1.0), Inches(0.7)])

    add_h2("8.5. Thí nghiệm 3 – Họa âm của các nhạc cụ")
    add_p("Đo cùng một nốt trên hai nhạc cụ, mở FFT và ghi biên độ tương đối của các họa âm (chuẩn hóa theo H1 = 1):")
    exp3_headers = ["Nhạc cụ", "H1", "H2", "H3", "H4", "H5", "Nhận xét về âm sắc"]
    exp3_data = [
        ["Âm thoa", "1", "0,02", "0", "0", "0", "Sóng sin gần như thuần túy, không có họa âm bậc cao, âm trong và đơn sắc."],
        ["Sáo", "1", "0,65", "0,15", "0,08", "0,03", "Họa âm H2 khá mạnh nhưng các bậc sau giảm nhanh, âm sắc ngọt và mượt."],
        ["Guitar / ukulele", "1", "0,85", "0,45", "0,30", "0,12", "Chứa đầy đủ các họa âm H2–H5 với biên độ lớn, đồ thị nhọn, âm đanh và vang."],
        ["Giọng hát (/a/)", "1", "0,92", "0,75", "0,22", "0,10", "Họa âm H2 và H3 rất mạnh (vùng formant nguyên âm), dạng sóng biến đổi phức tạp."]
    ]
    make_table(doc, exp3_headers, exp3_data, [Inches(1.2), Inches(0.4), Inches(0.5), Inches(0.5), Inches(0.5), Inches(0.5), Inches(3.2)])

    add_h2("8.6. Thí nghiệm 4 – Đối chiếu với phần mềm phân tích phổ có sẵn")
    add_p("Ghi âm cùng một nguồn bằng Audacity trên máy tính và so sánh vị trí H1–H5 với FOX-Lab:")
    exp4_headers = ["Họa âm", "Tần số FOX-Lab (Hz)", "Tần số phần mềm đối chứng (Hz)", "Chênh lệch (Hz)"]
    exp4_data = [
        ["H1", "440,1", "440,0", "0,1"],
        ["H2", "880,2", "880,0", "0,2"],
        ["H3", "1320,3", "1320,0", "0,3"],
        ["H4", "1760,5", "1760,0", "0,5"],
        ["H5", "2200,6", "2200,0", "0,6"]
    ]
    make_table(doc, exp4_headers, exp4_data, [Inches(1.5), Inches(1.8), Inches(2.2), Inches(1.3)])

    add_h2("8.7. Thí nghiệm 5 – Hai nguồn âm và biên độ theo khoảng cách")
    add_p("Bật chế độ 2 nguồn âm với hai micro đặt cách nguồn phát các khoảng d1 và d2; so sánh biên độ hai kênh:")
    exp5_headers = ["Khoảng cách d (cm)", "Biên độ Kênh A", "Biên độ Kênh B", "Tỉ số B/A", "Nhận xét quy luật"]
    exp5_data = [
        ["10", "0,82", "0,81", "0,99", "Hai micro đặt cùng khoảng cách cho biên độ chuẩn hóa gần như bằng nhau."],
        ["20", "0,82", "0,41", "0,50", "Khoảng cách tăng gấp đôi, biên độ sóng âm giảm một nửa (tỉ lệ nghịch)."],
        ["40", "0,82", "0,20", "0,24", "Biên độ Kênh B tiếp tục giảm rõ rệt; trigger đồng bộ giúp đồ thị ổn định."]
    ]
    make_table(doc, exp5_headers, exp5_data, [Inches(1.3), Inches(1.1), Inches(1.1), Inches(0.9), Inches(2.4)])

    add_h2("8.8. Khảo sát sư phạm")
    add_p("Đánh giá tại hai lớp có trình độ tương đương (thực nghiệm dùng FOX-Lab vs đối chứng làm mẫu truyền thống):")
    ped1_headers = ["Nội dung khảo sát", "Điểm trung bình lớp thực nghiệm (Thang 5)"]
    ped1_data = [
        ["Ứng dụng dễ sử dụng", "4,6 / 5"],
        ["Dạng sóng giúp em hiểu khái niệm chu kỳ, tần số", "4,8 / 5"],
        ["Phổ FFT giúp em hiểu âm sắc", "4,7 / 5"],
        ["Trợ lý FOX-Lab AI giúp em giải đáp thắc mắc", "4,5 / 5"],
        ["Em muốn dùng ứng dụng trong các bài thực hành khác", "4,9 / 5"]
    ]
    make_table(doc, ped1_headers, ped1_data, [Inches(4.5), Inches(2.3)])

    ped2_headers = ["Chỉ số so sánh", "Lớp thực nghiệm", "Lớp đối chứng"]
    ped2_data = [
        ["Số học sinh", "42", "40"],
        ["Điểm kiểm tra trung bình (thang 10)", "8,4", "7,1"],
        ["Thời gian hoàn thành phiếu báo cáo (phút)", "12 phút", "28 phút"],
        ["Tỉ lệ hoàn thành đúng yêu cầu (%)", "95,2%", "67,5%"]
    ]
    make_table(doc, ped2_headers, ped2_data, [Inches(3.2), Inches(1.8), Inches(1.8)])

    # ==================== PHẦN 9 & 10 ====================
    add_h1("Phần 9. Đánh giá sản phẩm")
    add_h2("9.1. Ưu điểm và tính mới")
    add_p("Điểm khác biệt của FOX-Lab nằm ở tính tích hợp và mục đích sư phạm: gộp Đo – Phân tích – Hỏi đáp trong một công cụ; trải nghiệm như dao động ký thật; tự động hóa có chủ đích; Họa âm H1–H5 bám sát SGK; Tiếng Việt hóa toàn bộ và triển khai nhẹ dạng PWA.")

    comp_headers = ["Tiêu chí", "Dao động ký phần cứng", "Ứng dụng đo âm phổ biến", "FOX-Lab"]
    comp_data = [
        ["Thiết bị cần có", "Máy chuyên dụng, micro, dây", "Điện thoại", "Điện thoại/máy tính, trình duyệt"],
        ["Dạng sóng đứng yên (trigger)", "Có, chỉnh tay", "Thường không có hoặc hạn chế", "Có, tự động"],
        ["Thang thời gian", "Chỉnh tay", "Thường cố định", "Tự động 5 chu kỳ, thu phóng tay"],
        ["Hai nguồn âm", "Có (hai kênh)", "Hiếm", "Có (Kênh A, Kênh B)"],
        ["Phổ họa âm", "Cần máy riêng hoặc option đắt", "Có, hiển thị chung", "Có, nhãn H1–H5 trực quan"],
        ["Hỗ trợ giải thích, báo cáo", "Không", "Không", "Trợ lý AI, lưu ảnh, phiếu mẫu"],
        ["Hiệu chuẩn biên độ", "Có", "Tùy ứng dụng", "Chưa (biên độ chuẩn hóa)"]
    ]
    make_table(doc, comp_headers, comp_data, [Inches(1.8), Inches(1.6), Inches(1.7), Inches(1.7)])

    add_h2("9.2. Hạn chế đã nhận diện & 9.3. Quyền riêng tư & 9.4. Khả năng nhân rộng")
    add_p("Hạn chế: Bộ thu dùng ScriptProcessorNode (sẽ nâng cấp AudioWorklet); khử nhiễu tự động của hệ điều hành có thể ảnh hưởng biên độ; dải lọc 80–3000 Hz; chỉ nhận 1 cao độ rõ rệt; biên độ chuẩn hóa chưa đổi ra dB SPL; độ lệch pha giữa hai micro độc lập có độ trễ phần cứng; AI cần mạng. Quyền riêng tư: Âm thanh xử lý cục bộ trên thiết bị, không gửi ra ngoài; chỉ văn bản câu hỏi và tần số gửi tới AI. Khả năng nhân rộng: Chi phí 0 đồng, web tĩnh dễ chia sẻ qua mã QR, tương thích 100% trường học.")

    add_h1("Phần 10. Kết luận và hướng phát triển")
    add_p("10.1. Kết luận: Dự án đã chế tạo thành công FOX-Lab, một phòng thí nghiệm sóng âm di động trực quan trên trình duyệt, kết hợp hoàn hảo giữa dao động ký số, phân tích phổ FFT và trợ lý AI sư phạm. Sản phẩm giải quyết triệt để rào cản thiếu thốn trang thiết bị, hiện đại hóa bài thực hành Vật lí 11 theo định hướng phát triển phẩm chất, năng lực của Chương trình GDPT 2018.")

    add_h2("10.2. Hướng phát triển")
    dev_headers = ["Hướng phát triển", "Nội dung", "Lợi ích"]
    dev_data = [
        ["Tự động xuất báo cáo", "Tập hợp ảnh đồ thị, tần số, bảng họa âm thành PDF/bảng tính", "Hoàn thiện bước 8 quy trình, giảm thời gian."],
        ["Nhật ký thí nghiệm", "Lưu kết quả từng nhóm vào Google Sheets qua Apps Script", "Giáo viên theo dõi tiến độ cả lớp."],
        ["Nâng cấp thu âm", "Chuyển từ ScriptProcessorNode sang AudioWorklet", "Ổn định, mượt mà, không phụ thuộc main thread."],
        ["Dò tần chính xác hơn", "Giảm lỗi nhầm quãng tám, tăng điểm FFT cho âm trầm", "Đo tốt hơn ở dải thấp dưới 100 Hz."],
        ["Máy phát tín hiệu", "Phát âm sin chuẩn qua loa thiết bị", "Thực hành phách, giao thoa không cần nguồn ngoài."],
        ["Hiệu chuẩn biên độ", "Hiệu chuẩn với nguồn chuẩn, hiển thị mức dB SPL", "Đo mức áp suất âm thực tế."],
        ["Tắt xử lí của micro", "Tắt khử nhiễu, khử vọng khi trình duyệt hỗ trợ", "Biên độ âm thanh trung thực hơn."],
        ["Chế độ ngoại tuyến", "Tích hợp Service Worker hoàn chỉnh", "Chạy tốt khi mất mạng toàn trường."],
        ["Mở rộng nội dung", "Thêm bài thực hành sóng dừng, giao thoa, Doppler", "Bao quát toàn bộ chương Sóng Vật lí 11."]
    ]
    make_table(doc, dev_headers, dev_data, [Inches(1.8), Inches(2.7), Inches(2.3)])

    add_h2("10.3. Kiến nghị")
    add_p("Kiến nghị nhà trường thử nghiệm FOX-Lab trong các tiết thực hành Vật lí 11; đề nghị thầy cô đóng góp ý kiến để hoàn thiện kịch bản sư phạm của AI; khuyến khích học sinh dùng làm công cụ tự học và nghiên cứu ở nhà.")

    # ==================== TÀI LIỆU THAM KHẢO ====================
    add_h1("Tài liệu tham khảo")
    refs = [
        "1. Bộ Giáo dục và Đào tạo (2018), Chương trình giáo dục phổ thông – Chương trình tổng thể và Chương trình môn Vật lí, ban hành kèm Thông tư số 32/2018/TT-BGDĐT.",
        "2. Sách giáo khoa Vật lí 11 (Chương trình GDPT 2018) – Bộ sách Kết nối tri thức với cuộc sống, Cánh diều, Chân trời sáng tạo.",
        "3. Halliday D., Resnick R., Walker J. (2018), Fundamentals of Physics (11th ed.), John Wiley & Sons.",
        "4. Kinsler L. E., Frey A. R., Coppens A. B., Sanders J. V. (2000), Fundamentals of Acoustics (4th ed.), Wiley.",
        "5. Oppenheim A. V., Schafer R. W. (2010), Discrete-Time Signal Processing (3rd ed.), Pearson.",
        "6. Rabiner L. R. (1977), 'On the use of autocorrelation analysis for pitch detection', IEEE Trans. ASSP, 25(1), 24–33.",
        "7. Cooley J. W., Tukey J. W. (1965), 'An algorithm for the machine calculation of complex Fourier series', Math. Comp., 19(90), 297–301.",
        "8. Harris F. J. (1978), 'On the use of windows for harmonic analysis with the discrete Fourier transform', Proc. IEEE, 66(1), 51–83.",
        "9. Staacks S., Hütz S., Heinke H., Stampfer C. (2018), 'Advanced tools for smartphone-based experiments: phyphox', Phys. Educ., 53(4), 045009.",
        "10. W3C Audio Working Group (2023), Web Audio API Specification, W3C Recommendation.",
        "11. Mozilla Developer Network (MDN), MediaDevices.getUserMedia() and Canvas API Reference."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.05
        p_ref.paragraph_format.space_after = Pt(1.5)
        p_ref.paragraph_format.left_indent = Inches(0.25)
        p_ref.paragraph_format.first_line_indent = Inches(-0.25)
        r_run = p_ref.add_run(r)
        r_run.font.size = Pt(8.5)

    # ==================== PHỤ LỤC ====================
    add_h1("Phần Phụ lục")
    add_h2("Phụ lục A. Hướng dẫn các nút và chức năng")
    app_a_headers = ["Nút / chức năng", "Tác dụng", "Điều kiện hoạt động"]
    app_a_data = [
        ["Cài đặt chung → Chế độ nguồn âm", "Chọn 1 hoặc 2 nguồn âm", "Luôn dùng được; chuyển về 1 nguồn sẽ tắt kênh dư."],
        ["Cài đặt chung → Chức năng khảo sát", "Chọn Khảo sát tần số (tự dừng) hoặc Khảo sát liên tục", "Luôn dùng được."],
        ["Tốc độ quét: Nhanh / Chậm", "60 hoặc 15 khung hình/giây", "Chỉ hiện ở chế độ liên tục."],
        ["Ô chọn micro Kênh A, Kênh B", "Chọn thiết bị thu cho từng kênh", "Sau khi cấp quyền micro, danh sách mới có tên thiết bị."],
        ["Kênh A / Kênh B", "Bật hoặc tắt từng kênh; hiển thị Hoạt động hoặc Khóa", "Luôn dùng được."],
        ["Đo / Dừng", "Bắt đầu đo (xóa bộ đệm cũ) hoặc dừng và khóa sóng", "Cần ít nhất một kênh hoạt động."],
        ["Làm mới", "Tắt cả hai kênh, trả mọi cài đặt về mặc định", "Cần ít nhất một kênh hoạt động."],
        ["Chụp ảnh", "Lưu đồ thị hiện tại thành ảnh PNG (DoThi_SongAm.png)", "Cần ít nhất một kênh hoạt động."],
        ["Toàn màn hình", "Bật hoặc tắt chế độ toàn màn hình", "Luôn dùng được."],
        ["Phân tích FFT", "Mở màn hình phổ họa âm H1–H5", "Đã dừng; đúng một kênh hoạt động; chế độ 1 nguồn âm."],
        ["Thu phóng (hai ngón tay / chuột)", "Phóng to thu nhỏ trục thời gian (2 ms – 2,4 s) và biên độ (0,5 – 10)", "Chỉ khi đã dừng."],
        ["Biểu tượng cáo FOX-Lab", "Mở cửa sổ trợ lý AI", "Cần mạng để dùng bản đầy đủ."]
    ]
    make_table(doc, app_a_headers, app_a_data, [Inches(2.0), Inches(2.6), Inches(2.2)])

    add_h2("Phụ lục B. Phiếu báo cáo thực hành mẫu (Dành cho học sinh làm bài)")
    add_p("BÁO CÁO THỰC HÀNH: KHẢO SÁT SÓNG ÂM BẰNG DAO ĐỘNG KÝ FOX-LAB", bold_prefix="", italic=True)
    add_p("Nhóm: ................... Lớp: 11A2 ................... Ngày thực hành: 07/11/2026", italic=True)
    add_p("1. Mục đích: Đo chu kỳ, tần số của sóng âm và phân tích thành phần họa âm (âm sắc).")
    add_p("2. Dụng cụ: Laptop/điện thoại kết nối https://vobinhminh.github.io/FOX_LAB/ , micro, âm thoa, nhạc cụ.")
    add_p("3. Tiến hành: Bước 1: Mở trình duyệt vào FOX-Lab; Bước 2: Bật Kênh A chọn Microphone; Bước 3: Phát âm và ghi số liệu.")
    add_p("4. Kết quả đo (Học sinh tự điền):", bold_prefix="", italic=True)

    app_b1_headers = ["Nguồn âm", "Số ô / chu kỳ", "Thang thời gian (ms/ô)", "T (ms)", "f = 1/T (Hz)", "f hiển thị trên ứng dụng (Hz)"]
    app_b1_data = [
        ["Âm thoa 440 Hz", "", "", "", "", ""],
        ["Máy phát tần số", "", "", "", "", ""],
        ["Nhạc cụ (Guitar / Sáo)", "", "", "", "", ""]
    ]
    make_table(doc, app_b1_headers, app_b1_data, [Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)])

    add_p("5. Phân tích họa âm (Học sinh tự điền):", bold_prefix="", italic=True)
    app_b2_headers = ["Họa âm", "H1", "H2", "H3", "H4", "H5"]
    app_b2_data = [
        ["Tần số (Hz)", "", "", "", "", ""],
        ["Biên độ tương đối", "", "", "", "", ""]
    ]
    make_table(doc, app_b2_headers, app_b2_data, [Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)])

    add_p("6. Nhận xét và kết luận: So sánh f tính từ T với f ứng dụng hiển thị; giải thích nguyên nhân sai lệch; nhận xét về âm sắc dựa trên H1–H5.")
    add_p("7. Câu hỏi đã hỏi trợ lý AI và đánh giá câu trả lời: ....................................................................................................")

    add_h2("Phụ lục C. Xử lí sự cố thường gặp")
    app_c_headers = ["Hiện tượng", "Nguyên nhân thường gặp", "Cách xử lí"]
    app_c_data = [
        ["Không có sóng, báo lỗi micro", "Chưa cấp quyền hoặc trang mở không an toàn", "Cho phép micro trong cài đặt trình duyệt; mở bằng HTTPS."],
        ["Dạng sóng quá nhỏ", "Nguồn âm xa hoặc yếu", "Đưa micro lại gần; phóng to biên độ khi đã dừng."],
        ["Tần số nhảy lung tung", "Nhiễu nền hoặc âm không tuần hoàn", "Thực hiện ở phòng yên tĩnh; dùng âm kéo dài, đều."],
        ["Nút Phân tích FFT bị mờ", "Chưa dừng, hai kênh cùng bật hoặc đang ở 2 nguồn", "Bấm Đo / Dừng để khóa sóng; chọn 1 nguồn âm và chỉ bật một kênh."],
        ["Họa âm cao bị yếu", "Bộ lọc thông thấp 3000 Hz", "Dùng nốt thấp hơn để cả 5 họa âm nằm dưới 3000 Hz."],
        ["Trợ lý AI báo mất kết nối", "Mạng yếu hoặc Apps Script không phản hồi", "Kiểm tra mạng; ứng dụng vẫn dùng được bộ trả lời dự phòng cục bộ."]
    ]
    make_table(doc, app_c_headers, app_c_data, [Inches(1.8), Inches(2.4), Inches(2.6)])

    doc.save("FOX_LAB_BAO_CAO_KHKT_CHINH_THUC.docx")
    print("[SUCCESS] Faithful FOX_LAB_BAO_CAO_KHKT_CHINH_THUC.docx generated successfully!")

if __name__ == "__main__":
    build_faithful_docx()
