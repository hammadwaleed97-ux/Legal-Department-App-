import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# =====================================
# إعداد الصفحة
# =====================================
st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =====================================
# تهيئة قاعدة البيانات (مهم جداً لمنع تكرار الاتصال)
# =====================================
if "conn" not in st.session_state:
    st.session_state.conn = sqlite3.connect("cases.db", check_same_thread=False)
    st.session_state.cur = st.session_state.conn.cursor()

conn = st.session_state.conn
cur = st.session_state.cur

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

# =====================================
# CSS
# =====================================
st.markdown("""
<style>
.stApp{ background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6{ color:white !important; }
.stSelectbox div[data-baseweb="select"] > div{ background:white !important; color:black !important; }
div[role="option"]{ color:black !important; background:white !important; }
input, textarea{ color:black !important; }
.logo-box{ text-align:center; }
div.stButton > button{ width:320px; height:65px; border-radius:15px; border:none; background:#2f55d4; color:white; font-size:20px; font-weight:bold; display:block; margin:auto; }
</style>
""", unsafe_allow_html=True)

# =====================================
# اللوجو
# =====================================
st.markdown("""
<div class="logo-box">
<div class="logo-icon">⚖️</div>
<div class="logo-main">الهيئة القومية للتأمين الاجتماعى</div>
<div class="logo-sub">الإدارة العامة للشؤون القانونية</div>
<div class="prepare">إعداد</div>
<div class="name">وليد شعبان حماد</div>
<div class="place">ديوان عام منطقة البحيرة</div>
</div>
""", unsafe_allow_html=True)

# =====================================
# القائمة الرئيسية
# =====================================
if "page" not in st.session_state:
    st.session_state.page = "home"

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⚖️ تسجيل القضايا", key="btn_reg"): st.session_state.page = "cases"
    if st.button("🔔 التنبيهات", key="btn_alert"): st.session_state.page = "alerts"
    if st.button("📊 التقارير", key="btn_rep"): st.session_state.page = "reports"
    if st.button("📂 أرشيف القضايا", key="btn_arch"): st.session_state.page = "archive"
    if st.button("🔍 البحث عن دعوى", key="btn_src"): st.session_state.page = "search"
    if st.button("❌ القضايا المحذوفة", key="btn_del"): st.session_state.page = "deleted"

# =====================================
# تسجيل القضايا
# =====================================
if st.session_state.page == "cases":
    st.markdown("<h2 style='color:white;text-align:center'>⚖️ تسجيل القضايا</h2>", unsafe_allow_html=True)

    litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"], key="l_type")
    claimant_type = st.selectbox("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"], key="c_type")
    claimant = st.text_input("اسم الخصم الأول", key="claimant")
    defendant_type = st.selectbox("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"], key="d_type")
    defendant = st.text_input("اسم الخصم الثاني", key="defendant")
    case_no = st.text_input("رقم الدعوى", key="case_no")
    judicial_year = st.text_input("السنة القضائية", key="year")
    circuit = st.text_input("الدائرة", key="circuit")
    case_type = st.text_input("النوع", key="ctype")
    court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"], key="court")
    court_name = st.text_input("اسم المحكمة", key="cname")
    subject = st.text_area("موضوع الدعوى", key="subject")
    session_date = st.date_input("تاريخ الجلسة", key="s_date")
    decision_date = st.date_input("تاريخ القرار", key="d_date")
    reason = st.text_area("السبب", key="reason")
    notes = st.text_area("ملاحظات", key="notes")
    judgment_result = st.selectbox("نتيجة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"], key="res")
    mobile = st.text_input("رقم الموبايل لإرسال التنبيهات", key="mobile")

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

مع تحيات وليد حماد
الادارة العامة للشءون القانونية ديوان عام منطقة البحيرة
