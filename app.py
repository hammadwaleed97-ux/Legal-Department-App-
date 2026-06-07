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
# جدول القضايا
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

appeal_office TEXT,

subject TEXT,

session_date TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

status TEXT DEFAULT 'متداولة',

created_at TEXT

)

""")

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
# ترقية قواعد البيانات القديمة
# =====================================

try:
    cur.execute(
        "ALTER TABLE cases ADD COLUMN appeal_office TEXT"
    )
except:
    pass

conn.commit()

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

.stApp{
    background:#062456;
}

h1,h2,h3,h4,h5,h6,
label,p,span{
    color:white !important;
}

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

.stTextInput input{
    color:black !important;
}

.stTextArea textarea{
    color:black !important;
}

.stDateInput input{
    color:black !important;
}

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
}

.logo-sub{
    font-size:24px;
    font-weight:900;
    color:white;
}

.logo-place{
    font-size:22px;
    font-weight:900;
    color:white;
}

.logo-greeting{
    font-size:20px;
    font-weight:bold;
    color:white;
}

.logo-name{
    font-size:32px;
    font-weight:900;
    color:#FFD700;
}

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
الإدارة العامة للشئون القانونية
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

    if st.button("📋 حصر عام القضايا"):
        st.session_state.page = "all_cases"

    if st.button("🔍 البحث"):
        st.session_state.page = "search"

    if st.button("❌ القضايا المحذوفة"):
        st.session_state.page = "deleted"
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
        ["دعوى", "استئناف", "نقض"]
    )

    claimant_type = st.selectbox(
        "صفة الخصم الأول",
        ["المدعى", "المستأنف", "الطاعن"]
    )

    claimant = st.text_input(
        "اسم الخصم الأول"
    )

    defendant_type = st.selectbox(
        "صفة الخصم الثاني",
        ["المدعى عليه", "المستأنف ضده", "المطعون ضده"]
    )

    defendant = st.text_input(
        "اسم الخصم الثاني"
    )

    case_no = st.text_input(
        "رقم الدعوى / الاستئناف / الطعن"
    )

    judicial_year = st.text_input(
        "السنة القضائية"
    )

    circuit = st.text_input(
        "الدائرة"
    )

    case_type = st.text_input(
        "نوع الدعوى"
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
        ]
    )

    court_name = st.text_input(
        "اسم المحكمة"
    )

    appeal_office = ""

    if litigation_type == "استئناف":

        appeal_office = st.text_input(
            "مأمورية الاستئناف"
        )

    subject = st.text_area(
        "موضوع الدعوى"
    )

    session_date = st.date_input(
        "تاريخ الجلسة"
    )

    reason = st.text_area(
        "السبب والإجراء المطلوب"
    )

    notes = st.text_area(
        "ملاحظات"
    )

    judgment_result = st.selectbox(
        "حالة الدعوى",
        [
            "متداولة",
            "لصالح الهيئة",
            "ضد الهيئة"
        ]
    )

    mobile = st.text_input(
        "رقم الهاتف"
    )

    if st.button("💾 حفظ القضية"):

        cur.execute(
            """
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
                appeal_office,
                subject,
                session_date,
                reason,
                notes,
                judgment_result,
                mobile,
                created_at
            )
            VALUES
            (
                ?,?,?,?,?,?,
                ?,?,?,?,?,?,
                ?,?,?,?,?,?,
                ?,?
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
                appeal_office,
                subject,
                str(session_date),
                reason,
                notes,
                judgment_result,
                mobile,
                str(datetime.now())
            )
        )

        conn.commit()

        st.success("تم حفظ القضية بنجاح")
# =====================================
# الحصر العام للقضايا
# =====================================

