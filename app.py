import streamlit as st
import sqlite3
from io import BytesIO
from docx import Document
from datetime import datetime

# =========================
# Session State (لازم أول البرنامج)
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "cases"

if "full_name" not in st.session_state:
    st.session_state.full_name = "مستخدم"
    # =========================
# Database Connection
# =========================

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# =========================
# إنشاء جدول القضايا (مهم جدًا)
# =========================

cur.execute("""
CREATE TABLE IF NOT EXISTS cases (
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
    roll_no TEXT,
    session_date TEXT,
    reason TEXT,
    notes TEXT,
    judgment_result TEXT,
    notifications_enabled INTEGER,
    whatsapp_number TEXT,
    status TEXT,
    owner_user TEXT,
    created_at TEXT
)
""")

conn.commit()

# =========================
# Database
# =========================

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()
# =========================
# Session State (لازم أول البرنامج)
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "cases"

if "full_name" not in st.session_state:
    st.session_state.full_name = "مستخدم"
# =========================
# Database
# =========================

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# =========================
# Word Report
# =========================

def create_word(rows, user_name):

    doc = Document()

    doc.add_heading("التقرير القضائي", level=1)

    doc.add_paragraph("الهيئة القومية للتأمين الاجتماعي")
    doc.add_paragraph("الإدارة العامة للشئون القانونية")
    doc.add_paragraph("ديوان عام منطقة البحيرة")
    doc.add_paragraph(f"المستخدم: {user_name}")

    doc.add_paragraph("===================================")

    table = doc.add_table(rows=1, cols=5)
    table.style = "Table Grid"

    hdr = table.rows[0].cells
    hdr[0].text = "م"
    hdr[1].text = "رقم القضية"
    hdr[2].text = "الخصوم"
    hdr[3].text = "الموضوع"
    hdr[4].text = "النتيجة"

    for i, row in enumerate(rows, start=1):

        cells = table.add_row().cells
        cells[0].text = str(i)
        cells[1].text = f"{row[6]}/{row[7]}"
        cells[2].text = f"{row[3]} ضد {row[5]}"
        cells[3].text = str(row[13] or "")
        cells[4].text = str(row[17] or "")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
    # =====================================
# 📄 PDF Report (محسن)
# =====================================

def create_pdf(rows, user_name):

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    y = 800

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "التقرير القضائي")
    y -= 30

    p.setFont("Helvetica", 10)
    p.drawString(50, y, "الهيئة القومية للتأمين الاجتماعي")
    y -= 20
    p.drawString(50, y, "الإدارة العامة للشئون القانونية")
    y -= 20
    p.drawString(50, y, f"المستخدم: {user_name}")
    y -= 30

    for i, row in enumerate(rows, start=1):

        if y < 50:
            p.showPage()
            y = 800

        p.drawString(
            50,
            y,
            f"{i} - {row[6]}/{row[7]} - {row[3]} ضد {row[5]} - {row[17]}"
        )
        y -= 20

    p.save()
    buffer.seek(0)
    return buffer
    # =========================
    # بيانات القضية
    # =========================

    litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])

    claimant_type = st.selectbox("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"])
    claimant = st.text_input("اسم الخصم الأول")

    defendant_type = st.selectbox("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"])
    defendant = st.text_input("اسم الخصم الثاني")

    case_no = st.text_input("رقم الدعوى / الاستئناف / الطعن")
    judicial_year = st.text_input("السنة القضائية")
    circuit = st.text_input("الدائرة")
    case_type = st.text_input("نوع الدعوى")

    court = st.selectbox(
        "المحكمة",
        ["ابتدائي", "استئناف", "نقض", "إدارية", "تأديبية", "قضاء إداري", "إدارية عليا"]
    )

    court_name = st.text_input("اسم المحكمة")

    appeal_office = ""
    if litigation_type == "استئناف":
        appeal_office = st.text_input("مأمورية الاستئناف")

    subject = st.text_area("موضوع الدعوى")
    session_date = st.date_input("تاريخ الجلسة")
    reason = st.text_area("السبب والإجراء المطلوب")
    notes = st.text_area("ملاحظات")

    judgment_result = st.selectbox(
        "حالة الدعوى",
        ["متداولة", "لصالح الهيئة", "ضد الهيئة"]
    )

    # =========================
    # إشعارات واتساب
    # =========================
    st.markdown("---")

    notifications_enabled = st.checkbox("تفعيل تنبيهات واتساب", value=True)

    whatsapp_number = ""
    if notifications_enabled:
        whatsapp_number = st.text_input("رقم واتساب التنبيهات")

    # =========================
    # 🟢 زر الحفظ
    # =========================
    st.markdown("---")

    if st.button("💾 حفظ القضية"):

        cur.execute("""
            INSERT INTO cases (
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
                owner_user,
                created_at
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
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
            st.session_state.full_name,
            str(datetime.now())
        ))

        conn.commit()

        st.success("تم حفظ القضية بنجاح ✔")

        st.rerun()
        # =====================================
# 📦 إعداد قاعدة البيانات (Tables)
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    full_name TEXT,
    role TEXT DEFAULT 'user',
    active INTEGER DEFAULT 1,
    created_at TEXT
)
""")

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
# 👤 إنشاء مستخدم افتراضي
# =====================================

