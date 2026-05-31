import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق الموحد
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    #stDecoration { display: none !important; }
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        color: #ffffff;
        text-align: center;
        margin: -40px -10px 20px -10px;
    }
    .footer-text { font-size: 0.8rem; color: #88aacc; margin-top: 5px; }
    /* تنسيق شبكة الأزرار لتشمل 5 أقسام */
    .nav-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# الشعار
st.markdown("""
    <div class="header-frame">
        <div style="font-size: 2.5rem;">⚖️</div>
        <div style="font-size: 1.2rem; font-weight: bold;">الهيئة القومية للتأمين الاجتماعي</div>
        <div style="font-size: 1rem;">الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة</div>
        <div class="footer-text">إعداد: وليد حماد</div>
    </div>
    """, unsafe_allow_html=True)

# تهيئة حالة الصفحة
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

# نظام التنقل (استخدام صفين ليظهر بشكل ممتاز على الموبايل)
col1, col2, col3 = st.columns(3)
if col1.button("🏠 الرئيسية"): st.session_state.page = "الرئيسية"
if col2.button("📁 القضايا"): st.session_state.page = "القضايا"
if col3.button("📝 الفتاوى"): st.session_state.page = "الفتاوى"

col4, col5 = st.columns(2)
if col4.button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"
if col5.button("📚 المكتبة"): st.session_state.page = "المكتبة"

# عرض المحتوى
st.markdown("---")
if st.session_state.page == "الرئيسية":
    st.write("### 🏛️ الصفحة الرئيسية")
elif st.session_state.page == "القضايا":
    st.write("### 📁 إدارة القضايا القانونية")
elif st.session_state.page == "الفتاوى":
    st.write("### 📝 قسم الفتاوى")
elif st.session_state.page == "التحقيقات":
    st.write("### 🔍 قسم التحقيقات")
elif st.session_state.page == "المكتبة":
    st.write("### 📚 المكتبة القانونية")
