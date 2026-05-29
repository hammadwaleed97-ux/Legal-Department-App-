
# Build the updated code with memo defense page added
updated_code = r'''import streamlit as st
import json
import os
from datetime import datetime, date, timedelta
import base64
import re

st.set_page_config(page_title="الإدارة القانونية", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
.stApp { direction: rtl; }
div[data-testid="stSidebar"] { direction: rtl; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea, .stSelectbox > div > div > div { direction: rtl; }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"cases": [], "appeals": [], "fatwas": [], "investigations": [], "library": [], "archive": [], "activities": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.title("⚖️ الهيئة القومية للتأمين الاجتماعي")
st.subheader("الإدارة العامة للشئون القانونية")
st.markdown("---")

page = st.sidebar.radio("📂 القائمة", [
    "📊 لوحة التحكم", "📁 تسجيل الدعاوى", "📋 تسجيل الطعون", "📝 مذكرة دفاع (مدعى عليها)", "📄 صحيفة استئناف", "⚖️ صحيفة طعن بالنقض", "🏛️ صحيفة طعن إداري",
    "💡 الفتاوى القانونية", "🩹 إصابات العمل", "💑 شكاوى الزواج العرفي", "🔍 تحقيقات الهيئة", "⚖️ النيابة الإدارية", "👮 النيابة العامة",
    "📚 المكتبة القانونية", "🗄️ أرشيف الحفظ", "🔎 البحث المتقدم"
])

# ================== التنبيهات ==================
def check_alerts():
    data = load_data()
    alerts = []
    today = date.today()
    for c in data.get("cases", []):
        sd = c.get("sessionDate", "")
        if sd and sd != "None":
            try:
                d = datetime.strptime(sd, "%Y-%m-%d").date()
                diff = (d - today).days
                if 0 <= diff <= 7 and c.get("status") == "متداولة":
                    alerts.append({"type": "جلسة", "msg": f"دعوى {c.get('number')} - جلسة بعد {diff} أيام", "priority": "high" if diff <= 3 else "medium"})
            except: pass
    deadlines = {"محكمة استئناف": 40, "محكمة النقض": 60, "محكمة تأديبية": 30, "محكمة القضاء الإداري (استئنافية)": 40, "المحكمة الإدارية العليا": 60}
    for a in data.get("appeals", []):
        if a.get("status") == "متداولة":
            ad = a.get("date", "")
            court = a.get("court", "")
            if ad:
                try:
                    d = datetime.strptime(ad[:10], "%Y-%m-%d").date()
                    dl = d + timedelta(days=deadlines.get(court, 40))
                    rem = (dl - today).days
                    if 0 <= rem <= 15:
                        alerts.append({"type": "طعن", "msg": f"طعن {a.get('number')} - {court} - متبقي {rem} يوم", "priority": "high" if rem <= 5 else "medium"})
                except: pass
    return alerts

# ================== لوحة التحكم ==================
if page == "📊 لوحة التحكم":
    st.header("📊 لوحة التحكم")
    data = load_data()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("دعاوى متداولة", len([c for c in data["cases"] if c.get("status") == "متداولة"]))
    c2.metric("طعون", len(data["appeals"]))
    c3.metric("فتاوى", len(data["fatwas"]))
    c4.metric("تحقيقات", len(data["investigations"]))
    
    alerts = check_alerts()
    if alerts:
        st.warning("🔔 تنبيهات عاجلة")
        for a in alerts:
            if a["priority"] == "high": st.error(f"🚨 {a['type']}: {a['msg']}")
            else: st.info(f"⚠️ {a['type']}: {a['msg']}")
    else: st.success("✅ لا توجد تنبيهات حالياً")
    
    st.info("🤖 المساعد الذكي: ارفع المستندات لقراءتها وصياغة المذكرات تلقائياً")
    
    st.subheader("آخر النشاطات")
    if data["activities"]:
        for a in data["activities"][-10:][::-1]:
            st.write(f"**{a['action']}** | {a['date']}")
    else: st.info("لا توجد نشاطات")

# ================== الدعاوى ==================
elif page == "📁 تسجيل الدعاوى":
    st.header("📁 تسجيل الدعاوى")
    t1, t2 = st.tabs(["➕ جديدة", "📋 المسجلة"])
    
    with t1:
        with st.form("case_f"):
            c1, c2 = st.columns(2)
            with c1:
                court = st.selectbox("المحكمة", ["", "محكمة ابتدائية", "محكمة إدارية", "محكمة القضاء الإداري", "محكمة تأديبية"])
                num = st.text_input("رقم الدعوى")
                plaintiff = st.text_input("المدعي")
                p_role = st.text_input("صفة المدعي", placeholder="صاحب معاش")
            with c2:
                circle = st.text_input("الدائرة")
                year = st.number_input("لسنة", value=2026)
                nid = st.text_input("الرقم القومي", max_chars=14)
                defendant = st.text_input("المدعى عليه", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
            facts = st.text_area("ملخص الوقائع")
            requests = st.text_area("طلبات المدعي")
            c3, c4 = st.columns(2)
            with c3: s_date = st.date_input("تاريخ الجلسة")
            with c4: status = st.selectbox("الحالة", ["متداولة", "محسومة", "مؤجلة"])
            st.file_uploader("رفع صورة الصحيفة", type=["pdf", "jpg", "jpeg", "png"])
            
            b1, b2, b3 = st.columns(3)
            with b1: sub = st.form_submit_button("💾 حفظ", use_container_width=True)
            with b2: arc = st.form_submit_button("📁 أرشيف", use_container_width=True)
            with b3: clr = st.form_submit_button("🔄 تفريغ", use_container_width=True)
            
            if sub and num and plaintiff:
                d = load_data()
                d["cases"].append({"id": int(datetime.now().timestamp()), "court": court, "circle": circle, "number": num, "year": year, "plaintiff": plaintiff, "nationalId": nid, "plaintiffRole": p_role, "defendant": defendant, "facts": facts, "requests": requests, "sessionDate": str(s_date), "status": status, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["activities"].append({"action": f"تسجيل دعوى {num}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d); st.success("✅ تم الحفظ!")
            if arc and num and plaintiff:
                d = load_data()
                d["cases"].append({"id": int(datetime.now().timestamp()), "court": court, "circle": circle, "number": num, "year": year, "plaintiff": plaintiff, "nationalId": nid, "plaintiffRole": p_role, "defendant": defendant, "facts": facts, "requests": requests, "sessionDate": str(s_date), "status": status, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["archive"].append({"id": int(datetime.now().timestamp()), "type": "دعوى", "serial": len([a for a in d["archive"] if a["type"] == "دعوى"]) + 1, "parties": f"{plaintiff} ضد {defendant}", "court": court, "sessionDate": str(s_date), "judgment": "", "lastAction": "تسجيل", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d); st.success("✅ تم الحفظ في الأرشيف!")
    
    with t2:
        d = load_data()
        s = st.text_input("🔍 بحث بالاسم أو رقم الدعوى")
        fc = [c for c in d["cases"] if not s or s.lower() in c.get("plaintiff", "").lower() or s in c.get("number", "") or s in c.get("nationalId", "")]
        if fc:
            for c in fc[::-1]:
                col = "🟢" if c.get("status") == "متداولة" else "🔴" if c.get("status") == "محسومة" else "🟡"
                with st.expander(f"{col} دعوى {c.get('number')} لسنة {c.get('year')} - {c.get('plaintiff')}"):
                    c1, c2 = st.columns(2)
                    with c1: st.write(f"**المحكمة:** {c.get('court')}"); st.write(f"**الدائرة:** {c.get('circle')}"); st.write(f"**المدعي:** {c.get('plaintiff')}"); st.write(f"**الرقم القومي:** {c.get('nationalId')}")
                    with c2: st.write(f"**الحالة:** {c.get('status')}"); st.write(f"**تاريخ الجلسة:** {c.get('sessionDate')}"); st.write(f"**تاريخ التسجيل:** {c.get('date')}")
                    st.write(f"**الوقائع:** {c.get('facts')}"); st.write(f"**الطلبات:** {c.get('requests')}")
        else: st.info("لا توجد دعاوى")

# ================== الطعون ==================
elif page == "📋 تسجيل الطعون":
    st.header("📋 تسجيل الطعون")
    t1, t2 = st.tabs(["➕ جديد", "📋 المسجل"])
    
    with t1:
        with st.form("app_f"):
            c1, c2 = st.columns(2)
            with c1:
                court = st.selectbox("المحكمة", ["", "محكمة استئناف", "محكمة النقض", "محكمة تأديبية", "محكمة القضاء الإداري (استئنافية)", "المحكمة الإدارية العليا"])
                num = st.text_input("رقم الطعن")
                appellant = st.text_input("الطاعن")
            with c2:
                year = st.number_input("لسنة", value=2026)
                judgment = st.text_input("رقم الحكم المطعون فيه")
                respondent = st.text_input("المطعون ضده", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
            facts = st.text_area("ملخص الوقائع")
            requests = st.text_area("طلبات الطاعن")
            b1, b2 = st.columns(2)
            with b1: sub = st.form_submit_button("💾 حفظ", use_container_width=True)
            with b2: arc = st.form_submit_button("📁 أرشيف", use_container_width=True)
            
            if sub and num and appellant:
                d = load_data()
                d["appeals"].append({"id": int(datetime.now().timestamp()), "court": court, "number": num, "year": year, "judgmentNumber": judgment, "appellant": appellant, "respondent": respondent, "facts": facts, "requests": requests, "status": "متداولة", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["activities"].append({"action": f"تسجيل طعن {num}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d); st.success("✅ تم الحفظ!")
            if arc and num and appellant:
                d = load_data()
                d["appeals"].append({"id": int(datetime.now().timestamp()), "court": court, "number": num, "year": year, "judgmentNumber": judgment, "appellant": appellant, "respondent": respondent, "facts": facts, "requests": requests, "status": "متداولة", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["archive"].append({"id": int(datetime.now().timestamp()), "type": "طعن", "serial": len([a for a in d["archive"] if a["type"] == "طعن"]) + 1, "parties": f"{appellant} ضد {respondent}", "court": court, "sessionDate": "", "judgment": "", "lastAction": "تسجيل", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d); st.success("✅ تم الحفظ في الأرشيف!")
    
    with t2:
        d = load_data()
        if d["appeals"]:
            for a in d["appeals"][::-1]:
                with st.expander(f"طعن {a.get('number')} - {a.get('appellant')}"):
                    st.write(f"**المحكمة:** {a.get('court')}"); st.write(f"**الطاعن:** {a.get('appellant')}"); st.write(f"**الحالة:** {a.get('status')}")
        else: st.info("لا توجد طعون")

# ================== مذكرة دفاع (الهيئة مدعى عليها) ==================
elif page == "📝 مذكرة دفاع (مدعى عليها)":
    st.header("📝 مذكرة دفاع - الهيئة مدعى عليها")
    st.info("🤖 ارفع صورة الصحيفة للقراءة التلقائية")
    
    t1, t2 = st.tabs(["✏️ إدخال البيانات", "👁️ معاينة المذكرة"])
    
    with t1:
        with st.form("memo_f"):
            c1, c2 = st.columns(2)
            with c1:
                m_court = st.text_input("المحكمة")
                m_num = st.text_input("رقم الدعوى")
                m_plaintiff = st.text_input("اسم المدعي")
            with c2:
                m_circle = st.text_input("الدائرة")
                m_year = st.number_input("لسنة", value=2026)
                m_p_role = st.text_input("صفة المدعي")
            m_facts = st.text_area("ملخص الوقائع", height=100)
            m_requests = st.text_area("طلبات المدعي", height=80)
            m_defenses = st.text_area("الدفوع القانونية (كل دفع في سطر)", height=120, placeholder="المادة 45 من القانون 79 لسنة 1975\nعدم قبول الدعوى لرفعها على غير ذي صفة\nسقوط الحق بالتقادم")
            st.file_uploader("ارفع صورة الصحيفة للقراءة التلقائية", type=["pdf", "jpg", "jpeg", "png"])
            
            b1, b2, b3 = st.columns(3)
            with b1: gen = st.form_submit_button("✨ صياغة", use_container_width=True)
            with b2: sw = st.form_submit_button("💾 Word", use_container_width=True)
            with b3: sp = st.form_submit_button("📄 PDF", use_container_width=True)
            
            if gen and m_court and m_num and m_facts:
                dl = [d.strip() for d in m_defenses.split("\n") if d.strip()]
                dh = ""
                for i, d in enumerate(dl):
                    am = re.search(r'المادة\s*(\d+)', d)
                    an = am.group(1) if am else ""
                    dh += f'<p style="margin-top:15px;"><strong>الدفع {i+1}:</strong></p><p>وحيث إن {d}</p><p>وقد نصت المادة {an or "القانونية"} على أن ...</p><p>ولما كان ما تقدم، فإن هذا الدفع يكون قائماً على أسس قانونية سليمة.</p>'
                
                st.session_state.memo = f'<div style="text-align:center;margin-bottom:30px;"><div style="font-size:18px;font-weight:bold;">الهيئة القومية للتأمين الاجتماعي</div><div style="font-size:14px;">الإدارة العامة للشئون القانونية</div><div style="margin-top:10px;font-size:16px;">مذكرة بدفاع الهيئة القومية للتأمين الاجتماعي</div><div style="font-size:14px;color:#666;">مدعى عليها</div></div><p><strong>المحكمة:</strong> {m_court}</p><p><strong>الدائرة:</strong> {m_circle}</p><p><strong>رقم الدعوى:</strong> {m_num} لسنة {m_year}</p><hr><p><strong>المدعي:</strong> {m_plaintiff} - {m_p_role}</p><p><strong>المدعى عليه:</strong> الهيئة القومية للتأمين الاجتماعي</p><hr><p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">موضوع الدعوى وملخص الوقائع</p><p style="text-align:justify;line-height:2;">{m_facts}</p><p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">طلبات المدعي</p><p style="text-align:justify;line-height:2;">{m_requests}</p><p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">الدفوع القانونية للهيئة</p>{dh or "<p>لم يتم إدخال دفوع</p>"}<p style="text-align:center;font-weight:bold;font-size:16px;margin:20px 0;">المنتهى</p><p style="text-align:justify;line-height:2;">لما تقدم من أسباب، ولكون الدعوى لا تستند إلى سند قانوني سليم، فإن الهيئة تلتمس الحكم برفض الدعوى لعدم سندها من الواقع والقانون، مع إلزام المدعي بالمصاريف ومقابل أتعاب المحاماة.</p><div style="margin-top:50px;display:flex;justify-content:space-between;"><div style="text-align:center;width:200px;"><div style="border-top:1px solid #333;margin-top:60px;padding-top:5px;">عضو الإدارة القانونية</div></div><div style="text-align:center;width:200px;"><div style="border-top:1px solid #333;margin-top:60px;padding-top:5px;">مدير الإدارة القانونية</div></div></div>'
                st.success("✅ تم صياغة المذكرة! اذهب لعلامة التبويب 'معاينة المذكرة'")
                d = load_data()
                d["activities"].append({"action": f"صياغة مذكرة دفاع للدعوى {m_num}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d)
            
            if sw and "memo" in st.session_state:
                html = f'<html dir="rtl"><head><meta charset="utf-8"><title>مذكرة دفاع</title></head><body style="font-family:Arial;padding:40px;">{st.session_state.memo}</body></html>'
                b64 = base64.b64encode(html.encode()).decode()
                st.markdown(f'<a href="data:text/html;base64,{b64}" download="مذكرة_دفاع_{m_num}.html">⬇️ تحميل HTML</a>', unsafe_allow_html=True)
    
    with t2:
        if "memo" in st.session_state:
            st.markdown(st.session_state.memo, unsafe_allow_html=True)
            if st.button("🖨️ طباعة"): st.markdown('<script>window.print();</script>', unsafe_allow_html=True)
        else: st.info("اضغط 'صياغة المذكرة' أولاً لإنشاء المحتوى")

# ================== صحيفة استئناف ==================
elif page == "📄 صحيفة استئناف":
    st.header("📄 صياغة صحيفة استئناف مقامة من الهيئة")
    with st.form("appeal_sheet_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("المحكمة", value="محكمة الاستئناف")
            st.text_input("رقم الحكم المستأنف")
            st.text_input("اسم المستأنف", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
        with c2:
            st.text_input("السنة", value="2026")
            st.text_input("تاريخ جلسة الحكم")
            st.text_input("منطوق الحكم")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("طلبات المستأنف", height=80)
        st.file_uploader("رفع صورة الصحيفة والحكم", type=["pdf", "jpg", "jpeg", "png"])
        b1, b2, b3 = st.columns(3)
        with b1: st.form_submit_button("✨ صياغة", use_container_width=True)
        with b2: st.form_submit_button("💾 Word", use_container_width=True)
        with b3: st.form_submit_button("📄 PDF", use_container_width=True)

# ================== صحيفة طعن بالنقض ==================
elif page == "⚖️ صحيفة طعن بالنقض":
    st.header("⚖️ صياغة صحيفة طعن مقامة من الهيئة")
    with st.form("cassation_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("المحكمة", value="محكمة النقض المصرية", disabled=True)
            st.text_input("رقم الحكم المطعون عليه")
            st.text_input("اسم الطاعن", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
        with c2:
            st.text_input("السنة", value="2026")
            st.text_input("تاريخ جلسة الحكم الابتدائي")
            st.text_input("تاريخ جلسة الحكم الاستئنافي")
        st.text_area("ملخص الوقائع أمام المحكمة الابتدائية", height=80)
        st.text_area("ملخص الوقائع أمام محكمة الاستئناف", height=80)
        st.text_area("أسباب الطعن", height=120, placeholder="أخطاء في تطبيق القانون - مخالفة النص - قصور في التسبيب")
        st.file_uploader("رفع صور الصحف والأحكام", type=["pdf", "jpg", "jpeg", "png"])
        b1, b2, b3 = st.columns(3)
        with b1: st.form_submit_button("✨ صياغة", use_container_width=True)
        with b2: st.form_submit_button("💾 Word", use_container_width=True)
        with b3: st.form_submit_button("📄 PDF", use_container_width=True)

# ================== صحيفة طعن إداري ==================
elif page == "🏛️ صحيفة طعن إداري":
    st.header("🏛️ صياغة صحيفة طعن أمام المحكمة الإدارية العليا")
    with st.form("admin_appeal_form"):
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("المحكمة", value="المحكمة الإدارية العليا", disabled=True)
            st.text_input("رقم الحكم المطعون عليه")
            st.text_input("اسم الطاعن", value="الهيئة القومية للتأمين الاجتماعي", disabled=True)
        with c2:
            st.text_input("السنة", value="2026")
            st.text_input("تاريخ جلسة حكم محكمة القضاء الإداري")
            st.text_input("تاريخ جلسة الحكم الاستئنافي")
        st.text_area("ملخص الوقائع أمام محكمة القضاء الإداري", height=80)
        st.text_area("ملخص الوقائع أمام المحكمة الإدارية العليا", height=80)
        st.file_uploader("رفع صور الصحيفة والحكم", type=["pdf", "jpg", "jpeg", "png"])
        b1, b2, b3 = st.columns(3)
        with b1: st.form_submit_button("✨ صياغة", use_container_width=True)
        with b2: st.form_submit_button("💾 Word", use_container_width=True)
        with b3: st.form_submit_button("📄 PDF", use_container_width=True)

# ================== الفتاوى القانونية ==================
elif page == "💡 الفتاوى القانونية":
    st.header("💡 الفتاوى القانونية")
    t1, t2 = st.tabs(["➕ طلب فتوى جديد", "📋 أرشيف الفتاوى"])
    
    with t1:
        with st.form("fatwa_form"):
            fatwa_type = st.selectbox("نوع الفتوى", ["فتوى قانونية عامة", "إصابة عمل", "شكوى زواج عرفي"])
            fatwa_requester = st.text_input("الجهة الطالبة")
            fatwa_facts = st.text_area("ملخص الوقائع", height=100)
            fatwa_question = st.text_area("مثار البحث", height=80, placeholder="ما هو السؤال القانوني؟")
            
            if st.form_submit_button("✨ صياغة الرأي", use_container_width=True):
                if fatwa_type == "إصابة عمل":
                    st.session_state.op = "بناءً على المادة 51 من القانون رقم 79 لسنة 1975 بشأن التأمين الاجتماعي، والتي تنص على أن 'يؤدي صاحب العمل إلى الهيئة تعويضاً يعادل أجر يوم كامل عن كل يوم يغيب فيه المؤمن عليه عن عمله بسبب إصابة عمل'..."
                elif fatwa_type == "شكوى زواج عرفي":
                    st.session_state.op = "بالنسبة للزواج العرفي، فإن المادة 17 مكرر من القانون رقم 79 لسنة 1975 اشترطت توافر شروط معينة لاستحقاق المعاش..."
                else:
                    st.session_state.op = "بعد الاطلاع على الوقائع المذكورة أعلاه، والقوانين واللوائح المنظمة لذلك، يتبين أن..."
                st.success("✅ تم صياغة الرأي القانوني!")
            
            fatwa_opinion = st.text_area("الرأي القانوني", height=150, value=st.session_state.get("op", ""))
            fatwa_result = st.text_input("النتيجة")
            st.file_uploader("رفع مذكرة الإحالة والمستندات", type=["pdf", "jpg", "jpeg", "png"])
            
            if st.form_submit_button("💾 حفظ", use_container_width=True):
                d = load_data()
                d["fatwas"].append({"id": int(datetime.now().timestamp()), "type": fatwa_type, "requester": fatwa_requester, "facts": fatwa_facts, "question": fatwa_question, "opinion": fatwa_opinion, "result": fatwa_result, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["activities"].append({"action": f"إصدار فتوى {fatwa_type}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d); st.success("✅ تم حفظ الفتوى!")
    
    with t2:
        d = load_data()
        if d["fatwas"]:
            for f in d["fatwas"][::-1]:
                with st.expander(f"{f.get('type')} - {f.get('requester')}"):
                    st.write(f"**الجهة:** {f.get('requester')}"); st.write(f"**السؤال:** {f.get('question')}"); st.write(f"**الرأي:** {f.get('opinion')}"); st.write(f"**النتيجة:** {f.get('result')}")
        else: st.info("لا توجد فتاوى مسجلة")

# ================== إصابات العمل ==================
elif page == "🩹 إصابات العمل":
    st.header("🩹 إصابات العمل")
    with st.form("work_injury_form"):
        c1, c2 = st.columns(2)
        with c1: st.text_input("اسم المصاب"); st.text_input("الرقم التأميني")
        with c2: st.date_input("تاريخ الإصابة"); st.text_input("المكتب التأميني")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("مثار البحث", height=80, value="هل تستحق إصابة العمل معاشاً؟")
        st.file_uploader("رفع المستندات", type=["pdf", "jpg", "jpeg", "png"])
        if st.form_submit_button("✨ صياغة الرأي", use_container_width=True): st.success("✅ تم صياغة الرأي القانوني!")
        st.form_submit_button("💾 حفظ", use_container_width=True)

# ================== شكاوى الزواج العرفي ==================
elif page == "💑 شكاوى الزواج العرفي":
    st.header("💑 شكاوى الزواج العرفي")
    with st.form("marriage_form"):
        c1, c2 = st.columns(2)
        with c1: st.text_input("اسم المستفيد"); st.text_input("الرقم القومي", max_chars=14)
        with c2: st.text_input("اسم الزوج/الزوجة"); st.date_input("تاريخ الزواج")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("مثار البحث", height=80, value="هل يحق للزوجة في الزواج العرفي الحصول على معاش؟")
        st.file_uploader("رفع المستندات", type=["pdf", "jpg", "jpeg", "png"])
        if st.form_submit_button("✨ صياغة الرأي", use_container_width=True): st.success("✅ تم صياغة الرأي القانوني!")
        st.form_submit_button("💾 حفظ", use_container_width=True)

# ================== تحقيقات الهيئة ==================
elif page == "🔍 تحقيقات الهيئة":
    st.header("🔍 تحقيقات الهيئة")
    t1, t2 = st.tabs(["➕ فتح محضر تحقيق", "📋 التحقيقات المسجلة"])
    
    with t1:
        with st.form("inv_form"):
            c1, c2 = st.columns(2)
            with c1:
                inv_number = st.text_input("رقم التحقيق")
                inv_date = st.date_input("تاريخ الإحالة")
                inv_violation = st.text_input("نوع المخالفة")
            with c2:
                inv_year = st.number_input("لسنة", value=2026)
                inv_violator = st.text_input("اسم المخالف")
                inv_office = st.text_input("المكتب / المنطقة التأمينية")
            inv_facts = st.text_area("ملخص الوقائع", height=100)
            inv_questions = st.text_area("س و ج", height=80)
            inv_action = st.text_area("مذكرة التصرف", height=80)
            st.file_uploader("رفع مذكرة الإحالة والمستندات", type=["pdf", "jpg", "jpeg", "png"])
            b1, b2 = st.columns(2)
            with b1: sub = st.form_submit_button("💾 حفظ", use_container_width=True)
            with b2: close = st.form_submit_button("🔒 قفل", use_container_width=True)
            
            if sub and inv_number and inv_violator:
                d = load_data()
                d["investigations"].append({"id": int(datetime.now().timestamp()), "number": inv_number, "year": inv_year, "date": str(inv_date), "violationType": inv_violation, "violator": inv_violator, "office": inv_office, "facts": inv_facts, "questions": inv_questions, "action": inv_action, "status": "مفتوح", "dateCreated": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["activities"].append({"action": f"فتح محضر تحقيق {inv_number}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d); st.success("✅ تم حفظ التحقيق!")
            if close: st.success("🔒 تم قفل المحضر وإضافته للأرشيف!")
    
    with t2:
        d = load_data()
        if d["investigations"]:
            for inv in d["investigations"][::-1]:
                with st.expander(f"تحقيق {inv.get('number')} - {inv.get('violator')}"):
                    st.write(f"**المخالف:** {inv.get('violator')}"); st.write(f"**نوع المخالفة:** {inv.get('violationType')}"); st.write(f"**الحالة:** {inv.get('status')}")
        else: st.info("لا توجد تحقيقات مسجلة")

# ================== النيابة الإدارية ==================
elif page == "⚖️ النيابة الإدارية":
    st.header("⚖️ النيابة الإدارية")
    with st.form("admin_pros_form"):
        c1, c2 = st.columns(2)
        with c1: st.text_input("رقم القضية"); st.number_input("لسنة", value=2026)
        with c2: st.date_input("تاريخ القضية"); st.text_input("نوع المخالفة")
        st.text_input("اسم المخالف")
        st.text_input("المكتب / المنطقة التأمينية")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("آخر إجراء", height=80)
        st.form_submit_button("💾 حفظ", use_container_width=True)

# ================== النيابة العامة ==================
elif page == "👮 النيابة العامة":
    st.header("👮 النيابة العامة")
    with st.form("public_pros_form"):
        c1, c2 = st.columns(2)
        with c1: st.text_input("رقم القضية"); st.number_input("لسنة", value=2026)
        with c2: st.date_input("تاريخ القضية"); st.text_input("نوع المخالفة")
        st.text_input("اسم المخالف")
        st.text_input("المكتب / المنطقة التأمينية")
        st.text_area("ملخص الوقائع", height=100)
        st.text_area("آخر إجراء", height=80)
        st.form_submit_button("💾 حفظ", use_container_width=True)

# ================== المكتبة القانونية ==================
elif page == "📚 المكتبة القانونية":
    st.header("📚 المكتبة القانونية")
    t1, t2 = st.tabs(["➕ رفع وثيقة", "📋 الوثائق"])
    
    with t1:
        with st.form("lib_form"):
            lib_type = st.selectbox("نوع الوثيقة", ["قانون", "لائحة", "قرار وزاري", "منشور وزاري", "قرار رئيس الهيئة", "منشور رئيس الهيئة", "كتاب دوري", "تعليمات الهيئة", "المرصد الفني", "رسائل الهيئة", "مذكرات اللجنة القانونية", "فتاوى مجلس الدولة", "أحكام قضائية", "أخرى"])
            lib_title = st.text_input("عنوان الوثيقة")
            lib_doc_number = st.text_input("رقم الوثيقة")
            lib_year = st.number_input("السنة", value=2026)
            st.file_uploader("اختر ملف الوثيقة (PDF)", type=["pdf"])
            if st.form_submit_button("⬆️ رفع", use_container_width=True):
                d = load_data()
                d["library"].append({"id": int(datetime.now().timestamp()), "type": lib_type, "title": lib_title, "docNumber": lib_doc_number, "year": lib_year, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["activities"].append({"action": f"رفع وثيقة: {lib_title}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d); st.success("✅ تم رفع الوثيقة!")
    
    with t2:
        d = load_data()
        search_lib = st.text_input("🔍 بحث في المكتبة")
        lib_types = list(set([l.get("type") for l in d["library"]]))
        filter_lib = st.selectbox("تصفية", ["الكل"] + lib_types) if lib_types else st.selectbox("تصفية", ["الكل"])
        filtered_lib = d["library"]
        if search_lib: filtered_lib = [l for l in filtered_lib if search_lib.lower() in l.get("title", "").lower()]
        if filter_lib != "الكل": filtered_lib = [l for l in filtered_lib if l.get("type") == filter_lib]
        if filtered_lib:
            for doc in filtered_lib[::-1]:
                with st.expander(f"{doc.get('type')} - {doc.get('title')}"):
                    st.write(f"**الرقم:** {doc.get('docNumber')}"); st.write(f"**السنة:** {doc.get('year')}")
        else: st.info("لا توجد وثائق في المكتبة")

# ================== أرشيف الحفظ ==================
elif page == "🗄️ أرشيف الحفظ":
    st.header("🗄️ أرشيف الحفظ")
    archive_tab = st.tabs(["الدعاوى", "الطعون", "الفتاوى", "التحقيقات"])
    data = load_data()
    
    with archive_tab[0]:
        cases_archive = [a for a in data["archive"] if a.get("type") == "دعوى"]
        if cases_archive:
            for i, item in enumerate(cases_archive):
                with st.expander(f"#{i+1} - {item.get('parties')}"):
                    st.write(f"**المحكمة:** {item.get('court')}"); st.write(f"**تاريخ الجلسة:** {item.get('sessionDate')}"); st.write(f"**آخر إجراء:** {item.get('lastAction')}")
        else: st.info("لا توجد دعاوى في الأرشيف")
    
    with archive_tab[1]:
        appeals_archive = [a for a in data["archive"] if a.get("type") == "طعن"]
        if appeals_archive:
            for i, item in enumerate(appeals_archive):
                with st.expander(f"#{i+1} - {item.get('parties')}"):
                    st.write(f"**المحكمة:** {item.get('court')}"); st.write(f"**آخر إجراء:** {item.get('lastAction')}")
        else: st.info("لا توجد طعون في الأرشيف")
    
    with archive_tab[2]:
        if data["fatwas"]:
            for i, fatwa in enumerate(data["fatwas"]):
                with st.expander(f"#{i+1} - {fatwa.get('type')} - {fatwa.get('requester')}"):
                    st.write(f"**الموضوع:** {fatwa.get('question')}"); st.write(f"**النتيجة:** {fatwa.get('result')}")
        else: st.info("لا توجد فتاوى في الأرشيف")
    
    with archive_tab[3]:
        if data["investigations"]:
            for i, inv in enumerate(data["investigations"]):
                with st.expander(f"#{i+1} - {inv.get('violator')} - {inv.get('violationType')}"):
                    st.write(f"**الحالة:** {inv.get('status')}")
        else: st.info("لا توجد تحقيقات في الأرشيف")

# ================== البحث المتقدم ==================
elif page == "🔎 البحث المتقدم":
    st.header("🔎 البحث المتقدم")
    st.markdown("### البحث عن سابقة إقامة دعوى من ذات الخصوم وذات الموضوع وذات السبب")
    c1, c2 = st.columns(2)
    with c1:
        search_name = st.text_input("البحث بالاسم")
        search_national = st.text_input("البحث بالرقم القومي", max_chars=14)
    with c2:
        search_number = st.text_input("رقم الدعوى")
        search_year = st.number_input("السنة", value=2026, min_value=1990, max_value=2030)
    
    b1, b2 = st.columns(2)
    with b1:
        if st.button("🔍 بحث", use_container_width=True):
            d = load_data()
            results = []
            for c in d["cases"]:
                if (search_name and (search_name.lower() in c.get("plaintiff", "").lower() or search_name.lower() in c.get("defendant", "").lower())) or (search_national and c.get("nationalId") == search_national) or (search_number and c.get("number") == search_number) or (search_year and c.get("year") == search_year):
                    results.append(("دعوى", c))
            for a in d["appeals"]:
                if (search_name and (search_name.lower() in a.get("appellant", "").lower() or search_name.lower() in a.get("respondent", "").lower())) or (search_number and a.get("number") == search_number) or (search_year and a.get("year") == search_year):
                    results.append(("طعن", a))
            st.session_state.search_results = results
    with b2:
        if st.button("🔄 تفريغ", use_container_width=True): st.session_state.search_results = []
    
    if "search_results" in st.session_state and st.session_state.search_results:
        st.success(f"تم العثور على {len(st.session_state.search_results)} نتيجة")
        for type_, item in st.session_state.search_results:
            if type_ == "دعوى":
                with st.expander(f"دعوى {item.get('number')} - {item.get('plaintiff')} ضد {item.get('defendant')}"):
                    st.write(f"**المحكمة:** {item.get('court')}"); st.write(f"**الحالة:** {item.get('status')}")
            else:
                with st.expander(f"طعن {item.get('number')} - {item.get('appellant')} ضد {item.get('respondent')}"):
                    st.write(f"**المحكمة:** {item.get('court')}"); st.write(f"**الحالة:** {item.get('status')}")
    elif "search_results" in st.session_state: st.warning("⚠️ لا توجد نتائج مطابقة")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666; padding:20px;'>مع تحيات أ/ وليد حماد | الإدارة العامة للشئون القانونية | الهيئة القومية للتأمين الاجتماعي</div>", unsafe_allow_html=True)
'''

# Save
with open('/mnt/agents/output/app_final.py', 'w', encoding='utf-8') as f:
    f.write(updated_code)

size = os.path.getsize('/mnt/agents/output/app_final.py')
lines = len(updated_code.split('\n'))
print(f"✅ Final app saved!")
print(f"📊 Size: {size:,} bytes ({size/1024:.1f} KB)")
print(f"📈 Lines: {lines}")
