
html_code = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>الهيئة القومية للتأمين الاجتماعي</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', Tahoma, Arial, sans-serif; background: #f0f2f5; direction: rtl; }

/* الهيدر */
.header {
    background: linear-gradient(135deg, #1a5f7a 0%, #2c8da8 100%);
    color: white;
    padding: 15px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}
.header-left { display: flex; align-items: center; gap: 15px; }
.header-icon { font-size: 30px; }
.header-title { font-size: 18px; font-weight: bold; }
.header-subtitle { font-size: 12px; opacity: 0.9; }
.header-right { font-size: 14px; }

/* المحتوى الرئيسي */
.container { display: flex; height: calc(100vh - 60px); }

/* القائمة الجانبية */
.sidebar {
    width: 280px;
    background: #1e2a3a;
    color: #b0c4de;
    overflow-y: auto;
    padding: 10px 0;
}
.sidebar-item {
    padding: 12px 20px;
    cursor: pointer;
    transition: all 0.3s;
    border-right: 3px solid transparent;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sidebar-item:hover { background: #2a3a4a; color: white; }
.sidebar-item.active { background: #2a3a4a; color: white; border-right-color: #4fc3f7; }
.sidebar-section {
    padding: 8px 20px;
    font-size: 11px;
    text-transform: uppercase;
    color: #5a7a9a;
    margin-top: 10px;
    letter-spacing: 1px;
}
.sidebar-icon { font-size: 16px; width: 25px; text-align: center; }

/* المحتوى */
.content {
    flex: 1;
    padding: 30px;
    overflow-y: auto;
    background: #f5f7fa;
}
.content-title {
    font-size: 24px;
    color: #1a5f7a;
    margin-bottom: 25px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

/* البطاقات */
.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    text-align: center;
}
.card-number { font-size: 36px; font-weight: bold; color: #1a5f7a; }
.card-label { font-size: 14px; color: #666; margin-top: 5px; }

/* التنبيهات */
.alerts {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.alert-item {
    padding: 10px 15px;
    margin: 8px 0;
    border-radius: 5px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.alert-success { background: #e8f5e9; color: #2e7d32; border-right: 4px solid #4caf50; }
.alert-warning { background: #fff3e0; color: #ef6c00; border-right: 4px solid #ff9800; }
.alert-danger { background: #ffebee; color: #c62828; border-right: 4px solid #f44336; }

/* النماذج */
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: bold; color: #333; font-size: 14px; }
.form-group input, .form-group select, .form-group textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ddd;
    border-radius: 6px;
    font-size: 14px;
    font-family: inherit;
}
.form-group textarea { resize: vertical; min-height: 80px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }

/* الأزرار */
.btn {
    padding: 10px 25px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: all 0.3s;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}
.btn-primary { background: #1a5f7a; color: white; }
.btn-primary:hover { background: #134b61; }
.btn-success { background: #4caf50; color: white; }
.btn-success:hover { background: #45a049; }
.btn-warning { background: #ff9800; color: white; }
.btn-warning:hover { background: #e68900; }
.btn-group { display: flex; gap: 10px; margin-top: 20px; }

/* التبويبات */
.tabs { display: flex; gap: 5px; margin-bottom: 20px; border-bottom: 2px solid #e0e0e0; }
.tab {
    padding: 10px 20px;
    cursor: pointer;
    border-bottom: 3px solid transparent;
    transition: all 0.3s;
    font-weight: bold;
    color: #666;
}
.tab:hover { color: #1a5f7a; }
.tab.active { color: #1a5f7a; border-bottom-color: #1a5f7a; }

/* الجدول */
.table-container { background: white; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); overflow: hidden; }
table { width: 100%; border-collapse: collapse; }
th { background: #1a5f7a; color: white; padding: 12px; text-align: right; font-size: 13px; }
td { padding: 12px; border-bottom: 1px solid #eee; font-size: 13px; }
tr:hover { background: #f5f7fa; }

/* المعاينة */
.preview-box {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    line-height: 2;
    font-size: 15px;
}
.preview-header { text-align: center; margin-bottom: 30px; }
.preview-header h2 { font-size: 20px; color: #1a5f7a; }
.preview-header h3 { font-size: 14px; color: #666; margin-top: 5px; }
.signature-line { border-top: 1px solid #333; margin-top: 60px; padding-top: 5px; width: 200px; text-align: center; }

/* الفوتر */
.footer {
    text-align: center;
    padding: 20px;
    color: #666;
    font-size: 12px;
    border-top: 1px solid #e0e0e0;
    margin-top: 30px;
}

/* إخفاء/إظهار */
.page { display: none; }
.page.active { display: block; }

/* مخصص للموبايل */
@media (max-width: 768px) {
    .sidebar { width: 100%; position: fixed; bottom: 0; z-index: 100; display: flex; overflow-x: auto; height: auto; }
    .sidebar-item { white-space: nowrap; }
    .container { flex-direction: column; }
    .content { padding: 15px; }
    .form-row { grid-template-columns: 1fr; }
}
</style>
</head>
<body>

<!-- الهيدر -->
<div class="header">
    <div class="header-left">
        <div class="header-icon">⚖️</div>
        <div>
            <div class="header-title">الهيئة القومية للتأمين الاجتماعي</div>
            <div class="header-subtitle">الإدارة العامة للشئون القانونية</div>
        </div>
    </div>
    <div class="header-right">مع تحيات أ/ وليد حماد</div>
</div>

<!-- المحتوى -->
<div class="container">
    <!-- القائمة الجانبية -->
    <div class="sidebar">
        <div class="sidebar-item active" onclick="showPage('dashboard')">
            <span class="sidebar-icon">📊</span> لوحة التحكم
        </div>
        
        <div class="sidebar-section">الإدارة العامة للقضايا</div>
        <div class="sidebar-item" onclick="showPage('cases')">
            <span class="sidebar-icon">📁</span> تسجيل الدعاوى
        </div>
        <div class="sidebar-item" onclick="showPage('appeals')">
            <span class="sidebar-icon">📋</span> تسجيل الطعون
        </div>
        <div class="sidebar-item" onclick="showPage('memo')">
            <span class="sidebar-icon">📝</span> مذكرة دفاع
        </div>
        <div class="sidebar-item" onclick="showPage('memo2')">
            <span class="sidebar-icon">📄</span> مذكرة مدعية
        </div>
        <div class="sidebar-item" onclick="showPage('appeal-sheet')">
            <span class="sidebar-icon">📨</span> صحيفة استئناف
        </div>
        <div class="sidebar-item" onclick="showPage('cassation')">
            <span class="sidebar-icon">⚖️</span> صحيفة طعن بالنقض
        </div>
        <div class="sidebar-item" onclick="showPage('admin-appeal')">
            <span class="sidebar-icon">🏛️</span> صحيفة طعن إداري
        </div>
        
        <div class="sidebar-section">الإدارة العامة للفتوى</div>
        <div class="sidebar-item" onclick="showPage('fatwa')">
            <span class="sidebar-icon">💡</span> الفتاوى القانونية
        </div>
        <div class="sidebar-item" onclick="showPage('injury')">
            <span class="sidebar-icon">🩹</span> إصابات العمل
        </div>
        <div class="sidebar-item" onclick="showPage('marriage')">
            <span class="sidebar-icon">💑</span> شكاوى الزواج العرفي
        </div>
        
        <div class="sidebar-section">التحقيقات والنيابات</div>
        <div class="sidebar-item" onclick="showPage('investigation')">
            <span class="sidebar-icon">🔍</span> تحقيقات الهيئة
        </div>
        <div class="sidebar-item" onclick="showPage('admin-pros')">
            <span class="sidebar-icon">⚖️</span> النيابة الإدارية
        </div>
        <div class="sidebar-item" onclick="showPage('public-pros')">
            <span class="sidebar-icon">👮</span> النيابة العامة
        </div>
        
        <div class="sidebar-section">المكتبة والأرشيف</div>
        <div class="sidebar-item" onclick="showPage('library')">
            <span class="sidebar-icon">📚</span> المكتبة القانونية
        </div>
        <div class="sidebar-item" onclick="showPage('archive')">
            <span class="sidebar-icon">🗄️</span> أرشيف الحفظ
        </div>
        <div class="sidebar-item" onclick="showPage('search')">
            <span class="sidebar-icon">🔎</span> البحث المتقدم
        </div>
    </div>

    <!-- المحتوى -->
    <div class="content">
        
        <!-- لوحة التحكم -->
        <div id="dashboard" class="page active">
            <div class="content-title">📊 لوحة التحكم</div>
            <div class="cards">
                <div class="card"><div class="card-number" id="caseCount">0</div><div class="card-label">دعاوى متداولة</div></div>
                <div class="card"><div class="card-number" id="appealCount">0</div><div class="card-label">طعون</div></div>
                <div class="card"><div class="card-number" id="fatwaCount">0</div><div class="card-label">فتاوى</div></div>
                <div class="card"><div class="card-number" id="invCount">0</div><div class="card-label">تحقيقات</div></div>
            </div>
            <div class="alerts">
                <h3 style="margin-bottom:15px;">🔔 التنبيهات</h3>
                <div id="alertsContainer">
                    <div class="alert-item alert-success">✅ لا توجد تنبيهات حالياً</div>
                </div>
            </div>
        </div>

        <!-- تسجيل الدعاوى -->
        <div id="cases" class="page">
            <div class="content-title">📁 تسجيل الدعاوى</div>
            <div class="tabs">
                <div class="tab active" onclick="showTab(this, 'newCase')">➕ جديدة</div>
                <div class="tab" onclick="showTab(this, 'listCase')">📋 المسجلة</div>
            </div>
            <div id="newCase">
                <div class="form-row">
                    <div class="form-group"><label>المحكمة</label><select id="caseCourt"><option value="">اختر</option><option>محكمة ابتدائية</option><option>محكمة إدارية</option><option>محكمة القضاء الإداري</option><option>محكمة تأديبية</option></select></div>
                    <div class="form-group"><label>الدائرة</label><input type="text" id="caseCircle" placeholder="الدائرة"></div>
                </div>
                <div class="form-row">
                    <div class="form-group"><label>رقم الدعوى</label><input type="text" id="caseNum" placeholder="رقم الدعوى"></div>
                    <div class="form-group"><label>لسنة</label><input type="number" id="caseYear" value="2026"></div>
                </div>
                <div class="form-row">
                    <div class="form-group"><label>المدعي</label><input type="text" id="casePlaintiff" placeholder="اسم المدعي"></div>
                    <div class="form-group"><label>الرقم القومي</label><input type="text" id="caseNid" placeholder="14 رقم" maxlength="14"></div>
                </div>
                <div class="form-group"><label>المدعى عليه</label><input type="text" value="الهيئة القومية للتأمين الاجتماعي" disabled></div>
                <div class="form-group"><label>ملخص الوقائع</label><textarea id="caseFacts" placeholder="ملخص الوقائع..."></textarea></div>
                <div class="form-group"><label>طلبات المدعي</label><textarea id="caseRequests" placeholder="طلبات المدعي..."></textarea></div>
                <div class="form-row">
                    <div class="form-group"><label>تاريخ الجلسة</label><input type="date" id="caseDate"></div>
                    <div class="form-group"><label>الحالة</label><select id="caseStatus"><option>متداولة</option><option>محسومة</option><option>مؤجلة</option></select></div>
                </div>
                <div class="form-group"><label>رفع صورة الصحيفة</label><input type="file" id="caseFile" accept=".pdf,.jpg,.jpeg,.png"></div>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="saveCase()">💾 حفظ</button>
                    <button class="btn btn-success" onclick="archiveCase()">📁 أرشيف</button>
                    <button class="btn btn-warning" onclick="clearCase()">🔄 تفريغ</button>
                </div>
            </div>
            <div id="listCase" style="display:none;">
                <div class="form-group"><input type="text" id="caseSearch" placeholder="🔍 بحث بالاسم أو رقم الدعوى" onkeyup="searchCases()"></div>
                <div class="table-container"><table><thead><tr><th>رقم الدعوى</th><th>المدعي</th><th>المحكمة</th><th>الحالة</th><th>الجلسة</th></tr></thead><tbody id="casesTable"></tbody></table></div>
            </div>
        </div>

        <!-- مذكرة دفاع -->
        <div id="memo" class="page">
            <div class="content-title">📝 مذكرة دفاع - الهيئة مدعى عليها</div>
            <div class="tabs">
                <div class="tab active" onclick="showTab(this, 'memoForm')">✏️ إدخال البيانات</div>
                <div class="tab" onclick="showTab(this, 'memoPreview')">👁️ معاينة المذكرة</div>
            </div>
            <div id="memoForm">
                <div class="form-row">
                    <div class="form-group"><label>المحكمة</label><input type="text" id="memoCourt" placeholder="المحكمة"></div>
                    <div class="form-group"><label>الدائرة</label><input type="text" id="memoCircle" placeholder="الدائرة"></div>
                </div>
                <div class="form-row">
                    <div class="form-group"><label>رقم الدعوى</label><input type="text" id="memoNum" placeholder="رقم الدعوى"></div>
                    <div class="form-group"><label>لسنة</label><input type="number" id="memoYear" value="2026"></div>
                </div>
                <div class="form-row">
                    <div class="form-group"><label>المدعي</label><input type="text" id="memoPlaintiff" placeholder="اسم المدعي"></div>
                    <div class="form-group"><label>صفة المدعي</label><input type="text" id="memoRole" placeholder="صاحب معاش"></div>
                </div>
                <div class="form-group"><label>ملخص الوقائع</label><textarea id="memoFacts" rows="4" placeholder="ملخص الوقائع..."></textarea></div>
                <div class="form-group"><label>طلبات المدعي</label><textarea id="memoRequests" rows="3" placeholder="طلبات المدعي..."></textarea></div>
                <div class="form-group"><label>الدفوع القانونية (كل دفع في سطر)</label><textarea id="memoDefenses" rows="4" placeholder="المادة 45 من القانون 79 لسنة 1975&#10;عدم قبول الدعوى لرفعها على غير ذي صفة&#10;سقوط الحق بالتقادم"></textarea></div>
                <div class="form-group"><label>رفع صورة الصحيفة</label><input type="file" accept=".pdf,.jpg,.jpeg,.png"></div>
                <div class="btn-group">
                    <button class="btn btn-primary" onclick="generateMemo()">✨ صياغة</button>
                    <button class="btn btn-success" onclick="downloadMemo()">💾 Word</button>
                    <button class="btn btn-warning" onclick="printMemo()">📄 PDF</button>
                </div>
            </div>
            <div id="memoPreview" style="display:none;">
                <div class="preview-box" id="memoContent">
                    <div class="preview-header">
                        <h2>الهيئة القومية للتأمين الاجتماعي</h2>
                        <h3>الإدارة العامة للشئون القانونية</h3>
                        <h2 style="margin-top:10px;">مذكرة بدفاع الهيئة</h2>
                        <h3 style="color:#999;">مدعى عليها</h3>
                    </div>
                    <p style="text-align:center;">اضغط "صياغة" لإنشاء المذكرة</p>
                </div>
            </div>
        </div>

        <!-- باقي الصفحات -->
        <div id="appeals" class="page"><div class="content-title">📋 تسجيل الطعون</div><p>قريباً...</p></div>
        <div id="memo2" class="page"><div class="content-title">📄 مذكرة مدعية</div><p>قريباً...</p></div>
        <div id="appeal-sheet" class="page"><div class="content-title">📨 صحيفة استئناف</div><p>قريباً...</p></div>
        <div id="cassation" class="page"><div class="content-title">⚖️ صحيفة طعن بالنقض</div><p>قريباً...</p></div>
        <div id="admin-appeal" class="page"><div class="content-title">🏛️ صحيفة طعن إداري</div><p>قريباً...</p></div>
        <div id="fatwa" class="page"><div class="content-title">💡 الفتاوى القانونية</div><p>قريباً...</p></div>
        <div id="injury" class="page"><div class="content-title">🩹 إصابات العمل</div><p>قريباً...</p></div>
        <div id="marriage" class="page"><div class="content-title">💑 شكاوى الزواج العرفي</div><p>قريباً...</p></div>
        <div id="investigation" class="page"><div class="content-title">🔍 تحقيقات الهيئة</div><p>قريباً...</p></div>
        <div id="admin-pros" class="page"><div class="content-title">⚖️ النيابة الإدارية</div><p>قريباً...</p></div>
        <div id="public-pros" class="page"><div class="content-title">👮 النيابة العامة</div><p>قريباً...</p></div>
        <div id="library" class="page"><div class="content-title">📚 المكتبة القانونية</div><p>قريباً...</p></div>
        <div id="archive" class="page"><div class="content-title">🗄️ أرشيف الحفظ</div><p>قريباً...</p></div>
        <div id="search" class="page"><div class="content-title">🔎 البحث المتقدم</div><p>قريباً...</p></div>

    </div>
</div>

<script>
// البيانات
let data = JSON.parse(localStorage.getItem('legalData')) || { cases: [], appeals: [], fatwas: [], investigations: [], archive: [], activities: [] };

function saveData() {
    localStorage.setItem('legalData', JSON.stringify(data));
    updateDashboard();
}

function updateDashboard() {
    document.getElementById('caseCount').textContent = data.cases.filter(c => c.status === 'متداولة').length;
    document.getElementById('appealCount').textContent = data.appeals.length;
    document.getElementById('fatwaCount').textContent = data.fatwas.length;
    document.getElementById('invCount').textContent = data.investigations.length;
    checkAlerts();
}

function checkAlerts() {
    let alerts = [];
    let today = new Date();
    data.cases.forEach(c => {
        if (c.sessionDate && c.status === 'متداولة') {
            let d = new Date(c.sessionDate);
            let diff = Math.ceil((d - today) / (1000 * 60 * 60 * 24));
            if (diff >= 0 && diff <= 7) {
                alerts.push({ type: 'جلسة', msg: `دعوى ${c.number} - جلسة بعد ${diff} أيام`, priority: diff <= 3 ? 'high' : 'medium' });
            }
        }
    });
    
    let container = document.getElementById('alertsContainer');
    if (alerts.length === 0) {
        container.innerHTML = '<div class="alert-item alert-success">✅ لا توجد تنبيهات حالياً</div>';
    } else {
        container.innerHTML = alerts.map(a => 
            `<div class="alert-item alert-${a.priority === 'high' ? 'danger' : 'warning'}">${a.priority === 'high' ? '🚨' : '⚠️'} ${a.type}: ${a.msg}</div>`
        ).join('');
    }
}

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
    document.querySelectorAll('.sidebar-item').forEach(i => i.classList.remove('active'));
    event.target.closest('.sidebar-item').classList.add('active');
}

function showTab(tab, contentId) {
    tab.parentElement.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
    let parent = tab.closest('.page');
    parent.querySelectorAll('[id]').forEach(el => {
        if (el.id !== parent.id && !el.classList.contains('content-title')) {
            if (el.id === contentId) el.style.display = 'block';
            else if (parent.contains(el)) el.style.display = 'none';
        }
    });
    document.getElementById(contentId).style.display = 'block';
}

function saveCase() {
    let caseData = {
        id: Date.now(),
        court: document.getElementById('caseCourt').value,
        circle: document.getElementById('caseCircle').value,
        number: document.getElementById('caseNum').value,
        year: document.getElementById('caseYear').value,
        plaintiff: document.getElementById('casePlaintiff').value,
        nationalId: document.getElementById('caseNid').value,
        facts: document.getElementById('caseFacts').value,
        requests: document.getElementById('caseRequests').value,
        sessionDate: document.getElementById('caseDate').value,
        status: document.getElementById('caseStatus').value,
        date: new Date().toLocaleString('ar-EG')
    };
    if (!caseData.number || !caseData.plaintiff) { alert('أدخل رقم الدعوى والمدعي'); return; }
    data.cases.push(caseData);
    data.activities.push({ action: `تسجيل دعوى ${caseData.number}`, date: new Date().toLocaleString('ar-EG') });
    saveData();
    alert('✅ تم الحفظ!');
    clearCase();
}

function archiveCase() {
    saveCase();
    let lastCase = data.cases[data.cases.length - 1];
    data.archive.push({
        id: Date.now(), type: 'دعوى', serial: data.archive.filter(a => a.type === 'دعوى').length + 1,
        parties: `${lastCase.plaintiff} ضد الهيئة`, court: lastCase.court,
        sessionDate: lastCase.sessionDate, lastAction: 'تسجيل', date: new Date().toLocaleString('ar-EG')
    });
    saveData();
    alert('✅ تم الحفظ في الأرشيف!');
}

function clearCase() {
    document.getElementById('caseCourt').value = '';
    document.getElementById('caseCircle').value = '';
    document.getElementById('caseNum').value = '';
    document.getElementById('casePlaintiff').value = '';
    document.getElementById('caseNid').value = '';
    document.getElementById('caseFacts').value = '';
    document.getElementById('caseRequests').value = '';
    document.getElementById('caseDate').value = '';
}

function searchCases() {
    let s = document.getElementById('caseSearch').value.toLowerCase();
    let filtered = data.cases.filter(c => !s || c.plaintiff.toLowerCase().includes(s) || c.number.includes(s) || c.nationalId.includes(s));
    document.getElementById('casesTable').innerHTML = filtered.map(c => 
        `<tr><td>${c.number} لسنة ${c.year}</td><td>${c.plaintiff}</td><td>${c.court}</td><td>${c.status}</td><td>${c.sessionDate}</td></tr>`
    ).join('');
}

function generateMemo() {
    let court = document.getElementById('memoCourt').value;
    let circle = document.getElementById('memoCircle').value;
    let num = document.getElementById('memoNum').value;
    let year = document.getElementById('memoYear').value;
    let plaintiff = document.getElementById('memoPlaintiff').value;
    let role = document.getElementById('memoRole').value;
    let facts = document.getElementById('memoFacts').value;
    let requests = document.getElementById('memoRequests').value;
    let defenses = document.getElementById('memoDefenses').value.split('\n').filter(d => d.trim());
    
    if (!court || !num || !facts) { alert('أدخل المحكمة ورقم الدعوى والوقائع'); return; }
    
    let dh = defenses.map((d, i) => {
        let m = d.match(/المادة\s*(\d+)/);
        let an = m ? m[1] : '';
        return `<p style="margin-top:15px;"><strong>الدفع ${i+1}:</strong></p><p>وحيث إن ${d}</p><p>وقد نصت المادة ${an || 'القانونية'} على أن ...</p><p>ولما كان ما تقدم، فإن هذا الدفع يكون قائماً على أسس قانونية سليمة.</p>`;
    }).join('');
    
    let memo = `
        <div class="preview-header">
            <h2>الهيئة القومية للتأمين الاجتماعي</h2>
            <h3>الإدارة العامة للشئون القانونية</h3>
            <h2 style="margin-top:10px;">مذكرة بدفاع الهيئة القومية للتأمين الاجتماعي</h2>
            <h3 style="color:#999;">مدعى عليها</h3>
        </div>
        <p><strong>المحكمة:</strong> ${court}</p>
        <p><strong>الدائرة:</strong> ${circle}</p>
        <p><strong>رقم الدعوى:</strong> ${num} لسنة ${year}</p>
        <hr>
        <p><strong>المدعي:</strong> ${plaintiff} - ${role}</p>
        <p><strong>المدعى عليه:</strong> الهيئة القومية للتأمين الاجتماعي</p>
        <hr>
        <h3 style="text-align:center; margin:20px 0;">موضوع الدعوى وملخص الوقائع</h3>
        <p style="text-align:justify; line-height:2;">${facts}</p>
        <h3 style="text-align:center; margin:20px 0;">طلبات المدعي</h3>
        <p style="text-align:justify; line-height:2;">${requests}</p>
        <h3 style="text-align:center; margin:20px 0;">الدفوع القانونية للهيئة</h3>
        ${dh || '<p>لم يتم إدخال دفوع</p>'}
        <h3 style="text-align:center; margin:20px 0;">المنتهى</h3>
        <p style="text-align:justify; line-height:2;">لما تقدم من أسباب، ولكون الدعوى لا تستند إلى سند قانوني سليم، فإن الهيئة تلتمس الحكم برفض الدعوى لعدم سندها من الواقع والقانون، مع إلزام المدعي بالمصاريف ومقابل أتعاب المحاماة.</p>
        <div style="display:flex; justify-content:space-between; margin-top:50px;">
            <div style="text-align:center;"><div class="signature-line">عضو الإدارة القانونية</div></div>
            <div style="text-align:center;"><div class="signature-line">مدير الإدارة القانونية</div></div>
        </div>
    `;
    
    document.getElementById('memoContent').innerHTML = memo;
    data.activities.push({ action: `صياغة مذكرة دفاع للدعوى ${num}`, date: new Date().toLocaleString('ar-EG') });
    saveData();
    alert('✅ تم الصياغة!');
    showTab(document.querySelector('#memo .tab:nth-child(2)'), 'memoPreview');
}

function downloadMemo() {
    let content = document.getElementById('memoContent').innerHTML;
    let html = `<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><title>مذكرة دفاع</title><style>body{font-family:Arial;padding:40px;line-height:2;}</style></head><body>${content}</body></html>`;
    let blob = new Blob([html], {type: 'text/html'});
    let url = URL.createObjectURL(blob);
    let a = document.createElement('a');
    a.href = url;
    a.download = 'مذكرة_دفاع.html';
    a.click();
}

function printMemo() {
    let content = document.getElementById('memoContent').innerHTML;
    let w = window.open('', '_blank');
    w.document.write(`<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><title>مذكرة دفاع</title><style>body{font-family:Arial;padding:40px;line-height:2;}</style></head><body>${content}</body></html>`);
    w.document.close();
    w.print();
}

// تحديث عند التحميل
updateDashboard();
searchCases();
</script>

</body>
</html>
'''

with open('/mnt/agents/output/index.html', 'w', encoding='utf-8') as f:
    f.write(html_code)

import os
size = os.path.getsize('/mnt/agents/output/index.html')
print(f"✅ HTML app saved: {size:,} bytes ({size/1024:.1f} KB)")
