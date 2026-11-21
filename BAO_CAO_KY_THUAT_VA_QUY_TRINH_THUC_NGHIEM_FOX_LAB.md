# BÁO CÁO KỸ THUẬT VÀ QUY TRÌNH THỰC NGHIỆM
## Hệ Thống Phòng Thí Nghiệm Vật Lý Ảo — FOX_LAB (Phiên bản v6.4.0)

---

**Mô tả tổng quan:**  
Tài liệu kỹ thuật và quy trình thực nghiệm toàn diện của hệ thống phòng thí nghiệm Vật lý số hóa chuyên sâu về sóng cơ học và âm học (**FOX_LAB**), tích hợp công nghệ xử lý tín hiệu số thời gian thực (**Web Audio DSP Engine**), Trợ lý ảo trí tuệ nhân tạo (**Google Gemini AI**) và Hệ thống số hóa phiếu báo cáo thực hành chuẩn **A4** (đồng bộ đa luồng, hỗ trợ ngoại tuyến **PWA Offline**). Tài liệu phục vụ công tác nghiên cứu khoa học kỹ thuật (KHKT), giảng dạy STEM và thực hành thí nghiệm theo Chương trình Giáo dục Phổ thông 2018 (Vật lý 11).

---

# PHẦN 1: TỔNG HỢP TẤT CẢ CÁC CHỨC NĂNG VÀ THUẬT TOÁN ĐI KÈM

---

### 1. Hệ thống Xử lý Tín hiệu Âm thanh Thời gian thực (Web Audio DSP Engine)

- **Mô tả chức năng:**  
  Thu nhận luồng tín hiệu âm thanh đa kênh từ phần cứng microphone (hỗ trợ chế độ 1 nguồn đơn kênh và 2 nguồn Stereo đa kênh), chuẩn hóa tốc độ lấy mẫu ($f_s \approx 44.100\text{ Hz} - 48.000\text{ Hz}$), loại bỏ tạp âm nền và bảo toàn dữ liệu liên tục phục vụ phân tích dạng sóng, phổ tần số và năng lượng âm.

- **Thuật toán 1 — AudioWorklet Đa luồng nền (Multi-threading `FoxAudioProcessor`):**  
  - *Nguyên lý:* Thay thế hoàn toàn cơ chế `ScriptProcessorNode` cũ (vốn chạy trên luồng giao diện chính UI Thread gây drop frame khi DOM render), hệ thống triển khai `AudioWorkletNode` chạy trên tiến trình thời gian thực độc lập (`AudioWorkletGlobalScope`).  
  - *Cơ chế:* Khối xử lý thu nhận từng khối dữ liệu $128$ mẫu âm thanh (`channelData`), đóng gói và truyền thông điệp bất đồng bộ qua `port.postMessage()` về luồng chính để nạp vào bộ đệm, giải phóng hoàn toàn UI Thread cho Canvas 60 FPS.

- **Thuật toán 2 — Bộ lọc số dải thông IIR bậc 2 (Cascaded Biquad Filter):**  
  - *Bộ lọc thông cao (High-pass Filter):* Cắt bỏ tần số hạ âm và tiếng ù cơ học:
    $$f_{c,\text{HP}} = 45\text{ Hz}, \quad Q = 0.707\text{ (Butterworth)}$$
  - *Bộ lọc thông thấp (Low-pass Filter):* Ngăn chặn hiện tượng chồng phổ (Aliasing) và triệt tiêu tạp âm tần số siêu cao:
    $$f_{c,\text{LP}} = 5000\text{ Hz}, \quad Q = 0.707$$
  - *Mã nguồn triển khai:* Cấu hình chuỗi nốt trong `script.js`:
    ```javascript
    cfg.filterHP = audioCtx.createBiquadFilter(); 
    cfg.filterHP.frequency.value = 45; 
    cfg.filterHP.type = 'highpass';

    cfg.filterLP = audioCtx.createBiquadFilter(); 
    cfg.filterLP.frequency.value = 5000; 
    cfg.filterLP.type = 'lowpass';
    ```

- **Thuật toán 3 — Bộ đệm xoay vòng tĩnh (Static Ring Buffer):**  
  - *Cấu trúc:* Mảng đệm tuyến tính `Float32Array` kích thước $10\text{ giây} \times f_s$ (khoảng $441.000 - 480.000$ phần tử).
  - *Nguyên tắc ghi:* Chỉ số ghi `writeIndex` tự động quay vòng theo phép chia lấy dư modulo:
    $$\text{idx} = (\text{writeIndex} + i) \pmod{L}$$
    Kỹ thuật này đảm bảo bộ nhớ không bị cấp phát lại (zero-garbage collection), ngăn ngừa trình thu gom rác (Garbage Collector) của JavaScript gây giật khung hình.

---

### 2. Chế độ Dao động ký 1 Kênh & 2 Kênh (Oscilloscope Mode)

- **Mô tả chức năng:**  
  Mô phỏng chức năng của dao động ký điện tử hiện đại trên nền Web Canvas. Hiển thị dạng sóng thời gian thực, tự động cố định đồ thị đứng yên chống trôi hình (Trigger/Hold), hỗ trợ phóng to/thu nhỏ trục thời gian ($t$) và trục biên độ ($u$).

- **Thuật toán 1 — Tự tương quan (Autocorrelation Function - ACF) & Nội suy Parabolic:**  
  - *Hàm tự tương quan:* Để tìm chu kỳ cơ bản $T_0$ của dạng sóng tuần hoàn không sin (như giọng nói, nhạc cụ), hệ thống tính hệ số tương quan theo độ trễ $\tau$:
    $$R(\tau) = \sum_{t=0}^{W - 1} x[t] \cdot x[t + \tau]$$
  - *Nội suy Parabolic:* Sau khi tìm được đỉnh rời rạc $\tau_{\text{peak}}$, thuật toán nội suy đỉnh thực tế bằng parabol đi qua 3 điểm liền kề $(\tau - 1, R_1), (\tau, R_2), (\tau + 1, R_3)$:
    $$\Delta \tau = \frac{R_1 - R_3}{2(R_1 - 2R_2 + R_3)}, \quad \tau^* = \tau_{\text{peak}} + \Delta \tau$$
    Tần số cơ bản được xác định cực kỳ chính xác:
    $$f_0 = \frac{f_s}{\tau^*}$$

- **Thuật toán 2 — Khóa pha qua điểm 0 với ngưỡng trễ (Zero-Crossing Trigger with Hysteresis):**  
  - *Nguyên lý:* Đồ thị dao động ký sẽ bị rung lắc trôi dạt liên tục nếu điểm bắt đầu vẽ thay đổi. Thuật toán tìm điểm tín hiệu chuyển từ âm sang dương:
    $$x[i - 1] \le 0 \quad \text{và} \quad x[i] > 0$$
  - *Ngưỡng trễ Hysteresis chống nhiễu:* Chỉ chấp nhận điểm kích hoạt khi độ dốc vượt ngưỡng:
    $$x[i] - x[i - 1] > 0.02 \cdot A_{\text{peak}}$$
    Nhờ đó, đồ thị sóng trên màn hình đứng yên tuyệt đối dù nguồn âm thay đổi nhẹ cường độ.

