import streamlit as st
import google.generativeai as genai
import time
import os

# ڕێکخستنی لاپەڕە
st.set_page_config(page_title="سەنتەری زیرەکی کوردی", layout="wide")
st.title("🎙️ سیستەمی هەمەگیری وەرگێڕان و داڕشتنەوە")

# لێرە کلیلەکەی خۆت دابنێ
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# دروستکردنی تابەکان (Tabs)
tab1, tab2, tab3 = st.tabs(["📁 بارکردنی فایل (ڤیدیۆ/دەنگ)", "✍️ داڕشتنەوەی ڕاپۆرت و هەواڵ", "🎤 قسەکردن (Voice to Text)"])

# ١. بەشی بارکردنی فایلە گەورەکان
with tab1:
    st.subheader("بارکردنی فایلی میدیا")
    file = st.file_uploader("ڤیدیۆ یان دەنگ باربکە (تا ٢ گێگا)", type=["mp4", "mxf", "mp3", "wav", "m4a"])
    if file and st.button("پڕۆسێس بکە"):
        with st.spinner("⏳ گوگل خەریکی شیکردنەوەی فایلەکەیە..."):
            with open("temp", "wb") as f: f.write(file.getbuffer())
            g_file = genai.upload_file(path="temp")
            while g_file.state.name == "PROCESSING":
                time.sleep(2)
                g_file = genai.get_file(g_file.name)
            
            prompt = "ئەم فایلە بکە بە دەق و بە شێوازێکی هەواڵیی کوردی زۆر جوان دایبڕێژەوە."
            response = model.generate_content([g_file, prompt])
            st.success("تەواو بوو!")
            st.write(response.text)
            os.remove("temp")

# ٢. بەشی داڕشتنەوەی دەق و ڕاپۆرت
with tab2:
    st.subheader("داڕشتنەوەی دەقی ئامادە")
    raw_text = st.text_area("ڕاپۆرت یان دەقەکە لێرە دابنێ:", height=300, placeholder="بۆ نموونە: هەواڵێکی خاو لێرە دابنێ...")
    style = st.selectbox("شێوازی داڕشتنەوە هەڵبژێرە:", ["هەواڵیی فەرمی", "ئەدەبی و پاراو", "کورتکراوە"])
    
    if st.button("ئەنجام بدە"):
        if raw_text:
            with st.spinner("⏳ خەریکی داڕشتنەوەم..."):
                prompt = f"تۆ پسپۆڕی زمانی کوردییت. ئەم دەقە بە شێوازی ({style}) و بە خاڵبەندی وردەوە دابڕێژەوە:\n\n{raw_text}"
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
        else:
            st.warning("تکایە دەقێک بنووسە.")

# ٣. بەشی قسەکردن (بە بەکارهێنانی مۆدێلی Gemini وەک گوێگر)
with tab3:
    st.subheader("تۆمارکردنی دەنگی ڕاستەوخۆ")
    audio_value = st.audio_input("لێرە کلیک بکە و قسە بکە (بۆ ئەوەی ببێتە دەق):")
    if audio_value:
        with st.spinner("⏳ گوێم لێیە، ئێستا دەیکەم بە دەق..."):
            with open("voice_temp.wav", "wb") as f: f.write(audio_value.read())
            g_voice = genai.upload_file(path="voice_temp.wav")
            while g_voice.state.name == "PROCESSING":
                time.sleep(1)
                g_voice = genai.get_file(g_voice.name)
            
            response = model.generate_content([g_voice, "تکایە هەرچی لەم دەنگەدا وتراوە ڕێک وەک خۆی بینوسەرەوە بەبێ زیاد و کەم."])
            st.info("ئەوەی وتت:")
            st.write(response.text)
            os.remove("voice_temp.wav")
