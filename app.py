import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# =====================================
# إعداد الصفحة
# =====================================
st.set_page_config(
    page_title="نظام القضايا PRO",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================
# Session State
# =====================================
for k,v in {
    "page":"home",
    "selected_case":None
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def go(page):
    st.session_state.page = page
    st.rerun()

# =====================================
# DB
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
created_at TEXT
)
""")
conn.commit()

# =====================================
# HOME
# =====================================
if st.session_state.page == "home":

    st.title("⚖️ نظام إدارة القضايا")

    c1,c2,c3 = st.columns(3)

    with c1:
        if st.button("📋 الحصر العام"):
            go("inventory")

    with c2:
        if st.button("📊 التقارير"):
            go("reports")

    with c3:
        if st.button("➕ تسجيل قضية"):
            go("add")


# =====================================
# ADD CASE
# =====================================
elif st.session_state.page == "add":

    st.subheader("➕ تسجيل قضية")

    case_type = st.selectbox("النوع", ["دعوى","استئناف","طعن"])
    court_type = st.text_input("المحكمة")
    court_name = st.text_input("اسم المحكمة")
    mission = st.text_input("المأمورية")

    case_number = st.text_input("رقم القضية")
    judicial_year = st.text_input("السنة")

    circuit = st.text_input("الدائرة")
    case_category = st.text_input("النوع")

    plaintiff = st.text_input("المدعي")
    defendant = st.text_input("المدعى عليه")

    subject = st.text_area("الموضوع")
    notes = st.text_area("ملاحظات")

    if st.button("💾 حفظ"):
        cur.execute("""
        INSERT INTO cases VALUES(
        NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?
        )
        """,(
        case_type,court_type,court_name,mission,
        case_number,judicial_year,circuit,
        case_category,plaintiff,defendant,
        subject,notes,datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        go("inventory")


# =====================================
# INVENTORY (🔥 TABLE MODE)
# =====================================
elif st.session_state.page == "inventory":

    st.subheader("📋 الحصر العام (جدول احترافي)")

    search = st.text_input("🔍 بحث")

    if search:
        cur.execute("""
        SELECT * FROM cases
        WHERE case_number LIKE ?
        OR plaintiff LIKE ?
        OR defendant LIKE ?
        ORDER BY id DESC
        """,(f"%{search}%",f"%{search}%",f"%{search}%"))
    else:
        cur.execute("SELECT * FROM cases ORDER BY id DESC")

    rows = cur.fetchall()

    if not rows:
        st.warning("لا توجد قضايا")
        if st.button("⬅ رجوع"):
            go("home")
    else:

        df = pd.DataFrame(rows, columns=[
            "ID","النوع","المحكمة","اسم المحكمة","المأمورية",
            "رقم القضية","السنة","الدائرة","النوع","المدعي",
            "المدعى عليه","الموضوع","ملاحظات","التاريخ"
        ])

        st.dataframe(df, use_container_width=True)

        st.markdown("### 🎯 اختيار قضية")

        case_id = st.selectbox("اختر رقم القضية", df["ID"])

        c1,c2,c3 = st.columns(3)

        with c1:
            if st.button("📂 فتح"):
                st.session_state.selected_case = case_id
                go("case")

        with c2:
            if st.button("✏️ تعديل"):
                st.session_state.selected_case = case_id
                go("edit")

        with c3:
            if st.button("🗑 حذف"):
                cur.execute("DELETE FROM cases WHERE id=?", (case_id,))
                conn.commit()
                st.rerun()

        if st.button("⬅ رجوع"):
            go("home")


# =====================================
# CASE DETAILS
# =====================================
elif st.session_state.page == "case":

    case_id = st.session_state.selected_case

    cur.execute("SELECT * FROM cases WHERE id=?", (case_id,))
    c = cur.fetchone()

    if not c:
        st.error("غير موجود")
        go("inventory")
    else:

        st.subheader("⚖️ ملف القضية")

        st.write(f"رقم: {c[5]}")
        st.write(f"سنة: {c[6]}")
        st.write(f"محكمة: {c[3]}")
        st.write(f"دائرة: {c[7]}")
        st.write(f"مدعي: {c[9]}")
        st.write(f"مدعى عليه: {c[10]}")
        st.write(f"موضوع: {c[11]}")

        if st.button("⬅ رجوع"):
            go("inventory")


# =====================================
# EDIT
# =====================================
elif st.session_state.page == "edit":

    case_id = st.session_state.selected_case

    cur.execute("SELECT * FROM cases WHERE id=?", (case_id,))
    c = cur.fetchone()

    if not c:
        st.error("غير موجود")
        go("inventory")
    else:

        st.subheader("✏️ تعديل")

        case_type = st.selectbox("نوع", ["دعوى","استئناف","طعن"],
                                 index=["دعوى","استئناف","طعن"].index(c[1]) if c[1] in ["دعوى","استئناف","طعن"] else 0)

        court_type = st.text_input("المحكمة", value=c[2])
        court_name = st.text_input("اسم المحكمة", value=c[3])
        mission = st.text_input("المأمورية", value=c[4])
        case_number = st.text_input("رقم القضية", value=c[5])
        judicial_year = st.text_input("السنة", value=c[6])
        circuit = st.text_input("الدائرة", value=c[7])
        case_category = st.text_input("النوع", value=c[8])
        plaintiff = st.text_input("مدعي", value=c[9])
        defendant = st.text_input("مدعى عليه", value=c[10])
        subject = st.text_area("موضوع", value=c[11])
        notes = st.text_area("ملاحظات", value=c[12])

        if st.button("💾 حفظ التعديل"):
            cur.execute("""
            UPDATE cases SET
            case_type=?,court_type=?,court_name=?,mission=?,
            case_number=?,judicial_year=?,circuit=?,case_category=?,
            plaintiff=?,defendant=?,subject=?,notes=?
            WHERE id=?
            """,(
            case_type,court_type,court_name,mission,
            case_number,judicial_year,circuit,case_category,
            plaintiff,defendant,subject,notes,case_id
            ))
            conn.commit()
            go("inventory")


# =====================================
# REPORTS (🔥 STRONG)
# =====================================
elif st.session_state.page == "reports":

    st.subheader("📊 التقارير")

    cur.execute("SELECT * FROM cases ORDER BY id DESC")
    rows = cur.fetchall()

    st.success(f"إجمالي القضايا: {len(rows)}")

    if rows:

        df = pd.DataFrame(rows, columns=[
            "ID","النوع","المحكمة","اسم المحكمة","المأمورية",
            "رقم القضية","السنة","الدائرة","النوع","المدعي",
            "المدعى عليه","الموضوع","ملاحظات","التاريخ"
        ])

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "⬇ تحميل Excel/CSV",
            df.to_csv(index=False).encode("utf-8-sig"),
            "cases_report.csv",
            "text/csv"
        )

    if st.button("⬅ رجوع"):
        go("home")
