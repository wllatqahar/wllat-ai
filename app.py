import streamlit as st
import google.generativeai as genai
import os

# ڕێکخستنی لاپەڕە بۆ ئەوپەڕی خێرایی
st.set_page_config(page_title="AI خێرا", layout="centered")
st.markdown("""<style> .main {direction: rtl; text-align: right;} </style>""", unsafe_allow_html=True)

# کلیلەکەت لێرە دابنێ
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ" 
genai.configure(api_key=API_KEY)
# بەکارهێنانی مۆدێلی Flash بۆ خێرایی بێ وێنە
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("⚡ داڕێژەری خێرا و زیرەک")

tab1, tab2 = st.tabs(["✍️ داڕشتنەوەی دەق", "📁 بارکردنی فایل"])

# ١. بەشی دەق (ئەمە وەک مووشەک خێرایە)
with tab1:
    user_input = st.text_area("دەقەکە لێرە دابنێ:", height=200, placeholder="ڕاپۆرت یان هەواڵەکە لێرە دابنێ...")
    
    if st.button("🚀 ئێستا دایبڕێژەوە"):
        if user_input:
            res_box = st.empty() # شوێنی نوسینەکە
            full_res = ""
            
            # پرۆمپتێکی ورد بۆ داڕشتنەوەی شاز
            prompt = f"""تۆ پسپۆڕێکی زمانی کوردییت. ئەم دەقەی خوارەوە بە شێوازێکی یەکجار جوان، فەرمی، 
            و بە خاڵبەندییەکی وردەوە دابڕێژەوە. با زمانەکەی زۆر پاراو بێت:
            
            {user_input}"""
            
            # بەکارهێنانی stream=True بۆ خێرایی
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                full_res += chunk.text
                res_box.markdown(full_res + "▌") # نیشاندانی پیت بە پیت
            res_box.markdown(full_res)
        else:
            st.warning("تکایە دەقێک بنووسە.")

# ٢. بەشی فایل
with tab2:
    file = st.file_uploader("فایل (ڤیدیۆ/دەنگ)", type=["mp4", "mxf", "mp3", "wav"])
    if file and st.button("شیکردنەوەی خێرا"):
        with st.spinner("⏳ خەریکی خوێندنەوەم..."):
            with open("t_f", "wb") as f: f.write(file.getbuffer())
            g_file = genai.upload_file(path="t_f")
            
            # داواکردنی وەڵام بە شێوازی Stream
            res_f = model.generate_content([g_file, "ئەمە بە کوردییەکی پاراو بنوسەرەوە و دایبڕێژەوە."], stream=True)
            out_f = st.empty()
            txt_f = ""
            for chunk in res_f:
                txt_f += chunk.text
                out_f.markdown(txt_f + "▌")
            out_f.markdown(txt_f)
            os.remove("t_f")
