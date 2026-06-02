import streamlit as st
import sqlite3
import pandas as pd

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, نوع_القضية TEXT, المحكمة TEXT, رقم_الدعوى TEXT, 
                  السنة TEXT, المدعي TEXT, المدعى_عليه TEXT, الموضوع TEXT, الحالة TEXT)''')
    conn.commit()
    conn.close()

init_db()

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

# 1. تبويب المكتبة (مع حماية)
if menu == "📂 المكتبة القانونية":
    st.header("📂 المكتبة القانونية")
    pwd = st.text_input("أدخل كلمة المرور:", type="password")
    if pwd == "WALID2026": 
        st.success("تم الدخول بنجاح")
        st.markdown('[اضغط هنا لفتح مجلد المكتبة](https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke)', unsafe_allow_html=True)
    elif pwd != "":
        st.error("كلمة المرور غير صحيحة")

# 2. تبويب إضافة قضايا (مثال للقضاء العادي)
elif menu == "⚖️ قضاء عادي":
    st.header("⚖️ تسجيل قضاء عادي")
    with st.form("case_form"):
        court = st.text_input("المحكمة")
        no = st.text_input("رقم الدعوى")
        if st.form_submit_button("حفظ القضية"):
            conn = sqlite3.connect('legal_system.db')
            c = conn.cursor()
            c.execute("INSERT INTO cases (المحكمة, رقم_الدعوى) VALUES (?,?)", (court, no))
            conn.commit()
            conn.close()
            st.success("تم حفظ القضية!")

# 3. تبويب البحث
elif menu == "🔍 البحث القانوني":
    st.header("🔍 البحث القانوني")
    term = st.text_input("اكتب رقم الدعوى أو اسم المحكمة للبحث:")
    if term:
        conn = sqlite3.connect('legal_system.db')
        df = pd.read_sql(f"SELECT * FROM cases WHERE المحكمة LIKE '%{term}%' OR رقم_الدعوى LIKE '%{term}%'", conn)
        conn.close()
        st.dataframe(df)

# 4. تبويب السجل
elif menu == "📊 سجل المتابعة":
    st.header("📊 سجل المتابعة")
    conn = sqlite3.connect('legal_system.db')
    df = pd.read_sql("SELECT * FROM cases", conn)
    conn.close()
    st.dataframe(df)
