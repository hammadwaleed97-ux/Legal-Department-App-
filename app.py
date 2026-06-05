import streamlit as st

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background-color:#031d4a;
}

.block-container{
    padding-top:20px;
}

.title{
    text-align:center;
    color:white;
    font-size:42px;
    font-weight:bold;
}

.sub{
    text-align:center;
    color:white;
    font-size:32px;
    font-weight:bold;
}

.name{
    text-align:center;
    color:white;
    font-size:28px;
    font-weight:bold;
}

.stButton button{
    width:100%;
    height:80px;
    font-size:18px;
    font-weight:bold;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# اللوجو
st.markdown(
"""
<div style="text-align:center;font-size:90px;">
⚖️
</div>
""",
unsafe_allow_html=True
)

# العناوين
st.markdown(
'<div class="title">الهيئة القومية للتأمين الاجتماعى</div>',
unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
'<div class="sub">الإدارة العامة للشؤون القانونية</div>',
unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
'<div class="name">إعداد</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="name">وليد شعبان حماد</div>',
unsafe_allow_html=True
)

st.markdown(
'<div class="name">ديوان عام منطقة البحيرة</div>',
unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# الصف الأول
c1, c2, c3 = st.columns(3)

with c1:
    st.button("📁 تسجيل القضايا")

with c2:
    st.button("🔔 التنبيهات")

with c3:
    st.button("📊 التقارير")

st.markdown("<br>", unsafe_allow_html=True)

# الصف الثاني
c4, c5, c6 = st.columns(3)

with c4:
    st.button("🗂️ أرشيف القضايا")

with c5:
    st.button("🔎 البحث عن دعوى")

with c6:
    st.button("🗑️ القضايا المحذوفة")
