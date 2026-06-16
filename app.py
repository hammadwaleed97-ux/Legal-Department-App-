import streamlit as st
import sqlite3
from datetime import datetime, date

st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

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
    owner_user TEXT,
    created_at TEXT
)
""")

try: cur.execute("ALTER TABLE cases ADD COLUMN owner_user TEXT")
except: pass

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
    status_reason TEXT,
    reserved_judgment_date TEXT,
    judgment_text TEXT,
    judgment_result TEXT,
    judgment_action TEXT
)
""")

try: cur.execute("ALTER TABLE case_updates ADD COLUMN roll_no TEXT")
except: pass

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

try:
    cur.execute("INSERT INTO users (username, password, full_name, role, active, created_at) VALUES (?,?,?,?,?,?)",
    ("waleedhammad", "123456", "وليد حماد", "admin", 1, str(datetime.now())))
    conn.commit()
except: pass

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
if "role" not in st.session_state: st.session_state.role = ""
if "full_name" not in st.session_state: st.session_state.full_name = ""
if "page" not in st.session_state: st.session_state.page = "home"
if "selected_case" not in st.session_state: st.session_state.selected_case = None

if not st.session_state.logged_in:
    st.markdown("""<style>.stApp{ background:#062456; } h1,h2,h3,h4,h5,h6, label,p,span{ color:white!important; }.login-box{ text-align:center; color:white; margin-top:50px; }</style>""", unsafe_allow_html=True)
    st.markdown('<div class="login-box"><h1>⚖️ إدارة القضايا</h1><h3>تسجيل الدخول</h3></div>', unsafe_allow_html=True)
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        user = cur.execute("SELECT username, password, full_name, role FROM users WHERE username=? AND active=1", (username,)).fetchone()
        if user and user[1] == password:
            st.session_state.logged_in = True
            st.session_state.username = user[0]
            st.session_state.full_name = user[2]
            st.session_state.role = user[3]
            st.rerun()
        else:
            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    st.stop()

st.markdown("""<style>.stApp{ background:#062456; } h1,h2,h3,h4,h5,h6, label,p,span{ color:white!important; }.stTextInput input{ color:black!important; }.stTextArea textarea{ color:black!important; }.stDateInput input{ color:black!important; }.stSelectbox div[data-baseweb="select"] > div{ color:black!important; }.logo-box{ text-align:center; color:white; }.logo-icon{ font-size:60px; }.logo-main{ font-size:28px; font-weight:bold; }.logo-sub{ font-size:24px; font-weight:bold; }.logo-place{ font-size:22px; font-weight:bold; }.logo-name{ color:#FFD700; font-size:30px; font-weight:bold; } div.stButton > button{ width:340px; height:65px; border-radius:15px; border:none; background:#2f55d4; color:white; font-size:20px; font-weight:bold; display:block; margin:auto; }</style>""", unsafe_allow_html=True)