elif st.session_state.page == "all_cases":

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

            last_update = cur.execute(
                """
                SELECT
                next_session_date,
                adjournment_reason
                FROM case_updates
                WHERE case_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (row["id"],)
            ).fetchone()

            last_session = row["session_date"]
            last_reason = ""

            if last_update:

                if last_update[0]:
                    last_session = last_update[0]

                if last_update[1]:
                    last_reason = last_update[1]

            defendant_name = row["defendant"]

            if "الهيئة القومية للتأمين" in defendant_name:
                defendant_name = "الهيئة"

            title = f"""
{row['claimant']} ضد {defendant_name}

{row['litigation_type']} {row['case_no']} لسنة {row['judicial_year']}

الدائرة {row['circuit']}

محكمة {row['court']}

{row['court_name']}

جلسة {last_session}

{last_reason}
"""

            with st.expander(title):

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
                    f"المحكمة : {row['court']}"
                )

                st.write(
                    f"اسم المحكمة : {row['court_name']}"
                )

                if row["appeal_office"]:

                    st.write(
                        f"مأمورية الاستئناف : {row['appeal_office']}"
                    )

                st.write(
                    f"موضوع الدعوى : {row['subject']}"
                )

                st.write(
                    f"السبب والإجراء المطلوب : {row['reason']}"
                )

                st.write(
                    f"الحالة : {row['judgment_result']}"
                )

                st.markdown("---")

                delete_reason = st.text_input(
                    "سبب الحذف",
                    key=f"del_{row['id']}"
                )

                if st.button(
                    "❌ حذف القضية",
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
                        VALUES (?,?,?,?,?,?,?,?,?)
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
                        WHERE id = ?
                        """,
                        (row["id"],)
                    )

                    conn.commit()

                    st.success(
                        "تم نقل القضية إلى سجل المحذوفات"
                    )

                    st.rerun()

                st.markdown("---")

                st.subheader("متابعة القضية")

                adjournment_reason = st.text_area(
                    "سبب القرار أو التأجيل",
                    key=f"adj_{row['id']}"
                )

                next_session_date = st.date_input(
                    "الجلسة القادمة",
                    key=f"next_{row['id']}"
                )

                status_reason = st.text_area(
                    "ملاحظات المتابعة",
                    key=f"status_{row['id']}"
                )

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
                        VALUES (?,?,?,?,?)
                        """,
                        (
                            row["id"],
                            str(datetime.now()),
                            adjournment_reason,
                            str(next_session_date),
                            status_reason
                        )
                    )

                    conn.commit()

                    st.success("تم حفظ المتابعة")

                    st.rerun()
# =====================================
# البحث عن دعوى
# =====================================

elif st.session_state.page == "search":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    🔍 البحث عن دعوى
    </h2>
    """, unsafe_allow_html=True)

    search_text = st.text_input(
        "اكتب رقم الدعوى أو اسم أحد الخصوم أو موضوع الدعوى"
    )

    if search_text:

        result = pd.read_sql_query(
            """
            SELECT *
            FROM cases
            WHERE
            claimant LIKE ?
            OR defendant LIKE ?
            OR case_no LIKE ?
            OR subject LIKE ?
            ORDER BY session_date ASC
            """,
            conn,
            params=(
                f"%{search_text}%",
                f"%{search_text}%",
                f"%{search_text}%",
                f"%{search_text}%"
            )
        )

        if result.empty:

            st.warning("لا توجد نتائج")

        else:

            st.success(
                f"تم العثور على {len(result)} قضية"
            )

            for _, row in result.iterrows():

                last_update = cur.execute(
                    """
                    SELECT
                    next_session_date,
                    adjournment_reason
                    FROM case_updates
                    WHERE case_id = ?
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (row["id"],)
                ).fetchone()

                last_session = row["session_date"]
                last_reason = ""

                if last_update:

                    if last_update[0]:
                        last_session = last_update[0]

                    if last_update[1]:
                        last_reason = last_update[1]

                title = (
                    f"{row['claimant']} ضد "
                    f"{row['defendant']} | "
                    f"{row['litigation_type']} "
                    f"{row['case_no']}"
                )

                with st.expander(title):

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
                        f"المحكمة : {row['court']}"
                    )

                    st.write(
                        f"اسم المحكمة : {row['court_name']}"
                    )

                    if row["appeal_office"]:

                        st.write(
                            f"مأمورية الاستئناف : "
                            f"{row['appeal_office']}"
                        )

                    st.write(
                        f"موضوع الدعوى : {row['subject']}"
                    )

                    st.write(
                        f"آخر جلسة : {last_session}"
                    )

                    st.write(
                        f"آخر إجراء : {last_reason}"
                    )

                    st.write(
                        f"الحالة : "
                        f"{row['judgment_result']}"
                    )
# =====================================
# التنبيهات
# =====================================

elif st.session_state.page == "alerts":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    🔔 التنبيهات
    </h2>
    """, unsafe_allow_html=True)

    today = datetime.today().date()

    st.subheader("📅 جلسات خلال 7 أيام")

    found_sessions = False

    cases_df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        WHERE judgment_result='متداولة'
        """,
        conn
    )

    for _, row in cases_df.iterrows():

        try:

            session_date = datetime.strptime(
                row["session_date"],
                "%Y-%m-%d"
            ).date()

            days_left = (
                session_date - today
            ).days

            if 0 <= days_left <= 7:

                found_sessions = True

                st.warning(
                    f"متبقى {days_left} يوم على جلسة القضية رقم {row['case_no']}"
                )

                st.write(
                    f"{row['claimant']} ضد {row['defendant']}"
                )

                st.write(
                    f"المحكمة : {row['court']}"
                )

                st.write(
                    f"اسم المحكمة : {row['court_name']}"
                )

                st.write(
                    f"الجلسة : {row['session_date']}"
                )

                st.markdown("---")

        except:
            pass

    if not found_sessions:

        st.success(
            "لا توجد جلسات خلال 7 أيام"
        )

    st.markdown("---")

    st.subheader(
        "⚖️ مواعيد طعن خلال 15 يوم"
    )

    found_appeals = False

    judgments_df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        WHERE judgment_result <> 'متداولة'
        """,
        conn
    )

    for _, row in judgments_df.iterrows():

        try:

            judgment_date = datetime.strptime(
                row["created_at"][:10],
                "%Y-%m-%d"
            ).date()

            deadline = (
                judgment_date + timedelta(days=40)
            )

            remaining = (
                deadline - today
            ).days

            if 0 <= remaining <= 15:

                found_appeals = True

                st.error(
                    f"متبقى {remaining} يوم على انتهاء ميعاد الطعن"
                )

                st.write(
                    f"{row['claimant']} ضد {row['defendant']}"
                )

                st.write(
                    f"رقم الدعوى : {row['case_no']}"
                )

                st.write(
                    f"المحكمة : {row['court']}"
                )

                st.write(
                    f"الحكم : {row['judgment_result']}"
                )

                st.markdown("---")

        except:
            pass

    if not found_appeals:

        st.success(
            "لا توجد مواعيد طعن خلال 15 يوم"
        )
