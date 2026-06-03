import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام الإدارة القانونية", layout="wide")

# التصميم والألوان (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    h1 { color: #003366; text-align: center; }
    .stButton>button { background-color: #003366; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# العنوان واللوجو
st.title("⚖️ الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة")

# تهيئة بيانات القضايا في الذاكرة
if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=["رقم القضية", "الموضوع", "تاريخ الجلسة", "الحالة"])

# القوائم الجانبية
menu = st.sidebar.radio("القائمة الرئيسية", ["إضافة قضية", "متابعة القضايا", "التقارير"])

# 1. إضافة قضية
if menu == "إضافة قضية":
    st.subheader("إضافة قضية جديدة")
    with st.form("case_form"):
        case_no = st.text_input("رقم القضية")
        subject = st.text_area("موضوع القضية")
        date = st.date_input("تاريخ الجلسة القادمة")
        status = st.selectbox("الحالة", ["قيد التداول", "محجوزة للحكم", "منتهية"])
        submit = st.form_submit_button("حفظ القضية")
        
        if submit:
            new_data = {"رقم القضية": case_no, "الموضوع": subject, "تاريخ الجلسة": date, "الحالة": status}
            st.session_state.cases = pd.concat([st.session_state.cases, pd.DataFrame([new_data])], ignore_index=True)
            st.success("تم حفظ القضية بنجاح!")

# 2. متابعة القضايا والتنبيهات
elif menu == "متابعة القضايا":
    st.subheader("سجل القضايا المتابع")
    st.dataframe(st.session_state.cases, use_container_width=True)
    
    # التنبيهات البسيطة
    st.subheader("⚠️ تنبيهات عاجلة")
    today = datetime.now().date()
    urgent = st.session_state.cases[pd.to_datetime(st.session_state.cases["تاريخ الجلسة"]).dt.date <= today]
    if not urgent.empty:
        st.warning("هناك قضايا موعد جلستها اليوم أو مضى!")
        st.write(urgent)
    else:
        st.info("لا توجد قضايا عاجلة حالياً.")

# 3. التقارير
elif menu == "التقارير":
    st.subheader("تقرير حالة القضايا")
    if not st.session_state.cases.empty:
        report = st.session_state.cases['الحالة'].value_counts()
        st.bar_chart(report)
    else:
        st.write("لا توجد بيانات كافية لاستخراج تقرير.")

# التوقيع الرسمي في الجانب
st.sidebar.markdown("---")
st.sidebar.write("مع تحيات وليد حماد")
st.sidebar.write("الإدارة العامة للشئون القانونية")
st.sidebar.write("ديوان عام منطقة البحيرة")
