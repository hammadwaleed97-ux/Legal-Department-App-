import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني - ديوان عام منطقة البحيرة", layout="wide")

# التصميم (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #003366; text-align: center; font-family: serif; }
    .header-box { text-align: center; background-color: #003366; color: white; padding: 15px; border-radius: 10px; margin-bottom: 20px; }
    .stButton>button { background-color: #003366; color: white; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# الهوية واللوجو (Header)
with st.container():
    st.markdown("<div class='header-box'><h3>الهيئة القومية للتأمين الاجتماعى</h3><h4>الإدارة العامة للشؤون القانونية</h4><p>إعداد: وليد شعبان حماد</p><h5>ديوان عام منطقة البحيرة</h5></div>", unsafe_allow_html=True)

# تهيئة الحالة
if 'cases_db' not in st.session_state: st.session_state.cases_db = pd.DataFrame()
if 'archive_db' not in st.session_state: st.session_state.archive_db = pd.DataFrame()

# الأقسام الرئيسية في صفحة واحدة
tab1, tab2, tab3, tab4, tab5 = st.tabs(["⚖️ تسجيل القضايا", "🔔 التنبيهات", "📊 التقارير", "📂 الأرشيف", "🔍 البحث"])

# 1. إدارة القضايا
with tab1:
    st.subheader("تسجيل قضية جديدة")
    with st.form("new_case"):
        col1, col2 = st.columns(2)
        with col1:
            party_a = st.selectbox("الطرف الأول", ["المدعى", "المستأنف", "الطاعن"])
            party_b = st.selectbox("الطرف الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"])
            case_no = st.text_input("رقم الدعوى")
            case_year = st.text_input("السنة القضائية")
        with col2:
            circle = st.text_input("الدائرة")
            case_type = st.text_input("نوع الدعوى")
            court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"])
            subject = st.text_area("موضوع الدعوى")
        
        submit = st.form_submit_button("حفظ القضية")
        if submit:
            new_row = pd.DataFrame([{"رقم الدعوى": case_no, "السنة": case_year, "الدائرة": circle, "النوع": case_type, "الطرف الأول": party_a, "الطرف الثاني": party_b, "المحكمة": court, "الموضوع": subject, "الحالة": "متداولة"}])
            st.session_state.cases_db = pd.concat([st.session_state.cases_db, new_row], ignore_index=True)
            st.success("تم حفظ القضية!")

# 2. التنبيهات
with tab2:
    st.subheader("تنبيهات عاجلة 🔴")
    st.warning("عرض القضايا قبل الجلسة بأسبوع | أحكام الطعن قبل 15 يوم")
    # هنا سيتم إضافة منطق الفلترة بناءً على التاريخ

# 3. التقارير
with tab3:
    st.subheader("التقارير القانونية")
    report_type = st.selectbox("نوع التقرير", ["تقرير بالدعاوى المتداولة", "تقرير بالأحكام الصادرة"])
    start_date = st.date_input("من تاريخ")
    end_date = st.date_input("إلى تاريخ")
    if st.button("توليد التقرير"):
        st.info(f"جاري إعداد {report_type}.. سيتم توفير روابط التحميل (Word/PDF)")

# 4. الأرشيف
with tab4:
    st.subheader("أرشيف القضايا المنتهية")
    st.dataframe(st.session_state.archive_db)

# 5. البحث
with tab5:
    st.subheader("البحث عن دعوى")
    search_type = st.radio("طريقة البحث:", ["برقم وسنة الدعوى", "بالاسم"])
    query = st.text_input("أدخل نص البحث:")
