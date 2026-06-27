import streamlit as st
import sqlite3
from datetime import datetime
import os

# ====================== قاعدة البيانات ======================
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

CREATE TABLE IF NOT EXISTS documents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER, document_type TEXT, document_description TEXT,
    file_name TEXT, file_path TEXT, uploaded_at TEXT
);
""")
conn.commit()

# ====================== إعدادات Streamlit ======================
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

    /* الشريط السفلي */
    .news-bar{
        position:fixed;
        bottom:0;
        right:0;
        width:100%;
        height:45px;
        background:#000814;
        border-top:3px solid gold;
        overflow:hidden;
        z-index:999999;
    }

    .news-text{
        position:absolute;
        white-space:nowrap;
        font-size:21px;
        font-weight:bold;
        line-height:45px;
        animation:scrollText 40s linear infinite;
    }

    @keyframes scrollText{
        0%   { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
</style>
""", unsafe_allow_html=True)

# اللوجو + العنوان
st.markdown('<div class="logo">⚖️</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">إدارة القضايا</div>', unsafe_allow_html=True)

# ====================== الشريط السفلي ======================
st.markdown("""
<div class="news-bar">
    <div class="news-text">
        مع تحيات / وليد حماد &nbsp;&nbsp;|&nbsp;&nbsp; 
        الإدارة العامة للشئون القانونية &nbsp;&nbsp;|&nbsp;&nbsp; 
        ديوان عام منطقة البحيرة &nbsp;&nbsp;|&nbsp;&nbsp; 
        الهيئة القومية للتأمين الاجتماعى
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
        if st.button("📊 التقارير", use_container_width=True):
            st.session_state.page = "reports"; st.rerun()

# ====================== تسجيل قضية ======================
if st.session_state.page == "cases":
    st.subheader("⚖️ تسجيل قضية جديدة")
    st.info("صفحة التسجيل تحتاج توسيع - يمكنك إضافتها من النسخ السابقة")
    if st.button("⬅ العودة"):
        st.session_state.page = "home"; st.rerun()

# ====================== الحصر العام (جدول) ======================
if st.session_state.page == "inventory":
    st.subheader("📋 الحصر العام للقضايا")

    cur.execute("""
        SELECT c.id, c.case_number, c.judicial_year, c.circuit, c.case_category,
               c.court_name, c.mission, c.plaintiff, c.defendant,
               (SELECT session_date FROM sessions WHERE case_id = c.id ORDER BY session_date DESC LIMIT 1) as last_session,
               (SELECT procedure FROM sessions WHERE case_id = c.id ORDER BY session_date DESC LIMIT 1) as last_procedure
        FROM cases c ORDER BY c.id DESC
    """)
    rows = cur.fetchall()

    if not rows:
        st.warning("لا توجد قضايا مسجلة")
    else:
        for row in rows:
            case_id = row[0]
            opponents = f"{(row[7] or '')[:25]} ضد {(row[8] or '')[:25]}"

            cols = st.columns([1.5,1,1.2,1.2,2,1.2,3.5,1.8,2.5,1,1,1])
            cols[0].write(row[1])           # رقم الدعوى
            cols[1].write(row[2])           # السنة
            cols[2].write(row[3])           # الدائرة
            cols[3].write(row[4])           # النوع
            cols[4].write(row[5])           # اسم المحكمة
            cols[5].write(row[6] or "—")    # المأمورية
            cols[6].write(opponents)        # الخصوم
            cols[7].write(row[9] or "—")    # آخر جلسة
            cols[8].write((row[10] or "—")[:60])  # سبب الجلسة

            with cols[9]:
                if st.button("📂", key=f"o{case_id}"):
                    st.session_state.selected_case = case_id
                    st.session_state.page = "case_details"
                    st.rerun()
            with cols[10]:
                if st.button("✏️", key=f"e{case_id}"):
                    st.session_state.selected_case = case_id
                    st.session_state.page = "edit_case"
                    st.rerun()
            with cols[11]:
                if st.button("🗑", key=f"d{case_id}"):
                    st.session_state.delete_case_id = case_id

            if st.session_state.delete_case_id == case_id:
                st.warning("هل تريد حذف القضية؟")
                if st.button("✅ نعم"):
                    cur.execute("DELETE FROM cases WHERE id=?", (case_id,))
                    cur.execute("DELETE FROM sessions WHERE case_id=?", (case_id,))
                    conn.commit()
                    st.success("تم الحذف")
                    st.session_state.delete_case_id = None
                    st.rerun()
                if st.button("❌ إلغاء"):
                    st.session_state.delete_case_id = None
                    st.rerun()

            st.markdown("---")

    if st.button("⬅ العودة"):
        st.session_state.page = "home"; st.rerun()

# ====================== صفحات أخرى (مختصرة) ======================
if st.session_state.page in ["case_details", "edit_case", "reports"]:
    st.info("هذه الصفحات تحت التطوير - يمكن توسيعها")

st.caption(" ")