- **Thuật toán 3 — Căn chỉnh vạch đo thời gian & Co giãn biên độ chuẩn (Timebase & Voltage Division):**  
  - Tự động căn chỉnh màn hình hiển thị vừa vặn $5$ chu kỳ sóng:
    $$t_{\text{screen}} = 5 \cdot T_0 = \frac{5}{f_0}$$
  - Chia lưới màn hình thành $10$ ô thời gian ngang ($10\text{ DIV}$) và $8$ ô biên độ dọc ($8\text{ DIV}$). Giá trị định lượng hiển thị rõ ràng từng nấc $\text{ms/ô}$ và $\text{V/ô}$.

---

### 3. Module Phân tích 2 Điểm Đo & Đồ thị Động học Dao động ($u-t, v-t, a-t$)

- **Mô tả chức năng:**  
  Cho phép người học chọn trực tiếp 2 điểm bất kỳ trên đồ thị dao động ký để trích xuất số liệu chu kỳ $T$, tần số $f$, độ lệch pha $\Delta \varphi$; đồng thời tự động vẽ các đồ thị dẫn xuất của chuyển động dao động: li độ $u(t)$, vận tốc $v(t)$, gia tốc $a(t)$.

- **Thuật toán 1 — Đo vi phân thời gian và pha giữa 2 điểm con trỏ:**  
  - Khoảng thời gian giữa 2 con trỏ $t_1, t_2$:
    $$\Delta t = |t_2 - t_1| = \frac{|\text{index}_2 - \text{index}_1|}{f_s}$$
  - Chu kỳ và tần số ứng với số chu kỳ $N$ do người dùng chọn:
    $$T = \frac{\Delta t}{N}, \quad f = \frac{1}{T} = \frac{N}{\Delta t}$$
  - Độ lệch pha tương đối giữa 2 trạng thái dao động:
    $$\Delta \varphi = \left(\frac{\Delta t}{T}\right) \cdot 2\pi \pmod{2\pi}$$

- **Thuật toán 2 — Đạo hàm số sai phân trung tâm (Central Finite Difference):**  
  - *Vận tốc tức thời:*
    $$v(t) = \frac{du}{dt} \approx \frac{u(t + \Delta t) - u(t - \Delta t)}{2\Delta t}$$
  - *Gia tốc tức thời:*
    $$a(t) = \frac{dv}{dt} = \frac{d^2u}{dt^2} \approx \frac{u(t + \Delta t) - 2u(t) + u(t - \Delta t)}{\Delta t^2}$$
  - *Đặc điểm sư phạm:* Đồ thị trực quan hóa hoàn hảo quy luật pha trong SGK Vật lý: vận tốc $v(t)$ sớm pha $\pi/2$ so với li độ $u(t)$, gia tốc $a(t)$ ngược pha ($\pi$) so với li độ $u(t)$.

---

### 4. Chế độ Đo Mức Cường độ Âm (dB Meter Mode)

- **Mô tả chức năng:**  
  Đo và hiển thị mức cường độ âm theo thời gian thực dưới dạng thanh đo tốc độ cao và biểu đồ lịch sử 120 cột ($6\text{ giây}$). Đánh giá cảnh báo ô nhiễm tiếng ồn theo quy chuẩn an toàn thính giác.

- **Thuật toán 1 — Tính giá trị hiệu dụng RMS & Mức Cường độ Âm chuẩn ($dB$):**  
  - *Giá trị điện áp hiệu dụng (Root-Mean-Square):*
    $$U_{\text{RMS}} = \sqrt{\frac{1}{N}\sum_{i=1}^{N} x_i^2}$$
  - *Mức cường độ âm quy đổi:*
    $$L = 20 \cdot \lg\left(\frac{U_{\text{RMS}}}{p_0}\right)$$
    với áp suất âm thanh chuẩn ở ngưỡng nghe là $p_0 = 2 \cdot 10^{-5}\text{ Pa}$. Dải hiển thị chuẩn hóa từ $30.0\text{ dB}$ (phòng yên tĩnh) đến $120.0\text{ dB}$ (ngưỡng chói tai).

- **Thuật toán 2 — Hiệu chuẩn Micro phần cứng (Calibration Offset):**  
  - Bù trừ sai số độ nhạy giữa các dòng microphone khác nhau thông qua biến bù offset:
    $$L_{\text{calib}} = L_{\text{raw}} + \Delta L_{\text{offset}}$$
  - Cho phép người dùng lấy mẫu tại điểm mốc chuẩn ($r_0, L_0$) để tự động lưu hệ số hiệu chuẩn vào `localStorage`.

- **Thuật toán 3 — Lọc ngưỡng bảo vệ thính lực:**  
  - Hệ thống tự động phân loại cột đo theo màu sắc:
    - Xanh lá / Xanh dương: $L < 75\text{ dB}$ (Mức an toàn).
    - Vàng cam: $75\text{ dB} \le L \le 85\text{ dB}$ (Ngưỡng chú ý).
    - Đỏ cam đậm (`#ea580c`): $L > 85\text{ dB}$ (Vượt ngưỡng an toàn lao động / ô nhiễm tiếng ồn trường học).

---

### 5. Module Phân tích Họa âm FFT (Spectrum Analysis)

- **Mô tả chức năng:**  
  Biến đổi tín hiệu âm thanh từ miền thời gian sang miền tần số, bóc tách tần số cơ bản ($f_0$) và toàn bộ phổ họa âm ($2f_0, 3f_0, 4f_0, 5f_0\dots$) giúp học sinh hiểu bản chất vật lý của **Âm sắc**.

- **Thuật toán 1 — Biến đổi Fourier Nhanh Cooley-Tukey (Fast Fourier Transform - FFT):**  
  - Kích thước cửa sổ: $N = 4096\text{ mẫu}$ (độ phân giải tần số $\Delta f = f_s / 4096 \approx 10.7\text{ Hz}$).
  - Công thức biến đổi:
    $$X[k] = \sum_{n=0}^{N-1} x[n] \cdot e^{-j \frac{2\pi}{N} k n}, \quad k = 0, 1, \dots, N-1$$

- **Thuật toán 2 — Cửa sổ Hanning chống rò rỉ phổ (Hanning Window Function):**  
  - Để khắc phục hiện tượng nhảy bậc ở hai mép mẫu hữu hạn gây rò rỉ năng lượng sang các dải lân cận, tín hiệu được nhân với hàm cửa sổ trước khi đưa vào FFT:
    $$w[n] = 0.5 \cdot \left[1 - \cos\left(\frac{2\pi n}{N - 1}\right)\right]$$
    $$x_{\text{windowed}}[n] = x[n] \cdot w[n]$$

