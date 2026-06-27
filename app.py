import streamlit as st
import sqlite3
from datetime import datetime
import os

# =====================================
# قاعدة البيانات
# =====================================

if not os.path.exists("uploads"):
    os.makedirs("uploads")

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

# إنشاء الجداول
cur.execute("""
CREATE TABLE IF NOT EXISTS cases(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_type TEXT,
    court_type TEXT,
    court_name TEXT,
    mission TEXT,
    case_number TEXT,
    judicial_year TEXT,
    circuit TEXT,
    case_category TEXT,
    plaintiff TEXT,
    defendant TEXT,
    subject TEXT,
    notes TEXT,
    whatsapp_enabled INTEGER,
    whatsapp_number TEXT,
    created_at TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS sessions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    session_date TEXT,
    roll_number TEXT,
    procedure TEXT,
    created_at TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS documents(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_id INTEGER,
    document_type TEXT,
    document_description TEXT,
    file_name TEXT,
    file_path TEXT,
    uploaded_at TEXT
)
""")

conn.commit()

# =====================================
# إعدادات Streamlit
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

if "delete_case_id" not in st.session_state:
    st.session_state.delete_case_id = None

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CSS
# =========================
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp{
    background: linear-gradient(180deg, #00152d, #002b5c, #00152d);
}

html, body, [class*="css"]{ direction:rtl; }

.main-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:#FFD700;
    text-shadow:0 0 20px gold;
}

.logo{ text-align:center; font-size:110px; }

.watermark{
    position:fixed; top:35%; left:50%; transform:translate(-50%,-50%);
    font-size:280px; opacity:0.05; z-index:0;
}

label, [data-testid="stWidgetLabel"]{
    color:white !important; font-size:20px !important; font-weight:bold !important;
}

