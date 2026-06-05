import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

# =====================================
# إعداد الصفحة
# =====================================
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# =====================================
# قاعدة البيانات
# =====================================
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# =====================================
# CSS - تنسيق نهائي لضمان المظهر
# =====================================
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; font-size: 18px !important; }
div[role="radiogroup"] label { color: white !important; font-weight: bold !important; }
input, textarea { color: black !important; background-color: white !important; }
.logo-box { text-align:center; }
div.stButton > button { 
    width:320px; height:65px; border-radius:15px; border:none; 
    background:#2f55d4; color:white; font-size:20px; font-weight:bold; 
    display:block; margin:auto; margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# اللوجو
# =====================================
st.markdown("""
<div class="logo-box">
<div style="font-size:50px">⚖️</div>
<div style="font-size:28px; font-weight:bold">الهيئة القومية للتأمين الاجتماعى</div>
<div style="font-size:22px; font-weight:bold">الإدارة العامة للشؤون القانونية</div>
</div>
""", unsafe_allow_html=True)

# =====================================
# التنقل
# =====================================
if "page" not in st.session_state: st.session_state.page = "home"
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⚖️ تسجيل القضايا", key="b1"): st.session_state.page = "cases"
    if st.button("🔔 التنبيهات", key="b2"): st.session_state.page = "alerts"
    if st.button("📊 التقارير", key="b3"): st.session_state.page = "reports"
    if st.button("📂 أرشيف القضايا", key="b4"): st.session_state.page = "archive"
    if st.button("🔍 البحث عن دعوى", key="b5"): st.session_state.page = "search"
    if st.button("❌ القضايا المحذوفة", key="b6"): st.session_state.page = "deleted"

# =====================================
# الجدول
# =====================================
cur.execute("""CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT,
    defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT,
    case_type TEXT, court TEXT, court_name TEXT, subject TEXT, session_date TEXT,
    decision_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, mobile TEXT,
    status TEXT DEFAULT 'متداولة')""")
conn.commit()

# =====================================
# الصفحات (كاملة كما كانت لديك)
# =====================================
if st.session_state.page == "cases":
    st.markdown("<h2 style='text-align:center'>⚖️ تسجيل القضايا</h2>", unsafe_allow_html=True)
    
    litigation_type = st.radio("نوع الإجراء", ["دعوى", "استئناف", "نقض"], horizontal=True, key="s1")
    claimant_type = st.radio("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"], horizontal=True, key="s2")
    claimant = st.text_input("اسم الخصم الأول", key="t1")
    defendant_type = st.radio("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"], horizontal=True, key="s3")
    defendant = st.text_input("اسم الخصم الثاني", key="t2")
    case_no = st.text_input("رقم الدعوى", key="t3")
    judicial_year = st.text_input("السنة القضائية", key="t4")
    circuit = st.text_input("الدائرة", key="t5")
    case_type = st.text_input("النوع", key="t6")
    court = st.radio("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"], horizontal=True, key="s4")
    court_name = st.text_input("اسم المحكمة", key="t7")
    subject = st.text_area("موضوع الدعوى", key="t8")
    session_date = st.date_input("تاريخ الجلسة", key="d1")
    decision_date = st.date_input("تاريخ القرار", key="d2")
    reason = st.text_area("السبب", key="t9")
    notes = st.text_area("ملاحظات", key="t10")
    judgment_result = st.radio("نتيجة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"], horizontal=True, key="s5")
    mobile = st.text_input("رقم الموبايل", key="t11")

    if st.button("💾 حفظ القضية", key="save"):
        cur.execute("""INSERT INTO cases (litigation_type, claimant_type, claimant, defendant_type, defendant, 
        case_no, judicial_year, circuit, case_type, court, court_name, subject, 
        session_date, decision_date, reason, notes, judgment_result, mobile, status) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (litigation_type, claimant_type, claimant, defendant_type, defendant, 
         case_no, judicial_year, circuit, case_type, court, court_name, subject, 
         str(session_date), str(decision_date), reason, notes, judgment_result, mobile, "متداولة"))
        conn.commit()
        st.success("تم حفظ القضية بنجاح")

elif st.session_state.page == "alerts": st.header("🔔 التنبيهات")
elif st.session_state.page == "reports": st.header("📊 التقارير")
elif st.session_state.page == "archive": st.header("📂 أرشيف القضايا")
elif st.session_state.page == "search": st.header("🔍 البحث عن دعوى")
elif st.session_state.page == "deleted": st.header("❌ القضايا المحذوفة")
# =====================================
# جدول القضايا المحذوفة
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS deleted_cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

litigation_type TEXT,

claimant_type TEXT,
claimant TEXT,

defendant_type TEXT,
defendant TEXT,

case_no TEXT,

judicial_year TEXT,

circuit TEXT,

case_type TEXT,

court TEXT,

court_name TEXT,

subject TEXT,

session_date TEXT,

decision_date TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

delete_reason TEXT,

delete_date TEXT

)
""")

