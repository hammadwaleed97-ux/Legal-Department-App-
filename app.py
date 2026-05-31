import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS ليتطابق مع 1000286358.png
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .hero-container {
        background: linear-gradient(180deg, #0b1e30 0%, #1a3a6e 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .hero-container h3, .hero-container p { color: white; margin: 5px; }
    .divider { border-top: 1px solid rgba(255,255,255,0.3); margin: 20px auto; width: 80%; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي كما في 1000286358.png
st.markdown("""
    <div class="hero-container">
        <div style="font-size: 50px;">⚖️</div>
        <h3>الهيئة القومية للتأمين الاجتماعي</h3>
        <p style="font-size: 1.2em;">الإدارة العامة للشئون القانونية</p>
        <p>ديوان عام منطقة البحيرة</p>
        <div class="divider"></div>
        <p style="opacity: 0.8;">إعداد: وليد حماد</p>
    </div>
    """, unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    # هنا ستكون أزرار الإدارات كما في التقسيمة السابقة
    if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()
    if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()
    if st.button("📦 الأرشيف الإلكتروني"): st.session_state.page = "الأرشيف"; st.rerun()
