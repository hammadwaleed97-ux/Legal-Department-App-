import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق الموحد الثابت
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #0b1e30 !important; color: white; }
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 30px;
        border-radius: 0 0 20px 20px;
        color: #ffffff;
        text-align: center;
        margin: -20px -10px 20px -10px;
    }
    .icon-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 15px;
        margin-top: 10px;
    }
    .icon-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        font-weight: bold;
        color: #0b1e30;
    }
    </style>
    """, unsafe_allow_html=True)

# الشعار
st.markdown("""
    <div class="header-frame">
        <div style="font-size: 3rem;">⚖️</div>
        <div style="font-size: 1.3rem; font-weight: bold;">الهيئة القومية للتأمين الاجتماعي</div>
        <div style="font-size: 1.1rem; margin-top: 5px;">الإدارة العامة للشؤون القانونية</div>
        <div style="font-size: 0.9rem; color: #a0c4e0;">ديوان عام منطقة البحيرة</div>
    </div>
    """, unsafe_allow_html=True)

# الأيقونات الثابتة (بدون السهم)
st.markdown("""
    <div class="icon-grid">
        <div class="icon-card">📁<br>القضايا</div>
        <div class="icon-card">📝<br>الفتاوى</div>
        <div class="icon-card">🔍<br>التحقيقات</div>
        <div class="icon-card">📚<br>المكتبة</div>
    </div>
    """, unsafe_allow_html=True)

# القائمة الجانبية (للتنقل)
st.sidebar.title("🏛️ القائمة الرئيسية")
choice = st.sidebar.radio("اختر القسم", ["الرئيسية", "القضايا", "الفتاوى", "التحقيقات"])

st.sidebar.markdown("---")
st.sidebar.write("مع تحيات وليد حماد")
st.sidebar.write("الإدارة العامة للشؤون القانونية")
