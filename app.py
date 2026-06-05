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
    background:#062456;
}

/* النصوص */

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
}

/* القوائم المنسدلة */

.stSelectbox div[data-baseweb="select"] > div{
    background:white !important;
    color:black !important;
}

div[role="option"]{
    color:black !important;
    background:white !important;
}

/* الإدخال */

input{
    color:black !important;
}

textarea{
    color:black !important;
}

/* اللوجو */

.logo-box{
    text-align:center;
}

.logo-icon{
    font-size:50px;
    margin-top:15px;
}

.logo-main{
    font-size:28px;
    font-weight:bold;
    margin-top:10px;
}

.logo-sub{
    font-size:22px;
    font-weight:bold;
    margin-top:10px;
}

.prepare{
    font-size:18px;
    margin-top:20px;
}

.name{
    font-size:28px;
    font-weight:bold;
    margin-top:10px;
}

.place{
    font-size:22px;
    font-weight:bold;
    margin-top:10px;
}

/* الأزرار */

div.stButton > button{
    width:320px;
    height:65px;
    border-radius:15px;
    border:none;
    background:#2f55d4;
    color:white;
    font-size:20px;
    font-weight:bold;
    display:block;
    margin:auto;
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
# صفحة تسجيل القضايا
# =====================================

if st.session_state.page == "cases":

    st.markdown("---")

    st.markdown(
        """
        <h2 style='text-align:center'>
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

        cur.execute(
            """
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

    df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        ORDER BY session_date ASC
        """,
        conn
    )

    if not df.empty:

        st.dataframe(
            df,
            use_container_width=True
        )
