import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد قاعدة البيانات
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    # جدول القضايا
    c.execute('''CREATE TABLE IF NOT EXISTS cases 
                 (id INTEGER PRIMARY KEY, court TEXT, case_no TEXT, circle TEXT, year TEXT, 
                  plaintiff TEXT, defendant TEXT, details TEXT, date TEXT)''')
    # جدول المكتبة
    c.execute('''CREATE TABLE IF NOT EXISTS library 
                 (id INTEGER PRIMARY KEY, category TEXT, title TEXT, file_path TEXT)''')
    conn.commit()
    conn.close()
init_db()

# الهيدر المنسق (تنسيق ثابت ومنظم)
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px; border-bottom: 5px solid #FFD700;">
        <h2 style="margin: 0;">الهيئة القومية للتأمين الاجتماعي</h2>
        <h4 style="margin: 5px 0;">الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</h4>
        <p style="margin: 0; font-weight: bold;">إعداد: أ/ وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚖️ القسم القضائي", "📚 المكتبة القانونية"])

with tab1:
    s1, s2, s3, s4, s5 = st.tabs(["تسجيل قضية", "سجل القضايا", "التنبيهات", "التقارير", "إدارة وتعديل"])
    
    with s1:
        with st.form("case_add"):
            c1, c2 = st.columns(2)
            court = c1.text_input("المحكمة")
            case_no = c2.text_input("رقم الدعوى")
            circle = c1.text_input("الدائرة")
            year = c2.text_input("السنة")
            plaintiff = st.text_input("اسم المدعى")
            defendant = st.text_input("اسم المدعى عليه")
            details = st.text_area("الموضوع / الوقائع")
            if st.form_submit_button("حفظ القضية في السجل"):
                conn = sqlite3.connect('legal_system.db')
                c = conn.cursor()
                c.execute("INSERT INTO cases (court, case_no, circle, year, plaintiff, defendant, details, date) VALUES (?,?,?,?,?,?,?,?)", 
                          (court, case_no, circle, year, plaintiff, defendant, details, datetime.now().strftime("%Y-%m-%d")))
                conn.commit()
                conn.close()
                st.success("تم الحفظ بنجاح")

    with s2:
        st.subheader("جدول القضايا المتداولة")
        conn = sqlite3.connect('legal_system.db')
        df = pd.read_sql("SELECT * FROM cases", conn)
        conn.close()
        st.dataframe(df, use_container_width=True)

    with s3: st.info("تنبيهات الجلسات القادمة (مربوطة بالتاريخ)")
    with s4: st.info("تقرير إنجازات الإدارة")
    with s5: st.warning("خيارات التعديل والحذف متاحة هنا بناءً على رقم ID")

with tab2:
    st.subheader("إدارة المكتبة القانونية")
    cat = st.selectbox("نوع المستند", ["قوانين", "لوائح", "قرارات وزارية", "كتب دورية", "منشورات", "تعليمات", "فتاوى", "أحكام"])
    title = st.text_input("عنوان المستند")
    uploaded_file = st.file_uploader("تحميل ملف المستند")
    
    col1, col2 = st.columns(2)
    if col1.button("إضافة للمكتبة"):
        st.success(f"تم إضافة {title} إلى {cat}")
    if col2.button("فتح/اطلاع على المستند"):
        st.info("جاري استعراض المستند...")
