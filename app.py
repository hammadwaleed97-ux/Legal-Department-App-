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
# إضافة أعمدة مطلوبة إذا لم تكن موجودة
# =====================================

try:
    cur.execute("""
    ALTER TABLE cases
    ADD COLUMN first_roll TEXT
    """)
except:
    pass

try:
    cur.execute("""
    ALTER TABLE case_documents
    ADD COLUMN file_name TEXT
    """)
except:
    pass

conn.commit()

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
                    f"{row[6]} • {row[7]} • {row[8]}"
                )

                st.write(
                    f"{row[9]} • {row[10]} • {row[11]}"
                )

                st.write(
                    f"{row[3]} ضد {row[5]}"
                )

                st.write(
                    f"موضوع الدعوى : {row[13]}"
                )

# =====================================
# الحصر العام
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

            claimant_type = str(row[2])

            if claimant_type in [
                "المدعى",
                "المستأنف",
                "الطاعن"
            ]:

                card_color = "#B22222"
                text_color = "#FFFFFF"

            else:

                card_color = "#D4A017"
                text_color = "#111111"

            st.markdown(
                f"""
                <div style="
                background:{card_color};
                color:{text_color};
                padding:15px;
                border-radius:12px;
                margin-bottom:10px;
                ">

                ⚖️ ملف قضية

                <br><br>

                رقم القضية : {row[6]}

                <br>

                السنة القضائية : {row[7]}

                <br>

                الدائرة : {row[8]}

                <br>

                النوع : {row[9]}

                <br>

                المحكمة : {row[10]}

                <br>

                اسم المحكمة : {row[11]}

                <br>

                الخصوم :

                {row[3]}

                ضد

                {row[5]}

                </div>
                """,
                unsafe_allow_html=True
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

        claimant_type = str(case_data[2])

        if claimant_type in [
            "المدعى",
            "المستأنف",
            "الطاعن"
        ]:

            cover_color = "#B22222"
            font_color = "#FFFFFF"

        else:

            cover_color = "#D4A017"
            font_color = "#111111"

        st.markdown(
            f"""
            <div style="
            background:{cover_color};
            color:{font_color};
            padding:25px;
            border-radius:15px;
            border:3px solid #000;
            font-size:15px;
            line-height:2;
            ">

            <div style="text-align:center">

            ⚖️

            <h3>ملف قضية</h3>

            </div>

            رقم القضية : {case_data[6]}
            <br>

            السنة القضائية : {case_data[7]}
            <br>

            رقم الدائرة : {case_data[8]}
            <br>

            النوع : {case_data[9]}
            <br>

            المحكمة : {case_data[10]}
            <br>

            اسم المحكمة : {case_data[11]}
            <br>
            """,
            unsafe_allow_html=True
        )

        if case_data[12]:

            st.markdown(
                f"""
                المأمورية : {case_data[12]}
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <hr>

            {case_data[2]} :

            {case_data[3]}

            <br><br>

            ضــــد

            <br><br>

            {case_data[4]} :

            {case_data[5]}

            <hr>

            <b>موضوع الدعوى</b>

            <br>

            {case_data[13]}

            <hr>
            """,
            unsafe_allow_html=True
        )

        st.markdown("### الجلسات")

        session_rows = []

        session_rows.append(
            [
                case_data[21] if len(case_data) > 21 else "",
                case_data[14],
                case_data[15],
                case_data[16]
            ]
        )

        updates = cur.execute("""
            SELECT
                next_session_date,
                status_reason,
                adjournment_reason
            FROM case_updates
            WHERE case_id=?
            ORDER BY next_session_date ASC
        """,(case_id,)).fetchall()

        for item in updates:

            session_rows.append(
                [
                    "",
                    item[0],
                    item[1],
                    item[2]
                ]
            )

        st.markdown(
            """
            الرول | الجلسة | الإجراءات | الملاحظات
            """
        )

        for row_item in session_rows:

            st.write(
                f"{row_item[0]} | {row_item[1]} | {row_item[2]} | {row_item[3]}"
            )

        st.markdown("---")
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

    st.success("تم حفظ الجلسة")

    st.rerun()

# =====================================
# تعديل بيانات القضية
# =====================================

st.markdown("---")

st.subheader("✏️ تعديل بيانات القضية")

edit_subject = st.text_area(
    "موضوع الدعوى",
    value=case_data[13]
)

edit_notes = st.text_area(
    "ملاحظات القضية",
    value=case_data[16]
)

edit_status = st.selectbox(
    "الحالة",
    [
        "متداولة",
        "لصالح الهيئة",
        "ضد الهيئة"
    ],
    index=[
        "متداولة",
        "لصالح الهيئة",
        "ضد الهيئة"
    ].index(case_data[17])
)

if st.button("💾 حفظ التعديلات"):

    cur.execute("""
        UPDATE cases
        SET
        subject=?,
        notes=?,
        judgment_result=?
        WHERE id=?
    """,
    (
        edit_subject,
        edit_notes,
        edit_status,
        case_id
    ))

    conn.commit()

    st.success("تم حفظ التعديلات")

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

    for d in docs:

        with st.container(border=True):

            st.write(
                f"اسم المستند : {d[2]}"
            )

            st.write(
                f"النوع : {d[3]}"
            )

            st.write(
                f"التاريخ : {d[4]}"
            )

            st.write(
                f"البيانات : {d[5]}"
            )

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
