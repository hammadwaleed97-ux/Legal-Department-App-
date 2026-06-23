import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# =========================
# إعداد
# =========================
st.set_page_config(page_title="إدارة القضايا", layout="wide", page_icon="⚖️")

st.markdown("""
<style>
.stApp{background:#061a33;color:white;}
.card{
    background:white;
    color:black;
    padding:12px;
    border-radius:12px;
    margin:10px 0;
    border-left:5px solid #1f4e79;
}
button{
    background:#1f4e79 !important;
    color:white !important;
    font-weight:bold !important;
    border-radius:10px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
conn = sqlite3.connect("cases.db", check_same_thread=False)
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
        action TEXT,
        notes TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS deleted_cases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_id INTEGER,
        reason TEXT,
        deleted_at TEXT
    )
    """)

    conn.commit()

init_db()

# =========================
# STATE
# =========================
if "page" not in st.session_state:
    st.session_state.page = "add"

# =========================
# MENU
# =========================
st.title("⚖️ نظام إدارة القضايا")

c1,c2,c3,c4,c5,c6 = st.columns(6)

if c1.button("➕ تسجيل"):
    st.session_state.page = "add"

if c2.button("📋 حصر عام"):
    st.session_state.page = "all"

if c3.button("📊 تقارير"):
    st.session_state.page = "reports"

if c4.button("🔔 تنبيهات"):
    st.session_state.page = "alerts"

if c5.button("📂 أرشيف"):
    st.session_state.page = "archive"

if c6.button("🗑️ محذوفات"):
    st.session_state.page = "deleted"

# =========================
# ADD CASE
# =========================
if st.session_state.page == "add":

    st.subheader("➕ تسجيل قضية")

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

# =========================
# ALL CASES (حصر عام)
# =========================
if st.session_state.page == "all":

    st.subheader("📋 الحصر العام للقضايا")

    rows = cur.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()

    for r in rows:

        st.markdown(f"""
        <div class="card">
        <b>{r[1]} / {r[2]}</b><br>
        {r[3]} ضد {r[4]}<br>
        {r[5]}<br>
        <b>الحالة:</b> {r[6]}
        </div>
        """, unsafe_allow_html=True)

        reason = st.text_input(f"سبب الحذف {r[0]}", key=f"del_{r[0]}")

        if st.button(f"🗑️ حذف {r[0]}", key=f"btn_{r[0]}"):

            cur.execute("""
            INSERT INTO deleted_cases(case_id,reason,deleted_at)
            VALUES(?,?,?)
            """,(r[0],reason,str(datetime.now())))

            cur.execute("DELETE FROM cases WHERE id=?",(r[0],))
            conn.commit()
            st.rerun()

# =========================
# ALERTS (تنبيهات)
# =========================
if st.session_state.page == "alerts":

    st.subheader("🔔 تنبيهات الجلسات")

    rows = cur.execute("SELECT * FROM cases WHERE status='متداولة'").fetchall()

    if not rows:
        st.info("لا توجد تنبيهات")

    for r in rows:
        st.write(f"⚖️ {r[1]} / {r[2]} - {r[3]} ضد {r[4]}")

# =========================
# ARCHIVE
# =========================
if st.session_state.page == "archive":

    st.subheader("📂 الأرشيف")

    rows = cur.execute("SELECT * FROM cases WHERE status!='متداولة'").fetchall()

    for r in rows:
        st.markdown(f"""
        <div class="card">
        {r[1]} / {r[2]}<br>
        {r[3]} ضد {r[4]}<br>
        {r[5]}<br>
        <b>{r[6]}</b>
        </div>
        """, unsafe_allow_html=True)

# =========================
# DELETED
# =========================
if st.session_state.page == "deleted":

    st.subheader("🗑️ القضايا المحذوفة")

    rows = cur.execute("""
    SELECT * FROM deleted_cases
    """).fetchall()

    for r in rows:
        st.write(f"قضية {r[1]} - سبب: {r[2]} - {r[3]}")

# =========================
# REPORTS
# =========================
if st.session_state.page == "reports":

    st.subheader("📊 التقارير")

    rows = cur.execute("SELECT * FROM cases").fetchall()

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)

    doc = Document()
    doc.add_heading("تقرير القضايا",0)

    for i,r in enumerate(rows,1):
        doc.add_paragraph(f"{i}- {r[1]} / {r[2]} - {r[3]} ضد {r[4]}")

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)

    st.download_button("Word",buf,"report.docx")

    pdf = BytesIO()
    p = canvas.Canvas(pdf,pagesize=A4)

    y=800
    for i,r in enumerate(rows,1):
        p.drawString(50,y,f"{i}- {r[1]} / {r[2]} - {r[3]} ضد {r[4]}")
        y-=20

    p.save()
    pdf.seek(0)

    st.download_button("PDF",pdf,"report.pdf")
