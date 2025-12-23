import streamlit as st
import google.generativeai as genai
import time
import os

st.set_page_config(page_title="وەرگێڕی خێرای گوگل", layout="wide")
st.title("🚀 وەرگێڕی زیرەکی گوگل (خێرا و بەهێز)")

# API Key
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ" 
genai.configure(api_key=API_KEY)

uploaded_file = st.file_uploader("ڤیدیۆ یان دەنگەکە لێرە دابنێ (تا ٢ گێگا)", type=["mp4", "mxf", "mp3", "wav"])

if uploaded_file:
    if st.button("✨ دەستپێکردنی خێرا"):
        with st.spinner("⏳ گوگل خەریکی خوێندنەوەی فایلەکەیە..."):
            # پاشەکەوتکردنی کاتی بۆ ناردن
            with open("temp_file", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # ناردنی فایل بۆ گوگل
            kurdish_file = genai.upload_file(path="temp_file")
            
            # چاوەڕێکردن تا گوگل فایلەکە ئامادە دەکات
            while kurdish_file.state.name == "PROCESSING":
                time.sleep(2)
                kurdish_file = genai.get_file(kurdish_file.name)

            # داواکردنی داڕشتنەوە لە Gemini
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")
            response = model.generate_content([kurdish_file, "تکایە ئەم ڤیدیۆیە یان دەنگە بگۆڕە بۆ دەق و بە کوردییەکی زۆر جوان و پاراو دایبڕێژەوە."])
            
            st.subheader("📜 ئەنجامی کۆتایی:")
            st.write(response.text)
            
            # سڕینەوەی فایلی کاتی
            genai.delete_file(kurdish_file.name)
            os.remove("temp_file")
