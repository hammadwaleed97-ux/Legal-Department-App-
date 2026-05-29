import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# تنسيق CSS لضمان بقاء القائمة ظاهرة وتنسيقها بشكل جميل
st.markdown("""
    <style>
    /* تنسيق القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #1a252f;
        color: white;
        padding-top: 20px;
    }
    /* تنسيق العناوين داخل القائمة */
    .sidebar-header {
        color: #3498db;
        font-weight: bold;
        font-size: 16px;
        margin-top: 20px;
        margin-bottom: 10px;
        border-bottom: 1px solid #333;
    }
    /* تنسيق العناصر */
    .sidebar-item {
        color: white;
        font-size: 15px;
        padding: 8px 0;
        display: block;
    }
    .alert-item {
        background-color: #581845;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
        color: #ffcccb;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# الشريط الجانبي (القائمة)
with st.sidebar:
    # اللوجو والبيانات
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h3 style="color: white;">الهيئة القومية للتأمين الاجتماعي</h3>
            <p style="color: #bdc3c7;">الإدارة العامة للشئون القانونية</p>
            <div style="color: #3498db; font-weight: bold;">
                إعداد: وليد حماد<br>ديوان عام منطقة البحيرة
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # القوائم ظاهرة دائماً
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

# المحتوى الرئيسي
st.title("لوحة تحكم الإدارة القانونية")
st.write("تم ضبط القائمة لتكون ظاهرة دائماً. يمكنك الآن البدء في ربط كل قسم بمهامه البرمجية.")
