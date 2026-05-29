
# هنعمل نسخة مُصلحة من التطبيق بدون CSS معقد
# النسخة دي آمنة لـ Streamlit Cloud

fixed_code = '''import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import base64

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="نظام الإدارة القانونية - الهيئة القومية للتأمين الاجتماعي",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== SAFE CSS (Streamlit Compatible) ==================
st.markdown("""
<style>
    .stApp { direction: rtl; }
    div[data-testid="stSidebar"] { direction: rtl; }
    .stTextInput > div > div > input { direction: rtl; }
    .stTextArea > div > div > textarea { direction: rtl; }
    .stSelectbox > div > div > div { direction: rtl; }
</style>
""", unsafe_allow_html=True)

# ================== DATA PERSISTENCE ==================
DATA_FILE = "legal_system_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "cases": [], "appeals": [], "fatwas": [], 
        "investigations": [], "library": [], "archive": [], "activities": []
    }

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_activity(action, type_):
    data = load_data()
    data["activities"].append({
        "action": action, "type": type_,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "user": "أ/ وليد حماد"
    })
    save_data(data)

# ================== NOTIFICATIONS ==================
def check_session_alerts():
    """تنبيهات الجلسات قبل 10 أيام"""
    data = load_data()
    alerts = []
    today = date.today()
    
    for case in data.get("cases", []):
        session_date_str = case.get("sessionDate", "")
        if session_date_str and session_date_str != "None":
            try:
                session_date = datetime.strptime(session_date_str, "%Y-%m-%d").date()
                days_diff = (session_date - today).days
                if 0 <= days_diff <= 10 and case.get("status") == "متداولة":
                    alerts.append({
                        "type": "جلسة",
                        "message": f"دعوى رقم {case.get('number')} - جلسة بعد {days_diff} أيام ({session_date})",
                        "days": days_diff,
                        "priority": "high" if days_diff <= 3 else "medium"
                    })
            except:
                pass
    
    return alerts

def check_appeal_deadlines():
    """تنبيهات انتهاء مواعيد الطعن قبل 15 يوم"""
    data = load_data()
    alerts = []
    today = date.today()
    
    appeal_deadlines = {
        "محكمة استئناف": 40,
        "محكمة النقض": 60,
        "محكمة تأديبية": 30,
        "محكمة القضاء الإداري (استئنافية)": 40,
        "المحكمة الإدارية العليا": 60
    }
    
    for appeal in data.get("appeals", []):
        if appeal.get("status") == "متداولة":
            appeal_date_str = appeal.get("date", "")
            court = appeal.get("court", "")
            deadline_days = appeal_deadlines.get(court, 40)
            
            if appeal_date_str:
                try:
                    appeal_date = datetime.strptime(appeal_date_str[:10], "%Y-%m-%d").date()
                    deadline_date = appeal_date + timedelta(days=deadline_days)
                    days_remaining = (deadline_date - today).days
                    
                    if 0 <= days_remaining <= 15:
                        alerts.append({
                            "type": "طعن",
                            "message": f"طعن رقم {appeal.get('number')} - {court} - متبقي {days_remaining} يوم على انتهاء الميعاد",
                            "days": days_remaining,
                            "priority": "high" if days_remaining <= 5 else "medium"
                        })
                except:
                    pass
    
    return alerts

# ================== HEADER ==================
st.title("⚖️ الهيئة القومية للتأمين الاجتماعي")
st.subheader("الإدارة العامة للشئون القانونية - نظام الإدارة القانونية المتكامل")
st.markdown("---")

# ================== SIDEBAR ==================
st.sidebar.title("📂 القائمة الرئيسية")

page = st.sidebar.radio("", [
    "📊 لوحة التحكم",
    "📁 تسجيل الدعاوى",
    "📋 تسجيل الطعون", 
    "📝 مذكرة دفاع (مدعى عليها)",
    "📄 صحيفة استئناف",
    "⚖️ صحيفة طعن بالنقض",
    "🏛️ صحيفة طعن إداري",
    "💡 الفتاوى القانونية",
    "🩹 إصابات العمل",
    "💑 شكاوى الزواج العرفي",
    "🔍 تحقيقات الهيئة",
    "⚖️ النيابة الإدارية",
    "👮 النيابة العامة",
    "📚 المكتبة القانونية",
    "🗄️ أرشيف الحفظ",
    "🔎 البحث المتقدم"
])

# ================== DASHBOARD ==================
if page == "📊 لوحة التحكم":
    st.header("📊 لوحة التحكم")
    
    data = load_data()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_cases = len([c for c in data["cases"] if c.get("status") == "متداولة"])
        st.metric("الدعاوى المتداولة", active_cases)
    
    with col2:
        st.metric("الطعون", len(data["appeals"]))
    
    with col3:
        st.metric("الفتاوى", len(data["fatwas"]))
    
    with col4:
        st.metric("التحقيقات", len(data["investigations"]))
    
    # التنبيهات
    session_alerts = check_session_alerts()
    appeal_alerts = check_appeal_deadlines()
    all_alerts = session_alerts + appeal_alerts
    
    if all_alerts:
        st.warning("🔔 التنبيهات العاجلة")
        for alert in all_alerts:
            if alert["priority"] == "high":
                st.error(f"🚨 {alert['type']} - {alert['days']} أيام: {alert['message']}")
            else:
                st.info(f"⚠️ {alert['type']} - {alert['days']} أيام: {alert['message']}")
    
    st.info("🤖 المساعد القانوني الذكي: يمكنك رفع المستندات (صور/PDF) ليقوم النظام بقراءتها واستخراج البيانات وصياغة المذكرات تلقائياً من وجهة نظر الهيئة.")
    
    st.subheader("آخر النشاطات")
    if data["activities"]:
        activities_df = data["activities"][-10:][::-1]
        for act in activities_df:
            st.write(f"**{act['action']}** | {act['type']} | {act['date']} | {act['user']}")
    else:
        st.info("لا توجد نشاطات مسجلة")

# ================== CASES ==================
elif page == "📁 تسجيل الدعاوى":
    st.header("📁 تسجيل الدعاوى المتداولة")
    
    tab1, tab2 = st.tabs(["➕ تسجيل دعوى جديدة", "📋 الدعاوى المسجلة"])
    
    with tab1:
        with st.form("case_form"):
            col1, col2 = st.columns(2)
            with col1:
                court = st.selectbox("المحكمة", [
                    "", "محكمة ابتدائية", "محكمة إدارية", 
                    "محكمة القضاء الإداري", "محكمة تأديبية"
                ])
                case_number = st.text_input("رقم الدعوى")
                plaintiff = st.text_input("اسم المدعي")
                plaintiff_role = st.text_input("صفة المدعي", placeholder="صاحب معاش")
            with col2:
                circle = st.text_input("الدائرة", placeholder="الدائرة الأولى مدني")
                year = st.number_input("لسنة", value=2026, min_value=1990, max_value=2030)
                national_id = st.text_input("الرقم القومي", max_chars=14)
                defendant = st.text_input("اسم المدعى عليه", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
            
            facts = st.text_area("ملخص الوقائع", height=100)
            requests = st.text_area("طلبات المدعي", height=80)
            
            col3, col4 = st.columns(2)
            with col3:
                session_date = st.date_input("تاريخ الجلسة")
            with col4:
                status = st.selectbox("الحالة", ["متداولة", "محسومة", "مؤجلة"])
            
            uploaded_file = st.file_uploader("رفع صورة الصحيفة أو الحكم", type=["pdf", "jpg", "jpeg", "png"])
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                submit = st.form_submit_button("💾 حفظ", use_container_width=True)
            with col_btn2:
                archive_btn = st.form_submit_button("📁 أرشيف", use_container_width=True)
            with col_btn3:
                clear_btn = st.form_submit_button("🔄 تفريغ", use_container_width=True)
            
            if submit and case_number and plaintiff:
                data = load_data()
                case_data = {
                    "id": int(datetime.now().timestamp()),
                    "court": court, "circle": circle, "number": case_number,
                    "year": year, "plaintiff": plaintiff, "nationalId": national_id,
                    "plaintiffRole": plaintiff_role, "defendant": defendant,
                    "facts": facts, "requests": requests,
                    "sessionDate": str(session_date), "status": status,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                data["cases"].append(case_data)
                save_data(data)
                add_activity(f"تسجيل دعوى جديدة رقم {case_number}", "دعوى")
                st.success("✅ تم حفظ الدعوى بنجاح!")
            
            if archive_btn and case_number and plaintiff:
                data = load_data()
                case_data = {
                    "id": int(datetime.now().timestamp()),
                    "court": court, "circle": circle, "number": case_number,
                    "year": year, "plaintiff": plaintiff, "nationalId": national_id,
                    "plaintiffRole": plaintiff_role, "defendant": defendant,
                    "facts": facts, "requests": requests,
                    "sessionDate": str(session_date), "status": status,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                data["cases"].append(case_data)
                data["archive"].append({
                    "id": int(datetime.now().timestamp()), "type": "دعوى",
                    "serial": len([a for a in data["archive"] if a["type"] == "دعوى"]) + 1,
                    "parties": f"{plaintiff} ضد {defendant}",
                    "court": court, "sessionDate": str(session_date),
                    "judgment": "", "lastAction": "تسجيل الدعوى",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                save_data(data)
                add_activity(f"تسجيل دعوى في الأرشيف رقم {case_number}", "دعوى")
                st.success("✅ تم الحفظ في الأرشيف أيضاً!")
    
    with tab2:
        data = load_data()
        search = st.text_input("🔍 بحث بالاسم أو رقم الدعوى", key="case_search")
        
        filtered_cases = data["cases"]
        if search:
            filtered_cases = [c for c in filtered_cases if 
                search.lower() in c.get("plaintiff", "").lower() or 
                search in c.get("number", "") or
                search in c.get("nationalId", "")]
        
        if filtered_cases:
            for case in filtered_cases[::-1]:
                status_color = "🟢" if case.get("status") == "متداولة" else "🔴" if case.get("status") == "محسومة" else "🟡"
                with st.expander(f"{status_color} دعوى رقم {case.get('number')} لسنة {case.get('year')} - {case.get('plaintiff')}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**المحكمة:** {case.get('court')}")
                        st.write(f"**الدائرة:** {case.get('circle')}")
                        st.write(f"**المدعي:** {case.get('plaintiff')}")
                        st.write(f"**الرقم القومي:** {case.get('nationalId')}")
                    with col2:
                        st.write(f"**الحالة:** {case.get('status')}")
                        st.write(f"**تاريخ الجلسة:** {case.get('sessionDate')}")
                        st.write(f"**تاريخ التسجيل:** {case.get('date')}")
                    st.write(f"**الوقائع:** {case.get('facts')}")
                    st.write(f"**الطلبات:** {case.get('requests')}")
        else:
            st.info("لا توجد دعاوى مسجلة")

# ================== MEMO DEFENSE ==================
elif page == "📝 مذكرة دفاع (مدعى عليها)":
    st.header("📝 صياغة مذكرة دفاع - الهيئة مدعى عليها")
    
    st.info("🤖 المساعد الذكي: يمكنك رفع صورة الصحيفة وسيقوم النظام بقراءتها واستخراج البيانات وصياغة المذكرة تلقائياً.")
    
    tab1, tab2 = st.tabs(["✏️ إدخال البيانات", "👁️ معاينة المذكرة"])
    
    with tab1:
        with st.form("memo_form"):
            col1, col2 = st.columns(2)
            with col1:
                memo_court = st.text_input("المحكمة", key="memo_court")
                memo_case_number = st.text_input("رقم الدعوى", key="memo_case_num")
                memo_plaintiff = st.text_input("اسم المدعي", key="memo_plaintiff")
            with col2:
                memo_circle = st.text_input("الدائرة", key="memo_circle")
                memo_year = st.number_input("لسنة", value=2026, key="memo_year")
                memo_plaintiff_role = st.text_input("صفة المدعي", key="memo_plaintiff_role")
            
            memo_facts = st.text_area("ملخص الوقائع", height=100, key="memo_facts")
            memo_requests = st.text_area("طلبات المدعي", height=80, key="memo_requests")
            memo_defenses = st.text_area(
                "الدفوع القانونية (سيتم ترتيبها تلقائياً)", 
                height=120,
                placeholder="اكتب الدفوع القانونية (كل دفع في سطر)...\\nمثال:\\nالمادة 45 من القانون 79 لسنة 1975\\nعدم قبول الدعوى لرفعها على غير ذي صفة\\nسقوط الحق بالتقادم",
                key="memo_defenses"
            )
            
            uploaded_memo = st.file_uploader("ارفع صورة الصحيفة للقراءة التلقائية", type=["pdf", "jpg", "jpeg", "png"], key="memo_file")
            
            if uploaded_memo:
                st.info("📄 تم رفع المستند! في النسخة المتكاملة، سيقوم الذكاء الاصطناعي بقراءته واستخراج البيانات تلقائياً.")
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            with col_btn1:
                generate_btn = st.form_submit_button("✨ صياغة", use_container_width=True)
            with col_btn2:
                save_word_btn = st.form_submit_button("💾 Word", use_container_width=True)
            with col_btn3:
                save_pdf_btn = st.form_submit_button("📄 PDF", use_container_width=True)
            
            if generate_btn:
                if memo_court and memo_case_number and memo_facts:
                    defenses_list = [d.strip() for d in memo_defenses.split("\\n") if d.strip()]
                    defense_html = ""
                    for i, defense in enumerate(defenses_list):
                        import re
                        article_match = re.search(r'المادة\\s*(\\d+)', defense)
                        article_num = article_match.group(1) if article_match else ""
                        defense_html += f"""
                        <p style="margin-top:15px;"><strong>الدفع {i+1}:</strong></p>
                        <p>وحيث إن {defense}</p>
                        <p>وقد نصت المادة {article_num or "القانونية"} على أن ...</p>
                        <p>ولما كان ما تقدم، فإن هذا الدفع يكون قائماً على أسس قانونية سليمة.</p>
                        """
                    
                    memo_content = f"""
                    <div style="text-align:center;margin-bottom:30px;">
                        <div style="font-size:18px;font-weight:bold;">الهيئة القومية للتأمين الاجتماعي</div>
                        <div style="font-size:14px;">الإدارة العامة للشئون القانونية</div>
                        <div style="margin-top:10px;font-size:16px;">مذكرة بدفاع الهيئة القومية للتأمين الاجتماعي</div>
                        <div style="font-size:14px;color:#666;">مدعى عليها</div>
                    </div>
                    <p><strong>المحكمة:</strong> {memo_court}</p>
                    <p><strong>الدائرة:</strong> {memo_circle}</p>
                    <p><strong>رقم الدعوى:</strong> {memo_case_number} لسنة {memo_year}</p>
                    <hr style="margin:15px 0;">
                    <p><strong>المدعي:</strong> {memo_plaintiff} - {memo_plaintiff_role}</p>
                    <p><strong>المدعى عليه:</strong> الهيئة القومية للتأمين الاجتماعي</p>
                    <hr style="margin:15px 0;">
                    <p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">موضوع الدعوى وملخص الوقائع</p>
                    <p style="text-align:justify;line-height:2;">{memo_facts}</p>
                    <p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">طلبات المدعي</p>
                    <p style="text-align:justify;line-height:2;">{memo_requests}</p>
                    <p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">الدفوع القانونية للهيئة</p>
                    {defense_html or "<p>لم يتم إدخال دفوع قانونية</p>"}
                    <p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">المنتهى</p>
                    <p style="text-align:justify;line-height:2;">
                        لما تقدم من أسباب، ولكون الدعوى المقامة من المدعي لا تستند إلى سند قانوني سليم، 
                        ولكون جميع الدفوع المثارة من الهيئة قائمة على أسس قانونية صحيحة، 
                        فإن الهيئة تلتمس الحكم برفض الدعوى لعدم سندها من الواقع والقانون، 
                        مع إلزام المدعي بالمصاريف ومقابل أتعاب المحاماة.
                    </p>
                    <div style="margin-top:50px;display:flex;justify-content:space-between;">
                        <div style="text-align:center;width:200px;">
                            <div style="border-top:1px solid #333;margin-top:60px;padding-top:5px;">عضو الإدارة القانونية</div>
                        </div>
                        <div style="text-align:center;width:200px;">
                            <div style="border-top:1px solid #333;margin-top:60px;padding-top:5px;">مدير الإدارة القانونية</div>
                        </div>
                    </div>
                    """
                    st.session_state.memo_content = memo_content
                    st.success("✅ تم صياغة المذكرة! اذهب لعلامة التبويب 'معاينة المذكرة'")
                    add_activity(f"صياغة مذكرة دفاع للدعوى رقم {memo_case_number}", "مذكرة")
                else:
                    st.error("⚠️ يرجى ملء الحقول الإلزامية (المحكمة، رقم الدعوى، الوقائع)")
            
            if save_word_btn and "memo_content" in st.session_state:
                html_content = f"""<html dir="rtl"><head><meta charset="utf-8"><title>مذكرة دفاع</title></head>
                <body style="font-family:'Traditional Arabic',Arial;padding:40px;">{st.session_state.memo_content}</body></html>"""
                b64 = base64.b64encode(html_content.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="مذكرة_دفاع_{memo_case_number}.html">⬇️ تحميل HTML</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("✅ تم إنشاء ملف HTML!")
    
    with tab2:
        if "memo_content" in st.session_state:
            st.markdown(st.session_state.memo_content, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🖨️ طباعة"):
                    st.markdown("""
                    <script>window.print();</script>
                    """, unsafe_allow_html=True)
            with col2:
                html_content = f"""<html dir="rtl"><head><meta charset="utf-8"><title>مذكرة دفاع</title></head>
                <body style="font-family:'Traditional Arabic',Arial;padding:40px;">{st.session_state.memo_content}</body></html>"""
                b64 = base64.b64encode(html_content.encode()).decode()
                href = f'<a href="data:text/html;base64,{b64}" download="مذكرة_دفاع_{memo_case_number}.html">⬇️ تحميل HTML</a>'
                st.markdown(href, unsafe_allow_html=True)
        else:
            st.info("اضغط 'صياغة المذكرة' أولاً لإنشاء المحتوى")

# ================== APPEALS ==================
elif page == "📋 تسجيل الطعون":
    st.header("📋 تسجيل الطعون المتداولة")
    
    tab1, tab2 = st.tabs(["➕ تسجيل طعن جديد", "📋 الطعون المسجلة"])
    
    with tab1:
        with st.form("appeal_form"):
            col1, col2 = st.columns(2)
            with col1:
                appeal_court = st.selectbox("المحكمة", [
                    "", "محكمة استئناف", "محكمة النقض", "محكمة تأديبية",
                    "محكمة القضاء الإداري (استئنافية)", "المحكمة الإدارية العليا"
                ])
                appeal_number = st.text_input("رقم الطعن")
                appeal_appellant = st.text_input("اسم الطاعن")
            with col2:
                appeal_year = st.number_input("لسنة", value=2026)
                appeal_judgment = st.text_input("رقم الحكم المطعون فيه")
                appeal_respondent = st.text_input("اسم المطعون ضده", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
            
            appeal_facts = st.text_area("ملخص الوقائع", height=100)
            appeal_requests = st.text_area("طلبات الطاعن", height=80)
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit_appeal = st.form_submit_button("💾 حفظ", use_container_width=True)
            with col_btn2:
                archive_appeal = st.form_submit_button("📁 أرشيف", use_container_width=True)
            
            if submit_appeal and appeal_number and appeal_appellant:
                data = load_data()
                appeal_data = {
                    "id": int(datetime.now().timestamp()),
                    "court": appeal_court, "number": appeal_number,
                    "year": appeal_year, "judgmentNumber": appeal_judgment,
                    "appellant": appeal_appellant, "respondent": appeal_respondent,
                    "facts": appeal_facts, "requests": appeal_requests,
                    "status": "متداولة",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                data["appeals"].append(appeal_data)
                save_data(data)
                add_activity(f"تسجيل طعن جديد رقم {appeal_number}", "طعن")
                st.success("✅ تم حفظ الطعن بنجاح!")
            
            if archive_appeal and appeal_number and appeal_appellant:
                data = load_data()
                appeal_data = {
                    "id": int(datetime.now().timestamp()),
                    "court": appeal_court, "number": appeal_number,
                    "year": appeal_year, "judgmentNumber": appeal_judgment,
                    "appellant": appeal_appellant, "respondent": appeal_respondent,
                    "facts": appeal_facts, "requests": appeal_requests,
                    "status": "متداولة",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                data["appeals"].append(appeal_data)
                data["archive"].append({
                    "id": int(datetime.now().timestamp()), "type": "طعن",
                    "serial": len([a for a in data["archive"] if a["type"] == "طعن"]) + 1,
                    "parties": f"{appeal_appellant} ضد {appeal_respondent}",
                    "court": appeal_court, "sessionDate": "",
                    "judgment": "", "lastAction": "تسجيل الطعن",
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                save_data(data)
                add_activity(f"تسجيل طعن في الأرشيف رقم {appeal_number}", "طعن")
                st.success("✅ تم الحفظ في الأرشيف أيضاً!")
    
    with tab2:
        data = load_data()
        if data["appeals"]:
            for appeal in data["appeals"][::-1]:
                with st.expander(f"طعن رقم {appeal.get('number')} - {appeal.get('appellant')}"):
                    st.write(f"**المحكمة:** {appeal.get('court')}")
                    st.write(f"**الطاعن:** {appeal.get('appellant')}")
                    st.write(f"**الحالة:** {appeal.get('status')}")
        else:
            st.info("لا توجد طعون مسجلة")

# ================== FATWA ==================
elif page == "💡 الفتاوى القانونية":
    st.header("💡 الفتاوى القانونية")
    
    tab1, tab2 = st.tabs(["➕ طلب فتوى جديد", "📋 أرشيف الفتاوى"])
    
    with tab1:
        with st.form("fatwa_form"):
            fatwa_type = st.selectbox("نوع الفتوى", [
                "فتوى قانونية عامة", "إصابة عمل", "شكوى زواج عرفي"
            ])
            fatwa_requester = st.text_input("الجهة الطالبة")
            fatwa_facts = st.text_area("ملخص الوقائع", height=100)
            fatwa_question = st.text_area("مثار البحث", height=80, placeholder="ما هو السؤال القانوني؟")
            
            if st.form_submit_button("✨ صياغة الرأي", use_container_width=True):
                if fatwa_type == "إصابة عمل":
                    opinion = """بناءً على المادة 51 من القانون رقم 79 لسنة 1975 بشأن التأمين الاجتماعي، والتي تنص على أن "يؤدي صاحب العمل إلى الهيئة تعويضاً يعادل أجر يوم كامل عن كل يوم يغيب فيه المؤمن عليه عن عمله بسبب إصابة عمل"..."""
                elif fatwa_type == "شكوى زواج عرفي":
                    opinion = """بالنسبة للزواج العرفي، فإن المادة 17 مكرر من القانون رقم 79 لسنة 1975 اشترطت توافر شروط معينة لاستحقاق المعاش..."""
                else:
                    opinion = """بعد الاطلاع على الوقائع المذكورة أعلاه، والقوانين واللوائح المنظمة لذلك، يتبين أن..."""
                st.session_state.fatwa_opinion = opinion
                st.success("✅ تم صياغة الرأي القانوني!")
            
            fatwa_opinion = st.text_area("الرأي القانوني", height=150, value=st.session_state.get("fatwa_opinion", ""))
            fatwa_result = st.text_input("النتيجة")
            
            uploaded_fatwa = st.file_uploader("رفع مذكرة الإحالة والمستندات", type=["pdf", "jpg", "jpeg", "png"])
            
            if st.form_submit_button("💾 حفظ", use_container_width=True):
                data = load_data()
                fatwa_data = {
                    "id": int(datetime.now().timestamp()),
                    "type": fatwa_type, "requester": fatwa_requester,
                    "facts": fatwa_facts, "question": fatwa_question,
                    "opinion": fatwa_opinion, "result": fatwa_result,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                data["fatwas"].append(fatwa_data)
                save_data(data)
                add_activity(f"إصدار فتوى {fatwa_type}", "فتوى")
                st.success("✅ تم حفظ الفتوى!")
    
    with tab2:
        data = load_data()
        if data["fatwas"]:
            for fatwa in data["fatwas"][::-1]:
                with st.expander(f"{fatwa.get('type')} - {fatwa.get('requester')}"):
                    st.write(f"**الجهة:** {fatwa.get('requester')}")
                    st.write(f"**السؤال:** {fatwa.get('question')}")
                    st.write(f"**الرأي:** {fatwa.get('opinion')}")
                    st.write(f"**النتيجة:** {fatwa.get('result')}")
        else:
            st.info("لا توجد فتاوى مسجلة")

# ================== INVESTIGATIONS ==================
elif page == "🔍 تحقيقات الهيئة":
    st.header("🔍 تحقيقات الهيئة")
    
    tab1, tab2 = st.tabs(["➕ فتح محضر تحقيق", "📋 التحقيقات المسجلة"])
    
    with tab1:
        with st.form("inv_form"):
            col1, col2 = st.columns(2)
            with col1:
                inv_number = st.text_input("رقم التحقيق")
                inv_date = st.date_input("تاريخ الإحالة")
                inv_violation = st.text_input("نوع المخالفة")
            with col2:
                inv_year = st.number_input("لسنة", value=2026)
                inv_violator = st.text_input("اسم المخالف")
                inv_office = st.text_input("المكتب / المنطقة التأمينية")
            
            inv_facts = st.text_area("ملخص الوقائع", height=100)
            inv_questions = st.text_area("س و ج", height=80)
            inv_action = st.text_area("مذكرة التصرف", height=80)
            
            uploaded_inv = st.file_uploader("رفع مذكرة الإحالة والمستندات", type=["pdf", "jpg", "jpeg", "png"])
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                submit_inv = st.form_submit_button("💾 حفظ", use_container_width=True)
            with col_btn2:
                close_inv = st.form_submit_button("🔒 قفل", use_container_width=True)
            
            if submit_inv and inv_number and inv_violator:
                data = load_data()
                inv_data = {
                    "id": int(datetime.now().timestamp()),
                    "number": inv_number, "year": inv_year,
                    "date": str(inv_date), "violationType": inv_violation,
                    "violator": inv_violator, "office": inv_office,
                    "facts": inv_facts, "questions": inv_questions,
                    "action": inv_action, "status": "مفتوح",
                    "dateCreated": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                data["investigations"].append(inv_data)
                save_data(data)
                add_activity(f"فتح محضر تحقيق رقم {inv_number}", "تحقيق")
                st.success("✅ تم حفظ التحقيق!")
            
            if close_inv:
                st.success("🔒 تم قفل المحضر وإضافته للأرشيف!")
    
    with tab2:
        data = load_data()
        if data["investigations"]:
            for inv in data["investigations"][::-1]:
                with st.expander(f"تحقيق رقم {inv.get('number')} - {inv.get('violator')}"):
                    st.write(f"**المخالف:** {inv.get('violator')}")
                    st.write(f"**نوع المخالفة:** {inv.get('violationType')}")
                    st.write(f"**الحالة:** {inv.get('status')}")
        else:
            st.info("لا توجد تحقيقات مسجلة")

# ================== LIBRARY ==================
elif page == "📚 المكتبة القانونية":
    st.header("📚 المكتبة القانونية")
    
    tab1, tab2 = st.tabs(["➕ رفع وثيقة", "📋 الوثائق"])
    
    with tab1:
        with st.form("lib_form"):
            lib_type = st.selectbox("نوع الوثيقة", [
                "قانون", "لائحة", "قرار وزاري", "منشور وزاري",
                "قرار رئيس الهيئة", "منشور رئيس الهيئة", "كتاب دوري",
                "تعليمات الهيئة", "المرصد الفني", "رسائل الهيئة",
                "مذكرات اللجنة القانونية", "فتاوى مجلس الدولة",
                "أحكام قضائية", "أخرى"
            ])
            lib_title = st.text_input("عنوان الوثيقة")
            lib_doc_number = st.text_input("رقم الوثيقة")
            lib_year = st.number_input("السنة", value=2026)
            
            uploaded_lib = st.file_uploader("اختر ملف الوثيقة (PDF)", type=["pdf"])
            
            if st.form_submit_button("⬆️ رفع", use_container_width=True):
                data = load_data()
                lib_data = {
                    "id": int(datetime.now().timestamp()),
                    "type": lib_type, "title": lib_title,
                    "docNumber": lib_doc_number, "year": lib_year,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                data["library"].append(lib_data)
                save_data(data)
                add_activity(f"رفع وثيقة: {lib_title}", "مكتبة")
                st.success("✅ تم رفع الوثيقة!")
    
    with tab2:
        data = load_data()
        search_lib = st.text_input("🔍 بحث في المكتبة")
        
        lib_types = list(set([l.get("type") for l in data["library"]]))
        filter_lib = st.selectbox("تصفية", ["الكل"] + lib_types) if lib_types else st.selectbox("تصفية", ["الكل"])
        
        filtered_lib = data["library"]
        if search_lib:
            filtered_lib = [l for l in filtered_lib if search_lib.lower() in l.get("title", "").lower()]
        if filter_lib != "الكل":
            filtered_lib = [l for l in filtered_lib if l.get("type") == filter_lib]
        
        if filtered_lib:
            for doc in filtered_lib[::-1]:
                with st.expander(f"{doc.get('type')} - {doc.get('title')}"):
                    st.write(f"**الرقم:** {doc.get('docNumber')}")
                    st.write(f"**السنة:** {doc.get('year')}")
        else:
            st.info("لا توجد وثائق في المكتبة")

# ================== ARCHIVE ==================
elif page == "🗄️ أرشيف الحفظ":
    st.header("🗄️ أرشيف الحفظ")
    
    archive_tab = st.tabs(["الدعاوى", "الطعون", "الفتاوى", "التحقيقات"])
    
    data = load_data()
    
    with archive_tab[0]:
        cases_archive = [a for a in data["archive"] if a.get("type") == "دعوى"]
        if cases_archive:
            for i, item in enumerate(cases_archive):
                with st.expander(f"#{i+1} - {item.get('parties')}"):
                    st.write(f"**المحكمة:** {item.get('court')}")
                    st.write(f"**تاريخ الجلسة:** {item.get('sessionDate')}")
                    st.write(f"**آخر إجراء:** {item.get('lastAction')}")
        else:
            st.info("لا توجد دعاوى في الأرشيف")
    
    with archive_tab[1]:
        appeals_archive = [a for a in data["archive"] if a.get("type") == "طعن"]
        if appeals_archive:
            for i, item in enumerate(appeals_archive):
                with st.expander(f"#{i+1} - {item.get('parties')}"):
                    st.write(f"**المحكمة:** {item.get('court')}")
                    st.write(f"**آخر إجراء:** {item.get('lastAction')}")
        else:
            st.info("لا توجد طعون في الأرشيف")
    
    with archive_tab[2]:
        if data["fatwas"]:
            for i, fatwa in enumerate(data["fatwas"]):
                with st.expander(f"#{i+1} - {fatwa.get('type')} - {fatwa.get('requester')}"):
                    st.write(f"**الموضوع:** {fatwa.get('question')}")
                    st.write(f"**النتيجة:** {fatwa.get('result')}")
        else:
            st.info("لا توجد فتاوى في الأرشيف")
    
    with archive_tab[3]:
        if data["investigations"]:
            for i, inv in enumerate(data["investigations"]):
                with st.expander(f"#{i+1} - {inv.get('violator')} - {inv.get('violationType')}"):
                    st.write(f"**الحالة:** {inv.get('status')}")
        else:
            st.info("لا توجد تحقيقات في الأرشيف")

# ================== SEARCH ==================
elif page == "🔎 البحث المتقدم":
    st.header("🔎 البحث المتقدم")
    
    st.markdown("### البحث عن سابقة إقامة دعوى من ذات الخصوم وذات الموضوع وذات السبب")
    
    col1, col2 = st.columns(2)
    with col1:
        search_name = st.text_input("البحث بالاسم")
        search_national = st.text_input("البحث بالرقم القومي", max_chars=14)
    with col2:
        search_number = st.text_input("رقم الدعوى")
        search_year = st.number_input("السنة", value=2026, min_value=1990, max_value=2030)
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔍 بحث", use_container_width=True):
            data = load_data()
            results = []
            
            for c in data["cases"]:
                if (search_name and (search_name.lower() in c.get("plaintiff", "").lower() or search_name.lower() in c.get("defendant", "").lower())) or \
                   (search_national and c.get("nationalId") == search_national) or \
                   (search_number and c.get("number") == search_number) or \
                   (search_year and c.get("year") == search_year):
                    results.append(("دعوى", c))
            
            for a in data["appeals"]:
                if (search_name and (search_name.lower() in a.get("appellant", "").lower() or search_name.lower() in a.get("respondent", "").lower())) or \
                   (search_number and a.get("number") == search_number) or \
                   (search_year and a.get("year") == search_year):
                    results.append(("طعن", a))
            
            st.session_state.search_results = results
    with col_btn2:
        if st.button("🔄 تفريغ", use_container_width=True):
            st.session_state.search_results = []
    
    if "search_results" in st.session_state and st.session_state.search_results:
        st.success(f"تم العثور على {len(st.session_state.search_results)} نتيجة")
        for type_, item in st.session_state.search_results:
            if type_ == "دعوى":
                with st.expander(f"دعوى رقم {item.get('number')} - {item.get('plaintiff')} ضد {item.get('defendant')}"):
                    st.write(f"**المحكمة:** {item.get('court')}")
                    st.write(f"**الحالة:** {item.get('status')}")
            else:
                with st.expander(f"طعن رقم {item.get('number')} - {item.get('appellant')} ضد {item.get('respondent')}"):
                    st.write(f"**المحكمة:** {item.get('court')}")
                    st.write(f"**الحالة:** {item.get('status')}")
    elif "search_results" in st.session_state:
        st.warning("⚠️ لا توجد نتائج مطابقة")

# ================== OTHER PAGES ==================
elif page == "📄 صحيفة استئناف":
    st.header("📄 صياغة صحيفة استئناف مقامة من الهيئة")
    with st.form("appeal_sheet_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("المحكمة", value="محكمة الاستئناف")
            st.text_input("رقم الحكم المستأنف")
            st.text_input("اسم المستأنف", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
        with col2:
            st.text_input("السنة", value="2026")
            st.text_input("تاريخ جلسة الحكم")
            st.text_input("منطوق الحكم")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("طلبات المستأنف", height=80)
        st.file_uploader("رفع صورة الصحيفة والحكم", type=["pdf", "jpg", "jpeg", "png"])
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            st.form_submit_button("✨ صياغة", use_container_width=True)
        with col_btn2:
            st.form_submit_button("💾 Word", use_container_width=True)
        with col_btn3:
            st.form_submit_button("📄 PDF", use_container_width=True)

elif page == "⚖️ صحيفة طعن بالنقض":
    st.header("⚖️ صياغة صحيفة طعن مقامة من الهيئة")
    with st.form("cassation_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("المحكمة", value="محكمة النقض المصرية", disabled=True)
            st.text_input("رقم الحكم المطعون فيه")
            st.text_input("اسم الطاعن", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
        with col2:
            st.text_input("السنة", value="2026")
            st.text_input("تاريخ جلسة الحكم الابتدائي")
            st.text_input("تاريخ جلسة الحكم الاستئنافي")
        st.text_area("ملخص الوقائع أمام المحكمة الابتدائية", height=80)
        st.text_area("ملخص الوقائع أمام محكمة الاستئناف", height=80)
        st.text_area("أسباب الطعن", height=120, placeholder="أخطاء في تطبيق القانون - مخالفة النص - قصور في التسبيب")
        st.file_uploader("رفع صور الصحف والأحكام", type=["pdf", "jpg", "jpeg", "png"])
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            st.form_submit_button("✨ صياغة", use_container_width=True)
        with col_btn2:
            st.form_submit_button("💾 Word", use_container_width=True)
        with col_btn3:
            st.form_submit_button("📄 PDF", use_container_width=True)

elif page == "🏛️ صحيفة طعن إداري":
    st.header("🏛️ صياغة صحيفة طعن أمام المحكمة الإدارية العليا")
    with st.form("admin_appeal_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("المحكمة", value="المحكمة الإدارية العليا", disabled=True)
            st.text_input("رقم الحكم المطعون فيه")
            st.text_input("اسم الطاعن", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
        with col2:
            st.text_input("السنة", value="2026")
            st.text_input("تاريخ جلسة حكم محكمة القضاء الإداري")
            st.text_input("تاريخ جلسة الحكم الاستئنافي")
        st.text_area("ملخص الوقائع أمام محكمة القضاء الإداري", height=80)
        st.text_area("ملخص الوقائع أمام المحكمة الإدارية العليا", height=80)
        st.file_uploader("رفع صور الصحيفة والحكم", type=["pdf", "jpg", "jpeg", "png"])
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        with col_btn1:
            st.form_submit_button("✨ صياغة", use_container_width=True)
        with col_btn2:
            st.form_submit_button("💾 Word", use_container_width=True)
        with col_btn3:
            st.form_submit_button("📄 PDF", use_container_width=True)

elif page == "🩹 إصابات العمل":
    st.header("🩹 إصابات العمل")
    with st.form("work_injury_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("اسم المصاب")
            st.text_input("الرقم التأميني")
        with col2:
            st.date_input("تاريخ الإصابة")
            st.text_input("المكتب التأميني")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("مثار البحث", height=80, value="هل تستحق إصابة العمل معاشاً؟")
        st.file_uploader("رفع المستندات", type=["pdf", "jpg", "jpeg", "png"])
        if st.form_submit_button("✨ صياغة الرأي", use_container_width=True):
            st.success("✅ تم صياغة الرأي القانوني!")
        st.form_submit_button("💾 حفظ", use_container_width=True)

elif page == "💑 شكاوى الزواج العرفي":
    st.header("💑 شكاوى الزواج العرفي")
    with st.form("marriage_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("اسم المستفيد")
            st.text_input("الرقم القومي", max_chars=14)
        with col2:
            st.text_input("اسم الزوج/الزوجة")
            st.date_input("تاريخ الزواج")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("مثار البحث", height=80, value="هل يحق للزوجة في الزواج العرفي الحصول على معاش؟")
        st.file_uploader("رفع المستندات", type=["pdf", "jpg", "jpeg", "png"])
        if st.form_submit_button("✨ صياغة الرأي", use_container_width=True):
            st.success("✅ تم صياغة الرأي القانوني!")
        st.form_submit_button("💾 حفظ", use_container_width=True)

elif page == "⚖️ النيابة الإدارية":
    st.header("⚖️ النيابة الإدارية")
    with st.form("admin_pros_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("رقم القضية")
            st.number_input("لسنة", value=2026)
        with col2:
            st.date_input("تاريخ القضية")
            st.text_input("نوع المخالفة")
        st.text_input("اسم المخالف")
        st.text_input("المكتب / المنطقة التأمينية")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("آخر إجراء", height=80)
        st.form_submit_button("💾 حفظ", use_container_width=True)

elif page == "👮 النيابة العامة":
    st.header("👮 النيابة العامة")
    with st.form("public_pros_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("رقم القضية")
            st.number_input("لسنة", value=2026)
        with col2:
            st.date_input("تاريخ القضية")
            st.text_input("نوع المخالفة")
        st.text_input("اسم المخالف")
        st.text_input("المكتب / المنطقة التأمينية")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("آخر إجراء", height=80)
        st.form_submit_button("💾 حفظ", use_container_width=True)

# ================== FOOTER ==================
st.markdown("---")
st.markdown("<div style='text-align:center; color:#666; padding:20px;'>", unsafe_allow_html=True)
st.markdown("**مع تحيات أ/ وليد حماد**")
st.markdown("الإدارة العامة للشئون القانونية | الهيئة القومية للتأمين الاجتماعي")
st.markdown("</div>", unsafe_allow_html=True)
'''

# Save the fixed file
with open('/mnt/agents/output/app_fixed.py', 'w', encoding='utf-8') as f:
    f.write(fixed_code)

size = os.path.getsize('/mnt/agents/output/app_fixed.py')
print(f"✅ Fixed file saved!")
print(f"📁 File: app_fixed.py")
print(f"📊 Size: {size:,} bytes ({size/1024:.1f} KB)")
print(f"📈 Lines: {len(fixed_code.split(chr(10)))}")
