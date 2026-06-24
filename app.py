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
# =====================================
# الشريط السفلي المتحرك الاحترافي
# =====================================

st.markdown("""
<style>

.news-bar{
    position:fixed;
    bottom:0;
    right:0;
    width:100%;
    height:42px;
    background:#000814;
    border-top:2px solid gold;
    overflow:hidden;
    z-index:999999;
}

.news-text{
    position:absolute;
    white-space:nowrap;
    line-height:42px;
    font-size:20px;
    font-weight:bold;
    right:-2200px;
    animation:
        newsmove 35s linear infinite,
        colorchange 6s linear infinite;
}

@keyframes newsmove{
    from{
        right:-2200px;
    }
    to{
        right:100%;
    }
}

@keyframes colorchange{

    0%{
        color:#FFD700;
        text-shadow:0 0 10px #FFD700;
    }

    25%{
        color:#00FFFF;
        text-shadow:0 0 10px #00FFFF;
    }

    50%{
        color:#7FFF00;
        text-shadow:0 0 10px #7FFF00;
    }

    75%{
        color:#FF4500;
        text-shadow:0 0 10px #FF4500;
    }

    100%{
        color:#FFD700;
        text-shadow:0 0 10px #FFD700;
    }

}

</style>

<div class="news-bar">

<div class="news-text">

⚖️ مع تحيات / وليد حماد — الإدارة العامة للشئون القانونية — ديوان عام منطقة البحيرة — الهيئة القومية للتأمين الاجتماعى ⚖️

</div>

</div>

""", unsafe_allow_html=True)
