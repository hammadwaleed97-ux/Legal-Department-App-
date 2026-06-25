import streamlit as st
import sqlite3
from datetime import datetime

# =====================================
# قاعدة البيانات
# =====================================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

# =====================================
# جدول القضايا
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_type TEXT,

court_type TEXT,

court_name TEXT,

mission TEXT,

case_number TEXT,

judicial_year TEXT,

circuit TEXT,

case_category TEXT,

plaintiff TEXT,

defendant TEXT,

subject TEXT,

notes TEXT,

whatsapp_enabled INTEGER,

whatsapp_number TEXT,

created_at TEXT

)
""")

# =====================================
# جدول الجلسات
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS sessions(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_id INTEGER,

session_date TEXT,

roll_number TEXT,

procedure TEXT,

created_at TEXT

)
""")

# =====================================
# جدول المستندات
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS documents(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_id INTEGER,

document_type TEXT,

document_description TEXT,

file_name TEXT,

file_path TEXT,

uploaded_at TEXT

)
""")

conn.commit()
# =====================================
# الصفحات
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"
st.set_page_config(
    page_title="",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background: linear-gradient(180deg,#00152d,#002b5c,#00152d);
}

html, body, [class*="css"]{
    direction:rtl;
}

.main-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:#FFD700;
    text-shadow:0px 0px 15px gold;
}

.logo{
    text-align:center;
    font-size:110px;
}

.watermark{
    position:fixed;
    top:35%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:280px;
    opacity:0.05;
    z-index:0;
}

.stButton > button{
    width:100%;
    height:95px;
    font-size:28px;
    font-weight:bold;
    border-radius:25px;
    border:3px solid gold;
    background:linear-gradient(135deg,#0d47a1,#1565c0);
    color:white !important;
    box-shadow:0 0 25px rgba(255,215,0,.6);
}

.stButton > button:hover{
    transform:scale(1.03);
}

.news-bar{
    position:fixed;
    bottom:0;
    right:0;
    width:100%;
    height:42px;
    background:#000814;
    border-top:2px solid gold;
    overflow:hidden;
    z-index:999999;
}

.news-text{
    position:absolute;
    white-space:nowrap;
    font-size:20px;
    font-weight:bold;
    line-height:42px;
    animation:scrollText 25s linear infinite;
}

@keyframes scrollText{
0%{
transform:translateX(-100%);
}
100%{
transform:translateX(100vw);
}
}

</style>
""", unsafe_allow_html=True)

# =========================
# خلفية ميزان شفافة
# =========================

st.markdown("""
<div class="watermark">
⚖️
</div>
""", unsafe_allow_html=True)

# =========================
# اللوجو
# =========================

st.markdown("""
<div class="logo">⚖️</div>
<div class="main-title">إدارة القضايا</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# =========================
# الأيقونات
# =========================

c1,c2,c3 = st.columns([2,4,2])

with c2:

    st.button("⚖️ تسجيل القضايا", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("📋 الحصر العام", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("🔔 التنبيهات", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("📊 التقارير", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("🗄️ الأرشيف", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("📚 المكتبة القانونية", use_container_width=True)

# =========================
# الشريط السفلي
# =========================

st.markdown("""

<div class="news-bar">
<div class="news-text">

<span style="color:#FFD700;">
مع تحيات / وليد حماد
</span>

<span style="color:white;"> | </span>

<span style="color:#00FFFF;">
الإدارة العامة للشئون القانونية
</span>

<span style="color:white;"> | </span>

<span style="color:#7FFF00;">
ديوان عام منطقة البحيرة
</span>

<span style="color:white;"> | </span>

<span style="color:#FF4500;">
الهيئة القومية للتأمين الاجتماعى
</span>

</div>
</div>

""", unsafe_allow_html=True)