- **Thuật toán 3 — Tự động dò đỉnh họa âm & Quét hoạt họa (Harmonic Peak Detection & Sweep Animation):**  
  - Xác định tần số cơ bản $f_0 = \arg\max |X[k]|$.
  - Tự động dò tìm các đỉnh cực đại địa phương tại các bội số nguyên:
    $$f_k \approx k \cdot f_0 \quad (k = 2, 3, 4, 5)$$
  - Chức năng **Quét họa âm** tự động chạy hoạt họa tia quét tần số trên Canvas, gắn thẻ nhãn biên độ tương đối ($\%$) của từng họa âm so với âm cơ bản.

---

### 6. Module Phân tích & Xử lý 2 Nguồn Âm (Ghép sóng & Sóng phách)

- **Mô tả chức năng:**  
  Khảo sát hiện tượng giao thoa sóng, ghép sóng Kênh A và Kênh B, tổng hợp 2 dao động điều hòa cùng phương ($u = u_A + u_B$), đo độ lệch pha $\Delta \varphi$ và phát hiện hiện tượng sóng phách khi $f_A \ne f_B$.

- **Thuật toán 1 — Tương quan chéo đo độ lệch pha chính xác (Cross-Correlation Phase Analysis):**  
  - Độ tương quan chéo giữa hai chuỗi tín hiệu $u_A$ và $u_B$:
    $$R_{AB}[s] = \sum_{k} u_A[k] \cdot u_B[k + s]$$
  - Tìm độ dịch thời gian tối ưu:
    $$s^* = \arg\max R_{AB}[s]$$
  - Góc lệch pha $\Delta \varphi$ được chuẩn hóa dấu vật lý chính xác (khi Kênh B sớm pha hơn Kênh A thì $\Delta \varphi > 0$):
    $$\Delta \varphi = -\left(\frac{s^*}{N_{\text{cycle}}}\right) \cdot 2\pi, \quad \Delta \varphi \in [-\pi, +\pi]$$

- **Thuật toán 2 — Phát hiện Sóng phách tự động (Beat Wave Detection):**  
  - Nếu độ chênh lệch tần số giữa 2 kênh:
    $$|f_A - f_B| > 3.0\text{ Hz}$$
  - Hệ thống tự động kích hoạt cảnh báo `⚠️ Cảnh báo: Hai nguồn khác tần số (Tạo Sóng Phách)`, khóa chức năng tính phương trình lượng giác đơn và chuyển sang mô phỏng biên độ biến thiên tuần hoàn theo tần số phách $f_{\text{beat}} = |f_A - f_B|$.

- **Thuật toán 3 — Tổng hợp dao động & Xuất phương trình lượng giác:**  
  - Với hai dao động cùng tần số:
    $$u_A = A_A \cos(\omega t + \varphi_A), \quad u_B = A_B \cos(\omega t + \varphi_B)$$
  - Biên độ tổng hợp:
    $$A = \sqrt{A_A^2 + A_B^2 + 2 A_A A_B \cos(\Delta \varphi)}$$
  - Pha ban đầu tổng hợp:
    $$\tan \varphi = \frac{A_A \sin \varphi_A + A_B \sin \varphi_B}{A_A \cos \varphi_A + A_B \cos \varphi_B}$$
  - Toàn bộ phương trình được kết xuất ra bảng HUD với ký hiệu toán học chuẩn.

---

### 7. Module Ước tính Khoảng cách Nguồn Âm từ Mức Cường độ Âm

- **Mô tả chức năng:**  
  Vận dụng định luật truyền sóng âm trong không gian mở (nguồn điểm đẳng hướng, bỏ qua hấp thụ môi trường) để tính khoảng cách từ vị trí đặt micro tới nguồn âm.

- **Thuật toán 1 — Định luật nghịch đảo bình phương khoảng cách (Inverse Square Law):**  
  - Cường độ âm $I$ giảm tỉ lệ nghịch với bình phương khoảng cách $r$:
    $$I = \frac{P}{4\pi r^2} \implies \frac{I_1}{I_2} = \left(\frac{r_2}{r_1}\right)^2$$
  - Hiệu mức cường độ âm giữa hai vị trí:
    $$L_1 - L_2 = 10 \lg\left(\frac{I_1}{I_2}\right) = 20 \lg\left(\frac{r_2}{r_1}\right)$$

- **Thuật toán 2 — Ước tính khoảng cách 1 điểm (dựa trên mốc chuẩn $r_0, L_0$):**  
  - Từ mức đo thực tế $L_{\text{tb}}$, tính khoảng cách:
    $$r = r_0 \cdot 10^{\frac{L_0 - L_{\text{tb}}}{20}}$$
    (Mặc định mốc kỹ thuật chuẩn: $r_0 = 1.0\text{ m}$ tương ứng $L_0 = 90.0\text{ dB}$).

- **Thuật toán 3 — Phân tích tỉ số khoảng cách 2 điểm (2 Kênh A & B):**  
  - Tỉ số khoảng cách thực tế giữa hai máy đo:
    $$\frac{r_B}{r_A} = 10^{\frac{L_A - L_B}{20}}$$
  - Độ chênh lệch cự ly:
    $$\Delta r = |r_B - r_A|$$

---

### 8. Module Phiếu Báo Cáo Thực Hành A4 & Ứng dụng Ngoại tuyến (PWA Offline)

- **Mô tả chức năng:**  
  Tự động hóa hoàn toàn quy trình lập báo cáo thực hành của học sinh; đồng bộ dữ liệu thời gian thực giữa màn hình đo chính và phiếu báo cáo A4, xuất file đa định dạng và hỗ trợ chạy hoàn toàn không cần Internet.

- **Thuật toán 1 — Đồng bộ dữ liệu liên tab (Cross-Tab Data Synchronization):**  
  - Sử dụng kết hợp `BroadcastChannel("foxlab_report_sync")` và `localStorage` làm kênh dự phòng. Mọi số liệu đo (tần số, chu kỳ, mức dB, bảng lần đo) và ảnh chụp đồ thị Canvas (dưới dạng chuỗi `Base64 Image`) từ màn hình chính được bắn sang trang `report.html` ngay lập tức mà không cần reload trang.

