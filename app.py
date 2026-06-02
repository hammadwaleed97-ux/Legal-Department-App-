import streamlit as st
import sqlite3

# إعداد الصفحة وتنسيق الألوان
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# تصميم الهيدر (أزرق داكن + لوجو)
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 20px; border-radius: 10px; color: white; text-align: center;">
        <h1 style="margin: 0; color: white;">⚖️ الإدارة العامة للشئون القانونية</h1>
        <p style="margin: 5px 0 0 0;">ديوان عام منطقة البحيرة</p>
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية (الأيقونات مفعّلة)
menu = st.sidebar.radio("القائمة الرئيسية", 
    ["📂 المكتبة القانونية", "⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "🔍 البحث القانوني", "📊 سجل المتابعة"])

# 1. المكتبة (باسورد خاص)
if menu == "📂 المكتبة القانونية":
    st.header("📂 المكتبة القانونية")
    pwd = st.text_input("أدخل كلمة المرور الخاصة بك:", type="password")
    if pwd == "WALID2026": # كلمة السر الخاصة بك
        st.success("تم تأكيد الهوية - يمكنك الدخول للمكتبة")
        st.markdown('[🔗 اضغط هنا لفتح مجلد المكتبة](https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke)', unsafe_allow_html=True)
    elif pwd != "":
        st.error("كلمة المرور غير صحيحة")

#
