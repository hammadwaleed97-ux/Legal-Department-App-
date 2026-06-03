import streamlit as st
import pandas as pd

st.set_page_config(page_title="المستشار القانوني", layout="wide")

# مسح أي بيانات سابقة من الذاكرة فوراً لتجنب أي تعارض
if st.button("اضغط هنا لبدء النظام من جديد (Reset)"):
    st.session_state.cases = pd.DataFrame(columns=["رقم الدعوى", "الطرف الأول", "الطرف الثاني", "تاريخ الجلسة", "القرار", "المحامي", "الموبايل", "الحالة"])
    st.experimental_rerun()

# تهيئة جدول البيانات (كل شيء كنص فقط)
if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=["رقم الدعوى", "الطرف الأول", "الطرف الثاني", "تاريخ الجلسة", "القرار", "المحامي", "الموبايل", "الحالة"])

st.title("نظام إدارة القضايا - منطقة البحيرة")

tab1, tab2, tab3 = st.tabs(["تسجيل قضية", "عرض القضايا (التنبيهات)", "بحث"])

with tab1:
    with st.form("new_case"):
        no = st.text_input("رقم الدعوى")
        p1 = st.text_input("الطرف الأول")
        p2 = st.text_input("الطرف الثاني")
        date = st.text_input("تاريخ الجلسة (مثال: 2026-06-05)")
        decision = st.text_area("القرار")
        lawyer = st.text_input("المحامي")
        phone = st.text_input("الموبايل")
        status = st.selectbox("الحالة", ["متداولة", "منتهية"])
        
        if st.form_submit_button("حفظ"):
            new_row = {"رقم الدعوى": no, "الطرف الأول": p1, "الطرف الثاني": p2, "تاريخ الجلسة": date, "القرار": decision, "المحامي": lawyer, "الموبايل": phone, "الحالة": status}
            st.session_state.cases = pd.concat([st.session_state.cases, pd.DataFrame([new_row])], ignore_index=True)
            st.success("تم الحفظ!")

with tab2:
    st.dataframe(st.session_state.cases)

with tab3:
    query = st.text_input("بحث")
    if query:
        st.dataframe(st.session_state.cases[st.session_state.cases.apply(lambda row: query in str(row.values), axis=1)])
