import streamlit as st

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background:#031d4a;
}

.main{
    background:#031d4a;
}

.title{
    color:white;
    text-align:center;
    font-size:52px;
    font-weight:bold;
}

.subtitle{
    color:white;
    text-align:center;
    font-size:40px;
    font-weight:bold;
}

.text{
    color:white;
    text-align:center;
    font-size:34px;
    font-weight:bold;
}

.stButton>button{
    width:100%;
    height:70px;
    border-radius:15px;
    font-size:20px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# اللوجو
# ==========================

st.markdown(
"""
<div style="text-align:center;font-size:120px;">
⚖️
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="title">
الهيئة القومية للتأمين الاجتماعى
</div>
""",
unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
"""
<div class="subtitle">
الإدارة العامة للشؤون القانونية
</div>
""",
unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
"""
<div class="text">
إعداد
</div>

<br>

<div class="text">
وليد شعبان حماد
</div>

<br>

<div class="text">
ديوان عام منطقة البحيرة
</div>
""",
unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# ==========================
# الصف الأول
# ==========================

c1,c2,c3 = st.columns(3)

with c1:
    st.button("تسجيل القضايا")

with c2:
    st.button("التنبيهات")

with c3:
    st.button("التقارير")

# ==========================
# الصف الثاني
# ==========================

c4,c5,c6 = st.columns(3)

with c4:
    st.button("أرشيف القضايا")

with c5:
    st.button("البحث عن دعوى")

with c6:
    st.button("القضايا المحذوفة")
