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
# التصميم
# =====================================

st.markdown("""
<style>

.stApp{
    background:#071d45;
    direction:rtl;
}

h1,h2,h3,h4,h5,h6,p,label{
    color:white !important;
    text-align:center;
}

.stButton button{
    background:#1d4ed8;
    color:white;
    border:none;
    border-radius:12px;
    width:100%;
    font-size:18px;
    font-weight:bold;
    padding:12px;
}

.stButton button:hover{
    background:#2563eb;
}

div[data-baseweb="select"] *{
    color:black !important;
}

input, textarea{
    color:black !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# قاعدة البيانات
# =====================================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

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

decision_date TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

status TEXT DEFAULT 'متداولة'
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS deleted_cases(

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

decision_date TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

delete_reason TEXT,

delete_date TEXT
)
""")

conn.commit()

# =====================================
# اللوجو الرئيسي
# =====================================

st.markdown("""
<div style='text-align:center'>

<div style='font-size:90px'>
⚖️
</div>

<h1>
الهيئة القومية للتأمين الاجتماعى
</h1>

<h2>
الإدارة العامة للشؤون القانونية
</h2>

<br>

<h3>
إعداد
</h3>

<h3>
وليد شعبان حماد
</h3>

<h3>
ديوان عام منطقة البحيرة
</h3>

</div>
""", unsafe_allow_html=True)

st.write("")

# =====================================
# القائمة الرئيسية
# =====================================

c1,c2,c3,c4,c5,c6 = st.columns(6)

if "page" not in st.session_state:
    st.session_state.page = "cases"

with c1:
    if st.button("إدارة القضايا"):
        st.session_state.page = "cases"

with c2:
    if st.button("التنبيهات"):
        st.session_state.page = "alerts"

with c3:
    if st.button("التقارير"):
        st.session_state.page = "reports"

with c4:
    if st.button("أرشيف القضايا"):
        st.session_state.page = "archive"

with c5:
    if st.button("البحث عن دعوى"):
        st.session_state.page = "search"

with c6:
    if st.button("القضايا المحذوفة"):
        st.session_state.page = "deleted"

page = st.session_state.page
