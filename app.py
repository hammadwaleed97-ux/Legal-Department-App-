import streamlit as st
import sqlite3
from datetime import datetime

# =====================================
# إعداد الصفحة
# =====================================

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =====================================
# الاتصال بقاعدة البيانات
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

    notifications_enabled INTEGER DEFAULT 0,

    whatsapp_number TEXT,

    status TEXT DEFAULT 'متداولة',

    created_at TEXT
)
""")
# =====================================
# جدول تحديثات القضايا
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS case_updates(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    case_id INTEGER,

    roll_no TEXT,

    update_date TEXT,

    adjournment_reason TEXT,

    next_session_date TEXT,

    status_reason TEXT
)
""")

try:
    cur.execute("""
    ALTER TABLE case_updates
    ADD COLUMN roll_no TEXT
    """)
except:
    pass

# =====================================
# جدول التنبيهات
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS notifications(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    case_id INTEGER,

    whatsapp_number TEXT,

    notification_type TEXT,

    sent_at TEXT,

    status TEXT
)
""")

# =====================================
# جدول المحذوفات
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS deleted_cases(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    original_case_id INTEGER,

    delete_reason TEXT,

    deleted_at TEXT
)
""")

conn.commit()

# =====================================
# اختبار التشغيل
# =====================================
# =====================================
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

.stTextInput input{
    color:black !important;
}

.stTextArea textarea{
    color:black !important;
}

.stDateInput input{
    color:black !important;
}

.stSelectbox div[data-baseweb="select"] > div{
    color:black !important;
}

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:60px;
}

.logo-main{
    font-size:28px;
    font-weight:bold;
}

.logo-sub{
    font-size:24px;
    font-weight:bold;
}

.logo-place{
    font-size:22px;
    font-weight:bold;
}

.logo-name{
    color:#FFD700;
    font-size:30px;
    font-weight:bold;
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
الهيئة القومية للتأمين الاجتماعي
</div>

<div class="logo-sub">
الإدارة العامة للشئون القانونية
</div>

<div class="logo-place">
ديوان عام منطقة البحيرة
</div>

<br>

<div>
مع تحيات
</div>

<div class="logo-name">
وليد شعبان حماد
</div>

</div>

""", unsafe_allow_html=True)

# =====================================
# الصفحة الحالية
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
            "ابتدائي",
            "استئناف",
            "نقض",
            "إدارية",
            "تأديبية",
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

    roll_no = st.text_input(
    "الرول"
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

    st.markdown("---")

    notifications_enabled = st.checkbox(
        "تفعيل تنبيهات واتساب",
        value=True
    )

    whatsapp_number = ""

    if notifications_enabled:

        whatsapp_number = st.text_input(
            "رقم واتساب التنبيهات"
        )
    
# =====================================
# جدول المستندات
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS case_documents(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    case_id INTEGER,

    document_name TEXT,

    document_type TEXT,

    document_date TEXT,

    document_notes TEXT,

    uploaded_at TEXT
)
""")

conn.commit()

# =====================================
# متغير القضية المختارة
# =====================================

if "selected_case" not in st.session_state:

    st.session_state.selected_case = None
# =====================================
# أرشيف القضايا
# =====================================

if st.session_state.page == "archive":

    st.header("📂 أرشيف القضايا")

    rows = cur.execute("""
        SELECT *
        FROM cases
        WHERE status <> 'متداولة'
        AND id NOT IN (
            SELECT original_case_id
            FROM deleted_cases
        )
        ORDER BY session_date ASC
    """).fetchall()

    if not rows:

        st.warning("لا توجد قضايا مؤرشفة")

    else:

        for row in rows:

            with st.container(border=True):

                st.write(
                    f"رقم {row[6]} / {row[7]}"
                )

                st.write(
                    f"{row[3]} ضد {row[5]}"
                )

                st.write(
                    f"موضوع الدعوى : {row[13]}"
                )

                st.write(
                    f"الحالة : {row[20]}"
                )
# =====================================
# الحصر العام للقضايا
# =====================================

