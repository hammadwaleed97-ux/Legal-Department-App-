import streamlit as st

st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

if 'page' not in st.session_state: st.session_state.page = "main"

st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .hero-container { background-color: #1a3a6e; padding: 20px; border-radius: 15px; color: white; text-align: center; }
    div.stButton > button { width: 100%; border: 2px solid #1a3a6e; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown('<div class="hero-container"><h3>الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشئون القانونية</h3><p>ديوان عام منطقة البحيرة | إعداد: أ/ وليد حماد</p></div>', unsafe_allow_html=True)

# 1. القضايا
def render_qadaya():
    show_header()
    tab1, tab2, tab3 = st.tabs(["القضاء العادي", "محكمة النقض", "مجلس الدولة"])
    with tab1:
        st.subheader("بيانات القضاء العادي")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("المحكمة")
            st.text_input("رقم الدعوى")
        with col2:
            st.text_input("الدائرة")
            st.text_input("السنة")
        st.text_area("بيانات الخصوم والموضوع")
    if st.button("العودة"): st.session_state.page = "main"; st.rerun()

# 2. الفتوى
def render_fatwa():
    show_header()
    st.subheader("سجل الفتاوى القانونية")
    st.text_input("موضوع الفتوى")
    st.text_area("نص الاستفسار الوارد")
    st.text_area("الرأي القانوني (الفتوى)")
    st.text_input("جهة الصدور")
    if st.button("العودة"): st.session_state.page = "main"; st.rerun()

# 3. التحقيقات
def render_tahqiqat():
    show_header()
    st.subheader("سجل التحقيقات والنيابات")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("رقم التحقيق")
        st.text_input("اسم المحال للتحقيق")
    with col2:
        st.text_input("السنة")
        st.text_input("الجهة المحال إليها")
    st.text_area("مذكرة التصرف")
    if st.button("العودة"): st.session_state.page = "main"; st.rerun()

# 4. المكتبة
def render_maktaba():
    show_header()
    st.subheader("المكتبة القانونية - بحث")
    st.text_input("عنوان التشريع أو الحكم")
    st.selectbox("نوع المستند", ["قانون", "قرار وزاري", "كتاب دوري", "حكم محكمة"])
    st.text_area("نص المستند أو ملخص الحكم")
    if st.button("العودة"): st.session_state.page = "main"; st.rerun()

# التنقل
if st.session_state.page == "main":
    show_header()
    if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()
    if st.button("🔍 الإدارة العامة للتحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()
elif st.session_state.page == "القضايا": render_qadaya()
elif st.session_state.page == "الفتوى": render_fatwa()
elif st.session_state.page == "التحقيقات": render_tahqiqat()
elif st.session_state.page == "المكتبة": render_maktaba()
