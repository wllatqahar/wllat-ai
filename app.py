import streamlit as st
import whisper
import google.generativeai as genai
import os
import tempfile

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="وەرگێڕی خێرای کوردی", layout="wide")
st.title("🚀 سیستەمی خێرای ناسینەوە و داڕشتنەوەی کوردی")

# ڕێکخستنی Gemini
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ" 
genai.configure(api_key=API_KEY)
model_gemini = genai.GenerativeModel('gemini-1.5-flash-latest')

# مۆدێلی Whisper (بۆ خێرایی لێرە دامان ناوە)
@st.cache_resource
def load_whisper():
    return whisper.load_model("base") # مۆدێلی base هاوسەنگییە لە نێوان خێرایی و وردی

whisper_model = load_whisper()

tab1, tab2 = st.tabs(["📁 بارکردنی فایلی گەورە (١ گێگا)", "✍️ داڕشتنەوەی دەق"])

with tab1:
    uploaded_file = st.file_uploader("فایلی ڤیدیۆ یان دەنگ (Max 1GB)", type=["mp4", "mxf", "mp3", "wav"])
    if uploaded_file:
        st.info(f"قەبارەی فایل: {uploaded_file.size / (1024*1024):.2f} MB")
        if st.button("🚀 دەستپێکردنی خێرا"):
            with st.spinner("⏳ خەریکی پڕۆسێسکردنی خێرام..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # ناسینەوەی دەنگ بە خێرایی
                result = whisper_model.transcribe(tmp_path, fp16=False)
                
                # ناردن بۆ Gemini
                prompt = f"ئەم دەقە بە خێرایی بە کوردییەکی زۆر پاراو و شاز دابڕێژەوە:\n\n{result['text']}"
                response = model_gemini.generate_content(prompt)
                
                st.subheader("📜 ئەنجام:")
                st.write(response.text)
                st.download_button("دابەزاندنی ئەنجام", response.text, file_name="fast_report.txt")
                os.remove(tmp_path)

with tab2:
    user_text = st.text_area("دەقەکە لێرە دابنێ:", height=300)
    if st.button("✨ داڕشتنەوەی خێرا"):
        if user_text:
            response = model_gemini.generate_content(f"ئەم دەقە بە شێوازێکی فەرمی و جوان دابڕێژەوە: {user_text}")
            st.write(response.text)
