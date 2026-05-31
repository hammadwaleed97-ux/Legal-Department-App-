st.markdown("""
<style>
    /* إخفاء زر الطي */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* تثبيت القائمة الجانبية */
    section[data-testid="stSidebar"] {
        width: 300px !important;
    }

    /* إصلاح تداخل المحتوى الرئيسي */
    .main .block-container {
        padding-top: 2rem !important;
        margin-right: 320px !important; /* زيادة المسافة قليلاً */
    }
</style>
""", unsafe_allow_html=True)
