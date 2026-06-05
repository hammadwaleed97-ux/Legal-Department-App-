import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime, timedelta

# =====================================
# إعداد الصفحة
# =====================================

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =====================================
# قاعدة البيانات
# =====================================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

.stApp{
    background-color:#062456;
}

.block-container{
    padding-top:5px;
}

label,
p,
span,
div,
h1,
h2,
h3,
h4,
h5,
h6{
    color:white !important;
    opacity:1 !important;
}

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:52px;
    margin-top:15px;
    margin-bottom:8px;
}

.logo-main{
    font-size:28px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:15px;
}

.logo-sub{
    font-size:22px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:35px;
}

.prepare{
    font-size:18px;
    margin-bottom:8px;
}

.name{
    font-size:28px;
    font-weight:bold;
    margin-bottom:12px;
}

.place{
    font-size:22px;
    font-weight:bold;
    margin-bottom:30px;
}

div.stButton > button{
    width:320px;
    height:65px;
    border-radius:18px;
    border:none;
    font-size:20px;
    font-weight:bold;
    margin:auto;
    display:block;
    background-color:#2f55d4;
    color:white;
}

div.stButton > button:hover{
    background-color:#4368e0;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# اللوجو
# =====================================

st.markdown("""
<div class="logo-box">

<div class="logo-icon">
⚖️
</div>

<div class="logo-main">
الهيئة القومية للتأمين الاجتماعى
</div>

<div class="logo-sub">
الإدارة العامة للشؤون القانونية
</div>

<div class="prepare">
إعداد
</div>

<div class="name">
وليد شعبان حماد
</div>

<div class="place">
ديوان عام منطقة البحيرة
</div>

</div>
""", unsafe_allow_html=True)

# =====================================
# الصفحات
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

# =====================================
# القائمة الرئيسية
# =====================================

col1, col2, col3 = st.columns([1,2,1])

with col2:

    if st.button("⚖️ تسجيل القضايا"):
        st.session_state.page = "cases"

    if st.button("🔔 التنبيهات"):
        st.session_state.page = "alerts"

    if st.button("📊 التقارير"):
        st.session_state.page = "reports"

    if st.button("📂 أرشيف القضايا"):
        st.session_state.page = "archive"

    if st.button("🔍 البحث عن دعوى"):
        st.session_state.page = "search"

    if st.button("❌ القضايا المحذوفة"):
        st.session_state.page = "deleted"
# =====================================
# إنشاء جدول القضايا
# =====================================

cur.execute("""

CREATE TABLE IF NOT EXISTS cases(

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
session_action TEXT,

decision_date TEXT,
decision_action TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

status TEXT DEFAULT 'متداولة'

)

""")

conn.commit()

# =====================================
# تسجيل القضايا
# =====================================

if st.session_state.page == "cases":

    st.markdown("---")

    st.markdown(
        """
        <h2 style='text-align:center;color:white'>
        ⚖️ تسجيل القضايا
        </h2>
        """,
        unsafe_allow_html=True
    )

    litigation_type = st.selectbox(
        "نوع الإجراء",
        ["دعوى", "استئناف", "نقض"],
        key="litigation_type"
    )

    claimant_type = st.selectbox(
        "صفة الخصم الأول",
        ["المدعى", "المستأنف", "الطاعن"],
        key="claimant_type"
    )

    claimant = st.text_input(
        "اسم الخصم الأول",
        key="claimant"
    )

    defendant_type = st.selectbox(
        "صفة الخصم الثاني",
        ["المدعى عليه", "المستأنف ضده", "المطعون ضده"],
        key="defendant_type"
    )

    defendant = st.text_input(
        "اسم الخصم الثاني",
        key="defendant"
    )

    case_no = st.text_input(
        "رقم الدعوى",
        key="case_no"
    )

    judicial_year = st.text_input(
        "السنة القضائية",
        key="judicial_year"
    )

    circuit = st.text_input(
        "الدائرة",
        key="circuit"
    )

    case_type = st.text_input(
        "النوع",
        key="case_type"
    )

    court = st.selectbox(
        "المحكمة",
        [
            "الابتدائية",
            "الاستئناف",
            "النقض",
            "إدارية",
            "قضاء إدارى",
            "إدارية عليا"
        ],
        key="court"
    )

    court_name = st.text_input(
        "اسم المحكمة",
        key="court_name"
    )

    subject = st.text_area(
        "موضوع الدعوى",
        key="subject"
    )

    session_date = st.date_input(
        "تاريخ الجلسة",
        key="session_date"
    )

    session_action = st.text_area(
        "الإجراء المطلوب بالجلسة",
        key="session_action"
    )

    decision_date = st.date_input(
        "تاريخ القرار",
        key="decision_date"
    )

    decision_action = st.text_area(
        "الإجراء المطلوب بعد القرار",
        key="decision_action"
    )

    reason = st.text_area(
        "السبب",
        key="reason"
    )

    notes = st.text_area(
        "ملاحظات",
        key="notes"
    )

    judgment_result = st.selectbox(
        "نتيجة الدعوى",
        [
            "متداولة",
            "لصالح الهيئة",
            "ضد الهيئة"
        ],
        key="judgment_result"
    )

    mobile = st.text_input(
        "رقم الموبايل لإرسال التنبيهات",
        key="mobile"
    )

    if st.button(
        "💾 حفظ القضية",
        key="save_case"
    ):

        cur.execute("""

        INSERT INTO cases(

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
        session_action,

        decision_date,
        decision_action,

        reason,

        notes,

        judgment_result,

        mobile

        )

        VALUES(

        ?,?,?,?,?,?,
        ?,?,?,?,?,?,
        ?,?,?,?,?,?,
        ?,?,?,?

        )

        """,

        (

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

        str(session_date),
        session_action,

        str(decision_date),
        decision_action,

        reason,

        notes,

        judgment_result,

        mobile

        )

        )

        conn.commit()

        st.success("تم حفظ القضية بنجاح")

    st.markdown("---")

    st.subheader("📅 سجل القضايا حسب تاريخ الجلسات")

    cases_df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        ORDER BY session_date ASC
        """,
        conn
    )

    if not cases_df.empty:

        for _, row in cases_df.iterrows():

            with st.expander(
                f"{row['session_date']} | {row['case_no']}"
            ):

                st.write(
                    f"المدعى : {row['claimant']}"
                )

                st.write(
                    f"المدعى عليه : {row['defendant']}"
                )

                st.write(
                    f"موضوع الدعوى : {row['subject']}"
                )

                st.write(
                    f"الإجراء المطلوب بالجلسة : {row['session_action']}"
                )

                new_decision = st.text_area(
                    "إضافة قرار جديد",
                    key=f"new_decision_{row['id']}"
                )

                if st.button(
                    "حفظ القرار الجديد",
                    key=f"save_decision_{row['id']}"
                ):

                    old_notes = row["notes"] if row["notes"] else ""

                    notes_text = (
                        old_notes +
                        "\n" +
                        new_decision
                    )

                    cur.execute(
                        """
                        UPDATE cases
                        SET notes=?
                        WHERE id=?
                        """,
                        (
                            notes_text,
                            row["id"]
                        )
                    )

                    conn.commit()

                    st.success(
                        "تم حفظ القرار الجديد"
                    )

                    st.rerun()
