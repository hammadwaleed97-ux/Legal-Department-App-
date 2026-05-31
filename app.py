import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# 1. إعداد قاعدة البيانات
conn = sqlite3.connect("legal.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS cases (id INTEGER PRIMARY KEY, case_no TEXT, case_type TEXT, status TEXT)")
conn.commit()

# 2. تنسيق الواجهة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# القائمة الجانبية
with st.sidebar:
    st.title("🏛️ الإدارة العامة")
    menu = ["الرئيسية", "القضايا", "الفتاوى", "التحقيقات"]
    choice = st.radio("القائمة", menu)
    st.markdown("---")
    st.write("مع تحيات وليد حماد")

# 3. المنطق (حسب اختيارك من القائمة)
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
            st.success("تم حفظ القضية!")
    
    # عرض القضايا
    df = pd.read_sql("SELECT * FROM cases", conn)
    st.table(df)

elif choice == "الفتاوى":
    st.title("قسم الفتوى والتشريع")
    st.write("جاري العمل على إضافة الفتاوى...")

elif choice == "التحقيقات":
    st.title("قسم التحقيقات")
    st.write("جاري العمل على إضافة التحقيقات...")