try:
    cur.execute("""
        INSERT INTO users (
            username, password, full_name, role, active, created_at
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "waleedhammad",
        "123456",
        "وليد حماد",
        "admin",
        1,
        str(datetime.now())
    ))
    conn.commit()
except:
    pass


# =====================================
# 🧠 Session State (نظيف)
# =====================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

if "full_name" not in st.session_state:
    st.session_state.full_name = ""


# =====================================
# 🔐 تسجيل الدخول
# =====================================

if not st.session_state.logged_in:

    st.markdown("""
    <style>
    .stApp{
        background:#062456;
    }
    h1,h2,h3,h4,h5,h6,label,p,span{
        color:white !important;
    }
    .login-box{
        text-align:center;
        color:white;
        margin-top:50px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-box">
        <h1>⚖️ إدارة القضايا</h1>
        <h3>تسجيل الدخول</h3>
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input("اسم المستخدم", key="login_user")
    password = st.text_input("كلمة المرور", type="password", key="login_pass")

    if st.button("دخول", key="login_btn"):

        user = cur.execute("""
            SELECT username, password, full_name, role
            FROM users
            WHERE username=? AND active=1
        """, (username,)).fetchone()

        if user and user[1] == password:

            st.session_state.logged_in = True
            st.session_state.username = user[0]
            st.session_state.full_name = user[2]
            st.session_state.role = user[3]

            st.rerun()

        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")

    st.stop()
# =====================================
# شكل البرنامج بعد الدخول
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
# معلومات المستخدم
# =====================================

col1, col2 = st.columns([4,1])

with col1:

    st.success(
        f"المستخدم: {st.session_state.full_name}"
    )

with col2:

    if st.button("🚪 خروج"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.session_state.role = ""

        st.session_state.full_name = ""

        st.rerun()
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
# مدير البرنامج
# =====================================

if st.session_state.role == "admin":

    st.markdown("---")

    with st.expander("👑 مدير البرنامج"):

        st.subheader("➕ إنشاء مستخدم جديد")

        new_username = st.text_input(
            "اسم المستخدم الجديد"
        )

        new_password = st.text_input(
            "كلمة المرور",
            type="password",
            key="new_pass"
        )

        new_full_name = st.text_input(
            "الاسم بالكامل"
        )

        if st.button("➕ إنشاء مستخدم"):

            try:

                cur.execute("""
                    INSERT INTO users
                    (
                        username,
                        password,
                        full_name,
                        role,
                        active,
                        created_at
                    )
                    VALUES
                    (?, ?, ?, ?, ?, ?)
                """,
                (
                    new_username,
                    new_password,
                    new_full_name,
                    "user",
                    1,
                    str(datetime.now())
                ))

                conn.commit()

                st.success("تم إنشاء المستخدم")

                st.rerun()

            except:

                st.error("اسم المستخدم موجود بالفعل")

        st.markdown("---")

        st.subheader("👥 المستخدمون")

        users = cur.execute("""
            SELECT
                id,
                username,
                full_name,
                role,
                active
            FROM users
            ORDER BY full_name
        """).fetchall()

        for u in users:

            col1, col2, col3 = st.columns([6,1,1])

            with col1:

                status = "✅ مفعل" if u[4] == 1 else "❌ موقوف"

                st.write(
                    f"{u[2]} | {u[1]} | {status}"
                )

            with col2:

                if u[1] != "waleedhammad":

                    if st.button(
                        "🔑",
                        key=f"reset_{u[0]}"
                    ):

                        cur.execute("""
                            UPDATE users
                            SET password='123456'
                            WHERE id=?
                        """,
                        (u[0],))

                        conn.commit()

                        st.success(
                            f"تم إعادة كلمة المرور للمستخدم {u[1]}"
                        )

                        st.rerun()

            with col3:

                if u[1] != "waleedhammad":

                    if st.button(
                        "🗑️",
                        key=f"delete_{u[0]}"
                    ):

                        cur.execute("""
                            DELETE FROM users
                            WHERE id=?
                        """,
                        (u[0],))

                        conn.commit()

                        st.success(
                            f"تم حذف المستخدم {u[1]}"
                        )

                        st.rerun()
# =====================================
# الصفحة الحالية
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"
    # =====================================
# إعداد الحالة الافتراضية
# =====================================
if "page" not in st.session_state:
    st.session_state.page = "cases"

if "full_name" not in st.session_state:
    st.session_state.full_name = "مستخدم"

# =====================================
# القائمة الرئيسية
# =====================================
col1, col2, col3 = st.columns([1, 2, 1])

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
# صفحة تسجيل القضايا
# =====================================

if st.session_state.page == "cases":

    # ===== فاصل + عنوان الصفحة =====
    st.markdown("### ⚖️ تسجيل القضايا")
    st.markdown("---")

    st.info(f"المستخدم الحالي: {st.session_state.full_name}")

    # ===== بيانات أساسية =====
    st.markdown("##### 🧾 البيانات الأساسية")
    st.markdown("---")

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
    claimant = st.text_input("اسم الخصم الأول", key="claimant")

    defendant_type = st.selectbox(
        "صفة الخصم الثاني",
        ["المدعى عليه", "المستأنف ضده", "المطعون ضده"],
        key="defendant_type"
    )
    defendant = st.text_input("اسم الخصم الثاني", key="defendant")

    st.markdown("---")

    # ===== بيانات القضية =====
    st.markdown("##### 📌 بيانات القضية")
    st.markdown("---")

    case_no = st.text_input("رقم الدعوى / الاستئناف / الطعن", key="case_no")
    judicial_year = st.text_input("السنة القضائية", key="judicial_year")
    circuit = st.text_input("الدائرة", key="circuit")
    case_type = st.text_input("نوع الدعوى", key="case_type")

    court = st.selectbox(
        "المحكمة",
        ["ابتدائي", "استئناف", "نقض", "إدارية", "تأديبية", "قضاء إداري", "إدارية عليا"],
        key="court"
    )

    court_name = st.text_input("اسم المحكمة", key="court_name")

    if litigation_type == "استئناف":
        appeal_office = st.text_input("مأمورية الاستئناف", key="appeal_office")
    else:
        appeal_office = ""

    st.markdown("---")

    # ===== موضوع القضية =====
    st.markdown("##### 📄 تفاصيل القضية")
    st.markdown("---")

    subject = st.text_area("موضوع الدعوى", key="subject")
    roll_no = st.text_input("الرول", key="roll_no")
    session_date = st.date_input("تاريخ الجلسة", key="session_date")
    reason = st.text_area("السبب والإجراء المطلوب", key="reason")
    notes = st.text_area("ملاحظات", key="notes")

    judgment_result = st.selectbox(
        "حالة الدعوى",
        ["متداولة", "لصالح الهيئة", "ضد الهيئة"],
        key="judgment_result"
    )

    st.markdown("---")

    # ===== إشعارات =====
    st.markdown("##### 🔔 التنبيهات")
    st.markdown("---")

    notifications_enabled = st.checkbox("تفعيل تنبيهات واتساب", value=True, key="notif")

    whatsapp_number = ""
    if notifications_enabled:
        whatsapp_number = st.text_input("رقم واتساب التنبيهات", key="whatsapp")

    st.markdown("---")

    # ===== زر الحفظ =====
    st.markdown("##### 💾 الحفظ")
    st.markdown("---")

    if st.button("💾 حفظ القضية", key="save_case_btn"):

        # تحقق بسيط من رقم الواتساب
        if notifications_enabled:
            if not (
                len(whatsapp_number) == 11 and
                whatsapp_number.startswith(("010", "011", "012", "015"))
            ):
                st.error("رقم واتساب غير صحيح")
                st.stop()

        cur.execute("""
            INSERT INTO cases (
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
                roll_no,
                session_date,
                reason,
                notes,
                judgment_result,
                notifications_enabled,
                whatsapp_number,
                status,
                owner_user,
                created_at
            )
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
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
            roll_no,
            str(session_date),
            reason,
            notes,
            judgment_result,
            1 if notifications_enabled else 0,
            whatsapp_number,
            "متداولة",
            st.session_state.full_name,
            str(datetime.now())
        ))

        conn.commit()
        st.success("تم حفظ القضية بنجاح ✔")
        st.rerun()
# =====================================
# صفحات أخرى (هيكل مبدئي)
# =====================================
elif st.session_state.page == "alerts":
    st.title("🔔 التنبيهات")

elif st.session_state.page == "reports":
    st.title("📊 التقارير")

elif st.session_state.page == "archive":
    st.title("📂 الأرشيف")

elif st.session_state.page == "all_cases":
    st.title("📋 حصر عام القضايا")

elif st.session_state.page == "search":
    st.title("🔍 البحث")

elif st.session_state.page == "deleted":
    st.title("❌ القضايا المحذوفة")
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
### {row[3]} ضد الهيئة

**موضوع الدعوى:** {row[13]}

**الجلسة:** {last_session}

**الإجراء:** {last_action}

**رقم القضية:** {row[6]}/{row[7]}

**الدائرة:** {row[8]}

**المحكمة:** {row[10]}

**اسم المحكمة:** {row[11]}
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

        # زرار التعديل
        col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
        with col_btn2:
            if st.button("✏️ تعديل بيانات القضية", key=f"edit_case_{case_id}", use_container_width=True):
                st.session_state.edit_mode = not st.session_state.get("edit_mode", False)
                st.rerun()

        case_title = "رقم الدعوى"
        case_type_title = "نوع الدعوى"
        subject_title = "موضوع الدعوى"

        if case_data[1] == "استئناف":
            case_title = "رقم الاستئناف"
            case_type_title = "نوع الاستئناف"
            subject_title = "موضوع الاستئناف"

        elif case_data[1] == "نقض":
            case_title = "رقم الطعن"
            case_type_title = "نوع الطعن"
            subject_title = "موضوع الطعن"

        # وضع التعديل
        if st.session_state.get("edit_mode", False):
            st.markdown("---")
            st.subheader("✏️ تعديل بيانات القضية")

            with st.form(f"edit_form_{case_id}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    new_case_no = st.text_input(case_title, value=case_data[6])
                with col2:
                    new_year = st.text_input("السنة القضائية", value=case_data[7])
                with col3:
                    new_circle = st.text_input("الدائرة", value=case_data[8])

                col4, col5, col6 = st.columns(3)
                with col4:
                    new_case_type = st.text_input(case_type_title, value=case_data[9])
                with col5:
                    new_court = st.text_input("المحكمة", value=case_data[10])
                with col6:
                    new_court_name = st.text_input("اسم المحكمة", value=case_data[11])

                new_subject = st.text_area(subject_title, value=case_data[13], height=100)

                col_save, col_cancel = st.columns(2)
                with col_save:
                    save_btn = st.form_submit_button("💾 حفظ التعديلات", use_container_width=True, type="primary")
                with col_cancel:
                    cancel_btn = st.form_submit_button("❌ إلغاء", use_container_width=True)

                if save_btn:
                    cur.execute("""
                        UPDATE cases SET
                        case_no=?, year=?, circle=?, case_type=?,
                        court=?, court_name=?, subject=?
                        WHERE id=?
                    """, (new_case_no, new_year, new_circle, new_case_type,
                          new_court, new_court_name, new_subject, case_id))
                    conn.commit()
                    st.success("تم حفظ التعديلات بنجاح ✅")
                    st.session_state.edit_mode = False
                    st.rerun()

                if cancel_btn:
                    st.session_state.edit_mode = False
                    st.rerun()

            st.markdown("---")

        st.markdown(f"""
<div dir="rtl" style="display:flex;gap:8px;margin-bottom:8px;">

<div style="flex:1;border:2px solid #0b3b91;background:white;color:black;padding:10px;text-align:center;border-radius:8px;">
<b>{case_title}</b><br>
{case_data[6]}
</div>

<div style="flex:1;border:2px solid #0b3b91;background:white;color:black;padding:10px;text-align:center;border-radius:8px;">
<b>السنة القضائية</b><br>
{case_data[7]}
</div>

<div style="flex:1;border:2px solid #0b3b91;background:white;color:black;padding:10px;text-align:center;border-radius:8px;">
<b>الدائرة</b><br>
{case_data[8]}
</div>

</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div dir="rtl" style="display:flex;gap:8px;margin-bottom:8px;">

<div style="flex:1;border:2px solid #0b3b91;background:white;color:black;padding:10px;text-align:center;border-radius:8px;">
<b>{case_type_title}</b><br>
{case_data[9]}
</div>

<div style="flex:1;border:2px solid #0b3b91;background:white;color:black;padding:10px;text-align:center;border-radius:8px;">
<b>المحكمة</b><br>
{case_data[10]}
</div>

<div style="flex:1;border:2px solid #0b3b91;background:white;color:black;padding:10px;text-align:center;border-radius:8px;">
<b>اسم المحكمة</b><br>
{case_data[11]}
</div>

</div>
""", unsafe_allow_html=True)

        if case_data[1] == "استئناف":

            st.markdown(f"""
<div dir="rtl" style="border:2px solid #0b3b91;background:white;color:black;padding:10px;margin-bottom:8px;text-align:center;border-radius:8px;">
<b>مأمورية استئناف</b><br>
{case_data[12] if case_data[12] else "ــــــ"}
</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div dir="rtl" style="display:flex;gap:8px;margin-bottom:8px;">

<div style="flex:1;border:2px solid #198754;background:#f8fff8;color:black;padding:15px;text-align:center;border-radius:8px;">
<div style="color:#198754;font-weight:bold;font-size:18px;">
{case_data[2]}
</div>
<hr>
<div style="color:#c00000;font-size:20px;font-weight:bold;">
{case_data[3]}
</div>
</div>

<div style="flex:1;border:2px solid #198754;background:#f8fff8;color:black;padding:15px;text-align:center;border-radius:8px;">
<div style="color:#198754;font-weight:bold;font-size:18px;">
{case_data[4]}
</div>
<hr>
<div color="#c00000;font-size:20px;font-weight:bold;">
{case_data[5]}
</div>
</div>

</div>
""", unsafe_allow_html=True)

        st.markdown(f"""
<div dir="rtl" style="border:2px solid #0b3b91;background:white;color:black;padding:15px;margin-bottom:8px;border-radius:8px;">

<div style="text-align:center;font-size:22px;font-weight:bold;color:#0b3b91;">
{subject_title}
</div>

<hr>

<div style="
text-align:center;
font-size:24px;
font-weight:bold;
color:#c00000;
padding:10px;
">
{case_data[13]}
</div>

</div>
""", unsafe_allow_html=True)
        st.markdown("---")

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

            st.markdown("""
<div dir="rtl" style="display:flex;gap:6px;margin-bottom:8px;">

<div style="flex:1;border:2px solid #0b3b91;background:#e8f0ff;color:#0b3b91;padding:8px;font-size:14px;text-align:center;border-radius:8px;font-weight:bold;">
الرول
</div>

<div style="flex:1;border:2px solid #0b3b91;background:#e8f0ff;color:#0b3b91;padding:8px;font-size:14px;text-align:center;border-radius:8px;font-weight:bold;">
تاريخ الجلسة
</div>

<div style="flex:2;border:2px solid #0b3b91;background:#e8f0ff;color:#0b3b91;padding:8px;font-size:14px;text-align:center;border-radius:8px;font-weight:bold;">
الإجراءات
</div>

<div style="flex:2;border:2px solid #0b3b91;background:#e8f0ff;color:#0b3b91;padding:8px;font-size:14px;text-align:center;border-radius:8px;font-weight:bold;">
الملاحظات
</div>

</div>
""", unsafe_allow_html=True)

            for item in updates:

                session_date = "—"

                if item[1]:
                    session_date = (
                        str(item[1])[:10].split("-")[2]
                        + "/"
                        + str(item[1])[:10].split("-")[1]
                        + "/"
                        + str(item[1])[:10].split("-")[0]
                    )

                st.markdown(f"""
<div dir="rtl" style="display:flex;gap:6px;margin-bottom:6px;">

<div style="flex:1;border:1px solid #0b3b91;background:white;color:black;padding:8px;font-size:14px;text-align:center;border-radius:8px;">
{item[0] if item[0] else "—"}
</div>

<div style="flex:1;border:1px solid #0b3b91;background:white;color:black;padding:8px;font-size:14px;text-align:center;border-radius:8px;">
{session_date}
</div>

<div style="flex:2;border:1px solid #0b3b91;background:white;color:black;padding:8px;font-size:14px;text-align:center;border-radius:8px;">
{item[2] if item[2] else "—"}
</div>

<div style="flex:2;border:1px solid #0b3b91;background:white;color:black;padding:8px;font-size:14px;text-align:center;border-radius:8px;">
{item[3] if item[3] else "—"}
</div>

</div>
""", unsafe_allow_html=True)

        else:

            st.info("لا توجد جلسات مسجلة")

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

        reserved_judgment_date = st.date_input(
            "جلسة الحكم"
        )

        judgment_text = st.text_area(
            "منطوق الحكم"
        )

        judgment_result = st.selectbox(
            "نتيجة الجلسة",
            [
                "",
                "لصالح الهيئة",
                "ضد الهيئة",
                "إعادة للمرافعة",
                "إحالة خبير",
                "إحالة طب شرعي",
                "تحقيق",
                "استجواب",
                "مد أجل للحكم",
                "وقف",
                "أخرى"
            ]
        )

        judgment_action = st.text_input(
            "الإجراء بعد الحكم"
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
                    status_reason,
                    reserved_judgment_date,
                    judgment_text,
                    judgment_result,
                    judgment_action
                )
                VALUES
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                case_id,
                new_roll,
                str(datetime.now()),
                adjournment_reason,
                str(next_session_date),
                status_reason,
                str(reserved_judgment_date),
                judgment_text,
                judgment_result,
                judgment_action
            ))

            # فقط الأحكام النهائية
            if judgment_result in [
                "لصالح الهيئة",
                "ضد الهيئة"
            ]:

                cur.execute("""
                    UPDATE cases
                    SET
                        status='محكوم فيها',
                        judgment_result=?
                    WHERE id=?
                """,
                (
                    judgment_result,
                    case_id
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
                # =====================================
# 📊 التقارير والإحصائيات
# =====================================

if st.session_state.page == "reports":

    import pandas as pd

    st.header("📊 التقارير والإحصائيات")

    # =========================
    # 🧪 بيانات تجريبية
    # =========================
    if st.button("🧪 إضافة بيانات تجريبية"):

        demo_cases = [
            (1, None, None, "محمد أحمد", None, "علي حسن", 2024, 2024, "دائرة 1", "مدني", "محكمة طنطا", "طنطا", None, "تعويض", None, None, None, "لصالح الهيئة", None, None, "متداولة"),
            (2, None, None, "سعيد علي", None, "أحمد محمود", 2025, 2025, "دائرة 2", "عمالي", "محكمة دمنهور", "دمنهور", None, "مستحقات", None, None, None, "ضد الهيئة", None, None, "حكم")
        ]

        for c in demo_cases:
            cur.execute("""
                INSERT INTO cases
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, c)

        conn.commit()
        st.success("تم إضافة بيانات تجريبية ✔")

    # =========================
    # الفلاتر
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        from_date = st.date_input("من تاريخ")

    with col2:
        to_date = st.date_input("حتى تاريخ")

    area_name = st.text_input("منطقة", value="البحيرة")
    lawyer_name = st.text_input("طرف الأستاذ /", value="")

    # =========================
    # جلب البيانات
    # =========================
    rows = cur.execute("""
        SELECT *
        FROM cases
        ORDER BY id DESC
    """).fetchall()

    # =========================
    # الإحصائيات
    # =========================
    total_active = 0
    total_reserved = 0
    total_judgments = 0
    total_win = 0
    total_lose = 0

    for row in rows:

        status = str(row[20])

        if status == "متداولة":
            total_active += 1

        if "حكم" in status:
            total_reserved += 1

        if row[17] == "لصالح الهيئة":
            total_judgments += 1
            total_win += 1

        if row[17] == "ضد الهيئة":
            total_judgments += 1
            total_lose += 1

    st.markdown("## 📈 الإحصائيات")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("المتداولة", total_active)
    c2.metric("محجوزة للحكم", total_reserved)
    c3.metric("الأحكام الصادرة", total_judgments)
    c4.metric("لصالح الهيئة", total_win)
    c5.metric("ضد الهيئة", total_lose)

    st.markdown("---")

    # =========================
    # نوع التقرير
    # =========================
    report_type = st.selectbox(
        "نوع التقرير",
        [
            "بيان بالدعاوى المتداولة",
            "بيان بالأحكام الصادرة",
            "بيان بالأحكام الصادرة لصالح الهيئة",
            "بيان بالأحكام الصادرة ضد الهيئة"
        ]
    )

    st.markdown(f"""
### الهيئة القومية للتأمين الاجتماعي  
### الإدارة العامة للشئون القانونية  
### ديوان عام منطقة {area_name}  

#### {report_type}  

من {from_date} إلى {to_date}  
طرف الأستاذ / {lawyer_name}
""")

    # =========================
    # تجهيز البيانات
    # =========================
    report_rows = []

    for row in rows:

        if report_type == "بيان بالدعاوى المتداولة":
            if row[17] in ["لصالح الهيئة", "ضد الهيئة"]:
                continue

        elif report_type == "بيان بالأحكام الصادرة":
            if row[17] not in ["لصالح الهيئة", "ضد الهيئة"]:
                continue

        elif report_type == "بيان بالأحكام الصادرة لصالح الهيئة":
            if row[17] != "لصالح الهيئة":
                continue

        elif report_type == "بيان بالأحكام الصادرة ضد الهيئة":
            if row[17] != "ضد الهيئة":
                continue

        updates = cur.execute("""
            SELECT next_session_date, status_reason
            FROM case_updates
            WHERE case_id=?
            ORDER BY id DESC
            LIMIT 1
        """, (row[0],)).fetchone()

        last_session = ""
        last_action = ""

        if updates:
            last_session = updates[0]
            last_action = updates[1]

        report_rows.append({
            "م": len(report_rows) + 1,
            "رقم القضية": row[6],
            "السنة": row[7],
            "الدائرة": row[8],
            "النوع": row[9],
            "المحكمة": row[10],
            "الخصوم": f"{row[3]} ضد {row[5]}",
            "الموضوع": row[13],
            "آخر جلسة": last_session,
            "آخر إجراء": last_action,
            "النتيجة": row[17]
        })

    # =========================
    # عرض الجدول
    # =========================
    if report_rows:

        df = pd.DataFrame(report_rows)
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("لا توجد بيانات خلال الفترة المحددة")

    st.markdown("---")

    st.markdown("""
### وتفضلوا بقبول وافر الاحترام  

عضو الإدارة القانونية  
مدير الإدارة القانونية  
مدير عام الإدارات القانونية  
""")

    # =========================
    # Word + PDF
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📝 تحميل Word",
            data=create_word(rows, st.session_state.full_name),
            file_name="التقرير.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    with col2:
        st.download_button(
            "📄 تحميل PDF",
            data=create_pdf(rows, st.session_state.full_name),
            file_name="التقرير.pdf",
            mime="application/pdf"
            )
