import streamlit as st
import sqlite3

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
# قاعدة البيانات
# =====================================

conn = sqlite3.connect("cases.db", check_same_thread=False)
cur = conn.cursor()

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
first_session_date TEXT,
roll_number TEXT,
first_procedure TEXT
)
""")

conn.commit()

# =====================================
# إعداد الصفحات
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

# =====================================
# الصفحة الرئيسية
# =====================================

if st.session_state.page == "home":

    st.title("⚖️ إدارة القضايا")

    col1,col2,col3 = st.columns([2,3,2])

    with col2:

        if st.button("⚖️ تسجيل القضايا", use_container_width=True):
            st.session_state.page = "cases"
            st.rerun()

        if st.button("📋 الحصر العام", use_container_width=True):
            st.session_state.page = "inventory"
            st.rerun()

# =====================================
# تسجيل القضايا
# =====================================

elif st.session_state.page == "cases":

    st.subheader("⚖️ تسجيل قضية جديدة")

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

    case_number = st.text_input("رقم الدعوى")

    judicial_year = st.text_input("السنة القضائية")

    circuit = st.text_input("الدائرة")

    case_category = st.text_input("النوع")

    plaintiff = st.text_input("المدعي / المستأنف / الطاعن")

    defendant = st.text_input("المدعى عليه / المستأنف ضده / المطعون ضده")

    subject = st.text_area("موضوع الدعوى")

    first_session_date = st.date_input("تاريخ أول جلسة")

    roll_number = st.text_input("الرول")

    first_procedure = st.text_area("سبب الجلسة")

    notes = st.text_area("ملاحظات")

    if st.button("💾 حفظ القضية"):

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
        first_session_date,
        roll_number,
        first_procedure
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
        str(first_session_date),
        roll_number,
        first_procedure
        ))

        conn.commit()

        st.success("تم حفظ القضية")

        st.session_state.page = "inventory"
        st.rerun()

# =====================================
# الحصر العام
# =====================================

elif st.session_state.page == "inventory":

    st.subheader("📋 الحصر العام")

    rows = cur.execute("""
    SELECT *
    FROM cases
    ORDER BY id DESC
    """).fetchall()

    for row in rows:

        st.info(
        f"""
رقم الدعوى : {row[5]}/{row[6]}

المحكمة : {row[2]}

الدائرة : {row[7]}

المدعي : {row[9]}

المدعى عليه : {row[10]}

الموضوع : {row[11]}

آخر جلسة : {row[13]}

الإجراء : {row[15]}
        """
        )

    if st.button("⬅ العودة للرئيسية"):
        st.session_state.page = "home"
        st.rerun()
