/**
 * =========================================================================
 * FOX-LAB AI ASSISTANT - GOOGLE APPS SCRIPT BACKEND PROXY
 * Phiên bản chuẩn hóa bảo mật cho GitHub Repository
 * =========================================================================
 * Hướng dẫn cấu hình an toàn:
 * 1. Vào Apps Script -> Project Settings (Cài đặt dự án) -> Script Properties (Thuộc tính tập lệnh).
 * 2. Thêm thuộc tính: GEMINI_API_KEYS với giá trị là danh sách key cách nhau bởi dấu phẩy:
 *    Ví dụ: key1,key2,key3
 * 3. Hoặc nếu chạy thử nội bộ cá nhân, bạn có thể điền tạm vào mảng DEFAULT_KEYS bên dưới.
 */

// ==========================================
// 1. CẤU HÌNH API KEYS
// ==========================================
function getApiKeys() {
  try {
    var props = PropertiesService.getScriptProperties().getProperty("GEMINI_API_KEYS");
    if (props) {
      return props.split(",").map(function(k) { return k.trim(); }).filter(Boolean);
    }
  } catch (e) {
    Logger.log("Không thể đọc Script Properties: " + e.toString());
  }

  // Danh sách key dự phòng (chỉ dùng nội bộ - KHÔNG commit key nhạy cảm lên Git công khai)
  var DEFAULT_KEYS = [
    // "YOUR_GEMINI_API_KEY_1",
    // "YOUR_GEMINI_API_KEY_2"
  ];
  return DEFAULT_KEYS;
}

// ==========================================
// 2. HÀM GỌI GEMINI AI
// ==========================================
function callAI(message, role, imageBase64) {
  var apiKeys = getApiKeys();
  if (!apiKeys || apiKeys.length === 0) {
    return "Lỗi cấu hình: Chưa tìm thấy Gemini API Key. Vui lòng thiết lập Script Properties 'GEMINI_API_KEYS' trong Google Apps Script.";
  }

  var roleInstruction = (role === "teacher") 
    ? "Bạn là Chế độ Giáo viên: Cung cấp phản hồi chuyên môn sư phạm, chuẩn mực, bám sát SGK Vật lý 11 chương trình GDPT mới." 
    : "Bạn là Chế độ Học sinh (Gia sư): Giải thích ngắn gọn, súc tích, đúng trọng tâm kiến thức vật lý, TUYỆT ĐỐI KHÔNG đưa ra câu hỏi gợi mở hay câu hỏi tư duy ở cuối câu trả lời.";

  var systemPrompt = `Bạn là Trợ lý Ảo phòng thí nghiệm Vật lý FOX-Lab. 
${roleInstruction}
Quy tắc bắt buộc cho tất cả câu trả lời:
1. Trình bày nội dung rõ ràng, khoa học, sử dụng các gạch đầu dòng để phân tách ý. Bám sát câu hỏi và trả lời đầy đủ, không tự ý bỏ sót ý hỏi.
2. Trả lời trực tiếp vào vấn đề, kết thúc bằng dấu chấm câu.
3. NGUYÊN TẮC XỬ LÝ SỐ LIỆU ĐO & PHÂN LOẠI CÂU HỎI:
   - Với câu hỏi lý thuyết, định nghĩa, hiện tượng, chứng minh hoặc viết phương trình tổng quát (như phương trình sóng, sóng dừng, dao động điều hòa...): Trình bày hoàn toàn bằng công thức đại số tổng quát với các đại lượng chuẩn (A, f, omega, lambda, v, t, phi...). TUYỆT ĐỐI KHÔNG tự tiện chèn số liệu tần số đo f hoặc thông số thiết bị vào câu trả lời lý thuyết.
   - Chỉ khi nào người dùng đặt câu hỏi phân tích kết quả đo thực tế, tính toán số liệu cụ thể từ đồ thị dao động ký đang đo, VÀ có thông số đo hợp lệ được cung cấp: Lúc đó mới áp dụng số liệu đo vào tính toán.
   - Nếu không có số liệu đo hoặc thiết bị chưa bật tín hiệu, TUYỆT ĐỐI KHÔNG giả định hay bịa số liệu đo.
4. TUYỆT ĐỐI KHÔNG thêm phần 'Câu hỏi gợi mở' hoặc các câu hỏi tư duy, dẫn dắt dư thừa ở cuối câu trả lời.`;

  var partsArray = [{"text": message}];
  
  if (imageBase64 && imageBase64.indexOf("data:image/") === 0) {
    try {
      var commaIdx = imageBase64.indexOf(",");
      var mimeType = imageBase64.substring(5, commaIdx).split(";")[0];
      var base64Data = imageBase64.substring(commaIdx + 1);
      partsArray.push({
        "inline_data": {
          "mime_type": mimeType,
          "data": base64Data
        }
      });
    } catch (imgErr) {
      Logger.log("Lỗi xử lý ảnh: " + imgErr.toString());
    }
  }

  var payload = {
    "system_instruction": {
      "parts": [{"text": systemPrompt}]
    },
    "contents": [{
      "parts": partsArray
    }],
    "generationConfig": {
      "maxOutputTokens": 5000, 
      "temperature": 0.2
    },
    "safetySettings": [
      { "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE" },
      { "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE" },
      { "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE" },
      { "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE" }
    ]
  };
  
  var options = {
    "method": "post",
    "contentType": "application/json",
    "payload": JSON.stringify(payload),
    "muteHttpExceptions": true
  };

  // Vòng lặp xoay tua các key dự phòng
  for (var k = 0; k < apiKeys.length; k++) {
    var currentKey = apiKeys[k].trim();
    if (!currentKey) continue;
    
    var url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + currentKey;
    
    try {
      var response = UrlFetchApp.fetch(url, options);
      var responseCode = response.getResponseCode();
      var data = JSON.parse(response.getContentText());
      
      if (responseCode === 200 && data.candidates && data.candidates.length > 0) {
        return data.candidates[0].content.parts[0].text;
      }
    } catch (error) {
      Logger.log("Lỗi key index " + k + ": " + error.toString());
      continue;
    }
  }
  
  return "Hệ thống AI đang tạm thời quá tải hoặc hết hạn ngạch truy vấn, vui lòng bấm gửi lại sau ít phút nhé!";
}

