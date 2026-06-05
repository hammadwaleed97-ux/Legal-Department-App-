from docx import Document

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =====================
# التصميم
# =====================

st.markdown("""
<style>

.stApp{
background:#0b1f3a;
direction:rtl;
}

h1,h2,h3,h4,h5,h6,p,label,div{
color:white !important;
}

.stButton button{
background:#163d7a;
color:white;
border-radius:10px;
font-weight:bold;
}

div[data-baseweb="select"]{
color:black;
}

</style>
""", unsafe_allow_html=True)

# =====================
# قاعدة البيانات
# =====================

conn = sqlite3.connect(
    "cases.db",
    check_same_thread=False
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

claimant_type TEXT,
claimant TEXT,

defendant_type TEXT,
defendant TEXT,

case_no TEXT,
judicial_year TEXT,

circuit TEXT,

case_type TEXT,

court TEXT,

subject TEXT,

session_date TEXT,

decision_date TEXT,

reason TEXT,

notes TEXT,

judgment_result TEXT,

mobile TEXT,

status TEXT DEFAULT 'متداولة'
)
""")

conn.commit()

# =====================
# رأس الصفحة
# =====================

st.markdown("""
# ⚖️ الهيئة القومية للتأمين الاجتماعى

## الإدارة العامة للشؤون القانونية

### إعداد

### وليد شعبان حماد

