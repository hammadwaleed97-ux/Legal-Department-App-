import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: إخفاء العناصر غير المرغوبة + تصميم اللوجو الثابت
st.markdown("""
    <style>
    [data-testid='stSidebar'], #stDecoration, [data-testid='stToolbar'], header { display: none !important; }
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 25px; color: #ffffff; text-align: center; 
        border-radius: 0 0 20px 20px; margin-top: -60px;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة عرض اللوجو الثابت
def show_header():
    st.markdown("""
        <div class="header-frame">
            <div style="font-size: 2.5rem;">⚖️</div>
            <h3>الهيئة القومية للتأمين الاجتماعي</h3>
            <p>الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة</p>
            <small>إعداد: وليد حماد</small>
        </div>
        """, unsafe_allow_html=True)

# تهيئة الحالة
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"
if 'cases' not in st.session_state: st.session_state.cases = pd.DataFrame(columns=["رقم القضية", "السنة", "النوع", "تاريخ الجلسة"])

# --- الصفحة الرئيسية ---
if st.session_state.page == "الرئيسية":
    show_header()
    st.write("<br>", unsafe_allow_html=True)
    
    # توزيع الأيقونات
    cols1 = st.columns(2)
    if cols1[0].button("📁 القضايا"): st.session_state.page = "القضايا"; st.rerun()
    if cols1[1].button("📝 الفتاوى"): st.session_state.page = "الفتاوى"; st.rerun()
    
    cols2 = st.columns(2)
    if cols2[0].button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if cols2[1].button("📚 المكتبة"): st.session_state.page = "المكتبة"; st.rerun()
    
    cols3 = st.columns(2)
    if cols3[0].button("📦 الأرشيف"): st.session_state.page = "الأرشيف"; st.rerun()

# --- قسم القضايا ---
elif st.session_state.page == "القضايا":
    show_header()
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
        st.write("قسم التنبيهات والتقارير جاهز للمتابعة...")
