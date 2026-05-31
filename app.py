import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: اللون الأزرق الداكن وتوزيع الأزرار
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
        border: 2px solid #1a3a6e;
        color: #1a3a6e;
        font-weight: bold;
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
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

# التوزيع: 2 يمين، 2 يسار، وواحدة في المنتصف
col1, col2 = st.columns(2)

with col1:
    if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()

with col2:
    if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()

# واحدة في المنتصف بالأسفل
st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
if st.button("📦 الأرشيف الإلكتروني", use_container_width=False): st.session_state.page = "الأرشيف"; st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
