import streamlit as st
import sqlite3
import pandas as pd

# 1. تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, نوع_القضية TEXT, المحكمة TEXT, رقم_الدعوى TEXT, 
                  السنة TEXT, المدعي TEXT, المدعى_عليه TEXT, الموضوع TEXT, تاريخ_الجلسة DATE, الحالة TEXT)''')
    conn.commit()
    conn.close()
init_db()

# 2. الهيدر
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 15px; border-radius: 8px; color: white; text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0; font-size: 18px;">الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</h3>
    </div>
""", unsafe_allow_html=True)

# 3. حماية المكتبة (تظهر فقط عند إدخال الباسورد)
st.subheader("🔒 الدخول الخاص للإدارة")
admin_pwd = st.text_input("أدخل كلمة المرور الخاصة بك لإظهار المكتبة", type="password")

if admin_pwd == "WALID2026": # كلمة سر خاصة بك، يمكنك تغييرها
    DRIVE_LINK = "https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke"
    st.markdown(f'''
        <div style="text-align: center; margin-bottom: 20px;">
            <a href="{DRIVE_LINK}" target="_blank" 
            style="background-color: #28a745; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">
            📂 فتح مكتبة الإدارة القانونية
            </a>
        </div>
    ''', unsafe_allow_html=True)
elif admin_pwd != "":
    st.error("كلمة المرور غير صحيحة")

# 4. باقي التطبيق (متاح للجميع)
tab1, tab2, tab3, tab4 = st.tabs(["⚖️ قضاء عادي", "🏛️ محكمة النقض", "⚖️ مجلس الدولة", "📊 سجل المتابعة"])

# ... (نفس كود حفظ القضايا السابق)
