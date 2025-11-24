from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import logging
import unicodedata
import re

# Tải mô hình PhoBERT
def load_phobert():

    model_name = "wonrax/phobert-base-vietnamese-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    pipe = pipeline(
        "sentiment-analysis",
        model=model,
        tokenizer=tokenizer
    )
    return pipe


# Phân loại text
def classify_text(pipe, text: str):

    # Tiền xử lý text
    text = preprocess_text(text)
    result = pipe(text)[0]
    
    # Đổi tên nhãn thành tiếng Việt
    mapping = {
        "POS": "tích cực",
        "NEG": "tiêu cực",
        "NEU": "trung tính"
    }

    sentiment = mapping.get(result["label"])
    return {
        "text": text,
        "sentiment": sentiment
    }


# Tiền xử lý
def preprocess_text(text: str) -> str:

    # ===== TỪ ĐIỂN KHÔNG DẤU  =====
    NO_DIACRITIC_MAP = {
        "buon": "buồn",
        "vui": "vui",
        "ghet": "ghét",
        "rat": "rất",
        "toi": "tôi",
        "yeu": "yêu",
        "khong": "không",
        "nhung": "nhưng",
        "thich": "thích",
        "xau": "xấu",
        "tot": "tốt",
        "do": "dở",
        "hom": "hôm",
    }

    # ===== TỪ ĐIỂN VIẾT TẮT =====
    ABBREVIATIONS = {
        "ko": "không",
        "k": "không",
        "kh": "không",
        "cx": "cũng",
        "dc": "được",
        "đc": "được",
        "vs": "với",
        "ms": "mới",
        "mik": "mình",
        "mk": "mật khẩu",
        "tl": "trả lời",
        "ib": "inbox",
        "ad": "admin",
        "mn": "mọi người",
        "t": "tôi",
        "bh": "bây giờ",
        "ns": "nói",
    }
   # Chuẩn hóa Unicode 
    text = unicodedata.normalize("NFC", text.strip())

    # Loại bỏ ký tự lạ 
    text = re.sub(r"[^a-zA-Z0-9À-ỹà-ỹ\s.,!?]", " ", text)

    # Tách từ 
    tokens = text.split()

    # Xử lý viết tắt và không dấu 
    processed_tokens = []
    for tk in tokens:
        # xử lý viết tắt
        if tk in ABBREVIATIONS:
            processed_tokens.append(ABBREVIATIONS[tk])
            continue
        
        # xử lý không dấu
        if tk in NO_DIACRITIC_MAP:
            processed_tokens.append(NO_DIACRITIC_MAP[tk])
            continue

        processed_tokens.append(tk)

    # Ghép lại câu 
    text = " ".join(processed_tokens)

    # Chuẩn hóa khoảng trắng 
    text = re.sub(r"\s+", " ", text)


    return text
