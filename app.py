import streamlit as st
import sqlite3
from datetime import datetime
import os

# =====================================
# إعداد الصفحة
# =====================================

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# Session State
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

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
# التصميم العام (CSS)
# =====================================

st.markdown("""
<style>

#MainMenu{visibility:hidden;}
header{visibility:hidden;}
footer{visibility:hidden;}

html,body,[class*="css"]{
    direction:rtl;
}

/* الخلفية */

.stApp{

background:
linear-gradient(
180deg,
#5A3A22 0%,
#4A2F1C 35%,
#352114 70%,
#24160D 100%
);

}

/* ميزان الخلفية */

.watermark{

position:fixed;

top:50%;

left:50%;

transform:translate(-50%,-50%);

font-size:320px;

opacity:.05;

z-index:0;

}

/* رأس البرنامج */

.header{

text-align:center;

position:relative;

z-index:999;

}

.logo{

font-size:90px;

margin-bottom:-15px;

}

.title1{

font-size:34px;

font-weight:bold;

color:#FFD700;

}

.title2{

font-size:27px;

font-weight:bold;

color:white;

}

.title3{

font-size:27px;

font-weight:bold;

color:white;

}

.title4{

font-size:27px;

font-weight:bold;

color:white;

}

/* الأزرار */

.stButton>button{

width:100%;

height:85px;

font-size:24px;

font-weight:bold;

border-radius:18px;

background:#6D4C41;

color:white;

border:2px solid gold;

transition:.3s;

}

.stButton>button:hover{

background:#8D6E63;

transform:scale(1.02);

box-shadow:0 0 18px gold;

}

/* الكتابة */

label,p,h1,h2,h3,h4,h5,h6,span{

color:white !important;

font-weight:bold;

}

/* الشريط السفلى */

.news-bar{

position:fixed;

bottom:0;

right:0;

width:100%;

height:45px;

background:#1A120B;

border-top:2px solid gold;

overflow:hidden;

z-index:999999;

}

.news-text{

position:absolute;

right:-100%;

white-space:nowrap;

line-height:45px;

font-size:20px;

font-weight:bold;

animation:scrollText 35s linear infinite;

}

@keyframes scrollText{

from{

right:-100%;

}

to{

right:100%;

}

}

</style>

""",unsafe_allow_html=True)

# =====================================
# الميزان بالخلفية
# =====================================

st.markdown("""

<div class="watermark">

⚖️

</div>

""",unsafe_allow_html=True)

# =====================================
# رأس البرنامج
# =====================================

st.markdown("""

<div class="header">

<div class="logo">
⚖️
</div>

<div class="title1">
الهيئة القومية للتأمين الاجتماعى
</div>

<div class="title2">
الإدارة المركزية للشئون القانونية
</div>

<div class="title3">
الإدارة العامة للقضايا
</div>

<div class="title4">
ديوان عام منطقة البحيرة
</div>

</div>

<br>

""",unsafe_allow_html=True)

# =====================================
# الشريط السفلى
# =====================================

st.markdown("""

<div class="news-bar">

<div class="news-text">

<span style="color:#FFD700;">
✨ مع تحيات / وليد حماد
</span>

<span style="color:white;">
&nbsp;&nbsp;|&nbsp;&nbsp;
</span>

<span style="color:#00FFFF;">
الإدارة العامة للقضايا
</span>

<span style="color:white;">
&nbsp;&nbsp;|&nbsp;&nbsp;
</span>

<span style="color:#7CFC00;">
الإدارة المركزية للشئون القانونية
</span>

<span style="color:white;">
&nbsp;&nbsp;|&nbsp;&nbsp;
</span>

<span style="color:#FFA500;">
ديوان عام منطقة البحيرة
</span>

<span style="color:white;">
&nbsp;&nbsp;|&nbsp;&nbsp;
</span>

<span style="color:#FF4444;">
الهيئة القومية للتأمين الاجتماعى
</span>

</div>

</div>

""",unsafe_allow_html=True)
# =====================================
# الصفحة الرئيسية
# =====================================

if st.session_state.page == "home":

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,3,1])

    with c2:

        if st.button(
            "⚖️ تسجيل القضايا",
            use_container_width=True
        ):
            st.session_state.page = "cases"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "📋 الحصر العام",
            use_container_width=True
        ):
            st.session_state.page = "inventory"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🔔 التنبيهات",
            use_container_width=True
        ):
            st.session_state.page = "notifications"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "📊 التقارير",
            use_container_width=True
        ):
            st.session_state.page = "reports"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🗄️ الأرشيف",
            use_container_width=True
        ):
            st.session_state.page = "archive"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "📚 المكتبة القانونية",
            use_container_width=True
        ):
            st.session_state.page = "library"
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🔍 البحث عن دعوى",
            use_container_width=True
        ):
            st.session_state.page = "search"
            st.rerun()


