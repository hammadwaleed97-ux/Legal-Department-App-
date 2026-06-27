import streamlit as st
import sqlite3
from datetime import datetime
import os

# ====================== DB ======================
if not os.path.exists("uploads"):
    os.makedirs("uploads")

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_type TEXT, court_type TEXT, court_name TEXT, mission TEXT,
    case_number TEXT, judicial_year TEXT, circuit TEXT, case_category TEXT,
    plaintiff TEXT, defendant TEXT, subject TEXT, notes TEXT,
    whatsapp_enabled INTEGER, whatsapp_number TEXT, created_at TEXT
);

CREATE TABLE IF NOT EXISTS sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER, session_date TEXT, roll_number TEXT,
    procedure TEXT, notes TEXT, created_at TEXT
);
""")
conn.commit()

# ====================== Session ======================
if "page" not in st.session_state: st.session_state.page = "home"
if "selected_case" not in st.session_state: st.session_state.selected_case = None
if "delete_case_id" not in st.session_state: st.session_state.delete_case_id = None

st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# ====================== CSS ======================
st.markdown("""
<style>
#MainMenu, footer, header {visibility:hidden;}
.stApp {background: linear-gradient(180deg, #00152d, #002b5c, #00152d);}
html, body, [class*="css"] {direction:rtl;}

.main-title {text-align:center; font-size:55px; font-weight:bold; color:#FFD700; text-shadow:0 0 20px gold;}
.logo {text-align:center; font-size:110px;}

.watermark {position:fixed; top:35%; left:50%; transform:translate(-50%,-50%); font-size:280px; opacity:0.05; z-index:0;}

.stButton > button {
    width:100%; height:85px; font-size:26px; font-weight:bold;
    border-radius:25px; border:3px solid gold;
    background:linear-gradient(135deg, #0d47a1, #1565c0);
    color:white !important;
}

.news-bar {position:fixed; bottom:0; right:0; width:100%; height:45px; background:#000814; border-top:3px solid gold; overflow:hidden; z-index:999999;}
.news-text {position:absolute; white-space:nowrap; font-size:21px; font-weight:bold; line-height:45px; animation:scrollText 40s linear infinite;}
@keyframes scrollText {0%{transform:translateX(100%);} 100%{transform:translateX(-100%);}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="watermark">⚖️</div>', unsafe_allow_html=True)
st.markdown('<div class="logo">⚖️</div><div class="main-title">إدارة القضايا</div>', unsafe_allow_html=True)

# الشريط السفلي
st.markdown("""
<div class="news-bar">
<div class="news-text">
مع تحيات / وليد حماد &nbsp;|&nbsp; الإدارة العامة للشئون القانونية &nbsp;|&nbsp; ديوان عام منطقة البحيرة &nbsp;|&nbsp; الهيئة القومية للتأمين الاجتماعى
</div>
</div>
""", unsafe_allow_html=True)

# ====================== الصفحة الرئيسية ======================
if st.session_state.page == "home":
    c1, c2, c3 = st.columns([2,4,2])
    with c2:
        if st.button("⚖️ تسجيل القضايا", use_container_width=True):
            st.session_state.page = "cases"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📋 الحصر العام", use_container_width=True):
            st.session_state.page = "inventory"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔔 التنبيهات", use_container_width=True):
            st.session_state.page = "alerts"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 التقارير", use_container_width=True):
            st.session_state.page = "reports"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗄️ الأرشيف", use_container_width=True):
            st.session_state.page = "archive"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📚 المكتبة القانونية", use_container_width=True):
            st.session_state.page = "library"; st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔍 بحث", use_container_width=True):
            st.session_state.page = "search"; st.rerun()

# ====================== تسجيل قضية ======================
if st.session_state.page == "cases":
    st.subheader("⚖️ تسجيل قضية جديدة")
    st.info("صفحة التسجيل - أضف النموذج الكامل من النسخ السابقة")
    if st.button("⬅ العودة"): st.session_state.page = "home"; st.rerun()

# ====================== الحصر العام ======================
if st.session_state.page == "inventory":
    st.subheader("📋 الحصر العام للقضايا")
    st.info("صفحة الحصر - أضف الجدول الكامل من النسخ السابقة")
    if st.button("⬅ العودة"): st.session_state.page = "home"; st.rerun()

# ====================== ملف القضية ======================
if st.session_state.page == "case_details" and st.session_state.selected_case:
    st.subheader("⚖️ ملف القضية")
    st.info("صفحة ملف القضية - زي الصورة اللي بعتها")
    if st.button("⬅ العودة"): st.session_state.page = "inventory"; st.rerun()

# ====================== باقي الصفحات ======================
pages = {
    "alerts": "🔔 التنبيهات",
    "reports": "📊 التقارير",
    "archive": "🗄️ الأرشيف",
    "library": "📚 المكتبة القانونية",
    "search": "🔍 بحث"
}

for p, title in pages.items():
    if st.session_state.page == p:
        st.subheader(title)
        st.info(f"صفحة {title} - تحت التطوير")
        if st.button("⬅ العودة"): st.session_state.page = "home"; st.rerun()

st.caption(" ")
if st.session_state.page == "cases":
    st.markdown("""
    <h1 style='text-align:center; color:#FFD700; text-shadow:0 0 30px gold; margin:20px 0 40px 0;'>
        تسجيل قضية جديدة ⚖️
    </h1>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**نوع الدعوى**")
        case_type = st.selectbox(" ", ["دعوى", "استئناف", "طعن"], label_visibility="collapsed")
        
        st.markdown("**المحكمة**")
        court_type = st.selectbox(" ", ["الابتدائية", "الاستئناف", "النقض", "الإدارية", "القضاء الإداري", "الإدارية العليا"], label_visibility="collapsed")
        
        st.markdown("**اسم المحكمة**")
        court_name = st.text_input(" ", placeholder="اسم المحكمة")
        
        st.markdown("**رقم الدعوى**")
        case_number = st.text_input(" ", placeholder="رقم الدعوى")

    with col2:
        st.markdown("**المدعي**")
        plaintiff = st.text_input(" ", placeholder="اسم المدعي")
        
        st.markdown("**المدعى عليه**")
        defendant = st.text_input(" ", placeholder="اسم المدعى عليه")
        
        st.markdown("**موضوع الدعوى**")
        subject = st.text_area(" ", height=150, placeholder="موضوع الدعوى")
        
        st.markdown("**تاريخ أول جلسة**")
        first_session_date = st.date_input(" ")

    st.markdown("---")

    whatsapp_enabled = st.checkbox("تفعيل التنبيهات عبر واتساب")
    whatsapp_number = st.text_input("رقم الواتساب") if whatsapp_enabled else ""

    uploaded_file = st.file_uploader("تحميل صحيفة الدعوى")

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 حفظ القضية", type="primary", use_container_width=True):
            st.success("✅ تم الحفظ بنجاح!")
            st.balloons()
            st.session_state.page = "inventory"
            st.rerun()

    with col_cancel:
        if st.button("⬅ العودة للرئيسية", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()
