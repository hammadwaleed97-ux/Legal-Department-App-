import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# تنسيق CSS لضمان وضوح النصوص في القوائم
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; }
/* فرض لون أسود للنص داخل القوائم المنسدلة */
div[data-baseweb="select"] { background-color: white !important; }
div[data-baseweb="select"] div, div[data-baseweb="select"] span { color: black !important; }
div[role="listbox"] { background-color: white !important; }
div[role="option"] { color: black !important; background-color: white !important; }
input, textarea { color: black !important; background-color: white !important; }
</style>
""", unsafe_allow_html=True)

# التنقل
if "page" not in st.session_state: st.session_state.page = "cases"

# إنشاء الجدول (19 عمود بيانات + id)
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT,
    case_type TEXT, court TEXT, court_name TEXT, subject TEXT, session_date TEXT,
    decision_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, mobile TEXT,
    status TEXT)""")
conn.commit()

# صفحة التسجيل
if st.session_state.page == "cases":
    st.markdown("<h2 style='text-align:center'>⚖️ تسجيل القضايا</h2>", unsafe_allow_html=True)
    
    litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])
    claimant_type = st.selectbox("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"])
    claimant = st.text_input("اسم الخصم الأول")
    defendant_type = st.selectbox("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"])
    defendant = st.text_input("اسم الخصم الثاني")
    case_no = st.text_input("رقم الدعوى")
    judicial_year = st.text_input("السنة القضائية")
    circuit = st.text_input("الدائرة")
    case_type = st.text_input("النوع")
    court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"])
    court_name = st.text_input("اسم المحكمة")
    subject = st.text_area("موضوع الدعوى")
    session_date = st.date_input("تاريخ الجلسة")
    decision_date = st.date_input("تاريخ القرار")
    reason = st.text_area("السبب")
    notes = st.text_area("ملاحظات")
    judgment_result = st.selectbox("نتيجة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"])
    mobile = st.text_input("رقم الموبايل")

    if st.button("💾 حفظ القضية"):
        # تم ضبط عدد علامات الاستفهام لتساوي عدد الأعمدة (19 عمود بيانات)
        cur.execute("""INSERT INTO cases (litigation_type, claimant_type, claimant, defendant_type, defendant, 
        case_no, judicial_year, circuit, case_type, court, court_name, subject, 
        session_date, decision_date, reason, notes, judgment_result, mobile, status) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (litigation_type, claimant_type, claimant, defendant_type, defendant, 
         case_no, judicial_year, circuit, case_type, court, court_name, subject, 
         str(session_date), str(decision_date), reason, notes, judgment_result, mobile, "متداولة"))
        conn.commit()
        st.success("تم حفظ القضية بنجاح")