if st.session_state.page == "all_cases":

    st.header("📋 حصر عام القضايا")

    rows = cur.execute("""
        SELECT *
        FROM cases
        WHERE status='متداولة'
        AND id NOT IN (
            SELECT original_case_id
            FROM deleted_cases
        )
        ORDER BY session_date ASC
    """).fetchall()

    if not rows:

        st.warning("لا توجد قضايا متداولة")

    else:

        for row in rows:

            case_id = row[0]

            last_session = row[14]
            last_action = row[15]

            update = cur.execute("""
                SELECT
                    next_session_date,
                    status_reason
                FROM case_updates
                WHERE case_id=?
                ORDER BY next_session_date DESC
                LIMIT 1
            """,(case_id,)).fetchone()

            if update:

                last_session = update[0]
                last_action = update[1]

            st.markdown(
                f"""
### {row[3]} ضد الهيئة - {row[13]} - جلسة {last_session} - {last_action}

**{row[6]}/{row[7]}** - **{row[8]} {row[9]} {row[11]}**
                """
            )

            if st.button(
                "📂 فتح القضية",
                key=f"open_case_{case_id}"
            ):

                st.session_state.selected_case = case_id
                st.session_state.page = "update_case"
                st.rerun()

            st.markdown("---")
# =====================================
# فتح القضية
# =====================================

if st.session_state.page == "update_case":

    case_id = st.session_state.selected_case

    case_data = cur.execute("""
        SELECT *
        FROM cases
        WHERE id=?
    """,(case_id,)).fetchone()

    if case_data:

        st.header("⚖️ ملف القضية")

        st.write(
            f"رقم القضية : {case_data[6]}"
        )

        st.write(
            f"السنة القضائية : {case_data[7]}"
        )

        st.write(
            f"الدائرة : {case_data[8]}"
        )

        st.write(
            f"النوع : {case_data[9]}"
        )

        st.write(
            f"المحكمة : {case_data[10]}"
        )

        st.write(
            f"اسم المحكمة : {case_data[11]}"
        )

        if case_data[12]:

            st.write(
                f"المأمورية : {case_data[12]}"
            )

        st.markdown("---")

        st.write(
            f"{case_data[3]} ({case_data[2]})"
        )

        st.write("ضــــد")

        st.write(
            f"{case_data[5]} ({case_data[4]})"
        )

        st.markdown("---")

        st.write(
            f"موضوع الدعوى : {case_data[13]}"
        )

        st.markdown("---")
# =====================================
# الجلسات
# =====================================

        st.subheader("📅 الجلسات")

        updates = cur.execute("""
            SELECT
                roll_no,
                next_session_date,
                status_reason,
                adjournment_reason
            FROM case_updates
            WHERE case_id=?
            ORDER BY next_session_date ASC
        """,(case_id,)).fetchall()

        if updates:

            for item in updates:

                with st.container(border=True):

                    if item[0]:

                        st.write(
                            f"الرول : {item[0]}"
                        )

                    st.write(
                        f"الجلسة : {item[1]}"
                    )

                    st.write(
                        f"الإجراءات : {item[2]}"
                    )

                    st.write(
                        f"الملاحظات : {item[3]}"
                    )

        else:

            st.info("لا توجد جلسات مضافة")
# =====================================
# إضافة جلسة جديدة
# =====================================

        st.markdown("---")

        st.subheader("➕ إضافة جلسة جديدة")

        new_roll = st.text_input(
            "الرول"
        )

        next_session_date = st.date_input(
            "تاريخ الجلسة"
        )

        status_reason = st.text_area(
            "الإجراءات"
        )

        adjournment_reason = st.text_area(
            "ملاحظات الجلسة"
        )

        if st.button(
            "💾 حفظ الجلسة الجديدة"
        ):

            cur.execute("""
                INSERT INTO case_updates
                (
                    case_id,
                    roll_no,
                    update_date,
                    adjournment_reason,
                    next_session_date,
                    status_reason
                )
                VALUES
                (?, ?, ?, ?, ?, ?)
            """,
            (
                case_id,
                new_roll,
                str(datetime.now()),
                adjournment_reason,
                str(next_session_date),
                status_reason
            ))

            conn.commit()

            st.success("تم حفظ الجلسة")

            st.rerun()
