import streamlit as st

# 1. إعداد الصفحة لتعمل بكامل العرض
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# 2. التنسيق: إخفاء السهم، القائمة الجانبية، والشريط العلوي تماماً
st.markdown("""
    <style>
    /* إخفاء القائمة الجانبية (Sidebar) */
    [data-testid="stSidebar"] { display: none !important; }
    
    /* إخفاء شريط الأدوات العلوي (Toolbar/Decoration) الذي أشرت إليه */
    #stDecoration { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 20px;
        border-radius: 0 0 20px 20px;
        color: #ffffff;
        text-align: center;
        margin: -40px -10px 20px -10px;
    }
    .footer-text { font-size: 0.8rem; color: #88aacc; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. عرض الهوية داخل الإطار
st.markdown("""
    <div class="header-frame">
        <div style="font-size: 2.5rem;">⚖️</div>
        <div style="font-size: 1.2rem; font-weight: bold;">الهيئة القومية للتأمين الاجتماعي</div>
        <div style="font-size: 1rem;">الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة</div>
        <div class="footer-text">إعداد: وليد حماد</div>
    </div>
    """, unsafe_allow_html=True)

# 4. تهيئة حالة الصفحة
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

# 5. نظام التنقل بالأزرار (صفين ليظهر بشكل ممتاز على الموبايل)
st.markdown("---")
col1, col2, col3 = st.columns(3)
if col1.button("🏠 الرئيسية"): st.session_state.page = "الرئيسية"
if col2.button("📁 القضايا"): st.session_state.page = "القضايا"
if col3.button("📝 الفتاوى"): st.session_state.page = "الفتاوى"

col4, col5 = st.columns(2)
if col4.button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"
if col5.button("📚 المكتبة"): st.session_state.page = "المكتبة"

# 6. عرض المحتوى بناءً على اختيار المستخدم
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
