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
    page_title="نظام مكتب قانوني",
    layout="wide",
    page_icon="⚖️"
)

# =========================
# ستايل احترافي
# =========================
st.markdown("""
<style>
.stApp {background:#062456;color:white;}
h1,h2,h3,h4,h5,h6,p,label,span{color:white!important;}

.block{
    background:white;
    color:black;
    padding:12px;
    border-radius:12px;
    margin:8px 0;
    border:2px solid #0b3b91;
}

button {
    border-radius:12px !important;
    background:#2f55d4 !important;
    color:white !important;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
conn = sqlite3.connect("legal.db", check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        full_name TEXT,
        role TEXT
    )
    """)

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
# Session
# =========================
if "logged" not in st.session_state:
    st.session_state.logged = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# =========================
# Create default admin
# =========================
try:
    cur.execute("""
    INSERT INTO users(username,password,full_name,role)
    VALUES(?,?,?,?)
    """, ("admin","1234","مدير النظام","admin"))
    conn.commit()
except:
    pass

# =========================
# LOGIN
# =========================
if st.session_state.page == "login":

    st.title("⚖️ تسجيل الدخول")

    u = st.text_input("المستخدم")
    p = st.text_input("كلمة المرور", type="password")

    if st.button("دخول"):

        user = cur.execute("""
        SELECT * FROM users WHERE username=? AND password=?
        """, (u,p)).fetchone()

        if user:
            st.session_state.logged = True
            st.session_state.page = "home"
            st.rerun()
        else:
            st.error("خطأ في البيانات")

    st.stop()

# =========================
# HEADER
# =========================
st.markdown("""
<div style="text-align:center">
<h1>⚖️ الهيئة القومية للتأمين الاجتماعي</h1>
<h3>الإدارة القانونية</h3>
<h4>نظام إدارة القضايا</h4>
<hr>
<h3 style="color:#FFD700">وليد حماد</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# MENU
# =========================
col1,col2,col3,col4,col5 = st.columns(5)

if col1.button("📌 القضايا"):
    st.session_state.page = "cases"

if col2.button("➕ إضافة"):
    st.session_state.page = "add"

if col3.button("📅 الجلسات"):
    st.session_state.page = "sessions"

if col4.button("📊 تقارير"):
    st.session_state.page = "reports"

if col5.button("🔍 بحث"):
    st.session_state.page = "search"

# =========================
# ADD CASE
# =========================
if st.session_state.page == "add":

    st.subheader("➕ إضافة قضية")

    case_no = st.text_input("رقم القضية")
    year = st.text_input("السنة")
    claimant = st.text_input("المدعي")
    defendant = st.text_input("المدعى عليه")
    subject = st.text_area("الموضوع")

    if st.button("حفظ"):

        cur.execute("""
        INSERT INTO cases(case_no,year,claimant,defendant,subject,status,created_at)
        VALUES(?,?,?,?,?,?,?)
        """,(case_no,year,claimant,defendant,subject,"متداولة",str(datetime.now())))

        conn.commit()
        st.success("تم الحفظ ✔")
        st.rerun()

# =========================
# CASES LIST
# =========================
if st.session_state.page == "cases":

    st.subheader("📌 القضايا")

    rows = cur.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()

    for r in rows:

        st.markdown(f"""
        <div class="block">
        <b>{r[1]} / {r[2]}</b><br>
        {r[3]} ضد {r[4]}<br>
        {r[5]}<br>
        <b>{r[6]}</b>
        </div>
        """, unsafe_allow_html=True)

# =========================
# SEARCH
# =========================
if st.session_state.page == "search":

    st.subheader("🔍 بحث")

    q = st.text_input("بحث")

    if q:
        rows = cur.execute("""
        SELECT * FROM cases
        WHERE case_no LIKE ? OR claimant LIKE ? OR defendant LIKE ?
        """,(f"%{q}%",f"%{q}%",f"%{q}%")).fetchall()

        for r in rows:
            st.write(f"{r[1]} - {r[3]} ضد {r[4]}")

# =========================
# SESSIONS
# =========================
if st.session_state.page == "sessions":

    st.subheader("📅 الجلسات")

    case_id = st.number_input("رقم القضية", min_value=1)

    session_date = st.date_input("تاريخ الجلسة")
    roll = st.text_input("الرول")
    action = st.text_area("الإجراء")
    notes = st.text_area("ملاحظات")

    if st.button("حفظ الجلسة"):

        cur.execute("""
        INSERT INTO sessions(case_id,session_date,roll,action,notes)
        VALUES(?,?,?,?,?)
        """,(case_id,str(session_date),roll,action,notes))

        conn.commit()
        st.success("تم الحفظ ✔")

# =========================
# REPORTS
# =========================
if st.session_state.page == "reports":

    st.subheader("📊 التقارير")

    rows = cur.execute("SELECT * FROM cases").fetchall()

    df = pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True)

    # Word
    doc = Document()
    doc.add_heading("تقرير القضايا",0)

    for i,r in enumerate(rows,1):
        doc.add_paragraph(f"{i} - {r[1]} - {r[3]} ضد {r[4]}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button("Word",buffer,"report.docx")

    # PDF
    pdf = BytesIO()
    p = canvas.Canvas(pdf,pagesize=A4)

    y=800
    for i,r in enumerate(rows,1):
        p.drawString(50,y,f"{i} - {r[1]} - {r[3]} ضد {r[4]}")
        y-=20

    p.save()
    pdf.seek(0)

    st.download_button("PDF",pdf,"report.pdf")
