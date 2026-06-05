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

h1,h2,h3,h4,h5,h6,
label,p,span{
    color:white !important;
}

.stSelectbox div[data-baseweb="select"] > div{
    background:white !important;
    color:black !important;
}

div[role="option"]{
    color:black !important;
    background:white !important;
}

div[role="listbox"] div{
    color:black !important;
}

[data-baseweb="popover"] *{
    color:black !important;
}

.stTextInput input{
    color:black !important;
}

.stTextArea textarea{
    color:black !important;
}

.stDateInput input{
    color:black !important;
}

.logo-box{
    text-align:center;
}

.logo-icon{
    font-size:50px;
    margin-top:15px;
    margin-bottom:10px;
}

.logo-main{
    font-size:28px;
    font-weight:bold;
    margin-bottom:12px;
}

.logo-sub{
    font-size:24px;
    font-weight:bold;
    margin-bottom:12px;
}

.logo-place{
    font-size:22px;
    font-weight:bold;
    margin-bottom:20px;
}

.logo-greeting{
    font-size:20px;
    margin-bottom:10px;
}

.logo-name{
    font-size:30px;
    font-weight:bold;
    margin-bottom:30px;
}

div.stButton > button{
    width:330px;
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

    if st.button("🔍 البحث عن دعوى"):
        st.session_state.page = "search"

    if st.button("❌ القضايا المحذوفة"):
        st.session_state.page = "deleted"