# =====================================
# التقارير
# =====================================

elif st.session_state.page == "reports":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📊 التقارير
    </h2>
    """, unsafe_allow_html=True)

    region_name = st.text_input(
        "اسم المنطقة"
    )

    lawyer_name = st.text_input(
        "اسم الأستاذ"
    )

    report_type = st.selectbox(
        "نوع التقرير",
        [
            "كشف بالدعاوى",
            "كشف بالأحكام"
        ]
    )

    if report_type == "كشف بالدعاوى":

        cases_option = st.selectbox(
            "نوع القضايا",
            [
                "المتداولة فقط",
                "الجميع"
            ]
        )

    date_from = st.date_input(
        "من تاريخ",
        key="report_from"
    )

    date_to = st.date_input(
        "إلى تاريخ",
        key="report_to"
    )

    if st.button("عرض التقرير"):

        if report_type == "كشف بالدعاوى":

            query = """
            SELECT *
            FROM cases
            WHERE session_date BETWEEN ? AND ?
            """

            params = [
                str(date_from),
                str(date_to)
            ]

            if cases_option == "المتداولة فقط":

                query += """
                AND judgment_result='متداولة'
                """

            report_df = pd.read_sql_query(
                query,
                conn,
                params=params
            )

            report_title = (
                "كشف بالدعاوى المتداولة"
                if cases_option == "المتداولة فقط"
                else
                "كشف بالدعاوى"
            )

        else:

            report_df = pd.read_sql_query(
                """
                SELECT *
                FROM cases
                WHERE judgment_result<>'متداولة'
                AND session_date BETWEEN ? AND ?
                """,
                conn,
                params=(
                    str(date_from),
                    str(date_to)
                )
            )

            report_title = "كشف بالأحكام الصادرة"

        st.markdown(f"""
        <div style='text-align:center;color:white'>

        <h3>
        الهيئة القومية للتأمين الاجتماعى
        </h3>

        <h3>
        الإدارة العامة للشئون القانونية
        </h3>

        <h3>
        ديوان عام منطقة {region_name}
        </h3>

        <br>

        <h3>
        {report_title}
        خلال الفترة من
        {date_from}
        حتى
        {date_to}
        طرف الأستاذ / {lawyer_name}
        </h3>

        </div>
        """, unsafe_allow_html=True)

        report_rows = []

        for _, row in report_df.iterrows():

            update = cur.execute(
                """
                SELECT
                next_session_date,
                adjournment_reason
                FROM case_updates
                WHERE case_id = ?
                ORDER BY id DESC
                LIMIT 1
                """,
                (row["id"],)
            ).fetchone()

            last_session = row["session_date"]
            last_reason = ""

            if update:

                if update[0]:
                    last_session = update[0]

                if update[1]:
                    last_reason = update[1]

            defendant_name = row["defendant"]

            if "الهيئة القومية للتأمين" in defendant_name:
                defendant_name = "الهيئة"

            report_rows.append({

                "م": row["id"],

                "رقم الدعوى":
                row["case_no"],

                "السنة القضائية":
                row["judicial_year"],

                "الدائرة":
                row["circuit"],

                "المحكمة":
                f"{row['court']} - {row['court_name']}",

                "الخصوم":
                f"{row['claimant']} ضد {defendant_name}",

                "موضوع الدعوى":
                row["subject"],

                "آخر إجراء":
                f"جلسة {last_session}\n{last_reason}"

            })

        final_df = pd.DataFrame(report_rows)

        if final_df.empty:

            st.warning(
                "لا توجد بيانات خلال الفترة المحددة"
            )

        else:

            st.dataframe(
                final_df,
                use_container_width=True,
                hide_index=True
            )

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("""
        <div style='text-align:center;color:white;font-size:20px'>

        وتفضلوا سيادتكم بقبول وافر الاحترام والتقدير

        <br><br><br>

        عضو الإدارة
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        مدير الإدارة

        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:

            st.button(
                "📄 فتح Word",
                key="word_report"
            )

        with col2:

            st.button(
                "📕 حفظ PDF",
                key="pdf_report"
            )
