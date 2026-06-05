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

h1,h2,h3,h4,h5,h6,
label,p,span{
    color:white !important;
}

/* القوائم المنسدلة */

.stSelectbox div[data-baseweb="select"] > div{
    background:white !important;
    color:black !important;
}

div[role="option"]{
    background:white !important;
    color:black !important;
}

div[role="listbox"] div{
    color:black !important;
}

[data-baseweb="popover"] *{
    color:black !important;
}

/* الإدخال */

.stTextInput input{
    color:black !important;
}

.stTextArea textarea{
    color:black !important;
}

.stDateInput input{
    color:black !important;
}

/* اللوجو */

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:52px;
    margin-top:15px;
    margin-bottom:10px;
}

.logo-main{
    font-size:26px;
    font-weight:900;
    color:white;
    text-shadow:2px 2px 4px black;
    margin-bottom:12px;
    white-space:nowrap;
}

.logo-sub{
    font-size:24px;
    font-weight:900;
    color:white;
    text-shadow:2px 2px 4px black;
    margin-bottom:12px;
}

.logo-place{
    font-size:22px;
    font-weight:900;
    color:white;
    text-shadow:2px 2px 4px black;
    margin-bottom:20px;
}

.logo-greeting{
    font-size:20px;
    font-weight:bold;
    color:white;
    margin-bottom:10px;
}

.logo-name{
    font-size:32px;
    font-weight:900;
    color:#FFD700;
    text-shadow:2px 2px 4px black;
    margin-bottom:30px;
}

/* الأزرار */

div.stButton > button{
    width:340px;
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

div.stButton > button:hover{
    background:#4b6df0;
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

<div class="logo-place">
ديوان عام منطقة البحيرة
</div>

<div class="logo-greeting">
مع تحيات
</div>

<div class="logo-name">
وليد شعبان حماد
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

    if st.button("📋 حصر عام القضايا المتداولة"):
        st.session_state.page = "all_cases"

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

status TEXT DEFAULT 'متداولة',

created_at TEXT

)

""")

# =====================================
# جدول القضايا المحذوفة
# =====================================

cur.execute("""

CREATE TABLE IF NOT EXISTS deleted_cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

original_case_id INTEGER,

litigation_type TEXT,

claimant TEXT,

defendant TEXT,

case_no TEXT,

judicial_year TEXT,

subject TEXT,

delete_reason TEXT,

deleted_at TEXT

)

""")

conn.commit()

# =====================================
# تعريف الصفحات
# =====================================

if st.session_state.page == "alerts":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    🔔 التنبيهات
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة التنبيهات فى الجزء القادم")

elif st.session_state.page == "reports":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📊 التقارير
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة التقارير فى الجزء القادم")

elif st.session_state.page == "archive":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📂 أرشيف القضايا
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة الأرشيف فى الجزء القادم")

elif st.session_state.page == "all_cases":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📋 حصر عام القضايا المتداولة
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة الحصر العام فى الجزء القادم")

elif st.session_state.page == "search":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    🔍 البحث عن دعوى
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة البحث فى الجزء القادم")

elif st.session_state.page == "deleted":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    ❌ القضايا المحذوفة
    </h2>
    """, unsafe_allow_html=True)

    st.info("سيتم إضافة سجل المحذوفات فى الجزء القادم")
# ==
# =====================================
# تسجيل القضايا
# =====================================

if st.session_state.page == "cases":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    ⚖️ تسجيل القضايا
    </h2>
    """, unsafe_allow_html=True)

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
            "قضاء إداري",
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

    if st.button("💾 حفظ القضية", key="save_case"):

        try:

            cur.execute("""
            INSERT INTO cases
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
                session_date,
                session_action,
                decision_date,
                decision_action,
                reason,
                notes,
                judgment_result,
                mobile
            )
            VALUES
            (
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?
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
            ))

            conn.commit()

            st.success("تم حفظ القضية بنجاح")

        except Exception as e:

            st.error(f"خطأ أثناء الحفظ: {e}")
            
from datetime import datetime
# =====================================
# جدول متابعات القضايا
# =====================================

cur.execute("""

CREATE TABLE IF NOT EXISTS case_updates(

id INTEGER PRIMARY KEY AUTOINCREMENT,

case_id INTEGER,

update_date TEXT,

adjournment_reason TEXT,

next_session_date TEXT,

status_reason TEXT

)

""")

