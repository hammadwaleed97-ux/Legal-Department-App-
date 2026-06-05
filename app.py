import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# قاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# إنشاء الجداول الأساسية والمحذوفة
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT,
    case_type TEXT, court TEXT, court_name TEXT, subject TEXT, session_date TEXT,
    decision_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, mobile TEXT,
    status TEXT DEFAULT 'متداولة')""")

cur.execute("""CREATE TABLE IF NOT EXISTS deleted_cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT,
    case_type TEXT, court TEXT, court_name TEXT, subject TEXT, session_date TEXT,
    decision_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, mobile TEXT,
    delete_reason TEXT, delete_date TEXT)""")
conn.commit()

# التنسيق (CSS) لضمان ظهور كل شيء بوضوح
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; font-size: 18px !important; }
div[role="radiogroup"] label { color: white !important; font-weight: bold !important; }
input, textarea { color: black !important; background-color: white !important; }
.logo-box { text-align:center; padding: 20px; border-bottom: 2px solid white; margin-bottom: 20px; }
.footer { text-align: center; margin-top: 50px; font-weight: bold; color: white; padding: 20px; border-top: 2px solid white; }
</style>
""", unsafe_allow_html=True)

# اللوجو والعنوان (كاملاً كما طلبت)
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
col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
with col2:
    if st.button("📋 القضايا المسجلة"): st.session_state.page = "view_cases"
# يمكن إضافة باقي الأزرار هنا إذا أردت

# =====================================
# صفحة تسجيل القضايا
# =====================================
if st.session_state.page == "cases":
    st.header("⚖️ تسجيل القضايا")
    with st.form("new_case"):
        litigation_type = st.radio("نوع الإجراء", ["دعوى", "استئناف", "نقض"], horizontal=True)
        claimant_type = st.radio("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"], horizontal=True)
        claimant = st.text_input("اسم الخصم الأول")
        defendant_type = st.radio("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"], horizontal=True)
        defendant = st.text_input("اسم الخصم الثاني")
        case_no = st.text_input("رقم الدعوى")
        judicial_year = st.text_input("السنة القضائية")
        circuit = st.text_input("الدائرة")
        case_type = st.text_input("النوع")
        court = st.radio("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"], horizontal=True)
        court_name = st.text_input("اسم المحكمة")
        subject = st.text_area("موضوع الدعوى")
        session_date = st.date_input("تاريخ الجلسة")
        decision_date = st.date_input("تاريخ القرار")
        reason = st.text_area("السبب")
        notes = st.text_area("ملاحظات")
        judgment_result = st.radio("نتيجة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"], horizontal=True)
        mobile = st.text_input("رقم الموبايل")
            
        submit = st.form_submit_button("💾 حفظ القضية")
        if submit:
            cur.execute("""INSERT INTO cases (litigation_type, claimant_type, claimant, defendant_type, defendant, 
            case_no, judicial_year, circuit, case_type, court, court_name, subject, 
            session_date, decision_date, reason, notes, judgment_result, mobile, status) 
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (litigation_type, claimant_type, claimant, defendant_type, defendant, 
             case_no, judicial_year, circuit, case_type, court, court_name, subject, 
             str(session_date), str(decision_date), reason, notes, judgment_result, mobile, "متداولة"))
            conn.commit()
            st.success("تم الحفظ بنجاح")

# =====================================
# صفحة القضايا المسجلة (كاملة)
# =====================================
elif st.session_state.page == "view_cases":
    st.markdown("---")
    st.subheader("📋 القضايا المسجلة")
    cases_df = pd.read_sql_query("SELECT * FROM cases ORDER BY id DESC", conn)
    if not cases_df.empty:
        for _, row in cases_df.iterrows():
            with st.expander(f"{row['case_no']} / {row['judicial_year']} - {row['claimant']} ضد {row['defendant']}"):
                st.write(f"نوع الإجراء : {row['litigation_type']}")
                st.write(f"{row['claimant_type']} : {row['claimant']}")
                st.write(f"{row['defendant_type']} : {row['defendant']}")
                st.write(f"رقم الدعوى : {row['case_no']}")
                st.write(f"السنة القضائية : {row['judicial_year']}")
                st.write(f"الدائرة : {row['circuit']}")
                st.write(f"النوع : {row['case_type']}")
                st.write(f"المحكمة : {row['court']}")
                st.write(f"اسم المحكمة : {row['court_name']}")
                st.write(f"موضوع الدعوى : {row['subject']}")
                st.write(f"تاريخ الجلسة : {row['session_date']}")
                st.write(f"نتيجة الدعوى : {row['judgment_result']}")
                
                delete_reason = st.selectbox("سبب الحذف", ["تسجيل الدعوى مرتين", "خطأ في رقم الدعوى", "خطأ في بيانات الخصوم", "أخرى"], key=f"reason_{row['id']}")
                other_reason = st.text_input("اكتب سبب الحذف", key=f"other_{row['id']}") if delete_reason == "أخرى" else ""
                
                if st.button(f"🗑️ حذف القضية رقم {row['id']}", key=f"delete_{row['id']}"):
                    final_reason = other_reason if delete_reason == "أخرى" else delete_reason
                    cur.execute("""INSERT INTO deleted_cases (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, circuit, case_type, court, court_name, subject, session_date, decision_date, reason, notes, judgment_result, mobile, delete_reason, delete_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (row["litigation_type"], row["claimant_type"], row["claimant"], row["defendant_type"], row["defendant"], row["case_no"], row["judicial_year"], row["circuit"], row["case_type"], row["court"], row["court_name"], row["subject"], row["session_date"], row["decision_date"], row["reason"], row["notes"], row["judgment_result"], row["mobile"], final_reason, str(datetime.now())))
                    cur.execute("DELETE FROM cases WHERE id=?", (row["id"],))
                    conn.commit()
                    st.success("تم نقل القضية إلى القضايا المحذوفة")
                    st.rerun()
    else:
        st.info("لا توجد قضايا مسجلة حالياً")

# التوقيع
st.markdown("""
<div class="footer">
مع تحيات<br>
وليد شعبان حماد
</div>
""", unsafe_allow_html=True)
