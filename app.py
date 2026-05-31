import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")
st.markdown("<style>[data-testid='stSidebar'], #stDecoration, [data-testid='stToolbar'], header { display: none !important; }</style>", unsafe_allow_html=True)

# تهيئة الحالة
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"
if 'cases' not in st.session_state: st.session_state.cases = pd.DataFrame(columns=["رقم القضية", "السنة", "النوع", "تاريخ الجلسة", "الحالة"])

# --- صفحة لوحة التحكم (الرئيسية) ---
if st.session_state.page == "الرئيسية":
    st.markdown("""<div style="background: linear-gradient(135deg, #0b1e30, #1a3a6e); padding: 30px; color: white; text-align: center; border-radius: 0 0 20px 20px;">
        <h2>نظام الإدارة القانونية الذكي</h2><p>ديوان عام منطقة البحيرة | وليد حماد</p></div>""", unsafe_allow_html=True)
    
    st.write("<br>", unsafe_allow_html=True)
    cols = st.columns(2)
    if cols[0].button("📁 القضايا"): st.session_state.page = "القضايا"; st.rerun()
    if cols[1].button("📝 الفتاوى"): st.session_state.page = "الفتاوى"; st.rerun()
    cols2 = st.columns(2)
    if cols2[0].button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if cols2[1].button("📚 المكتبة"): st.session_state.page = "المكتبة"; st.rerun()
    cols3 = st.columns(2)
    if cols3[0].button("📦 الأرشيف"): st.session_state.page = "الأرشيف"; st.rerun()

# --- صفحة قسم القضايا ---
elif st.session_state.page == "القضايا":
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    st.header("📁 إدارة القضايا القانونية")
    tab1, tab2, tab3 = st.tabs(["➕ إضافة قضية", "📂 عرض القضايا", "🔔 التنبيهات"])
    
    with tab1:
        with st.form("c_form", clear_on_submit=True):
            n, y = st.columns(2)
            num = n.text_input("رقم القضية")
            year = y.number_input("السنة", 2000, 2030, 2026)
            ctype = st.selectbox("النوع", ["عمالية", "تأمينية", "مدنية", "إدارية"])
            cdate = st.date_input("تاريخ الجلسة")
            if st.form_submit_button("حفظ"):
                st.session_state.cases = pd.concat([st.session_state.cases, pd.DataFrame([{"رقم القضية": num, "السنة": year, "النوع": ctype, "تاريخ الجلسة": cdate}])], ignore_index=True)
                st.success("تم الحفظ")
    with tab2:
        st.table(st.session_state.cases)
    with tab3:
        st.write("التنبيهات هنا...")