conn.commit()

# =====================================
# القضايا المسجلة
# =====================================

if st.session_state.page == "cases":

    st.markdown("---")

    st.subheader("📋 القضايا المسجلة")

    cases_df = pd.read_sql_query(
        "SELECT * FROM cases ORDER BY id DESC",
        conn
    )

    if not cases_df.empty:

        for _, row in cases_df.iterrows():

            with st.expander(
                f"{row['case_no']} / {row['judicial_year']} - {row['claimant']} ضد {row['defendant']}"
            ):

                st.write(
                    f"نوع الإجراء : {row['litigation_type']}"
                )

                st.write(
                    f"{row['claimant_type']} : {row['claimant']}"
                )

                st.write(
                    f"{row['defendant_type']} : {row['defendant']}"
                )

                st.write(
                    f"رقم الدعوى : {row['case_no']}"
                )

                st.write(
                    f"السنة القضائية : {row['judicial_year']}"
                )

                st.write(
                    f"الدائرة : {row['circuit']}"
                )

                st.write(
                    f"النوع : {row['case_type']}"
                )

                st.write(
                    f"المحكمة : {row['court']}"
                )

                st.write(
                    f"اسم المحكمة : {row['court_name']}"
                )

                st.write(
                    f"موضوع الدعوى : {row['subject']}"
                )

                st.write(
                    f"تاريخ الجلسة : {row['session_date']}"
                )

                st.write(
                    f"نتيجة الدعوى : {row['judgment_result']}"
                )

                delete_reason = st.selectbox(

                    "سبب الحذف",

                    [
                        "تسجيل الدعوى مرتين",
                        "خطأ في رقم الدعوى",
                        "خطأ في بيانات الخصوم",
                        "أخرى"
                    ],

                    key=f"reason_{row['id']}"

                )

                other_reason = ""

                if delete_reason == "أخرى":

                    other_reason = st.text_input(

                        "اكتب سبب الحذف",

                        key=f"other_{row['id']}"

                    )

                if st.button(

                    f"🗑️ حذف القضية رقم {row['id']}",

                    key=f"delete_{row['id']}"

                ):

                    final_reason = delete_reason

                    if delete_reason == "أخرى":

                        final_reason = other_reason

                    cur.execute("""

                    INSERT INTO deleted_cases(

                    litigation_type,

                    claimant_type,
                    claimant,

                    defendant_type,
                    defendant,

                    case_no,

                    judicial_year,

                    circuit,

                    case_type,

                    court,

                    court_name,

                    subject,

                    session_date,

                    decision_date,

                    reason,

                    notes,

                    judgment_result,

                    mobile,

                    delete_reason,

                    delete_date

                    )

                    VALUES(

                    ?,?,?,?,?,?,
                    ?,?,?,?,?,?,
                    ?,?,?,?,?,?,
                    ?,?,?,?

                    )

                    """,

                    (

                    row["litigation_type"],

                    row["claimant_type"],
                    row["claimant"],

                    row["defendant_type"],
                    row["defendant"],

                    row["case_no"],

                    row["judicial_year"],

                    row["circuit"],

                    row["case_type"],

                    row["court"],

                    row["court_name"],

                    row["subject"],

                    row["session_date"],

                    row["decision_date"],

                    row["reason"],

                    row["notes"],

                    row["judgment_result"],

                    row["mobile"],

                    final_reason,

                    str(datetime.now())

                    )

                    )

                    cur.execute(
                        "DELETE FROM cases WHERE id=?",
                        (row["id"],)
                    )

                    conn.commit()

                    st.success(
                        "تم نقل القضية إلى القضايا المحذوفة"
                    )

                    st.rerun()

    else:

        st.info(
            "لا توجد قضايا مسجلة حالياً"
        ) 
