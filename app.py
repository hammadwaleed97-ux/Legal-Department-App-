import streamlit as st
import pandas as pd

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني - البحيرة", layout="wide")

# التصميم الموحد
st.markdown("""
    <style>
    .header-box { text-align: center; background-color: #002b5b; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { background-color: #002b5b; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# الترويسة الثابتة
st.markdown("""
    <div class='header-box'>
    الهيئة القومية للتأمين الاجتماعى<br>
    الإدارة العامة للشؤون القانونية<br>
    إعداد: وليد شعبان حماد<br>
    ديوان عام منطقة البحيرة
    </div>
    """, unsafe_allow_html=True)

# تهيئة قاعدة البيانات في الذاكرة
if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=["رقم الدعوى", "الطرف الأول", "الطرف الثاني", "المحكمة", "تاريخ الجلسة", "القرار"])

# التبويبات
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ تسجيل القضايا", "🔔 التنبيهات", "📊 التقارير", "📂 الأرشيف", "🔍 البحث"])

with tab1:
    with st.form("case_form"):
        col1, col2 = st.columns(2)
        with col1:
            p1_type = st.selectbox("صفة الطرف الأول", ["مدعى", "مدعى عليه", "مستأنف", "مستأنف ضده", "طاعن", "مطعون ضده"])
            p1_name = st.text_input("اسم الطرف الأول")
            p2_type = st.selectbox("صفة الطرف الثاني", ["مدعى", "مدعى عليه", "مستأنف", "مستأنف ضده", "طاعن", "مطعون ضده"])
            p2_name = st.text_input("اسم الطرف الثاني")
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
            lawyer = st.text_input("المحامي المختص")
        
        if st.form_submit_button("حفظ القضية"):
            new_data = pd.DataFrame([[case_no, p1_name, p2_name, court_name, hearing_date, decision]], columns=st.session_state.cases.columns)
            st.session_state.cases = pd.concat([st.session_state.cases, new_data], ignore_index=True)
            st.success("تم حفظ القضية!")

with tab2:
    st.subheader("التنبيهات العاجلة")
    st.write("القضايا القريبة:")
    st.dataframe(st.session_state.cases)

with tab3:
    st.subheader("التقارير")
    st.selectbox("نوع التقرير", ["تقرير بالدعاوى المتداولة", "تقرير بالأحكام الصادرة"])
    if st.button("استخراج التقرير"):
        st.write("تم تجهيز التقرير (سيظهر هنا الجدول والتحميل)")

with tab4:
    st.subheader("أرشيف القضايا")
    st.write("القضايا المنتهية:")

with tab5:
    st.subheader("البحث")
    st.text_input("بحث بالرقم أو الاسم")
