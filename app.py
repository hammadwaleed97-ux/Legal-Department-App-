import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# إعداد قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# إنشاء الجداول الأساسية
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, 
    judicial_year TEXT, circuit TEXT, case_type TEXT, 
    court TEXT, court_name TEXT, subject TEXT, 
    session_date TEXT, decision_date TEXT, reason TEXT, 
    notes TEXT, judgment_result TEXT, mobile TEXT, status TEXT)""")

# جدول القضايا المحذوفة
cur.execute("""CREATE TABLE IF NOT EXISTS deleted_cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, 
    judicial_year TEXT, circuit TEXT, case_type TEXT, 
    court TEXT, court_name TEXT, subject TEXT, 
    session_date TEXT, decision_date TEXT, reason TEXT, 
    notes TEXT, judgment_result TEXT, mobile TEXT, 
    delete_reason TEXT, delete_date TEXT)""")
conn.commit()

# التنسيق (CSS) لضمان ظهور كل شيء بوضوح
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; }
.logo-box { text-align:center; padding: 20px; border-bottom: 2px solid white; margin-bottom: 20px; }
.footer { text-align: center; margin-top: 50px; font-weight: bold; color: white; padding: 20px; border-top: 2px solid white; }
</style>
""", unsafe_allow_html=True)

# اللوجو والعنوان (كاملاً)
st.markdown("""
<div class="logo-box">
<div style="font-size:50px">⚖️</div>
<div style="font-size:28px; font-weight:bold">الهيئة القومية للتأمين الاجتماعى</div>
<div style="font-size:28px; font-weight:bold">الإدارة العامة للشؤون القانونية</div>
<div style="font-size:24px; font-weight:bold">ديوان عام منطقة البحيرة</div>
</div>
""", unsafe_allow_html=True)

# التنقل
if "page" not in st.session_state: st.session_state.page = "cases"
col1, col2 = st.columns(2)
with col1:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
with col2:
    if st.button("📋 القضايا المسجلة"): st.session_state.page = "view_cases"

# صفحة تسجيل القضايا
if st.session_state.page == "cases":
    st.header("تسجيل قضية جديدة")
    with st.form("new_case"):
        col_a, col_b = st.columns(2)
        with col_a:
            litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])
            claimant_type = st.selectbox("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"])
            claimant = st.text_input("اسم الخصم الأول")
            defendant_type = st.selectbox("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"])
            defendant = st.text_input("اسم الخصم الثاني")
        with col_b:
            case_no = st.text_input("رقم الدعوى")
            judicial_year = st.text_input("السنة القضائية")
            court = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى"])
            mobile = st.text_input("رقم الموبايل")
            
        submit = st.form_submit_button("💾 حفظ القضية")
        if submit:
            cur.execute("INSERT INTO cases (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, court, mobile, status) VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, court, mobile, "متداولة"))
            conn.commit()
            st.success("تم الحفظ بنجاح")

# صفحة عرض القضايا
elif st.session_state.page == "view_cases":
    st.header("📋 القضايا المسجلة")
    cases = cur.execute("SELECT * FROM cases").fetchall()
    
    for case in cases:
        with st.expander(f"قضية رقم: {case[6]} - {case[3]} ضد {case[5]}"):
            st.write(f"الموضوع: {case[13]}")
            # نموذج تحديث القضية
            with st.form(f"form_{case[0]}"):
                new_session = st.date_input("تاريخ الجلسة القادمة", key=f"d_{case[0]}")
                new_action = st.text_input("الإجراء المطلوب", key=f"a_{case[0]}")
                if st.form_submit_button("تحديث الجلسة والإجراء"):
                    cur.execute("UPDATE cases SET session_date=?, reason=? WHERE id=?", (str(new_session), new_action, case[0]))
                    conn.commit()
                    st.rerun()

# التوقيع
st.markdown("""
<div class="footer">
مع تحيات<br>
وليد شعبان حماد
</div>
""", unsafe_allow_html=True)
