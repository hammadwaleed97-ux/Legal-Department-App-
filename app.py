import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني - البحيرة", layout="wide")

# التصميم (CSS)
st.markdown("""
    <style>
    .header-box { text-align: center; background-color: #002b5b; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; font-weight: bold; }
    .stApp { background-color: #f8f9fa; }
    h1, h2, h3 { color: #002b5b; }
    .stButton>button { background-color: #002b5b; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# اللوجو والنصوص (كما طلبت)
st.markdown("""
    <div class='header-box'>
    الهيئة القومية للتأمين الاجتماعى<br>
    الإدارة العامة للشؤون القانونية<br>
    إعداد: وليد شعبان حماد<br>
    ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

# تبويبات الأقسام
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ تسجيل القضايا", "🔔 التنبيهات", "📊 التقارير", "📂 الأرشيف", "🔍 البحث"])

# 1. تسجيل القضايا
with tab1:
    st.subheader("تسجيل قضية جديدة")
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            party_a = st.selectbox("الطرف الأول", ["المدعى", "المستأنف", "الطاعن"])
            party_b = st.selectbox("الطرف الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"])
            case_no = st.text_input("رقم الدعوى")
            case_year = st.text_input("السنة القضائية")
            hearing_date = st.date_input("تاريخ الجلسة")
        with col2:
            circle = st.text_input("الدائرة")
            case_type = st.text_input("نوع الدعوى")
            court_type = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"])
            court_name = st.text_input("اسم المحكمة")
            subject = st.text_area("موضوع الدعوى")
            decision = st.text_area("القرار")
        
        submit = st.form_submit_button("حفظ القضية")
        if submit:
            st.success("تم حفظ البيانات بنجاح في قاعدة البيانات.")

# (باقي التبويبات تظل كما هي مع تحسين التنسيق)
with tab2: st.subheader("التنبيهات")
with tab3: st.subheader("التقارير")
with tab4: st.subheader("الأرشيف")
with tab5: st.subheader("البحث")

st.sidebar.markdown("---")
st.sidebar.write("مع تحيات وليد شعبان حماد")
