import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. الإعدادات والتنسيق (الثابت)
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

st.markdown("""
    <style>
    [data-testid="stSidebar"], #stDecoration, [data-testid="stToolbar"], header { display: none !important; }
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 25px; color: #ffffff; text-align: center; 
        border-radius: 0 0 20px 20px; margin-top: -60px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="header-frame">
        <div style="font-size: 2.5rem;">⚖️</div>
        <h3>إدارة القضايا القانونية</h3>
        <small>ديوان عام منطقة البحيرة | إعداد: وليد حماد</small>
    </div>
    """, unsafe_allow_html=True)

# 2. تهيئة قاعدة البيانات المؤقتة
if 'cases' not in st.session_state:
    st.session_state.cases = pd.DataFrame(columns=["رقم القضية", "السنة", "النوع", "تاريخ الجلسة", "الحالة"])

# 3. نظام التبويبات للعمليات
tab1, tab2, tab3 = st.tabs(["➕ إضافة قضية", "📂 عرض القضايا", "🔔 التنبيهات والتقارير"])

with tab1:
    st.subheader("إدراج قضية جديدة")
    with st.form("case_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        num = c1.text_input("رقم القضية")
        year = c2.number_input("السنة", 2000, 2030, 2026)
        ctype = st.selectbox("نوع القضية", ["عمالية", "تأمينية", "مدنية", "إدارية"])
        cdate = st.date_input("تاريخ الجلسة القادمة")
        
        if st.form_submit_button("حفظ القضية"):
            new_entry = pd.DataFrame([{"رقم القضية": num, "السنة": year, "النوع": ctype, "تاريخ الجلسة": cdate, "الحالة": "قيد التداول"}])
            st.session_state.cases = pd.concat([st.session_state.cases, new_entry], ignore_index=True)
            st.success("تم إدراج القضية بنجاح في النظام")

with tab2:
    st.subheader("سجل القضايا")
    if not st.session_state.cases.empty:
        st.table(st.session_state.cases)
    else:
        st.info("لا توجد قضايا مسجلة حالياً.")

with tab3:
    st.subheader("🔔 التنبيهات والتقارير القانونية")
    if not st.session_state.cases.empty:
        today = datetime.now().date()
        cases_df = st.session_state.cases.copy()
        cases_df["تاريخ الجلسة"] = pd.to_datetime(cases_df["تاريخ الجلسة"]).dt.date
        
        # التنبيهات: قضايا الأسبوع القادم
        upcoming = cases_df[cases_df["تاريخ الجلسة"] <= (today + timedelta(days=7))]
        upcoming = upcoming[upcoming["تاريخ الجلسة"] >= today]
        
        if not upcoming.empty:
            st.warning("⚠️ قضايا عاجلة (جلسة خلال 7 أيام):")
            st.dataframe(upcoming)
        else:
            st.success("✅ لا توجد جلسات عاجلة في الأسبوع القادم.")
            
        st.write(f"📊 إجمالي القضايا المسجلة: **{len(st.session_state.cases)}**")
    else:
        st.write("نظام التنبيهات فارغ لعدم وجود قضايا.")
