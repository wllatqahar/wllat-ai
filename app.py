import streamlit as st
import google.generativeai as genai

# ڕێکخستنی سەرەتایی بۆ ئەوپەڕی خێرایی
st.set_page_config(page_title="Fast Kurdish AI", layout="centered")

# کلیلەکەت لێرە دابنێ
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ"
genai.configure(api_key=API_KEY)

# بەکارهێنانی خێراترین مۆدێلی جیهان (Flash-8B)
model = genai.GenerativeModel('gemini-1.5-flash-8b')

st.markdown("<h1 style='text-align: center;'>⚡ داڕێژەری خێرای کوردی</h1>", unsafe_allow_html=True)

# خانەی نووسین
user_input = st.text_area("دەقەکە لێرە دابنێ:", height=250, help="ڕاپۆرت یان هەواڵەکە لێرە کۆپی بکە")

if st.button("🚀 دەستبەجێ چاکی بکە"):
    if user_input:
        # پیشاندانی ئەنجام بە شێوەی پیت بە پیت (Streaming)
        with st.chat_message("assistant"):
            output_placeholder = st.empty()
            full_text = ""
            
            try:
                # پرۆمپتی کورت بۆ ئەوەی مۆدێلەکە کاتی تێنەچێت
                prompt = f"وەک پسپۆڕێکی زمان، ئەم دەقە کوردییە بە پاراوی و خاڵبەندییەوە دابڕێژەوە:\n\n{user_input}"
                
                # وەڵامدانەوەی دەستبەجێ
                response = model.generate_content(prompt, stream=True)
                
                for chunk in response:
                    full_text += chunk.text
                    output_placeholder.markdown(full_text)
            except Exception as e:
                st.error("کێشەیەک لە پەیوەندی هەیە. تکایە دووبارە کلیک بکە.")
    else:
        st.warning("تکایە دەقێک بنووسە.")
