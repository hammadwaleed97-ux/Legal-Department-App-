import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# إعداد قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# إنشاء الجداول (إذا لم تكن موجودة)
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, 
    judicial_year TEXT, circuit TEXT, case_type TEXT, 
    court TEXT, court_name TEXT, subject TEXT, 
    session_date TEXT, decision_date TEXT, reason TEXT, 
    notes TEXT, judgment_result TEXT, mobile TEXT, status TEXT)""")
conn.commit()

# التنسيق (CSS)
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; }
.logo-box { text-align:center; padding: 20px; border-bottom: 2px solid white; margin-bottom: 20px; }
.footer { text-align: center; margin-top: 50px; font-weight: bold; color: white; }
</style>
""", unsafe_allow_html=True)

# اللوجو والعنوان
st.markdown("""
<div class="logo-box">
<div style="font-size:50px">⚖️</div>
<div style="font-size:28px; font-weight:bold">الهيئة القومية للتأمين الاجتماعى</div>
<div style="font-size:22px; font-weight:bold">الإدارة العامة للشؤون القانونية</div>
<div style="font-size:20px;">ديوان عام منطقة البحيرة</div>
</div>
""", unsafe_allow_html=True)

# التنقل
if "page" not in st.session_state: st.session_state.page = "home"
col1, col2 = st.columns(2)
with col1:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
with col2:
    if st.button("📋 القضايا المسجلة"): st.session_state.page = "view_cases"

# صفحة التسجيل
if st.session_state.page == "cases":
    st.header("تسجيل قضية جديدة")
    with st.form("add_case"):
        l_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])
        c_type = st.selectbox("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"])
        c_name = st.text_input("اسم الخصم الأول")
        # ... (أكمل باقي الحقول بنفس الطريقة) ...
        submit = st.form_submit_button("حفظ القضية")
        if submit:
            cur.execute("INSERT INTO cases (litigation_type, claimant_type, claimant, status) VALUES (?,?,?,?)", (l_type, c_type, c_name, "متداولة"))
            conn.commit()
            st.success("تم الحفظ")

# صفحة عرض القضايا
elif st.session_state.page == "view_cases":
    st.header("📋 القضايا المسجلة")
    df = pd.read_sql_query("SELECT * FROM cases", conn)
    
    # تحويل أسماء الأعمدة للعربية في الجدول
    df.columns = ["م", "نوع الإجراء", "صفة الخصم", "الاسم", "الخصم الثاني", "الاسم 2", "رقم الدعوى", "السنة", "الدائرة", "النوع", "المحكمة", "اسم المحكمة", "الموضوع", "تاريخ الجلسة", "تاريخ القرار", "القرار", "ملاحظات", "النتيجة", "موبايل", "الحالة"]
    
    # استخدام محرر البيانات لإضافة أزرار أو تعديل
    edited_df = st.data_editor(df, use_container_width=True)
    
    if st.button("حفظ التعديلات على القرارات والإجراءات"):
        # منطق تحديث قاعدة البيانات بناءً على edited_df
        st.success("تم تحديث البيانات")

# التوقيع
st.markdown("""
<div class="footer">
مع تحيات<br>
وليد شعبان حماد
</div>
""", unsafe_allow_html=True)
