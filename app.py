import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني - البحيرة", layout="wide")

# تهيئة قاعدة البيانات مع معالجة الأعمدة المفقودة
columns = ["رقم الدعوى", "السنة", "الطرف الأول", "اسم الطرف الأول", "الطرف الثاني", "اسم الطرف الثاني", 
           "الدائرة", "النوع", "المحكمة", "اسم المحكمة", "موضوع الدعوى", "تاريخ الجلسة", "القرار", "المحامي", "رقم الموبايل", "الحالة"]

if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=columns)
else:
    # إصلاح هيكلي: إضافة الأعمدة المفقودة إذا وُجدت
    for col in columns:
        if col not in st.session_state.cases.columns:
            st.session_state.cases[col] = ""

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
            phone = st.text_input("رقم الموبايل")
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
            new_row = pd.DataFrame([[case_no, case_year, p1_type, p1_name, p2_type, p2_name, circle, case_type, court, court_name, subject, h_date, decision, lawyer, phone, status]], columns=columns)
            st.session_state.cases = pd.concat([st.session_state.cases, new_row], ignore_index=True)
            st.success("تم الحفظ!")

with tab2:
    st.subheader("التنبيهات العاجلة")
    df = st.session_state.cases.copy()
    if not df.empty:
        # تحويل التاريخ بأمان
        df['تاريخ الجلسة'] = pd.to_datetime(df['تاريخ الجلسة'], errors='coerce')
        today = datetime.now()
        urgent = df[(df['تاريخ الجلسة'] >= today) & (df['تاريخ الجلسة'] <= today + timedelta(days=7))]
        
        for _, row in urgent.iterrows():
            msg = f"هاااام: عندك جلسة يوم {row['تاريخ الجلسة'].date()} | القضية {row['رقم الدعوى']} | {row['اسم الطرف الأول']} ضد {row['اسم الطرف الثاني']}"
            st.error(msg)
            st.code(f"إرسال لـ {row['رقم الموبايل']}: {msg}")
    else:
        st.info("لا توجد بيانات لعرضها.")

with tab3:
    st.subheader("التقارير")
    st.dataframe(st.session_state.cases, use_container_width=True)

with tab4:
    st.subheader("أرشيف القضايا المنتهية")
    if not st.session_state.cases.empty:
        st.dataframe(st.session_state.cases[st.session_state.cases["الحالة"] == "منتهية"], use_container_width=True)

with tab5:
    st.subheader("البحث")
    search = st.text_input("أدخل كلمة البحث")
    if search:
        res = st.session_state.cases[st.session_state.cases.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
        st.dataframe(res, use_container_width=True)
