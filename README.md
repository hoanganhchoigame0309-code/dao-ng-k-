# 🦊 FOX_LAB - Phòng Thí Nghiệm Vật Lý Ảo Về Sóng Cơ Học & Sóng Âm

> Dự án nghiên cứu Khoa học Kỹ thuật (KHKT) ứng dụng công nghệ Web Audio API, Canvas 2D và Trí tuệ nhân tạo (AI) trong dạy học và thực hành Vật lý THPT (Chương trình GDPT mới).

---

## 📖 Giới thiệu tổng quan

**FOX_LAB** là một ứng dụng web mô phỏng và đo lường âm học thời gian thực, biến máy tính bảng, điện thoại thông minh hoặc laptop có micro thành một hệ thống thí nghiệm Vật lý chuyên dụng:
- **Khảo sát dao động và sóng**: Đo tần số ($f$), chu kỳ ($T$), bước sóng ($\lambda$), biên độ ($A$), vận tốc truyền âm ($v$).
- **Dao động ký số 2 kênh (Digital Oscilloscope)**: Quan sát trực quan dạng sóng âm thanh từ môi trường thực tế.
- **Phân tích phổ Fourier (FFT)**: Xác định tần số cơ bản và các họa âm bậc cao của nhạc cụ/giọng nói.
- **Thí nghiệm giao thoa & 2 nguồn âm**: Khảo sát hiện tượng giao thoa sóng, xác định độ lệch pha $\Delta \varphi$, vẽ phương trình sóng tổng hợp.
- **Trợ lý ảo AI thông minh (Fox AI)**: Giải đáp kiến thức chuẩn SGK Vật lý 11 hoặc phân tích trực tiếp đồ thị và số liệu đang đo.
- **Xuất phiếu báo cáo thí nghiệm**: Tự động tổng hợp số liệu, vẽ đồ thị và xuất file PDF/Ảnh/CSV chuẩn A4.

---

## 🗂 Cấu trúc thư mục dự án

```text
Fox_labKHKT/
├── index.html               # Giao diện chính của phòng thí nghiệm ảo
├── report.html              # Mẫu phiếu báo cáo thực hành thí nghiệm A4
├── style.css                # CSS giao diện Dark/Light theme, bố cục responsive
├── script.js                # Toàn bộ logic Web Audio, Canvas FFT, dao động ký, AI Chatbot
├── manifest.json            # Cấu hình PWA (Progressive Web App)
├── sw.js                    # Service Worker hỗ trợ lưu cache và chạy offline
├── version.json             # Quản lý phiên bản ứng dụng và tự động cập nhật
├── icon-192.png             # Icon ứng dụng kích thước 192x192
├── icon-512.png             # Icon ứng dụng kích thước 512x512
├── backend/                 # Mã nguồn backend cho trợ lý AI
│   ├── gas-foxlab-ai.js     # Script Google Apps Script chuẩn hóa bảo mật
│   └── README.md            # Hướng dẫn thiết lập Google Apps Script & Gemini API
├── .gitignore               # Tệp cấu hình loại trừ các file rác khi đẩy lên Git
└── README.md                # Tài liệu hướng dẫn dự án
```

---

## ⚡ Các tính năng nổi bật

### 1. Dao động ký số & Đo lường âm học
- Thu tín hiệu trực tiếp từ Micro qua **Web Audio API**.
- Tự động phát hiện điểm 0 (Zero-crossing) để cố định dạng sóng (Trigger/Hold) giúp học sinh dễ đọc số liệu.
- Chế độ đo tự dừng (Auto-hold) khi tín hiệu ổn định hoặc đo liên tục (Continuous).
- Hiệu chuẩn cường độ âm ($dB$) với mức áp suất âm chuẩn ($p_0 = 2 \cdot 10^{-5}\text{ Pa}$).

### 2. Phân tích phổ tần số (FFT Analyzer)
- Biến đổi Fourier nhanh (Fast Fourier Transform) với kích thước mẫu $2048$ đến $4096$.
- Chức năng **Quét họa âm** tự động gắn nhãn tần số cơ bản ($f_0$) và các họa âm $2f_0, 3f_0, \dots$.
- Bảng thống kê chi tiết biên độ tương đối của từng họa âm.

