import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق الموحد (اللوجو والألوان)
st.markdown("""
    <style>
    .hero-container { background-color: #1a3a6e; padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px; }
    div.stButton > button { width: 100%; border: 2px solid #1a3a6e; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# الهيدر الموحد
def show_header():
    st.markdown("""
        <div class="hero-container">
            <h3>الهيئة القومية للتأمين الاجتماعي</h3>
            <p>الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</p>
            <p>إعداد: أ/ وليد حماد</p>
        </div>
        """, unsafe_allow_html=True)

show_header()

# التبويبات الرئيسية
tab1, tab2 = st.tabs(["⚖️ القسم القضائي", "📚 المكتبة القانونية"])

# محتوى القسم القضائي
with tab1:
    sub1, sub2, sub3, sub4 = st.tabs(["بيانات الدعوى", "التنبيهات", "التقارير", "أرشيف الحفظ"])
    
    with sub1:
        st.text_input("المحكمة")
        st.text_input("رقم الدعوى")
        st.text_input("الدائرة")
        st.text_input("سنة")
        st.text_area("بيانات الخصوم والموضوع")
        st.file_uploader("ارفع صورة الصحيفة", type=['png', 'jpg', 'pdf'])
        
        # أزرار الإجراءات الأساسية
        st.button("صياغة المذكرة")
        col1, col2 = st.columns(2)
        col1.button("حفظ Word")
        col2.button("حفظ PDF")
        
        st.write("---")
        st.text("عضو الإدارة القانونية: __________ | مدير الإدارة القانونية: __________")

    with sub2: st.info("التنبيهات: سجل متابعة الجلسات")
    with sub3: st.info("التقارير: إحصائيات الإنجاز")
    with sub4: st.info("أرشيف الحفظ: القضايا المنتهية")

# محتوى المكتبة القانونية
with tab2:
    options = ["القوانين", "اللوائح", "القرارات الوزارية", "الكتب الدورية"]
    st.selectbox("اختر نوع التشريع", options)
    st.file_uploader("تحميل المستند")
    st.button("فتح التشريع")
    st.info("الذكاء الاصطناعي متاح للبحث في المستندات المرفقة فقط.")