# =====================================
# مستندات القضية
# =====================================

        st.markdown("---")

        st.subheader("📎 مستندات القضية")

        document_name = st.text_input(
            "اسم المستند"
        )

        document_type = st.selectbox(
            "نوع المستند",
            [
                "صحيفة دعوى",
                "مذكرة",
                "حافظة مستندات",
                "حكم",
                "إعلان",
                "مستند آخر"
            ]
        )

        document_date = st.date_input(
            "تاريخ المستند"
        )

        document_notes = st.text_area(
            "بيانات المستند"
        )

        if st.button(
            "💾 إضافة المستند"
        ):

            cur.execute("""
                INSERT INTO case_documents
                (
                    case_id,
                    document_name,
                    document_type,
                    document_date,
                    document_notes,
                    uploaded_at
                )
                VALUES
                (?, ?, ?, ?, ?, ?)
            """,
            (
                case_id,
                document_name,
                document_type,
                str(document_date),
                document_notes,
                str(datetime.now())
            ))

            conn.commit()

            st.success("تم إضافة المستند")

            st.rerun()

        docs = cur.execute("""
            SELECT *
            FROM case_documents
            WHERE case_id=?
            ORDER BY id DESC
        """,(case_id,)).fetchall()

        if docs:

            st.markdown("### 📂 المستندات المضافة")

            for d in docs:

                col1, col2, col3 = st.columns([6,1,1])

                with col1:

                    st.write(
                        f"{d[2]} | {d[3]} | {d[4]}"
                    )

                with col2:

                    if st.button(
                        "✏️",
                        key=f"edit_doc_{d[0]}"
                    ):

                        st.session_state.edit_doc = d[0]

                with col3:

                    if st.button(
                        "🗑️",
                        key=f"delete_doc_{d[0]}"
                    ):

                        cur.execute(
                            "DELETE FROM case_documents WHERE id=?",
                            (d[0],)
                        )

                        conn.commit()

                        st.rerun()
# =====================================
# حذف القضية
# =====================================

        st.markdown("---")

        st.subheader("🗑️ حذف القضية")

        delete_reason = st.text_area(
            "سبب الحذف"
        )

        if st.button(
            "🗑️ نقل إلى القضايا المحذوفة"
        ):

            if not delete_reason.strip():

                st.error(
                    "يجب كتابة سبب الحذف"
                )

            else:

                cur.execute("""
                    INSERT INTO deleted_cases
                    (
                        original_case_id,
                        delete_reason,
                        deleted_at
                    )
                    VALUES
                    (?, ?, ?)
                """,
                (
                    case_id,
                    delete_reason,
                    str(datetime.now())
                ))

                conn.commit()

                st.success(
                    "تم نقل القضية إلى القضايا المحذوفة"
                )

                st.session_state.page = "deleted"

                st.rerun()

# =====================================
# رجوع
# =====================================

        st.markdown("---")

        if st.button(
            "🔙 العودة للحصر العام"
        ):

            st.session_state.page = "all_cases"

            st.rerun()
# =====================================
# القضايا المحذوفة
# =====================================

if st.session_state.page == "deleted":

    st.header("❌ القضايا المحذوفة")

    rows = cur.execute("""
        SELECT
            d.id,
            d.original_case_id,
            d.delete_reason,
            d.deleted_at,
            c.case_no,
            c.judicial_year,
            c.claimant,
            c.defendant,
            c.subject
        FROM deleted_cases d
        LEFT JOIN cases c
        ON d.original_case_id = c.id
        ORDER BY d.deleted_at DESC
    """).fetchall()

    if not rows:

        st.warning(
            "لا توجد قضايا محذوفة"
        )

    else:

        for row in rows:

            with st.container(border=True):

                st.write(
                    f"رقم القضية : {row[4]} / {row[5]}"
                )

                st.write(
                    f"{row[6]} ضد {row[7]}"
                )

                st.write(
                    f"موضوع الدعوى : {row[8]}"
                )

                st.write(
                    f"سبب الحذف : {row[2]}"
                )

                st.write(
                    f"تاريخ الحذف : {row[3]}"
                )
     # =====================================
# التقارير والإحصائيات
# =====================================