col1, col2 = st.columns([4,1])
with col1: st.success(f"المستخدم: {st.session_state.full_name}")
with col2:
    if st.button("🚪 خروج"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.session_state.full_name = ""
        st.rerun()

st.markdown("""<div class="logo-box"><div class="logo-icon">⚖️</div><div class="logo-main">الهيئة القومية للتأمين الاجتماعي</div><div class="logo-sub">الإدارة العامة للشئون القانونية</div><div class="logo-place">ديوان عام منطقة البحيرة</div><br><div>مع تحيات</div><div class="logo-name">وليد شعبان حماد</div></div>""", unsafe_allow_html=True)

if st.session_state.role == "admin":
    st.markdown("---")
    with st.expander("👑 مدير البرنامج"):
        st.subheader("➕ إنشاء مستخدم جديد")
        new_username = st.text_input("اسم المستخدم الجديد")
        new_password = st.text_input("كلمة المرور", type="password", key="new_pass")
        new_full_name = st.text_input("الاسم بالكامل")
        if st.button("➕ إنشاء مستخدم"):
            try:
                cur.execute("INSERT INTO users (username, password, full_name, role, active, created_at) VALUES (?,?,?,?,?,?)",
                (new_username, new_password, new_full_name, "user", 1, str(datetime.now())))
                conn.commit()
                st.success("تم إنشاء المستخدم")
                st.rerun()
            except: st.error("اسم المستخدم موجود بالفعل")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
    if st.button("🔔 التنبيهات"): st.session_state.page = "alerts"
    if st.button("📊 التقارير"): st.session_state.page = "reports"
    if st.button("📂 أرشيف القضايا"): st.session_state.page = "archive"
    if st.button("📋 حصر عام القضايا"): st.session_state.page = "all_cases"
    if st.button("🔍 البحث"): st.session_state.page = "search"
    if st.button("❌ القضايا المحذوفة"): st.session_state.page = "deleted"

if st.session_state.page == "cases":
    st.markdown("<h2 style='text-align:center;color:white'>⚖️ تسجيل القضايا</h2>", unsafe_allow_html=True)
    st.info(f"المستخدم الحالي: {st.session_state.full_name}")

    litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])
    claimant_type = st.selectbox("صفة الخصم الأول", ["المدعى", "المستأنف", "الطاعن"])
    claimant = st.text_input("اسم الخصم الأول")
    defendant_type = st.selectbox("صفة الخصم الثاني", ["المدعى عليه", "المستأنف ضده", "المطعون ضده"])
    defendant = st.text_input("اسم الخصم الثاني")
    case_no = st.text_input("رقم الدعوى / الاستئناف / الطعن")
    judicial_year = st.text_input("السنة القضائية")
    circuit = st.text_input("الدائرة")
    case_type = st.text_input("نوع الدعوى")
    court = st.selectbox("المحكمة", ["ابتدائي", "استئناف", "نقض", "إدارية", "تأديبية", "قضاء إداري", "إدارية عليا"])
    court_name = st.text_input("اسم المحكمة")
    appeal_office = st.text_input("مأمورية الاستئناف") if litigation_type == "استئناف" else ""
    subject = st.text_area("موضوع الدعوى")
    roll_no = st.text_input("الرول")
    session_date = st.date_input("تاريخ الجلسة")
    reason = st.text_area("السبب والإجراء المطلوب")
    notes = st.text_area("ملاحظات")
    judgment_result = st.selectbox("حالة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"])

    st.markdown("---")
    notifications_enabled = st.checkbox("تفعيل تنبيهات واتساب", value=True)
    whatsapp_number = st.text_input("رقم واتساب التنبيهات") if notifications_enabled else ""

    if st.button("💾 حفظ القضية"):
        if notifications_enabled and (len(whatsapp_number)!= 11 or not whatsapp_number.startswith(("010", "011", "012", "015"))):
            st.error("رقم واتساب غير صحيح")
            st.stop()

        # تصليح نهائي: 22 عمود = 22 علامة استفهام
        cur.execute("""
            INSERT INTO cases (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, circuit, case_type, court, court_name, appeal_office, subject, session_date, reason, notes, judgment_result, notifications_enabled, whatsapp_number, status, owner_user, created_at)
            VALUES (?,?,?,?,?,?)
        """, (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, circuit, case_type, court, court_name, appeal_office, subject, str(session_date), reason, notes, judgment_result, 1 if notifications_enabled else 0, whatsapp_number, "متداولة", st.session_state.username, str(datetime.now())))
        conn.commit()

        new_case_id = cur.lastrowid
        cur.execute("INSERT INTO case_updates (case_id, roll_no, update_date, adjournment_reason, next_session_date, status_reason) VALUES (?,?,?,?,?,?)",
        (new_case_id, roll_no, str(datetime.now()), reason, str(session_date), reason))
        conn.commit()

        st.success("تم حفظ القضية بنجاح")
        st.rerun()

