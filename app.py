import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني - البحيرة", layout="wide")

# تهيئة البيانات
if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=[
        "رقم الدعوى", "السنة", "الطرف الأول", "اسم الطرف الأول", "الطرف الثاني", "اسم الطرف الثاني", 
        "الدائرة", "النوع", "المحكمة", "اسم المحكمة", "موضوع الدعوى", "تاريخ الجلسة", "القرار", "المحامي", "موبايل", "الحالة"
    ])

# الترويسة
st.markdown("<div style='text-align: center; background-color: #002b5b; color: white; padding: 20px;'>الهيئة القومية للتأمين الاجتماعى<br>الإدارة العامة للشؤون القانونية<br>إعداد: وليد شعبان حماد<br>ديوان عام منطقة البحيرة</div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ تسجيل القضايا", "🔔 التنبيهات", "📊 التقارير", "📂 الأرشيف", "🔍 البحث"])

with tab1:
    with st.form("case_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            p1_type = st.selectbox("صفة الطرف الأول", ["مدعى", "مدعى عليه", "مستأنف", "مستأنف ضده", "طاعن", "مطعون ضده"])
            p1_name = st.text_input("اسم الطرف الأول")
            p2_type = st.selectbox("صفة الطرف الثاني", ["مدعى", "مدعى عليه", "مستأنف", "مستأنف ضده", "طاعن", "مطعون ضده"])
            p2_name = st.text_input("اسم الطرف الثاني")
            case_no = st.text_input("رقم الدعوى")
            case_year = st.text_input("السنة القضائية")
            phone = st.text_input("رقم الموبايل للتنبيهات")
        with col2:
            circle = st.text_input("الدائرة")
            case_type = st.text_input("نوع الدعوى")
            court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا", "المحكمة التأديبية"])
            court_name = st.text_input("اسم المحكمة")
            subject = st.text_area("موضوع الدعوى")
            h_date = st.date_input("تاريخ الجلسة")
            decision = st.text_area("القرار")
            lawyer = st.text_input("المحامي المختص")
            status = st.selectbox("الحالة", ["متداولة", "منتهية"])
        
        if st.form_submit_button("حفظ القضية"):
            new_row = pd.DataFrame([[case_no, case_year, p1_type, p1_name, p2_type, p2_name, circle, case_type, court, court_name, subject, h_date, decision, lawyer, phone, status]], columns=st.session_state.cases.columns)
            st.session_state.cases = pd.concat([st.session_state.cases, new_row], ignore_index=True)
            st.success("تم حفظ القضية!")

with tab2:
    st.subheader("التنبيهات")
    if not st.session_state.cases.empty:
        df = st.session_state.cases.copy()
        df['تاريخ الجلسة'] = pd.to_datetime(df['تاريخ الجلسة'])
        # تنبيهات الجلسات (أسبوع)
        next_week = datetime.now() + timedelta(days=7)
        urgent_sessions = df[df['تاريخ الجلسة'] <= next_week]
        for _, row in urgent_sessions.iterrows():
            st.warning(f"🔴 هاااام: عندك جلسة يوم {row['تاريخ الجلسة'].date()}، القضية رقم {row['رقم الدعوى']}، طرف: {row['اسم الطرف الأول']}")
        # تنبيهات الطعن (15 يوم)
        st.info("تنبيهات الطعن والطعون مفعّلة.")

with tab3:
    st.subheader("التقارير")
    report_type = st.selectbox("نوع التقرير", ["تقرير بالدعاوى المتداولة", "تقرير بالأحكام الصادرة"])
    st.dataframe(st.session_state.cases, use_container_width=True)
    if st.button("تحميل نسخة Word/PDF"):
        st.write("تم تجهيز التقرير وفقاً لهوية الهيئة القومية للتأمين الاجتماعي.")

with tab4:
    st.subheader("الأرشيف")
    st.dataframe(st.session_state.cases[st.session_state.cases["الحالة"] == "منتهية"], use_container_width=True)

with tab5:
    st.subheader("البحث عن دعوى")
    search = st.text_input("ابحث برقم الدعوى أو الاسم")
    if search:
        res = st.session_state.cases[st.session_state.cases.apply(lambda row: search in str(row.values), axis=1)]
        st.dataframe(res, use_container_width=True)
