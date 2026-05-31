import streamlit as st

st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

if 'page' not in st.session_state: st.session_state.page = "main"

# التنسيق الموحد
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .hero-container { background-color: #1a3a6e; padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px; }
    div.stButton > button { width: 100%; border: 2px solid #1a3a6e; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown('<div class="hero-container"><h3>الهيئة القومية للتأمين الاجتماعي</h3><p>الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p><p>إعداد: أ/ وليد حماد</p></div>', unsafe_allow_html=True)

# 1. القضايا
def render_qadaya():
    show_header()
    tab1, tab2, tab3 = st.tabs(["القضاء العادي", "محكمة النقض", "مجلس الدولة"])
    with tab1:
        st.subheader("القضاء العادي")
        court = st.text_input("المحكمة")
        case_no = st.text_input("رقم الدعوى")
        circle = st.text_input("الدائرة")
        year = st.text_input("سنة")
        facts = st.text_area("بيانات الخصوم والموضوع")
        file = st.file_uploader("ارفع صورة الصحيفة")
        col1, col2, col3 = st.columns(3)
        col1.button("صياغة المذكرة")
        col2.button("حفظ Word")
        col3.button("حفظ PDF")
        st.write("---")
        st.text("عضو الإدارة القانونية: __________ | مدير الإدارة القانونية: __________")
        
    if st.button("العودة"): st.session_state.page = "main"; st.rerun()

# 2. الفتوى
def render_fatwa():
    show_header()
    st.subheader("الفتوى القانونية")
    st.text_area("ملخص الوقائع")
    st.text_area("مثار البحث")
    st.file_uploader("ارفع مذكرة الإحالة")
    if st.button("صياغة الرأي"): st.success("تمت الصياغة")
    col1, col2 = st.columns(2)
    col1.button("حفظ Word")
    col2.button("حفظ PDF")
    st.text("عضو الإدارة: __________ | مدير الإدارة: __________")
    if st.button("العودة"): st.session_state.page = "main"; st.rerun()

# 3. التحقيقات
def render_tahqiqat():
    show_header()
    st.subheader("التحقيقات والنيابات")
    st.text_input("رقم التحقيق / القضية")
    st.text_input("اسم المخالف")
    st.text_area("ملخص الوقائع")
    st.file_uploader("ارفع المستندات")
    st.button("صياغة مذكرة التصرف")
    col1, col2 = st.columns(2)
    col1.button("حفظ Word")
    col2.button("حفظ PDF")
    st.text("عضو الإدارة: __________ | مدير الإدارة: __________")
    if st.button("العودة"): st.session_state.page = "main"; st.rerun()

# 4. المكتبة
def render_maktaba():
    show_header()
    st.subheader("المكتبة القانونية")
    cat = st.selectbox("التصنيف", ["قوانين", "لوائح", "قرارات وزارية", "منشورات", "تعليمات", "فتاوى", "أحكام"])
    st.file_uploader(f"تحميل {cat}")
    st.button("فتح الملف")
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
