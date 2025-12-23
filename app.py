import streamlit as st
import google.generativeai as genai
import time
import os

# ڕێکخستنی لاپەڕە بۆ خێرایی و سادەیی
st.set_page_config(page_title="سیستەمی خێرای کوردی", layout="centered")
st.title("🚀 وەرگێڕ و داڕێژەری زیرەکی خێرا")

# ڕێکخستنی کلیل (API KEY)
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# دروستکردنی تابەکان
tab1, tab2, tab3 = st.tabs(["✍️ داڕشتنەوەی دەق", "📁 فایل (ڤیدیۆ/دەنگ)", "🎤 قسەکردن"])

# ١. بەشی دەق (زۆر خێرا و بە Streaming)
with tab1:
    user_text = st.text_area("دەقەکە لێرە دابنێ:", height=250)
    if st.button("🚀 داڕشتنەوەی خێرا"):
        if user_text:
            output_place = st.empty()
            full_text = ""
            # ناردن بە شێوازی Stream بۆ ئەوەی یەکسەر دەست بکات بە نووسین
            responses = model.generate_content(f"ئەم دەقە بە شێوازێکی فەرمی و جوان دابڕێژەوە: {user_text}", stream=True)
            for chunk in responses:
                full_text += chunk.text
                output_place.markdown(full_text + "▌")
            output_place.markdown(full_text)
        else:
            st.warning("تکایە دەق بنووسە.")

# ٢. بەشی فایل (فایلی گەورە و MXF)
with tab2:
    file = st.file_uploader("بارکردنی فایل (تا ٢ گێگا)", type=["mp4", "mxf", "mp3", "wav"])
    if file and st.button("پڕۆسێس"):
        with st.spinner("⏳ ناردن بۆ گوگل..."):
            with open("tmp_f", "wb") as f: f.write(file.getbuffer())
            g_file = genai.upload_file(path="tmp_f")
            while g_file.state.name == "PROCESSING":
                time.sleep(2)
                g_file = genai.get_file(g_file.name)
            
            # وەڵامدانەوەی فایلەکەش بە شێوازی Stream
            output_f = st.empty()
            f_text = ""
            res = model.generate_content([g_file, "ئەمە بکە بە دەق و دایبڕێژەوە."], stream=True)
            for chunk in res:
                f_text += chunk.text
                output_f.markdown(f_text + "▌")
            output_f.markdown(f_text)
            os.remove("tmp_f")

# ٣. بەشی قسەکردن (Voice to Text)
with tab3:
    audio = st.audio_input("قسە بکە (بۆ نوسینەوە):")
    if audio:
        with st.spinner("⏳ گوێم لێیە..."):
            with open("tmp_v.wav", "wb") as f: f.write(audio.read())
            gv = genai.upload_file(path="tmp_v.wav")
            res_v = model.generate_content([gv, "ئەم دەنگە بنوسەرەوە"])
            st.success("ئەوەی وتت:")
            st.write(res_v.text)
            os.remove("tmp_v.wav")
