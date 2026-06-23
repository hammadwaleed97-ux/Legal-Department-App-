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
    page_title="نظام المحاكم",
    layout="wide",
    page_icon="⚖️"
)

# =========================
# تصميم رسمي
# =========================
st.markdown("""
<style>
.stApp{background:#041a3a;color:white;}
h1,h2,h3,h4,h5,h6,p,label,span{color:white!important;}

.card{
    background:white;
    color:black;
    padding:12px;
    border-radius:12px;
    border-left:6px solid #c9a227;
    margin:10px 0;
}

button{
    background:#0b2c5f!important;
    color:white!important;
    font-weight:bold!important;
    border-radius:10px!important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
conn = sqlite3.connect("court.db", check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cases(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        case_no TEXT,
        year TEXT,
        degree TEXT,
        claimant TEXT,
        defendant TEXT,
        subject TEXT,
        status TEXT,
        judgment TEXT,
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
# SESSION
# =========================
if "page" not in st.session_state:
    st.session_state.page = "dashboard"

# =========================
# HEADER
# =========================
st.markdown("""
<div style="text-align:center">
<h1>⚖️ نظام إدارة المحاكم</h1>
<h3>وزارة العدل - نموذج تشغيلي داخلي</h3>
<hr>
<h4 style="color:#FFD700;">Court Management System</h4>
</div>
""", unsafe_allow_html=True)

# =========================
# DASHBOARD
# =========================
rows = cur.execute("SELECT * FROM cases").fetchall()

total = len(rows)
win = len([r for r in rows if r[8] == "لصالح الهيئة"])
lose = len([r for r in rows if r[8] == "ضد الهيئة"])

c1,c2,c3 = st.columns(3)
c1.metric("إجمالي القضايا", total)
c2.metric("أحكام لصالح", win)
c3.metric("أحكام ضد", lose)

st.markdown("---")

# =========================
# MENU
# =========================
m1,m2,m3,m4 = st.columns(4)

if m1.button("📁 القضايا"):
    st.session_state.page = "cases"

if m2.button("➕ تسجيل قضية"):
    st.session_state.page = "add"

if m3.button("⚖️ الأحكام"):
    st.session_state.page = "judgment"

if m4.button("📊 تقارير"):
    st.session_state.page = "reports"

# =========================
# ADD CASE
# =========================
if st.session_state.page == "add":

    st.subheader("➕ تسجيل قضية جديدة")

    case_no = st.text_input("رقم القضية")
    year = st.text_input("السنة")
    degree = st.selectbox("الدرجة", ["ابتدائي","استئناف","نقض"])
    claimant = st.text_input("المدعي")
    defendant = st.text_input("المدعى عليه")
    subject = st.text_area("الموضوع")

    if st.button("حفظ"):

        cur.execute("""
        INSERT INTO cases(case_no,year,degree,claimant,defendant,subject,status,judgment,created_at)
        VALUES(?,?,?,?,?,?,?,?,?)
        """,(case_no,year,degree,claimant,defendant,subject,"متداولة","",str(datetime.now())))

        conn.commit()
        st.success("تم الحفظ ✔")
        st.rerun()

# =========================
# CASE LIST
# =========================
if st.session_state.page == "cases":

    st.subheader("📁 القضايا")

    rows = cur.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()

    for r in rows:

        st.markdown(f"""
        <div class="card">
        <b>{r[1]} / {r[2]}</b><br>
        <b>الدرجة:</b> {r[3]}<br>
        {r[4]} ضد {r[5]}<br>
        {r[6]}<br>
        <b>الحالة:</b> {r[7]}<br>
        <b>الحكم:</b> {r[8] or "لم يصدر"}
        </div>
        """, unsafe_allow_html=True)

# =========================
# JUDGMENT SYSTEM (قلب النظام)
# =========================
if st.session_state.page == "judgment":

    st.subheader("⚖️ تسجيل حكم")

    case_id = st.number_input("رقم القضية", min_value=1)

    judgment = st.selectbox("الحكم", ["","لصالح الهيئة","ضد الهيئة","تأجيل","إحالة خبير"])

    if st.button("اعتماد الحكم"):

        cur.execute("""
        UPDATE cases
        SET judgment=?, status=?
        WHERE id=?
        """,(judgment,"منتهية" if judgment in ["لصالح الهيئة","ضد الهيئة"] else "متداولة",case_id))

        conn.commit()
        st.success("تم تسجيل الحكم ✔")
        st.rerun()

# =========================
# REPORTS
# =========================
if st.session_state.page == "reports":

    st.subheader("📊 تقارير المحاكم")

    rows = cur.execute("SELECT * FROM cases").fetchall()

    df = pd.DataFrame(rows)
    st.dataframe(df,use_container_width=True)

    doc = Document()
    doc.add_heading("تقرير المحاكم",0)

    for i,r in enumerate(rows,1):
        doc.add_paragraph(f"{i}- {r[1]} / {r[2]} - {r[4]} ضد {r[5]} - {r[8]}")

    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)

    st.download_button("Word",buf,"court.docx")

    pdf = BytesIO()
    p = canvas.Canvas(pdf,pagesize=A4)

    y=800
    for i,r in enumerate(rows,1):
        p.drawString(50,y,f"{i}- {r[1]} / {r[2]} - {r[4]} ضد {r[5]} - {r[8]}")
        y-=20

    p.save()
    pdf.seek(0)

    st.download_button("PDF",pdf,"court.pdf")