elif st.session_state.page == "search":
    st.header("🔍 البحث")
    search_text = st.text_input("ابحث برقم القضية أو الخصوم أو الموضوع")
    if search_text:
        rows = cur.execute("SELECT * FROM cases WHERE case_no LIKE? OR claimant LIKE? OR defendant LIKE? OR subject LIKE?",
        (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%", f"%{search_text}%")).fetchall()
        if not rows:
            st.warning("لا توجد نتائج")
        else:
            for row in rows:
                case_id = row[0]
                st.markdown(f"### {row[3]} ضد {row[5]}\n**{row[6]}/{row[7]}**\n-\n**{row[13]}**")
                if st.button("📂 فتح القضية", key=f"search_open_{case_id}"):
                    st.session_state.selected_case = case_id
                    st.session_state.page = "update_case"
                    st.rerun()
                st.markdown("---")

elif st.session_state.page == "update_case":
    st.button("⬅️ العودة للحصر العام", on_click=lambda: st.session_state.update({'page': 'all_cases'}))
    case_id = st.session_state.selected_case
    case_data = cur.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    if case_data:
        st.header("⚖️ ملف القضية")
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

        st.markdown(f"**{case_title}:** {case_data[6]}")
        st.markdown(f"**السنة القضائية:** {case_data[7]}")
        st.markdown(f"**الدائرة:** {case_data[8]}")
        st.markdown(f"**{case_type_title}:** {case_data[9]}")
        st.markdown(f"**المحكمة:** {case_data[10]}")
        st.markdown(f"**اسم المحكمة:** {case_data[11]}")
        if case_data[1] == "استئناف":
            st.markdown(f"**مأمورية استئناف:** {case_data[12]}")
        st.markdown(f"**{case_data[2]}:** {case_data[3]}")
        st.markdown(f"**{case_data[4]}:** {case_data[5]}")
        st.markdown(f"**{subject_title}:** {case_data[13]}")

        st.markdown("---")
        st.subheader("📅 الجلسات")
        updates = cur.execute("SELECT roll_no, next_session_date, status_reason, adjournment_reason FROM case_updates WHERE case_id=? ORDER BY next_session_date ASC", (case_id,)).fetchall()
        if updates:
            for item in updates:
                session_date = "—"
                if item[1]:
                    session_date = str(item[1])[:10].split("-")[2] + "/" + str(item[1])[:10].split("-")[1] + "/" + str(item[1])[:10].split("-")[0]
                st.markdown(f"**الرول:** {item[0] if item[0] else '—'} | **تاريخ الجلسة:** {session_date} | **الإجراءات:** {item[2] if item[2] else '—'} | **الملاحظات:** {item[3] if item[3] else '—'}")
        else:
            st.info("لا توجد جلسات مسجلة")

        st.markdown("---")
        st.subheader("➕ إضافة جلسة جديدة")
        new_roll = st.text_input("الرول")
        next_session_date = st.date_input("تاريخ الجلسة")
        status_reason = st.text_area("الإجراءات")
        adjournment_reason = st.text_area("ملاحظات الجلسة")
        judgment_result_new = st.selectbox("نتيجة الجلسة", ["", "لصالح الهيئة", "ضد الهيئة", "إعادة للمرافعة", "إحالة خبير"])

        if st.button("💾 حفظ الجلسة"):
            cur.execute("INSERT INTO case_updates (case_id, roll_no, update_date, adjournment_reason, next_session_date, status_reason, judgment_result) VALUES (?,?,?,?,?,?,?)",
            (case_id, new_roll, str(datetime.now()), adjournment_reason, str(next_session_date), status_reason, judgment_result_new))
            if judgment_result_new in ["لصالح الهيئة", "ضد الهيئة"]:
                cur.execute("UPDATE cases SET status='محكوم فيها', judgment_result=? WHERE id=?", (judgment_result_new, case_id))
            conn.commit()
            st.success("تم حفظ الجلسة")
            st.rerun()

elif st.session_state.page == "reports":
    st.button("⬅️ رجوع", on_click=lambda: st.session_state.update({'page': 'home'}))
    st.header("📊 التقارير والإحصائيات")
    col1, col2 = st.columns(2)
    with col1: from_date = st.date_input("من تاريخ", key="report_from")
    with col2: to_date = st.date_input("إلى تاريخ", key="report_to")
    st.markdown("---")
    total_cases = cur.execute("SELECT COUNT(*) FROM cases WHERE id NOT IN (SELECT original_case_id FROM deleted_cases)").fetchone()[0]
    active_cases = cur.execute("SELECT COUNT(*) FROM cases WHERE status='متداولة' AND id NOT IN (SELECT original_case_id FROM deleted_cases)").fetchone()[0]
    positive_judgments = cur.execute("SELECT COUNT(*) FROM cases WHERE judgment_result='لصالح الهيئة'").fetchone()[0]
    negative_judgments = cur.execute("SELECT COUNT(*) FROM cases WHERE judgment_result='ضد الهيئة'").fetchone()[0]
    total_judgments = positive_judgments + negative_judgments
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("إجمالي القضايا", total_cases)
    c2.metric("القضايا المتداولة", active_cases)
    c3.metric("إجمالي الأحكام الصادرة", total_judgments)
    c4.metric("الأحكام الصادرة لصالح", positive_judgments)
    c5.metric("الأحكام الصادرة ضد", negative_judgments)
    st.markdown("---")
    report_type = st.selectbox("نوع التقرير", ["جميع القضايا المتداولة", "القضايا المتداولة خلال الفترة", "جميع الأحكام الصادرة (لصالح / ضد)", "الأحكام الصادرة لصالح", "الأحكام الصادرة ضد"])
    if st.button("📄 استخراج التقرير"):
        rows = []
        if report_type == "جميع القضايا المتداولة":
            rows = cur.execute("SELECT * FROM cases WHERE status='متداولة'").fetchall()
        elif report_type == "القضايا المتداولة خلال الفترة":
            rows = cur.execute("SELECT * FROM cases WHERE status='متداولة' AND session_date BETWEEN? AND?", (str(from_date), str(to_date))).fetchall()
        elif report_type == "جميع الأحكام الصادرة (لصالح / ضد)":
            rows = cur.execute("SELECT * FROM cases WHERE judgment_result IN ('لصالح الهيئة','ضد الهيئة')").fetchall()
        elif report_type == "الأحكام الصادرة لصالح":
            rows = cur.execute("SELECT * FROM cases WHERE judgment_result='لصالح الهيئة'").fetchall()
        elif report_type == "الأحكام الصادرة ضد":
            rows = cur.execute("SELECT * FROM cases WHERE judgment_result='ضد الهيئة'").fetchall()
        if rows:
            st.markdown(f"### التقرير خلال الفترة من {from_date} حتى {to_date}")
            for row in rows:
                update = cur.execute("SELECT next_session_date, status_reason FROM case_updates WHERE case_id=? ORDER BY id DESC LIMIT 1", (row[0],)).fetchone()
                last_action = f"{update[0]} - {update[1]}" if update else f"{row[14]} - {row[15]}"
                st.markdown(f"**رقم القضية:** {row[6]}/{row[7]}\n**الخصوم:** {row[3]} ضد {row[5]}\n**المحكمة:** {row[11]}\n**الموضوع:** {row[13]}\n**آخر إجراء / منطوق الحكم:** {last_action}\n---")
        else:
            st.warning("لا توجد بيانات للفترة المحددة")

elif st.session_state.page == "archive":
    st.header("📂 أرشيف القضايا")
    rows = cur.execute("SELECT * FROM cases WHERE status <> 'متداولة' AND id NOT IN (SELECT original_case_id FROM deleted_cases) ORDER BY session_date ASC").fetchall()
    if not rows:
        st.warning("لا توجد قضايا مؤرشفة")
    else:
        for row in rows:
            with st.container(border=True):
                st.write(f"رقم {row[6]} / {row[7]}")
                st.write(f"{row[3]} ضد {row[5]}")
                st.write(f"موضوع الدعوى : {row[13]}")
                st.write(f"الحالة : {row[20]}")

elif st.session_state.page == "all_cases":
    st.header("📋 حصر عام القضايا")
    rows = cur.execute("SELECT * FROM cases WHERE status='متداولة' AND id NOT IN (SELECT original_case_id FROM deleted_cases) ORDER BY session_date ASC").fetchall()
    if not rows:
        st.warning("لا توجد قضايا متداولة")
    else:
        for row in rows:
            case_id = row[0]
            update = cur.execute("SELECT next_session_date, status_reason FROM case_updates WHERE case_id=? ORDER BY next_session_date DESC LIMIT 1", (case_id,)).fetchone()
            last_session = update[0] if update else row[14]
            last_action = update[1] if update else row[15]
            st.markdown(f"### {row[3]} ضد الهيئة\n**موضوع الدعوى:** {row[13]}\n**الجلسة:** {last_session}\n**الإجراء:** {last_action}\n**رقم القضية:** {row[6]}/{row[7]}\n**الدائرة:** {row[8]}\n**المحكمة:** {row[10]}\n**اسم المحكمة:** {row[11]}")
            if st.button("📂 فتح القضية", key=f"open_case_{case_id}"):
                st.session_state.selected_case = case_id
                st.session_state.page = "update_case"
                st.rerun()
            st.markdown("---")

elif st.session_state.page == "deleted":
    st.header("❌ القضايا المحذوفة")
    rows = cur.execute("SELECT d.id, d.original_case_id, d.delete_reason, d.deleted_at, c.case_no, c.judicial_year, c.claimant, c.defendant, c.subject FROM deleted_cases d LEFT JOIN cases c ON d.original_case_id = c.id ORDER BY d.deleted_at DESC").fetchall()
    if not rows:
        st.warning("لا توجد قضايا محذوفة")
    else:
        for row in rows:
            with st.container(border=True):
                st.write(f"رقم القضية : {row[4]} / {row[5]}")
                st.write(f"{row[6]} ضد {row[7]}")
                st.write(f"موضوع الدعوى : {row[8]}")
                st.write(f"سبب الحذف : {row[2]}")
                st.write(f"تاريخ الحذف : {row[3]}")

elif st.session_state.page == "alerts":
    st.header("🔔 التنبيهات")
    today = str(date.today())
    rows = cur.execute("SELECT * FROM case_updates WHERE next_session_date >=? ORDER BY next_session_date ASC", (today,)).fetchall()
    if not rows:
        st.info("لا توجد جلسات قادمة")
    else:
        for row in rows:
            case_data = cur.execute("SELECT * FROM cases WHERE id=?", (row[1],)).fetchone()
            if case_data:
                st.container(border=True)
                st.write(f"{case_data[3]} ضد {case_data[5]}")
                st.write(f"جلسة: {row[4]}")
                st.write(f"الإجراء: {row[5]}")
                st.markdown("---")
