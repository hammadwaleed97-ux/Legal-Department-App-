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

    update_date TEXT,

    adjournment_reason TEXT,

    next_session_date TEXT,

    status_reason TEXT
)
""")

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

    st.info(
        "تم تجهيز شاشة التسجيل - الحفظ سيتم إضافته في الجزء التالي"
    )
# =====================================
# حفظ القضية
# =====================================

if st.button("💾 حفظ القضية"):

    if notifications_enabled:

        if not (
            len(whatsapp_number) == 11
            and whatsapp_number.startswith(
                ("010", "011", "012", "015")
            )
        ):

            st.error("رقم واتساب غير صحيح")
            st.stop()

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
            notifications_enabled,
            whatsapp_number,
            status,
            created_at
        )
        VALUES
        (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?
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
            1 if notifications_enabled else 0,
            whatsapp_number,
            "متداولة",
            str(datetime.now())
        )
    )

    conn.commit()

    st.success("تم حفظ القضية بنجاح")
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
        ORDER BY id DESC
    """).fetchall()

    if rows:

        for row in rows:

            with st.container(border=True):

                st.markdown("## 📄 ملف قضية")

                st.write(f"رقم القضية : {row[6]}")
                st.write(f"السنة القضائية : {row[7]}")
                st.write(f"الدائرة : {row[8]}")
                st.write(f"نوع الدعوى : {row[9]}")

                st.write(f"المحكمة : {row[10]}")
                st.write(f"اسم المحكمة : {row[11]}")

                if row[12]:
                    st.write(f"المأمورية : {row[12]}")

                st.write(
                    f"الخصوم : {row[3]} ضد {row[5]}"
                )

                st.write(
                    f"موضوع الدعوى : {row[13]}"
                )

                st.write(
                    f"الحالة : {row[20]}"
                )

    else:

        st.warning("لا توجد قضايا مؤرشفة")


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

            next_session = row[14]
            next_reason = row[15]

            last_update = cur.execute("""
                SELECT
                    next_session_date,
                    status_reason
                FROM case_updates
                WHERE case_id=?
                ORDER BY next_session_date DESC
                LIMIT 1
            """,(case_id,)).fetchone()

            if last_update:

                next_session = last_update[0]
                next_reason = last_update[1]

            with st.container(border=True):

                st.markdown(
                    f"""
                    **رقم القضية:** {row[6]}

                    **السنة القضائية:** {row[7]}

                    **الدائرة:** {row[8]}

                    **نوع الدعوى:** {row[9]}

                    **المحكمة:** {row[10]}

                    **اسم المحكمة:** {row[11]}
                    """
                )

                if row[12]:

                    st.write(
                        f"المأمورية : {row[12]}"
                    )

                st.write(
                    f"الخصوم : {row[3]} ضد {row[5]}"
                )

                st.write(
                    f"موضوع الدعوى : {row[13]}"
                )

                st.write(
                    f"الجلسة الحالية : {next_session}"
                )

                st.write(
                    f"سببها : {next_reason}"
                )

                if st.button(
                    "📂 فتح القضية",
                    key=f"open_case_{case_id}"
                ):

                    st.session_state.selected_case = case_id
                    st.session_state.page = "update_case"
                    st.rerun()


# =====================================
# متغير القضية المختارة
# =====================================

if "selected_case" not in st.session_state:

    st.session_state.selected_case = None
# =====================================
# جدول مستندات القضايا
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
# جدول المرفقات
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS case_documents(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    case_id INTEGER,

    document_name TEXT,

    document_type TEXT,

    document_date TEXT,

    document_notes TEXT,

    file_name TEXT,

    uploaded_at TEXT
)
""")

conn.commit()


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

        st.markdown(f"""
        <div style="
        background:#F5E6C8;
        color:black;
        border:5px solid black;
        border-radius:15px;
        padding:25px;
        ">

        <center>

        <h1>⚖️</h1>

        <h2>ملف قضية</h2>

        <h3>الهيئة القومية للتأمين الاجتماعي</h3>

        <h3>الإدارة العامة للشئون القانونية</h3>

        <h3>ديوان عام منطقة البحيرة</h3>

        </center>

        <hr>

        <b>رقم القضية :</b> {case_data[6]}<br>

        <b>السنة القضائية :</b> {case_data[7]}<br>

        <b>الدائرة :</b> {case_data[8]}<br>

        <b>نوع الدعوى :</b> {case_data[9]}<br>

        <b>المحكمة :</b> {case_data[10]}<br>

        <b>اسم المحكمة :</b> {case_data[11]}<br>

        <b>المأمورية :</b> {case_data[12] if case_data[12] else "-"}<br>

        <b>الخصوم :</b>
        {case_data[3]} ضد {case_data[5]}<br>

        <b>موضوع الدعوى :</b>
        {case_data[13]}<br>

        <b>الحالة :</b>
        {case_data[20]}

        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("⚖️ سجل الجلسات")

        with st.container(border=True):

            st.write(
                f"📅 {case_data[14]}"
            )

            st.write(
                f"سبب الجلسة : {case_data[15]}"
            )

            if case_data[16]:

                st.write(
                    f"ملاحظات : {case_data[16]}"
                )

            updates = cur.execute("""
                SELECT
                    next_session_date,
                    status_reason,
                    adjournment_reason,
                    update_date
                FROM case_updates
                WHERE case_id=?
                ORDER BY next_session_date ASC
            """,(case_id,)).fetchall()

            if updates:

                for item in updates:

                    st.markdown("---")

                    st.write(
                        f"📅 {item[0]}"
                    )

                    st.write(
                        f"سبب الجلسة : {item[1]}"
                    )

                    if item[2]:

                        st.write(
                            f"ملاحظات : {item[2]}"
                        )

                    st.caption(
                        f"تم الإضافة بتاريخ {item[3]}"
                    )
