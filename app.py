import streamlit as st

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp{
    background-color:#062456;
}

.block-container{
    padding-top:5px;
}

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:60px;
    margin-top:25px;
    margin-bottom:10px;
}

.logo-main{
    font-size:30px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:20px;
}

.logo-sub{
    font-size:24px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:45px;
}

.prepare{
    font-size:20px;
    margin-bottom:10px;
}

.name{
    font-size:32px;
    font-weight:bold;
    margin-bottom:15px;
}

.place{
    font-size:24px;
    font-weight:bold;
    margin-bottom:35px;
}

div.stButton > button{
    width:280px;
    height:70px;
    border-radius:18px;
    border:none;
    font-size:21px;
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

# =========================
# اللوجو
# =========================

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

# =========================
# القائمة الرئيسية
# =========================

col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.button("⚖️ تسجيل القضايا")

    st.button("🔔 التنبيهات")

    st.button("📊 التقارير")

    st.button("📂 أرشيف القضايا")

    st.button("🔍 البحث عن دعوى")

    st.button("❌ القضايا المحذوفة")
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

decision_date TEXT,

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

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "cases":

    st.markdown("""
    <h2 style='color:white;text-align:center'>
    ⚖️ تسجيل القضايا
    </h2>
    """, unsafe_allow_html=True)

    litigation_type = st.selectbox(
        "نوع الإجراء",
        [
            "دعوى",
            "استئناف",
            "نقض"
        ]
    )

    claimant_type = st.selectbox(
        "صفة الخصم الأول",
        [
            "المدعى",
            "المستأنف",
            "الطاعن"
        ]
    )

    claimant = st.text_input(
        "اسم الخصم الأول"
    )

    defendant_type = st.selectbox(
        "صفة الخصم الثاني",
        [
            "المدعى عليه",
            "المستأنف ضده",
            "المطعون ضده"
        ]
    )

    defendant = st.text_input(
        "اسم الخصم الثاني"
    )

    case_no = st.text_input(
        "رقم الدعوى"
    )

    judicial_year = st.text_input(
        "السنة القضائية"
    )

    circuit = st.text_input(
        "الدائرة"
    )

    case_type = st.text_input(
        "النوع"
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
        ]
    )

    court_name = st.text_input(
        "اسم المحكمة"
    )

    subject = st.text_area(
        "موضوع الدعوى"
    )

    session_date = st.date_input(
        "تاريخ الجلسة"
    )

    decision_date = st.date_input(
        "تاريخ القرار"
    )

    reason = st.text_area(
        "السبب"
    )

    notes = st.text_area(
        "ملاحظات"
    )

    judgment_result = st.selectbox(
        "نتيجة الدعوى",
        [
            "متداولة",
            "لصالح الهيئة",
            "ضد الهيئة"
        ]
    )

    mobile = st.text_input(
        "رقم الموبايل لإرسال التنبيهات"
    )

    if st.button("💾 حفظ القضية"):

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

        decision_date,

        reason,

        notes,

        judgment_result,

        mobile

        )

        VALUES(

        ?,?,?,?,?,?,
        ?,?,?,?,?,?,
        ?,?,?,?,?,?,?

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

        str(decision_date),

        reason,

        notes,

        judgment_result,

        mobile

        )

        )

        conn.commit()

        st.success(
            "تم حفظ القضية بنجاح"
        )
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
# =====================================
# القضايا المحذوفة
# =====================================

if st.session_state.page == "deleted":

    st.markdown("""
    <h2 style='text-align:center'>
    ❌ القضايا المحذوفة
    </h2>
    """, unsafe_allow_html=True)

    search_deleted = st.text_input(
        "البحث داخل القضايا المحذوفة"
    )

    deleted_df = pd.read_sql_query(
        "SELECT * FROM deleted_cases ORDER BY id DESC",
        conn
    )

    if search_deleted:

        deleted_df = deleted_df[
            deleted_df.astype(str)
            .apply(
                lambda row:
                row.str.contains(
                    search_deleted,
                    case=False,
                    na=False
                ).any(),
                axis=1
            )
        ]

    if not deleted_df.empty:

        for _, row in deleted_df.iterrows():

            with st.expander(

                f"{row['case_no']} / {row['judicial_year']}"

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
                    f"القرار : {row['judgment_result']}"
                )

                st.write(
                    f"سبب الحذف : {row['delete_reason']}"
                )

                st.write(
                    f"تاريخ الحذف : {row['delete_date']}"
                )

    else:

        st.info(
            "لا توجد قضايا محذوفة"
        )
