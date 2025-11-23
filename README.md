Trợ lý Phân Loại Cảm Xúc Tiếng Việt (PhoBERT)

Dự án xây dựng ứng dụng phân loại cảm xúc tiếng Việt sử dụng mô hình PhoBERT và giao diện Streamlit.
Ứng dụng cho phép người dùng nhập văn bản, mô hình sẽ phân tích và trả về cảm xúc:
- tích cực
- tiêu cực
- trung tính

Lịch sử phân loại được lưu trong SQLite, người dùng có thể xem lại hoặc xuất file lịch sử.

1. Giới thiệu

Dự án nhằm xây dựng một trợ lý web có khả năng phân loại cảm xúc văn bản tiếng Việt dựa trên mô hình pre-trained PhoBERT.
Người dùng chỉ cần nhập câu cần phân tích, mô hình sẽ trả về kết quả ngay lập tức.

2. Yêu cầu hệ thống
- Python 3.9 – 3.11
- Streamlit
- Transformers (HuggingFace)
- Torch
- sqlite3 

3. Các thư viện cần thiết
| Thư viện         | Mục đích                                                       |
| ---------------- | -------------------------------------------------------------- |
| **transformers** | Tải mô hình PhoBERT, tokenizer, tạo pipeline phân loại cảm xúc |
| **torch**        | Nền tảng deep learning để chạy mô hình PhoBERT                 |
| **streamlit**    | Xây dựng giao diện web cho người dùng                          |
| **pandas**       | Thực hiện xuát file CSV                                        |
| **sqlite3**      | Lưu trữ lịch sử phân loại cảm xúc                              |
| **re (regex)**   | Làm sạch dữ liệu, loại ký tự không hợp lệ                      |

4. Mô tả các file trong dự án
🔹 app.py
    - Điều khiển giao diện người dùng bằng Streamlit.
    - Cho người dùng nhập văn bản, bấm nút phân loại.
    - Gọi hàm xử lý từ models.py.
    - Lưu kết quả vào database qua db.py.
    - Hiển thị lịch sử phân loại.

🔹 models.py
    - Chứa toàn bộ xử lý mô hình:
    - Tải PhoBERT 
    - Tạo pipeline sentiment-analysis
    - Hàm preprocess_text():
        Chuẩn hóa Unicode
        Xử lý viết tắt (ko, cx, dc, mik…)
        Xử lý từ không dấu (buon → buồn)
        Làm sạch ký tự
    - Hàm classify_text():
        Truyền văn bản vào pipeline
        Map nhãn POS/NEG/NEU → tiếng Việt

🔹 db.py
    - Xử lý cơ sở dữ liệu SQLite:
        init_db() → tạo database và bảng
        insert_sentiment() → thêm bản ghi lịch sử
        get_latest_sentiments() → lấy 50 bản ghi gần nhất   
        clear_sentiments() → xóa lịch sử

🔹 sentiments.db
    - File cơ sở dữ liệu SQLite tự sinh khi chạy app.

5. Cài đặt và chạy ứng dụng
Bước 1: Clone dự án
    git clone <link_repo>
    cd project

Bước 2: Cài đặt thư viện
    pip install -r requirements.txt

Bước 3: Chạy ứng dụng
    python -m streamlit run app.py

    Ứng dụng sẽ mở tại:
    http://localhost:8501

6. Đánh giá hiệu suất bằng Test Case
| STT | Câu nhập                   | Kết quả mô hình | Kỳ vọng    | Đúng/Sai |
| --- | -------------------------- | --------------- | ---------- | -------- |
| 1   | Phim này rất hay, xem cuốn | Tích cực        | Tích cực   | ✔        |
| 2   | Tệ thật sự, mất thời gian  | Tiêu cực        | Tiêu cực   | ✔        |
| 3   | Cũng được, không quá tệ    | Tích cực        | Tích cực   | ✔        |
| 4   | Ko vui tí nào              | Tiêu cực        | Tiêu cực   | ✔        |
| 5   | Ban rat tuyet voi          | Tích cực        | Tích cực   | ✔        |
| 6   | Tôi buồn ghê luôn...       | Tiêu cực        | Tiêu cực   | ✔        |
| 7   | Bình thường, không ý kiến  | Tiêu cực        | Trung tính | ✘        |
| 8   | Trời xấu quá trời          | Tiêu cực        | Tiêu cực   | ✔        |
| 9   | Tuyệt vời ông mặt trời     | Tích cực        | Tích cực   | ✔        |
| 10  | Không biết nữa, hơi chán   | Tiêu cực        | Tiêu cực   | ✔        |

7. Kết luận và hướng phát triển
Kết luận
    Hệ thống đã xây dựng thành công trợ lý phân loại cảm xúc tiếng Việt sử dụng PhoBERT.
    Độ chính xác cao (~90%), tốc độ xử lý nhanh, giao diện thân thiện.
    Đáp ứng đầy đủ mục tiêu đồ án.

Hướng phát triển
    Thêm khả năng phân tích đa nhãn (giận dữ, vui vẻ, lo lắng…)
    Nâng cấp tiền xử lý để hiểu tốt hơn ngôn ngữ mạng và emoji.
    Tối ưu mô hình bằng quantization để chạy nhanh hơn.
    Tích hợp API để sử dụng trên ứng dụng mobile.
    Xây dựng dashboard phân tích xu hướng cảm xúc theo thời gian.