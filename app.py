import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

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
# CSS - تنسيق نهائي لضمان المظهر ووضوح النصوص
# =====================================
st.markdown("""
<style>
.stApp { background:#062456; }
label, p, span, div, h1, h2, h3, h4, h5, h6 { color:white !important; font-size: 18px !important; }
div[role="radiogroup"] label { color: white !important; font-weight: bold !important; }
input, textarea { color: black !important; background-color: white !important; }
.logo-box { text-align:center; padding: 20px; }
div.stButton > button { width:320px; height:65px; border-radius:15px; border:none; background:#2f55d4; color:white; font-size:20px; font-weight:bold; display:block; margin:auto; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# =====================================
# اللوجو (تم إرجاعه كاملاً)
# =====================================
st.markdown("""
<div class="logo-box">
<div style="font-size:50px">⚖️</div>
<div style="font-size:28px; font-weight:bold">الهيئة القومية للتأمين الاجتماعى</div>
<div style="font-size:22px; font-weight:bold">الإدارة العامة للشؤون القانونية</div>
</div>
""", unsafe_allow_html=True)

# =====================================
# الجداول
# =====================================
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
# الصفحات
# =====================================
if st.session_state.page == "cases":
    st.markdown("<h2 style='text-align:center'>⚖️ تسجيل القضايا</h2>", unsafe_allow_html=True)
    
    litigation_type = st.radio("نوع الإجراء", ["دعوى", "استئناف", "نقض"], horizontal=True, key="s1")
    claimant_type = st.radio("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"], horizontal=True, key="s2")
    claimant = st.text_input("اسم الخصم الأول")
    defendant_type = st.radio("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"], horizontal=True, key="s3")
    defendant = st.text_input("اسم الخصم الثاني")
    case_no = st.text_input("رقم الدعوى")
    judicial_year = st.text_input("السنة القضائية")
    circuit = st.text_input("الدائرة")
    case_type = st.text_input("النوع")
    court = st.radio("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "إدارية", "قضاء إدارى", "إدارية عليا"], horizontal=True, key="s4")
    court_name = st.text_input("اسم المحكمة")
    subject = st.text_area("موضوع الدعوى")
    session_date = st.date_input("تاريخ الجلسة")
    decision_date = st.date_input("تاريخ القرار")
    reason = st.text_area("السبب")
    notes = st.text_area("ملاحظات")
    judgment_result = st.radio("نتيجة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"], horizontal=True, key="s5")
    mobile = st.text_input("رقم الموبايل")

    if st.button("💾 حفظ القضية"):
        # تم ضبط المدخلات لتطابق تماماً أعمدة الجدول الـ 19
        cur.execute("""INSERT INTO cases (litigation_type, claimant_type, claimant, defendant_type, defendant, 
        case_no, judicial_year, circuit, case_type, court, court_name, subject, 
        session_date, decision_date, reason, notes, judgment_result, mobile, status) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (litigation_type, claimant_type, claimant, defendant_type, defendant, 
         case_no, judicial_year, circuit, case_type, court, court_name, subject, 
         str(session_date), str(decision_date), reason, notes, judgment_result, mobile, "متداولة"))
        conn.commit()
        st.success("تم حفظ القضية بنجاح")
        st.rerun()

    st.markdown("---")
    st.subheader("📋 القضايا المسجلة")
    cases_df = pd.read_sql_query("SELECT * FROM cases ORDER BY id DESC", conn)
    
    if not cases_df.empty:
        for _, row in cases_df.iterrows():
            with st.expander(f"{row['case_no']} - {row['claimant']} ضد {row['defendant']}"):
                st.write(f"الموضوع: {row['subject']}")
                delete_reason = st.selectbox("سبب الحذف", ["تسجيل الدعوى مرتين", "خطأ في رقم الدعوى", "خطأ في بيانات الخصوم", "أخرى"], key=f"reason_{row['id']}")
                other_reason = st.text_input("اكتب سبب الحذف (إذا اخترت أخرى)", key=f"other_{row['id']}") if delete_reason == "أخرى" else ""
                
                if st.button(f"🗑️ حذف القضية {row['id']}", key=f"del_{row['id']}"):
                    final_reason = other_reason if delete_reason == "أخرى" else delete_reason
                    # نقل البيانات للجدول الآخر
                    cur.execute("INSERT INTO deleted_cases (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, circuit, case_type, court, court_name, subject, session_date, decision_date, reason, notes, judgment_result, mobile, delete_reason, delete_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (row['litigation_type'], row['claimant_type'], row['claimant'], row['defendant_type'], row['defendant'], row['case_no'], row['judicial_year'], row['circuit'], row['case_type'], row['court'], row['court_name'], row['subject'], row['session_date'], row['decision_date'], row['reason'], row['notes'], row['judgment_result'], row['mobile'], final_reason, str(datetime.now())))
                    cur.execute("DELETE FROM cases WHERE id=?", (row['id'],))
                    conn.commit()
                    st.rerun()
    else:
        st.info("لا توجد قضايا مسجلة")

elif st.session_state.page == "alerts": st.header("🔔 التنبيهات")
elif st.session_state.page == "reports": st.header("📊 التقارير")
elif st.session_state.page == "archive": st.header("📂 أرشيف القضايا")
elif st.session_state.page == "search": st.header("🔍 البحث عن دعوى")
elif st.session_state.page == "deleted": st.header("❌ القضايا المحذوفة")
