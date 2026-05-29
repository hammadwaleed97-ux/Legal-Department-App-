import streamlit as st

st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

st.markdown("""
    <style>
    /* إجبار القائمة على البقاء ظاهرة */
    [data-testid="stSidebar"] {
        width: 300px !important;
        display: block !important;
        background-color: #1a252f !important;
    }
    .sidebar-header { color: #3498db; font-weight: bold; margin-top: 15px; border-bottom: 1px solid #333; }
    .sidebar-item { color: white; padding: 5px 0; display: block; }
    .alert-item { background-color: #581845; padding: 8px; border-radius: 5px; color: #ffcccb; font-weight: bold; margin: 5px 0; }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 15px;">
            <h3 style="color: white; font-size: 18px;">الهيئة القومية للتأمين الاجتماعي</h3>
            <p style="color: #bdc3c7;">الإدارة العامة للشئون القانونية</p>
            <div style="color: #3498db; font-weight: bold;">إعداد: وليد حماد<br>ديوان عام منطقة البحيرة</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">🏛️ الإدارة العامة للقضايا</div>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-item">📁 تسجيل الدعاوى</span>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-item">📋 تسجيل الطعون</span>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-item">📝 مذكرة دفاع</span>', unsafe_allow_html=True)
    st.markdown('<div class="alert-item">🔔 تنبيهات الجلسات (قبل أسبوع)</div>', unsafe_allow_html=True)
    st.markdown('<div class="alert-item">🔔 تنبيهات الطعون (قبل 15 يوم)</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">💡 الإدارة العامة للفتوى</div>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-item">💡 الفتاوى القانونية</span>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-item">✏️ إصابات العمل</span>', unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-header">📚 المكتبة والأرشيف</div>', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-item">📚 المكتبة القانونية</span>', unsafe_allow_html=True)

st.title("لوحة تحكم الإدارة القانونية")
st.write("القائمة الجانبية مفروضة الآن لتكون ظاهرة.")
