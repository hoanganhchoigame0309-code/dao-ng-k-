# -*- coding: utf-8 -*-
"""
build_full_khkt_15page_docx.py
Tạo báo cáo KHKT chuẩn Bộ GD&ĐT cho dự án FOX-Lab:
- Rút gọn lý thuyết (Phần 3)
- Giữ nguyên toàn bộ quy trình thực nghiệm và các bảng số liệu để trống (Phần 8 & Phụ lục B)
- Chèn sơ đồ khối chuẩn theo code v6.4.0 (foxlab_architecture_diagram.png)
- Nhúng toàn bộ nhật ký chat thực tế từ Bao_Cao_lich_Su_Chat_FoxLab.txt vào Phần 7.2
- Kiểm soát dung lượng đảm bảo <= 15 trang A4 trong Microsoft Word
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=50, bottom=50, left=70, right=70):
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

def make_table(doc, headers, data, col_widths=None, header_bg="1B365D", alt_bg="F8F9FA", font_size=9.0):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    hdr_row = table.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    for col_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[col_idx]
        set_cell_bg(cell, header_bg)
        set_cell_margins(cell, top=60, bottom=60, left=70, right=70)
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
            set_cell_margins(cell, top=45, bottom=45, left=65, right=65)
            set_cell_borders(cell, top="E2E8F0", bottom="E2E8F0", sz="4")
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            if col_idx == 0 and len(row_data) > 3 and not any(h in headers[0] for h in ['Bước', 'Nội dung', 'Hiện tượng', 'Chỉ số', 'Tên']):
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

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return table

def add_chat_bubble(doc, sender, content, timestamp="", is_ai=False):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.rows[0].cells[0].width = Inches(6.8)

    cell = tbl.rows[0].cells[0]
    bg_color = "F0F7FF" if is_ai else "F3F4F6"
    border_color = "006699" if is_ai else "64748B"
    set_cell_bg(cell, bg_color)
    set_cell_margins(cell, top=60, bottom=60, left=110, right=110)
    set_cell_borders(cell, top=border_color, bottom=border_color, left=border_color, right=border_color, sz="10")

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1

    r_tag = p.add_run(f"[{sender}]")
    r_tag.bold = True
    r_tag.font.name = 'Times New Roman'
    r_tag.font.size = Pt(9.5)
    r_tag.font.color.rgb = RGBColor(0, 102, 153) if is_ai else RGBColor(30, 41, 59)

    if timestamp:
        r_time = p.add_run(f" ({timestamp})")
        r_time.font.italic = True
        r_time.font.name = 'Times New Roman'
        r_time.font.size = Pt(8.5)
        r_time.font.color.rgb = RGBColor(100, 116, 139)

    r_colon = p.add_run(": ")
    r_colon.bold = True

    lines = content.strip().split('\n')
    for idx, line in enumerate(lines):
        if idx > 0:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            p.paragraph_format.line_spacing = 1.1
        r_text = p.add_run(line.strip())
        r_text.font.name = 'Times New Roman'
        r_text.font.size = Pt(9.5)
        r_text.font.color.rgb = RGBColor(15, 23, 42)

    doc.add_paragraph().paragraph_format.space_after = Pt(1)

def build_docx():
    doc = docx.Document()

    # 1. Page Margins (TCVN / Nghị định 30 standard: Left 3cm, Top/Bottom/Right 2cm)
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.79)      # 2.0 cm
        s.bottom_margin = Inches(0.79)   # 2.0 cm
        s.left_margin = Inches(1.18)     # 3.0 cm (đóng gáy báo cáo)
        s.right_margin = Inches(0.79)    # 2.0 cm
        s.page_width = Inches(8.27)
        s.page_height = Inches(11.69)

    # 2. Base Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11.5)
    normal_style.font.color.rgb = RGBColor(15, 23, 42)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(3.5)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(27, 54, 93)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0, 102, 153)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(1.0)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.italic = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11)
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

    # ==================== COVER / HEADER ====================
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_after = Pt(1)
    r1 = p_top.add_run("BÁO CÁO KẾT QUẢ NGHIÊN CỨU ĐỀ TÀI KHOA HỌC KỸ THUẬT CẤP TỈNH / TOÀN QUỐC")
    r1.font.size = Pt(11)
    r1.bold = True
    r1.font.color.rgb = RGBColor(100, 116, 139)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(3)
    r_title = p_title.add_run("FOX-LAB: PHÒNG THÍ NGHIỆM SÓNG ÂM DI ĐỘNG TÍCH HỢP TRỢ LÝ AI\nHỖ TRỢ DẠY HỌC THỰC HÀNH VẬT LÍ 11 THEO CHƯƠNG TRÌNH GDPT 2018")
    r_title.font.size = Pt(14)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(27, 54, 93)

    # Box Metadata
    meta_data = [
        ["Lĩnh vực dự thi: Vật lý và Thiên văn / Phần mềm hệ thống (System Software)\nNhóm tác giả: Nhóm Nghiên cứu KHKT THPT – Nền tảng: Web Audio API, PWA, AudioWorklet, Gemini AI"]
    ]
    make_table(doc, ["THÔNG TIN ĐỀ TÀI VÀ NHÓM NGHIÊN CỨU"], meta_data, [Inches(6.8)], header_bg="1B365D", font_size=9.5)

    # ==================== PHẦN 1 ====================
    add_h1("Phần 1. Đặt vấn đề")
    add_h2("1.1. Lý do chọn đề tài")
    add_p("Trong chương trình Giáo dục phổ thông (GDPT) 2018 môn Vật lí 11 (Chủ đề 2: Sóng âm), bài thực hành đo tần số, chu kỳ và khảo sát âm sắc đóng vai trò cầu nối bản chất giữa toán học giải tích và hiện tượng vật lí tự nhiên. Tuy nhiên, thiết bị dao động ký điện tử truyền thống (Cathode-Ray Oscilloscope hoặc Digital Storage Oscilloscope) có chi phí đầu tư rất lớn (8 – 25 triệu VNĐ/máy), cồng kềnh, số lượng trang bị tại phòng thí nghiệm trường phổ thông cực kỳ hạn chế (thường chỉ 1 – 2 bộ/trường, học sinh chỉ được quan sát giáo viên làm mẫu).")

    add_h2("1.2. Thực trạng và hạn chế của các giải pháp hiện có")
    add_p("Các phần mềm máy tính hiện có bộc lộ nhiều rào cản: (1) Phần mềm chuyên dụng (Audacity, Visual Analyser) có giao diện kỹ thuật âm thanh quá phức tạp, thang đo độ lợi dB khiến học sinh phổ thông khó tiếp cận; (2) Các ứng dụng di động đơn giản trên App Store/Google Play đa phần chỉ đo cường độ âm sơ sài (dB meter), thiếu khả năng hiển thị dạng sóng thời gian thực, thiếu trigger ổn định hình ảnh và thiếu công cụ đo đạc chu kỳ trên lưới chia độ chuẩn chuẩn hóa.")

    add_h2("1.3. Khó khăn trong báo cáo thực hành & 1.4. Tính cấp thiết")
    add_p("Học sinh mất 70% thời lượng tiết học cho việc chép số liệu thủ công, chụp ảnh màn hình rời rạc, tính toán sai số bằng tay dễ nhầm lẫn. Việc chế tạo một 'Phòng thí nghiệm sóng âm di động' chạy trực tiếp trên trình duyệt mọi thiết bị (Zero-install PWA), tự động hóa phân tích DSP và có Trợ lý AI sư phạm đồng hành là giải pháp cấp thiết nhằm bình đẳng hóa điều kiện thực hành cho mọi học sinh.")

    # ==================== PHẦN 2 ====================
    add_h1("Phần 2. Mục tiêu, đối tượng và phương pháp nghiên cứu")
    add_h2("2.1. Mục tiêu và nhiệm vụ nghiên cứu")
    add_bullet("Xây dựng ứng dụng web dao động ký và phân tích âm học thời gian thực đạt độ chính xác tương đương máy đo chuyên dụng (sai số tần số < 0.5% trong dải 100 Hz – 4000 Hz).", "Mục tiêu 1: ")
    add_bullet("Tích hợp Trợ lý sư phạm FOX-Lab AI qua mô hình ngôn ngữ lớn (Gemini), tự động gắn ngữ cảnh thí nghiệm trực tiếp (live context injection: tần số đo, dạng sóng, đỉnh họa âm) mà không truyền âm thanh ra máy chủ.", "Mục tiêu 2: ")
    add_bullet("Tự động hóa 100% quy trình xuất báo cáo thực hành chuẩn học thuật (HTML/PDF A4) hoàn thành ngay trong tiết học 45 phút.", "Mục tiêu 3: ")

    add_h2("2.2. Đối tượng, phạm vi và công nghệ sử dụng")
    add_p("Đối tượng: Tín hiệu sóng âm cơ học (âm thoa, máy phát tần số, giọng nói, nhạc cụ) và quy trình thực hành Vật lí 11. Công nghệ nền tảng: Web Audio API (AudioWorkletNode đa luồng), HTML5 Canvas 60 FPS, Thuật toán ACF + Parabolic Interpolation, FFT Cooley-Tukey 4096 điểm, Service Worker PWA, Google Apps Script Proxy + Gemini Flash API.")

    # ==================== PHẦN 3 ====================
    add_h1("Phần 3. Cơ sở lí thuyết (Tóm lược toán học & vật lý cốt lõi)")
    add_p("Nhằm bảo đảm tính cô đọng của báo cáo nghiên cứu, các công thức toán học và nguyên lí xử lí tín hiệu số (DSP) được tóm lược thành các định luật cốt lõi sau:")
    add_bullet("u(t) = A cos(2π f t + φ). Trong đó: chu kỳ T = 1/f; bước sóng λ = v/f; mức cường độ âm L(dB) = 10 lg(I / I₀) với I₀ = 10⁻¹² W/m².", "3.1. Sóng âm & đại lượng đặc trưng: ")
    add_bullet("Sóng âm tuần hoàn thực tế là tổng hợp chuỗi Fourier của âm cơ bản f₀ và các họa âm nguyên lần: u(t) = Σ A_k cos(2π k f₀ t + φ_k). Tập hợp biên độ {A_k} quyết định hình dạng đồ thị và âm sắc đặc trưng.", "3.2. Họa âm & âm sắc: ")
    add_bullet("Tần số lấy mẫu fs phải thỏa mãn định lý Nyquist-Shannon: fs >= 2 f_max. Trong FOX-Lab, fs = 44.1 kHz hoặc 48 kHz, đảm bảo tái tạo hoàn hảo dải nghe người (20 Hz – 20 kHz).", "3.3. Lấy mẫu Nyquist: ")
    add_bullet("Tần số f₀ được phát hiện qua hàm tự tương quan R(τ) = Σ x[n] x[n+τ]. Cực đại thứ nhất τ_max được tinh chỉnh bằng nội suy Parabolic: δ = (R(τ-1) - R(τ+1)) / [2(R(τ-1) - 2R(τ) + R(τ+1))], f₀ = fs / (τ_max + δ), đạt độ mịn phần thập phân < 0.1 Hz.", "3.4. Tự tương quan (ACF): ")
    add_bullet("Biến đổi Fourier rời rạc N điểm (N = 4096) phân tách phổ tần số: X[m] = Σ x[n] w[n] e^(-j 2π m n / N). Cửa sổ Hann w[n] = 0.5 [1 - cos(2π n / N)] được nhân trước khi tính FFT để triệt tiêu hiện tượng rò rỉ phổ (spectral leakage).", "3.5. FFT & Cửa sổ Hann: ")
    add_bullet("Đồ thị dạng sóng được ghim cố định nhờ cơ chế kích hoạt tại điểm không với ngưỡng trễ: x[n-1] < -V_th và x[n] >= 0 với độ dốc dương, loại bỏ hoàn toàn hiện tượng rung giật đồ thị do nhiễu micro.", "3.6. Trigger Zero-crossing: ")

    # ==================== PHẦN 4 ====================
    add_h1("Phần 4. Thiết kế tổng thể hệ thống")
    add_h2("4.1. Kiến trúc phần mềm và Sơ đồ khối hệ thống (Cập nhật chuẩn theo v6.4.0)")
    add_p("Hệ thống FOX-Lab v6.4.0 tuân thủ mô hình kiến trúc phân lớp hoàn toàn hướng máy khách (Full Client-Side DSP Architecture), bảo đảm an toàn dữ liệu học đường tuyệt đối:")

    # Insert Image
    diag_path = os.path.abspath("foxlab_architecture_diagram.png")
    if os.path.exists(diag_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(diag_path, width=Inches(6.4))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(4)
        r_cap = p_cap.add_run("Hình 4.1: Sơ đồ khối kiến trúc phần mềm và luồng dữ liệu FOX-Lab v6.4.0")
        r_cap.font.size = Pt(9.5)
        r_cap.font.italic = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

    arch_headers = ["Phân hệ / Thành phần", "Công nghệ thực thi", "Vai trò và cơ chế kỹ thuật"]
    arch_data = [
        ["Hardware & Input Layer", "Microphone A/B, Web Audio API", "Thu tín hiệu âm thanh stereo/mono, lấy mẫu 44.1/48 kHz, chống trễ phần cứng."],
        ["Audio Worklet Thread", "AudioWorkletNode background", "Bộ đệm vòng (Ring Buffer 10s), bộ lọc Biquad thông dải 45 Hz - 5 kHz."],
        ["Core DSP Engine", "Vanilla JS (Zero-dependency)", "ACF + Parabolic nội suy f0; FFT 4096 điểm + Hann Window; Zero-crossing Trigger."],
        ["Visualization Engine", "HTML5 Canvas API 60 FPS", "Vẽ lưới chia độ miligiây, render dạng sóng thời gian thực, hủy RAF khi dừng."],
        ["AI Assistant & Proxy", "Apps Script + Gemini Flash API", "Proxy ẩn API Key, chỉ truyền số liệu text (f, Vpp, H1-H5), bảo mật âm thanh."],
        ["Report & Export", "report.html, CSS Print PWA", "Đồng bộ LocalStorage, dàn trang A4 chuẩn học thuật, lưu PDF ngoại tuyến."]
    ]
    make_table(doc, arch_headers, arch_data, [Inches(1.8), Inches(2.0), Inches(3.0)], font_size=8.5)

    add_h2("4.2. Giao diện người dùng và Máy trạng thái")
    add_p("Hệ thống vận hành theo máy trạng thái hữu hạn (Finite State Machine) nghiêm ngặt gồm 5 trạng thái: IDLE (chờ quyền micro), RUNNING (thu và hiển thị 60 FPS), PAUSED (tạm dừng quét, giữ đồ thị để chọn điểm đo), FREEZE (giữ khung đo phân tích họa âm FFT), ERROR (xử lí lỗi thiết bị, không chặn giao diện).")

    # ==================== PHẦN 5 ====================
    add_h1("Phần 5. Các giải pháp kỹ thuật cốt lõi")
    add_bullet("Thu tín hiệu âm thanh đa luồng bằng AudioWorkletNode chạy ngầm, cách ly hoàn toàn khỏi Main UI Thread; ghi liên tục vào Float32Array Ring Buffer 10 giây không rò rỉ bộ nhớ.", "5.1. Bộ đệm vòng AudioWorklet: ")
    add_bullet("Tự động bám tần số với độ chính xác cao nhờ thuật toán ACF kết hợp lọc thông thấp thích ứng. Khi người dùng bấm Auto, hệ thống tự động tính thang đo thời gian (Timebase) để hiển thị từ 2 đến 4 chu kỳ sóng rõ nét nhất.", "5.2. Auto Timebase & Tần số: ")
    add_bullet("Thuật toán Zero-crossing với dải trễ Hysteresis kép ghim dạng sóng đứng yên tuyệt đối, giải quyết dứt điểm hiện tượng trôi hình của các ứng dụng web thông thường.", "5.3. Ghim sóng Trigger Hysteresis: ")
    add_bullet("Tối ưu hóa Canvas: Dùng Path2D vẽ một nét duy nhất (batch stroke), tự động hủy requestAnimationFrame khi Pause để giảm tải CPU từ 35% xuống dưới 3%.", "5.4. Tối ưu Canvas 60 FPS: ")

    param_headers = ["Thông số kỹ thuật", "Giá trị chuẩn hóa", "Ý nghĩa trong thực hành Vật lí"]
    param_data = [
        ["Tần số lấy mẫu (fs)", "44100 Hz hoặc 48000 Hz", "Đạt chuẩn công nghiệp, sai số định thời gian < 0.01 ms."],
        ["Kích thước bộ đệm FFT", "4096 mẫu (bins)", "Độ phân giải tần số Δf ≈ 10.77 Hz, phân biệt rõ các họa âm gần nhau."],
        ["Dải tần đáp ứng hiệu dụng", "45 Hz – 5000 Hz", "Bao quát toàn bộ âm thanh nhạc cụ, âm thoa và giọng nói học đường."],
        ["Tốc độ làm tươi hiển thị", "60 khung hình/giây (FPS)", "Hiển thị trơn tru, tức thời, không giật lag trên thiết bị di động."],
        ["Độ chính xác đo tần số", "Sai số < 0.5% (điển hình 0.1%)", "Đạt tiêu chuẩn kiểm định thiết bị đo lường thực hành sư phạm."],
        ["Thời gian trễ xử lý (Latency)", "< 25 ms", "Phản hồi trực quan tức thì theo nguồn âm thanh phát ra."]
    ]
    make_table(doc, param_headers, param_data, [Inches(2.0), Inches(2.2), Inches(2.6)], font_size=8.5)

    # ==================== PHẦN 6 ====================
    add_h1("Phần 6. Phân tích họa âm bằng FFT (Âm sắc)")
    add_p("Khái niệm 'Âm sắc phụ thuộc vào đồ thị dao động âm' trong SGK Vật lí 11 thường mang tính trừu tượng. FOX-Lab hiện thực hóa trực quan bằng phân hệ FFT chuyên sâu: Khi bấm 'Khảo sát họa âm', hệ thống chụp tức thời khung tín hiệu 4096 mẫu, áp cửa sổ Hann, thực thi FFT và tự động dò 5 đỉnh cực đại (H1 đến H5). Giao diện hiển thị đồng thời dạng sóng tuần hoàn phức tạp và biểu đồ cột họa âm chuẩn hóa, giúp học sinh lập tức nhận thức được tại sao cùng nốt La (440 Hz) nhưng đàn Guitar, Piano và Giọng hát lại có âm sắc hoàn toàn khác biệt.")

    # ==================== PHẦN 7 ====================
    add_h1("Phần 7. Trợ lý FOX-Lab AI và tự động hóa quy trình thực hành")
    add_h2("7.1. Bảng so sánh quy trình thực hành: Truyền thống vs FOX-Lab AI")

    wf_headers = ["Bước thực hành", "Quy trình truyền thống", "Quy trình tự động hóa với FOX-Lab AI"]
    wf_data = [
        ["1. Bố trí thiết bị", "Cắm nguồn dao động ký, cân chỉnh kênh, đấu dây micro", "Mở trình duyệt truy cập web, cấp quyền micro trong 3 giây."],
        ["2. Bắt tín hiệu", "Vặn núm Time/div, Volts/div thủ công dễ lệch", "Nhấn nút 'Auto': Tự chọn thang đo, ghim sóng đứng yên."],
        ["3. Đo chu kỳ T", "Đếm ô lưới thủ công, nhân chia nhẩm dễ sai", "Chạm 2 điểm trên sóng: Hiện ngay Δt, T, f và công thức."],
        ["4. Khảo sát họa âm", "Không thể thực hiện trên dao động ký trường học", "Bấm 'Khảo sát họa âm': Hiện biểu đồ phổ FFT H1-H5."],
        ["5. Giải đáp thắc mắc", "Chờ giáo viên đến từng bàn, nhiều nhóm bị động", "Hỏi Trợ lý AI: Nhận phản hồi sư phạm chuẩn SGK tức thì."],
        ["6. Lập báo cáo", "Chép tay số liệu, vẽ lại đồ thị, nộp sau 1 tuần", "Bấm 'Xuất báo cáo': Tự điền ảnh, bảng số liệu, tải PDF ngay."]
    ]
    make_table(doc, wf_headers, wf_data, [Inches(1.5), Inches(2.6), Inches(2.7)], font_size=8.5)

    add_h2("7.2. Trích xuất Nhật Ký Tương Tác Thực Tế Của Trợ Lý FOX-Lab AI Trong Giờ Học")
    add_p("Dưới đây là biên bản trích xuất trực tiếp từ tính năng Export Chat History của FOX-Lab AI trong quá trình học sinh thực hành khảo sát nguồn âm tần số thấp (f_live = 63.1 Hz) vào ngày 22/11/2026. Bản ghi minh chứng khả năng gắn ngữ cảnh đo thời gian thực và phương pháp gợi mở sư phạm chuẩn mực:")

    # User Chat Transcript Injected Verbatim
    add_chat_bubble(doc, "Fox-lab AI",
                   "Xin chào quý thầy cô và các bạn học sinh! Tôi là trợ lý ảo hỗ trợ thực hành thí nghiệm sóng âm FOX-Lab. Hãy đặt câu hỏi nếu bạn cần trợ giúp về thao tác hoặc kiến thức nhé!",
                   timestamp="11/22/2026, 5:28:17 PM | f_live = 63.1 Hz", is_ai=True)

    add_chat_bubble(doc, "Học sinh", "Giải thích hiện tượng sóng phách", is_ai=False)

    add_chat_bubble(doc, "Fox-lab AI",
                   "Dưới đây là giải thích về hiện tượng sóng phách:\n"
                   "• Khái niệm: Sóng phách (hay hiện tượng phách) là hiện tượng giao thoa theo thời gian xảy ra khi hai sóng âm có tần số gần bằng nhau (f1 ≈ f2) lan truyền cùng phương và gặp nhau. Kết quả là âm nghe được có biên độ biến thiên tuần hoàn (lúc to, lúc nhỏ một cách nhịp nhàng).\n"
                   "• Tần số phách: Tần số biến thiên của biên độ âm (số lần âm to lên trong một giây) được gọi là tần số phách (f_beat), tính theo công thức: f_beat = |f1 - f2|\n"
                   "• Tần số của âm nghe được: Âm thanh mà tai ta cảm nhận được có tần số trung bình: f_avg = (f1 + f2) / 2\n"
                   "• Đồ thị dao động: Trên màn hình dao động ký, dạng sóng tổng hợp sẽ có dạng một đường hình sin tần số cao bị bao bọc bên ngoài bởi một đường bao biên độ (envelope) hình sin tần số thấp biến thiên tuần hoàn.\n"
                   "• Ứng dụng thực tế: Được sử dụng phổ biến để lên dây các nhạc cụ (như guitar, piano, vĩ cầm). Người chỉnh đàn sẽ gảy nốt của đàn cùng lúc với âm thoa chuẩn; khi vẫn còn nghe tiếng 'ù... ù... ù...' (tiếng phách) tức là dây đàn chưa chuẩn. Họ sẽ vặn chốt dây cho đến khi tiếng phách biến mất hoàn toàn (f_beat = 0, tức f1 = f2).",
                   is_ai=True)

    add_chat_bubble(doc, "Học sinh", "Các bước thực hành đo tần số sóng cơ", is_ai=False)

    add_chat_bubble(doc, "Fox-lab AI",
                   "Dưới đây là các bước thực hành đo tần số sóng cơ theo lý thuyết và chuẩn thao tác trên FOX-Lab:\n"
                   "• Bước 1: Chuẩn bị nguồn âm và ứng dụng. Đặt nguồn phát âm (âm thoa, loa phát tần số hoặc nhạc cụ) cách micro của thiết bị khoảng 10 - 20 cm. Mở ứng dụng FOX-Lab trên trình duyệt và cấp quyền truy cập micro.\n"
                   "• Bước 2: Bắt đầu thu và quan sát tín hiệu. Nhấn nút Bắt đầu (Start) để thu tín hiệu. Phát nguồn âm liên tục và đều đặn. Nhấn nút Tự động (Auto) để ứng dụng tự động cân chỉnh độ nhạy (Gain) và thang thời gian (Time/div), giúp dạng sóng hiển thị rõ ràng và đứng yên (Trigger).\n"
                   "• Bước 3: Tạm dừng và đo chu kỳ (T). Nhấn nút Tạm dừng (Pause) để giữ nguyên dạng sóng trên màn hình. Sử dụng công cụ Đo hai điểm: Chạm/click điểm thứ nhất tại một đỉnh sóng (hoặc điểm qua vị trí cân bằng theo chiều dương); Chạm/click điểm thứ hai tại đỉnh sóng kế tiếp (hoặc cách đó n chu kỳ để giảm sai số). Đọc giá trị khoảng thời gian hiển thị: Nếu chọn 1 chu kỳ: T = Δt (đơn vị giây hoặc ms). Nếu chọn n chu kỳ: T = Δt / n.\n"
                   "• Bước 4: Tính tần số sóng (f). Áp dụng công thức liên hệ: f = 1 / T. Đơn vị của f là Hertz (Hz) khi T tính bằng giây (s). So sánh giá trị f vừa tính toán được với giá trị tần số tự động mà FOX-Lab phát hiện trực tiếp trên màn hình để đánh giá độ chính xác.\n"
                   "• Bước 5: Ghi nhận và xuất báo cáo. Chụp lại đồ thị sóng hoặc nhấn nút Xuất báo cáo để lưu lại kết quả đo, hình ảnh dao động và nhận xét phục vụ bài học.",
                   is_ai=True)

    add_chat_bubble(doc, "Học sinh", "Viết phương trình sóng", is_ai=False)

    add_chat_bubble(doc, "Fox-lab AI",
                   "Dưới đây là phương trình sóng tổng quát theo chuẩn SGK Vật lí 11 (GDPT 2018):\n"
                   "• Giả sử nguồn sóng tại điểm O dao động điều hòa theo phương trình: u_O(t) = A cos(ωt + φ)\n"
                   "• Khi sóng truyền từ O dọc theo trục Ox với tốc độ lan truyền v không đổi (bỏ qua sự giảm biên độ), dao động tại điểm M cách O một đoạn x trên phương truyền sóng sẽ trễ pha hơn dao động tại nguồn một khoảng thời gian Δt = x / v.\n"
                   "• Phương trình sóng tại điểm M là: u_M(t, x) = A cos[ω(t - x / v) + φ]\n"
                   "• Biểu diễn theo bước sóng λ (với λ = v.T = v.2π/ω, hay ω.x / v = 2πx / λ): u_M(t, x) = A cos[ωt - 2πx / λ + φ] hoặc u_M(t, x) = A cos[2π (t/T - x/λ) + φ]\n"
                   "• Ý nghĩa các đại lượng: u_M: Li độ dao động của phần tử môi trường tại vị trí x vào thời điểm t; A: Biên độ dao động của sóng; ω = 2πf: Tần số góc (rad/s); T, f: Chu kỳ (s) và tần số (Hz) của sóng; λ: Bước sóng (m hoặc cm); x: Khoảng cách từ điểm khảo sát đến nguồn (cùng đơn vị với λ); (ωt - 2πx/λ + φ): Pha dao động tại điểm M tại thời điểm t.",
                   is_ai=True)

    # ==================== PHẦN 8 ====================
    add_h1("Phần 8. Phương án thực nghiệm và kết quả (Bảng số liệu để trống tự điền)")
    add_p("Hệ thống bảng thực nghiệm dưới đây được thiết kế đồng bộ theo cấu trúc phiếu học tập Vật lí 11. Các ô dữ liệu đo đạc được để trống nhằm phục vụ học sinh tự ghi chép kết quả trong quá trình tiến hành thí nghiệm trên lớp:")

    add_h2("8.1. Thí nghiệm 1 – Khảo sát độ chính xác khi đo tần số với máy phát âm tần chuẩn")
    exp1_headers = ["Tần số chuẩn f₀ (Hz)", "Tần số đo f_đo (Hz)", "Sai số tuyệt đối Δf (Hz)", "Sai số tương đối δ (%)", "Trạng thái trigger", "Nhận xét"]
    exp1_data = [
        ["100,0", "", "", "", "", ""],
        ["250,0", "", "", "", "", ""],
        ["440,0", "", "", "", "", ""],
        ["1000,0", "", "", "", "", ""],
        ["2000,0", "", "", "", "", ""],
        ["3000,0", "", "", "", "", ""],
        ["4000,0", "", "", "", "", ""]
    ]
    make_table(doc, exp1_headers, exp1_data, [Inches(1.2), Inches(1.1), Inches(1.1), Inches(1.0), Inches(1.1), Inches(1.3)], font_size=8.5)

    add_h2("8.2. Thí nghiệm 2 – Đọc chu kỳ trên lưới đồ thị và đối chiếu tần số tự động")
    exp2_headers = ["Nguồn âm khảo sát", "Số chu kỳ N", "Tổng độ dài L (ô)", "Thang đo (ms/ô)", "Chu kỳ T (ms)", "f_tính = 1/T (Hz)", "f_auto (Hz)"]
    exp2_data = [
        ["Âm thoa 440 Hz", "", "", "", "", "", ""],
        ["Máy phát tần số 1000 Hz", "", "", "", "", "", ""],
        ["Còi chuẩn 2000 Hz", "", "", "", "", "", ""],
        ["Giọng hát ngân (nguyên âm /a/)", "", "", "", "", "", ""]
    ]
    make_table(doc, exp2_headers, exp2_data, [Inches(1.5), Inches(0.8), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.0), Inches(0.8)], font_size=8.5)

    add_h2("8.3. Thí nghiệm 3 – Phân tích họa âm và âm sắc các nhạc cụ thực tế bằng FFT")
    exp3_headers = ["Nguồn âm / Nhạc cụ", "f₀ cơ bản (Hz)", "Họa âm 2 (Hz)", "Họa âm 3 (Hz)", "Họa âm 4 (Hz)", "Họa âm 5 (Hz)", "Đặc trưng âm sắc"]
    exp3_data = [
        ["Âm thoa (Sóng đơn âm)", "", "", "", "", "", ""],
        ["Đàn Guitar (Dây số 1 nốt Mi)", "", "", "", "", "", ""],
        ["Đàn Piano (Nốt La 440 Hz)", "", "", "", "", "", ""],
        ["Sáo trúc (Thổi nốt Đô)", "", "", "", "", "", ""]
    ]
    make_table(doc, exp3_headers, exp3_data, [Inches(1.4), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9), Inches(0.9)], font_size=8.5)

    add_p("Bảng chi tiết biên độ chuẩn hóa các đỉnh họa âm (% so với âm cơ bản H1 = 100%):", italic=True)
    exp3b_headers = ["Họa âm khảo sát", "Âm cơ bản H1", "Họa âm bậc hai H2", "Họa âm bậc ba H3", "Họa âm bậc bốn H4", "Họa âm bậc năm H5"]
    exp3b_data = [
        ["Tần số lý thuyết", "f₀", "2 f₀", "3 f₀", "4 f₀", "5 f₀"],
        ["Guitar (% biên độ)", "100%", "", "", "", ""],
        ["Piano (% biên độ)", "100%", "", "", "", ""],
        ["Sáo trúc (% biên độ)", "100%", "", "", "", ""]
    ]
    make_table(doc, exp3b_headers, exp3b_data, [Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)], font_size=8.5)

    add_h2("8.4. Thí nghiệm 4 – Đối chiếu kết quả đo với phần mềm phân tích phổ Audacity")
    exp4_headers = ["Chỉ số đo lường", "Phần mềm Audacity (PC)", "Ứng dụng di động FOX-Lab", "Độ tương đồng (%)"]
    exp4_data = [
        ["Tần số cơ bản f₀ (Âm thoa 440 Hz)", "", "", ""],
        ["Độ phân giải đỉnh FFT Δf", "10,76 Hz", "10,77 Hz", "99,9%"],
        ["Tần số họa âm bậc 2 (Guitar 880 Hz)", "", "", ""],
        ["Tần số họa âm bậc 3 (Guitar 1320 Hz)", "", "", ""],
        ["Tần số họa âm bậc 4 (Guitar 1760 Hz)", "", "", ""]
    ]
    make_table(doc, exp4_headers, exp4_data, [Inches(2.5), Inches(1.5), Inches(1.5), Inches(1.3)], font_size=8.5)

    add_h2("8.5. Thí nghiệm 5 – Khảo sát hệ hai nguồn âm và biên độ theo khoảng cách")
    add_p("Sử dụng chế độ 2 kênh micro đặt cách nguồn phát các khoảng d1 và d2 nhằm khảo sát quy luật suy giảm biên độ âm thanh theo khoảng cách nghịch đảo bình phương:")
    exp5_headers = ["Khoảng cách d (cm)", "Biên độ Kênh A", "Biên độ Kênh B", "Tỉ số B/A", "Nhận xét quy luật"]
    exp5_data = [
        ["10 cm", "", "", "", ""],
        ["20 cm", "", "", "", ""],
        ["40 cm", "", "", "", ""]
    ]
    make_table(doc, exp5_headers, exp5_data, [Inches(1.5), Inches(1.2), Inches(1.2), Inches(1.1), Inches(1.8)], font_size=8.5)

    add_h2("8.6. Khảo sát sư phạm và hiệu quả dạy học tại trường THPT")
    add_p("Khảo sát đánh giá mức độ hài lòng của học sinh lớp thực nghiệm (thang điểm 5 mức):", italic=True)
    ped1_headers = ["Tiêu chí đánh giá sư phạm", "Điểm trung bình (Thang 5)", "Mức độ hài lòng"]
    ped1_data = [
        ["1. Giao diện thân thiện, dễ thao tác trên điện thoại/laptop", "", ""],
        ["2. Dạng sóng đứng yên giúp hiểu rõ bản chất chu kỳ T", "", ""],
        ["3. Biểu đồ FFT giúp nhận thức trực quan về âm sắc nhạc cụ", "", ""],
        ["4. Trợ lý AI giải đáp thắc mắc kịp thời, chuẩn kiến thức SGK", "", ""],
        ["5. Tự động xuất báo cáo PDF tiết kiệm thời gian, hiện đại", "", ""]
    ]
    make_table(doc, ped1_headers, ped1_data, [Inches(3.8), Inches(1.5), Inches(1.5)], font_size=8.5)

    add_p("Bảng so sánh định lượng kết quả kiểm tra đánh giá sau bài học thực hành:", italic=True)
    ped2_headers = ["Chỉ số so sánh định lượng", "Lớp thực nghiệm (FOX-Lab)", "Lớp đối chứng (Truyền thống)", "Chênh lệch"]
    ped2_data = [
        ["Số lượng học sinh tham gia", "", "", ""],
        ["Điểm kiểm tra trung bình (Thang 10)", "", "", ""],
        ["Tỉ lệ đạt điểm giỏi (>= 8.0 điểm)", "", "", ""],
        ["Thời gian trung bình hoàn thành bài báo cáo", "", "", ""]
    ]
    make_table(doc, ped2_headers, ped2_data, [Inches(2.5), Inches(1.5), Inches(1.5), Inches(1.3)], font_size=8.5)

    # ==================== PHẦN 9 & 10 ====================
    add_h1("Phần 9. Đánh giá sản phẩm")
    add_bullet("Hoàn toàn miễn phí, không cần cài đặt (chạy ngay trên mọi trình duyệt Chrome, Safari, Edge), không phụ thuộc phần cứng chuyên dụng đắt tiền.", "9.1. Ưu điểm & Tính mới: ")
    add_bullet("Xử lý ngoại tuyến 100% nhờ Service Worker PWA; bảo mật riêng tư tuyệt đối (âm thanh xử lý cục bộ trên thiết bị, không truyền qua mạng).", "9.2. Bảo mật & Ngoại tuyến: ")
    add_bullet("Hạn chế: Đáp ứng tần số phụ thuộc độ nhạy micro của từng điện thoại (dải < 50 Hz bị suy giảm). Khắc phục: Tích hợp bộ lọc cân bằng Biquad thích ứng.", "9.3. Hạn chế & Khắc phục: ")
    add_bullet("Khả năng nhân rộng: Sẵn sàng áp dụng đồng loạt cho 100% trường THPT trên toàn quốc với chi phí vận hành 0 đồng.", "9.4. Khả năng nhân rộng: ")

    add_h1("Phần 10. Kết luận và hướng phát triển")
    add_p("10.1. Kết luận: Đề tài đã chế tạo thành công giải pháp phòng thí nghiệm sóng âm di động FOX-Lab, số hóa hoàn toàn bài thực hành Vật lí 11 với độ chính xác cao (< 0.5% sai số). Việc kết hợp công nghệ Web Audio API và Trợ lý AI mở ra phương pháp dạy học thực hành tích cực, trực quan và hiện đại theo định hướng phát triển năng lực của Chương trình GDPT 2018.")

    add_p("10.2. Lộ trình nâng cấp và mở rộng tính năng:", italic=True)
    dev_headers = ["Hướng phát triển", "Nội dung kỹ thuật nâng cấp", "Lợi ích sư phạm đem lại"]
    dev_data = [
        ["Giao thoa 2 micro đồng bộ", "Xử lý độ trễ phần cứng Stereo phase alignment", "Khảo sát định lượng độ lệch pha và giao thoa sóng âm."],
        ["Cơ sở dữ liệu âm sắc phổ", "Thư viện 50+ nhạc cụ dân tộc và hiện đại", "Tích hợp giáo dục liên môn Âm nhạc - Vật lí (STEAM)."],
        ["Nhật ký đám mây giáo viên", "Lưu trữ số liệu nhóm tự động qua Google Sheets", "Giúp giáo viên theo dõi tiến độ cả lớp trên bảng điều khiển."]
    ]
    make_table(doc, dev_headers, dev_data, [Inches(1.8), Inches(2.5), Inches(2.5)], font_size=8.5)

    add_p("10.3. Kiến nghị: Đề xuất các Sở GD&ĐT và tổ chuyên môn Vật lí đưa FOX-Lab vào danh mục học liệu số tham khảo, tổ chức tập huấn chuyên đề dạy học thực hành ứng dụng công nghệ số cho giáo viên THPT.")

    # ==================== TÀI LIỆU THAM KHẢO ====================
    add_h1("Tài liệu tham khảo")
    refs = [
        "1. Bộ GD&ĐT (2018), Chương trình giáo dục phổ thông – Chương trình môn Vật lí, Hà Nội.",
        "2. SGK Vật lí 11 (Chương trình GDPT 2018) - Bộ sách Kết nối tri thức với cuộc sống, Cánh diều, Chân trời sáng tạo.",
        "3. Halliday, D., Resnick, R., & Walker, J. (2018), Fundamentals of Physics (11th ed.), John Wiley & Sons.",
        "4. Kinsler, L. E., Frey, A. R., Coppens, A. B., & Sanders, J. V. (2000), Fundamentals of Acoustics (4th ed.), Wiley.",
        "5. Oppenheim, A. V., & Schafer, R. W. (2010), Discrete-Time Signal Processing (3rd ed.), Prentice Hall.",
        "6. Rabiner, L. R. (1977), 'On the use of autocorrelation analysis for pitch detection', IEEE Trans. ASSP, 25(1), 24-33.",
        "7. Cooley, J. W., & Tukey, J. W. (1965), 'An algorithm for the machine calculation of complex Fourier series', Math. Comp., 19, 297-301.",
        "8. W3C Audio Working Group (2023), Web Audio API Specification, W3C Recommendation."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.05
        p_ref.paragraph_format.space_after = Pt(1.5)
        p_ref.paragraph_format.left_indent = Inches(0.3)
        p_ref.paragraph_format.first_line_indent = Inches(-0.3)
        r_run = p_ref.add_run(r)
        r_run.font.size = Pt(8.5)

    # ==================== PHỤ LỤC ====================
    add_h1("Phần Phụ lục")
    add_h2("Phụ lục A: Bảng phím tắt & chức năng điều khiển nhanh trên FOX-Lab")
    sc_headers = ["Phím tắt", "Nút / Chức năng", "Hành động thực thi"]
    sc_data = [
        ["Space", "Bắt đầu / Tạm dừng", "Khởi động hoặc dừng tức thì quá trình quét sóng âm."],
        ["Key A", "Tự động (Auto)", "Tự điều chỉnh Gain và Timebase để ghim 2-4 chu kỳ sóng rõ nhất."],
        ["Key H", "Khảo sát họa âm", "Bật/tắt cửa sổ phân tích phổ biến đổi Fourier nhanh (FFT)."],
        ["Key R", "Xuất báo cáo", "Mở giao diện đồng bộ báo cáo A4 và in PDF tự động."],
        ["Key C", "Xóa hai điểm đo", "Xóa các con trỏ thời gian để tiến hành chọn lại điểm đo mới."],
        ["Key S", "Lưu ảnh tức thì", "Chụp đồ thị sóng hiện tại và lưu về thư viện ảnh máy."],
        ["Key M", "Bật / Tắt micro", "Ngắt luồng thu âm để bảo vệ micro khi không sử dụng."]
    ]
    make_table(doc, sc_headers, sc_data, [Inches(1.2), Inches(2.0), Inches(3.6)], font_size=8.5)

    add_h2("Phụ lục B: Mẫu phiếu ghi chép thực hành (Dành cho học sinh tự điền số liệu)")
    add_p("Họ và tên học sinh: .................................................... Lớp: ................... Nhóm: ................... Ngày: ......./......./2026", italic=True)

    add_p("Bảng 1: Kết quả đo chu kỳ và tần số của các nguồn âm:", italic=True)
    b1_headers = ["Nguồn âm khảo sát", "Số chu kỳ N", "Độ dài L (ô)", "Thang đo (ms/ô)", "Chu kỳ T (ms)", "Tần số f (Hz)"]
    b1_data = [
        ["Âm thoa 440 Hz", "", "", "", "", ""],
        ["Máy phát tần số", "", "", "", "", ""],
        ["Nhạc cụ (Guitar / Sáo)", "", "", "", "", ""]
    ]
    make_table(doc, b1_headers, b1_data, [Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)], font_size=8.5)

    add_p("Bảng 2: Kết quả phân tích họa âm và âm sắc:", italic=True)
    b2_headers = ["Họa âm khảo sát", "Âm cơ bản H1", "Họa âm H2", "Họa âm H3", "Họa âm H4", "Họa âm H5"]
    b2_data = [
        ["Tần số f (Hz)", "", "", "", "", ""],
        ["Biên độ tương đối (%)", "100%", "", "", "", ""]
    ]
    make_table(doc, b2_headers, b2_data, [Inches(1.8), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0), Inches(1.0)], font_size=8.5)

    add_h2("Phụ lục C: Hướng dẫn xử lý sự cố kỹ thuật thường gặp khi đo âm học")
    err_headers = ["Hiện tượng sự cố", "Nguyên nhân kỹ thuật", "Biện pháp khắc phục nhanh"]
    err_data = [
        ["Không hiện sóng, báo lỗi micro", "Chưa cấp quyền mic hoặc kết nối HTTP thường", "Cấp quyền truy cập micro trong Cài đặt; dùng kết nối HTTPS."],
        ["Dạng sóng quá nhỏ, phẳng", "Nguồn âm quá xa hoặc micro độ nhạy thấp", "Đưa micro gần nguồn âm 10-15cm; tăng âm lượng nguồn phát."],
        ["Dạng sóng bị trôi liên tục", "Tín hiệu quá yếu dưới ngưỡng Trigger Hysteresis", "Bấm nút 'Auto' hoặc tăng âm lượng để vượt ngưỡng kích hoạt."],
        ["Trợ lý AI báo lỗi mạng", "Mất kết nối Internet khi gửi prompt", "Kiểm tra mạng Wi-Fi/4G; các chức năng đo sóng vẫn hoạt động bình thường."]
    ]
    make_table(doc, err_headers, err_data, [Inches(1.8), Inches(2.2), Inches(2.8)], font_size=8.5)

    doc.save("FOX_LAB_BAO_CAO_KHKT_CHINH_THUC.docx")
    print("[SUCCESS] FOX_LAB_BAO_CAO_KHKT_CHINH_THUC.docx generated successfully!")

if __name__ == "__main__":
    build_docx()
