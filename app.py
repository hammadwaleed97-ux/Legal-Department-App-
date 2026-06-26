import streamlit as st
import sqlite3
from datetime import datetime

# =====================================
# قاعدة البيانات
# =====================================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

# =====================================
# جدول القضايا
# =====================================

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

# =====================================
# جدول الجلسات
# =====================================

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

# =====================================
# جدول المستندات
# =====================================

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
# الصفحات
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"
st.set_page_config(
    page_title="",
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
    background: linear-gradient(
        180deg,
        #00152d,
        #002b5c,
        #00152d
    );
}

html, body, [class*="css"]{
    direction:rtl;
}

.main-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:#FFD700;
    text-shadow:0 0 20px gold;
}

.logo{
    text-align:center;
    font-size:110px;
}

.watermark{
    position:fixed;
    top:35%;
    left:50%;
    transform:translate(-50%,-50%);
    font-size:280px;
    opacity:0.05;
    z-index:0;
}

/* ===== إصلاح ظهور أسماء الحقول ===== */

label{
    color:white !important;
    font-size:20px !important;
    font-weight:bold !important;
    opacity:1 !important;
}

[data-testid="stWidgetLabel"]{
    color:white !important;
    font-size:20px !important;
    font-weight:bold !important;
    opacity:1 !important;
}

.stSelectbox label,
.stTextInput label,
.stTextArea label,
.stDateInput label,
.stFileUploader label{
    color:white !important;
    font-size:20px !important;
    font-weight:bold !important;
}

p,h1,h2,h3,h4,h5,h6,span{
    color:white !important;
}

/* ===== الأزرار ===== */

.stButton > button{
    width:100%;
    height:95px;
    font-size:28px;
    font-weight:bold;
    border-radius:25px;
    border:3px solid gold;
    background:linear-gradient(
        135deg,
        #0d47a1,
        #1565c0
    );
    color:white !important;
    box-shadow:0 0 25px rgba(255,215,0,.6);
}

.stButton > button:hover{
    transform:scale(1.03);
}

/* ===== الشريط السفلي ===== */

.news-bar{
    position:fixed;
    bottom:0;
    right:0;
    width:100%;
    height:42px;
    background:#000814;
    border-top:2px solid gold;
    overflow:hidden;
    z-index:999999;
}

.news-text{
    position:absolute;
    white-space:nowrap;
    font-size:20px;
    font-weight:bold;
    line-height:42px;
    animation:scrollText 25s linear infinite;
}

@keyframes scrollText{
0%{
transform:translateX(-100%);
}
100%{
transform:translateX(100vw);
}
}

</style>
""", unsafe_allow_html=True)
# =========================
# خلفية ميزان شفافة
# =========================

st.markdown("""
<div class="watermark">
⚖️
</div>
""", unsafe_allow_html=True)

# =========================
# اللوجو
# =========================

st.markdown("""
<div class="logo">⚖️</div>
<div class="main-title">إدارة القضايا</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# =========================
# الأيقونات
# =========================
# =========================
# الصفحة الرئيسية
# =========================

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

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔔 التنبيهات", use_container_width=True):
            pass

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📊 التقارير", use_container_width=True):
            pass

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🗄️ الأرشيف", use_container_width=True):
            pass

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("📚 المكتبة القانونية", use_container_width=True):
            pass
# =========================
# الشريط السفلي
# =========================

st.markdown("""

<div class="news-bar">
<div class="news-text">

<span style="color:#FFD700;">
مع تحيات / وليد حماد
</span>

<span style="color:white;"> | </span>

<span style="color:#00FFFF;">
الإدارة العامة للشئون القانونية
</span>

<span style="color:white;"> | </span>

<span style="color:#7FFF00;">
ديوان عام منطقة البحيرة
</span>

<span style="color:white;"> | </span>

<span style="color:#FF4500;">
الهيئة القومية للتأمين الاجتماعى
</span>

</div>
</div>

""", unsafe_allow_html=True)
# =====================================
# تسجيل القضايا
# =====================================

