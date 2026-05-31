import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق الموحد للوجو (الهيدر)
st.markdown("""
    <style>
    .hero-container { background-color: #1a3a6e; padding: 25px; border-radius: 20px; text-align: center; color: white; margin-bottom: 25px; }
    .hero-container h3 { font-size: 0.9em; margin: 5px; }
    div.stButton > button { width: 100%; border: 2px solid #1a3a6e; color: #1a3a6e; font-weight: bold; background-color: white; border-radius: 10px; margin-bottom: 10px; }
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

show_header()

# تبويبات النظام الأساسية (القضايا + المكتبة)
tab1, tab2 = st.tabs(["⚖️ الإدارة العامة للقضايا", "📚 المكتبة القانونية"])

with tab1:
    st.subheader("القسم القضائي")
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs(["بيانات الدعوى", "التنبيهات", "التقارير", "أرشيف الحفظ"])
    
    with sub_tab1:
        col1, col2 = st.columns(2)
        with col1:
            court = st.text_input("المحكمة")
            case_no = st.text_input("رقم الدعوى")
        with col2:
            circle = st.text_input("الدائرة")
            year = st.text_input("سنة")
        st.text_area("بيانات الخصوم والموضوع")
        st.file_uploader("ارفع صورة الصحيفة")
        if st.button("حفظ بيانات الدعوى"):
            st.success("تم الحفظ في الأرشيف")
        
        st.write("---")
        c1, c2 = st.columns(2)
        c1.text("عضو الإدارة القانونية: __________")
        c2.text("مدير الإدارة القانونية: __________")

    with sub_tab2: st.info("التنبيهات: لا توجد جلسات قريبة.")
    with sub_tab3: st.write("التقارير: إحصائيات القضايا.")
    with sub_tab4: st.write("أرشيف الحفظ: سجل القضايا المنتهية.")

with tab2:
    st.subheader("المكتبة القانونية")
    st.selectbox("اختر نوع التشريع", ["القوانين", "اللوائح", "القرارات الوزارية", "الكتب الدورية"])
    st.file_uploader("تحميل ملف جديد للمكتبة")
    st.button("فتح التشريع")
    st.info("الذكاء الاصطناعي متاح للبحث في المستندات المرفقة فقط.")

