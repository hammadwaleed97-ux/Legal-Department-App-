import streamlit as st
import sqlite3
import pandas as pd

# (كود قاعدة البيانات كما هو ثابت)
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, نوع_القضية TEXT, المحكمة TEXT, رقم_الدعوى TEXT, 
                  السنة TEXT, المدعي TEXT, المدعى_عليه TEXT, الموضوع TEXT, تاريخ_الجلسة DATE, الحالة TEXT)''')
    conn.commit()
    conn.close()
init_db()

# الهيدر المنسق
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 15px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0; font-size: 18px;">الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 🔒 منطقة التحكم في المكتبة (لك أنت فقط)
st.subheader("إدارة المكتبة القانونية")
pwd = st.text_input("أدخل كلمة المرور الخاصة بك للوصول للمكتبة", type="password")

if pwd == "WALID2026": # يمكنك تغيير هذه الكلمة
    st.success("مرحباً أستاذ وليد، المكتبة متاحة الآن:")
    st.markdown(f'''
        <a href="https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke" target="_blank" 
        style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
        📂 فتح المجلد المخصص للمكتبة القانونية فقط
        </a>
    ''', unsafe_allow_html=True)
elif pwd != "":
    st.error("كلمة مرور غير صحيحة")

# أقسام القضايا (متاحة للجميع)
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "📊 سجل المتابعة"])

# ... (باقي كود القضايا كما هو)