// ==========================================
// 3. HÀM KẾT NỐI WEB PHƯƠNG THỨC GET (doGet)
// ==========================================
function doGet(e) {
  try {
    if (e && e.parameter && e.parameter.action === "chat") {
      var userMessage = e.parameter.message || "Xin chào";
      var rawFreq = e.parameter.frequency;
      var hasFreq = rawFreq && parseFloat(rawFreq) > 0;
      var role = e.parameter.role || "student";
      var roleLabel = (role === "teacher" ? "Giáo viên" : "Học sinh");
      
      var contextHeader = "[Vai trò: " + roleLabel + "]";
      if (hasFreq) {
        contextHeader += " [Thông số đo thực tế nếu cần phân tích thí nghiệm: f = " + parseFloat(rawFreq).toFixed(1) + " Hz]";
      } else {
        contextHeader += " [Chế độ: Câu hỏi lý thuyết / Nguyên lý chung - Không tự chèn số liệu đo]";
      }

      var contextMessage = contextHeader + "\n\nNội dung câu hỏi:\n" + userMessage;
      var aiResponse = callAI(contextMessage, role, null);
      
      return ContentService.createTextOutput(JSON.stringify({
        status: "success",
        reply: aiResponse
      })).setMimeType(ContentService.MimeType.JSON);
    }
    
    return ContentService.createTextOutput(JSON.stringify({status: "ready", message: "API FOX-Lab Ready!"}))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      reply: "Lỗi Server: " + err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// ==========================================
// 4. HÀM KẾT NỐI WEB PHƯƠNG THỨC POST (doPost)
// ==========================================
function doPost(e) {
  try {
    var requestData = JSON.parse(e.postData.contents);
    var userMessage = requestData.message || "Xin chào";
    var hasFreq = requestData.frequency && parseFloat(requestData.frequency) > 0;
    var role = requestData.role || "student";
    var roleLabel = (role === "teacher" ? "Giáo viên" : "Học sinh");
    var imageBase64 = requestData.imageBase64 || null;
    
    var contextHeader = "[Vai trò: " + roleLabel + "]";
    if (hasFreq) {
      contextHeader += " [Thông số đo thực tế nếu cần phân tích thí nghiệm: f = " + parseFloat(requestData.frequency).toFixed(1) + " Hz]";
    } else {
      contextHeader += " [Chế độ: Câu hỏi lý thuyết / Nguyên lý chung - Không tự chèn số liệu đo]";
    }

    // Telemetry dữ liệu phòng thí nghiệm (nếu có)
    if (requestData.labData) {
      contextHeader += "\n[Dữ liệu đo đạc chi tiết: " + JSON.stringify(requestData.labData) + "]";
    }

    var fullPrompt = contextHeader + "\n\nNội dung câu hỏi:\n" + userMessage;
    var aiResponse = callAI(fullPrompt, role, imageBase64);

    return ContentService.createTextOutput(JSON.stringify({
      status: "success",
      reply: aiResponse
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: "error",
      reply: "Lỗi xử lý yêu cầu: " + err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
