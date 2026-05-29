import streamlit as st
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
    "📊 لوحة التحكم", "📁 تسجيل الدعاوى", "📋 تسجيل الطعون", "📝 مذكرة دفاع (مدعى عليها)"
])

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
    for a in data.get("appeals", []):
        if a.get("status") == "متداولة":
            ad = a.get("date", "")
            if ad:
                try:
                    d = datetime.strptime(ad[:10], "%Y-%m-%d").date()
                    dl = d + timedelta(days=40)
                    rem = (dl - today).days
                    if 0 <= rem <= 15:
                        alerts.append({"type": "طعن", "msg": f"طعن {a.get('number')} - متبقي {rem} يوم", "priority": "high" if rem <= 5 else "medium"})
                except: pass
    return alerts

if page == "📊 لوحة التحكم":
    st.header("📊 لوحة التحكم")
    data = load_data()
    c1, c2, c3 = st.columns(3)
    c1.metric("دعاوى متداولة", len([c for c in data["cases"] if c.get("status") == "متداولة"]))
    c2.metric("طعون", len(data["appeals"]))
    c3.metric("نشاطات", len(data["activities"]))
    
    alerts = check_alerts()
    if alerts:
        st.warning("🔔 تنبيهات عاجلة")
        for a in alerts:
            if a["priority"] == "high": st.error(f"🚨 {a['type']}: {a['msg']}")
            else: st.info(f"⚠️ {a['type']}: {a['msg']}")
    else: st.success("✅ لا توجد تنبيهات حالياً")

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
                save_data(d)
                st.success("✅ تم الحفظ!")
            if arc and num and plaintiff:
                d = load_data()
                d["cases"].append({"id": int(datetime.now().timestamp()), "court": court, "circle": circle, "number": num, "year": year, "plaintiff": plaintiff, "nationalId": nid, "plaintiffRole": p_role, "defendant": defendant, "facts": facts, "requests": requests, "sessionDate": str(s_date), "status": status, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["archive"].append({"id": int(datetime.now().timestamp()), "type": "دعوى", "serial": len([a for a in d["archive"] if a["type"] == "دعوى"]) + 1, "parties": f"{plaintiff} ضد {defendant}", "court": court, "sessionDate": str(s_date), "judgment": "", "lastAction": "تسجيل", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d)
                st.success("✅ تم الحفظ في الأرشيف!")
    
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
                save_data(d)
                st.success("✅ تم الحفظ!")
            if arc and num and appellant:
                d = load_data()
                d["appeals"].append({"id": int(datetime.now().timestamp()), "court": court, "number": num, "year": year, "judgmentNumber": judgment, "appellant": appellant, "respondent": respondent, "facts": facts, "requests": requests, "status": "متداولة", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["archive"].append({"id": int(datetime.now().timestamp()), "type": "طعن", "serial": len([a for a in d["archive"] if a["type"] == "طعن"]) + 1, "parties": f"{appellant} ضد {respondent}", "court": court, "sessionDate": "", "judgment": "", "lastAction": "تسجيل", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d)
                st.success("✅ تم الحفظ في الأرشيف!")
    
    with t2:
        d = load_data()
        if d["appeals"]:
            for a in d["appeals"][::-1]:
                with st.expander(f"طعن {a.get('number')} - {a.get('appellant')}"):
                    st.write(f"**المحكمة:** {a.get('court')}"); st.write(f"**الطاعن:** {a.get('appellant')}"); st.write(f"**الحالة:** {a.get('status')}")
        else: st.info("لا توجد طعون")

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

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666; padding:20px;'>مع تحيات أ/ وليد حماد | الإدارة العامة للشئون القانونية | الهيئة القومية للتأمين الاجتماعي</div>", unsafe_allow_html=True)
