import streamlit as st
import json
import os
from datetime import datetime, date, timedelta

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
    return {"cases": [], "appeals": [], "activities": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

st.title("⚖️ الهيئة القومية للتأمين الاجتماعي")
st.subheader("الإدارة العامة للشئون القانونية")

page = st.sidebar.radio("📂 القائمة", ["📊 لوحة التحكم", "📁 الدعاوى", "📋 الطعون"])

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

elif page == "📁 الدعاوى":
    st.header("📁 تسجيل الدعاوى")
    t1, t2 = st.tabs(["➕ جديدة", "📋 المسجلة"])
    
    with t1:
        with st.form("case_f"):
            c1, c2 = st.columns(2)
            with c1:
                court = st.selectbox("المحكمة", ["", "محكمة ابتدائية", "محكمة إدارية", "محكمة القضاء الإداري", "محكمة تأديبية"])
                num = st.text_input("رقم الدعوى")
                plaintiff = st.text_input("المدعي")
            with c2:
                circle = st.text_input("الدائرة")
                year = st.number_input("لسنة", value=2026)
                nid = st.text_input("الرقم القومي", max_chars=14)
            facts = st.text_area("ملخص الوقائع")
            requests = st.text_area("طلبات المدعي")
            s_date = st.date_input("تاريخ الجلسة")
            status = st.selectbox("الحالة", ["متداولة", "محسومة", "مؤجلة"])
            
            if st.form_submit_button("💾 حفظ", use_container_width=True) and num and plaintiff:
                d = load_data()
                d["cases"].append({"id": int(datetime.now().timestamp()), "court": court, "circle": circle, "number": num, "year": year, "plaintiff": plaintiff, "nationalId": nid, "facts": facts, "requests": requests, "sessionDate": str(s_date), "status": status, "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["activities"].append({"action": f"تسجيل دعوى {num}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d)
                st.success("✅ تم الحفظ!")
    
    with t2:
        d = load_data()
        s = st.text_input("🔍 بحث")
        fc = [c for c in d["cases"] if not s or s.lower() in c.get("plaintiff", "").lower() or s in c.get("number", "")]
        if fc:
            for c in fc[::-1]:
                col = "🟢" if c.get("status") == "متداولة" else "🔴"
                with st.expander(f"{col} دعوى {c.get('number')} - {c.get('plaintiff')}"):
                    st.write(f"**المحكمة:** {c.get('court')}"); st.write(f"**الحالة:** {c.get('status')}"); st.write(f"**الجلسة:** {c.get('sessionDate')}")
        else: st.info("لا توجد دعاوى")

elif page == "📋 الطعون":
    st.header("📋 تسجيل الطعون")
    t1, t2 = st.tabs(["➕ جديد", "📋 المسجل"])
    
    with t1:
        with st.form("app_f"):
            c1, c2 = st.columns(2)
            with c1:
                court = st.selectbox("المحكمة", ["", "محكمة استئناف", "محكمة النقض", "محكمة تأديبية"])
                num = st.text_input("رقم الطعن")
                appellant = st.text_input("الطاعن")
            with c2:
                year = st.number_input("لسنة", value=2026)
                judgment = st.text_input("رقم الحكم المطعون فيه")
            facts = st.text_area("ملخص الوقائع")
            requests = st.text_area("طلبات الطاعن")
            
            if st.form_submit_button("💾 حفظ", use_container_width=True) and num and appellant:
                d = load_data()
                d["appeals"].append({"id": int(datetime.now().timestamp()), "court": court, "number": num, "year": year, "judgmentNumber": judgment, "appellant": appellant, "facts": facts, "requests": requests, "status": "متداولة", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                d["activities"].append({"action": f"تسجيل طعن {num}", "date": datetime.now().strftime("%Y-%m-%d %H:%M")})
                save_data(d)
                st.success("✅ تم الحفظ!")
    
    with t2:
        d = load_data()
        if d["appeals"]:
            for a in d["appeals"][::-1]:
                with st.expander(f"طعن {a.get('number')} - {a.get('appellant')}"):
                    st.write(f"**المحكمة:** {a.get('court')}"); st.write(f"**الحالة:** {a.get('status')}")
        else: st.info("لا توجد طعون")

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666;'>مع تحيات أ/ وليد حماد | الإدارة العامة للشئون القانونية | الهيئة القومية للتأمين الاجتماعي</div>", unsafe_allow_html=True)
