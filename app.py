import streamlit as st
import sqlite3
from io import BytesIO
from docx import Document
from datetime import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# =========================
# Session State
# =========================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "page" not in st.session_state:
    st.session_state.page = "cases"

if "full_name" not in st.session_state:
    st.session_state.full_name = "مستخدم"

if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

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
# Tables
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

cur.execute("""
CREATE TABLE IF NOT EXISTS case_updates (
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
CREATE TABLE IF NOT EXISTS case_documents (
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
CREATE TABLE IF NOT EXISTS deleted_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_case_id INTEGER,
    delete_reason TEXT,
    deleted_at TEXT
)
""")

conn.commit()

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

# =========================
# PDF
# =========================

def create_pdf(rows, user_name):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    y = 800
    p.drawString(200, y, "التقرير القضائي")

    y -= 40
    p.drawString(50, y, f"المستخدم: {user_name}")

    y -= 30

    for i, row in enumerate(rows, start=1):
        if y < 50:
            p.showPage()
            y = 800

        p.drawString(50, y, f"{i}- {row[6]}/{row[7]} - {row[3]} ضد {row[5]}")
        y -= 20

    p.save()
    buffer.seek(0)
    return buffer

# =========================
# PAGE DEFAULT FIX
# =========================

if st.session_state.page is None:
    st.session_state.page = "cases"

# =========================
# LOGIN (مختصر بدون تغيير كبير)
# =========================

if not st.session_state.logged_in:
    st.title("تسجيل الدخول")

    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):
        user = cur.execute("""
            SELECT username, password, full_name
            FROM users
            WHERE username=?
        """, (u,)).fetchone()

        if user and user[1] == p:
            st.session_state.logged_in = True
            st.session_state.full_name = user[2]
            st.rerun()
        else:
            st.error("خطأ في البيانات")

    st.stop()

# =========================
# PAGE: CASES (الحفظ مصحح)
# =========================

if st.session_state.page == "cases":

    st.title("⚖️ تسجيل القضايا")

    litigation_type = st.selectbox("نوع الإجراء", ["دعوى", "استئناف", "نقض"])
    claimant = st.text_input("المدعي")
    defendant = st.text_input("المدعى عليه")
    case_no = st.text_input("رقم القضية")
    year = st.text_input("السنة")
    subject = st.text_area("الموضوع")

    if st.button("حفظ القضية"):
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
            "",
            claimant,
            "",
            defendant,
            case_no,
            year,
            "",
            "",
            "",
            "",
            "",
            subject,
            "",
            str(datetime.now()),
            "",
            "",
            "",
            0,
            "",
            "متداولة",
            st.session_state.full_name,
            str(datetime.now())
        ))

        conn.commit()
        st.success("تم الحفظ")
        st.rerun()
