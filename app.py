import streamlit as st
import pandas as pd

# الإعدادات الأساسية
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS
st.markdown("""
    <style>
    [data-testid='stSidebar'], #stDecoration, [data-testid='stToolbar'], header { display: none !important; }
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 20px; color: #ffffff; text-align: center; 
        border-radius: 0 0 20px 20px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown("""
        <div class="header-frame">
            <h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3>
            <p>الإدارة العامة للشئون القانونية | مع تحيات أ/ وليد حماد</p>
        </div>
        """, unsafe_allow_html=True)

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = "الرئيسية"

if st.session_state.page == "الرئيسية":
    show_header()
    st.write("### لوحة التحكم الرئيسية")
    
    # توزيع الأيقونات بطريقة آمنة
    c1, c2 = st.columns(2)
    if c1.button("📁 القضايا"): st.session_state.page = "القضايا"; st.rerun()
    if c2.button("📝 الفتاوى"): st.session_state.page = "الفتاوى"; st.rerun()
    
    c3, c4 = st.columns(2)
    if c3.button("🔍 التحقيقات"): st.session_state.page = "التحقيقات"; st.rerun()
    if c4.button("📚 المكتبة"): st.session_state.page = "المكتبة"; st.rerun()
    
    c5, c6 = st.columns(2)
    if c5.button("📦 الأرشيف"): st.session_state.page = "الأرشيف"; st.rerun()
    if c6.button("🔔 التنبيهات والتقارير"): st.session_state.page = "التنبيهات"; st.rerun()

elif st.session_state.page == "القضايا":
    show_header()
    if st.button("⬅️ عودة للرئيسية"): st.session_state.page = "الرئيسية"; st.rerun()
    st.header("📁 إدارة القضايا القانونية")
    # هنا سيبدأ بناء قسم القضايا التفصيلي
    st.info("جاري تجهيز قسم القضايا...")
