from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CODE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>نظام الإدارة القانونية</title>
    <style>
        body { margin: 0; font-family: sans-serif; display: flex; height: 100vh; background-color: #f4f6f9; }
        .sidebar { width: 300px; background-color: #1a252f; color: #aeb9c5; padding: 20px; overflow-y: auto; }
        .logo-box { text-align: center; color: white; margin-bottom: 20px; border-bottom: 1px solid #333; padding-bottom: 15px; }
        .author { color: #3498db; font-weight: bold; margin-top: 10px; font-size: 14px; }
        .menu-item { padding: 12px; cursor: pointer; transition: 0.3s; border-radius: 4px; font-size: 14px; }
        .menu-item:hover { background-color: #2c3e50; color: white; }
        .alert { color: #e74c3c; font-weight: bold; }
        .main-content { flex-grow: 1; padding: 40px; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="logo-box">
            <h3>الهيئة القومية للتأمين الاجتماعـــــــي</h3>
            <p>الإدارة العامة للشئون القانونية</p>
            <div class="author">إعداد: وليد حماد<br>ديوان عام منطقة البحيرة</div>
        </div>
        <div class="menu-item">📁 تسجيل الدعاوى</div>
        <div class="menu-item">📋 تسجيل الطعون</div>
        <div class="menu-item">📝 مذكرة دفاع</div>
        <div class="menu-item alert">🔔 تنبيهات الجلسات (قبل أسبوع)</div>
        <div class="menu-item alert">🔔 تنبيهات الطعون (قبل 15 يوم)</div>
        <div class="menu-item">💡 الفتاوى القانونية</div>
        <div class="menu-item">🔍 تحقيقات الهيئة</div>
        <div class="menu-item">📚 المكتبة القانونية</div>
    </div>
    <div class="main-content">
        <h1>لوحة تحكم الإدارة القانونية</h1>
        <p>مرحباً بك أستاذ وليد، النظام جاهز للبدء.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_CODE)

if __name__ == '__main__':
    app.run(debug=True)
