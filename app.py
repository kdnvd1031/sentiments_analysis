import streamlit as st
from db import init_db, insert_sentiment, get_latest_sentiments, clear_sentiments
from models import classify_text, load_phobert

# Khởi tạo database
init_db()

st.set_page_config(page_title="Trợ lý phân loại cảm xúc tiếng Việt", layout="centered")
st.title("📝 Trợ lý phân loại cảm xúc Tiếng Việt")
st.markdown("Nhập văn bản tiếng Việt dưới đây và bấm **Phân loại**. Lịch sử sẽ được lưu vào SQLite.")

# Load pipeline
pipeline_info = None
try: 
    pipeline_info = load_phobert()
except Exception as e:
    st.error(f"Lỗi tải mô hình: {e}")

# Input text
text = st.text_area("Nhập nội dung cần phân loại cảm xúc", height=180)

col1, col2 = st.columns(2)
with col1:
    # Nút phân loại cảm xúc
    if st.button("Phân loại"):
        if not text or len(text.strip().split()) < 4:  # Kiểm tra input
            st.toast("Câu không hợp lệ, thử lại")
        else:
            try:
                result = classify_text(pipeline_info, text)  # Phân loại
                st.success(f"**Kết quả:** {result['sentiment']}")
                insert_sentiment(result["text"], result["sentiment"])
            except Exception as e:
                # Nếu pipeline lỗi, tokenizer lỗi, model lỗi,...
                st.toast("Có lỗi xảy ra, thử lại")

with col2:
    if st.button("Xóa toàn bộ lịch sử"): # Nút xóa lịch sử phân loại
        clear_sentiments()
        st.info("Đã xóa toàn bộ lịch sử!")

# Hiển thị lịch sử
st.markdown("---")
st.subheader("📜 Lịch sử phân loại (50 bản ghi gần nhất)")

rows = get_latest_sentiments(limit=50)

if rows:
    import pandas as pd
    df = pd.DataFrame(rows, columns=["ID", "Text", "Sentiment", "Timestamp"])
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "Tải CSV lịch sử",
        data=csv,
        file_name="sentiment_history.csv",
        mime="text/csv"
    )
else:
    st.write("Chưa có bản ghi nào.")
