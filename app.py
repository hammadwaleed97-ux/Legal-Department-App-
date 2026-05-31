import streamlit as st

# الإعدادات
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق الموحد
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .header-frame { background: linear-gradient(135deg, #0b1e30, #1a3a6e); padding: 20px; color: white; text-align: center; border-radius: 0 0 20px 20px; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""<div class="header-frame"><h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3><p>الإدارة العامة للشئون القانونية | مع تحيات أ/ وليد حماد</p></div>""", unsafe_allow_html=True)

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    show_header()
    st.write("### لوحة التحكم الرئيسية")
    # الأيقونات (تم دمج التنبيهات والتقارير داخل القضايا)
    if st.button("📁 إدارة القضايا والتنبيهات"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الفتاوى"): st.session_state.page = "الفتاوى"; st.rerun()
    if st.button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📚 المكتبة"): st.session_state.page = "المكتبة"; st.rerun()
    if st.button("📦 الأرشيف"): st.session_state.page = "الأرشيف"; st.rerun()

elif st.session_state.page == "القضايا":
    show_header()
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    
    st.header("📁 إدارة القضايا والتنبيهات")
    
    # تبويبات داخل القضايا
    tab1, tab2, tab3 = st.tabs(["تسجيل قضية جديدة", "متابعة وتنبيهات الجلسات", "تقارير الإنجاز"])
    
    with tab1:
        st.subheader("بيانات الدعوى")
        # نموذج تسجيل القضية (المحكمة، الرقم، السنة، الخ)
        st.text_input("رقم القضية")
        st.date_input("تاريخ الجلسة القادمة")
        st.button("حفظ القضية")
        
    with tab2:
        st.subheader("🔔 تنبيهات الجلسات")
        st.warning("تنبيه: توجد جلسة غداً للقضية رقم...")
        
    with tab3:
        st.subheader("📊 تقارير الإنجاز")
        st.write("إحصائية القضايا التي تم إنجازها هذا الشهر.")
