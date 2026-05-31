st.markdown("""
    <style>
    /* الحل الجذري لإخفاء السهم وكل ما يتعلق بهيدر القائمة */
    [data-testid="stSidebarCollapseButton"], 
    [data-testid="collapsedControl"], 
    .st-emotion-cache-12fmueu, 
    button[kind="header"] { 
        display: none !important; 
        visibility: hidden !important; 
    }
    
    /* التأكد من إخفاء أي عنصر تداخل في الأعلى */
    header { visibility: hidden !important; }
    
    [data-testid="stSidebar"] { background-color: #0b1e30 !important; color: white; }
    
    .header-frame {
        background: linear-gradient(135deg, #0b1e30, #1a3a6e);
        padding: 30px;
        border-radius: 0 0 20px 20px;
        color: #ffffff;
        text-align: center;
        margin: -40px -10px 20px -10px; /* تم تعديل الهامش للأعلى لإخفاء فراغ الهيدر */
    }
    .footer-text {
        font-size: 0.8rem;
        color: #88aacc;
        margin-top: 10px;
        border-top: 1px solid #3d5a80;
        padding-top: 5px;
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