### 3. Thí nghiệm 2 nguồn âm & Động học sóng
- Hỗ trợ ghép 2 kênh micro độc lập (Kênh A và Kênh B).
- Chế độ **Ghép sóng (Overlay)** và tính toán độ lệch pha $\Delta \varphi$.
- Tự động suy ra phương trình sóng $u_1(t), u_2(t)$ và phương trình sóng tổng hợp $u(t) = 2A\cos\left(\frac{\Delta \varphi}{2}\right)\cos\left(\omega t + \frac{\varphi_1+\varphi_2}{2}\right)$.
- Đồ thị động học dao động điều hòa: Li độ $x(t)$, Vận tốc $v(t)$, Gia tốc $a(t)$.

### 4. Trợ lý ảo AI Fox-Lab tích hợp
- Hỗ trợ 2 chế độ tương tác:
  - 👨‍🏫 **Giáo viên**: Phản hồi sư phạm chuẩn mực, phân tích an toàn thí nghiệm, bám sát SGK Vật lý mới.
  - 👨‍🎓 **Học sinh (Gia sư)**: Giải thích ngắn gọn, súc tích, hướng dẫn tư duy từng bước.
- **Multimodal AI**: Chụp ảnh bài tập gửi lên hoặc tự động chụp đồ thị dao động ký hiện tại kèm thông số tần số đo để AI phân tích.
- Tự động hiển thị công thức Toán - Lý đẹp mắt qua **MathJax v3**.

### 5. Hỗ trợ PWA & Chạy Offline
- Cài đặt trực tiếp lên màn hình chính máy tính, điện thoại mà không cần thông qua App Store.
- Lưu cache tự động qua `sw.js`, kiểm tra cập nhật phiên bản mới qua `version.json`.

---

## 🚀 Hướng dẫn cài đặt & Chạy ứng dụng

### Chạy trực tiếp trên máy cục bộ (Local)

Do ứng dụng sử dụng **Web Audio API** (truy cập micro) và **Service Worker**, trình duyệt yêu cầu chạy trên giao thức `https://` hoặc `http://localhost`.

1. **Cách 1: Sử dụng VS Code Live Server (Khuyên dùng)**
   - Mở thư mục dự án trong Visual Studio Code.
   - Cài đặt extension **Live Server**.
   - Chuột phải vào file `index.html` -> Chọn **Open with Live Server**.

2. **Cách 2: Sử dụng Python HTTP Server**
   ```bash
   # Di chuyển vào thư mục dự án
   cd Fox_labKHKT
   
   # Chạy server cục bộ
   python -m http.server 8000
   ```
   Mở trình duyệt và truy cập: `http://localhost:8000`

3. **Cách 3: Sử dụng Node.js serve**
   ```bash
   npx serve .
   ```

---

## 🌐 Hướng dẫn đẩy lên GitHub & Triển khai GitHub Pages

### 1. Khởi tạo Git & Commit đầu tiên
```bash
git add .
git commit -m "feat: Initial commit for Fox_labKHKT v6.4.0"
```

### 2. Đẩy lên kho lưu trữ GitHub
```bash
# Đổi tên nhánh chính thành main
git branch -M main

# Thêm remote repository từ GitHub của bạn
git remote add origin https://github.com/TÊN_NGƯỜI_DÙNG/TÊN_REPO.git

# Đẩy code lên GitHub
git push -u origin main
```

### 3. Bật GitHub Pages miễn phí
1. Truy cập vào trang GitHub Repository của bạn.
2. Vào **Settings** -> Mục **Pages** ở thanh bên trái.
3. Tại phần **Build and deployment** -> **Branch**:
   - Chọn nhánh: `main`
   - Chọn thư mục: `/ (root)`
   - Bấm **Save**.
4. Chờ 1 - 2 phút, GitHub sẽ cung cấp đường link web công khai có hỗ trợ HTTPS (Ví dụ: `https://ten-nguoidung.github.io/ten-repo/`).

---

## ⚠️ Lưu ý quan trọng về Bảo mật API Key

- Tuyệt đối không lưu trực tiếp Gemini API Key vào mã nguồn frontend hoặc đẩy file chứa API key lên GitHub.
- **Bảo mật Backend**: Hãy cấu hình Google Apps Script theo tài liệu tại [backend/README.md](backend/README.md) bằng **Script Properties** (`GEMINI_API_KEY`).

---

## 📄 Bản quyền & Tác giả

- **Dự án**: FOX_LAB - Phòng thí nghiệm Vật lý KHKT
- **Phiên bản**: `6.4.0-fft-dothi`
- **Giấy phép**: MIT License
