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

.stApp{
    background-color:#062456;
}

.block-container{
    padding-top:10px;
}

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:90px;
    margin-bottom:10px;
}

.logo-main{
    font-size:34px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:25px;
}

.logo-sub{
    font-size:28px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:60px;
}

.prepare{
    font-size:24px;
    margin-bottom:15px;
}

.name{
    font-size:38px;
    font-weight:bold;
    margin-bottom:20px;
}

.place{
    font-size:28px;
    font-weight:bold;
    margin-bottom:50px;
}

div.stButton > button{
    width:320px;
    height:80px;
    border-radius:20px;
    border:none;
    font-size:24px;
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

# =========================
# اللوجو
# =========================

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

# =========================
# القائمة الرئيسية
# =========================

col1,col2,col3 = st.columns([1,2,1])

with col2:

    st.button("⚖️ تسجيل القضايا")

    st.button("🔔 التنبيهات")

    st.button("📊 التقارير")

    st.button("📂 أرشيف القضايا")

    st.button("🔍 البحث عن دعوى")

    st.button("❌ القضايا المحذوفة")