- **Thuật toán 2 — Bộ lọc khử khuẩn DOM XSS bảo mật cao (Enhanced Sanitizer):**  
  - Ngăn ngừa hoàn toàn nguy cơ chèn mã độc JavaScript thông qua ô nhận xét bài tập `contenteditable`:
    ```javascript
    function sanitizeReportHtml(htmlStr) {
      if (!htmlStr) return '';
      let sanitized = htmlStr
        .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
        .replace(/<iframe\b[^<]*(?:(?!<\/iframe>)<[^<]*)*<\/iframe>/gi, '')
        .replace(/<object\b[^<]*(?:(?!<\/object>)<[^<]*)*<\/object>/gi, '')
        .replace(/<svg\b[^<]*(?:(?!<\/svg>)<[^<]*)*<\/svg>/gi, '')
        .replace(/<math\b[^<]*(?:(?!<\/math>)<[^<]*)*<\/math>/gi, '')
        .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
        .replace(/<base\b[^<]*>/gi, '')
        .replace(/<form\b[^<]*(?:(?!<\/form>)<[^<]*)*<\/form>/gi, '');
      sanitized = sanitized.replace(/\s*on\w+\s*=\s*(?:'[^']*'|"[^"]*"|[^\s>]+)/gi, '');
      sanitized = sanitized.replace(/(href|src|xlink:href|formaction|action)\s*=\s*(?:'(?:javascript|vbscript|data):[^']*'|"(?:javascript|vbscript|data):[^"]*"|(?:javascript|vbscript|data):[^\s>]+)/gi, '');
      return sanitized;
    }
    ```

- **Thuật toán 3 — Kết xuất Báo cáo Đa định dạng (PDF / CSV / PNG):**  
  - *Xuất PDF chuẩn in A4:* Tích hợp `html2pdf.js` cấu hình kích thước khổ giấy A4 dọc ($210 \times 297\text{ mm}$), chia trang tự động (`pagebreak: avoid-all`).
  - *Xuất Excel CSV:* Tạo mảng dữ liệu nhị phân chuẩn encoding `UTF-8 with BOM` (`\uFEFF`) giúp mở trực tiếp trên Microsoft Excel không bao giờ bị lỗi font tiếng Việt.
  - *Xuất ảnh Canvas:* Trích xuất đồ thị sang ảnh độ phân giải cao `image/png` kèm dấu mờ kỹ thuật số (Timestamp Watermark).

- **Thuật toán 4 — Bộ nhớ đệm PWA Service Worker (Cache-First Offline Strategy):**  
  - Tệp `sw.js` phiên bản `foxlab-pwa-v6.4.0` đăng ký lưu sẵn toàn bộ tài nguyên cốt lõi (`index.html`, `report.html`, `style.css`, `script.js`, `manifest.json`, `version.json`, các biểu tượng `icon-192.png`, `icon-512.png`). Ứng dụng có thể cài đặt trực tiếp lên màn hình chính máy tính hoặc điện thoại (Standalone PWA) và hoạt động mượt mà ở các phòng thí nghiệm không có sóng Wi-Fi.

---

### 9. Trợ Lý Ảo FOX_LAB AI Chatbot (Google Gemini Flash Engine)

- **Mô tả chức năng:**  
  Trợ lý gia sư AI tích hợp sẵn trong phòng thí nghiệm, có khả năng đọc hiểu ngữ cảnh đo đạc thời gian thực, giải đáp bài tập, nhận diện ảnh đề bài, nhận lệnh giọng nói và hỗ trợ học sinh thực hiện các phép tính Vật lý phức tạp.

- **Thuật toán 1 — Xử lý Ngữ cảnh Hội thoại Đa lượt (Multi-turn Context Memory):**  
  - Tích hợp mảng lịch sử `requestData.history` truyền qua Google Apps Script proxy (`backend/gas-foxlab-ai.js`), xây dựng mảng `contents` chứa toàn bộ các lượt đối thoại trước đó giữa `user` và `model`, đảm bảo AI ghi nhớ mạch trao đổi bài học của học sinh.

- **Thuật toán 2 — Truyền ngữ cảnh số liệu đo trực tiếp (Live Measurement Context Injection):**  
  - Khi học sinh bấm gửi câu hỏi, hệ thống tự động bóc tách trạng thái phòng thí nghiệm hiện thời (tần số đo được $f$, chu kỳ $T$, mức $\text{dB}$, chế độ lọc) và đính kèm vào phần đầu tin nhắn ẩn chuyển tới AI. AI có thể trả lời chính xác: *"Dựa vào tần số 440 Hz bạn vừa đo được từ âm thoa..."*.

- **Thuật toán 3 — Nhận diện giọng nói & Đọc đề bài bằng thị giác máy tính:**  
  - *Giọng nói:* Tích hợp `webkitSpeechRecognition` hỗ trợ tiếng Việt (`vi-VN`) giúp học sinh nhập câu hỏi rảnh tay trong khi đang thao tác thí nghiệm cơ học.
  - *Thị giác máy tính:* Cho phép chụp ảnh đề bài thi/đồ thị trong sách bài tập, nén ảnh Base64 và gửi trực tiếp cho mô hình Gemini Vision phân tích.

- **Thuật toán 4 — Bộ xử lý công thức Toán - Lý (MathJax TeX & Regex LaTeX Engine):**  
  - Tự động nhận diện cú pháp LaTeX (`$...$`, `$$...$$`, `\frac{...}{...}`, `\lambda`, `\Delta \varphi`) và kích hoạt `MathJax.typesetPromise()` để render công thức chuẩn mực như sách giáo khoa.

---

### Bảng Tổng hợp Tải lượng Tính năng & Thuật toán Cốt lõi của Hệ thống

| STT | Phân hệ Chức năng | Thuật toán Cốt lõi Triển khai | Tệp Mã nguồn Chính |
| :---: | :--- | :--- | :--- |
| **1** | **Xử lý Luồng Âm thanh (DSP Engine)** | `AudioWorkletNode`, Biquad Bandpass Filter (HP 45 Hz, LP 5000 Hz), Static Ring Buffer 10s | `script.js` |
| **2** | **Dao động ký (Oscilloscope)** | Autocorrelation Function (ACF), Parabolic Interpolation, Zero-crossing Hysteresis Trigger | `script.js` |
| **3** | **Phân tích 2 Điểm & Đồ thị Động học** | Time/Phase Cursor Differential, Đạo hàm số sai phân trung tâm ($u \to v \to a$) | `script.js` |
| **4** | **Đo Mức Cường độ Âm (dB Meter)** | True RMS Calculation, Logarithmic Decibel Scaling, Ngưỡng cảnh báo an toàn $85\text{ dB}$ | `script.js` |
| **5** | **Phổ Họa âm Spectrum (FFT Analyzer)** | Cooley-Tukey FFT ($N=4096$), Hanning Windowing, Harmonic Peak Extraction & Sweep Animation | `script.js` |
| **6** | **Xử lý 2 Nguồn Âm & Sóng phách** | Cross-Correlation Phase Analysis, Beat Wave Thresholding ($>3\text{ Hz}$), Harmonic Superposition | `script.js` |
| **7** | **Đo Khoảng cách Nguồn Âm** | Inverse Square Law Scaling ($I \propto 1/r^2$), Quy đổi Decibel 1 vị trí & tỉ số 2 vị trí | `script.js` |
| **8** | **Phiếu Báo cáo A4 & PWA Offline** | Cross-Tab Sync (BroadcastChannel), Bộ lọc DOM XSS, html2pdf.js, PWA Cache-First Service Worker | `report.html`, `sw.js` |
| **9** | **Trợ lý Ảo AI (Gemini Flash)** | Multi-turn History Context, Live Measurement Injection, Speech-to-Text, MathJax TeX Parser | `backend/gas-foxlab-ai.js` |

