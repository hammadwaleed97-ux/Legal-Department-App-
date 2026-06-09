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
# الحصر العام للقضايا (النسخة النهائية)
# =====================================

if st.session_state.page == "all_cases":

    st.markdown("""
    <h2 style='text-align:center;color:white'>
    📋 حصر عام القضايا المتداولة
    </h2>
    """, unsafe_allow_html=True)

    # =========================
    # حذف القضايا الفارغة
    # =========================
    if st.button("🗑️ حذف القضايا الفارغة"):

        cur.execute("""
            DELETE FROM cases
            WHERE
                (claimant IS NULL OR claimant = '')
                AND
                (defendant IS NULL OR defendant = '')
        """)

        conn.commit()
        st.success("تم حذف القضايا الفارغة")
        st.rerun()

    # =========================
    # جلب البيانات (بدون pandas)
    # =========================
    cases = cur.execute("""
        SELECT *
        FROM cases
        ORDER BY session_date ASC
    """).fetchall()

    if not cases:
        st.warning("لا توجد قضايا مسجلة")

    else:

        def safe(v):
            return v if v not in (None, "", "NULL") else "-"

        for row in cases:

            case_id = row["id"]

            # آخر متابعة
            last_update = cur.execute("""
                SELECT adjournment_reason, next_session_date, status_reason
                FROM case_updates
                WHERE case_id = ?
                ORDER BY id DESC
                LIMIT 1
            """, (case_id,)).fetchone()

            last_action = "-"

            if last_update and last_update["adjournment_reason"]:
                last_action = last_update["adjournment_reason"]

            title = (
                f"{safe(row['claimant'])} ضد {safe(row['defendant'])} | "
                f"دعوى {safe(row['case_no'])} لسنة {safe(row['judicial_year'])} | "
                f"جلسة {safe(row['session_date'])} | "
                f"{last_action}"
            )

            with st.expander(title):

                st.write(f"الخصوم : {safe(row['claimant'])} ضد {safe(row['defendant'])}")
                st.write(f"رقم الدعوى : {safe(row['case_no'])}")
                st.write(f"السنة القضائية : {safe(row['judicial_year'])}")
                st.write(f"الدائرة : {safe(row['circuit'])}")
                st.write(f"نوع الإجراء : {safe(row['litigation_type'])}")
                st.write(f"نوع الدعوى : {safe(row['case_type'])}")
                st.write(f"المحكمة : {safe(row['court'])}")
                st.write(f"اسم المحكمة : {safe(row['court_name'])}")
                st.write(f"الموضوع : {safe(row['subject'])}")
                st.write(f"تاريخ الجلسة : {safe(row['session_date'])}")

                st.markdown("---")

                # =========================
                # حذف القضية
                # =========================
                delete_reason = st.text_input(
                    "سبب الحذف",
                    key=f"del_reason_{case_id}"
                )

                if st.button("❌ حذف القضية", key=f"delete_{case_id}"):

                    cur.execute("""
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
                    """, (
                        case_id,
                        row["litigation_type"],
                        row["claimant"],
                        row["defendant"],
                        row["case_no"],
                        row["judicial_year"],
                        row["subject"],
                        delete_reason,
                        str(datetime.now())
                    ))

                    cur.execute("""
                        DELETE FROM cases
                        WHERE id = ?
                    """, (case_id,))

                    conn.commit()
                    st.success("تم حذف القضية ونقلها للمحذوفات")
                    st.rerun()

                st.markdown("---")

                # =========================
                # متابعة القضية
                # =========================
                st.subheader("متابعة القضية")

                adjournment_reason = st.text_area(
                    "سبب التأجيل",
                    key=f"adj_{case_id}"
                )

                next_session_date = st.date_input(
                    "الجلسة القادمة",
                    key=f"next_{case_id}"
                )

                status_reason = st.text_area(
                    "القرار أو الإجراء الجديد",
                    key=f"status_{case_id}"
                )

                if st.button("💾 حفظ المتابعة", key=f"save_{case_id}"):

                    cur.execute("""
                        INSERT INTO case_updates
                        (
                            case_id,
                            update_date,
                            adjournment_reason,
                            next_session_date,
                            status_reason
                        )
                        VALUES (?,?,?,?,?)
                    """, (
                        case_id,
                        str(datetime.now()),
                        adjournment_reason,
                        str(next_session_date),
                        status_reason
                    ))

                    conn.commit()
                    st.success("تم حفظ المتابعة")
                    st.rerun()
