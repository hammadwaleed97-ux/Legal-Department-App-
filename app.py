import streamlit as st
import sqlite3

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
}

.stButton button{
    width:100%;
    height:75px;
    background:#2450d3;
    color:white;
    border:none;
    border-radius:15px;
    font-size:18px;
    font-weight:bold;
}

.stButton button:hover{
    background:#3564ef;
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
id INTEGER PRIMARY KEY AUTOINCREMENT
)
""")

conn.commit()

# =====================================
# اللوجو الرئيسي
# =====================================

st.markdown("""
<div style="text-align:center">

<div style="
font-size:120px;
margin-top:20px;
">
⚖️
</div>

<div style="
font-size:26px;
font-weight:bold;
color:white;
margin-top:15px;
">
الهيئة القومية للتأمين الاجتماعى
</div>

<br>

<div style="
font-size:22px;
font-weight:bold;
color:white;
">
الإدارة العامة للشؤون القانونية
</div>

<br><br>

<div style="
font-size:20px;
font-weight:bold;
color:white;
">
إعداد
</div>

<br>

<div style="
font-size:24px;
font-weight:bold;
color:white;
">
وليد شعبان حماد
</div>

<br>

<div style="
font-size:24px;
font-weight:bold;
color:white;
">
ديوان عام منطقة البحيرة
</div>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# =====================================
# القائمة الرئيسية
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

# الصف الأول

col1,col2,col3 = st.columns(3)

with col1:
    if st.button("تسجيل القضايا"):
        st.session_state.page = "cases"

with col2:
    if st.button("التنبيهات"):
        st.session_state.page = "alerts"

with col3:
    if st.button("التقارير"):
        st.session_state.page = "reports"

st.write("")

# الصف الثاني

col4,col5,col6 = st.columns(3)

with col4:
    if st.button("أرشيف القضايا"):
        st.session_state.page = "archive"

with col5:
    if st.button("البحث عن دعوى"):
        st.session_state.page = "search"

with col6:
    if st.button("القضايا المحذوفة"):
        st.session_state.page = "deleted"

page = st.session_state.page
