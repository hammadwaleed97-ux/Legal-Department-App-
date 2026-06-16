import streamlit as st
import sqlite3
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="إدارة القضايا", page_icon="⚖️", layout="wide")

# الاتصال بقاعدة البيانات
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# إنشاء الجداول
cur.execute("CREATE TABLE IF NOT EXISTS cases(id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT, defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT, case_type TEXT, court TEXT, court_name TEXT, appeal_office TEXT, subject TEXT, session_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, notifications_enabled INTEGER DEFAULT 0, whatsapp_number TEXT, status TEXT DEFAULT 'متداولة', owner_user TEXT, created_at TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, full_name TEXT, role TEXT DEFAULT 'user', active INTEGER DEFAULT 1, created_at TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS case_updates(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, roll_no TEXT, update_date TEXT, adjournment_reason TEXT, next_session_date TEXT, status_reason TEXT, reserved_judgment_date TEXT, judgment_text TEXT, judgment_result TEXT, judgment_action TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS case_documents(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, document_name TEXT, document_type TEXT, document_date TEXT, document_notes TEXT, uploaded_at TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS deleted_cases(id INTEGER PRIMARY KEY AUTOINCREMENT, original_case_id INTEGER, delete_reason TEXT, deleted_at TEXT)")
conn.commit()

# دالة التذييل الموحدة
def show_footer():
    st.markdown("<hr><div style='text-align:center;'>مع تحيات وليد حماد الادارة العامة للشئون القانونية ديوان عام منطقة البحيرة</div>", unsafe_allow_html=True)

# تسجيل المستخدم الافتراضي
try:
    cur.execute("INSERT INTO users (username, password, full_name, role, active, created_at) VALUES (?, ?, ?, ?, ?, ?)", ("waleedhammad", "123456", "وليد شعبان حماد", "admin", 1, str(datetime.now())))
    conn.commit()
except: pass

# التصميم الموحد (CSS)
st.markdown("""<style>.stApp{ background:#062456; } h1,h2,h3,h4,h5,h6,label,p,span{ color:white !important; } .logo-box{ text-align:center; color:white; } .logo-icon{ font-size:60px; } .logo-main{ font-size:28px; font-weight:bold; } .logo-sub{ font-size:24px; font-weight:bold; } .logo-place{ font-size:22px; font-weight:bold; } .logo-name{ color:#FFD700; font-size:30px; font-weight:bold; } div.stButton > button{ width:340px; height:65px; border-radius:15px; border:none; background:#2f55d4; color:white; font-size:20px; font-weight:bold; display:block; margin:auto; }</style>""", unsafe_allow_html=True)

# منطق الدخول
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if not st.session_state.logged_in:
    st.markdown("<div class='logo-box'><h1>⚖️ إدارة القضايا</h1><h3>تسجيل الدخول</h3></div>", unsafe_allow_html=True)
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        user = cur.execute("SELECT username, full_name, role FROM users WHERE username=? AND password=? AND active=1", (username, password)).fetchone()
        if user:
            st.session_state.update({"logged_in": True, "username": user[0], "full_name": user[1], "role": user[2]})
            st.rerun()
        else: st.error("بيانات الدخول غير صحيحة")
    show_footer()
    st.stop()

