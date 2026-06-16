import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# =====================================
# إنشاء الجداول
# =====================================
cur.execute("""CREATE TABLE IF NOT EXISTS cases(id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT, defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT, case_type TEXT, court TEXT, court_name TEXT, appeal_office TEXT, subject TEXT, session_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, notifications_enabled INTEGER DEFAULT 0, whatsapp_number TEXT, status TEXT DEFAULT 'متداولة', owner_user TEXT, created_at TEXT)""")
cur.execute("""CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, full_name TEXT, role TEXT DEFAULT 'user', active INTEGER DEFAULT 1, created_at TEXT)""")
cur.execute("""CREATE TABLE IF NOT EXISTS case_updates(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, roll_no TEXT, update_date TEXT, adjournment_reason TEXT, next_session_date TEXT, status_reason TEXT, reserved_judgment_date TEXT, judgment_text TEXT, judgment_result TEXT, judgment_action TEXT)""")
cur.execute("""CREATE TABLE IF NOT EXISTS case_documents(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, document_name TEXT, document_type TEXT, document_date TEXT, document_notes TEXT, uploaded_at TEXT)""")
cur.execute("""CREATE TABLE IF NOT EXISTS notifications(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, whatsapp_number TEXT, notification_type TEXT, sent_at TEXT, status TEXT)""")
cur.execute("""CREATE TABLE IF NOT EXISTS deleted_cases(id INTEGER PRIMARY KEY AUTOINCREMENT, original_case_id INTEGER, delete_reason TEXT, deleted_at TEXT)""")
conn.commit()

# إضافة أعمدة لو ناقصة
for col in ["owner_user", "created_at"]:
    try: cur.execute(f"ALTER TABLE cases ADD COLUMN {col} TEXT")
    except: pass
for col in ["reserved_judgment_date", "judgment_text", "judgment_result", "judgment_action"]:
    try: cur.execute(f"ALTER TABLE case_updates ADD COLUMN {col} TEXT")
    except: pass

try:
    cur.execute("INSERT INTO users (username, password, full_name, role, active, created_at) VALUES (?,?,?,?,?,?)",
    ("waleedhammad", "123456", "وليد حماد", "admin", 1, str(datetime.now())))
    conn.commit()
except: pass

# =====================================
# Session State
# =====================================
for key, val in {"logged_in":False, "username":"", "role":"", "full_name":"", "page":"home", "selected_case":None}.items():
    if key not in st.session_state: st.session_state[key] = val

# =====================================
# تسجيل الدخول
# =====================================
if not st.session_state.logged_in:
    st.markdown("<style>.stApp{background:#062456;} h1,h2,h3,h4,h5,h6,label,p,span{color:white!important;}.login-box{text-align:center;color:white;margin-top:50px;}</style>", unsafe_allow_html=True)
    st.markdown('<div class="login-box"><h1>⚖️ إدارة القضايا</h1><h3>تسجيل الدخول</h3></div>', unsafe_allow_html=True)
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        user = cur.execute("SELECT username, password, full_name, role FROM users WHERE username=? AND active=1", (username,)).fetchone()
        if user and user[1] == password:
            st.session_state.logged_in = True
            st.session_state.username, st.session_state.full_name, st.session_state.role = user[0], user[2], user[3]
            st.rerun()
        else: st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
    st.stop()

