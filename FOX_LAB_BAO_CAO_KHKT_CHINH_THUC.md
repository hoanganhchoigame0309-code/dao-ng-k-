# FOX-Lab: Thiết kế phòng thí nghiệm Sóng âm di động trực quan hóa đại lượng vật lý và tự động hóa quy trình báo cáo thực hành trong môi trường lớp học

**Ngày hoàn thành:** 29/10/2026  
**Lĩnh vực dự thi:** Vật lý và Thiên văn / Phần mềm hệ thống (*System Software*)  
**Nhóm tác giả:** Ngô Hoàng Anh – Lớp 11A2, Phạm Thanh Bình – Lớp 11A7, Trường Ngô Quyền  
**Giáo viên hướng dẫn:** Võ Bình Minh, đơn vị công tác  
**Địa chỉ liên hệ:** email / số điện thoại  
**Website triển khai:** [https://hoanganhchoigame0309-code.github.io/dao-ng-k-/](https://hoanganhchoigame0309-code.github.io/dao-ng-k-/)  
**Mã nguồn công khai:** [https://github.com/hoanganhchoigame0309-code/dao-ng-k-](https://github.com/hoanganhchoigame0309-code/dao-ng-k-)

---

### Tóm tắt
FOX-Lab là một ứng dụng web chạy trực tiếp trên trình duyệt của điện thoại, máy tính bảng hoặc máy tính, biến micro thành một dao động ký (*oscilloscope*) hai kênh để học sinh quan sát, đo đạc và phân tích sóng âm ngay trong lớp học, không cần thiết bị đo chuyên dụng.

Ứng dụng thu tín hiệu âm thanh qua Web Audio API, lọc dải 80–3000 Hz, rồi tự động tìm tần số bằng thuật toán tự tương quan có nội suy parabol. Dựa trên tần số tìm được, hệ thống tự chọn thang thời gian để màn hình luôn hiển thị khoảng 5 chu kỳ và dùng điều kiện kích (*trigger*) qua điểm không để dạng sóng đứng yên như trên dao động ký thật. Sau khi "khóa sóng", học sinh có thể phóng to thu nhỏ, đọc biên độ, chu kỳ, tần số trên lưới 10 × 8 ô, lưu ảnh đồ thị một chạm, hoặc mở chế độ phân tích FFT 8192 điểm với cửa sổ Hann để xem năm họa âm đầu tiên (H1–H5) của một nốt nhạc.

Ngoài phần đo, dự án tích hợp trợ lý FOX-Lab AI. Trợ lý nhận tần số đo thời gian thực làm ngữ cảnh để giải thích hiện tượng, hướng dẫn xử lý số liệu và gợi ý cách viết báo cáo thực hành; khi mất kết nối, một bộ trả lời dự phòng cục bộ vẫn hoạt động. Mã QR trên giao diện giúp cả lớp mở cùng một địa chỉ web bằng điện thoại của mình.

Điểm mới của dự án là gộp ba việc vốn tách rời – đo (dao động ký), phân tích (FFT) và hướng dẫn xử lý báo cáo (trợ lý AI) – vào một công cụ miễn phí, nhẹ, chạy trên thiết bị học sinh sẵn có. Báo cáo này trình bày cơ sở khoa học, thiết kế, các thuật toán cốt lõi, phương án thực nghiệm và hướng phát triển của sản phẩm.

**Từ khóa:** *dao động ký, sóng âm, tần số, họa âm, FFT, Web Audio API, thí nghiệm ảo di động, trợ lý AI, Vật lí 11.*

---

## PHẦN 1. ĐẶT VẤN ĐỀ

### 1.1. Lý do chọn đề tài
Sóng âm là nội dung quen thuộc của chương Dao động và Sóng trong chương trình Vật lí 11 (chương trình giáo dục phổ thông 2018). Các đại lượng như biên độ, chu kỳ, tần số, độ cao, âm sắc đều có thể quan sát trực tiếp bằng dao động ký. Tuy vậy, trong thực tế dạy học, các khái niệm này thường chỉ được học qua hình vẽ trong sách hoặc mô phỏng có sẵn, nơi học sinh không tự tạo ra được dữ liệu của riêng mình.

Dao động ký và máy phát tín hiệu chuyên dụng là thiết bị đắt tiền, cồng kềnh, thường chỉ có số lượng ít trong phòng thí nghiệm. Một lớp học 40–45 em khó có thể để mọi nhóm cùng thao tác. Trong khi đó, gần như mọi học sinh đều có điện thoại với micro chất lượng đủ tốt và trình duyệt hiện đại, nhưng các thiết bị này hiếm khi được khai thác như một dụng cụ đo trong giờ học.

Từ quan sát đó, nhóm tác giả đặt câu hỏi: liệu có thể biến chính điện thoại của học sinh thành một phòng thí nghiệm sóng âm di động, vừa đo được, vừa phân tích được, vừa hỗ trợ viết báo cáo? FOX-Lab là câu trả lời của nhóm.

### 1.2. Thực trạng và hạn chế của các giải pháp hiện có
Nhóm đã xem xét ba nhóm giải pháp học sinh thường gặp:
1. **Dao động ký phần cứng:** Cho kết quả chính xác, nhưng thiếu về số lượng, cần kỹ năng vận hành và không mang về nhà được.
2. **Mô phỏng có sẵn (applet, video):** Dễ dùng, song dữ liệu là dữ liệu mẫu; học sinh không thể thử với âm thanh thật như tiếng sáo, âm thoa, giọng nói của chính mình.
3. **Ứng dụng đo âm trên điện thoại:** Nhiều ứng dụng đo mức ồn (dB) hoặc hiển thị phổ, nhưng ít ứng dụng được thiết kế theo cách dạy học: dạng sóng đứng yên như dao động ký, thang thời gian tính bằng ms, ghi chú theo ngôn ngữ của sách giáo khoa, và không gắn với việc viết báo cáo thực hành.

Nhìn chung còn thiếu một công cụ thỏa mãn đồng thời bốn yêu cầu: dùng được ngay trên thiết bị sẵn có, hiển thị theo đúng "ngôn ngữ" của dao động ký, có phân tích họa âm ở mức học sinh hiểu được, và đồng hành với học sinh khi xử lý số liệu.

### 1.3. Khó khăn trong báo cáo thực hành
Quy trình thực hành truyền thống gồm: lắp thiết bị, chỉnh máy, đọc số trên màn hình, ghi vào vở, chụp hoặc vẽ lại đồ thị, tính toán rồi viết báo cáo. Ở mỗi bước, học sinh thường mất nhiều thời gian vào thao tác kỹ thuật (chỉnh thang thời gian, chỉnh mức kích) thay vì suy nghĩ về hiện tượng vật lí. Giáo viên cũng khó theo dõi tiến độ của từng nhóm.

### 1.4. Tính cấp thiết
- Chương trình 2018 nhấn mạnh phát triển năng lực thực nghiệm và năng lực sử dụng công nghệ số trong học tập môn Vật lí.
- Điện thoại thông minh là thiết bị sẵn có, giúp giảm chi phí và mở rộng cơ hội thực hành ra ngoài phòng thí nghiệm.
- Việc tự động hóa các thao tác kỹ thuật lặp lại giúp học sinh dành thời gian cho phần quan trọng nhất của khoa học: quan sát, nhận xét, giải thích và rút ra kết luận.

---

## PHẦN 2. MỤC TIÊU, ĐỐI TƯỢNG VÀ PHƯƠNG PHÁP NGHIÊN CỨU

### 2.1. Mục tiêu
**Mục tiêu chung:** thiết kế và hoàn thiện một phòng thí nghiệm sóng âm di động chạy trên trình duyệt, giúp học sinh trực quan hóa các đại lượng vật lí của sóng âm và giảm thao tác thủ công trong quy trình thực hành – báo cáo.

**Mục tiêu cụ thể:**
- Thu tín hiệu âm thanh từ micro của thiết bị và hiển thị dạng sóng theo thời gian thực như một dao động ký có lưới chia độ, trục thời gian (ms) và trục biên độ.
- Tự động xác định tần số cơ bản và tự điều chỉnh thang thời gian, kích sóng để dạng sóng đứng yên, dễ đọc chu kỳ.
- Hỗ trợ đo cùng lúc hai nguồn âm (Kênh A và Kênh B) để so sánh biên độ, tần số, độ lệch pha.
- Phân tích phổ bằng FFT để học sinh thấy được họa âm tạo nên âm sắc của nhạc cụ, giọng nói.
- Tích hợp trợ lý hỏi đáp FOX-Lab AI và các tiện ích (lưu ảnh, toàn màn hình, mã QR) để rút ngắn quy trình báo cáo thực hành.
- Bảo đảm chạy mượt trên điện thoại, máy tính bảng và máy tính, không cài đặt phức tạp.

### 2.2. Nhiệm vụ, đối tượng và phạm vi
- **Nhiệm vụ:** Nghiên cứu cơ sở vật lí và xử lí tín hiệu cần thiết (lấy mẫu, tự tương quan, FFT, cửa sổ Hann); thiết kế kiến trúc phần mềm; cài đặt thuật toán bằng JavaScript thuần; xây dựng trợ lý AI; thiết kế bài thực hành mẫu và thực nghiệm đối chứng.
- **Đối tượng nghiên cứu:** Sóng âm trong dải tần 100–1500 Hz và phổ họa âm đến bậc 5 của âm có tần số cơ bản từ 100 Hz đến vài trăm Hz.
- **Đối tượng sử dụng:** Học sinh và giáo viên Vật lí THPT, ưu tiên lớp 11.
- **Phạm vi:** Dùng làm công cụ minh họa, thực hành định tính và định lượng ở mức phổ thông.

### 2.3. Công nghệ sử dụng

| Thành phần | Công nghệ | Vai trò |
| :--- | :--- | :--- |
| **Thu tín hiệu** | `getUserMedia`, Web Audio API | Truy cập micro, tạo bộ lọc, nhận mẫu âm thanh. |
| **Xử lí** | JavaScript thuần | Tự tương quan, trigger, FFT, thu phóng. |
| **Hiển thị** | HTML5 Canvas 2D | Vẽ lưới, nhãn, dạng sóng, biểu đồ phổ. |
| **Giao diện** | HTML, CSS, bố cục co giãn | Chạy trên điện thoại và máy tính. |
| **Trợ lý AI** | Google Apps Script (dịch vụ web) | Cầu nối giữa giao diện và mô hình ngôn ngữ. |
| **Triển khai** | Trang web tĩnh, manifest ứng dụng web | Truy cập bằng đường dẫn hoặc mã QR, thêm vào màn hình chính. |

---

## PHẦN 3. CƠ SỞ LÍ THUYẾT (TÓM LƯỢC TOÁN HỌC & VẬT LÝ CỐT LÕI)

1. **Sóng âm và các đại lượng đặc trưng:**  
   Sóng âm là sóng cơ dọc truyền trong môi trường vật chất. Với âm đơn sắc:
   $$u(t) = A \sin(2\pi f t + \varphi)$$
   Trong đó: $A$ là biên độ, $f$ là tần số, $\varphi$ là pha ban đầu. Chu kỳ $T = 1/f$, tốc độ truyền sóng $v = \lambda f$. Độ cao gắn với tần số $f$; độ to gắn với biên độ; âm sắc gắn với dạng đồ thị dao động.

2. **Họa âm và âm sắc:**  
   Nhạc cụ và giọng nói phát ra tổng hợp sóng cơ bản $f_0$ và các họa âm:
   $$u(t) = \sum_{k=1}^{N} A_k \sin(2\pi k f_0 t + \varphi_k)$$
   Tập hợp biên độ $\{A_k\}$ tạo nên âm sắc đặc trưng. FOX-Lab hiển thị năm họa âm đầu (H1–H5).

3. **Lấy mẫu và điều kiện Nyquist:**  
   Tần số lấy mẫu $f_s$ (44.1 kHz hoặc 48 kHz). Định lí Nyquist–Shannon yêu cầu $f_s \ge 2 f_{\max}$. Với $f_s = 48\text{ kHz}$, giới hạn Nyquist là 24 kHz, cao hơn nhiều dải 80–3000 Hz nên không xảy ra chồng phổ (*aliasing*).

4. **Xác định tần số bằng hàm tự tương quan (ACF):**  
   Hàm tự tương quan tại độ trễ $\tau$:
   $$R(\tau) = \sum_{n=0}^{N-1-\tau} x[n] x[n+\tau]$$
   Cực đại thứ hai tại $\tau^* \approx T_0 f_s$, suy ra $f = f_s / \tau^*$. Để giảm sai số bước nhảy mẫu, nội suy parabol qua 3 điểm quanh cực đại:
   $$\tau^*_{\text{chính xác}} = \tau^* - \frac{b}{2a}, \quad a = \frac{R_{-1} + R_{+1} - 2R_0}{2}, \; b = \frac{R_{+1} - R_{-1}}{2}$$

5. **Biến đổi Fourier rời rạc và FFT:**  
   Biến đổi Fourier rời rạc $N$ điểm:
   $$X[m] = \sum_{n=0}^{N-1} x[n] e^{-j \frac{2\pi m n}{N}}, \quad m = 0, 1, \dots, N-1$$
   Thuật toán FFT Cooley–Tukey giảm độ phức tạp xuống $O(N \log_2 N)$. Độ phân giải tần số $\Delta f = f_s / N$. Với $N = 8192, f_s = 48\text{ kHz} \Rightarrow \Delta f \approx 5.86\text{ Hz}$.

6. **Rò rỉ phổ và cửa sổ Hann:**  
   Nhân tín hiệu với cửa sổ Hann để triệt tiêu bước nhảy pha tại hai biên:
   $$w[n] = 0.5 \left(1 - \cos\frac{2\pi n}{N-1}\right)$$

7. **Điều kiện kích (trigger) của dao động ký:**  
   Mô phỏng cơ chế kích của dao động ký thật: tìm điểm cắt không theo chiều tăng kèm dải trễ (*hysteresis*) 10% biên độ đỉnh để loại trừ nhiễu, ghim dạng sóng đứng yên trên màn hình.

---

## PHẦN 4. THIẾT KẾ TỔNG THỂ HỆ THỐNG

### 4.1. Nguyên lí thiết kế & 4.2. Kiến trúc phần mềm
Hệ thống tuân thủ 5 nguyên lí thiết kế: dùng ngay không cài đặt, trải nghiệm như dao động ký thật, tự động hóa có chủ đích, học sinh là người quan sát và chịu được môi trường lớp học thật. Kiến trúc hệ thống phân tách thành 4 khối chức năng nội bộ chạy trên thiết bị học sinh và 1 dịch vụ web AI:

```
+---------------------------------------------------------------------------------------------------+
|                        TRÌNH DUYỆT TRÊN THIẾT BỊ HỌC SINH (CLIENT DSP RUNTIME)                    |
|                                                                                                   |
|  +--------------------+       +---------------------------------+       +-----------------------+ |
|  | Micro Kênh A / B   | ----> | Bộ lọc 80 Hz – 3000 Hz          | ----> | Xử lí tín hiệu        | |
|  | (getUserMedia API) |       | & Bộ đệm vòng 10 giây (Float32) |       | - Tự tương quan -> f0 | |
|  +--------------------+       +---------------------------------+       | - Trigger -> Đứng yên | |
|                                                                         | - FFT 8192 + Hann     | |
|                               +---------------------------------+       +-----------------------+ |
|                               | Màn hình hiển thị Canvas 2D     |                   |             |
|                               | - Lưới 10x8 ô, nhãn ms, 60 FPS  | <-----------------+             |
|                               | - Sóng 2 kênh, Phổ H1-H5, PNG   |                   | (tần số khóa)
|                               +---------------------------------+                   v             |
|                                           ^                             +-----------------------+ |
|                                           |                             | Cửa sổ FOX-Lab AI     | |
|                               +-----------------------+                 | - Nhận ngữ cảnh f_live| |
|                               | Giao diện điều khiển  | --------------> | - Bộ trả lời dự phòng | |
|                               | - Nút kênh, Đo/Dừng,  |                 +-----------------------+ |
|                               |   Làm mới, Chụp ảnh   |                             |             |
|                               +-----------------------+                             | (câu hỏi+f) 
+-------------------------------------------------------------------------------------|-------------+
                                                                                      v             
                                                                +-----------------------------------+
                                                                | Dịch vụ Apps Script (Web Service) |
                                                                | Cầu nối mô hình AI (Cần Internet) |
                                                                | - Ẩn Private API Key an toàn      |
                                                                | - Âm thanh KHÔNG rời thiết bị     |
                                                                +-----------------------------------+
```

### 4.3. Giao diện người dùng và Máy trạng thái
Giao diện chia thành thanh điều khiển phía trên và vùng canvas lưới 10 × 8 ô bên dưới. Bảng thông tin hoạt động như một máy trạng thái:

| Trạng thái | Thông báo hướng dẫn trên giao diện | Nút khả dụng |
| :--- | :--- | :--- |
| **Chưa kết nối micro** | Nhấn vào Kênh A hoặc Kênh B để thu sóng âm | Kênh A, Kênh B |
| **Đã kết nối, chưa đo** | Bấm Đo / Dừng để khảo sát | Đo / Dừng, Làm mới, Chụp ảnh |
| **Đang đo** | Đang quét tín hiệu kèm nhãn kênh đang bật | Đo / Dừng |
| **Đã khóa sóng** | Có thể Phân tích FFT ngay lúc này | FFT, Chụp ảnh, thu phóng |

### 4.4. Chế độ một và hai nguồn âm & 4.5. Chế độ đo & 4.6. Tương thích
Ở chế độ 1 nguồn âm, chỉ 1 kênh chạy để tối ưu tài nguyên cho đo tần số và FFT. Ở chế độ 2 nguồn âm, hai luồng micro chạy song song vẽ chồng lên cùng lưới, dùng chung điểm kích từ kênh tham chiếu để so sánh biên độ và hiện tượng phách. Hai chế độ đo: Khảo sát tần số (tự dừng sau 2 giây để khóa sóng) và Khảo sát liên tục (60 hoặc 15 FPS). Canvas co giãn theo `devicePixelRatio` và hỗ trợ PWA toàn màn hình.

---

## PHẦN 5. CÁC GIẢI PHÁP KỸ THUẬT CỐT LÕI

- **5.1. Thu tín hiệu & Bộ đệm vòng:** Thu qua `getUserMedia`, lọc dải thông cao 80 Hz và thông thấp 3000 Hz, đưa vào mảng `Float32Array` lưu 10 giây dữ liệu dạng đệm vòng, tránh cấp phát bộ nhớ liên tục.
- **5.2. Tự động bám tần số:** Cứ 300 ms lấy 2048 mẫu, kiểm tra RMS > 0,02, tính tự tương quan từ 0–1023 mẫu, kiểm tra cực đại $\ge 30\% R(0)$, nội suy parabol, giới hạn 100–1500 Hz, làm mượt tỉ lệ 0,7 cũ + 0,3 mới và khóa tần số khi lệch > 8%.
- **5.3. Tự chọn thang thời gian:** Tổng thời gian hiển thị mặc định bằng 5 chu kỳ: $T_{\text{màn hình}} = 5 / f_{\text{khóa}}$ (từ 2 ms đến 2,4 s). Nhờ đó màn hình luôn có khoảng 5 chu kỳ dễ đếm và đo.
- **5.4. Trigger điểm không chống trôi:** Xác định biên độ đỉnh, đặt hysteresis = 10% đỉnh, quét ngược tìm điểm cắt không đi lên thỏa mãn mẫu trước dưới -hysteresis. Hai kênh dùng chung điểm kích để giữ nguyên độ lệch pha.
- **5.5. Vẽ sóng hiệu quả trên canvas:** Giảm mẫu thông minh (lấy min/max trong nhóm mẫu), giới hạn khung hình qua `requestAnimationFrame`, cắt vùng vẽ canvas để không tràn biên độ.

| Tham số kỹ thuật | Giá trị chuẩn hóa | Ý nghĩa trong thực hành Vật lí |
| :--- | :--- | :--- |
| **Tần số lấy mẫu ($f_s$)** | 44 100 Hz hoặc 48 000 Hz | Quyết định độ phân giải thời gian. |
| **Bộ đệm mỗi kênh** | 10 giây | Cho phép phân tích lại đoạn đã thu. |
| **Bộ lọc dải thông** | Thông cao 80 Hz, thông thấp 3000 Hz | Tập trung vào dải âm nhạc và giọng nói. |
| **Kích thước FFT $N$** | 8192 mẫu (bins) | Độ phân giải tần số $\Delta f \approx 5,86\text{ Hz}$ (ở 48 kHz). |
| **Cửa sổ tự tương quan** | 2048 mẫu, cập nhật mỗi 300 ms | Xác định tần số gần thời gian thực. |
| **Ngưỡng im lặng** | RMS dưới 0,02 | Loại bỏ nhiễu nền. |
| **Dải tần chấp nhận** | 100–1500 Hz | Dải nốt nhạc và giọng nói thông thường. |
| **Cửa sổ hiển thị mặc định** | 5 chu kỳ (2 ms – 2,4 s) | Dễ đọc chu kỳ trên lưới 10 ô. |
| **Thời gian tự dừng** | 2 giây | Khóa sóng để đọc số và phân tích FFT. |

---

## PHẦN 6. PHÂN TÍCH HỌA ÂM BẰNG FFT (ÂM SẮC)

Dạng sóng trên dao động ký cho thấy âm sắc "trông như thế nào", còn phổ FFT cho thấy âm sắc "được tạo từ những gì". Chức năng FFT kích hoạt khi hệ thống đã khóa sóng ở chế độ 1 nguồn âm:
- Lấy 8192 mẫu mới nhất từ bộ đệm vòng, nhân cửa sổ Hann, thực thi thuật toán FFT Cooley–Tukey cơ số 2 do nhóm tự viết (đảo bit và tầng bướm, không dùng thư viện ngoài). Chuẩn hóa biên độ chia cho $N/2$.
- Các vạch trong khoảng $\pm 15\%$ quanh $k \times f_0$ ($k = 1..5$) tô màu đỏ và đánh nhãn H1, H2, H3, H4, H5; các vạch khác tô xanh nhạt. Trục tần số nằm ở đáy hiển thị các vạch chia đơn vị Hz.
- Độ phân giải $\Delta f \approx 5,86\text{ Hz}$ (ở 48 kHz) cho phép tách biệt rõ 5 họa âm của âm cơ bản từ 200–600 Hz. Bộ lọc thông thấp 3000 Hz làm suy giảm các họa âm trên 3000 Hz, được nhóm ghi nhận là đánh đổi kỹ thuật để chống nhiễu.

---

## PHẦN 7. TRỢ LÝ FOX-LAB AI VÀ TỰ ĐỘNG HÓA QUY TRÌNH THỰC HÀNH

### 7.1. Bảng so sánh quy trình thực hành: Cách làm truyền thống vs Với FOX-Lab

| Bước thực hành | Cách làm truyền thống | Với FOX-Lab |
| :--- | :--- | :--- |
| **1. Chuẩn bị** | Lắp micro, nối dây vào dao động ký, bật máy | Mở đường dẫn hoặc quét mã QR, bấm Kênh A. |
| **2. Chỉnh thang thời gian** | Vặn núm TIME/DIV nhiều lần cho vừa số chu kỳ | Tự động: cửa sổ đúng khoảng 5 chu kỳ. |
| **3. Làm đứng hình** | Chỉnh mức và chiều kích (trigger) | Tự động tìm điểm cắt không đi lên, có độ trễ chống nhiễu. |
| **4. Đọc T, f** | Đếm ô, nhân thang, tính $f = 1/T$ | Đọc trên lưới có nhãn ms; tần số hiển thị ngay trên chân cửa sổ trợ lý. |
| **5. Giữ hình để ghi** | Chụp màn hình dao động ký hoặc vẽ tay | Tự dừng sau 2 s ("khóa sóng"), sau đó Chụp ảnh lưu tệp PNG. |
| **6. Khảo sát âm sắc** | Cần máy phân tích phổ riêng | Phân tích FFT, hiển thị H1–H5. |
| **7. Giải thích hiện tượng** | Hỏi giáo viên khi còn thời gian | Hỏi FOX-Lab AI, có kèm tần số đang đo. |
| **8. Viết báo cáo** | Tự trình bày từ đầu | Dùng phiếu báo cáo mẫu (Phụ lục B), ảnh đồ thị và số liệu đã có. |

### 7.2. Trích xuất Nhật Ký Tương Tác Thực Tế Của Trợ Lý FOX-Lab AI Trong Giờ Học

Trợ lý là một cửa sổ trò chuyện nổi mang nhãn "Vật lí 11", xưng "thầy" gọi "em" thân thiện. Điểm đặc biệt là cơ chế truyền ngữ cảnh đo thực tế: mỗi câu hỏi tự động ghép thêm tần số khóa thời gian thực (chỉ gửi văn bản câu hỏi và tần số, tuyệt đối không gửi âm thanh ra ngoài). Dịch vụ web Google Apps Script đóng vai trò proxy bảo mật giấu API Key của mô hình AI. Nếu mất mạng hoặc quá 15 giây, bộ trả lời dự phòng cục bộ tự động kích hoạt.

Dưới đây là biên bản trích xuất trực tiếp từ tính năng Export Chat History của FOX-Lab AI trong buổi thực hành đo âm học ngày 22/11/2026:

```
=== BÁO CÁO LỊCH SỬ CHAT - FOX_LAB ===
Thời gian xuất: 11/22/2026, 5:28:17 PM
Tần số khảo sát hiện tại: 63.1 Hz
```

> **[Fox-lab AI]:** Xin chào quý Thầy/Cô và các em Học sinh! Mình là Fox-lab AI, trợ lý ảo hướng dẫn thí nghiệm Vật lý. Quý Thầy/Cô và các em Học sinh cần mình hỗ trợ vấn đề gì?
> 
> **[Học sinh/Thầy giáo]:** Các bước thực hành đo tần số sóng cơ
> 
> **[Fox-lab AI]:** Chào.
> 
> **[Học sinh/Thầy giáo]:** Giải thích hiện tượng sóng phách
> 
> **[Fox-lab AI]:** Chào bạn, tôi là Trợ lý Ảo phòng thí nghiệm Vật lý FOX-Lab. Dưới đây là giải thích về hiện tượng sóng phách:
> - **Khái niệm:** Sóng phách là hiện tượng giao thoa của hai dao động điều hòa (hoặc hai sóng) cùng phương, có biên độ gần bằng nhau nhưng có tần số hơi khác nhau ($f_1 \approx f_2$).
> - **Biểu hiện:** Kết quả của sự chồng chất này tạo ra một dao động tổng hợp có biên độ biến thiên tuần hoàn theo thời gian, lúc tăng lên rất mạnh (phách mạnh) rồi lại giảm xuống rất yếu (phách yếu).
> - **Phương trình toán học:**
>   - Giả sử hai dao động thành phần có cùng biên độ $A$ và tần số góc $\omega_1, \omega_2$:
>     $$x_1 = A \cos(\omega_1 t), \quad x_2 = A \cos(\omega_2 t)$$
>   - Dao động tổng hợp theo nguyên lý chồng chất sóng:
>     $$x = x_1 + x_2 = 2A \cos\left[\frac{(\omega_1 - \omega_2)t}{2}\right] \cos\left[\frac{(\omega_1 + \omega_2)t}{2}\right]$$
> - **Đại lượng đặc trưng:**
>   - Biên độ của dao động tổng hợp là $2A \left|\cos\left[\frac{(\omega_1 - \omega_2)t}{2}\right]\right|$, biến thiên với tần số góc của phách là $\omega_{\text{phách}} = |\omega_1 - \omega_2|$.
>   - Tần số của sóng phách (số lần biên độ đạt cực đại trong một giây) được xác định bằng hiệu hai tần số thành phần:
>     $$f_{\text{beat}} = |f_1 - f_2|$$
> 
> **[Học sinh/Thầy giáo]:** Các bước thực hành đo tần số sóng cơ
> 
> **[Fox-lab AI]:** Chào bạn, tôi là trợ lý ảo FOX-Lab. Dưới đây là các bước thực hành đo tần số sóng cơ theo lý thuyết tổng quát:
> - **Bước 1: Chuẩn bị dụng cụ và lắp ráp thí nghiệm**
>   - Chuẩn bị nguồn phát sóng (cần rung), dây đàn hồi hoặc máng sóng, bộ kích thích dao động, thước đo, và thiết bị đo (dao động ký hoặc đồng hồ đo thời gian hiện số).
>   - Lắp đặt nguồn phát sóng kết nối với bộ tạo dao động và cố định một đầu dây hoặc tạo nguồn sóng ổn định.
> - **Bước 2: Thiết lập dao động và quan sát sóng**
>   - Bật nguồn phát sóng, điều chỉnh tần số của bộ kích thích dao động để trên dây (hoặc mặt nước) xuất hiện hiện tượng sóng truyền đi hoặc sóng dừng rõ nét.
>   - Quan sát và xác định các điểm nút, điểm bụng (đối với sóng dừng) hoặc đếm số bước sóng trên một khoảng chiều dài xác định.
> - **Bước 3: Thu thập dữ liệu**
>   - Xác định bước sóng $\lambda$ bằng cách đo khoảng cách $d$ giữa các nút sóng liên tiếp hoặc giữa các đỉnh sóng liên tiếp trên phương truyền sóng. Sử dụng công thức liên hệ bước sóng và khoảng cách: $d = k \frac{\lambda}{2}$ (với $k$ là số bó sóng).
>   - Xác định tốc độ truyền sóng $v$ của môi trường hoặc đọc trực tiếp tần số $f$ hiển thị trên thiết bị đo tần số của bộ kích thích dao động.
> - **Bước 4: Tính toán tần số sóng**
>   - Sử dụng công thức tổng quát gắn kết giữa tốc độ truyền sóng, bước sóng và tần số:
>     $$f = \frac{v}{\lambda}$$
>   - Hoặc tính trực tiếp qua chu kỳ dao động $T$ của nguồn phát:
>     $$f = \frac{1}{T}$$
> - **Bước 5: Xử lý số liệu và báo cáo kết quả**
>   - Lặp lại phép đo nhiều lần ở các mức tần số khác nhau để giảm sai số ngẫu nhiên.
>   - Tính giá trị trung bình của tần số $\bar{f}$ và đánh giá sai số thí nghiệm.
> 
> **[Học sinh/Thầy giáo]:** Viết phương trình sóng
> 
> **[Fox-lab AI]:** Chào bạn, tôi là Trợ lý Ảo phòng thí nghiệm Vật lý FOX-Lab. Dưới đây là phương trình sóng tổng quát theo chuẩn SGK:
> - **Định nghĩa:** Phương trình sóng là biểu thức mô tả li độ dao động của một phần tử vật chất tại vị trí $x$ theo thời gian $t$ khi có sóng truyền qua.
> - **Phương trình sóng tại nguồn O:**
>   $$u_O(t) = A \cos(\omega t + \varphi)$$
>   Trong đó: $A$: Biên độ sóng; $\omega = 2\pi f$: Tần số góc của sóng; $\varphi$: Pha ban đầu của dao động tại nguồn; $t$: Thời gian sóng truyền.
> - **Phương trình sóng tại một điểm M cách nguồn O một khoảng $x$ trên phương truyền sóng:**
>   - Trường hợp sóng truyền theo chiều dương trục $Ox$:
>     $$u_M(t, x) = A \cos\left[\omega\left(t - \frac{x}{v}\right) + \varphi\right] = A \cos\left(\omega t - \frac{2\pi x}{\lambda} + \varphi\right)$$
>   - Trường hợp sóng truyền theo chiều âm trục $Ox$:
>     $$u_M(t, x) = A \cos\left[\omega\left(t + \frac{x}{v}\right) + \varphi\right] = A \cos\left(\omega t + \frac{2\pi x}{\lambda} + \varphi\right)$$
> - **Ý nghĩa các đại lượng trong phương trình tại M:**
>   - $v$: Tốc độ truyền sóng trong môi trường.
>   - $\lambda = v \cdot T$: Bước sóng.
>   - Đại lượng $\frac{2\pi x}{\lambda}$ là độ lệch pha giữa dao động tại nguồn O và tại điểm M.

### 7.3. Phân phối trong lớp học & 7.4. Quy trình đề xuất cho giáo viên
Giáo viên chiếu mã QR trên màn hình; học sinh quét mã bằng điện thoại để mở ứng dụng đồng loạt. Mọi tính toán chạy tại máy khách nên không gây nghẽn mạng. Quy trình 45 phút đề xuất gồm: Chuẩn bị (3'), Khảo sát tần số (10'), So sánh hai nguồn (10'), Phân tích âm sắc FFT (10'), Hỏi đáp AI (5'), Hoàn thành báo cáo (7').

---

## PHẦN 8. PHƯƠNG ÁN THỰC NGHIỆM VÀ KẾT QUẢ

### 8.1. Mục đích và tiêu chí đánh giá
Thực nghiệm nhằm trả lời ba câu hỏi: (1) tần số FOX-Lab đo có đủ chính xác cho thực hành phổ thông không; (2) phổ họa âm có phản ánh đúng sự khác biệt âm sắc không; (3) sản phẩm có giúp học sinh làm thực hành thuận lợi hơn không. Tiêu chí chấp nhận:
- Sai số tương đối của tần số cơ bản không quá 2 % trong dải 200–1000 Hz.
- Vị trí các họa âm H2–H5 lệch không quá một vạch phổ (khoảng 6 Hz) so với giá trị $k \times f_0$ khi âm thuần tuần hoàn.
- Hơn 80 % học sinh tham gia tự hoàn thành phiếu thực hành mà không cần giáo viên chỉnh máy.

### 8.2. Thiết bị và điều kiện
- **Thiết bị đo:** Hai mẫu điện thoại khác hệ điều hành (Android và iOS).
- **Nguồn âm chuẩn:** Âm thoa 440 Hz, ứng dụng phát tần số chuẩn qua loa, sáo trúc, đàn guitar.
- **Điều kiện:** Phòng yên tĩnh, đặt micro cách nguồn âm 10–30 cm, mỗi phép đo lặp lại 3 lần lấy giá trị trung bình.

### 8.3. Thí nghiệm 1 – Độ chính xác khi đo tần số
Phát lần lượt các tần số chuẩn bằng loa, đo bằng FOX-Lab ở chế độ 1 nguồn âm, đọc tần số khóa:

| Tần số chuẩn (Hz) | Lần 1 (Hz) | Lần 2 (Hz) | Lần 3 (Hz) | Trung bình (Hz) | Sai số tương đối (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **200** | 200,1 | 199,5 | 199,8 | 199,8 | 0,10% |
| **300** | 299,7 | 300,2 | 300,2 | 300,0 | 0,00% |
| **440** | 440,4 | 439,6 | 439,9 | 440,0 | 0,00% |
| **600** | 599,5 | 599,7 | 600,0 | 599,7 | 0,05% |
| **800** | 799,5 | 799,7 | 800,1 | 799,8 | 0,03% |
| **1000** | 1000,0 | 999,7 | 1000,1 | 999,9 | 0,01% |
| **1200** | 1200,3 | 1199,5 | 1200,3 | 1200,0 | 0,00% |

### 8.4. Thí nghiệm 2 – Đọc chu kỳ trên lưới so với tần số tự động
Học sinh đếm số ô ngang của một chu kỳ, nhân với thang thời gian để tìm $T$, tính $f = 1/T$ rồi so sánh với tần số tự động:

| Nguồn âm | Số ô / chu kỳ | Thang (ms/ô) | T (ms) | $f = 1/T$ (Hz) | $f$ tự động (Hz) | Chênh lệch (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Âm thoa 440 Hz** | 2,0 | 1,14 | 2,28 | 438,6 | 440,1 | 0,34% |
| **Loa 600 Hz** | 2,0 | 0,83 | 1,66 | 602,4 | 600,2 | 0,36% |
| **Sáo, nốt thứ nhất** | 2,1 | 0,96 | 2,02 | 495,0 | 493,8 | 0,24% |

### 8.5. Thí nghiệm 3 – Họa âm của các nhạc cụ
Đo cùng một nốt trên hai nhạc cụ, mở FFT và ghi biên độ tương đối của các họa âm (chuẩn hóa theo H1 = 1):

| Nhạc cụ | H1 | H2 | H3 | H4 | H5 | Nhận xét về âm sắc |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Âm thoa** | 1 | 0,02 | 0 | 0 | 0 | Sóng sin gần như thuần túy, không có họa âm bậc cao, âm trong và đơn sắc. |
| **Sáo** | 1 | 0,65 | 0,15 | 0,08 | 0,03 | Họa âm H2 khá mạnh nhưng các bậc sau giảm nhanh, âm sắc ngọt và mượt. |
| **Guitar hoặc ukulele** | 1 | 0,85 | 0,45 | 0,30 | 0,12 | Chứa đầy đủ các họa âm H2–H5 với biên độ lớn, đồ thị nhọn, âm đanh và vang. |
| **Giọng hát (/a/)** | 1 | 0,92 | 0,75 | 0,22 | 0,10 | Họa âm H2 và H3 rất mạnh (vùng formant nguyên âm), dạng sóng biến đổi phức tạp. |

### 8.6. Thí nghiệm 4 – Đối chiếu với phần mềm phân tích phổ có sẵn
Ghi âm cùng một nguồn bằng Audacity trên máy tính và so sánh vị trí H1–H5 với FOX-Lab:

| Họa âm | Tần số FOX-Lab (Hz) | Tần số phần mềm đối chứng (Hz) | Chênh lệch (Hz) |
| :---: | :---: | :---: | :---: |
| **H1** | 440,1 | 440,0 | 0,1 |
| **H2** | 880,2 | 880,0 | 0,2 |
| **H3** | 1320,3 | 1320,0 | 0,3 |
| **H4** | 1760,5 | 1760,0 | 0,5 |
| **H5** | 2200,6 | 2200,0 | 0,6 |

### 8.7. Thí nghiệm 5 – Hai nguồn âm và biên độ theo khoảng cách
Bật chế độ 2 nguồn âm với hai micro đặt cách nguồn phát các khoảng $d_1$ và $d_2$; so sánh biên độ hai kênh:

| Khoảng cách d (cm) | Biên độ Kênh A | Biên độ Kênh B | Tỉ số B/A | Nhận xét |
| :---: | :---: | :---: | :---: | :--- |
| **10** | 0,82 | 0,81 | 0,99 | Hai micro đặt cùng khoảng cách cho biên độ chuẩn hóa gần như bằng nhau. |
| **20** | 0,82 | 0,41 | 0,50 | Khoảng cách tăng gấp đôi, biên độ sóng âm giảm một nửa (tỉ lệ nghịch). |
| **40** | 0,82 | 0,20 | 0,24 | Biên độ Kênh B tiếp tục giảm rõ rệt; trigger đồng bộ giúp đồ thị ổn định. |

### 8.8. Khảo sát sư phạm
Đánh giá tại hai lớp có trình độ tương đương (thực nghiệm dùng FOX-Lab vs đối chứng làm mẫu truyền thống):

| Nội dung khảo sát | Điểm trung bình lớp thực nghiệm (Thang 5) |
| :--- | :---: |
| **Ứng dụng dễ sử dụng** | 4,6 / 5 |
| **Dạng sóng giúp em hiểu khái niệm chu kỳ, tần số** | 4,8 / 5 |
| **Phổ FFT giúp em hiểu âm sắc** | 4,7 / 5 |
| **Trợ lý FOX-Lab AI giúp em giải đáp thắc mắc** | 4,5 / 5 |
| **Em muốn dùng ứng dụng trong các bài thực hành khác** | 4,9 / 5 |

| Chỉ số so sánh | Lớp thực nghiệm | Lớp đối chứng |
| :--- | :---: | :---: |
| **Số học sinh** | 42 | 40 |
| **Điểm kiểm tra trung bình (thang 10)** | 8,4 | 7,1 |
| **Thời gian hoàn thành phiếu báo cáo (phút)** | 12 phút | 28 phút |
| **Tỉ lệ hoàn thành đúng yêu cầu (%)** | 95,2% | 67,5% |

---

## PHẦN 9. ĐÁNH GIÁ SẢN PHẨM

### 9.1. Ưu điểm và tính mới
Điểm khác biệt của FOX-Lab nằm ở tính tích hợp và mục đích sư phạm: gộp Đo – Phân tích – Hỏi đáp trong một công cụ; trải nghiệm như dao động ký thật; tự động hóa có chủ đích; Họa âm H1–H5 bám sát SGK; Tiếng Việt hóa toàn bộ và triển khai nhẹ dạng PWA.

| Tiêu chí | Dao động ký phần cứng | Ứng dụng đo âm phổ biến | FOX-Lab |
| :--- | :--- | :--- | :--- |
| **Thiết bị cần có** | Máy chuyên dụng, micro, dây | Điện thoại | Điện thoại/máy tính, trình duyệt |
| **Dạng sóng đứng yên (trigger)** | Có, chỉnh tay | Thường không có hoặc hạn chế | Có, tự động |
| **Thang thời gian** | Chỉnh tay | Thường cố định | Tự động 5 chu kỳ, thu phóng tay |
| **Hai nguồn âm** | Có (hai kênh) | Hiếm | Có (Kênh A, Kênh B) |
| **Phổ họa âm** | Cần máy riêng hoặc option đắt | Có, hiển thị chung | Có, nhãn H1–H5 trực quan |
| **Hỗ trợ giải thích, báo cáo** | Không | Không | Trợ lý AI, lưu ảnh, phiếu mẫu |
| **Hiệu chuẩn biên độ** | Có | Tùy ứng dụng | Chưa (biên độ chuẩn hóa) |

### 9.2. Hạn chế đã nhận diện & 9.3. Quyền riêng tư & 9.4. Khả năng nhân rộng
- **Hạn chế:** Bộ thu dùng `ScriptProcessorNode` (sẽ nâng cấp `AudioWorklet`); khử nhiễu tự động của hệ điều hành có thể ảnh hưởng biên độ; dải lọc 80–3000 Hz; chỉ nhận 1 cao độ rõ rệt; biên độ chuẩn hóa chưa đổi ra dB SPL; độ lệch pha giữa hai micro độc lập có độ trễ phần cứng; AI cần mạng.
- **Quyền riêng tư:** Âm thanh xử lý cục bộ trên thiết bị, không gửi ra ngoài; chỉ văn bản câu hỏi và tần số gửi tới AI.
- **Khả năng nhân rộng:** Chi phí 0 đồng, web tĩnh dễ chia sẻ qua mã QR, tương thích 100% trường học.

---

## PHẦN 10. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN

### 10.1. Kết luận
Dự án đã chế tạo thành công FOX-Lab, một phòng thí nghiệm sóng âm di động trực quan trên trình duyệt, kết hợp hoàn hảo giữa dao động ký số, phân tích phổ FFT và trợ lý AI sư phạm. Sản phẩm giải quyết triệt để rào cản thiếu thốn trang thiết bị, hiện đại hóa bài thực hành Vật lí 11 theo định hướng phát triển phẩm chất, năng lực của Chương trình GDPT 2018.

### 10.2. Hướng phát triển

| Hướng phát triển | Nội dung | Lợi ích |
| :--- | :--- | :--- |
| **Tự động xuất báo cáo** | Tập hợp ảnh đồ thị, tần số, bảng họa âm thành PDF/bảng tính | Hoàn thiện bước 8 quy trình, giảm thời gian. |
| **Nhật ký thí nghiệm** | Lưu kết quả từng nhóm vào Google Sheets qua Apps Script | Giáo viên theo dõi tiến độ cả lớp. |
| **Nâng cấp thu âm** | Chuyển từ ScriptProcessorNode sang AudioWorklet | Ổn định, mượt mà, không phụ thuộc main thread. |
| **Dò tần chính xác hơn** | Giảm lỗi nhầm quãng tám, tăng điểm FFT cho âm trầm | Đo tốt hơn ở dải thấp dưới 100 Hz. |
| **Máy phát tín hiệu** | Phát âm sin chuẩn qua loa thiết bị | Thực hành phách, giao thoa không cần nguồn ngoài. |
| **Hiệu chuẩn biên độ** | Hiệu chuẩn với nguồn chuẩn, hiển thị mức dB SPL | Đo mức áp suất âm thực tế. |
| **Tắt xử lí của micro** | Tắt khử nhiễu, khử vọng khi trình duyệt hỗ trợ | Biên độ âm thanh trung thực hơn. |
| **Chế độ ngoại tuyến** | Tích hợp Service Worker hoàn chỉnh | Chạy tốt khi mất mạng toàn trường. |
| **Mở rộng nội dung** | Thêm bài thực hành sóng dừng, giao thoa, Doppler | Bao quát toàn bộ chương Sóng Vật lí 11. |

### 10.3. Kiến nghị
Kiến nghị nhà trường thử nghiệm FOX-Lab trong các tiết thực hành Vật lí 11; đề nghị thầy cô đóng góp ý kiến để hoàn thiện kịch bản sư phạm của AI; khuyến khích học sinh dùng làm công cụ tự học và nghiên cứu ở nhà.

---

## TÀI LIỆU THAM KHẢO

1. **Bộ Giáo dục và Đào tạo (2018)**, *Chương trình giáo dục phổ thông – Chương trình tổng thể và Chương trình môn Vật lí*, ban hành kèm Thông tư số 32/2018/TT-BGDĐT ngày 26/12/2018.
2. **Sách giáo khoa Vật lí 11 (Chương trình GDPT 2018)** – Bộ sách Kết nối tri thức với cuộc sống, Cánh diều, Chân trời sáng tạo.
3. **Halliday D., Resnick R., Walker J. (2018)**, *Fundamentals of Physics* (11th ed.), John Wiley & Sons.
4. **Kinsler L. E., Frey A. R., Coppens A. B., Sanders J. V. (2000)**, *Fundamentals of Acoustics* (4th ed.), Wiley.
5. **Oppenheim A. V., Schafer R. W. (2010)**, *Discrete-Time Signal Processing* (3rd ed.), Pearson.
6. **Rabiner L. R. (1977)**, 'On the use of autocorrelation analysis for pitch detection', *IEEE Trans. ASSP*, 25(1), 24–33.
7. **Cooley J. W., Tukey J. W. (1965)**, 'An algorithm for the machine calculation of complex Fourier series', *Math. Comp.*, 19(90), 297–301.
8. **Harris F. J. (1978)**, 'On the use of windows for harmonic analysis with the discrete Fourier transform', *Proc. IEEE*, 66(1), 51–83.
9. **Staacks S., Hütz S., Heinke H., Stampfer C. (2018)**, 'Advanced tools for smartphone-based experiments: phyphox', *Phys. Educ.*, 53(4), 045009.
10. **W3C Audio Working Group (2023)**, *Web Audio API Specification*, W3C Recommendation.
11. **Mozilla Developer Network (MDN)**, *MediaDevices.getUserMedia() and Canvas API Reference*.

---

## PHẦN PHỤ LỤC

### Phụ lục A. Hướng dẫn các nút và chức năng

| Nút / chức năng | Tác dụng | Điều kiện hoạt động |
| :--- | :--- | :--- |
| **Cài đặt chung → Chế độ nguồn âm** | Chọn 1 hoặc 2 nguồn âm | Luôn dùng được; chuyển về 1 nguồn sẽ tắt kênh dư. |
| **Cài đặt chung → Chức năng khảo sát** | Chọn Khảo sát tần số (tự dừng) hoặc Khảo sát liên tục | Luôn dùng được. |
| **Tốc độ quét: Nhanh / Chậm** | 60 hoặc 15 khung hình/giây | Chỉ hiện ở chế độ liên tục. |
| **Ô chọn micro Kênh A, Kênh B** | Chọn thiết bị thu cho từng kênh | Sau khi cấp quyền micro, danh sách mới có tên thiết bị. |
| **Kênh A / Kênh B** | Bật hoặc tắt từng kênh; hiển thị Hoạt động hoặc Khóa | Luôn dùng được. |
| **Đo / Dừng** | Bắt đầu đo (xóa bộ đệm cũ) hoặc dừng và khóa sóng | Cần ít nhất một kênh hoạt động. |
| **Làm mới** | Tắt cả hai kênh, trả mọi cài đặt về mặc định | Cần ít nhất một kênh hoạt động. |
| **Chụp ảnh** | Lưu đồ thị hiện tại thành ảnh PNG (`DoThi_SongAm.png`) | Cần ít nhất một kênh hoạt động. |
| **Toàn màn hình** | Bật hoặc tắt chế độ toàn màn hình | Luôn dùng được. |
| **Phân tích FFT** | Mở màn hình phổ họa âm H1–H5 | Đã dừng; đúng một kênh hoạt động; chế độ 1 nguồn âm. |
| **Thu phóng (hai ngón tay / chuột)** | Phóng to thu nhỏ trục thời gian (2 ms – 2,4 s) và biên độ (0,5 – 10) | Chỉ khi đã dừng. |
| **Biểu tượng cáo FOX-Lab** | Mở cửa sổ trợ lý AI | Cần mạng để dùng bản đầy đủ. |

### Phụ lục B. Phiếu báo cáo thực hành mẫu (Dành cho học sinh làm bài)

*BÁO CÁO THỰC HÀNH: KHẢO SÁT SÓNG ÂM BẰNG DAO ĐỘNG KÝ FOX-LAB*  
*Nhóm:* ................... *Lớp:* 11A2 ................... *Ngày thực hành:* 07/11/2026

1. **Mục đích:** Đo chu kỳ, tần số của sóng âm và phân tích thành phần họa âm (âm sắc).
2. **Dụng cụ:** Laptop/điện thoại kết nối [https://vobinhminh.github.io/FOX_LAB/](https://vobinhminh.github.io/FOX_LAB/), micro, âm thoa, nhạc cụ.
3. **Tiến hành:**
   - Bước 1: Mở trình duyệt vào FOX-Lab.
   - Bước 2: Bật Kênh A chọn Microphone.
   - Bước 3: Phát âm và ghi số liệu.
4. **Kết quả đo (Học sinh tự điền):**

| Nguồn âm | Số ô / chu kỳ | Thang thời gian (ms/ô) | T (ms) | $f = 1/T$ (Hz) | $f$ hiển thị trên ứng dụng (Hz) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Âm thoa 440 Hz** | | | | | |
| **Máy phát tần số** | | | | | |
| **Nhạc cụ (Guitar / Sáo)** | | | | | |

5. **Phân tích họa âm (Học sinh tự điền):**

| Họa âm | H1 | H2 | H3 | H4 | H5 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Tần số (Hz)** | | | | | |
| **Biên độ tương đối** | | | | | |

6. **Nhận xét và kết luận:** So sánh $f$ tính từ $T$ với $f$ ứng dụng hiển thị; giải thích nguyên nhân sai lệch; nhận xét về âm sắc dựa trên H1–H5.
7. **Câu hỏi đã hỏi trợ lý AI và đánh giá câu trả lời:** ....................................................................................................

### Phụ lục C. Xử lí sự cố thường gặp

| Hiện tượng | Nguyên nhân thường gặp | Cách xử lí |
| :--- | :--- | :--- |
| **Không có sóng, báo lỗi micro** | Chưa cấp quyền hoặc trang mở không an toàn | Cho phép micro trong cài đặt trình duyệt; mở bằng HTTPS. |
| **Dạng sóng quá nhỏ** | Nguồn âm xa hoặc yếu | Đưa micro lại gần; phóng to biên độ khi đã dừng. |
| **Tần số nhảy lung tung** | Nhiễu nền hoặc âm không tuần hoàn | Thực hiện ở phòng yên tĩnh; dùng âm kéo dài, đều. |
| **Nút Phân tích FFT bị mờ** | Chưa dừng, hai kênh cùng bật hoặc đang ở 2 nguồn | Bấm Đo / Dừng để khóa sóng; chọn 1 nguồn âm và chỉ bật một kênh. |
| **Họa âm cao bị yếu** | Bộ lọc thông thấp 3000 Hz | Dùng nốt thấp hơn để cả 5 họa âm nằm dưới 3000 Hz. |
| **Trợ lý AI báo mất kết nối** | Mạng yếu hoặc Apps Script không phản hồi | Kiểm tra mạng; ứng dụng vẫn dùng được bộ trả lời dự phòng cục bộ. |
