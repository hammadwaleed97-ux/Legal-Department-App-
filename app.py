import streamlit as st

st.set_page_config(
    page_title="إدارة القضايا",
    page_icon="⚖️",
    layout="wide"
)

# =========================
# CSS
# =========================

st.markdown("""
<style>

.stApp{
    background-color:#062456;
}

.block-container{
    padding-top:5px;
}

.logo-box{
    text-align:center;
    color:white;
}

.logo-icon{
    font-size:60px;
    margin-top:25px;
    margin-bottom:10px;
}

.logo-main{
    font-size:30px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:20px;
}

.logo-sub{
    font-size:24px;
    font-weight:bold;
    white-space:nowrap;
    margin-bottom:45px;
}

.prepare{
    font-size:20px;
    margin-bottom:10px;
}

.name{
    font-size:32px;
    font-weight:bold;
    margin-bottom:15px;
}

.place{
    font-size:24px;
    font-weight:bold;
    margin-bottom:35px;
}

div.stButton > button{
    width:280px;
    height:70px;
    border-radius:18px;
    border:none;
    font-size:21px;
    font-weight:bold;
    margin:auto;
    display:block;
    background-color:#2f55d4;
    color:white;
}

div.stButton > button:hover{
    background-color:#4368e0;
    color:white;
}

</style>
""", unsafe_allow_html=True)

# =========================
# اللوجو
# =========================

st.markdown("""
<div class="logo-box">

<div class="logo-icon">
⚖️
</div>

<div class="logo-main">
الهيئة القومية للتأمين الاجتماعى
</div>

<div class="logo-sub">
الإدارة العامة للشؤون القانونية
</div>

<div class="prepare">
إعداد
</div>

<div class="name">
وليد شعبان حماد
</div>

<div class="place">
ديوان عام منطقة البحيرة
</div>

</div>
""", unsafe_allow_html=True)

# =========================
# القائمة الرئيسية
# =========================

col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.button("⚖️ تسجيل القضايا")

    st.button("🔔 التنبيهات")

    st.button("📊 التقارير")

    st.button("📂 أرشيف القضايا")

    st.button("🔍 البحث عن دعوى")

    st.button("❌ القضايا المحذوفة")
# =====================================
# إنشاء جدول القضايا
# =====================================

cur.execute("""
CREATE TABLE IF NOT EXISTS cases(

id INTEGER PRIMARY KEY AUTOINCREMENT,

litigation_type TEXT,

claimant_type TEXT,
claimant TEXT,

defendant_type TEXT,
defendant TEXT,

case_no TEXT,

judicial_year TEXT,

circuit TEXT,

case_type TEXT,

court TEXT,

court_name TEXT,

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

# =====================================
# تسجيل القضايا
# =====================================

if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "cases":

    st.markdown("""
    <h2 style='color:white;text-align:center'>
    ⚖️ تسجيل القضايا
    </h2>
    """, unsafe_allow_html=True)

    litigation_type = st.selectbox(
        "نوع الإجراء",
        [
            "دعوى",
            "استئناف",
            "نقض"
        ]
    )

    claimant_type = st.selectbox(
        "صفة الخصم الأول",
        [
            "المدعى",
            "المستأنف",
            "الطاعن"
        ]
    )

    claimant = st.text_input(
        "اسم الخصم الأول"
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
        "اسم الخصم الثاني"
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

    court_name = st.text_input(
        "اسم المحكمة"
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
        "نتيجة الدعوى",
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

        cur.execute("""

        INSERT INTO cases(

        litigation_type,

        claimant_type,
        claimant,

        defendant_type,
        defendant,

        case_no,

        judicial_year,

        circuit,

        case_type,

        court,

        court_name,

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
        ?,?,?,?,?,?,
        ?,?,?,?,?,?,?

        )

        """,

        (

        litigation_type,

        claimant_type,
        claimant,

        defendant_type,
        defendant,

        case_no,

        judicial_year,

        circuit,

        case_type,

        court,

        court_name,

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