---

# PHẦN 2: QUY TRÌNH THỰC NGHIỆM CHO TẤT CẢ CÁC CHỨC NĂNG SẢN PHẨM

---

### Quy trình 1: Đo Tần số, Chu kỳ và Khảo sát Dạng Sóng Cơ Học
*(Phù hợp Bài học: "Dao động điều hòa" & "Sóng cơ và sự truyền sóng cơ" — Vật lý 11)*

- **1. Mục đích thí nghiệm:**  
  - Quan sát dạng đồ thị li độ - thời gian của sóng âm phát ra từ nguồn âm tuần hoàn (âm thoa chuẩn, máy phát âm tần Tone Generator hoặc nhạc cụ).
  - Xác định chính xác chu kỳ dao động $T$ (ms) và tần số dao động $f$ (Hz).
  - Đối chiếu giá trị đo thực nghiệm với tần số danh định của nguồn âm để đánh giá sai số.

- **2. Dụng cụ chuẩn bị:**  
  - 01 Thiết bị (Máy tính xách tay, máy tính bảng hoặc điện thoại thông minh) chạy ứng dụng FOX_LAB.
  - Microphone tích hợp sẵn trên thiết bị hoặc micro rời cắm qua cổng $3.5\text{ mm}$ / USB.
  - 01 Âm thoa chuẩn (ví dụ loại $440\text{ Hz}$ hoặc $512\text{ Hz}$) kèm búa cao su (hoặc mở ứng dụng phát tần số Tone Generator trên điện thoại phụ).

- **3. Các bước tiến hành:**  
  - **Bước 1:** Khởi động FOX_LAB trên trình duyệt. Tại thanh cài đặt phía trên, thiết lập:
    - *Nguồn âm:* `1 Nguồn`.
    - *Chế độ hiển thị:* `Dao động ký`.
    - *Tốc độ:* `Nhanh`.
  - **Bước 2:** Nhấn nút **Kênh A (Khóa)** để kích hoạt quyền truy cập microphone; nút chuyển trạng thái sang **Kênh A (Hoạt động)** màu xanh.
  - **Bước 3:** Nhấn nút **Đo / Dừng** (màu xanh lá) để bắt đầu quét tín hiệu.
  - **Bước 4:** Gõ nhẹ búa cao su vào nhánh âm thoa và đưa sát vào microphone (khoảng cách $5 - 10\text{ cm}$).
  - **Bước 5:** Quan sát dạng sóng hình sin xuất hiện trên màn hình Canvas. Nhờ thuật toán Zero-Crossing Hysteresis, đồ thị sóng đứng yên hoàn toàn.
  - **Bước 6:** Bấm nút **Đang đo...** (nút màu đỏ) để dừng và khóa dạng sóng.
  - **Bước 7:** Đọc trực tiếp các giá trị số hiển thị tại góc trên màn hình:
    - Tần số đo được: $f_{\text{đo}}\text{ (Hz)}$.
    - Chu kỳ đo được: $T_{\text{đo}}\text{ (ms)}$.
    - Biên độ đỉnh: $A_{\text{peak}}\text{ (V)}$.

- **4. Báo cáo & Xử lý số liệu:**  
  - Ghi giá trị vào bảng thực hành. Tính sai số tuyệt đối và sai số tương đối:
    $$\Delta f = |f_{\text{đo}} - f_{\text{chuẩn}}|, \quad \delta f = \frac{\Delta f}{f_{\text{chuẩn}}} \cdot 100\%$$
  - *Đánh giá chuẩn:* Với âm thoa chuẩn $440\text{ Hz}$, sai số thực tế của thuật toán tự tương quan trên FOX_LAB thường $< 0.5\%$.

---

### Quy trình 2: Phân tích 2 Điểm Đo & Khảo sát Mối Liên Hệ Động Học ($u-t, v-t, a-t$)
*(Phù hợp Bài học: "Vận tốc, gia tốc trong dao động điều hòa" — Vật lý 11)*

- **1. Mục đích thí nghiệm:**  
  - Sử dụng công cụ con trỏ 2 điểm để đo khoảng thời gian giữa hai trạng thái dao động bất kỳ trên đồ thị thực.
  - Khảo sát sự biến thiên của đồ thị li độ $u(t)$, vận tốc $v(t)$ và gia tốc $a(t)$ rút ra từ tín hiệu đo thực tế.
  - Chứng minh thực nghiệm: Vận tốc sớm pha $\pi/2$ so với li độ, gia tốc ngược pha ($\pi$) so với li độ.

- **2. Dụng cụ chuẩn bị:**  
  - Thiết bị chạy FOX_LAB có tín hiệu sóng âm đã được khóa sau khi thực hiện Quy trình 1.

- **3. Các bước tiến hành:**  
  - **Bước 1:** Sau khi khóa sóng ở Quy trình 1, bấm nút **Phân tích đồ thị ▼** trên thanh điều khiển, chọn tính năng **🎯 1. Chọn 2 điểm đo T, f, Δφ**.
  - **Bước 2:** Chạm/Nhấp chuột vào đỉnh thứ nhất của đồ thị để đặt **Điểm 1** (vòng tròn đánh dấu màu xanh).
  - **Bước 3:** Chạm/Nhấp chuột vào đỉnh thứ hai liền kề (hoặc cách $N$ chu kỳ) để đặt **Điểm 2** (vòng tròn đánh dấu màu cam).
  - **Bước 4:** Quan sát bảng HUD kết quả hiện ra góc phải: Đọc $\Delta t\text{ (ms)}$, chu kỳ $T$, tần số $f$ và góc lệch pha $\Delta \varphi$.
  - **Bước 5:** Tiếp tục bấm menu **Phân tích đồ thị ▼**, chọn tính năng **📈 2. Vẽ các đồ thị liên quan (u-t, v-t, a-t)**.
  - **Bước 6:** Modal đồ thị động học xuất hiện:
    - Bấm nút **u-t & v-t**: Quan sát đồ thị sóng li độ $u$ (đỏ) và vận tốc $v$ (xanh lá). Kiểm tra thấy khi $u$ qua vị trí cân bằng ($u=0$) thì $|v|$ đạt cực đại.
    - Bấm nút **u-t & a-t**: Quan sát đồ thị li độ $u$ (đỏ) và gia tốc $a$ (tím). Kiểm tra thấy hai đồ thị luôn ngược pha nhau đối xứng qua trục hoành.
    - Bấm nút **Cả hai (v-t & a-t)** để đối sánh toàn diện 3 đại lượng.

