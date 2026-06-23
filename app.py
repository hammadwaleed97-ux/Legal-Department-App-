import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="نظام رئاسة إدارة القضايا",
    layout="wide",
    page_icon="⚖️"
)

# =========================
# تصميم رئاسي رسمي
# =========================
st.markdown("""
<style>

.stApp {
    background: #041a3a;
    color: white;
}

/* العناوين */
h1,h2,h3,h4,h5,h6,p,label,span {
    color: white !important;
}

/* صناديق البيانات */
.card {
    background: white;
    color: black;
    padding: 14px;
    border-radius: 14px;
    border-left: 6px solid #0b3b91;
    margin-bottom: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

/* أزرار */
button {
    background: #0b3b91 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: bold;
}

/* لوجو */
.header {
    text-align:center;
    padding:20px;
}

.badge {
    background:#FFD700;
    color:black;
    padding:5px 12px;
    border-radius:20px;
    font-weight:bold;
    display:inline-block;
}

</style>
""", unsafe_allow_html=True)

# =========================
# قاعدة البيانات
# =========================
conn = sqlite3.connect("presidency.db", check_same_thread=False)
cur = conn.cursor()

def init_db():

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_no TEXT,
        year TEXT,
        claimant TEXT,
        defendant TEXT,
        subject TEXT,
        status TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS sessions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        session_date TEXT,
        roll TEXT,
        action TEXT,
        notes TEXT
    )
    """)

    conn.commit()

init_db()

# =========================
# Session State
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# HEADER (رئاسة)
# =========================
st.markdown("""
<div class="header">
<h1>⚖️ جمهورية مصر العربية</h1>
<h2>رئاسة الهيئة العامة لإدارة القضايا</h2>
<h3>الإدارة المركزية للشئون القانونية</h3>
<hr>
<span class="badge">نظام إدارة القضايا الرسمي</span>
<br><br>
<h3>وليد حماد</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# MENU رئاسي
# =========================
col1,col2,col3,col4,col5 = st.columns(5)

if col1.button("📁 القضايا"):
    st.session_state.page = "cases"

if col2.button("➕ إضافة"):
    st.session_state.page = "add"

if col3.button("📅 الجلسات"):
    st.session_state.page = "sessions"

if col4.button("📊 تقارير رئاسية"):
    st.session_state.page = "reports"

if col5.button("🔍 بحث مركزي"):
    st.session_state.page = "search"

# =========================
# إضافة قضية
# =========================
if st.session_state.page == "add":

    st.subheader("➕ تسجيل قضية جديدة (إدارة مركزية)")

    case_no = st.text_input("رقم القضية")
    year = st.text_input("السنة القضائية")
    claimant = st.text_input("المدعي")
    defendant = st.text_input("المدعى عليه")
    subject = st.text_area("موضوع الدعوى")

    if st.button("💾 اعتماد القضية"):

        cur.execute("""
        INSERT INTO cases(case_no,year,claimant,defendant,subject,status,created_at)
        VALUES(?,?,?,?,?,?,?)
        """,(case_no,year,claimant,defendant,subject,"تحت الدراسة",str(datetime.now())))

        conn.commit()
        st.success("تم الاعتماد بنجاح ✔")
        st.rerun()

# =========================
# عرض القضايا
# =========================
if st.session_state.page == "cases":

    st.subheader("📁 القضايا المسجلة")

    rows = cur.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()

    for r in rows:

        st.markdown(f"""
        <div class="card">
        <b>رقم القضية:</b> {r[1]} / {r[2]}<br>
        <b>الأطراف:</b> {r[3]} ضد {r[4]}<br>
        <b>الموضوع:</b> {r[5]}<br>
        <b>الحالة:</b> {r[6]}
        </div>
        """, unsafe_allow_html=True)

# =========================
# الجلسات
# =========================
if st.session_state.page == "sessions":

    st.subheader("📅 إدارة الجلسات")

    case_id = st.number_input("رقم القضية", min_value=1)

    session_date = st.date_input("تاريخ الجلسة")
    roll = st.text_input("رقم الرول")
    action = st.text_area("الإجراء")
    notes = st.text_area("ملاحظات")

    if st.button("💾 تسجيل الجلسة"):

        cur.execute("""
        INSERT INTO sessions(case_id,session_date,roll,action,notes)
        VALUES(?,?,?,?,?)
        """,(case_id,str(session_date),roll,action,notes))

        conn.commit()
        st.success("تم تسجيل الجلسة ✔")

# =========================
# البحث
# =========================
if st.session_state.page == "search":

    st.subheader("🔍 بحث مركزي")

    q = st.text_input("بحث شامل")

    if q:

        rows = cur.execute("""
        SELECT * FROM cases
        WHERE case_no LIKE ? OR claimant LIKE ? OR defendant LIKE ?
        """,(f"%{q}%",f"%{q}%",f"%{q}%")).fetchall()

        for r in rows:
            st.write(f"⚖️ {r[1]} - {r[3]} ضد {r[4]}")

# =========================
# التقارير الرئاسية
# =========================
if st.session_state.page == "reports":

    st.subheader("📊 التقارير الرئاسية")

    rows = cur.execute("SELECT * FROM cases").fetchall()

    df = pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True)

    # Word
    doc = Document()
    doc.add_heading("تقرير رئاسي لإدارة القضايا",0)

    for i,r in enumerate(rows,1):
        doc.add_paragraph(f"{i} - {r[1]} / {r[2]} - {r[3]} ضد {r[4]}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button("📄 اعتماد Word",buffer,"presidency_report.docx")

    # PDF
    pdf = BytesIO()
    p = canvas.Canvas(pdf,pagesize=A4)

    y=800
    p.setFont("Helvetica-Bold",14)
    p.drawString(200,y,"تقرير رئاسي للقضايا")

    y-=40

    for i,r in enumerate(rows,1):
        p.drawString(50,y,f"{i} - {r[1]} / {r[2]} - {r[3]} ضد {r[4]}")
        y-=20

    p.save()
    pdf.seek(0)

    st.download_button("📊 اعتماد PDF",pdf,"presidency_report.pdf")
