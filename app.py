import streamlit as st
import sqlite3
from datetime import datetime
from io import BytesIO
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# =========================
# إعداد الصفحة
# =========================
st.set_page_config(
    page_title="نظام إدارة القضايا",
    layout="wide",
    page_icon="⚖️"
)

# =========================
# ستايل احترافي أزرق داكن
# =========================
st.markdown("""
<style>

.stApp {
    background: #062456;
    color: white;
}

h1,h2,h3,h4,h5,h6,p,label,span {
    color: white !important;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div {
    color: black !important;
}

.block {
    background: white;
    color: black;
    padding: 12px;
    border-radius: 12px;
    margin: 5px 0;
    border: 2px solid #0b3b91;
}

.btn-main button {
    background: #2f55d4 !important;
    color: white !important;
    border-radius: 12px;
    height: 50px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================
# DB
# =========================
conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS cases (
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

conn.commit()

# =========================
# Session
# =========================
if "page" not in st.session_state:
    st.session_state.page = "home"

# =========================
# لوجو
# =========================
st.markdown("""
<div style="text-align:center;">
<h1>⚖️ الهيئة القومية للتأمين الاجتماعي</h1>
<h3>الإدارة العامة للشئون القانونية</h3>
<h4>ديوان عام منطقة البحيرة</h4>
<hr>
<h3 style="color:#FFD700;">وليد حماد</h3>
</div>
""", unsafe_allow_html=True)

# =========================
# MENU
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📌 تسجيل القضايا"):
        st.session_state.page = "add"

with col2:
    if st.button("📋 القضايا"):
        st.session_state.page = "list"

with col3:
    if st.button("📊 التقارير"):
        st.session_state.page = "reports"

with col4:
    if st.button("🔍 البحث"):
        st.session_state.page = "search"

# =========================
# ADD CASE
# =========================
if st.session_state.page == "add":

    st.subheader("➕ تسجيل قضية جديدة")

    case_no = st.text_input("رقم القضية")
    year = st.text_input("السنة")
    claimant = st.text_input("المدعي")
    defendant = st.text_input("المدعى عليه")
    subject = st.text_area("الموضوع")

    if st.button("💾 حفظ القضية"):

        cur.execute("""
        INSERT INTO cases(case_no,year,claimant,defendant,subject,status,created_at)
        VALUES (?,?,?,?,?,?,?)
        """, (
            case_no, year, claimant, defendant,
            subject, "متداولة", str(datetime.now())
        ))

        conn.commit()
        st.success("تم الحفظ بنجاح ✔")
        st.rerun()

# =========================
# LIST CASES
# =========================
if st.session_state.page == "list":

    st.subheader("📋 القضايا")

    rows = cur.execute("SELECT * FROM cases ORDER BY id DESC").fetchall()

    for r in rows:

        st.markdown(f"""
        <div class="block">
        <b>رقم:</b> {r[1]} / {r[2]} <br>
        <b>الخصوم:</b> {r[3]} ضد {r[4]} <br>
        <b>الموضوع:</b> {r[5]} <br>
        <b>الحالة:</b> {r[6]}
        </div>
        """, unsafe_allow_html=True)

# =========================
# SEARCH
# =========================
if st.session_state.page == "search":

    st.subheader("🔍 بحث")

    q = st.text_input("ابحث")

    if q:
        rows = cur.execute("""
        SELECT * FROM cases
        WHERE case_no LIKE ? OR claimant LIKE ? OR defendant LIKE ?
        """, (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()

        for r in rows:
            st.write(f"{r[1]} - {r[3]} ضد {r[4]}")

# =========================
# REPORTS
# =========================
if st.session_state.page == "reports":

    st.subheader("📊 التقارير")

    rows = cur.execute("SELECT * FROM cases").fetchall()

    st.write(f"إجمالي القضايا: {len(rows)}")

    # Word
    doc = Document()
    doc.add_heading("تقرير القضايا", 0)

    for i, r in enumerate(rows, 1):
        doc.add_paragraph(f"{i} - {r[1]} - {r[3]} ضد {r[4]}")

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    st.download_button(
        "📥 تحميل Word",
        buffer,
        file_name="report.docx"
    )

    # PDF
    pdf = BytesIO()
    p = canvas.Canvas(pdf, pagesize=A4)

    y = 800
    for i, r in enumerate(rows, 1):
        p.drawString(50, y, f"{i} - {r[1]} - {r[3]} ضد {r[4]}")
        y -= 20

    p.save()
    pdf.seek(0)

    st.download_button(
        "📄 تحميل PDF",
        pdf,
        file_name="report.pdf"
    )
