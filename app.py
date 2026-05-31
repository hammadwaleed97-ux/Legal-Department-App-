import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS ليكون مطابقاً للهوية الإدارية
st.markdown("""
    <style>
    .main-title { background: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #1a3a6e; }
    .btn-container { display: flex; justify-content: center; gap: 20px; margin-top: 30px; }
    div.stButton > button { width: 250px; height: 60px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# العنوان الرئيسي كما في 388e49a4-3715-41f3-94f8-25eea5301b47
st.markdown("""
    <div class="main-title">
        <h3>الهيئة القومية للتأمين الاجتماعي</h3>
        <h4>الإدارة العامة للشئون القانونية | ديوان عام منطقة البحيرة</h4>
        <p>إعداد: أ/ وليد شعبان حماد</p>
    </div>
    """, unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    st.write("---")
    # توزيع الأزرار حسب التقسيمة الإدارية
    col1, col2 = st.columns(2)
    
    if col1.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if col2.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()
    
    st.write("---")
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()
    if st.button("📦 الأرشيف الإلكتروني"): st.session_state.page = "الأرشيف"; st.rerun()

# منطق التنقل لباقي الصفحات (سنبدأ بناءها تباعاً)
elif st.session_state.page == "القضايا":
    # هنا سنضع محتوى القضايا الذي اتفقنا عليه
    pass
