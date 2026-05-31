import streamlit as st

# إعدادات الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: الأزرق الداكن وتوزيع الأزرار
st.markdown("""
    <style>
    [data-testid='stSidebar'], header { display: none !important; }
    .hero-container {
        background: linear-gradient(180deg, #0b1e30 0%, #1a3a6e 100%);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 30px;
    }
    .hero-container h3, .hero-container p { color: white; margin: 5px; }
    .divider { border-top: 1px solid rgba(255,255,255,0.3); margin: 20px auto; width: 80%; }
    
    div.stButton > button {
        width: 100%;
        border: 2px solid #1a3a6e;
        color: #1a3a6e;
        font-weight: bold;
        background-color: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# الهوية البصرية (اللوجو والأيقونة)
st.markdown("""
    <div class="hero-container">
        <div style="font-size: 50px;">⚖️</div>
        <h3>الهيئة القومية للتأمين الاجتماعي</h3>
        <p style="font-size: 1.2em;">الإدارة العامة للشئون القانونية</p>
        <p>ديوان عام منطقة البحيرة</p>
        <div class="divider"></div>
        <p style="opacity: 0.8;">إعداد: وليد حماد</p>
    </div>
    """, unsafe_allow_html=True)

# الأزرار تحت اللوجو (التوزيع المعتمد)
col1, col2 = st.columns(2)

with col1:
    if st.button("⚖️ الإدارة العامة للقضايا"): st.session_state.page = "القضايا"; st.rerun()
    if st.button("📝 الإدارة العامة للفتوى"): st.session_state.page = "الفتوى"; st.rerun()
    if st.button("📚 المكتبة القانونية"): st.session_state.page = "المكتبة"; st.rerun()

with col2:
    if st.button("🔍 الإدارة العامة للتحقيقات والنيابات"): st.session_state.page = "التحقيقات"; st.rerun()
    if st.button("📦 الأرشيف الإلكتروني"): st.session_state.page = "الأرشيف"; st.rerun()