# =====================================
# التنبيهات
# =====================================

if st.session_state.page == "alerts":

    st.markdown("""
    <h2 style='text-align:center'>
    🔔 التنبيهات
    </h2>
    """, unsafe_allow_html=True)

    today = datetime.now().date()

    cases_df = pd.read_sql_query(
        "SELECT * FROM cases",
        conn
    )

    session_alerts = []
    appeal_alerts = []

    if not cases_df.empty:

        for _, row in cases_df.iterrows():

            # =====================
            # تنبيه الجلسات
            # =====================

            try:

                session_date = datetime.strptime(
                    row["session_date"],
                    "%Y-%m-%d"
                ).date()

                days_left = (
                    session_date - today
                ).days

                if 0 <= days_left <= 7:

                    session_alerts.append(row)

            except:
                pass

            # =====================
            # تنبيه الطعن
            # =====================

            try:

                if row["judgment_result"] == "ضد الهيئة":

                    decision_date = datetime.strptime(
                        row["decision_date"],
                        "%Y-%m-%d"
                    ).date()

                    appeal_deadline = (
                        decision_date +
                        timedelta(days=40)
                    )

                    remaining = (
                        appeal_deadline - today
                    ).days

                    if 0 <= remaining <= 15:

                        appeal_alerts.append(row)

            except:
                pass

    total_alerts = (
        len(session_alerts)
        +
        len(appeal_alerts)
    )

    st.error(
        f"عدد التنبيهات الحالية : {total_alerts}"
    )

    st.markdown("---")

    st.subheader(
        "🔴 القضايا التي يتبقى على جلساتها أسبوع أو أقل"
    )

    if session_alerts:

        for row in session_alerts:

            st.warning(

                f"""⬅️ جلسة بتاريخ
                {row['session_date']}

                | رقم الدعوى:
                {row['case_no']}

                | {row['claimant']}
                ضد
                {row['defendant']}
                """

            )

    else:

        st.success(
            "لا توجد جلسات خلال الأسبوع القادم"
        )

    st.markdown("---")

    st.subheader(
        "🔴 أحكام ضد الهيئة وقرب انتهاء ميعاد الطعن"
    )

    if appeal_alerts:

        for row in appeal_alerts:

            st.error(

                f"""⬅️ آخر ميعاد للطعن يقترب

                رقم الدعوى:
                {row['case_no']}

                {row['claimant']}
                ضد
                {row['defendant']}
                """

            )

    else:

        st.success(
            "لا توجد مواعيد طعن قريبة"
        )
# =====================================
# جدول الأرشيف
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS archive_cases(

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

archive_date TEXT

)
""")

conn.commit()

# =====================================
# نقل قضية للأرشيف
# =====================================

def archive_case(row):

    cur.execute("""

    INSERT INTO archive_cases(

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

    archive_date

    )

    VALUES(

    ?,?,?,?,?,?,
    ?,?,?,?,?,?,
    ?,?,?,?,?,?,
    ?,?

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

    str(datetime.now())

    )

    )

    cur.execute(
        "DELETE FROM cases WHERE id=?",
        (row["id"],)
    )

    conn.commit()

# =====================================
# البحث عن دعوى
# =====================================