if st.session_state.page == "reports":

    st.header("📊 التقارير والإحصائيات")

    col1, col2 = st.columns(2)

    with col1:
        from_date = st.date_input(
            "من تاريخ",
            key="report_from"
        )

    with col2:
        to_date = st.date_input(
            "إلى تاريخ",
            key="report_to"
        )

    st.markdown("---")

    total_cases = cur.execute("""
        SELECT COUNT(*)
        FROM cases
        WHERE id NOT IN (
            SELECT original_case_id
            FROM deleted_cases
        )
    """).fetchone()[0]

    active_cases = cur.execute("""
        SELECT COUNT(*)
        FROM cases
        WHERE status='متداولة'
        AND id NOT IN (
            SELECT original_case_id
            FROM deleted_cases
        )
    """).fetchone()[0]

    positive_judgments = cur.execute("""
        SELECT COUNT(*)
        FROM cases
        WHERE judgment_result='لصالح الهيئة'
    """).fetchone()[0]

    negative_judgments = cur.execute("""
        SELECT COUNT(*)
        FROM cases
        WHERE judgment_result='ضد الهيئة'
    """).fetchone()[0]

    total_judgments = (
        positive_judgments +
        negative_judgments
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("إجمالي القضايا", total_cases)
    c2.metric("القضايا المتداولة", active_cases)
    c3.metric("إجمالي الأحكام الصادرة", total_judgments)
    c4.metric("الأحكام الصادرة لصالح", positive_judgments)
    c5.metric("الأحكام الصادرة ضد", negative_judgments)

    st.markdown("---")

    report_type = st.selectbox(
        "نوع التقرير",
        [
            "جميع القضايا المتداولة",
            "القضايا المتداولة خلال الفترة",
            "جميع الأحكام الصادرة (لصالح / ضد)",
            "الأحكام الصادرة لصالح",
            "الأحكام الصادرة ضد"
        ]
    )

    if st.button("📄 استخراج التقرير"):

        rows = []

        if report_type == "جميع القضايا المتداولة":

            rows = cur.execute("""
                SELECT *
                FROM cases
                WHERE status='متداولة'
            """).fetchall()

        elif report_type == "القضايا المتداولة خلال الفترة":

            rows = cur.execute("""
                SELECT *
                FROM cases
                WHERE status='متداولة'
                AND session_date BETWEEN ? AND ?
            """,
            (
                str(from_date),
                str(to_date)
            )).fetchall()

        elif report_type == "جميع الأحكام الصادرة (لصالح / ضد)":

            rows = cur.execute("""
                SELECT *
                FROM cases
                WHERE judgment_result IN
                ('لصالح الهيئة','ضد الهيئة')
            """).fetchall()

        elif report_type == "الأحكام الصادرة لصالح":

            rows = cur.execute("""
                SELECT *
                FROM cases
                WHERE judgment_result='لصالح الهيئة'
            """).fetchall()

        elif report_type == "الأحكام الصادرة ضد":

            rows = cur.execute("""
                SELECT *
                FROM cases
                WHERE judgment_result='ضد الهيئة'
            """).fetchall()

        if rows:

            st.markdown(
                f"### التقرير خلال الفترة من {from_date} حتى {to_date}"
            )

            for row in rows:

                update = cur.execute("""
                    SELECT
                        next_session_date,
                        status_reason
                    FROM case_updates
                    WHERE case_id=?
                    ORDER BY id DESC
                    LIMIT 1
                """,(row[0],)).fetchone()

                if update:

                    last_action = (
                        f"{update[0]} - {update[1]}"
                    )

                else:

                    last_action = (
                        f"{row[14]} - {row[15]}"
                    )

                st.markdown(
                    f"""
**رقم القضية:** {row[6]}/{row[7]}

**الخصوم:** {row[3]} ضد {row[5]}

**المحكمة:** {row[11]}

**الموضوع:** {row[13]}

**آخر إجراء / منطوق الحكم:** {last_action}

---
                    """
                )

        else:

            st.warning(
                "لا توجد بيانات للفترة المحددة"
            )           
# =====================================
# البحث
# =====================================

if st.session_state.page == "search":

    st.header("🔍 البحث")

    search_text = st.text_input(
        "ابحث برقم القضية أو الخصوم أو الموضوع"
    )

    if search_text:

        rows = cur.execute("""
            SELECT *
            FROM cases
            WHERE
            case_no LIKE ?
            OR claimant LIKE ?
            OR defendant LIKE ?
            OR subject LIKE ?
        """,
        (
            f"%{search_text}%",
            f"%{search_text}%",
            f"%{search_text}%",
            f"%{search_text}%"
        )).fetchall()

        if not rows:

            st.warning("لا توجد نتائج")

        else:

            for row in rows:

                case_id = row[0]

                st.markdown(
                    f"""
### {row[3]} ضد {row[5]}

**{row[6]}/{row[7]}**
-
**{row[13]}**
                    """
                )

                if st.button(
                    "📂 فتح القضية",
                    key=f"search_open_{case_id}"
                ):

                    st.session_state.selected_case = case_id
                    st.session_state.page = "update_case"
                    st.rerun()

                st.markdown("---")
# =====================================
# التنبيهات
# =====================================

if st.session_state.page == "alerts":

    st.header("🔔 التنبيهات")

    today = str(datetime.now().date())

    rows = cur.execute("""
        SELECT *
        FROM case_updates
        WHERE next_session_date >= ?
        ORDER BY next_session_date ASC
    """,(today,)).fetchall()

    if not rows:

        st.info("لا توجد جلسات قادمة")

    else:

        for row in rows:

            case_data = cur.execute("""
                SELECT *
                FROM cases
                WHERE id=?
            """,(row[1],)).fetchone()

            if case_data:

                st.container(border=True)

                st.write(
                    f"{case_data[3]} ضد {case_data[5]}"
                )

                st.write(
                    f"جلسة : {row[5]}"
                )

                st.write(
                    f"الإجراء : {row[6]}"
                )

                st.markdown("---")
