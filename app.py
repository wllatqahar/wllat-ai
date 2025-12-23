import streamlit as st
import google.generativeai as genai

# ڕێکخستنی لاپەڕە بۆ سووکی و خێرایی
st.set_page_config(page_title="داڕێژەری خێرا", layout="centered")

# ستایلێکی سادە بۆ ڕاست بۆ چەپ
st.markdown("""<style> .stTextArea textarea {direction: rtl; text-align: right;} .stMarkdown {direction: rtl; text-align: right;} </style>""", unsafe_allow_html=True)

# کلیلەکە لێرە دابنێ
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ"
genai.configure(api_key=API_KEY)

# بەکارهێنانی مۆدێلی Flash کە بۆ "خێرایی" دروست کراوە
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("⚡ داڕێژەری کوردی خێرا")

# بەشی تێکست (گرنگترین بەش بۆ تۆ)
user_input = st.text_area("دەقەکە لێرە دابنێ:", height=250)

if st.button("🚀 دەستبەجێ دایبڕێژەوە"):
    if user_input:
        # دروستکردنی شوێنی بەتاڵ بۆ وەڵامەکە بۆ ئەوەی یەکسەر دەربکەوێت
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # پرۆمپتی کورت و خێرا
            prompt = f"ئەم دەقە بە کوردییەکی پاراو و بە خاڵبەندییەوە دابڕێژەوە: {user_input}"
            
            try:
                # بەکارهێنانی stream=True واتا پیت بە پیت وەڵام بدەرەوە بێ وەستان
                responses = model.generate_content(prompt, stream=True)
                
                for chunk in responses:
                    full_response += chunk.text
                    response_placeholder.markdown(full_response)
            except Exception as e:
                st.error("کێشەیەک لە پەیوەندی دروست بوو، تکایە جارێکی تر کلیک بکەرەوە.")
    else:
        st.warning("تکایە دەقێک بنووسە.")

st.divider()
st.caption("ئەم سیستمە ڕاستەوخۆ بە گوگلەوە بەستراوە بۆ ئەوپەڕی خێرایی.")