# =====================================
# أرشيف القضايا
# =====================================

elif st.session_state.page == "archive":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📂 أرشيف القضايا
    </h2>
    """, unsafe_allow_html=True)

    archive_df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        WHERE judgment_result <> 'متداولة'
        ORDER BY session_date DESC
        """,
        conn
    )

    if archive_df.empty:

        st.warning(
            "لا توجد قضايا مؤرشفة"
        )

    else:

        st.success(
            f"عدد القضايا المؤرشفة : {len(archive_df)}"
        )

        for _, row in archive_df.iterrows():

            update = cur.execute(
                """
                SELECT
                next_session_date,
                adjournment_reason
                FROM case_updates
                WHERE case_id=?
                ORDER BY id DESC
                LIMIT 1
                """,
                (row["id"],)
            ).fetchone()

            last_session = row["session_date"]
            last_reason = ""

            if update:

                if update[0]:
                    last_session = update[0]

                if update[1]:
                    last_reason = update[1]

            defendant_name = row["defendant"]

            if "الهيئة القومية للتأمين" in defendant_name:
                defendant_name = "الهيئة"

            title = f"""
{row['claimant']} ضد {defendant_name}

{row['litigation_type']} {row['case_no']} لسنة {row['judicial_year']}

الدائرة {row['circuit']}

محكمة {row['court']}
{row['court_name']}

الحكم : {row['judgment_result']}
"""

            with st.expander(title):

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
                    f"المحكمة : {row['court']}"
                )

                st.write(
                    f"اسم المحكمة : {row['court_name']}"
                )

                if row["appeal_office"]:

                    st.write(
                        f"مأمورية الاستئناف : {row['appeal_office']}"
                    )

                st.write(
                    f"موضوع الدعوى : {row['subject']}"
                )

                st.write(
                    f"آخر جلسة : {last_session}"
                )

                st.write(
                    f"آخر إجراء : {last_reason}"
                )

                st.write(
                    f"نتيجة الحكم : {row['judgment_result']}"
                )
# =====================================
# القضايا المحذوفة
# =====================================

