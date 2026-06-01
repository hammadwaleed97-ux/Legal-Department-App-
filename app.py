import streamlit as st
import sqlite3
import pandas as pd

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('cases_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY, المحكمة TEXT, رقم_الدعوى TEXT, الدائرة TEXT, السنة TEXT, 
                  المدعي TEXT, المدعى_عليه TEXT, الموضوع TEXT, تاريخ_الجلسة DATE)''')
    conn.commit()
    conn.close()
init_db()

# الهيدر المنسق (تعديل الحجم ليصبح في سطر واحد)
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0; font-size: 20px;">الهيئة القومية للتأمين الاجتماعي</h3>
        <p style="margin: 5px 0 0 0; font-size: 14px;">الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة | إعداد: أ/ وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

# رابط المكتبة (ضع رابط فولدر الدرايف هنا)
google_drive_link = "https://your-google-drive-link-here"
st.markdown(f'<div style="text-align: center;"><a href="{google_drive_link}" target="_blank" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">📂 فتح المكتبة القانونية (Google Drive)</a></div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚖️ إدارة القضايا", "📊 التقارير والإحصائيات"])

with tab1:
    sub1, sub2 = st.tabs(["تسجيل قضية جديدة", "سجل القضايا المحدث"])
    with sub1:
        with st.form("new_case"):
            c1, c2 = st.columns(2)
            court = c1.text_input("المحكمة")
            case_no = c2.text_input("رقم الدعوى")
            circle = c1.text_input("الدائرة")
            year = c2.text_input("السنة")
            date = st.date_input("تاريخ الجلسة")
            plaintiff = st.text_input("اسم المدعي")
            defendant = st.text_input("اسم المدعى عليه")
            details = st.text_area("الموضوع")
            if st.form_submit_button("حفظ القضية"):
                conn = sqlite3.connect('cases_system.db')
                c = conn.cursor()
                c.execute("INSERT INTO cases VALUES (NULL,?,?,?,?,?,?,?,?)", (court, case_no, circle, year, plaintiff, defendant, details, date))
                conn.commit()
                conn.close()
                st.success("تم الحفظ")
    with sub2:
        conn = sqlite3.connect('cases_system.db')
        df = pd.read_sql("SELECT * FROM cases", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)

with tab2:
    st.subheader("استخراج تقرير مخصص")
    d1 = st.date_input("من تاريخ")
    d2 = st.date_input("إلى تاريخ")
    if st.button("استخراج التقرير"):
        conn = sqlite3.connect('cases_system.db')
        df = pd.read_sql(f"SELECT * FROM cases WHERE تاريخ_الجلسة BETWEEN '{d1}' AND '{d2}'", conn)
        conn.close()
        st.dataframe(df)
