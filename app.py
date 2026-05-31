import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تهيئة الحالة
if 'page' not in st.session_state: st.session_state.page = "main"

# التنسيق الموحد
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .hero-container { background-color: #1a3a6e; padding: 25px; border-radius: 20px; text-align: center; color: white; margin-bottom: 25px; }
    .hero-container h3 { font-size: 0.9em; margin: 5px; }
    .button-container { display: flex; flex-direction: column; align-items: center; }
    div.stButton > button { width: 350px; height: 50px; border: 2px solid #1a3a6e; color: #1a3a6e; font-weight: bold; background-color: white; border-radius: 10px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div class="hero-container">
            <h3>الهيئة القومية للتأمين الاجتماعي</h3>
            <p>الإدارة العامة للشئون القانونية</p>
            <p>ديوان عام منطقة البحيرة</p>
            <hr style="border-top: 1px solid white;">
            <p>إعداد: أ/ وليد حماد</p>
        </div>
        """, unsafe_allow_html=True)

# 1. الواجهة الرئيسية
if st.session_state.page == "main":
    show_header()
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()
    if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 2. الإدارة العامة للقضايا
elif st.session_state.page == "القضايا":
    show_header()
    st.subheader("⚖️ الإدارة العامة للقضايا")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["القضاء العادي", "محكمة النقض", "مجلس الدولة", "تسجيل الدعاوى والطعون", "التنبيهات والتقارير"])
    with tab1: st.write("صياغة مذكرات (مدعي/مدعى عليه)، استئناف، مذكرات استئنافية")
    with tab2: st.write("صياغة طعون، مذكرات دفاع (طاعن/مطعون ضده)")
    with tab3: st.write("المحاكم الإدارية، التأديبية، القضاء الإداري، الإدارية العليا")
    with tab4: st.write("تسجيل الدعاوى والطعون وأرشيف الحفظ")
    with tab5: st.write("التنبيهات، التقارير، البحث عن سابقة فصل")
    if st.button("العودة للرئيسية"): st.session_state.page = "main"; st.rerun()

# 3. الإدارة العامة للفتوى
elif st.session_state.page == "الفتوى":
    show_header()
    st.subheader("📝 الإدارة العامة للفتوى")
    st.write("فتاوى، إصابات عمل، شكاوى الزواج العرفي، أرشيف الفتاوى")
    if st.button("العودة للرئيسية"): st.session_state.page = "main"; st.rerun()

# 4. التحقيقات والنيابات
elif st.session_state.page == "التحقيقات":
    show_header()
    st.subheader("🔍 الإدارة العامة للتحقيقات والنيابات")
    st.write("تحقيقات الهيئة، النيابة الإدارية، النيابة العامة، أرشيف التحقيقات")
    if st.button("العودة للرئيسية"): st.session_state.page = "main"; st.rerun()

# 5. المكتبة القانونية
elif st.session_state.page == "المكتبة":
    show_header()
    st.subheader("📚 المكتبة القانونية")
    st.write("قوانين، لوائح، قرارات وزارية، منشورات، تعليمات، أحكام قضائية، مذكرات فنية")
    if st.button("العودة للرئيسية"): st.session_state.page = "main"; st.rerun()
