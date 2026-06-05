import streamlit as st

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# ======================
# تنسيق الصفحة
# ======================

st.markdown("""
<style>

.stApp{
    background-color:#062456;
}

.block-container{
    padding-top:1rem;
}

.logo-title{
    text-align:center;
    color:white;
}

.logo-title h1{
    font-size:55px;
    margin-bottom:20px;
}

.logo-title h2{
    font-size:38px;
    margin-bottom:40px;
}

.logo-title h3{
    font-size:28px;
    margin-top:20px;
}

.main-btn{
    width:280px;
    height:85px;
    border:none;
    border-radius:20px;
    background:#2f55d4;
    color:white;
    font-size:26px;
    font-weight:bold;
    margin:10px auto;
    display:block;
}

div.stButton > button{
    width:280px;
    height:85px;
    border-radius:20px;
    font-size:24px;
    font-weight:bold;
    display:block;
    margin:auto;
}

</style>
""", unsafe_allow_html=True)

# ======================
# اللوجو
# ======================

st.markdown("""
<div class="logo-title">

<h1>⚖️</h1>

<h2>
الهيئة القومية للتأمين الاجتماعى
</h2>

<h3>
الإدارة العامة للشؤون القانونية
</h3>

<br>

<h3>إعداد</h3>

<h2>
وليد شعبان حماد
</h2>

<h3>
ديوان عام منطقة البحيرة
</h3>

</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ======================
# الأيقونات بالمنتصف
# ======================

col1,col2,col3 = st.columns([1,2,1])

with col2:

    تسجيل_القضايا = st.button("تسجيل القضايا")

    التنبيهات = st.button("التنبيهات")

    التقارير = st.button("التقارير")

    أرشيف_القضايا = st.button("أرشيف القضايا")

    البحث_عن_دعوى = st.button("البحث عن دعوى")

    القضايا_المحذوفة = st.button("القضايا المحذوفة")
