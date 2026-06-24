
import streamlit as st

# =====================================
# إعداد الصفحة
# =====================================

st.set_page_config(
    page_title="",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# إخفاء عناصر Streamlit
# =====================================

st.markdown("""
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background: linear-gradient(
        180deg,
        #00152d,
        #002b5c,
        #00152d
    );
}

html, body, [class*="css"]{
    direction:rtl;
}

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

.stButton > button{
    width:100%;
    height:95px;
    font-size:24px;
    font-weight:bold;
    border-radius:20px;
    border:2px solid gold;
    background:linear-gradient(
        135deg,
        #0d47a1,
        #1565c0
    );
    color:white !important;
    box-shadow:0 0 15px rgba(255,215,0,.5);
}

.stButton > button:hover{
    transform:scale(1.03);
}

.logo{
    text-align:center;
    font-size:90px;
}

.title{
    text-align:center;
    color:gold;
    font-size:42px;
    font-weight:bold;
}

.footer{
    text-align:center;
    font-size:24px;
    font-weight:bold;
    line-height:2;
    animation:glow 2s infinite alternate;
}

@keyframes glow{
from{opacity:.4;}
to{opacity:1;}
}

</style>
""", unsafe_allow_html=True)

# =====================================
# اللوجو
# =====================================

st.markdown(
"""
<div class='logo'>
⚖️
</div>

<div class='title'>
إدارة القضايا
</div>
""",
unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================
# الأزرار في منتصف الصفحة بالطول
# =====================================

left, center, right = st.columns([2,3,2])

with center:

    st.button("⚖️ تسجيل القضايا", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("📋 الحصر العام", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("🔔 التنبيهات", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("📊 التقارير", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("🗄️ الأرشيف", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.button("📚 المكتبة القانونية", use_container_width=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
<marquee
direction="left"
scrollamount="5"
style="
position:fixed;
bottom:0;
left:0;
width:100%;
background:#000814;
border-top:2px solid gold;
padding:8px;
font-size:18px;
font-weight:bold;
z-index:9999;">

<span style="color:#FFD700;">مع تحيات / وليد حماد</span>

<span style="color:white;"> ⚖️ </span>

<span style="color:#00FFFF;">الإدارة العامة للشئون القانونية</span>

<span style="color:white;"> ⚖️ </span>

<span style="color:#7FFF00;">ديوان عام منطقة البحيرة</span>

<span style="color:white;"> ⚖️ </span>

<span style="color:#FF4500;">الهيئة القومية للتأمين الاجتماعى</span>

</marquee>
""", unsafe_allow_html=True)
