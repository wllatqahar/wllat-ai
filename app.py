import streamlit as st
import google.generativeai as genai

# ڕێکخستنی لاپەڕە (بۆ ئەوپەڕی خێرایی)
st.set_page_config(page_title="داڕێژەری زیرەک", layout="centered")

# کلیلەکەت لێرە دابنێ (دڵنیا بەرەوە کە API Key ڕاستە)
API_KEY = "کلیلەکەی_خۆت_لێرە_دابنێ"
genai.configure(api_key=API_KEY)

# بەکارهێنانی مۆدێلی Flash کە خێراترینە
model = genai.GenerativeModel('gemini-1.5-flash')

st.markdown("<h2 style='text-align: center;'>✨ داڕێژەری خێرای ڕاپۆرت و هەواڵ</h2>", unsafe_allow_html=True)

# خانەی نووسین
user_input = st.text_area("دەقەکە لێرە دابنێ:", height=250)

if st.button("🚀 ئێستا دایبڕێژەوە"):
    if user_input:
        # بەکارهێنانی سیستەمی "پیت بە پیت" (Streaming) بۆ ئەوەی نەوەستێت
        res_area = st.empty()
        full_res = ""
        
        try:
            # ناردنی دەقەکە بە شێوازێکی سادە
            prompt = f"ئەم دەقە کوردییە بە پاراوترین شێوە و بە خاڵبەندی ورد دابڕێژەوە:\n\n{user_input}"
            
            # ئەنجام بە شێوەی ستریم (ئەمە وادەکات سێرڤەرەکە چاوەڕێ نەکات و یەکسەر دەست پێ بکات)
            response = model.generate_content(prompt, stream=True)
            
            for chunk in response:
                full_res += chunk.text
                res_area.markdown(full_res + "▌") # نیشاندانی کارەکە لە کاتی نووسیندا
            
            res_area.markdown(full_res) # نیشاندانی ئەنجامی کۆتایی
            
        except Exception as e:
            st.error("⚠️ سێرڤەر کەمێک خاوە، تکایە جارێکی تر کلیک بکەرەوە.")
    else:
        st.warning("تکایە سەرەتا دەقەکە بنووسە.")

st.markdown("---")
st.caption("تێبینی: ئەگەر زۆر خاو بوو، یەکجار لاپەڕەکە Refresh بکەرەوە.")
