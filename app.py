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
# قاعدة البيانات
# =====================================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

.stApp{
    background:#062456;
}

/* النصوص */

h1,h2,h3,h4,h5,h6,
label,p,span{
    color:white !important;
}

/* القوائم المنسدلة */

.stSelectbox div[data-baseweb="select"] > div{
    background:white !important;
    color:black !important;
}

div[role="option"]{
    background:white !important;
    color:black !important;
}

div[role="listbox"] div{
    color:black !important;
}

[data-baseweb="popover"] *{
    color:black !important;
}

/* الإدخال */

.stTextInput input{
    color:black !important;
}

.stTextArea textarea{
    color:black !important;
}

.stDateInput input{
    color:black !important;
}

/* اللوجو */

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:52px;
    margin-top:15px;
    margin-bottom:10px;
}

.logo-main{
    font-size:26px;
    font-weight:900;
    color:white;
    text-shadow:2px 2px 4px black;
    margin-bottom:12px;
    white-space:nowrap;
}

.logo-sub{
    font-size:24px;
    font-weight:900;
    color:white;
    text-shadow:2px 2px 4px black;
    margin-bottom:12px;
}

.logo-place{
    font-size:22px;
    font-weight:900;
    color:white;
    text-shadow:2px 2px 4px black;
    margin-bottom:20px;
}

.logo-greeting{
    font-size:20px;
    font-weight:bold;
    color:white;
    margin-bottom:10px;
}

.logo-name{
    font-size:32px;
    font-weight:900;
    color:#FFD700;
    text-shadow:2px 2px 4px black;
    margin-bottom:30px;
}

/* الأزرار */

div.stButton > button{
    width:340px;
    height:65px;
    border-radius:15px;
    border:none;
    background:#2f55d4;
    color:white;
    font-size:20px;
    font-weight:bold;
    display:block;
    margin:auto;
}

div.stButton > button:hover{
    background:#4b6df0;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# اللوجو
# =====================================

st.markdown("""

<div class="logo-box">

<div class="logo-icon">
⚖️
</div>

<div class="logo-main">
الهيئة القومية للتأمين الاجتماعى
</div>

<div class="logo-sub">
الإدارة العامة للشؤون القانونية
</div>

<div class="logo-place">
ديوان عام منطقة البحيرة
</div>

<div class="logo-greeting">
مع تحيات
</div>

<div class="logo-name">
وليد شعبان حماد
</div>

</div>

""", unsafe_allow_html=True)

# =====================================
# الصفحات
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

# =====================================
# القائمة الرئيسية
# =====================================

col1, col2, col3 = st.columns([1,2,1])

with col2:

    if st.button("⚖️ تسجيل القضايا"):
        st.session_state.page = "cases"

    if st.button("🔔 التنبيهات"):
        st.session_state.page = "alerts"

    if st.button("📊 التقارير"):
        st.session_state.page = "reports"

    if st.button("📂 أرشيف القضايا"):
        st.session_state.page = "archive"

    if st.button("📋 حصر عام القضايا المتداولة"):
        st.session_state.page = "all_cases"

    if st.button("🔍 البحث عن دعوى"):
        st.session_state.page = "search"

    if st.button("❌ القضايا المحذوفة"):
        st.session_state.page = "deleted"
# =====================================
# إنشاء جدول القضايا
# =====================================

cur.execute("""

CREATE TABLE IF NOT EXISTS cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

litigation_type TEXT,

claimant_type TEXT,
claimant TEXT,

defendant_type TEXT,
defendant TEXT,

case_no TEXT,

judicial_year TEXT,

circuit TEXT,

case_type TEXT,

court TEXT,

court_name TEXT,

subject TEXT,

session_date TEXT,
session_action TEXT,

decision_date TEXT,
decision_action TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

status TEXT DEFAULT 'متداولة',

created_at TEXT

)

""")

# =====================================
# جدول القضايا المحذوفة
# =====================================

cur.execute("""

CREATE TABLE IF NOT EXISTS deleted_cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

original_case_id INTEGER,

litigation_type TEXT,

claimant TEXT,

defendant TEXT,

case_no TEXT,

judicial_year TEXT,

subject TEXT,

delete_reason TEXT,

deleted_at TEXT

)

""")

conn.commit()

# =====================================
# تعريف الصفحات
# =====================================

if st.session_state.page == "alerts":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    🔔 التنبيهات
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة التنبيهات فى الجزء القادم")

elif st.session_state.page == "reports":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📊 التقارير
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة التقارير فى الجزء القادم")

elif st.session_state.page == "archive":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📂 أرشيف القضايا
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة الأرشيف فى الجزء القادم")

elif st.session_state.page == "all_cases":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📋 حصر عام القضايا المتداولة
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة الحصر العام فى الجزء القادم")

elif st.session_state.page == "search":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    🔍 البحث عن دعوى
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة البحث فى الجزء القادم")

elif st.session_state.page == "deleted":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    ❌ القضايا المحذوفة
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة سجل المحذوفات فى الجزء القادم")
