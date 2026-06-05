import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# تهيئة قاعدة البيانات (حل مشكلة NameError)
# =========================
if "conn" not in st.session_state:
    st.session_state.conn = sqlite3.connect("legal_cases.db", check_same_thread=False)
    st.session_state.cur = st.session_state.conn.cursor()

conn = st.session_state.conn
cur = st.session_state.cur

# =========================
# CSS
# =========================
st.markdown("""
<style>
.stApp{ background-color:#062456; }
.block-container{ padding-top:5px; }
.logo-box{ text-align:center; color:white; }
.logo-icon{ font-size:60px; margin-top:25px; margin-bottom:10px; }
.logo-main{ font-size:30px; font-weight:bold; white-space:nowrap; margin-bottom:20px; }
.logo-sub{ font-size:24px; font-weight:bold; white-space:nowrap; margin-bottom:45px; }
.prepare{ font-size:20px; margin-bottom:10px; }
.name{ font-size:32px; font-weight:bold; margin-bottom:15px; }
.place{ font-size:24px; font-weight:bold; margin-bottom:35px; }
div.stButton > button{ width:280px; height:70px; border-radius:18px; border:none; font-size:21px; font-weight:bold; margin:auto; display:block; background-color:#2f55d4; color:white; }
div.stButton > button:hover{ background-color:#4368e0; color:white; }
</style>
""", unsafe_allow_html=True)

# =========================
# اللوجو
# =========================
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
# إنشاء جدول القضايا (تم نقله بعد التهيئة)
# =====================================
cur.execute("""
CREATE TABLE IF NOT EXISTS cases(
id INTEGER PRIMARY KEY AUTOINCREMENT,
litigation_type TEXT,
claimant_type TEXT, claimant TEXT,
defendant_type TEXT, defendant TEXT,
case_no TEXT, judicial_year TEXT, circuit TEXT,
case_type TEXT, court TEXT, court_name TEXT,
subject TEXT, session_date TEXT, decision_date TEXT,
reason TEXT, notes TEXT, judgment_result TEXT,
mobile TEXT, status TEXT DEFAULT 'متداولة'
)
""")
conn.commit()

# =========================
# القائمة الرئيسية
# =========================
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
    st.button("🔔 التنبيهات")
    st.button("📊 التقارير")
    st.button("📂 أرشيف القضايا")
    st.button("🔍 البحث عن دعوى")
    st.button("❌ القضايا المحذوفة")

# =====================================
# تسجيل القضايا
# =====================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "cases":
    # (باقي كود تسجيل القضايا الخاص بك يوضع هنا...)
    pass