# =====================================
# صفحات تحت الإنشاء
# =====================================

elif st.session_state.page == "notifications":

    st.info("🚧 سيتم تنفيذ قسم التنبيهات فى المرحلة القادمة.")

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()


elif st.session_state.page == "reports":

    st.info("🚧 سيتم تنفيذ قسم التقارير فى المرحلة القادمة.")

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()


elif st.session_state.page == "archive":

    st.info("🚧 سيتم تنفيذ قسم الأرشيف فى المرحلة القادمة.")

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()


elif st.session_state.page == "library":

    st.info("🚧 سيتم تنفيذ قسم المكتبة القانونية فى المرحلة القادمة.")

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()


elif st.session_state.page == "search":

    st.info("🚧 سيتم تنفيذ البحث عن الدعاوى فى المرحلة القادمة.")

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()
        # ==========================================================
# تسجيل القضايا - الجزء الأول
# ==========================================================

elif st.session_state.page == "cases":

    st.markdown("""

    <div style="
    background:#4E342E;
    padding:15px;
    border-radius:15px;
    border:2px solid gold;
    text-align:center;
    color:white;
    font-size:30px;
    font-weight:bold;
    box-shadow:0 0 15px rgba(255,215,0,.4);
    ">

    ⚖️ تسجيل قضية جديدة

    </div>

    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # =====================================
    # العمود الأول
    # =====================================

    with col1:

        case_type = st.selectbox(
            "نوع الدعوى",
            [
                "دعوى",
                "استئناف",
                "طعن"
            ]
        )

        court_type = st.selectbox(
            "المحكمة",
            [
                "الابتدائية",
                "الاستئناف",
                "النقض",
                "الإدارية",
                "القضاء الإدارى",
                "الإدارية العليا"
            ]
        )

        court_name = st.text_input(
            "اسم المحكمة"
        )

        mission = ""

        if case_type == "استئناف":

            mission = st.text_input(
                "المأمورية"
            )

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
        # =====================================
    # العمود الثانى
    # =====================================

    with col2:

        plaintiff = st.text_input(
            "اسم المدعى / المستأنف / الطاعن"
        )

        defendant = st.text_input(
            "اسم المدعى عليه / المستأنف ضده / المطعون ضده"
        )

        subject = st.text_area(
            "موضوع الدعوى",
            height=130
        )

        first_session_date = st.date_input(
            "تاريخ أول جلسة"
        )

        roll_number = st.text_input(
            "الرول"
        )

        first_procedure = st.text_area(
            "سبب الجلسة",
            height=120
        )

        notes = st.text_area(
            "ملاحظات",
            height=120
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    # =====================================
    # تنبيهات الواتساب
    # =====================================

    whatsapp_enabled = st.checkbox(
        "📲 تفعيل التنبيهات عبر واتساب"
    )

    whatsapp_number = ""

    if whatsapp_enabled:

        whatsapp_number = st.text_input(
            "رقم هاتف واتساب"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # =====================================
    # رفع المستندات
    # =====================================

    document_type = st.selectbox(

        "نوع المستند",

        [

            "صحيفة الدعوى",

            "صحيفة الاستئناف",

            "صحيفة الطعن"

        ]

    )

    uploaded_file = st.file_uploader(

        "تحميل المستند",

        type=[
            "pdf",
            "doc",
            "docx"
        ]

    )

    st.markdown("<br>", unsafe_allow_html=True)
    # =====================================
    # أزرار الحفظ والحذف
    # =====================================

    col_save, col_delete = st.columns(2)

    # =====================================
    # حفظ القضية
    # =====================================

    with col_save:

        if st.button(
            "💾 حفظ القضية",
            use_container_width=True
        ):

            # التحقق من البيانات الأساسية

            if case_number.strip() == "":
                st.error("برجاء إدخال رقم القضية")
                st.stop()

            if court_name.strip() == "":
                st.error("برجاء إدخال اسم المحكمة")
                st.stop()

            if plaintiff.strip() == "":
                st.error("برجاء إدخال اسم المدعى")
                st.stop()

            # حفظ القضية

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

            VALUES(

            ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?

            )

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

            )

            )

            conn.commit()

            case_id = cur.lastrowid

            # =====================================
            # حفظ أول جلسة
            # =====================================

            cur.execute("""

            INSERT INTO sessions(

            case_id,
            session_date,
            roll_number,
            procedure,
            created_at

            )

            VALUES(

            ?,?,?,?,?

            )

            """,

            (

            case_id,
            str(first_session_date),
            roll_number,
            first_procedure,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            )

            )

            conn.commit()

            st.success("✅ تم حفظ القضية بنجاح")

            st.session_state.page = "inventory"

            st.rerun()

    # =====================================
    # حذف البيانات المدخلة
    # =====================================

    with col_delete:

        if st.button(
            "🗑 حذف البيانات",
            use_container_width=True
        ):

            st.rerun()
