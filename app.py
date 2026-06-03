import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="نظام إدارة القضايا", layout="wide")

st.title("📂 نظام إدارة القضايا - ديوان عام منطقة البحيرة")

# تهيئة ملف البيانات (إذا لم يكن موجوداً)
if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=["رقم القضية", "اسم الخصم", "الموضوع", "التاريخ", "الحالة"])

# واجهة الإدخال
with st.sidebar:
    st.header("إضافة قضية جديدة")
    case_no = st.text_input("رقم القضية")
    opponent = st.text_input("اسم الخصم")
    topic = st.text_area("موضوع القضية")
    status = st.selectbox("الحالة", ["قيد التداول", "محجوزة للحكم", "تم الفصل فيها"])
    
    if st.button("حفظ القضية"):
        new_case = {"رقم القضية": case_no, "اسم الخصم": opponent, "الموضوع": topic, "التاريخ": datetime.now().strftime("%Y-%m-%d"), "الحالة": status}
        st.session_state.cases = pd.concat([st.session_state.cases, pd.DataFrame([new_case])], ignore_index=True)
        st.success("تم حفظ القضية!")

# عرض القضايا
st.subheader("سجل القضايا")
st.table(st.session_state.cases)

st.sidebar.markdown("---")
st.sidebar.write("مع تحيات وليد حماد - الإدارة العامة للشئون القانونية")
