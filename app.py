import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# إعداد قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# إنشاء الجداول الأساسية والمحذوفة
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant TEXT,
    defendant TEXT, case_no TEXT, status TEXT DEFAULT 'متداولة')""")
cur.execute("""CREATE TABLE IF NOT EXISTS deleted_cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant TEXT,
    defendant TEXT, case_no TEXT, delete_reason TEXT, delete_date TEXT)""")
conn.commit()

# التنسيق (CSS) لضمان ثبات أماكن الأيقونات والألوان
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; font-size: 18px !important; }
.logo-box { text-align:center; padding: 20px; border-bottom: 2px solid white; margin-bottom: 20px; }
.footer { text-align: center; margin-top: 50px; font-weight: bold; color: white; padding: 20px; border-top: 2px solid white; }
div.stButton > button { width:100%; height:60px; border-radius:10px; background:#2f55d4; color:white; font-weight:bold; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# اللوجو والعنوان (كاملاً)
st.markdown("""
<div class="logo-box">
<div style="font-size:50px">⚖️</div>
<div style="font-size:28px; font-weight:bold">الهيئة القومية للتأمين الاجتماعى</div>
<div style="font-size:28px; font-weight:bold">الإدارة العامة للشؤون القانونية</div>
<div style="font-size:24px; font-weight:bold">ديوان عام منطقة البحيرة</div>
</div>
""", unsafe_allow_html=True)

# التنقل (الأزرار الستة كما في الصورة)
if "page" not in st.session_state: st.session_state.page = "home"

if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
if st.button("🔔 التنبيهات"): st.session_state.page = "alerts"
if st.button("📊 التقارير"): st.session_state.page = "reports"
if st.button("📂 أرشيف القضايا"): st.session_state.page = "archive"
if st.button("🔍 البحث عن دعوى"): st.session_state.page = "search"
if st.button("📋 القضايا المسجلة"): st.session_state.page = "view_cases"

# صفحات التطبيق
if st.session_state.page == "cases":
    st.header("تسجيل قضية جديدة")
    with st.form("add_case"):
        l_type = st.radio("نوع الإجراء", ["نقض", "استئناف", "دعوى"], horizontal=True)
        c_name = st.text_input("اسم الخصم الأول")
        d_name = st.text_input("اسم الخصم الثاني")
        case_no = st.text_input("رقم الدعوى")
        if st.form_submit_button("💾"):
            cur.execute("INSERT INTO cases (litigation_type, claimant, defendant, case_no) VALUES (?,?,?,?)", (l_type, c_name, d_name, case_no))
            conn.commit()
            st.success("تم الحفظ")

elif st.session_state.page == "view_cases":
    st.header("📋 القضايا المسجلة")
    cases = cur.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()
    for case in cases:
        with st.expander(f"{case[2]} ضد {case[3]}"):
            st.write(f"رقم الدعوى: {case[4]}")

# التوقيع
st.markdown("""
<div class="footer">
مع تحيات<br>
وليد شعبان حماد
</div>
""", unsafe_allow_html=True)