- **4. Báo cáo & Xử lý số liệu:**  
  - Chụp ảnh đồ thị bằng nút **📷 Xuất ảnh đồ thị** để đính kèm vào báo cáo thực hành.

---

### Quy trình 3: Khảo sát Mức Cường độ Âm & Đánh giá Ô nhiễm Tiếng ồn Môi trường
*(Phù hợp Bài học: "Đặc trưng vật lý và sinh lý của âm" — Vật lý 11)*

- **1. Mục đích thí nghiệm:**  
  - Làm quen với đại lượng Mức Cường độ Âm và thang đo Logarit Decibel ($dB$).
  - Đo mức cường độ âm của các nguồn âm khác nhau trong môi trường học tập (tiếng quạt, tiếng nói thì thầm, tiếng vỗ tay, tiếng reo hò).
  - Đánh giá mức độ ô nhiễm tiếng ồn theo tiêu chuẩn an toàn lao động ($85\text{ dB}$).

- **2. Dụng cụ chuẩn bị:**  
  - Thiết bị chạy FOX_LAB kết nối microphone.
  - Thước dây để cố định khoảng cách đo.

- **3. Các bước tiến hành:**  
  - **Bước 1:** Trên thanh cài đặt, chuyển mục **Chế độ hiển thị** từ `Dao động ký` sang `Cường độ âm (dB)`.
  - **Bước 2:** Nhấn nút **Đo / Dừng**. Màn hình chuyển sang giao diện đo $dB$ với biểu đồ cột chạy liên tục cập nhật mỗi $50\text{ ms}$.
  - **Bước 3:** Để yên trong phòng không có người nói chuyện trong $5\text{ giây}$ để ghi nhận tiếng ồn nền phòng học ($L_{\text{nền}}$).
  - **Bước 4:** Lần lượt tạo các nguồn âm ở khoảng cách $1.0\text{ m}$:
    - Người nói chuyện mức bình thường.
    - Phát bài nhạc trên điện thoại ở mức âm lượng vừa.
    - Vỗ tay mạnh dứt khoát.
  - **Bước 5:** Nhấn **Đo / Dừng** để dừng quét. Quan sát các cột lịch sử đo:
    - Di chuột hoặc chạm vào thanh cột bất kỳ để xem bảng Tooltip chi tiết: giá trị $dB$ và mốc thời gian mẫu.
    - Nhận diện các cột đổi sang màu cam đậm/đỏ ($> 85\text{ dB}$) biểu thị âm thanh có nguy cơ gây hại thính giác nếu tiếp xúc kéo dài.
  - **Bước 6:** Bấm nút **Phân tích MCĐ nguồn âm** để mở bảng thống kê đầy đủ: $L_{\text{max}}$, $L_{\text{min}}$, $L_{\text{tb}}$.

- **4. Báo cáo & Xử lý số liệu:**  
  - Hoàn thành bảng số liệu mức cường độ âm theo từng hoạt động. Đưa ra đề xuất cải thiện môi trường âm học trong lớp học.

---

### Quy trình 4: Phân tích Phổ Họa âm & Khảo sát Âm sắc của Nhạc cụ
*(Phù hợp Bài học: "Âm sắc và các đặc trưng sinh lý của âm" — Vật lý 11)*

- **1. Mục đích thí nghiệm:**  
  - Sử dụng công cụ phân tích phổ FFT để giải thích bản chất vật lý của **Âm sắc**: Tại sao cùng một nốt nhạc (cùng tần số cơ bản $f_0$) nhưng âm thanh đàn guitar, đàn piano và sáo trúc lại nghe hoàn toàn khác nhau.
  - Xác định tần số cơ bản $f_0$ và tỷ lệ biên độ của các họa âm bậc $2, 3, 4, 5$.

- **2. Dụng cụ chuẩn bị:**  
  - Thiết bị chạy FOX_LAB.
  - Các loại nhạc cụ thật (Đàn guitar, đàn ukulele, sáo) hoặc các file âm thanh ghi âm tiếng nhạc cụ chuẩn nốt La4 ($f_0 = 440\text{ Hz}$).

- **3. Các bước tiến hành:**  
  - **Bước 1:** Khởi động chế độ `Dao động ký 1 Nguồn`. Gảy nốt La trên đàn guitar gần micro, bấm nút **Đo / Dừng** để khóa sóng.
  - **Bước 2:** Bấm nút **Phân tích FFT** (nút màu xanh trên thanh điều khiển).
  - **Bước 3:** Cửa sổ Modal Phổ tần số FFT xuất hiện:
    - Trục hoành biểu thị tần số ($0 - 3000\text{ Hz}$), trục tung biểu thị biên độ tương đối.
    - Tần số đỉnh cao nhất chính là âm cơ bản $f_0 \approx 440\text{ Hz}$.
  - **Bước 4:** Bấm nút **Quét Họa âm**. Hệ thống tự động kích hoạt vạch quét laser và đánh dấu 5 đỉnh họa âm:
    - Âm cơ bản $1f_0 = 440\text{ Hz}$.
    - Họa âm 2: $2f_0 = 880\text{ Hz}$.
    - Họa âm 3: $3f_0 = 1320\text{ Hz}$.
    - Họa âm 4: $4f_0 = 1760\text{ Hz}$.
    - Họa âm 5: $5f_0 = 2200\text{ Hz}$.
  - **Bước 5:** Bấm **📊 Bảng tần số & họa âm** để mở bảng thống kê phần trăm biên độ chi tiết ($A_1, A_2, A_3, A_4, A_5$).
  - **Bước 6:** Lặp lại thí nghiệm với tiếng sáo trúc hoặc đàn piano.

- **4. Báo cáo & Xử lý số liệu:**  
  - Vẽ lại phổ vạch hoặc chụp ảnh phổ FFT của hai nhạc cụ. So sánh phổ vạch và rút ra kết luận: *Âm sắc phụ thuộc vào số lượng và tỷ lệ biên độ của các họa âm trong phổ.*

---

### Quy trình 5: Khảo sát Ghép Sóng, Tổng Hợp Dao Động & Hiện Tượng Sóng Phách
*(Phù hợp Bài học: "Giao thoa sóng" & "Tổng hợp hai dao động điều hòa cùng phương, cùng tần số" — Vật lý 11)*