elif st.session_state.page == "deleted":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    ❌ القضايا المحذوفة
    </h2>
    """, unsafe_allow_html=True)

    deleted_df = pd.read_sql_query(
        """
        SELECT *
        FROM deleted_cases
        ORDER BY deleted_at DESC
        """,
        conn
    )

    if deleted_df.empty:

        st.warning(
            "لا توجد قضايا محذوفة"
        )

    else:

        st.success(
            f"عدد القضايا المحذوفة : {len(deleted_df)}"
        )

        for _, row in deleted_df.iterrows():

            title = f"""
{row['claimant']} ضد {row['defendant']}

{row['litigation_type']}
رقم {row['case_no']}
لسنة {row['judicial_year']}
"""

            with st.expander(title):

                st.write(
                    f"الخصم الأول : {row['claimant']}"
                )

                st.write(
                    f"الخصم الثاني : {row['defendant']}"
                )

                st.write(
                    f"رقم الدعوى : {row['case_no']}"
                )

                st.write(
                    f"السنة القضائية : {row['judicial_year']}"
                )

                st.write(
                    f"موضوع الدعوى : {row['subject']}"
                )

                st.write(
                    f"سبب الحذف : {row['delete_reason']}"
                )

                st.write(
                    f"تاريخ الحذف : {row['deleted_at']}"
                )
# =====================================
# التنبيهات
# =====================================

elif st.session_state.page == "alerts":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    🔔 التنبيهات
    </h2>
    """, unsafe_allow_html=True)

    today = datetime.today().date()

    st.subheader("📅 جلسات خلال 7 أيام")

    found_sessions = False

    cases_df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        WHERE judgment_result='متداولة'
        """,
        conn
    )

    for _, row in cases_df.iterrows():

        try:

            update = cur.execute(
                """
                SELECT
                next_session_date,
                adjournment_reason
                FROM case_updates
                WHERE case_id=?
                ORDER BY id DESC
                LIMIT 1
                """,
                (row["id"],)
            ).fetchone()

            session_date = row["session_date"]

            if update and update[0]:
                session_date = update[0]

            session_obj = datetime.strptime(
                session_date,
                "%Y-%m-%d"
            ).date()

            days_left = (
                session_obj - today
            ).days

            if 0 <= days_left <= 7:

                found_sessions = True

                st.warning(
                    f"متبقى {days_left} يوم على الجلسة"
                )

                defendant_name = row["defendant"]

                if "الهيئة القومية للتأمين" in defendant_name:
                    defendant_name = "الهيئة"

                st.write(
                    f"**{row['claimant']} ضد {defendant_name}**"
                )

                st.write(
                    f"{row['litigation_type']} {row['case_no']} لسنة {row['judicial_year']}"
                )

                st.write(
                    f"الدائرة {row['circuit']}"
                )

                st.write(
                    f"محكمة {row['court']}"
                )

                st.write(
                    row['court_name']
                )

                st.write(
                    f"جلسة {session_date}"
                )

                st.markdown("---")

        except:
            pass

    if not found_sessions:

        st.success(
            "لا توجد جلسات خلال 7 أيام"
        )

    st.markdown("---")

    st.subheader("⚖️ مواعيد طعن خلال 15 يوم")

    found_appeals = False

    judgments_df = pd.read_sql_query(
        """
        SELECT *
        FROM cases
        WHERE judgment_result<>'متداولة'
        """,
        conn
    )

    for _, row in judgments_df.iterrows():

        try:

            judgment_date = datetime.strptime(
                row["created_at"][:10],
                "%Y-%m-%d"
            ).date()

            deadline = (
                judgment_date + timedelta(days=40)
            )

            remaining = (
                deadline - today
            ).days

            if 0 <= remaining <= 15:

                found_appeals = True

                st.error(
                    f"متبقى {remaining} يوم على انتهاء ميعاد الطعن"
                )

                defendant_name = row["defendant"]

                if "الهيئة القومية للتأمين" in defendant_name:
                    defendant_name = "الهيئة"

                st.write(
                    f"**{row['claimant']} ضد {defendant_name}**"
                )

                st.write(
                    f"{row['litigation_type']} {row['case_no']} لسنة {row['judicial_year']}"
                )

                st.write(
                    f"الدائرة {row['circuit']}"
                )

                st.write(
                    f"محكمة {row['court']}"
                )

                st.write(
                    row['court_name']
                )

                st.write(
                    f"الحكم : {row['judgment_result']}"
                )

                st.markdown("---")

        except:
            pass

    if not found_appeals:

        st.success(
            "لا توجد مواعيد طعن خلال 15 يوم"
        )
