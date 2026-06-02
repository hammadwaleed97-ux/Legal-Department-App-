import streamlit as st

# إعداد الصفحة لتناسب الموبايل
st.set_page_config(layout="centered")

st.markdown("""
    <div style="background-color: #1a3a6e; padding: 15px; border-radius: 8px; color: white; text-align: center;">
        <h4 style="margin: 0;">الإدارة العامة للشئون القانونية - منطقة البحيرة</h4>
    </div>
""", unsafe_allow_html=True)

# قائمة جانبية بسيطة
page = st.sidebar.radio("القائمة الرئيسية", ["⚖️ سجل القضايا", "🔍 البحث", "📂 المكتبة القانونية"])

if page == "⚖️ سجل القضايا":
    st.header("سجل القضايا")
    st.info("سجل القضايا يعمل الآن بشكل طبيعي بعد توفر المساحة.")
    
elif page == "🔍 البحث":
    st.header("محرك البحث")
    st.text_input("اكتب كلمة للبحث:")
    
elif page == "📂 المكتبة القانونية":
    st.header("المكتبة القانونية")
    st.markdown("[📂 اضغط هنا لفتح مجلد المكتبة](https://drive.google.com/drive/folders/12qOOtQncyClP9g6zi6VQQ2SozfWAlLke)")

# تذييل بسيط
st.sidebar.markdown("---")
st.sidebar.text("مع تحيات وليد حماد")
