import sqlite3
from datetime import datetime

DB_PATH = "sentiments.db"

# Khởi tạo db
def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS sentiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Thêm 1 bản ghi vào bảng
def insert_sentiment(text: str, sentiment: str, path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    iso_time = datetime.utcnow().isoformat()  
    c.execute(
        "INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)",
        (text, sentiment, iso_time)
    )
    conn.commit()
    conn.close()

# Lấy lịch sử phân loại (50 bản ghi gần nhất)
def get_latest_sentiments(limit: int = 50, path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute(
        "SELECT id, text, sentiment, timestamp FROM sentiments ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = c.fetchall()
    conn.close()
    return rows

# Xóa lịch sử phân loại
def clear_sentiments(path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute("DELETE FROM sentiments")
    conn.commit()
    conn.close()
