import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS بالأزرق الداكن
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .header-box {
        border: 2px solid #1a3a6e;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 30px;
    }
    .header-box h3, .header-box h4, .header-box p { color: #1a3a6e; }
    div.stButton > button {
        width: 100%;
        border: 1px solid #1a3a6e;
        color: #1a3a6e;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي الموحد
st.markdown("""
    <div class="header-box">
        <h3>الهيئة القومية للتأمين الاجتماعي</h3>
        <h4>الإدارة العامة للشئون القانونية | ديوان عام منطقة البحيرة</h4>
        <p>إعداد: أ/ وليد شعبان حماد</p>
    </div>
    """, unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    # توزيع الأزرار حسب التقسيمة
    if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()
    if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()
    if st.button("📦 الأرشيف الإلكتروني"): st.session_state.page = "الأرشيف"; st.rerun()

elif st.session_state.page == "القضايا":
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    st.header("⚖️ الإدارة العامة للقضايا")
    # هنا سيتم وضع تفاصيل القضايا
