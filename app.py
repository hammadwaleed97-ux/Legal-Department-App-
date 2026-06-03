import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني - البحيرة", layout="wide")

# تهيئة قاعدة البيانات
if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=[
        "رقم الدعوى", "السنة", "الطرف الأول", "اسم الطرف الأول", "الطرف الثاني", "اسم الطرف الثاني", 
        "الدائرة", "النوع", "المحكمة", "اسم المحكمة", "موضوع الدعوى", "تاريخ الجلسة", "القرار", "المحامي", "رقم الموبايل", "الحالة"
    ])

# الترويسة
st.markdown("<div style='text-align: center; background-color: #002b5b; color: white; padding: 20px;'>الهيئة القومية للتأمين الاجتما
