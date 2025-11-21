import streamlit as st
from deep_translator import GoogleTranslator
from textblob import TextBlob

st.set_page_config(page_title="Multilingual Support System", layout="wide")
st.title("🌍 Multilingual Customer Support System (No API Key)")

# History
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("📝 Enter customer message (any language):")
user_msg = st.text_area("Message:", height=150)

col1, col2 = st.columns(2)
with col1:
    translate_btn = st.button("🔤 Translate")
with col2:
    reset_btn = st.button("♻️ Clear History")

def detect_language(text):
    detector = GoogleTranslator(source="auto", target="en")
    result = detector.translate(text)
    lang = detector.source
    return lang

def translate_to_english(text):
    return GoogleTranslator(source="auto", target="en").translate(text)

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "Positive"
    elif polarity < -0.2:
        return "Negative"
    else:
        return "Neutral"

def support_reply(text):
    return f"""
Thank you for reaching out. We have received your message:

\"{text}\"

Our support team is reviewing your request and will respond soon.
If you have more details, feel free to share them.
"""

if translate_btn:
    if not user_msg.strip():
        st.warning("Please enter a message first.")
    else:
        lang = detect_language(user_msg)
        translation = translate_to_english(user_msg)
        sentiment = analyze_sentiment(translation)
        reply = support_reply(translation)

        st.session_state.history.insert(0, {
            "original": user_msg,
            "language": lang,
            "translated": translation,
            "sentiment": sentiment,
            "reply": reply
        })

if reset_btn:
    st.session_state.history = []

st.subheader("📚 Translation History")

if len(st.session_state.history) == 0:
    st.info("No translations yet.")
else:
    for i, item in enumerate(st.session_state.history):
        with st.expander(f"Query #{i+1}"):
            st.write("### 🌐 Original Message:")
            st.write(item["original"])

            st.write("### 🔍 Detected Language:")
            st.write(item["language"])

            st.write("### 🔤 Translation to English:")
            st.success(item["translated"])

            st.write("### 😊 Sentiment:")
            st.info(item["sentiment"])

            st.write("### 💬 Support Reply:")
            st.write(item["reply"])
