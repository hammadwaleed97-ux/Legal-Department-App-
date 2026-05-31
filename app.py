import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: إخفاء عناصر Streamlit + اللوجو
st.markdown("""
    <style>
    [data-testid='stSidebar'], #stDecoration, [data-testid='stToolbar'], header { display: none !important; }
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 20px; color: #ffffff; text-align: center; 
        border-radius: 0 0 20px 20px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة عرض الهوية الموحدة
def show_header():
    st.markdown("""
        <div class="header-frame">
            <h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3>
            <p>الإدارة العامة للشئون القانونية | مع تحيات أ/ وليد حماد</p>
        </div>
        """, unsafe_allow_html=True)

# تهيئة الصفحة الحالية
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

# --- التنقل بين الصفحات ---
if st.session_state.page == "الرئيسية":
    show_header()
    st.write("### لوحة التحكم الرئيسية")
    
    # شبكة الأيقونات
    cols1, cols2, cols3 = st.columns(3)
    if cols1[0].button("📁 القضايا"): st.session_state.page = "القضايا"; st.rerun()
    if cols1[1].button("📝 الفتاوى"): st.session_state.page = "الفتاوى"; st.rerun()
    if cols2[0].button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if cols2[1].button("📚 المكتبة"): st.session_state.page = "المكتبة"; st.rerun()
    if cols3[0].button("📦 الأرشيف"): st.session_state.page = "الأرشيف"; st.rerun()
    if cols3[1].button("🔔 التنبيهات والتقارير"): st.session_state.page = "التنبيهات"; st.rerun()

elif st.session_state.page == "القضايا":
    show_header()
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    st.header("📁 إدارة القضايا القانونية")
    
    # تفريغ المعطيات المطلوبة (القسم القضائي)
    court_type = st.radio("اختر نوع المحاكم:", ["المحاكم الابتدائية", "المحاكم الاستئنافية", "محكمة النقض"])
    
    if court_type == "المحاكم الابتدائية":
        action = st.selectbox("اختر الإجراء:", ["صياغة مذكرة بدفاع (الهيئة مدعى عليها)", "صياغة مذكرة بدفاع (الهيئة مدعية)"])
        # هنا سنبدأ إضافة تفاصيل النموذج...
        st.write(f"جاري إعداد نموذج: {action}")

elif st.session_state.page == "التنبيهات":
    show_header()
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    st.header("🔔 التنبيهات والتقارير")
    st.info("سجل متابعة الجلسات والإنجازات القانونية.")
