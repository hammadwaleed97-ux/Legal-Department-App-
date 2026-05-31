import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: إخفاء القائمة الجانبية + إطار يغطي الجزء العلوي
st.markdown("""
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    #stDecoration { display: none !important; }
    
    /* جعل الإطار الأزرق يغطي مساحة واسعة ليخفي أي تداخل */
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 40px 20px;
        color: #ffffff;
        text-align: center;
        margin: -60px -10px 30px -10px;
    }
    
    /* توزيع الأيقونات في الصفحة بالكامل */
    .main-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 25px;
        padding: 20px;
    }
    .icon-box {
        background: #f8f9fa;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid #e9ecef;
        transition: transform 0.3s, border-color 0.3s;
    }
    .icon-box:hover { transform: translateY(-10px); border-color: #1a3a6e; }
    </style>
    """, unsafe_allow_html=True)

# الشعار
st.markdown("""
    <div class="header-frame">
        <div style="font-size: 3rem;">⚖️</div>
        <h1>الهيئة القومية للتأمين الاجتماعي</h1>
        <h3>الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة</h3>
        <p style="color: #88aacc;">إعداد: وليد حماد</p>
    </div>
    """, unsafe_allow_html=True)

# الأيقونات موزعة في الصفحة
st.markdown("""
    <div class="main-grid">
        <div class="icon-box"><h1>📁</h1><h3>القضايا</h3></div>
        <div class="icon-box"><h1>📝</h1><h3>الفتاوى</h3></div>
        <div class="icon-box"><h1>🔍</h1><h3>التحقيقات</h3></div>
        <div class="icon-box"><h1>📚</h1><h3>المكتبة</h3></div>
        <div class="icon-box"><h1>🏠</h1><h3>الرئيسية</h3></div>
    </div>
    """, unsafe_allow_html=True)
