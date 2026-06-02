import streamlit as st

# إعداد الصفحة
st.set_page_config(page_title="المستشار القانوني الذكي", layout="wide")

# التصميم الموحد (أزرق داكن + لوجو الميزان)
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    .stButton>button {width: 100%; background-color: #1a3a6e; color: white; border-radius: 8px;}
    .header {background-color: #1a3a6e; padding: 20px; border-radius: 10px; color: white; text-align: center;}
    </style>
    <div class="header">
        <h1>⚖️ المستشار القانوني الذكي</h1>
        <p>ديوان عام منطقة البحيرة</p>
    </div>
""", unsafe_allow_html=True)

# القائمة الجانبية
menu = st.sidebar.radio("القائمة الرئيسية", ["🔍 البحث القانوني الذكي", "📂 المكتبة القانونية"])

if menu == "🔍 البحث القانوني الذكي":
    st.subheader("طرح الاستعلام القانوني")
    question = st.text_area("اكتب سؤالك هنا (مثال: هل يستحق الورثة منحة قطع المعاش؟)")
    
    if st.button("بحث وتحليل"):
        if question:
            with st.spinner('جاري التحليل واستخراج النص القانوني...'):
                # هنا سيقوم النظام بالبحث في نصوص ملفات الدرايف
                # (سيتم ربط المجلد هنا)
                st.markdown("""
                ---
                **الإجابة القانونية:**
                بناءً على نص **المادة (10) من القانون رقم 148 لسنة 2019**، فإن استحقاق المنحة مشروط بـ ...
                
                **التحليل:**
                وحيث أن الابن المذكور قد توفى قبل تاريخ الصرف، وبناءً على ما تقدم...
                
                **النتيجة:** لا يستحق الورثة صرف المنحة.
                ---
                📄 *مرجع الاستخراج: قانون_التأمينات_الموحد.txt*
                """)
        else:
            st.warning("يرجى كتابة السؤال أولاً.")

elif menu == "📂 المكتبة القانونية":
    st.subheader("📂 ملفات المكتبة القانونية")
    st.write("يمكنك الوصول لجميع ملفاتك مباشرة عبر الرابط التالي:")
    st.markdown('[🔗 افتح مجلد المكتبة على Google Drive](https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke)')

# التذييل
st.sidebar.markdown("---")
st.sidebar.write("مع تحيات وليد حماد")
st.sidebar.write("الادارة العامة للشئون القانونية")