- **1. Mục đích thí nghiệm:**  
  - Thực hành ghép và tổng hợp tín hiệu âm thanh thu được từ hai nguồn độc lập trên Kênh A và Kênh B.
  - Quan sát dạng sóng tổng hợp khi hai nguồn đồng pha, ngược pha hoặc lệch pha bất kỳ.
  - Khảo sát hiện tượng **Sóng phách (Beats)** khi hai nguồn âm có tần số gần bằng nhau ($f_A \approx f_B$).

- **2. Dụng cụ chuẩn bị:**  
  - 02 Chiếc điện thoại phát âm tần mở ứng dụng Tone Generator (Nguồn 1 và Nguồn 2).
  - 01 Máy tính chạy FOX_LAB.

- **3. Các bước tiến hành:**  
  - **Bước 1:** Trên thanh cài đặt FOX_LAB, chọn:
    - *Nguồn âm:* `2 Nguồn`.
    - Kích hoạt cả **Kênh A (Hoạt động)** và **Kênh B (Hoạt động)**.
  - **Bước 2 — Thí nghiệm Tổng hợp Dao động (Cùng tần số):**  
    - Cài đặt cả 2 điện thoại phát âm tần $f_1 = f_2 = 440\text{ Hz}$.
    - Nhấn nút **Đo / Dừng** để thu tín hiệu 2 kênh, sau đó nhấn **Dừng**.
    - Bấm nút **Xử lý nguồn âm** (màu hồng).
    - Bấm nút **Ghép sóng**: Quan sát đồ thị màu đỏ (Kênh A) và màu xanh (Kênh B) cùng hiển thị đồng thời.
    - Bấm nút **Tổng hợp (A+B)**: Quan sát đồ thị màu tím biểu diễn dao động tổng hợp $u = u_A + u_B$.
    - Thay đổi vị trí 2 micro để thay đổi độ lệch pha $\Delta \varphi$. Bấm **📐 Phương trình** để xem phương trình dao động thành phần và phương trình tổng hợp do hệ thống giải tự động.
  - **Bước 3 — Thí nghiệm Sóng phách (Lệch tần số nhẹ):**  
    - Cài đặt Nguồn 1 phát $f_A = 440\text{ Hz}$, Nguồn 2 phát $f_B = 444\text{ Hz}$ (chênh lệch $\Delta f = 4\text{ Hz}$).
    - Bấm đo tín hiệu. Lắng nghe âm thanh có độ to trầm bổng biến thiên tuần hoàn (tiếng phách ngân nga).
    - Quan sát trên màn hình: Hệ thống tự động nhận diện chênh lệch tần số $> 3\text{ Hz}$ và kích hoạt cảnh báo màu vàng: `⚠️ Cảnh báo: Hai nguồn khác tần số (Tạo Sóng Phách)`.
    - Dạng sóng tổng hợp hiển thị rõ nét hình bao sóng phách (Envelope) với các múi thắt và bụng dao động.

- **4. Báo cáo & Xử lý số liệu:**  
  - Tính tần số phách thực nghiệm $f_{\text{phách}} = |f_A - f_B|$, so sánh với số lần âm thanh to lên trong $1\text{ giây}$ đếm được bằng tai.

---

### Quy trình 6: Xác Định Khoảng Cách Nguồn Âm Dựa Trên Mức Cường Độ Âm
*(Phù hợp Bài học: "Định luật truyền sóng và bảo toàn năng lượng âm" — Vật lý 11 nâng cao & STEM)*

- **1. Mục đích thí nghiệm:**  
  - Ứng dụng quy luật suy giảm mức cường độ âm theo khoảng cách để ước tính khoảng cách từ vị trí đặt máy đo tới nguồn phát âm mà không cần dùng thước dây.
  - Khảo sát sự suy giảm năng lượng sóng âm lan truyền trong không gian.

- **2. Dụng cụ chuẩn bị:**  
  - 01 Loa phát âm đơn tần phát liên tục $1000\text{ Hz}$ với công suất không đổi.
  - Thước dây cuộn $5\text{ m}$ để đối chứng kết quả thực tế.
  - Thiết bị chạy FOX_LAB.

- **3. Các bước tiến hành:**  
  - **Phương án 1: Đo khoảng cách 1 điểm (dùng mốc chuẩn):**  
    - Bước 1: Đặt loa phát âm ổn định. Đặt micro thiết bị cách loa một khoảng bất kỳ $r_x$ chưa biết.
    - Bước 2: Chọn chế độ đo cường độ âm `1 Nguồn`, quét đo mức decibel trung bình $L_{\text{tb}}$.
    - Bước 3: Nhấn nút **🎯 Hiệu chuẩn** nếu muốn lấy lại mốc cự ly $r_0 = 1.0\text{ m}$ tương ứng $L_0$ thực tế của loa.
    - Bước 4: Mở tính năng tính khoảng cách, hệ thống tự động tính ra giá trị cự ly $r_x\text{ (m)}$.
  - **Phương án 2: Đo khoảng cách 2 vị trí (Độc lập nguồn phát):**  
    - Bước 1: Đặt Microphone A ở vị trí 1 (gần nguồn âm), Microphone B ở vị trí 2 (xa nguồn âm).
    - Bước 2: Đo đồng thời cường độ âm của 2 vị trí ở chế độ `2 Nguồn`, ghi nhận $L_A$ và $L_B$.
    - Bước 3: Nhấn **Phân tích MCĐ nguồn âm** $\to$ **Tính khoảng cách nguồn âm chính xác**.
    - Bước 4: Đọc tỉ số khoảng cách tính toán tự động:
      $$\frac{r_B}{r_A} = 10^{\frac{L_A - L_B}{20}}$$
  - **Bước 5:** Dùng thước dây đo khoảng cách thực tế $r_{\text{thực}}$ giữa loa và micro.

- **4. Báo cáo & Xử lý số liệu:**  
  - So sánh khoảng cách tính từ âm học và khoảng cách đo hình học. Giải thích nguyên nhân sai số (do phản xạ âm từ tường, đồ vật trong phòng thí nghiệm).

---

### Quy trình 7: Lập Phiếu Báo Cáo Thực Hành A4, Đồng Bộ Số Liệu & Xuất File (PDF/Excel)
*(Phù hợp: Hoạt động đánh giá kết thúc buổi thực hành)*

- **1. Mục đích thí nghiệm:**  
  - Thu thập toàn bộ kết quả đo đạc từ các quy trình trước, kết xuất ra phiếu báo cáo thực hành thí nghiệm chuẩn A4 có đầy đủ thông tin học sinh, biểu bảng, đồ thị thực tế và phần nhận xét.
  - Xuất file báo cáo sang định dạng PDF chính thức nộp cho giáo viên hoặc file Excel CSV để phân tích sai số chuyên sâu.

- **2. Dụng cụ chuẩn bị:**  
  - Trình duyệt đã hoàn thành các phép đo ở các Quy trình 1, 3, 4.

