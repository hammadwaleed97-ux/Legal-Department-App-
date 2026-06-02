import streamlit as st
import sqlite3

# 1. إعداد الصفحة
st.set_page_config(layout="wide")

# 2. الهيدر
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 10px; border-radius: 8px; color: white; text-align: center;">
        <h4 style="margin: 0;">الإدارة العامة للشئون القانونية - منطقة البحيرة</h4>
    </div>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية
menu = st.sidebar.radio("القائمة الرئيسية", 
    ["📂 المكتبة القانونية", "⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "📊 سجل المتابعة"])

# 4. منطق العمل
if menu == "📂 المكتبة القانونية":
    st.header("📂 المكتبة القانونية")
    pwd = st.text_input("أدخل كلمة المرور:", type="password")
    if pwd == "WALID2026": 
        st.success("تم الدخول بنجاح")
        st.markdown('[اضغط هنا لفتح مجلد المكتبة](https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke)', unsafe_allow_html=True)
    elif pwd != "":
        st.error("كلمة المرور غير صحيحة")

elif menu == "⚖️ قضاء عادي":
    st.header("⚖️ قضاء عادي")
    st.write("هنا ستظهر بيانات القضاء العادي...")
    # يمكنك إضافة فورم الإدخال هنا

elif menu == "📊 سجل المتابعة":
    st.header("📊 سجل المتابعة")
    # يمكنك استدعاء البيانات من قاعدة البيانات هنا