if st.session_state.page == "cases":
    st.markdown("""
<h2 style='color:#FFD700;
text-align:center;
text-shadow:0 0 10px gold;'>
⚖️ تسجيل قضية جديدة
</h2>
""", unsafe_allow_html=True)
    col1,col2 = st.columns(2)

    with col1:

        case_type = st.selectbox(
            "نوع الدعوى",
            ["دعوى","استئناف","طعن"]
        )

        court_type = st.selectbox(
            "المحكمة",
            [
                "الابتدائية",
                "الاستئناف",
                "النقض",
                "الإدارية",
                "القضاء الإداري",
                "الإدارية العليا"
            ]
        )

        court_name = st.text_input("اسم المحكمة")

        mission = ""

        if case_type == "استئناف":
            mission = st.text_input("المأمورية")

        case_number = st.text_input(
            "رقم الدعوى / الاستئناف / الطعن"
        )

        judicial_year = st.text_input(
            "السنة القضائية"
        )

        circuit = st.text_input(
            "الدائرة"
        )

        case_category = st.text_input(
            "النوع"
        )

    with col2:

        plaintiff = st.text_input(
            "المدعي / المستأنف / الطاعن"
        )

        defendant = st.text_input(
            "المدعى عليه / المستأنف ضده / المطعون ضده"
        )

        subject = st.text_area(
            "موضوع الدعوى",
            height=120
        )

        first_session_date = st.date_input(
            "تاريخ أول جلسة"
        )

        roll_number = st.text_input(
            "الرول"
        )

        first_procedure = st.text_area(
            "سبب الجلسة",
            height=100
        )

        notes = st.text_area(
            "ملاحظات",
            height=100
        )

    st.markdown("---")

    whatsapp_enabled = st.checkbox(
        "تفعيل التنبيهات عبر واتساب"
    )

    whatsapp_number = ""

    if whatsapp_enabled:

        whatsapp_number = st.text_input(
            "رقم واتساب"
        )

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "تحميل صحيفة الدعوى / الاستئناف / الطعن"
    )

    col_save,col_cancel = st.columns(2)

    with col_save:

        if st.button(
            "💾 حفظ القضية",
            use_container_width=True
        ):

            cur.execute("""
            INSERT INTO cases(
            case_type,
            court_type,
            court_name,
            mission,
            case_number,
            judicial_year,
            circuit,
            case_category,
            plaintiff,
            defendant,
            subject,
            notes,
            whatsapp_enabled,
            whatsapp_number,
            created_at
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
            case_type,
            court_type,
            court_name,
            mission,
            case_number,
            judicial_year,
            circuit,
            case_category,
            plaintiff,
            defendant,
            subject,
            notes,
            int(whatsapp_enabled),
            whatsapp_number,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            ))

            conn.commit()

            case_id = cur.lastrowid

            cur.execute("""
            INSERT INTO sessions(
            case_id,
            session_date,
            roll_number,
            procedure,
            created_at
            )
            VALUES(?,?,?,?,?)
            """,
            (
            case_id,
            str(first_session_date),
            roll_number,
            first_procedure,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            ))

            conn.commit()

            st.success(
                "تم حفظ القضية بنجاح"
            )

            st.session_state.page = "inventory"
            st.rerun()

    with col_cancel:

        if st.button(
            "⬅ العودة للرئيسية",
            use_container_width=True
        ):
            st.session_state.page = "home"
            st.rerun()                                    
# =====================================
# الحصر العام
# =====================================

if st.session_state.page == "inventory":

    st.markdown("## 📋 الحصر العام للقضايا")

    if "delete_case_id" not in st.session_state:
        st.session_state.delete_case_id = None

    cur.execute("""
    SELECT
    c.id,
    c.case_type,
    c.case_number,
    c.judicial_year,
    c.circuit,
    c.case_category,
    c.court_name,
    c.mission,
    c.plaintiff,
    c.defendant,
    c.subject,

    (
        SELECT session_date
        FROM sessions s
        WHERE s.case_id = c.id
        ORDER BY session_date DESC
        LIMIT 1
    ) AS last_session,

    (
        SELECT procedure
        FROM sessions s
        WHERE s.case_id = c.id
        ORDER BY session_date DESC
        LIMIT 1
    ) AS last_procedure

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

        plaintiff = row[8].replace(
            "الهيئة القومية للتأمين الاجتماعى",
            "الهيئة"
        )

        defendant = row[9].replace(
            "الهيئة القومية للتأمين الاجتماعى",
            "الهيئة"
        )

        line = (
            f"{row[2]} لسنة {row[3]}   "
            f"دائرة {row[4]}   "
            f"{row[5]}   "
            f"{case_type}   "
            f"{row[6]}"
        )

        if row[7]:
            line += f"   مأمورية {row[7]}"

        line += (
            f"   {plaintiff} ضد {defendant}"
            f"   {row[10]}"
            f"   {row[11]}"
            f"   {row[12]}"
        )

        st.markdown(
            f"""
            <div style="
                font-size:18px;
                font-weight:bold;
                color:white;
                padding:6px 0px;
            ">
            {line}
            </div>
            """,
            unsafe_allow_html=True
        )

        b1, b2, b3, b4 = st.columns([1.2,1.2,1.2,8])

        with b1:
            if st.button(
                "📂 فتح",
                key=f"open_{case_id}",
                use_container_width=True
            ):
                st.session_state.selected_case = case_id
                st.session_state.page = "case_details"
                st.rerun()

        with b2:
            if st.button(
                "✏️ تعديل",
                key=f"edit_{case_id}",
                use_container_width=True
            ):
                st.session_state.selected_case = case_id
                st.session_state.page = "edit_case"
                st.rerun()

        with b3:
            if st.button(
                "🗑 حذف",
                key=f"delete_{case_id}",
                use_container_width=True
            ):
                st.session_state.delete_case_id = case_id

        if st.session_state.delete_case_id == case_id:

            st.warning("هل ترغب فى حذف القضية نهائياً ؟")

            d1, d2 = st.columns(2)

            with d1:

                if st.button(
                    "✅ تأكيد الحذف",
                    key=f"confirm_{case_id}"
                ):

                    cur.execute(
                        "DELETE FROM sessions WHERE case_id=?",
                        (case_id,)
                    )

                    cur.execute(
                        "DELETE FROM documents WHERE case_id=?",
                        (case_id,)
                    )

                    cur.execute(
                        "DELETE FROM cases WHERE id=?",
                        (case_id,)
                    )

                    conn.commit()

                    st.session_state.delete_case_id = None

                    st.success("تم حذف القضية بنجاح")

                    st.rerun()

            with d2:

                if st.button(
                    "❌ إلغاء",
                    key=f"cancel_{case_id}"
                ):

                    st.session_state.delete_case_id = None
                    st.rerun()

        st.markdown(
            "<hr style='margin-top:6px;margin-bottom:10px;'>",
            unsafe_allow_html=True
        )

if st.button(
    "⬅ العودة للرئيسية",
    use_container_width=True
):

    st.session_state.page = "home"
    st.rerun()
    
                        
