import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =====================
# تصميم الصفحة
# =====================

st.markdown("""
<style>

.stApp{
background-color:#0b1f3a;
direction:rtl;
}

h1,h2,h3,h4,h5,h6,p,label,span{
color:white !important;
}

.stButton button{
background:#163d7a;
color:white;
border-radius:10px;
font-weight:bold;
width:100%;
}

div[data-baseweb="select"] *{
color:black !important;
}

.stTextInput input{
background:white;
color:black;
}

.stTextArea textarea{
background:white;
color:black;
}

</style>
""", unsafe_allow_html=True)

# =====================
# قاعدة البيانات
# =====================

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

# =====================
# اللوجو
# =====================

st.markdown("""
<div style='text-align:center'>

<h1>⚖️</h1>

<h2>الهيئة القومية للتأمين الاجتماعى</h2>

<h3>الإدارة العامة للشؤون القانونية</h3>

<h4>إعداد</h4>

<h4>وليد شعبان حماد</h4>

<h4>ديوان عام منطقة البحيرة</h4>

</div>
""", unsafe_allow_html=True)

# =====================
# القائمة الرئيسية
# =====================

c1,c2,c3,c4,c5,c6 = st.columns(6)

if "page" not in st.session_state:
    st.session_state.page="cases"

with c1:
    if st.button("إدارة القضايا"):
        st.session_state.page="cases"

with c2:
    if st.button("التنبيهات"):
        st.session_state.page="alerts"

with c3:
    if st.button("التقارير"):
        st.session_state.page="reports"

with c4:
    if st.button("أرشيف القضايا"):
        st.session_state.page="archive"

with c5:
    if st.button("البحث عن دعوى"):
        st.session_state.page="search"

with c6:
    if st.button("القضايا المحذوفة"):
        st.session_state.page="deleted"

page = st.session_state.page
