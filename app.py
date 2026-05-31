import streamlit as st
import sqlite3
import pandas as pd

# 1. إعداد الصفحة لتكون واسعة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# 2. تنسيق CSS لضمان عدم تداخل القائمة مع المحتوى
# لقد أضفنا خاصية z-index و padding-left دقيقة لضبط العرض
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 300px !important;
        flex-shrink: 0;
    }
    .main .block-container {
        padding-left: 320px !important;
        padding-right: 20px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد قاعدة البيانات
conn = sqlite3.connect("legal.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS cases (id INTEGER PRIMARY KEY, case_no TEXT, case_type TEXT, status TEXT)")
conn.commit()

# القائمة الجانبية
with st.sidebar:
    st.title("🏛️ الإدارة العامة")
    menu = ["الرئيسية", "القضايا", "الفتاوى", "التحقيقات"]
    choice = st.radio("القائمة", menu)
    st.markdown("---")
    st.write("مع تحيات وليد حماد")
    st.write("ديوان عام منطقة البحيرة")

# 4. عرض المحتوى بناءً على اختيار القائمة
if choice == "الرئيسية":
    st.title("لوحة تحكم ديوان عام منطقة البحيرة")
    st.metric("إجمالي القضايا", "15")

elif choice == "القضايا":
    st.title("إدارة القضايا")
    # نموذج إضافة قضية
    with st.form("add_case"):
        c_no = st.text_input("رقم القضية")
        c_type = st.selectbox("نوع القضية", ["مدني", "تأمين", "إداري"])
        submitted = st.form_submit_button("حفظ القضية")
        if submitted:
            c.execute("INSERT INTO cases (case_no, case_type, status) VALUES (?, ?, ?)", (c_no, c_type, "جارية"))
            conn.commit()
            st.success("تم الحفظ بنجاح!")
    
    # عرض القضايا
    df = pd.read_sql("SELECT * FROM cases", conn)
    st.table(df)

elif choice == "الفتاوى":
    st.title("قسم الفتوى والتشريع")
    st.info("هذا القسم قيد التطوير...")

elif choice == "التحقيقات":
    st.title("قسم التحقيقات")
    st.info("هذا القسم قيد التطوير...")
