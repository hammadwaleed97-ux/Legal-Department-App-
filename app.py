import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية - القضايا")

# التنسيق الموحد
st.markdown("""
    <style>
    .hero-container { background-color: #1a3a6e; padding: 20px; border-radius: 15px; color: white; text-align: center; }
    div.stButton > button { width: 100%; border: 2px solid #1a3a6e; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown('<div class="hero-container"><h3>نظام إدارة القضايا القانونية</h3><p>الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p></div>', unsafe_allow_html=True)

show_header()

# تبويبات العمل القضائي
tab1, tab2, tab3, tab4 = st.tabs(["بيانات الدعوى", "التنبيهات", "التقارير", "أرشيف الحفظ"])

with tab1:
    st.subheader("إدخال بيانات الدعوى")
    col1, col2 = st.columns(2)
    with col1:
        court = st.text_input("المحكمة")
        case_no = st.text_input("رقم الدعوى")
    with col2:
        circle = st.text_input("الدائرة")
        year = st.text_input("السنة")
    
    st.text_area("بيانات الخصوم والموضوع")
    st.file_uploader("ارفع صورة الصحيفة")
    
    if st.button("حفظ بيانات الدعوى"):
        st.success("تم حفظ البيانات بنجاح في الأرشيف")
    
    st.write("---")
    c1, c2 = st.columns(2)
    c1.text("عضو الإدارة القانونية: __________")
    c2.text("مدير الإدارة القانونية: __________")

with tab2:
    st.subheader("التنبيهات القضائية")
    st.info("لا توجد جلسات قريبة في الأسبوع الحالي.")

with tab3:
    st.subheader("التقارير")
    st.write("إحصائيات القضايا المتداولة والمحجوزة للحكم.")
    st.button("تحميل تقرير كامل بصيغة PDF")

with tab4:
    st.subheader("أرشيف الحفظ")
    st.write("سجل كامل للقضايا المنتهية.")

if st.button("العودة للرئيسية"):
    st.rerun()
