import streamlit as st
import whisper
import google.generativeai as genai
import os
import tempfile

st.set_page_config(page_title="وەرگێڕی زیرەکی کوردی", layout="centered")
st.title("📝 سیستەمی زیرەکی داڕشتنەوەی کوردی")

# لێرە API Key-ەکەت دابنێ
API_KEY = "کۆدەکەی_خۆت_لێرە_دابنێ"
genai.configure(api_key=API_KEY)
model_gemini = genai.GenerativeModel('gemini-1.5-flash-latest')

uploaded_file = st.file_uploader("فایلی ڤیدیۆ یان دەنگ باربکە", type=["mp4", "mxf", "mp3", "wav"])

if uploaded_file is not None:
    with st.spinner("⏳ خەریکی ناسینەوەی دەنگ و داڕشتنەوەم..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        # Whisper
        model = whisper.load_model("base")
        result = model.transcribe(tmp_path)
        
        # Gemini
        prompt = f"ئەم دەقە کوردییە بە جوانترین شێوە و بە خاڵبەندیی وردەوە دابڕێژەوە: {result['text']}"
        response = model_gemini.generate_content(prompt)
        
        st.success("✅ تەواو بوو!")
        st.subheader("📜 ئەنجامی کۆتایی:")
        st.write(response.text)
        st.download_button("دابەزاندنی دەقەکە", response.text, file_name="kurdish_report.txt")
        os.remove(tmp_path)
