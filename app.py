import streamlit as st

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

st.markdown("""
<style>

.main{
    background-color:#031d4a;
}

[data-testid="stAppViewContainer"]{
    background-color:#031d4a;
}

h1,h2,h3,p{
    color:white;
    text-align:center;
}

.stButton > button{
    width:100%;
    height:120px;
    border-radius:20px;
    font-size:22px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================
# اللوجو
# =====================

st.markdown(
"""
<h1 style='font-size:120px;text-align:center'>
⚖️
</h1>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<h1>
الهيئة القومية للتأمين الاجتماعى
</h1>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<h2>
الإدارة العامة للشؤون القانونية
</h2>
""",
unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
"""
<h2>
إعداد
</h2>

<h1>
وليد شعبان حماد
</h1>

<h2>
ديوان عام منطقة البحيرة
</h2>
""",
unsafe_allow_html=True
)

st.markdown("<br><br>", unsafe_allow_html=True)

# =====================
# الصف الأول
# =====================

col1,col2,col3 = st.columns(3)

with col1:
    btn1 = st.button(
        "📁\nتسجيل القضايا",
        use_container_width=True
    )

with col2:
    btn2 = st.button(
        "🔔\nالتنبيهات",
        use_container_width=True
    )

with col3:
    btn3 = st.button(
        "📊\nالتقارير",
        use_container_width=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# =====================
# الصف الثاني
# =====================

col4,col5,col6 = st.columns(3)

with col4:
    btn4 = st.button(
        "🗂️\nأرشيف القضايا",
        use_container_width=True
    )

with col5:
    btn5 = st.button(
        "🔎\nالبحث عن دعوى",
        use_container_width=True
    )

with col6:
    btn6 = st.button(
        "🗑️\nالقضايا المحذوفة",
        use_container_width=True
    )