conn.commit()
# =====================================
# الحصر العام للقضايا
# =====================================

if st.session_state.page == "all_cases":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📋 حصر عام القضايا المتداولة
    </h2>
    """, unsafe_allow_html=True)

    cases_df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        ORDER BY session_date ASC
        """,
        conn
    )

    if cases_df.empty:

        st.warning("لا توجد قضايا مسجلة")

    else:

        for _, row in cases_df.iterrows():

            title = (
                f"{row['claimant']} ضد {row['defendant']} | "
                f"رقم {row['case_no']} لسنة {row['judicial_year']} | "
                f"{row['case_type']} | "
                f"{row['subject']} | "
                f"جلسة {row['session_date']}"
            )

            with st.expander(title):

                st.write(
                    f"الخصوم : {row['claimant']} ضد {row['defendant']}"
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
                    f"نوع الإجراء : {row['litigation_type']}"
                )

                st.write(
                    f"نوع الدعوى : {row['case_type']}"
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
                    f"الإجراء المطلوب : {row['session_action']}"
                )

                st.markdown("---")

                st.subheader("متابعة القضية")

                adjournment_reason = st.text_area(
                    "سبب التأجيل",
                    key=f"adj_{row['id']}"
                )

                next_session_date = st.date_input(
                    "الجلسة القادمة",
                    key=f"next_{row['id']}"
                )

                status_reason = st.text_area(
                    "ملاحظات الجلسة الجديدة",
                    key=f"reason_{row['id']}"
                )

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "💾 حفظ المتابعة",
                        key=f"save_{row['id']}"
                    ):

                        cur.execute(
                            """
                            INSERT INTO case_updates
                            (
                            case_id,
                            update_date,
                            adjournment_reason,
                            next_session_date,
                            status_reason
                            )
                            VALUES(?,?,?,?,?)
                            """,
                            (
                                row["id"],
                                str(datetime.now()),
                                adjournment_reason,
                                str(next_session_date),
                                status_reason
                            )
                        )

                        cur.execute(
                            """
                            UPDATE cases
                            SET session_date=?
                            WHERE id=?
                            """,
                            (
                                str(next_session_date),
                                row["id"]
                            )
                        )

                        conn.commit()

                        st.success(
                            "تم حفظ المتابعة"
                        )

                        st.rerun()

                with col2:

                    delete_reason = st.text_input(
                        "سبب الحذف",
                        key=f"delete_reason_{row['id']}"
                    )

                    if st.button(
                        "🗑 حذف القضية",
                        key=f"delete_{row['id']}"
                    ):

                        cur.execute(
                            """
                            INSERT INTO deleted_cases
                            (
                            original_case_id,
                            litigation_type,
                            claimant,
                            defendant,
                            case_no,
                            judicial_year,
                            subject,
                            delete_reason,
                            deleted_at
                            )
                            VALUES(?,?,?,?,?,?,?,?,?)
                            """,
                            (
                                row["id"],
                                row["litigation_type"],
                                row["claimant"],
                                row["defendant"],
                                row["case_no"],
                                row["judicial_year"],
                                row["subject"],
                                delete_reason,
                                str(datetime.now())
                            )
                        )

                        cur.execute(
                            """
                            DELETE FROM cases
                            WHERE id=?
                            """,
                            (row["id"],)
                        )

                        conn.commit()

                        st.success(
                            "تم نقل القضية إلى المحذوفات"
                        )

                        st.rerun()

                st.markdown("---")

                st.subheader("السجل التاريخي")

                history = pd.read_sql_query(
                    """
                    SELECT *
                    FROM case_updates
                    WHERE case_id=?
                    ORDER BY id DESC
                    """,
                    conn,
                    params=(row["id"],)
                )

                if history.empty:

                    st.info(
                        "لا توجد متابعات سابقة"
                    )

                else:

                    for _, h in history.iterrows():

                        st.write(
                            f"📅 تاريخ المتابعة : {h['update_date']}"
                        )

                        st.write(
                            f"📌 سبب التأجيل : {h['adjournment_reason']}"
                        )

                        st.write(
                            f"📆 الجلسة القادمة : {h['next_session_date']}"
                        )

                        st.write(
                            f"📝 الملاحظات : {h['status_reason']}"
                        )

                        st.markdown("---")
