import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS ليكون مطابقاً للصورة
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #1a252f;
        color: white;
    }
    .sidebar-header {
        color: #3498db;
        font-weight: bold;
        margin-top: 15px;
        padding-bottom: 5px;
        border-bottom: 1px solid #333;
    }
    .sidebar-item {
        color: white;
        padding: 8px 0;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي (القائمة)
with st.sidebar:
    st.markdown("### الهيئة القومية للتأمين الاجتماعي")
    st.markdown("الإدارة العامة للشئون القانونية")
    st.markdown("---")
    
    st.markdown('<div class="sidebar-header">الرئيسية</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📊 لوحة التحكم</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">الإدارة العامة للقضايا</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📁 تسجيل الدعاوى</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📋 تسجيل الطعون</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📝 مذكرة دفاع</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">⚖️ صحيفة استئناف</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">الإدارة العامة للفتوى</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">💡 الفتاوى القانونية</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">✏️ إصابات العمل</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">التحقيقات والنيابات</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">🔍 تحقيقات الهيئة</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">المكتبة والأرشيف</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-item">📚 المكتبة القانونية</div>', unsafe_allow_html=True)

# المحتوى الرئيسي
st.title("لوحة تحكم الإدارة القانونية")
st.write("مرحباً بك أستاذ وليد. النظام جاهز للبدء في ربط المهام البرمجية.")
