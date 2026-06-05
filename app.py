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
# التصميم
# =====================

st.markdown("""
<style>

.stApp{
background:#0b1f3a;
direction:rtl;
}

h1,h2,h3,h4,h5,h6,p,label,div{
color:white !important;
}

.stButton button{
background:#163d7a;
color:white;
border-radius:10px;
font-weight:bold;
}

div[data-baseweb="select"]{
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

claimant_type TEXT,
claimant TEXT,

defendant_type TEXT,
defendant TEXT,

case_no TEXT,
judicial_year TEXT,

circuit TEXT,

case_type TEXT,

court TEXT,

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

conn.commit()

# =====================
# رأس الصفحة
# =====================

st.markdown("""
# ⚖️ الهيئة القومية للتأمين الاجتماعى

## الإدارة العامة للشؤون القانونية

### إعداد

### وليد شعبان حماد

### ديوان عام منطقة البحيرة
""")

# =====================
# القائمة الرئيسية
# =====================

c1,c2,c3,c4,c5 = st.columns(5)

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

page = st.session_state.page
