import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: توسيط الأزرار وتعديل الهوية البصرية
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
    .button-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    div.stButton > button {
        width: 350px; /* تم زيادة العرض قليلاً ليناسب التصميم */
        height: 55px;
        border: 2px solid #1a3a6e;
        color: #1a3a6e;
        font-weight: bold;
        background-color: white;
        border-radius: 10px;
        margin-bottom: 12px;
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)

# الرأس (اللوجو بعد التعديل: كلمة الاجتماعي في السطر الأول)
st.markdown("""
    <div class="hero-container">
        <h3>الهيئة القومية للتأمين الاجتماعي</h3>
        <p>الإدارة العامة للشئون القانونية</p>
        <p>ديوان عام منطقة البحيرة</p>
        <hr style="border-top: 1px solid white;">
        <p>إعداد: وليد حماد</p>
    </div>
    """, unsafe_allow_html=True)

# وضع الأزرار في المنتصف
st.markdown('<div class="button-container">', unsafe_allow_html=True)

if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()
if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()
if st.button("📦 الأرشيف الإلكتروني"): st.session_state.page = "الأرشيف"; st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
