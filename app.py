import streamlit as st
import sqlite3
import pandas as pd

# تهيئة قاعدة البيانات
def init_db():
    conn = sqlite3.connect('legal_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS cases (id INTEGER PRIMARY KEY, court TEXT, case_no TEXT, circle TEXT, year TEXT, details TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS library (id INTEGER PRIMARY KEY, category TEXT, title TEXT, file_name TEXT)''')
    conn.commit()
    conn.close()
init_db()

# الهيدر المنسق (كما في 1000286867.png)
st.markdown("""
    <div style="background-color: #1a3a6e; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom: 20px;">
        <h3 style="margin: 0;">الهيئة القومية للتأمين الاجتماعي</h3>
        <p style="margin: 5px 0 0 0;">الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>
        <p style="margin: 0; font-weight: bold;">إعداد: أ/ وليد حماد</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["⚖️ القسم القضائي", "📚 المكتبة القانونية"])

with tab1:
    sub1, sub2, sub3, sub4, sub5 = st.tabs(["تسجيل قضية", "سجل القضايا", "التنبيهات", "التقارير", "إدارة وتعديل"])
    with sub1:
        with st.form("case_form"):
            court = st.text_input("المحكمة")
            case_no = st.text_input("رقم الدعوى")
            circle = st.text_input("الدائرة")
            year = st.text_input("سنة")
            details = st.text_area("بيانات الخصوم والموضوع")
            if st.form_submit_button("حفظ القضية"):
                conn = sqlite3.connect('legal_system.db')
                c = conn.cursor()
                c.execute("INSERT INTO cases (court, case_no, circle, year, details) VALUES (?,?,?,?,?)", (court, case_no, circle, year, details))
                conn.commit()
                conn.close()
                st.success("تم الحفظ")
    with sub2: st.subheader("جدول القضايا المسجلة")
    with sub3: st.info("شاشة التنبيهات: متابعة الجلسات")
    with sub4: st.info("شاشة التقارير: الإحصائيات")
    with sub5: st.warning("خيارات التعديل والحذف هنا")

with tab2:
    st.subheader("إدارة المكتبة القانونية")
    # القائمة المنسدلة للمكتبة (كما في 1000286868.png و 1000286869.png)
    category = st.selectbox("نوع التشريع", ["قوانين", "لوائح", "قرارات وزارية", "كتب دورية", "منشورات", "تعليمات", "فتاوى", "أحكام"])
    title = st.text_input("عنوان المستند")
    uploaded_file = st.file_uploader("تحميل المستند")
    
    col1, col2 = st.columns(2)
    if col1.button("إضافة للمكتبة"): st.success("تمت الإضافة")
    if col2.button("فتح المستند"): st.info("جاري الفتح...")
    
    st.write("---")
    st.subheader("قائمة المستندات المتاحة")
    # عرض الجدول الخاص بالمكتبة
