import streamlit as st
import sqlite3

# ==================================
# إعداد الصفحة
# ==================================

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# ==================================
# CSS
# ==================================

st.markdown("""
<style>

.stApp{
    background:#071d45;
}

h1,h2,h3,h4,h5,h6,p,label{
    color:white !important;
}

.stButton button{
    width:100%;
    background:#1e40af;
    color:white;
    border-radius:12px;
    border:none;
    font-size:18px;
    font-weight:bold;
    padding:14px;
}

.stButton button:hover{
    background:#2563eb;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# قاعدة البيانات
# ==================================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS cases(
id INTEGER PRIMARY KEY AUTOINCREMENT
)
""")

conn.commit()

# ==================================
# اللوجو الرئيسي
# ==================================

st.markdown("""

<div style="text-align:center;">

<div style="
font-size:100px;
margin-bottom:10px;
">
⚖️
</div>

<div style="
font-size:34px;
font-weight:bold;
color:white;
margin-bottom:25px;
">
الهيئة القومية للتأمين الاجتماعى
</div>

<div style="
font-size:28px;
font-weight:bold;
color:white;
margin-bottom:50px;
">
الإدارة العامة للشؤون القانونية
</div>

<div style="
font-size:24px;
font-weight:bold;
color:white;
margin-bottom:15px;
">
إعداد
</div>

<div style="
font-size:28px;
font-weight:bold;
color:white;
margin-bottom:15px;
">
وليد شعبان حماد
</div>

<div style="
font-size:28px;
font-weight:bold;
color:white;
margin-bottom:50px;
">
ديوان عام منطقة البحيرة
</div>

</div>

""", unsafe_allow_html=True)

# ==================================
# القائمة الرئيسية
# ==================================

if "page" not in st.session_state:
    st.session_state.page = "home"

row1_col1,row1_col2 = st.columns(2)

with row1_col1:
    if st.button("إدارة القضايا"):
        st.session_state.page = "cases"

with row1_col2:
    if st.button("التنبيهات"):
        st.session_state.page = "alerts"

row2_col1,row2_col2 = st.columns(2)

with row2_col1:
    if st.button("التقارير"):
        st.session_state.page = "reports"

with row2_col2:
    if st.button("أرشيف القضايا"):
        st.session_state.page = "archive"

row3_col1,row3_col2 = st.columns(2)

with row3_col1:
    if st.button("البحث عن دعوى"):
        st.session_state.page = "search"

with row3_col2:
    if st.button("القضايا المحذوفة"):
        st.session_state.page = "deleted"

page = st.session_state.page
