import streamlit as st

# =====================================
# إعداد الصفحة
# =====================================

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =====================================
# تنسيق البرنامج
# =====================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        to bottom,
        #001f3f,
        #003366,
        #001f3f
    );
}

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white !important;
}

.stButton > button{
    width:100%;
    height:120px;
    font-size:24px;
    font-weight:bold;
    border-radius:20px;
    border:2px solid gold;
    background:linear-gradient(
        135deg,
        #0d47a1,
        #1565c0
    );
    color:white;
}

.stButton > button:hover{
    transform:scale(1.03);
}

.footer{
    text-align:center;
    color:gold;
    font-size:22px;
    font-weight:bold;
    animation: glow 2s infinite alternate;
}

@keyframes glow{
    from{
        opacity:0.4;
    }
    to{
        opacity:1;
    }
}

</style>
""", unsafe_allow_html=True)

# =====================================
# اللوجو
# =====================================

st.markdown(
"""
<div style='text-align:center'>

<h1 style='font-size:70px'>
⚖️
</h1>

<h1>
إدارة القضايا
</h1>

</div>
""",
unsafe_allow_html=True
)

st.markdown("---")

# =====================================
# القائمة الرئيسية
# =====================================

left,center,right = st.columns([1,3,1])

with center:

    col1,col2,col3 = st.columns(3)

    with col1:
        st.button("⚖️\nتسجيل القضايا")

    with col2:
        st.button("📋\nالحصر العام")

    with col3:
        st.button("🔔\nالتنبيهات")

    st.markdown("<br>", unsafe_allow_html=True)

    col4,col5,col6 = st.columns(3)

    with col4:
        st.button("📊\nالتقارير")

    with col5:
        st.button("🗄️\nالأرشيف")

    with col6:
        st.button("📚\nالمكتبة القانونية")

# =====================================
# تذييل الصفحة
# =====================================

st.markdown("<br><br><br>", unsafe_allow_html=True)

st.markdown(
"""
<div class='footer'>

مع تحيات / وليد حماد

<br>

الإدارة العامة للشئون القانونية

<br>

ديوان عام منطقة البحيرة

<br>

الهيئة القومية للتأمين الاجتماعي

</div>
""",
unsafe_allow_html=True
)