### ديوان عام منطقة البحيرة
""")

# =====================
# القائمة الرئيسية
# =====================

c1,c2,c3,c4,c5 = st.columns(5)

if "page" not in st.session_state:
    st.session_state.page="cases"

with c1:
    if st.button("إدارة القضايا"):
        st.session_state.page="cases"

with c2:
    if st.button("التنبيهات"):
        st.session_state.page="alerts"

with c3:
    if st.button("التقارير"):
        st.session_state.page="reports"

with c4:
    if st.button("أرشيف القضايا"):
        st.session_state.page="archive"

with c5:
    if st.button("البحث عن دعوى"):
        st.session_state.page="search"

page = st.session_state.page
# =====================
# إدارة القضايا
# =====================
def create_word_report(df):

    doc = Document()

    doc.add_heading(
        "الهيئة القومية للتأمين الاجتماعى",
        0
    )

    doc.add_paragraph(
        "الإدارة القانونية منطقة البحيرة"
    )

    table = doc.add_table(
        rows=1,
        cols=len(df.columns)
    )

    hdr = table.rows[0].cells

    for i,col in enumerate(df.columns):
        hdr[i].text = str(col)

    for _, row in df.iterrows():

        cells = table.add_row().cells

        for i,val in enumerate(row):
            cells[i].text = str(val)

    doc.save("report.docx")


def create_pdf_report(df):

    pdf = SimpleDocTemplate(
        "report.pdf"
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "الهيئة القومية للتأمين الاجتماعى",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            "الإدارة القانونية منطقة البحيرة",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1,12)
    )

    for _, row in df.iterrows():

        txt = " | ".join(
            [str(x) for x in row]
        )

        content.append(
            Paragraph(
                txt,
                styles["BodyText"]
            )
        )

    pdf.build(content)
if page == "cases":

    st.header("📂 تسجيل القضايا")

    claimant_type = st.selectbox(
        "صفة الخصم الأول",
        [
            "المدعى",
            "المستأنف",
            "الطاعن"
        ]
    )

    claimant = st.text_input(
        "اسم المدعى / المستأنف / الطاعن"
    )

    defendant_type = st.selectbox(
        "صفة الخصم الثاني",
        [
            "المدعى عليه",
            "المستأنف ضده",
            "المطعون ضده"
        ]
    )

    defendant = st.text_input(
        "اسم المدعى عليه / المستأنف ضده / المطعون ضده"
    )

    case_no = st.text_input(
        "رقم الدعوى"
    )

    judicial_year = st.text_input(
        "السنة القضائية"
    )

    circuit = st.text_input(
        "الدائرة"
    )

    case_type = st.text_input(
        "النوع"
    )

    court = st.selectbox(
        "المحكمة",
        [
            "الابتدائية",
            "الاستئناف",
            "النقض",
            "إدارية",
            "قضاء إدارى",
            "إدارية عليا"
        ]
    )

    subject = st.text_area(
        "موضوع الدعوى"
    )

    session_date = st.date_input(
        "تاريخ الجلسة"
    )

    decision_date = st.date_input(
        "تاريخ القرار"
    )

    reason = st.text_area(
        "السبب"
    )

    notes = st.text_area(
        "ملاحظات"
    )

    judgment_result = st.selectbox(
        "نتيجة الحكم",
        [
            "متداولة",
            "لصالح الهيئة",
            "ضد الهيئة"
        ]
    )

    mobile = st.text_input(
        "رقم الموبايل لإرسال التنبيهات"
    )

    if st.button("💾 حفظ القضية"):

        cur.execute(
        """
        INSERT INTO cases(

        claimant_type,
        claimant,

        defendant_type,
        defendant,

        case_no,
        judicial_year,

        circuit,

        case_type,

        court,

        subject,

        session_date,

        decision_date,

        reason,

        notes,

        judgment_result,

        mobile

        )

        VALUES(

        ?,?,?,?,?,?,
        ?,?,?,?,
        ?,?,?,?,
        ?,?

        )
        """,

        (

        claimant_type,
        claimant,

        defendant_type,
        defendant,

        case_no,
        judicial_year,

        circuit,

        case_type,

        court,

        subject,

        str(session_date),

        str(decision_date),

        reason,

        notes,

        judgment_result,

        mobile

        )

        )

        conn.commit()

        st.success(
            "تم حفظ القضية بنجاح"
        )

    st.divider()

    st.subheader("القضايا المسجلة")

    df = pd.read_sql(
        """
        SELECT *
        FROM cases
        ORDER BY id DESC
        """,
        conn
    )

    st.dataframe(
        df,
        use_container_width=True
    )
# =====================
# التنبيهات
# =====================

elif page == "alerts":

    st.header("🔔 التنبيهات")

    df = pd.read_sql(
        "SELECT * FROM cases",
        conn
    )

    today = datetime.now().date()

    st.subheader("📅 الجلسات خلال أسبوع")

    found = False

    for _, row in df.iterrows():

        try:

            session_date = datetime.strptime(
                row["session_date"],
                "%Y-%m-%d"
            ).date()

            days_left = (
                session_date - today
            ).days

            if 0 <= days_left <= 7:

                found = True

                st.error(
                    f"⬅️ هاااام عندك جلسة يوم {session_date} "
                    f"رقم الدعوى {row['case_no']} "
                    f"باقي {days_left} يوم"
                )

        except:
            pass

    if not found:
        st.success(
            "لا توجد جلسات خلال الأسبوع القادم"
        )

    st.divider()

    st.subheader(
        "⚠️ الأحكام الصادرة ضد الهيئة وقرب انتهاء الطعن"
    )

    found = False

    for _, row in df.iterrows():

        try:

            if row["judgment_result"] == "ضد الهيئة":

                decision_date = datetime.strptime(
                    row["decision_date"],
                    "%Y-%m-%d"
                ).date()

                appeal_date = (
                    decision_date +
                    timedelta(days=40)
                )

                remaining = (
                    appeal_date - today
                ).days

                if 0 <= remaining <= 15:

                    found = True

                    st.error(
                        f"⬅️ هاااام آخر ميعاد للطعن "
                        f"{appeal_date} "
                        f"دعوى رقم {row['case_no']} "
                        f"متبقي {remaining} يوم"
                    )

        except:
            pass

    if not found:

        st.success(
            "لا توجد مواعيد طعن قريبة"
        )


# =====================
# أرشيف القضايا
# =====================

elif page == "archive":

    st.header(
        "📁 أرشيف القضايا المنتهية"
    )

    cur.execute("""
    UPDATE cases
    SET status='منتهية'
    WHERE judgment_result
    IN (
    'لصالح الهيئة',
    'ضد الهيئة'
    )
    """)

    conn.commit()

    archive = pd.read_sql(
        """
        SELECT *
        FROM cases
        WHERE status='منتهية'
        ORDER BY id DESC
        """,
        conn
    )

    st.dataframe(
        archive,
        use_container_width=True
                )
# =====================
# البحث
# =====================

elif page == "search":

    st.header("🔎 البحث عن دعوى")

    search_type = st.selectbox(
        "طريقة البحث",
        [
            "برقم وسنة الدعوى",
            "بالاسم"
        ]
    )

    if search_type == "برقم وسنة الدعوى":

        case_no = st.text_input(
            "رقم الدعوى"
        )

        judicial_year = st.text_input(
            "السنة القضائية"
        )

        if st.button("بحث"):

            result = pd.read_sql(
            f"""
            SELECT *
            FROM cases
            WHERE case_no='{case_no}'
            AND judicial_year='{judicial_year}'
            """,
            conn
            )

            st.dataframe(
                result,
                use_container_width=True
            )

    else:

        name = st.text_input(
            "اسم الخصم"
        )

        if st.button("بحث بالاسم"):

            result = pd.read_sql(
            f"""
            SELECT *
            FROM cases
            WHERE claimant LIKE '%{name}%'
            OR defendant LIKE '%{name}%'
            """,
            conn
            )

            st.dataframe(
                result,
                use_container_width=True
            )


# =====================
# التقارير
# =====================

elif page == "reports":

    st.header("📊 التقارير")

    report_type = st.selectbox(
        "نوع التقرير",
        [
            "تقرير بالدعاوى المتداولة",
            "تقرير بالأحكام الصادرة"
        ]
    )

    start_date = st.date_input(
        "من تاريخ"
    )

    end_date = st.date_input(
        "إلى تاريخ"
    )

    if report_type == "تقرير بالدعاوى المتداولة":

        if st.button("عرض التقرير"):

            report = pd.read_sql(
            f"""
            SELECT

            case_no AS 'رقم الدعوى',
            judicial_year AS 'السنة القضائية',
            circuit AS 'الدائرة',
            case_type AS 'النوع',
            claimant AS 'اسم المدعى',
            defendant AS 'اسم المدعى عليه',
            subject AS 'موضوع الدعوى',
            judgment_result AS 'آخر إجراء'

            FROM cases

            WHERE session_date
            BETWEEN '{start_date}'
            AND '{end_date}'
            """,
            conn
            )

            st.markdown("""
            ### الهيئة القومية للتأمين الاجتماعى

            #### الإدارة القانونية منطقة البحيرة

            ### بيان بالدعاوى المتداولة
            """)

            st.dataframe(
                report,
                use_container_width=True
            )

            csv = report.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "تحميل Excel",
                csv,
                "الدعاوى_المتداولة.csv",
                "text/csv"
            )

    else:

        result_filter = st.selectbox(
            "نتيجة الحكم",
            [
                "لصالح الهيئة",
                "ضد الهيئة",
                "الكل"
            ]
        )

        if st.button("عرض تقرير الأحكام"):

            query = """
            SELECT
            case_no,
            judicial_year,
            circuit,
            case_type,
            claimant,
            defendant,
            subject,
            decision_date,
            judgment_result
            FROM cases
            """

            if result_filter != "الكل":

                query += f"""
                WHERE judgment_result=
                '{result_filter}'
                """

            report = pd.read_sql(
                query,
                conn
            )

            st.markdown("""
            ### الهيئة القومية للتأمين الاجتماعى

            #### الإدارة القانونية منطقة البحيرة

            ### بيان الأحكام الصادرة
            """)

            st.dataframe(
                report,
                use_container_width=True
            )

            csv = report.to_csv(
                index=False
            ).encode("utf-8-sig")

            st.download_button(
                "تحميل Excel",
                csv,
                "الأحكام_الصادرة.csv",
                "text/csv"
            )
