# Hướng dẫn thiết lập Backend AI Chatbot (Google Apps Script)

Backend của trợ lý AI Fox-Lab hoạt động dựa trên Google Apps Script (GAS) làm proxy kết nối an toàn với Google Gemini API.

## Cách triển khai Google Apps Script:

1. Truy cập [Google Apps Script](https://script.google.com/) và tạo một dự án mới (Đặt tên: `FoxLab-AI-Backend`).
2. Sao chép toàn bộ mã trong file [gas-foxlab-ai.js](gas-foxlab-ai.js) và dán vào trình soạn thảo `Code.gs`.
3. **Cấu hình API Key bảo mật (Khuyên dùng)**:
   - Vào biểu tượng bánh răng **Project Settings** (Cài đặt dự án) ở thanh bên trái.
   - Cuộn xuống mục **Script Properties** (Thuộc tính tập lệnh) -> Bấm **Add script property**.
   - **Property**: `GEMINI_API_KEYS`
   - **Value**: Nhập các API key Gemini của bạn, phân tách bằng dấu phẩy nếu có nhiều key (Ví dụ: `AIzaSy...,AIzaSy...`).
   - Bấm **Save script properties**.
4. **Triển khai ứng dụng Web (Deploy as Web App)**:
   - Bấm nút **Deploy** (Triển khai) -> Chọn **New deployment** (Triển khai mới).
   - Chọn loại: **Web app**.
   - Cấu hình:
     - **Execute as**: `Me` (Tôi)
     - **Who has access**: `Anyone` (Bất kỳ ai)
   - Bấm **Deploy**.
   - Cấp quyền cho script khi Google yêu cầu xác nhận.
5. **Cập nhật URL vào Frontend**:
   - Sau khi Deploy, Google sẽ cung cấp **Web app URL** có dạng:
     `https://script.google.com/macros/s/AKfycb.../exec`
   - Phần ID sau `/s/` và trước `/exec` chính là `CHAT_GAS_ID`.
   - Mở file `script.js` ở dòng 87 và cập nhật ID này:
     ```javascript
     const CHAT_GAS_ID = "AKfycb...";
     ```
