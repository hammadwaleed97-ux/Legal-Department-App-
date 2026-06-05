st.markdown("""
<style>
/* خلفية التطبيق العامة */
.stApp {
    background: #062456;
}

/* النصوص العامة باللون الأبيض */
label, p, span, div, h1, h2, h3, h4, h5, h6 {
    color: white !important;
}

/* إصلاح القوائم المنسدلة (Selectbox) */
/* جعل خلفية القائمة بيضاء والنص أسود */
.stSelectbox div[data-baseweb="select"] {
    background-color: white !important;
}

/* التأكد من أن النص داخل القائمة يظهر باللون الأسود */
.stSelectbox div[data-baseweb="select"] span {
    color: black !important;
}

/* خيارات القائمة عند الفتح */
div[role="option"] {
    color: black !important;
    background-color: white !important;
}

/* حقول الإدخال */
input, textarea {
    color: black !important;
    background-color: white !important;
}

/* تنسيق الأزرار واللوجو كما هي */
div.stButton > button {
    width: 320px;
    height: 65px;
    border-radius: 15px;
    border: none;
    background: #2f55d4;
    color: white;
    font-size: 20px;
    font-weight: bold;
    display: block;
    margin: auto;
}
</style>
""", unsafe_allow_html=True)