st.markdown("""
<style>
.stApp{background:#062456;}
h1,h2,h3,h4,h5,h6,label,p,span{color:white!important;}
.stTextInput input,.stTextArea textarea,.stDateInput input{color:black!important;}
.stSelectbox div[data-baseweb="select"] > div{color:black!important;}
.logo-box{text-align:center;color:white;}
.logo-icon{font-size:60px;}
.logo-main{font-size:28px;font-weight:bold;}
.logo-sub{font-size:24px;font-weight:bold;}
.logo-place{font-size:22px;font-weight:bold;}
.logo-name{color:#FFD700;font-size:30px;font-weight:bold;}
div.stButton > button{width:340px;height:65px;border-radius:15px;border:none;background:#2f55d4;color:white;font-size:20px;font-weight:bold;display:block;margin:auto;}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([4,1])
with col1: st.success(f"المستخدم: {st.session_state.full_name}")
with col2:
    if st.button("🚪 خروج"):
        for k in ["logged_in","username","role","full_name"]: st.session_state[k] = False if k=="logged_in" else ""
        st.rerun()

st.markdown('<div class="logo-box"><div class="logo-icon">⚖️</div><div class="logo-main">الهيئة القومية للتأمين الاجتماعي</div><div class="logo-sub">الإدارة العامة للشئون القانونية</div><div class="logo-place">ديوان عام منطقة البحيرة</div><br><div>مع تحيات</div><div class="logo-name">وليد شعبان حماد</div></div>', unsafe_allow_html=True)

# مدير البرنامج
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
        st.markdown("---")
        st.subheader("👥 المستخدمون")
        users = cur.execute("SELECT id, username, full_name, role, active FROM users ORDER BY full_name").fetchall()
        for u in users:
            col1, col2, col3 = st.columns([6,1,1])
            with col1: st.write(f"{u[2]} | {u[1]} | {'✅ مفعل' if u[4] == 1 else '❌ موقوف'}")
            with col2:
                if u[1]!= "waleedhammad" and st.button("🔑", key=f"reset_{u[0]}"):
                    cur.execute("UPDATE users SET password='123456' WHERE id=?", (u[0],))
                    conn.commit()
                    st.success(f"تم إعادة كلمة المرور للمستخدم {u[1]}")
                    st.rerun()
            with col3:
                if u[1]!= "waleedhammad" and st.button("🗑️", key=f"delete_{u[0]}"):
                    cur.execute("DELETE FROM users WHERE id=?", (u[0],))
                    conn.commit()
                    st.success(f"تم حذف المستخدم {u[1]}")
                    st.rerun()

# القائمة الرئيسية
col1, col2, col3 = st.columns([1,2,1])
with col2:
    pages = [("⚖️ تسجيل القضايا","cases"),("🔔 التنبيهات","alerts"),("📊 التقارير","reports"),("📂 أرشيف القضايا","archive"),("📋 حصر عام القضايا","all_cases"),("🔍 البحث","search"),("❌ القضايا المحذوفة","deleted")]
    for label, pg in pages:
        if st.button(label): st.session_state.page = pg

# =====================================
# تسجيل القضايا
# =====================================
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
        if notifications_enabled and not (len(whatsapp_number) == 11 and whatsapp_number.startswith(("010", "011", "012", "015"))):
            st.error("رقم واتساب غير صحيح")
            st.stop()
        # 22 عمود = 22 علامة?
        cur.execute("INSERT INTO cases (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, circuit, case_type, court, court_name, appeal_office, subject, session_date, reason, notes, judgment_result, notifications_enabled, whatsapp_number, status, owner_user, created_at) VALUES (?,?,?,?,?,?)",
        (litigation_type, claimant_type, claimant, defendant_type, defendant, case_no, judicial_year, circuit, case_type, court, court_name, appeal_office, subject, str(session_date), reason, notes, judgment_result, 1 if notifications_enabled else 0, whatsapp_number, "متداولة", st.session_state.username, str(datetime.now())))
        conn.commit()
        new_case_id = cur.lastrowid
        # 10 أعمدة = 10 علامات?
        cur.execute("INSERT INTO case_updates (case_id, roll_no, update_date, adjournment_reason, next_session_date, status_reason, reserved_judgment_date, judgment_text, judgment_result, judgment_action) VALUES (?,?,?,?,?,?)",
        (new_case_id, roll_no, str(datetime.now()), reason, str(session_date), reason, "", ""))
        conn.commit()
        st.success("تم حفظ القضية بنجاح")
        st.rerun()

# =====================================
# أرشيف القضايا
# =====================================
if st.session_state.page == "archive":
    st.header("📂 أرشيف القضايا")
    rows = cur.execute("SELECT * FROM cases WHERE status <> 'متداولة' AND id NOT IN (SELECT original_case_id FROM deleted_cases) ORDER BY session_date ASC").fetchall()
    if not rows: st.warning("لا توجد قضايا مؤرشفة")
    else:
        for row in rows:
            with st.container(border=True):
                st.write(f"رقم {row[6]} / {row[7]}")
                st.write(f"{row[3]} ضد {row[5]}")
                st.write(f"موضوع الدعوى : {row[13]}")
                st.write(f"الحالة : {row[20]}")

# =====================================
# الحصر العام
# =====================================
if st.session_state.page == "all_cases":
    st.header("📋 حصر عام القضايا")
    rows = cur.execute("SELECT * FROM cases WHERE status='متداولة' AND id NOT IN (SELECT original_case_id FROM deleted_cases) ORDER BY session_date ASC").fetchall()
    if not rows: st.warning("لا توجد قضايا متداولة")
    else:
        for row in rows:
            case_id = row[0]
            last_session, last_action = row[14], row[15]
            update = cur.execute("SELECT next_session_date, status_reason FROM case_updates WHERE case_id=? ORDER BY next_session_date DESC LIMIT 1",(case_id,)).fetchone()
            if update: last_session, last_action = update[0], update[1]
            st.markdown(f"### {row[3]} ضد الهيئة\n**موضوع الدعوى:** {row[13]}\n**الجلسة:** {last_session}\n**الإجراء:** {last_action}\n**رقم القضية:** {row[6]}/{row[7]}\n**الدائرة:** {row[8]}\n**المحكمة:** {row[10]}\n**اسم المحكمة:** {row[11]}")
            if st.button("📂 فتح القضية", key=f"open_case_{case_id}"):
                st.session_state.selected_case = case_id
                st.session_state.page = "update_case"
                st.rerun()
            st.markdown("---")

# =====================================
# فتح القضية
# =====================================
if st.session_state.page == "update_case":
    case_id = st.session_state.selected_case
    case_data = cur.execute("SELECT * FROM cases WHERE id=?",(case_id,)).fetchone()
    if case_data:
        st.header("⚖️ ملف القضية")
        case_title = "رقم الدعوى" if case_data[1] == "دعوى" else "رقم الاستئناف" if case_data[1] == "استئناف" else "رقم الطعن"
        case_type_title = "نوع الدعوى" if case_data[1] == "دعوى" else "نوع الاستئناف" if case_data[1] == "استئناف" else "نوع الطعن"
        subject_title = "موضوع الدعوى" if case_data[1] == "دعوى" else "موضوع الاستئناف" if case_data[1] == "استئناف" else "موضوع الطعن"

        st.markdown(f'<div dir="rtl" style="display:flex;gap:8px;margin-bottom:8px;"><div style="flex:1;border:2px solid #0b3b91;background:white;color:black;padding:10px;text-align:center;border-radius:8px;"><b>{case_title}</b><br>{case_data[6]}</
