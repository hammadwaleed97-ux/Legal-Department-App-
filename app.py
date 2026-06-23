import streamlit as st
import sqlite3
from io import BytesIO
from docx import Document
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import pandas as pd

# =========================
# Session State
# =========================
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "page" not in st.session_state: st.session_state.page = "cases"
if "full_name" not in st.session_state: st.session_state.full_name = "مستخدم"

# =========================
# Database
# =========================
DB_PATH = "cases.db"
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    return conn

conn = get_conn()
cur = conn.cursor()

# =========================
# إنشاء الجداول
# =========================
cur.execute("CREATE TABLE IF NOT EXISTS cases (id INTEGER PRIMARY KEY AUTOINCREMENT, litigation_type TEXT, claimant_type TEXT, claimant TEXT, defendant_type TEXT, defendant TEXT, case_no TEXT, judicial_year TEXT, circuit TEXT, case_type TEXT, court TEXT, court_name TEXT, appeal_office TEXT, subject TEXT, roll_no TEXT, session_date TEXT, reason TEXT, notes TEXT, judgment_result TEXT, notifications_enabled INTEGER, whatsapp_number TEXT, status TEXT, owner_user TEXT, created_at TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, full_name TEXT, role TEXT DEFAULT 'user', active INTEGER DEFAULT 1, created_at TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS case_updates(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, roll_no TEXT, update_date TEXT, adjournment_reason TEXT, next_session_date TEXT, status_reason TEXT, reserved_judgment_date TEXT, judgment_text TEXT, judgment_result TEXT, judgment_action TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS case_documents(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, document_name TEXT, document_type TEXT, document_date TEXT, document_notes TEXT, uploaded_at TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS notifications(id INTEGER PRIMARY KEY AUTOINCREMENT, case_id INTEGER, whatsapp_number TEXT, notification_type TEXT, sent_at TEXT, status TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS deleted_cases(id INTEGER PRIMARY KEY AUTOINCREMENT, original_case_id INTEGER, delete_reason TEXT, deleted_at TEXT)")
conn.commit()

# =========================
# إنشاء مستخدم افتراضي
# =========================
try:
    cur.execute("INSERT INTO users (username, password, full_name, role, active, created_at) VALUES (?, ?, ?, ?, ?, ?)", ("waleedhammad", "123456", "وليد حماد", "admin", 1, str(datetime.now())))
    conn.commit()
except: pass

# =========================
# دوال التقارير
# =========================
def create_word(rows, user_name):
    doc = Document()
    doc.add_heading("التقرير القضائي", level=1)
    doc.add_paragraph(f"المستخدم: {user_name}")
    table = doc.add_table(rows=1, cols=5)
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    hdr[0].text = "م"; hdr[1].text = "رقم القضية"; hdr[2].text = "الخصوم"; hdr[3].text = "الموضوع"; hdr[4].text = "النتيجة"
    for i, row in enumerate(rows, start=1):
        cells = table.add_row().cells
        cells[0].text = str(i); cells[1].text = f"{row[6]}/{row[7]}"; cells[2].text = f"{row[3]} ضد {row[5]}"; cells[3].text = str(row[13] or ""); cells[4].text = str(row[18] or "")
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def create_pdf(rows, user_name):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 800, "التقرير القضائي")
    y = 750
    for i, row in enumerate(rows, start=1):
        if y < 50: p.showPage(); y = 800
        p.drawString(50, y, f"{i} - {row[6]}/{row[7]} - {row[3]} ضد {row[5]} - {row[18]}")
        y -= 20
    p.save()
    buffer.seek(0)
    return buffer

# =========================
# تسجيل الدخول
# =========================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center;'>⚖️ إدارة القضايا</h1>", unsafe_allow_html=True)
    username = st.text_input("اسم المستخدم")
    password = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        user = cur.execute("SELECT username, password, full_name, role FROM users WHERE username=? AND active=1", (username,)).fetchone()
        if user and user[1] == password:
            st.session_state.logged_in = True
            st.session_state.full_name = user[2]
            st.session_state.role = user[3]
            st.rerun()
    st.stop()

# =========================
# القائمة الرئيسية
# =========================
if st.button("🚪 خروج"): st.session_state.logged_in = False; st.rerun()
st.markdown("<div style='text-align:center;'>⚖️ <b>الهيئة القومية للتأمين الاجتماعي - الإدارة العامة للشئون القانونية - ديوان عام منطقة البحيرة</b></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("⚖️ تسجيل القضايا"): st.session_state.page = "cases"
    if st.button("🔔 التنبيهات"): st.session_state.page = "alerts"
    if st.button("📊 التقارير"): st.session_state.page = "reports"
    if st.button("📂 أرشيف"): st.session_state.page = "archive"
    if st.button("📋 حصر عام"): st.session_state.page = "all_cases"
    if st.button("🔍 البحث"): st.session_state.page = "search"
    if st.button("❌ القضايا المحذوفة"): st.session_state.page = "deleted"

# =========================
# الصفحات
# =========================
if st.session_state.page == "cases":
    st.header("⚖️ تسجيل القضايا")
    with st.form("new_case"):
        l_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])
        c_name = st.text_input("اسم الخصم الأول")
        d_name = st.text_input("اسم الخصم الثاني")
        case_no = st.text_input("رقم الدعوى")
        j_year = st.text_input("السنة القضائية")
        subject = st.text_area("موضوع الدعوى")
        if st.form_submit_button("💾 حفظ"):
            cur.execute("INSERT INTO cases (litigation_type, claimant, defendant, case_no, judicial_year, subject, status, owner_user, created_at) VALUES (?,?,?,?,?,?,?,?,?)", (l_type, c_name, d_name, case_no, j_year, subject, "متداولة", st.session_state.full_name, str(datetime.now())))
            conn.commit(); st.rerun()

elif st.session_state.page == "all_cases":
    st.header("📋 حصر عام القضايا")
    rows = cur.execute("SELECT * FROM cases WHERE status='متداولة'").fetchall()
    for row in rows:
        st.write(f"رقم {row[6]}/{row[7]} - {row[3]} ضد {row[5]}")
        if st.button(f"فتح {row[0]}", key=row[0]): st.session_state.selected_case = row[0]; st.session_state.page = "update_case"; st.rerun()

elif st.session_state.page == "update_case":
    case_id = st.session_state.selected_case
    st.header("⚖️ ملف القضية")
    # (هنا يكتمل كود تحديث القضية وإضافة الجلسات)
    new_roll = st.text_input("الرول")
    next_session = st.date_input("تاريخ الجلسة")
    if st.button("💾 حفظ الجلسة"):
        cur.execute("INSERT INTO case_updates (case_id, roll_no, next_session_date) VALUES (?,?,?)", (case_id, new_roll, str(next_session)))
        conn.commit(); st.rerun()

elif st.session_state.page == "reports":
    st.header("📊 التقارير")
    rows = cur.execute("SELECT * FROM cases").fetchall()
    st.download_button("📝 تحميل Word", data=create_word(rows, st.session_state.full_name), file_name="التقرير.docx")
    st.download_button("📄 تحميل PDF", data=create_pdf(rows, st.session_state.full_name), file_name="التقرير.pdf")

# التوقيع
st.markdown("---")
st.write("مع تحيات وليد حماد الادارة العامة للشئون القانونية ديوان عام منطقة البحيرة")
