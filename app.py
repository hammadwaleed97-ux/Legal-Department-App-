import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="المستشار القانوني", layout="wide")

COLUMNS = ["رقم الدعوى", "السنة", "الطرف الأول", "اسم الطرف الأول", "الطرف الثاني", "اسم الطرف الثاني", 
           "الدائرة", "النوع", "المحكمة", "اسم المحكمة", "موضوع الدعوى", "تاريخ الجلسة", "القرار", "المحامي", "رقم الموبايل", "الحالة"]

if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns
