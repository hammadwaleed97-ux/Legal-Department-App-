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

# ====================== Streamlit ======================
if "page" not in st.session_state: st.session_state.page = "home"
if "selected_case" not in st.session_state: st.session_state.selected_case = None
if "delete_case_id" not in st.session_state: st.session_state.delete_case_id = None

st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# ====================== CSS الأصلي ======================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{background: linear-gradient(180deg, #00152d, #002b5c, #00152d);}

html, body, [class*="css"]{direction:rtl;}

.main-title{
    text-align:center; font-size:55px; font-weight:bold; 
    color:#FFD700; text-shadow:0 0 20px gold;
}
.logo{text-align:center; font-size:110px;}

.watermark{
    position:fixed; top:35%; left:50%; transform:translate(-50%,-50%);
    font-size:280px; opacity:0.05; z-index:0;
}

label, [data-testid="stWidgetLabel"]{
    color:white !important; font-size:20px !important; font-weight:bold !important;
}

.stButton > button{
    width:100%; height:85px; font-size:26px; font-weight:bold;
    border-radius:25px; border:3px solid gold;
    background:linear-gradient(135deg, #0d47a1, #1565c0);
    color:white !important;
}

.news-bar{
    position:fixed; bottom:0; right:0; width:100%; height:45px;
    background:#000814; border-top:3px solid gold;
    overflow:hidden; z-index:999999;
}
.news-text{
    position:absolute; white-space:nowrap; font-size:21px; font-weight:bold;
    line-height:45px; animation:scrollText 40s linear infinite;
}
@keyframes scrollText{
    0% {transform:translateX(100%);}
    100% {transform:translateX(-100%);}
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="watermark">⚖️</div>', unsafe_allow_html=True)
st.markdown('<div class="logo">⚖️</div><div class="main-title">إدارة القضايا</div>', unsafe_allow_html=True)

# ====================== الشريط السفلي ======================
st.markdown("""
<div class="news-bar">
<div class="news-text">
مع تحيات / وليد حماد &nbsp;|&nbsp; 
الإدارة العامة للشئون القانونية &nbsp;|&nbsp; 
ديوان عام منطقة البحيرة &nbsp;|&nbsp; 
الهيئة القومية للتأمين الاجتماعى
</div>
</div>
""", unsafe_allow_html=True)

# ====================== الصفحة الرئيسية ======================
if st.session_state.page == "home":
    c1, c2, c3 = st.columns([2,4,2])
    with c2:
        if st.button("⚖️ تسجيل القضايا", use_container_width=True):
            st.session_state.page = "cases"
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📋 الحصر العام", use_container_width=True):
            st.session_state.page = "inventory"
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📊 التقارير", use_container_width=True):
            st.session_state.page = "reports"
            st.rerun()

# ====================== الحصر العام ======================
if st.session_state.page == "inventory":
    st.subheader("📋 الحصر العام للقضايا")
    
    cur.execute("""
        SELECT c.id, c.case_type, c.case_number, c.judicial_year, c.circuit, 
               c.case_category, c.court_name, c.mission, c.plaintiff, c.defendant,
               (SELECT session_date FROM sessions s WHERE s.case_id=c.id ORDER BY session_date DESC LIMIT 1) as last_date,
               (SELECT procedure FROM sessions s WHERE s.case_id=c.id ORDER BY session_date DESC LIMIT 1) as last_proc
        FROM cases c ORDER BY c.id DESC
    """)
    rows = cur.fetchall()

    for row in rows:
        case_id = row[0]
        line = f"{row[1]} {row[2]} لسنة {row[3]} دائرة {row[4]} {row[5]} {row[6]}"
        st.markdown(f"**{line}**")
        st.write(f"**الخصوم:** {row[8]} ضد {row[9]}")
        if row[10]: st.write(f"**آخر جلسة:** {row[10]} - {row[11]}")

        c1,c2,c3 = st.columns(3)
        with c1:
            if st.button("📂 فتح", key=f"open{case_id}", use_container_width=True):
                st.session_state.selected_case = case_id
                st.session_state.page = "case_details"
                st.rerun()
        with c2:
            if st.button("✏️ تعديل", key=f"edit{case_id}", use_container_width=True):
                st.session_state.selected_case = case_id
                st.session_state.page = "edit_case"
                st.rerun()
        with c3:
            if st.button("🗑 حذف", key=f"del{case_id}", use_container_width=True):
                st.session_state.delete_case_id = case_id

        if st.session_state.delete_case_id == case_id:
            st.warning("هل تريد الحذف؟")
            d1,d2 = st.columns(2)
            with d1:
                if st.button("✅ نعم", key=f"yes{case_id}"):
                    cur.execute("DELETE FROM cases WHERE id=?", (case_id,))
                    cur.execute("DELETE FROM sessions WHERE case_id=?", (case_id,))
                    conn.commit()
                    st.session_state.delete_case_id = None
                    st.rerun()
            with d2:
                if st.button("❌ إلغاء"):
                    st.session_state.delete_case_id = None
                    st.rerun()
        st.markdown("---")

    if st.button("⬅ العودة"):
        st.session_state.page = "home"; st.rerun()

st.caption(" ")
