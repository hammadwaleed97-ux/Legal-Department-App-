import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# تنسيق CSS
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; }
input, textarea { color: black !important; background-color: white !important; }
.logo-box { text-align:center; padding: 20px; }
div.stButton > button { background:#2f55d4; color:white; font-weight:bold; border-radius:10px; }
</style>
""", unsafe_allow_html=True)

# اللوجو
st.markdown("""
<div class="logo-box">
<div style="font-size:50px">⚖️</div>
<div style="font-size:28px; font-weight:bold">الهيئة القومية للتأمين الاجتماعى</div>
<div style="font-size:22px; font-weight:bold">الإدارة العامة للشؤون القانونية</div>
</div>
""", unsafe_allow_html=True)

# إنشاء الجداول
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT,
    case_type TEXT, court TEXT, court_name TEXT, subject TEXT, session_date TEXT,
    decision_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, mobile TEXT,
    status TEXT DEFAULT 'متداولة')""")
conn.commit()

# التنقل
if "page" not in st.session_state: st.session_state.page = "home"
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
    if st.button("📋 القضايا المسجلة"): st.session_state.page = "view_cases"

# صفحة التسجيل
if st.session_state.page == "cases":
    st.header("تسجيل قضية جديدة")
    # ... (بقية كود التسجيل الخاص بك) ...

# صفحة عرض القضايا في جدول
elif st.session_state.page == "view_cases":
    st.header("📋 القضايا المسجلة")
    
    # جلب البيانات
    df = pd.read_sql_query("SELECT * FROM cases", conn)
    
    if not df.empty:
        # عرض الجدول
        st.dataframe(df, use_container_width=True)
        
        st.subheader("إضافة إجراء أو قرار لقضية")
        case_id = st.selectbox("اختر رقم القضية", df['id'].tolist())
        
        with st.form("update_form"):
            new_decision = st.text_area("القرار الجديد")
            new_action = st.text_input("الإجراء المطلوب")
            submit = st.form_submit_button("حفظ التحديث")
            
            if submit:
                # تحديث قاعدة البيانات
                cur.execute("UPDATE cases SET reason = ?, notes = ? WHERE id = ?", (new_decision, new_action, case_id))
                conn.commit()
                st.success("تم تحديث القضية بنجاح!")
    else:
        st.info("لا توجد قضايا مسجلة.")
