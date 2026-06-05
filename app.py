import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# إعداد قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# إنشاء الجداول الأساسية
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT,
    case_type TEXT, court TEXT, court_name TEXT, subject TEXT, session_date TEXT,
    decision_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, mobile TEXT, status TEXT)""")

cur.execute("""CREATE TABLE IF NOT EXISTS deleted_cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT,
    case_type TEXT, court TEXT, court_name TEXT, subject TEXT, session_date TEXT,
    decision_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, mobile TEXT,
    delete_reason TEXT, delete_date TEXT)""")
conn.commit()

# التنسيق
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; font-size: 18px !important; }
.logo-box { text-align:center; padding: 20px; border-bottom: 2px solid white; margin-bottom: 20px; }
.footer { text-align: center; margin-top: 50px; font-weight: bold; color: white; padding: 20px; border-top: 2px solid white; }
div.stButton > button { width:100%; height:60px; border-radius:10px; background:#2f55d4; color:white; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

# اللوجو والعنوان
st.markdown("""
<div class="logo-box">
<div style="font-size:50px">⚖️</div>
<div style="font-size:28px; font-weight:bold">الهيئة القومية للتأمين الاجتماعى</div>
<div style="font-size:28px; font-weight:bold">الإدارة العامة للشؤون القانونية</div>
<div style="font-size:24px; font-weight:bold">ديوان عام منطقة البحيرة</div>
</div>
""", unsafe_allow_html=True)

# التنقل (الأزرار الستة)
if "page" not in st.session_state: st.session_state.page = "cases"

c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1:
    if st.button("⚖️ تسجيل"): st.session_state.page = "cases"
with c2:
    if st.button("🔔 تنبيهات"): st.session_state.page = "alerts"
with c3:
    if st.button("📊 تقارير"): st.session_state.page = "reports"
with c4:
    if st.button("📂 أرشيف"): st.session_state.page = "archive"
with c5:
    if st.button("🔍 بحث"): st.session_state.page = "search"
with c6:
    if st.button("📋 مسجلة"): st.session_state.page = "view_cases"

# منطق الصفحات
if st.session_state.page == "cases":
    st.header("تسجيل قضية جديدة")
    with st.form("add_case"):
        l_type = st.radio("نوع الإجراء", ["دعوى", "استئناف", "نقض"], horizontal=True)
        c_name = st.text_input("اسم الخصم الأول")
        d_name = st.text_input("اسم الخصم الثاني")
        case_no = st.text_input("رقم الدعوى")
        submit = st.form_submit_button("💾 حفظ القضية")
        if submit:
            cur.execute("INSERT INTO cases (litigation_type, claimant, defendant, case_no, status) VALUES (?,?,?,?,?)",
                        (l_type, c_name, d_name, case_no, "متداولة"))
            conn.commit()
            st.success("تم الحفظ")

elif st.session_state.page == "view_cases":
    st.header("📋 القضايا المسجلة")
    cases = cur.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()
    for case in cases:
        with st.expander(f"قضية رقم: {case[6]} - {case[3]} ضد {case[5]}"):
            with st.form(f"f_{case[0]}"):
                s_date = st.date_input("تاريخ الجلسة القادمة", key=f"d_{case[0]}")
                action = st.text_input("الإجراء المطلوب", key=f"a_{case[0]}")
                if st.form_submit_button("تحديث"):
                    cur.execute("UPDATE cases SET session_date=?, reason=? WHERE id=?", (str(s_date), action, case[0]))
                    conn.commit()
                    st.rerun()

# التوقيع
st.markdown("""
<div class="footer">
مع تحيات<br>
وليد شعبان حماد
</div>
""", unsafe_allow_html=True)