.stButton > button{
    width:100%; height:95px; font-size:28px; font-weight:bold;
    border-radius:25px; border:3px solid gold;
    background:linear-gradient(135deg, #0d47a1, #1565c0);
    color:white !important; box-shadow:0 0 25px rgba(255,215,0,.6);
}

.stButton > button:hover{ transform:scale(1.03); }

.news-bar{
    position:fixed; bottom:0; right:0; width:100%; height:42px;
    background:#000814; border-top:2px solid gold;
    overflow:hidden; z-index:999999;
}

.news-text{
    position:absolute; white-space:nowrap; font-size:20px;
    font-weight:bold; line-height:42px;
    animation:scrollText 25s linear infinite;
}

@keyframes scrollText{
    0%{transform:translateX(-100%);}
    100%{transform:translateX(100vw);}
}
</style>
""", unsafe_allow_html=True)

# خلفية + لوجو
st.markdown('<div class="watermark">⚖️</div>', unsafe_allow_html=True)
st.markdown('<div class="logo">⚖️</div><div class="main-title">إدارة القضايا</div>', unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

# الشريط السفلي
st.markdown("""
<div class="news-bar">
<div class="news-text">
<span style="color:#FFD700;">مع تحيات / وليد حماد</span>
<span style="color:white;"> | </span>
<span style="color:#00FFFF;">الإدارة العامة للشئون القانونية</span>
<span style="color:white;"> | </span>
<span style="color:#7FFF00;">ديوان عام منطقة البحيرة</span>
<span style="color:white;"> | </span>
<span style="color:#FF4500;">الهيئة القومية للتأمين الاجتماعى</span>
</div>
</div>
""", unsafe_allow_html=True)

# =====================================
# الصفحة الرئيسية
# =====================================
if st.session_state.page == "home":
    c1, c2, c3 = st.columns([2,4,2])
    with c2:
        if st.button("⚖️ تسجيل القضايا", use_container_width=True):
            st.session_state.page = "cases"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📋 الحصر العام", use_container_width=True):
            st.session_state.page = "inventory"
            st.rerun()

        # باقي الأزرار (يمكن تفعيلها لاحقاً)
        for text in ["🔔 التنبيهات", "📊 التقارير", "🗄️ الأرشيف", "📚 المكتبة القانونية"]:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(text, use_container_width=True):
                st.info("هذه الصفحة تحت الإنشاء")

# =====================================
# تسجيل قضية جديدة
# =====================================
if st.session_state.page == "cases":
    st.markdown("### ⚖️ تسجيل قضية جديدة")
    
    col1, col2 = st.columns(2)
    with col1:
        case_type = st.selectbox("نوع الدعوى", ["دعوى", "استئناف", "طعن"])
        court_type = st.selectbox("المحكمة", ["الابتدائية", "الاستئناف", "النقض", "الإدارية", "القضاء الإداري", "الإدارية العليا"])
        court_name = st.text_input("اسم المحكمة")
        mission = st.text_input("المأمورية") if case_type == "استئناف" else ""
        case_number = st.text_input("رقم الدعوى / الاستئناف / الطعن")
        judicial_year = st.text_input("السنة القضائية")
        circuit = st.text_input("الدائرة")
        case_category = st.text_input("النوع")

    with col2:
        plaintiff = st.text_input("المدعي / المستأنف / الطاعن")
        defendant = st.text_input("المدعى عليه / المستأنف ضده / المطعون ضده")
        subject = st.text_area("موضوع الدعوى", height=120)
        first_session_date = st.date_input("تاريخ أول جلسة")
        roll_number = st.text_input("الرول")
        first_procedure = st.text_area("سبب الجلسة", height=100)
        notes = st.text_area("ملاحظات", height=100)

    st.markdown("---")
    whatsapp_enabled = st.checkbox("تفعيل التنبيهات عبر واتساب")
    whatsapp_number = st.text_input("رقم واتساب") if whatsapp_enabled else ""

    uploaded_file = st.file_uploader("تحميل صحيفة الدعوى / الاستئناف / الطعن", type=["pdf", "docx", "jpg", "png"])

    col_save, col_cancel = st.columns(2)
    with col_save:
        if st.button("💾 حفظ القضية", use_container_width=True):
            try:
                cur.execute("""
                    INSERT INTO cases VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    case_type, court_type, court_name, mission, case_number,
                    judicial_year, circuit, case_category, plaintiff, defendant,
                    subject, notes, int(whatsapp_enabled), whatsapp_number,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                case_id = cur.lastrowid

                # حفظ الجلسة الأولى
                cur.execute("""
                    INSERT INTO sessions VALUES (NULL,?,?,?,?,?)
                """, (
                    case_id, str(first_session_date), roll_number, first_procedure,
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()

                # حفظ الملف إن وجد
                if uploaded_file:
                    file_path = f"uploads/{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    cur.execute("""
                        INSERT INTO documents VALUES (NULL,?,?,?,?,?,?)
                    """, (
                        case_id, "صحيفة الدعوى", "المستند الأساسي",
                        uploaded_file.name, file_path,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ))
                    conn.commit()

                st.success("✅ تم حفظ القضية بنجاح")
                st.session_state.page = "inventory"
                st.rerun()
            except Exception as e:
                st.error(f"خطأ: {e}")

    with col_cancel:
        if st.button("⬅ العودة للرئيسية", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

# =====================================
# الحصر العام
# =====================================
if st.session_state.page == "inventory":
    st.markdown("## 📋 الحصر العام للقضايا")

    cur.execute("""
        SELECT c.*, 
               (SELECT session_date FROM sessions s WHERE s.case_id = c.id ORDER BY session_date DESC LIMIT 1) as last_session,
               (SELECT procedure FROM sessions s WHERE s.case_id = c.id ORDER BY session_date DESC LIMIT 1) as last_procedure
        FROM cases c
        ORDER BY c.id DESC
    """)
    rows = cur.fetchall()

    if not rows:
        st.warning("لا توجد قضايا مسجلة")
    else:
        for row in rows:
            case_id = row[0]
            case_type = row[1]
            plaintiff = row[8].replace("الهيئة القومية للتأمين الاجتماعى", "الهيئة")
            defendant = row[9].replace("الهيئة القومية للتأمين الاجتماعى", "الهيئة")

            line = f"{case_type} {row[4]} لسنة {row[5]} دائرة {row[6]} {row[7]} {row[3]} {plaintiff} ضد {defendant} {row[10]}"

            if row[13]:  # last_session
                line += f" - آخر جلسة: {row[13]}"

            st.markdown(f"**{line}**")

            c1, c2, c3 = st.columns([1,1,1])
            with c1:
                if st.button("📂 فتح", key=f"open_{case_id}"):
                    st.session_state.selected_case = case_id
                    st.session_state.page = "case_details"
                    st.rerun()
            with c2:
                if st.button("✏️ تعديل", key=f"edit_{case_id}"):
                    st.session_state.selected_case = case_id
                    st.session_state.page = "edit_case"
                    st.rerun()
            with c3:
                if st.button("🗑 حذف", key=f"delete_{case_id}"):
                    st.session_state.delete_case_id = case_id

            if st.session_state.delete_case_id == case_id:
                st.warning("⚠️ هل ترغب في حذف القضية نهائياً؟")
                d1, d2 = st.columns(2)
                with d1:
                    if st.button("✅ تأكيد الحذف", key=f"confirm_{case_id}"):
                        cur.execute("DELETE FROM sessions WHERE case_id=?", (case_id,))
                        cur.execute("DELETE FROM documents WHERE case_id=?", (case_id,))
                        cur.execute("DELETE FROM cases WHERE id=?", (case_id,))
                        conn.commit()
                        st.success("تم الحذف")
                        st.session_state.delete_case_id = None
                        st.rerun()
                with d2:
                    if st.button("❌ إلغاء", key=f"cancel_{case_id}"):
                        st.session_state.delete_case_id = None
                        st.rerun()

            st.markdown("---")

    if st.button("⬅ العودة للرئيسية", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

# =====================================
# صفحات إضافية (أساسية)
# =====================================
if st.session_state.page == "case_details" and st.session_state.selected_case:
    st.title("تفاصيل القضية")
    st.info("صفحة التفاصيل تحت التطوير - سيتم توسيعها لاحقاً")
    if st.button("عودة"):
        st.session_state.page = "inventory"
        st.rerun()

if st.session_state.page == "edit_case" and st.session_state.selected_case:
    st.title("تعديل القضية")
    st.info("صفحة التعديل تحت التطوير")
    if st.button("عودة"):
        st.session_state.page = "inventory"
        st.rerun()