# =====================================
# مرفقات القضية
# =====================================

        st.markdown("---")

        st.subheader("📎 مرفقات القضية")

        docs = cur.execute("""
            SELECT *
            FROM case_documents
            WHERE case_id=?
            ORDER BY id DESC
        """,(case_id,)).fetchall()

        if docs:

            for doc in docs:

                with st.container(border=True):

                    st.write(
                        f"📄 {doc[2]}"
                    )

                    st.write(
                        f"النوع : {doc[3]}"
                    )

                    st.write(
                        f"التاريخ : {doc[4]}"
                    )

                    if doc[5]:

                        st.write(
                            f"البيانات : {doc[5]}"
                        )

                    if doc[6]:

                        st.write(
                            f"اسم الملف : {doc[6]}"
                        )

        else:

            st.info(
                "لا توجد مرفقات"
            )

        st.markdown("---")

        st.subheader("➕ إضافة مستند")

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
                "تقرير خبير",
                "مستند آخر"
            ]
        )

        document_date = st.date_input(
            "تاريخ المستند"
        )

        document_notes = st.text_area(
            "بيانات المستند"
        )

        uploaded_files = st.file_uploader(
            "رفع مستند أو أكثر",
            accept_multiple_files=True
        )

        if st.button(
            "💾 حفظ المستند"
        ):

            if not document_name:

                st.error(
                    "اكتب اسم المستند"
                )

            else:

                if uploaded_files:

                    for file in uploaded_files:

                        cur.execute("""
                            INSERT INTO case_documents
                            (
                                case_id,
                                document_name,
                                document_type,
                                document_date,
                                document_notes,
                                file_name,
                                uploaded_at
                            )
                            VALUES
                            (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            case_id,
                            document_name,
                            document_type,
                            str(document_date),
                            document_notes,
                            file.name,
                            str(datetime.now())
                        ))

                else:

                    cur.execute("""
                        INSERT INTO case_documents
                        (
                            case_id,
                            document_name,
                            document_type,
                            document_date,
                            document_notes,
                            file_name,
                            uploaded_at
                        )
                        VALUES
                        (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        case_id,
                        document_name,
                        document_type,
                        str(document_date),
                        document_notes,
                        "",
                        str(datetime.now())
                    ))

                conn.commit()

                st.success(
                    "تم حفظ المستند"
                )

                st.rerun()

        st.markdown("---")

        st.subheader("➕ إضافة جلسة جديدة")

        next_session_date = st.date_input(
            "تاريخ الجلسة القادمة"
        )

        status_reason = st.text_area(
            "سبب التأجيل"
        )

        adjournment_reason = st.text_area(
            "ملاحظات الجلسة"
        )

        if st.button(
            "💾 حفظ الجلسة"
        ):

            cur.execute("""
                INSERT INTO case_updates
                (
                    case_id,
                    update_date,
                    adjournment_reason,
                    next_session_date,
                    status_reason
                )
                VALUES
                (?, ?, ?, ?, ?)
            """,
            (
                case_id,
                str(datetime.now()),
                adjournment_reason,
                str(next_session_date),
                status_reason
            ))

            conn.commit()

            st.success(
                "تم حفظ الجلسة"
            )

            st.rerun()

        st.markdown("---")

        st.subheader("🗑️ حذف القضية")

        delete_reason = st.text_area(
            "سبب الحذف"
        )

        if st.button(
            "🗑️ حذف القضية"
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

        st.markdown("---")

        if st.button(
            "🔙 العودة للحصر العام"
        ):

            st.session_state.page = "all_cases"

            st.rerun()
