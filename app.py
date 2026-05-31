import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# حقن التنسيق الاحترافي الخاص بك (من ملفك الأصلي)
st.markdown(f"""
<style>
    /* دمج تنسيقك الخاص */
    [data-testid="stSidebar"] {{ background-color: #0b1e30 !important; width: 300px !important; }}
    .stApp {{ background-color: #eef2f7; }}
    .css-1544g2n {{ padding: 0 !important; }}
    h1 {{ color: #0b1e30; }}
</style>
""", unsafe_allow_html=True)

# إعداد قاعدة البيانات
conn = sqlite3.connect("legal.db", check_same_thread=False)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS cases (id INTEGER PRIMARY KEY, case_no TEXT, case_type TEXT, status TEXT)")
conn.commit()

# Sidebar (القائمة الجانبية)
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 20px;">
        <div style="font-size:2rem;">⚖️</div>
        <div style="font-weight:800; color:#fff;">الهيئة القومية للتأمين الاجتماعي</div>
        <div style="color:#6ea8ce; font-size:0.8rem;">الإدارة العامة للشئون القانونية</div>
    </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("القائمة الرئيسية", ["لوحة التحكم", "القضايا القانونية", "الفتاوى", "التحقيقات", "المكتبة"])

# المحتوى الرئيسي
if menu == "لوحة التحكم":
    st.title("لوحة تحكم ديوان عام منطقة البحيرة")
    st.metric("إجمالي القضايا", "15")

elif menu == "القضايا القانونية":
    st.title("📁 القضايا القانونية")
    with st.form("case_form"):
        c_no = st.text_input("رقم القضية")
        c_type = st.selectbox("نوع القضية", ["مدني", "تأمين"])
        if st.form_submit_button("إضافة"):
            c.execute("INSERT INTO cases (case_no, case_type, status) VALUES (?, ?, ?)", (c_no, c_type, "جارية"))
            conn.commit()
    
    st.table(pd.read_sql("SELECT * FROM cases", conn))

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("الإصدار 2.0.0 | أ/ وليد حماد")
