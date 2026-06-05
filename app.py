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
# التنسيق
# =====================================

st.markdown("""
<style>

.stApp{
    background:#071d45;
}

.stButton button{
    width:100%;
    background:#1d4ed8;
    color:white;
    border:none;
    border-radius:12px;
    padding:15px;
    font-size:18px;
    font-weight:bold;
}

.stButton button:hover{
    background:#2563eb;
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
# اللوجو
# =====================================

st.markdown("""
<div style="text-align:center;">

<div style="
font-size:90px;
margin-bottom:10px;
">
⚖️
</div>

<div style="
font-size:24px;
font-weight:bold;
color:white;
white-space:nowrap;
">
الهيئة القومية للتأمين الاجتماعى
</div>

<br>

<div style="
font-size:22px;
font-weight:bold;
color:white;
white-space:nowrap;
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

c1,c2,c3 = st.columns(3)

with c1:
    if st.button("إدارة القضايا"):
        st.session_state.page = "cases"

with c2:
    if st.button("التنبيهات"):
        st.session_state.page = "alerts"

with c3:
    if st.button("التقارير"):
        st.session_state.page = "reports"

# الصف الثاني

c4,c5,c6 = st.columns(3)

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
