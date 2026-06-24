import streamlit as st

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.main {
    background: linear-gradient(to bottom,#001f3f,#003366);
}

h1,h2,h3,h4,h5,h6,p,label{
    color:white !important;
}

.stButton>button{
    width:100%;
    background:#0d6efd;
    color:white;
    border-radius:12px;
    height:60px;
    font-size:22px;
    font-weight:bold;
}

.footer {
    text-align:center;
    color:gold;
    font-size:22px;
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    from {
        opacity:0.5;
    }
    to {
        opacity:1;
    }
}

</style>
""", unsafe_allow_html=True)

# =========================
# اللوجو
# =========================

st.markdown(
"""
<div style='text-align:center'>
<h1>⚖️</h1>
<h1>إدارة القضايا</h1>
</div>
""",
unsafe_allow_html=True
)

st.divider()

# =========================
# الأقسام
# =========================

col1,col2,col3 = st.columns(3)

with col1:
    st.button("⚖️ تسجيل القضايا")

with col2:
    st.button("📋 الحصر العام")

with col3:
    st.button("🔔 التنبيهات")

col4,col5,col6 = st.columns(3)

with col4:
    st.button("📊 التقارير")

with col5:
    st.button("🗄️ الأرشيف")

with col6:
    st.button("📚 المكتبة القانونية")

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
"""
<div class='footer'>
مع تحيات / وليد حماد <br>
الإدارة العامة للشئون القانونية <br>
ديوان عام منطقة البحيرة <br>
الهيئة القومية للتأمين الاجتماعي
</div>
""",
unsafe_allow_html=True
)
