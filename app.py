import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تهيئة حالة الصفحة
if 'page' not in st.session_state: st.session_state.page = "main"

# التنسيق العام
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
    st.subheader("⚖️ القسم القضائي")
    tabs = st.tabs(["القضاء العادي", "محكمة النقض", "مجلس الدولة", "تسجيل الدعاوى", "تسجيل الطعون", "أرشيف الحفظ", "التنبيهات والتقارير"])
    with tabs[0]: st.write("إجراءات القضاء العادي (المحاكم الابتدائية، الاستئنافية...)")
    with tabs[1]: st.write("إجراءات محكمة النقض")
    # ... وهكذا لبقية الأقسام
    if st.button("العودة للقائمة الرئيسية"): st.session_state.page = "main"; st.rerun()

# 3. الإدارة العامة للفتوى
elif st.session_state.page == "الفتوى":
    show_header()
    st.subheader("📝 قسم الإفتاء القانوني")
    st.write("فتاوى، إصابات العمل، الزواج العرفي، أرشيف الفتاوى")
    if st.button("العودة للقائمة الرئيسية"): st.session_state.page = "main"; st.rerun()

# 4. الإدارة العامة للتحقيقات
elif st.session_state.page == "التحقيقات":
    show_header()
    st.subheader("🔍 الإدارة العامة للتحقيقات والنيابات")
    st.write("تحقيقات الهيئة، النيابة الإدارية، النيابة العامة، أرشيف التحقيقات")
    if st.button("العودة للقائمة الرئيسية"): st.session_state.page = "main"; st.rerun()

# 5. المكتبة القانونية
elif st.session_state.page == "المكتبة":
    show_header()
    st.subheader("📚 المكتبة القانونية المتكاملة")
    st.write("القوانين، اللوائح، القرارات، المنشورات، الكتب الدورية، فتاوى مجلس الدولة، أحكام قضائية")
    if st.button("العودة للقائمة الرئيسية"): st.session_state.page = "main"; st.rerun()
