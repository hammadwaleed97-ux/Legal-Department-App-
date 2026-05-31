import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: الأزرق الداكن وتوزيع الأزرار
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .hero-container {
        background-color: #1a3a6e;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    div.stButton > button {
        width: 100%;
        height: 60px;
        border: 2px solid #1a3a6e;
        color: #1a3a6e;
        font-weight: bold;
        background-color: white;
        border-radius: 10px;
        margin-bottom: 15px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# الرأس (اللوجو)
st.markdown("""
    <div class="hero-container">
        <h3>الهيئة القومية للتأمين الاجتماعي</h3>
        <p>الإدارة العامة للشئون القانونية</p>
        <p>ديوان عام منطقة البحيرة</p>
        <hr style="border-top: 1px solid white;">
        <p>إعداد: وليد حماد</p>
    </div>
    """, unsafe_allow_html=True)

# التوزيع: 2 يمين، 2 شمال، وواحدة في المنتصف
col1, col2 = st.columns(2)

with col1:
    if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()

with col2:
    if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()

# زر الأرشيف في المنتصف تماماً
col_mid1, col_mid2, col_mid3 = st.columns([1, 2, 1])
with col_mid2:
    if st.button("📦 الأرشيف الإلكتروني"): st.session_state.page = "الأرشيف"; st.rerun()