# الهيدر الموحد
col1, col2 = st.columns([4,1])
with col1: st.success(f"المستخدم: {st.session_state.full_name}")
with col2: 
    if st.button("🚪 خروج"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

st.markdown("""<div class="logo-box"><div class="logo-icon">⚖️</div><div class="logo-main">الهيئة القومية للتأمين الاجتماعي</div><div class="logo-sub">الإدارة العامة للشئون القانونية</div><div class="logo-place">ديوان عام منطقة البحيرة</div><br><div>مع تحيات</div><div class="logo-name">وليد شعبان حماد</div></div>""", unsafe_allow_html=True)
# =====================================
# القائمة الرئيسية (Navigation)
# =====================================
if "page" not in st.session_state: st.session_state.page = "home"

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
    if st.button("🔔 التنبيهات"): st.session_state.page = "alerts"
    if st.button("📊 التقارير"): st.session_state.page = "reports"
    if st.button("📂 أرشيف القضايا"): st.session_state.page = "archive"
    if st.button("📋 حصر عام القضايا"): st.session_state.page = "all_cases"
    if st.button("🔍 البحث"): st.session_state.page = "search"
    if st.button("❌ القضايا المحذوفة"): st.session_state.page = "deleted"

# =====================================
# تسجيل القضايا
# =====================================
if st.session_state.page == "cases":
    st.markdown("<h2 style='text-align:center;'>⚖️ تسجيل القضايا</h2>", unsafe_allow_html=True)
    litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])
    claimant = st.text_input("اسم الخصم الأول")
    defendant = st.text_input("اسم الخصم الثاني")
    case_no = st.text_input("رقم القضية")
    judicial_year = st.text_input("السنة القضائية")
    subject = st.text_area("موضوع الدعوى")
    session_date = st.date_input("تاريخ الجلسة")
    judgment_result = st.selectbox("حالة الدعوى", ["متداولة", "لصالح الهيئة", "ضد الهيئة"])

    if st.button("💾 حفظ القضية"):
        cur.execute("INSERT INTO cases (litigation_type, claimant, defendant, case_no, judicial_year, subject, session_date, judgment_result, status, owner_user, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (litigation_type, claimant, defendant, case_no, judicial_year, subject, str(session_date), judgment_result, "متداولة" if judgment_result == "متداولة" else "محكوم فيها", st.session_state.username, str(datetime.now())))
        conn.commit()
        st.success("تم حفظ القضية")
        st.rerun()
    show_footer()

# =====================================
# إدارة المدير (Admin)
# =====================================
if st.session_state.role == "admin":
    with st.expander("👑 لوحة تحكم المدير"):
        new_username = st.text_input("اسم المستخدم الجديد")
        if st.button("➕ إنشاء مستخدم"):
            cur.execute("INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)", (new_username, "123456", "مستخدم جديد", "user"))
            conn.commit()
            st.rerun()

# =====================================
# الحصر العام (مع استبعاد المحذوفات)
# =====================================
if st.session_state.page == "all_cases":
    st.header("📋 حصر عام القضايا")
    rows = cur.execute("SELECT * FROM cases WHERE status='متداولة' AND id NOT IN (SELECT original_case_id FROM deleted_cases) ORDER BY session_date ASC").fetchall()
    for row in rows:
        st.write(f"رقم: {row[6]}/{row[7]} - {row[3]} ضد {row[5]}")
        if st.button("📂 فتح", key=f"open_{row[0]}"):
            st.session_state.update({"selected_case": row[0], "page": "update_case"})
            st.rerun()
    show_footer()
    
# =====================================
# فتح ملف القضية (تحديثات القضية)
# =====================================
if st.session_state.page == "update_case" and "selected_case" in st.session_state:
    case_id = st.session_state.selected_case
    case_data = cur.execute("SELECT * FROM cases WHERE id=?", (case_id,)).fetchone()
    
    st.header("⚖️ ملف القضية")
    st.write(f"رقم القضية: {case_data[6]}/{case_data[7]} | الموضوع: {case_data[13]}")
    
    # إضافة تحديث (جلسة)
    with st.expander("➕ إضافة تحديث/جلسة"):
        next_session = st.date_input("تاريخ الجلسة القادمة")
        judgment = st.selectbox("نتيجة الحكم", ["", "لصالح الهيئة", "ضد الهيئة"])
        action = st.text_area("الإجراء/منطوق الحكم")
        if st.button("💾 حفظ التحديث"):
            cur.execute("INSERT INTO case_updates (case_id, next_session_date, status_reason, judgment_result) VALUES (?, ?, ?, ?)", (case_id, str(next_session), action, judgment))
            if judgment in ["لصالح الهيئة", "ضد الهيئة"]:
                cur.execute("UPDATE cases SET status='محكوم فيها', judgment_result=? WHERE id=?", (judgment, case_id))
            conn.commit()
            st.rerun()

    # حذف القضية
    if st.button("🗑️ نقل إلى القضايا المحذوفة"):
        cur.execute("INSERT INTO deleted_cases (original_case_id, delete_reason) VALUES (?, ?)", (case_id, "تم الحذف من قبل المستخدم"))
        conn.commit()
        st.session_state.page = "all_cases"
        st.rerun()
    
    show_footer()

# =====================================
# التقارير والإحصائيات
# =====================================
if st.session_state.page == "reports":
    st.header("📊 التقارير")
    # استعلام القضايا مع استبعاد المحذوفة
    total = cur.execute("SELECT COUNT(*) FROM cases WHERE id NOT IN (SELECT original_case_id FROM deleted_cases)").fetchone()[0]
    st.metric("إجمالي القضايا", total)
    show_footer()

# =====================================
# البحث (البحث الذكي)
# =====================================
if st.session_state.page == "search":
    st.header("🔍 البحث")
    query = st.text_input("كلمة البحث")
    if query:
        results = cur.execute("SELECT * FROM cases WHERE (claimant LIKE ? OR defendant LIKE ? OR case_no LIKE ?) AND id NOT IN (SELECT original_case_id FROM deleted_cases)", (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
        for row in results:
            st.write(f"رقم: {row[6]} - {row[3]} ضد {row[5]}")
    show_footer()

# =====================================
# القضايا المحذوفة
# =====================================
if st.session_state.page == "deleted":
    st.header("❌ القضايا المحذوفة")
    deleted_rows = cur.execute("SELECT c.case_no, c.claimant FROM cases c JOIN deleted_cases d ON c.id = d.original_case_id").fetchall()
    for row in deleted_rows:
        st.write(f"القضية المحذوفة: {row[0]} - الخصم: {row[1]}")
    show_footer()