- **3. Các bước tiến hành:**  
  - **Bước 1:** Trên màn hình chính FOX_LAB, nhấn nút **📄 Xuất báo cáo** (màu xanh dương).
  - **Bước 2:** Cửa sổ Modal Phiếu Báo Cáo Thực Hành A4 hiện lên:
    - Hệ thống tự động điền các thông số kỹ thuật vừa đo: Thang đo ngang ($\text{ms/ô}$), Thang đo dọc ($\text{V/ô}$), Tần số lấy mẫu ($\text{Hz}$), Trạng thái bộ lọc số.
    - Chạm vào các ô trống ở phần đầu để điền: *Tên Trường, Lớp, Nhóm học sinh, Tên các thành viên*.
  - **Bước 3:** Nhấn nút **🔄 Đồng bộ dữ liệu** để nạp đồ thị đo mới nhất vào khung hiển thị báo cáo.
  - **Bước 4:** Thêm các dòng kết quả đo lường:
    - Tại Phần I (Dao động ký): Bấm **+ Thêm lần đo** để nhập các lần đo lặp lại. Hệ thống tự động tính giá trị trung bình $\bar{T}, \bar{f}$ và sai số tuyệt đối $(\bar{T} \pm \Delta T)$.
    - Tại Phần II (Phổ FFT): Bấm **+ Thêm nguồn âm** để lưu kết quả phân tích họa âm.
    - Tại Phần III (Cường độ âm): Bấm **+ Thêm vị trí đo** để lưu bảng số liệu decibel.
  - **Bước 5:** Học sinh chạm vào khung **PHẦN V: NHẬN XÉT VÀ ĐÁNH GIÁ** để gõ phần kết luận giải thích hiện tượng.
  - **Bước 6 — Xuất bản báo cáo:**  
    - Nhấn **📥 Xuất file** $\to$ **Xuất toàn bộ báo cáo (PDF A4)**: Trình duyệt tự động biên dịch toàn bộ văn bản và đồ thị sang file `FOXLAB_BaoCao_NhomX.pdf`.
    - Nhấn **Xuất bảng số liệu ra Excel (CSV)**: Tải về file `FOXLAB_BaoCao_DayDu.csv`.
    - (Tùy chọn) Bấm **↗ Trang riêng** để mở báo cáo ở tab độc lập `report.html`.

- **4. Tiêu chí đánh giá bài thực hành:**  
  - Độ chuẩn xác của số liệu thực nghiệm ($40\%$).
  - Chất lượng hình ảnh đồ thị và xử lý sai số thống kê ($30\%$).
  - Nhận xét bản chất vật lý và trả lời câu hỏi mở rộng ($30\%$).

---

### Quy trình 8: Khai Thác Trợ Lý AI (Fox-Lab AI) Hỗ Trợ Tự Học & Xử Lý Dữ Liệu
*(Phù hợp: Hoạt động tự học, nghiên cứu mở rộng và hướng dẫn phân hóa học sinh)*

- **1. Mục đích thí nghiệm:**  
  - Sử dụng trợ lý ảo AI Gemini tích hợp sẵn trong FOX_LAB để giải đáp lý thuyết sóng cơ, hướng dẫn các bước thao tác khi gặp khó khăn và kiểm tra chéo số liệu thực nghiệm.

- **2. Dụng cụ chuẩn bị:**  
  - Thiết bị chạy FOX_LAB có kết nối mạng Internet (để giao tiếp với API AI).

- **3. Các bước tiến hành:**  
  - **Bước 1:** Nhấn vào biểu tượng Trợ lý Fox ở góc dưới bên phải màn hình để bung mở khung Chatbox.
  - **Bước 2 — Chuyển đổi vai trò tương tác:**  
    - Nhấn nút **👨‍🎓 HS**: AI đóng vai trò gia sư sư phạm, gợi ý từng bước theo phương pháp đàm thoại gợi mở, không đưa ngay đáp án cuối cùng.
    - Nhấn chuyển sang nút **👨‍🏫 GV**: AI đóng vai trò đồng nghiệp trợ giảng, cung cấp đáp án chi tiết, gợi ý barem chấm điểm và giải thích sâu về kỹ thuật đo.
  - **Bước 3 — Sử dụng Chip câu hỏi nhanh (Quick Prompt Chips):**  
    - Bấm nhanh các nút: `🌊 Sóng phách`, `🔊 Mức cường độ âm`, `⚙️ Các bước thí nghiệm`, `📊 Phân tích FFT`.
  - **Bước 4 — Hỏi đáp gắn liền số liệu thời gian thực:**  
    - Đang đo một âm thanh trên dao động ký, mở chat và gõ: *"Hãy giải thích dạng sóng và tần số mà máy đang đo được"*.  
    - AI tự động đọc dữ liệu live tag (ví dụ `440.0 Hz`) và phản hồi chính xác về nguồn âm đang khảo sát.
  - **Bước 5 — Nhập liệu rảnh tay bằng Giọng nói:**  
    - Nhấn biểu tượng Micro trong khung chat, nói rõ ràng: *"Độ lệch pha giữa hai sóng được tính bằng công thức nào?"*. AI nhận diện giọng nói tiếng Việt và tự động gửi tin nhắn.
  - **Bước 6 — Tải ảnh bài tập bằng Thị giác AI:**  
    - Bấm biểu tượng hình ảnh, chụp/tải lên đề bài bài tập sóng cơ trong sách. AI tự đọc đề bài và hướng dẫn phương pháp giải.
  - **Bước 7:** Bấm biểu tượng **Copy** hoặc **Xuất biên bản hội thoại** để lưu kiến thức vào sổ tay thực hành.

---

### KẾT LUẬN VÀ KHUYẾN NGHỊ SƯ PHẠM

Hệ thống **FOX_LAB (v6.4.0)** là giải pháp chuyển đổi số toàn diện trong dạy học thực hành Vật lý, đáp ứng trọn vẹn yêu cầu phát triển phẩm chất và năng lực khoa học của học sinh theo định hướng giáo dục hiện đại:
1. **Tính chính xác và khoa học:** Xử lý tín hiệu thời gian thực ở cấp độ vi xử lý số (AudioWorklet, FFT 4096 điểm, tương quan chéo), cung cấp kết quả đo đạc tin cậy, trực quan.
2. **Tính sư phạm và linh hoạt:** Bao quát toàn diện các chủ đề cốt lõi của sóng cơ học (dao động, sóng, âm sắc, giao thoa, mức cường độ âm, hiệu ứng phách) chỉ với một thiết bị thông minh thông thường.
3. **Tính hiện đại và mở rộng:** Tích hợp Trợ lý Trí tuệ Nhân tạo đa phương thức (Văn bản, Giọng nói, Thị giác) cùng hệ thống tạo báo cáo chuẩn hóa và khả năng vận hành ngoại tuyến (PWA Offline) bền bỉ.
