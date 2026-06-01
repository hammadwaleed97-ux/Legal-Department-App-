import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# 1. إعداد قاعدة بيانات القضايا فقط
def init_db():
    conn = sqlite3.connect('cases_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY, court TEXT, case_no TEXT, circle TEXT, year TEXT, 
                  plaintiff TEXT, defendant TEXT, details TEXT, session_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# 2. الهيدر المنسق (تنسيق ثابت ومنظم)
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; border-bottom: 5px solid #FFD700;">
        <h2 style="margin: 0;">الهيئة القومية للتأمين الاجتماعي</h2>
        <h4 style="margin: 5px 0;">الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</h4>
        <p style="margin: 0; font-weight: bold;">إعداد: أ/ وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

# 3. زر الوصول السريع للمكتبة (الرابط)
# ضع رابط مجلدك في Google Drive هنا بين القوسين
google_drive_link = "https://your-google-drive-link-here" 
st.markdown(f'<div style="text-align: center; margin-bottom: 20px;"><a href="{google_drive_link}" target="_blank" style="background-color: #28a745; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">📂 فتح المكتبة القانونية (Google Drive)</a></div>', unsafe_allow_html=True)

# 4. التبويبات القضائية
tab1, tab2, tab3, tab4 = st.tabs(["➕ تسجيل قضية", "📋 سجل القضايا", "🔔 التنبيهات", "📊 التقارير"])

with tab1:
    with st.form("case_add"):
        c1, c2 = st.columns(2)
        court = c1.text_input("المحكمة")
        case_no = c2.text_input("رقم الدعوى")
        circle = c1.text_input("الدائرة")
        year = c2.text_input("سنة")
        plaintiff = st.text_input("اسم المدعى")
        defendant = st.text_input("اسم المدعى عليه")
        session_date = st.date_input("تاريخ الجلسة القادمة")
        details = st.text_area("الموضوع / الوقائع")
        
        if st.form_submit_button("حفظ القضية"):
            conn = sqlite3.connect('cases_system.db')
            c = conn.cursor()
            c.execute("INSERT INTO cases (court, case_no, circle, year, plaintiff, defendant, details, session_date) VALUES (?,?,?,?,?,?,?,?)", 
                      (court, case_no, circle, year, plaintiff, defendant, details, session_date))
            conn.commit()
            conn.close()
            st.success("تم حفظ القضية بنجاح")

with tab2:
    st.subheader("سجل القضايا")
    conn = sqlite3.connect('cases_system.db')
    df = pd.read_sql("SELECT * FROM cases", conn)
    conn.close()
    st.dataframe(df, use_container_width=True)

with tab3:
    st.info("تنبيهات: القضايا التي اقترب موعد جلستها:")
    # يمكننا هنا عمل فلتر للقضايا حسب التاريخ
    
with tab4:
    st.info("التقارير: إحصائيات الإنجاز")

# التوقيع في الأسفل
st.markdown("---")
st.write("مع تحيات وليد حماد | الإدارة العامة للشئون القانونية")
