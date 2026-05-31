import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# إخفاء السهم والقائمة الجانبية تماماً
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    #stDecoration { display: none !important; }
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 30px;
        border-radius: 0 0 20px 20px;
        color: #ffffff;
        text-align: center;
        margin: -40px -10px 20px -10px;
    }
    .footer-text { font-size: 0.8rem; color: #88aacc; margin-top: 10px; border-top: 1px solid #3d5a80; padding-top: 5px; }
    .nav-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 10px; }
    .nav-btn { background: #0b1e30; color: white; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; cursor: pointer; }
    </style>
    """, unsafe_allow_html=True)

# الشعار
st.markdown("""
    <div class="header-frame">
        <div style="font-size: 3rem;">⚖️</div>
        <div style="font-size: 1.3rem; font-weight: bold;">الهيئة القومية للتأمين الاجتماعي</div>
        <div style="font-size: 1.1rem; margin-top: 5px;">الإدارة العامة للشؤون القانونية</div>
        <div style="font-size: 0.9rem; color: #a0c4e0;">ديوان عام منطقة البحيرة</div>
        <div class="footer-text">إعداد: وليد حماد</div>
    </div>
    """, unsafe_allow_html=True)

# نظام التنقل بالأزرار
col1, col2, col3, col4 = st.columns(4)
if col1.button("🏠 الرئيسية"): st.session_state.page = "الرئيسية"
if col2.button("📁 القضايا"): st.session_state.page = "القضايا"
if col3.button("📝 الفتاوى"): st.session_state.page = "الفتاوى"
if col4.button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"

# المنطق لعرض الصفحة
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    st.write("### أهلاً بك في نظام الإدارة القانونية الذكي")
elif st.session_state.page == "القضايا":
    st.write("### إدارة القضايا القانونية")
