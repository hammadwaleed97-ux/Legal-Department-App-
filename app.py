import streamlit as st

# عنوان التطبيق
st.title("نظام إدارة القضايا")

# قائمة التنقل
page = st.sidebar.radio("القائمة", ["سجل القضايا", "بحث", "المكتبة"])

if page == "سجل القضايا":
    st.write("هنا ستدخل بيانات القضايا")
elif page == "بحث":
    st.write("هنا ستظهر نتائج البحث")
elif page == "المكتبة":
    st.write("مجلد المكتبة القانونية (الدرايف)")
    st.link_button("افتح المكتبة", "https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke")
