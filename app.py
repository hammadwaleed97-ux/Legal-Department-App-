import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني - البحيرة", layout="wide")

# التصميم (CSS)
st.markdown("""
    <style>
    .header-box { text-align: center; background-color: #002b5b; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; font-weight: bold; }
    .stButton>button { background-color: #002b5b; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# اللوجو والترويسة
st.markdown("""
    <div class='header-box'>
    الهيئة القومية للتأمين الاجتماعى<br>
    الإدارة العامة للشؤون القانونية<br>
    إعداد: وليد شعبان حماد<br>
    ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ تسجيل القضايا", "🔔 التنبيهات", "📊 التقارير", "📂 الأرشيف", "🔍 البحث"])

with tab1:
    st.subheader("تسجيل قضية جديدة")
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.write("### بيانات الطرف الأول")
            party_a_type = st.selectbox("صفة الطرف الأول", ["مدعى", "مدعى عليه", "مستأنف", "مستأنف ضده", "طاعن", "مطعون ضده"])
            party_a_name = st.text_input("اسم الطرف الأول")
            
            st.write("### بيانات الطرف الثاني")
            party_b_type = st.selectbox("صفة الطرف الثاني", ["مدعى", "مدعى عليه", "مستأنف", "مستأنف ضده", "طاعن", "مطعون ضده"])
            party_b_name = st.text_input("اسم الطرف الثاني")
            
            case_no = st.text_input("رقم الدعوى")
            case_year = st.text_input("السنة القضائية")
        
        with col2:
            circle = st.text_input("الدائرة")
            case_type = st.text_input("نوع الدعوى")
            court_type = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا", "المحكمة التأديبية"])
            court_name = st.text_input("اسم المحكمة")
            
            subject = st.text_area("موضوع الدعوى")
            hearing_date = st.date_input("تاريخ الجلسة")
            decision = st.text_area("القرار")
            lawyer_name = st.text_input("المحامي المختص")
        
        submit = st.form_submit_button("حفظ القضية")
        if submit:
            st.success("تم حفظ القضية بنجاح.")

# باقي الأقسام تظل كما هي
with tab2: st.subheader("التنبيهات")
with tab3: st.subheader("التقارير")
with tab4: st.subheader("الأرشيف")
with tab5: st.subheader("البحث")