if st.session_state.page == "search":

    st.markdown("""
    <h2 style='text-align:center'>
    🔍 البحث عن دعوى
    </h2>
    """, unsafe_allow_html=True)

    search_type = st.radio(

        "طريقة البحث",

        [

            "برقم وسنة الدعوى",

            "بالاسم"

        ]

    )

    result_df = pd.DataFrame()

    if search_type == "برقم وسنة الدعوى":

        case_no_search = st.text_input(
            "رقم الدعوى"
        )

        year_search = st.text_input(
            "السنة القضائية"
        )

        if st.button("بحث"):

            result_df = pd.read_sql_query(

                f"""

                SELECT *

                FROM cases

                WHERE case_no='{case_no_search}'

                AND judicial_year='{year_search}'

                """,

                conn

            )

    else:

        name_search = st.text_input(
            "اسم الخصم"
        )

        if st.button("بحث بالاسم"):

            result_df = pd.read_sql_query(

                f"""

                SELECT *

                FROM cases

                WHERE claimant LIKE '%{name_search}%'

                OR defendant LIKE '%{name_search}%'

                """,

                conn

            )

    if not result_df.empty:

        st.success(
            f"تم العثور على {len(result_df)} نتيجة"
        )

        st.dataframe(
            result_df,
            use_container_width=True
        )

    elif (
        "بحث" in st.session_state
        or len(result_df)==0
    ):
        pass

# =====================================
# أرشيف القضايا
# =====================================

if st.session_state.page == "archive":

    st.markdown("""
    <h2 style='text-align:center'>
    📂 أرشيف القضايا
    </h2>
    """, unsafe_allow_html=True)

    active_cases = pd.read_sql_query(
        "SELECT * FROM cases",
        conn
    )

    if not active_cases.empty:

        st.subheader(
            "القضايا المتاحة للأرشفة"
        )

        for _, row in active_cases.iterrows():

            with st.expander(

                f"{row['case_no']} / {row['judicial_year']}"

            ):

                st.write(
                    row["subject"]
                )

                st.write(
                    row["claimant"]
                )

                st.write(
                    row["defendant"]
                )

                if st.button(

                    f"📦 أرشفة القضية {row['id']}",

                    key=f"archive_{row['id']}"

                ):

                    archive_case(row)

                    st.success(
                        "تمت الأرشفة بنجاح"
                    )

                    st.rerun()

    st.markdown("---")

    st.subheader(
        "القضايا المؤرشفة"
    )

    archive_df = pd.read_sql_query(

        """

        SELECT *

        FROM archive_cases

        ORDER BY id DESC

        """,

        conn

    )

    if not archive_df.empty:

        st.dataframe(
            archive_df,
            use_container_width=True
        )

    else:

        st.info(
            "لا توجد قضايا مؤرشفة"
        )
# =====================================
# التقارير
# =====================================

if st.session_state.page == "reports":

    st.markdown("""
    <h2 style='text-align:center'>
    📊 التقارير
    </h2>
    """, unsafe_allow_html=True)

    report_type = st.selectbox(

        "اختر التقرير",

        [

            "تقرير الدعاوى المتداولة",

            "تقرير الأحكام الصادرة"

        ]

    )

    # =================================
    # تقرير الدعاوى المتداولة
    # =================================

    if report_type == "تقرير الدعاوى المتداولة":

        from_date = st.date_input(
            "من تاريخ",
            key="from_cases"
        )

        to_date = st.date_input(
            "إلى تاريخ",
            key="to_cases"
        )

        officer_name = st.text_input(
            "طرف الأستاذ /"
        )

        if st.button("عرض التقرير"):

            report_df = pd.read_sql_query(
                "SELECT * FROM cases",
                conn
            )

            if not report_df.empty:

                report_df = report_df[
                    (
                        pd.to_datetime(
                            report_df["session_date"]
                        )
                        >= pd.to_datetime(from_date)
                    )
                    &
                    (
                        pd.to_datetime(
                            report_df["session_date"]
                        )
                        <= pd.to_datetime(to_date)
                    )
                ]

                st.markdown(f"""

                ### الهيئة القومية للتأمين الاجتماعى

                ### الإدارة القانونية منطقة البحيرة

                **بيان بالدعاوى المتداولة**

                خلال الفترة من
                {from_date}

                حتى
                {to_date}

                طرف الأستاذ /
                {officer_name}

                """)
