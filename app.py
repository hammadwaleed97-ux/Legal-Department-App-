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
    background-color:#062456;
}

.block-container{
    padding-top:5px;
}

label,
p,
span,
div,
h1,
h2,
h3,
h4,
h5,
h6{
    color:white !important;
    opacity:1 !important;
}

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:52px;
    margin-top:15px;
    margin-bottom:8px;
}

.logo-main{
    font-size:28px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:15px;
}

.logo-sub{
    font-size:22px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:35px;
}

.prepare{
    font-size:18px;
    margin-bottom:8px;
}

.name{
    font-size:28px;
    font-weight:bold;
    margin-bottom:12px;
}

.place{
    font-size:22px;
    font-weight:bold;
    margin-bottom:30px;
}

div.stButton > button{
    width:320px;
    height:65px;
    border-radius:18px;
    border:none;
    font-size:20px;
    font-weight:bold;
    margin:auto;
    display:block;
    background-color:#2f55d4;
    color:white;
}

div.stButton > button:hover{
    background-color:#4368e0;
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

<div class="prepare">
إعداد
</div>

<div class="name">
وليد شعبان حماد
</div>

<div class="place">
ديوان عام منطقة البحيرة
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
