import streamlit as st
import pandas as pd

# الإعدادات
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")
st.markdown("<style>[data-testid='stSidebar'], #stDecoration, [data-testid='stToolbar'], header { display: none !important; } .header-frame { background: linear-gradient(135deg, #0b1e30, #1a3a6e); padding: 20px; color: white; text-align: center; border-radius: 0 0 20px 20px; }</style>", unsafe_allow_html=True)

def show_header():
    st.markdown("""<div class="header-frame"><h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3><p>الإدارة العامة للشئون القانونية | مع تحيات أ/ وليد حماد</p></div>""", unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    show_header()
    st.write("### لوحة التحكم")
    cols1 = st.columns(2)
    if cols1[0].button("📁 القضايا"): st.session_state.page = "القضايا"; st.rerun()
    if cols1[1].button("📝 الفتاوى"): st.session_state.page = "الفتاوى"; st.rerun()
    cols2 = st.columns(2)
    if cols2[0].button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if cols2[1].button("📚 المكتبة"): st.session_state.page = "المكتبة"; st.rerun()
    cols3 = st.columns(2)
    if cols3[0].button("📦 الأرشيف"): st.session_state.page = "الأرشيف"; st.rerun()
    if cols3[1].button("🔔 التنبيهات والتقارير"): st.session_state.page = "التنبيهات"; st.rerun()

elif st.session_state.page == "القضايا":
    show_header()
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    st.header("📁 إدارة القضايا")
    # هنا تضع تفاصيل القسم القضائي (التي بدأناها)
    st.radio("نوع المحاكم:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"])
    # ... (باقي الكود الخاص بالنماذج) ...

elif st.session_state.page == "التنبيهات":
    show_header()
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    st.header("🔔 التنبيهات والتقارير")
    st.info("هنا ستظهر تقارير الجلسات القادمة ومتابعة القضايا.")
