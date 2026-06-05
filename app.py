import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# CSS - تم تعديل ألوان القوائم لتظهر النصوص (أسود على خلفية بيضاء)
st.markdown("""
<style>
.stApp { background: #062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color: white !important; }

/* إصلاح القوائم المنسدلة */
div[data-baseweb="select"] { background-color: white !important; }
div[data-baseweb="select"] div, div[data-baseweb="select"] span { color: black !important; }
div[role="listbox"] div { color: black !important; background-color: white !important; }

/* حقول الإدخال */
input, textarea { color: black !important; background-color: white !important; }

/* الأزرار */
div.stButton > button {
    width: 320px; height: 65px; border-radius: 15px; border: none;
    background: #2f55d4; color: white; font-size: 20px; font-weight: bold;
    display: block; margin: auto;
}
</style>
""", unsafe_allow_html=True)

# اللوجو
st.markdown("""
<div style="text-align:center">
<h1>⚖️ الهيئة القومية للتأمين الاجتماعى</h1>
<h3>الإدارة العامة للشؤون القانونية</h3>
</div>
""", unsafe_allow_html=True)

# الحالة
if "page" not in st.session_state:
    st.session_state.page = "cases"

# إنشاء الجدول
cur.execute("""
CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT,
    judicial_year TEXT, circuit TEXT, case_type TEXT,
    court TEXT, court_name TEXT, subject TEXT,
    session_date TEXT, decision_date TEXT, reason TEXT,
    notes TEXT, judgment_result TEXT, mobile TEXT,
    status TEXT DEFAULT 'متداولة'
)
""")
conn.commit()

# تسجيل القضايا
st.markdown("<h2 style='text-align:center'>⚖️ تسجيل القضايا</h2>", unsafe_allow_html=True)

litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"], key="s1")
claimant_type = st.selectbox("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"], key="s2")
claimant = st.text_input("اسم الخصم الأول", key="t1")
defendant_type = st.selectbox("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"], key="s3")
defendant = st.text_input("اسم الخصم الثاني", key="t2")
case_no = st.text_input("رقم الدعوى", key="t3")
judicial_year = st.text_input("السنة القضائية", key="t4")
circuit = st.text_input("الدائرة", key="t5")
case_type = st.text_input("النوع", key="t6")
court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"], key="s4")
court_name = st.text_input("اسم المحكمة", key="t7")
subject = st.text_area("موضوع الدعوى", key="t8")
session_date = st.date_input("تاريخ الجلسة", key="d1")
decision_date = st.date_input("تاريخ القرار", key="d2")
reason = st.text_area("السبب", key="t9")
notes = st.text_area("ملاحظات", key="t10")
judgment_result = st.selectbox("نتيجة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"], key="s5")
mobile = st.text_input("رقم الموبايل", key="t11")

if st.button("💾 حفظ القضية", key="save_btn"):
    cur.execute("""
    INSERT INTO cases(litigation_type, claimant_type, claimant, defendant_type, defendant, 
    case_no, judicial_year, circuit, case_type, court, court_name, subject, 
    session_date, decision_date, reason, notes, judgment_result, mobile)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (litigation_type, claimant_type, claimant, defendant_type, defendant, 
          case_no, judicial_year, circuit, case_type, court, court_name, subject, 
          str(session_date), str(decision_date), reason, notes, judgment_result, mobile))
    conn.commit()
    st.success("تم حفظ القضية بنجاح")
