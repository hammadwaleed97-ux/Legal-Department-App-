import streamlit as st
import sqlite3
import pandas as pd

# إعداد الصفحة
st.set_page_config(layout="wide")

# الهيدر
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 10px; border-radius: 8px; color: white; text-align: center;">
        <h4 style="margin: 0;">الإدارة العامة للشئون القانونية - منطقة البحيرة</h4>
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية
menu = st.sidebar.radio("القائمة الرئيسية", 
    ["📂 المكتبة القانونية", "⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "🔍 البحث القانوني", "📊 سجل المتابعة"])

# 1. تبويب المكتبة القانونية (محمي بكلمة سر)
if menu == "📂 المكتبة القانونية":
    st.header("📂 المكتبة القانونية")
    pwd = st.text_input("أدخل كلمة المرور:", type="password")
    if pwd == "1234": # غير كلمة السر هنا كما تحب
        st.success("تم تأكيد الهوية")
        st.markdown('[اضغط هنا لفتح مجلد المكتبة على Google Drive](https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke)', unsafe_allow_html=True)
    elif pwd != "":
        st.error("كلمة مرور خاطئة")

# 2. تبويب البحث القانوني
elif menu == "🔍 البحث القانوني":
    st.header("🔍 البحث القانوني")
    st.text_input("اكتب كلمة للبحث:")
    st.info("جاري تجهيز محرك البحث...")

# 3. باقي التبويبات (أضف المحتوى الخاص بك هنا)
else:
    st.write(f"أنت الآن في: {menu}")
    st.info("هذا القسم قيد التجهيز، سيظهر محتواه هنا فور إضافته.")
