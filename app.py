import streamlit as st

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="نظام الإدارة القانونية")

# التنسيق: إخفاء كل شيء يخص Streamlit + تصميم الشبكة الثنائي
st.markdown("""
    <style>
    /* إخفاء القائمة الجانبية، شريط الأدوات، وكل أزرار الهيدر */
    [data-testid="stSidebar"], #stDecoration, [data-testid="stToolbar"], header { display: none !important; }
    
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 30px;
        color: #ffffff;
        text-align: center;
        border-radius: 0 0 20px 20px;
        margin-top: -60px; /* سحب التصميم للأعلى لإخفاء الشريط العلوي */
    }
    
    /* شبكة أيقونات ثنائية الأعمدة */
    .icon-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
        padding: 20px;
        margin-top: 20px;
    }
    .icon-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 1px solid #dee2e6;
        font-weight: bold;
        color: #0b1e30;
    }
    </style>
    """, unsafe_allow_html=True)

# الشعار
st.markdown("""
    <div class="header-frame">
        <div style="font-size: 2.5rem;">⚖️</div>
        <h3>الهيئة القومية للتأمين الاجتماعي</h3>
        <p>الإدارة العامة للشؤون القانونية - ديوان عام منطقة البحيرة</p>
        <small>إعداد: وليد حماد</small>
    </div>
    """, unsafe_allow_html=True)

# شبكة الأيقونات الثنائية
st.markdown("""
    <div class="icon-grid">
        <div class="icon-card">📁<br>القضايا</div>
        <div class="icon-card">📝<br>الفتاوى</div>
        <div class="icon-card">🔍<br>التحقيقات</div>
        <div class="icon-card">📚<br>المكتبة</div>
        <div class="icon-card">📦<br>الأرشيف</div>
        <div class="icon-card">🏠<br>الرئيسية</div>
    </div>
    """, unsafe_allow_html=True)
