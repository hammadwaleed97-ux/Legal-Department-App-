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

st.title("⚖️ إدارة القضايا")

st.success("تم تشغيل الجزء الأول بنجاح")
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
        SELECT
            id,
            case_no,
            judicial_year,
            claimant,
            defendant,
            subject,
            status
        FROM cases
        ORDER BY id DESC
    """).fetchall()

    if rows:

        st.dataframe(
            rows,
            use_container_width=True
        )

    else:

        st.warning("لا توجد قضايا مسجلة")
        # =====================================
# حصر عام القضايا
# =====================================

if st.session_state.page == "all_cases":

    st.header("📋 حصر عام القضايا")

    rows = cur.execute("""
        SELECT *
        FROM cases
        WHERE status='متداولة'
        ORDER BY id DESC
    """).fetchall()

    if rows:

        for row in rows:

            case_id = row[0]

            last_update = cur.execute("""
                SELECT
                    next_session_date,
                    status_reason
                FROM case_updates
                WHERE case_id=?
                ORDER BY id DESC
                LIMIT 1
            """,(case_id,)).fetchone()

            last_session = ""
            last_reason = ""

            if last_update:
                last_session = last_update[0]
                last_reason = last_update[1]
            else:
                last_session = row[13]
                last_reason = row[14]

            st.markdown("---")

            st.write(
                f"رقم القضية: {row[6]}"
            )

            st.write(
                f"السنة القضائية: {row[7]}"
            )

            st.write(
                f"الدائرة: {row[8]}"
            )

            st.write(
                f"المحكمة: {row[10]}"
            )

            st.write(
                f"المأمورية: {row[11]}"
            )

            st.write(
                f"موضوع الدعوى: {row[12]}"
            )
st.write("تاريخ الجلسة:", row[7])
st.write("السبب والإجراء المطلوب:", row[8])
            if st.button(
                f"تحديث القضية {case_id}"
            ):
                st.session_state.selected_case = case_id
                st.session_state.page = "update_case"
                st.rerun()
        # =====================================
# تحديث قضية
# =====================================

if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

if st.session_state.page == "update_case":

    case_id = st.session_state.selected_case

    row = cur.execute("""
        SELECT
            case_no,
            judicial_year,
            subject
        FROM cases
        WHERE id = ?
    """, (case_id,)).fetchone()

    if row:

        st.header("تحديث القضية")

        st.write(f"رقم القضية: {row[0]}")
        st.write(f"السنة القضائية: {row[1]}")
        st.write(f"الموضوع: {row[2]}")

        next_session_date = st.date_input(
            "تاريخ الجلسة القادمة"
        )

        status_reason = st.text_area(
            "قرار الجلسة / سبب التأجيل"
        )

        if st.button("حفظ التحديث"):

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
                status_reason,
                str(next_session_date),
                status_reason
            ))

            conn.commit()

            if "حكم لصالح الهيئة" in status_reason:

                cur.execute("""
                    UPDATE cases
                    SET status='لصالح الهيئة'
                    WHERE id=?
                """,(case_id,))

                conn.commit()

            elif "حكم ضد الهيئة" in status_reason:

                cur.execute("""
                    UPDATE cases
                    SET status='ضد الهيئة'
                    WHERE id=?
                """,(case_id,))

                conn.commit()

            st.success("تم حفظ التحديث")
st.success("تم حفظ القضية بنجاح")
