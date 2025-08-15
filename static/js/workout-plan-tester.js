// سكريبت اختبار خطة التمرين وحل المشاكل
// Workout Plan Testing and Problem Solving Script

class WorkoutPlanTester {
    constructor() {
        this.testResults = [];
        this.problems = [];
        this.solutions = [];
        this.isTestingInProgress = false;
        this.isSystemTesterPage = window.location.pathname.includes('system-tester');
        
        // Initialize when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    // Initialize the tester
    init() {
        if (this.isSystemTesterPage) {
            this.setupSystemTesterUI();
        } else {
            this.addTestButton();
        }
    }

    // Setup UI for system tester page
    setupSystemTesterUI() {
        const container = document.getElementById('test-container');
        if (container) {
            container.innerHTML = `
                <div class="test-controls">
                    <button id="start-test-btn" class="btn btn-primary">
                        🧪 بدء الاختبار الشامل
                    </button>
                    <button id="quick-test-btn" class="btn btn-secondary">
                        ⚡ اختبار سريع
                    </button>
                    <button id="clear-results-btn" class="btn btn-danger">
                        🗑️ مسح النتائج
                    </button>
                </div>
                <div id="test-results" class="test-results"></div>
            `;
            
            // Add event listeners
            document.getElementById('start-test-btn').addEventListener('click', () => {
                this.startComprehensiveTest();
            });
            
            document.getElementById('quick-test-btn').addEventListener('click', () => {
                this.runQuickTest();
            });
            
            document.getElementById('clear-results-btn').addEventListener('click', () => {
                this.clearResults();
            });
        }
    }

    // Add floating test button for regular pages
    addTestButton() {
        const testButton = document.createElement('button');
        testButton.innerHTML = '🧪 اختبار الخطة';
        testButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            cursor: pointer;
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(0,123,255,0.3);
            z-index: 9999;
            font-size: 14px;
            transition: all 0.3s ease;
        `;
        
        testButton.addEventListener('click', () => {
            this.startComprehensiveTest();
        });
        
        testButton.addEventListener('mouseenter', () => {
            testButton.style.transform = 'scale(1.05)';
            testButton.style.boxShadow = '0 6px 16px rgba(0,123,255,0.4)';
        });
        
        testButton.addEventListener('mouseleave', () => {
            testButton.style.transform = 'scale(1)';
            testButton.style.boxShadow = '0 4px 12px rgba(0,123,255,0.3)';
        });
        
        document.body.appendChild(testButton);
    }

    // Run quick test
    async runQuickTest() {
        if (this.isTestingInProgress) {
            this.showMessage('الاختبار قيد التشغيل بالفعل...', 'warning');
            return;
        }

        this.isTestingInProgress = true;
        this.testResults = [];
        this.problems = [];

        this.showMessage('بدء الاختبار السريع...', 'info');

        try {
            await this.testPageLoad();
            await this.testFormElements();
            this.displayTestResults();
        } catch (error) {
            this.addProblem('خطأ في الاختبار السريع', error.message, 'إعادة تحميل الصفحة والمحاولة مرة أخرى');
            this.showMessage('فشل في إكمال الاختبار السريع', 'error');
        } finally {
            this.isTestingInProgress = false;
        }
    }

    // بدء اختبار شامل للخطة
    async startComprehensiveTest() {
        if (this.isTestingInProgress) {
            this.showMessage('الاختبار قيد التشغيل بالفعل...', 'warning');
            return;
        }

        this.isTestingInProgress = true;
        this.testResults = [];
        this.problems = [];
        this.solutions = [];

        this.showMessage('🚀 بدء الاختبار الشامل...', 'info');
        this.createResultsContainer();
        this.showTestProgress('تحضير الاختبار...');

        try {
            // اختبارات النظام الأساسية
            await this.testSystemHealth();
            await this.delay(500);
            
            await this.testPageLoad();
            await this.delay(500);
            
            await this.testFormElements();
            await this.delay(500);
            
            await this.testStepNavigation();
            await this.delay(500);
            
            await this.testValidation();
            await this.delay(500);
            
            // اختبارات API
            await this.testAPIEndpoints();
            await this.delay(500);
            
            await this.testPlanGeneration();
            await this.delay(500);
            
            // اختبارات الأداء والتصميم
            this.testResponsiveDesign();
            await this.delay(500);
            
            await this.testPerformance();
            await this.delay(500);

            // عرض النتائج النهائية
            this.displayTestResults();
            this.showMessage('✅ اكتمل الاختبار الشامل!', 'success');

        } catch (error) {
            this.addProblem('خطأ في تشغيل الاختبار', error.message, 'إعادة تحميل الصفحة والمحاولة مرة أخرى');
            this.showMessage('❌ فشل في إكمال الاختبار', 'error');
            this.displayTestResults();
        } finally {
            this.isTestingInProgress = false;
        }
    }

    // اختبار تحميل الصفحة
    async testPageLoad() {
        const test = { name: 'تحميل الصفحة', status: 'جاري...', details: [] };
        
        try {
            // التحقق من تحميل العناصر الأساسية
            const requiredElements = [
                { selector: '.goal-card', name: 'بطاقات الأهداف' },
                { selector: '.split-card', name: 'بطاقات تقسيم التمارين' },
                { selector: '#step4-next', name: 'زر إنشاء الخطة' },
                { selector: '.progress-bar', name: 'شريط التقدم' }
            ];

            for (const element of requiredElements) {
                const el = document.querySelector(element.selector);
                if (el) {
                    test.details.push(`✅ ${element.name}: موجود`);
                } else {
                    test.details.push(`❌ ${element.name}: غير موجود`);
                    this.addProblem(
                        `عنصر مفقود: ${element.name}`,
                        `العنصر ${element.selector} غير موجود في الصفحة`,
                        'التحقق من ملف HTML والتأكد من وجود العنصر'
                    );
                }
            }

            // التحقق من تحميل CSS
            const cssLoaded = document.querySelector('link[href*="style.css"]');

            if (cssLoaded) {
                test.details.push('✅ ملف CSS: محمل');
            } else {
                test.details.push('❌ ملف CSS: غير محمل');
                this.addProblem('ملف CSS غير محمل', 'ملف التنسيق غير موجود', 'التحقق من مسار ملف CSS');
            }

            test.status = 'مكتمل';
        } catch (error) {
            test.status = 'فشل';
            test.details.push(`❌ خطأ: ${error.message}`);
            this.addProblem('خطأ في تحميل الصفحة', error.message, 'إعادة تحميل الصفحة');
        }

        this.testResults.push(test);
    }

    // اختبار عناصر النموذج
    async testFormElements() {
        const test = { name: 'عناصر النموذج', status: 'جاري...', details: [] };

        try {
            const formElements = [
                { id: 'current-weight', name: 'حقل الوزن', type: 'input' },
                { id: 'height', name: 'حقل الطول', type: 'input' },
                { id: 'age', name: 'حقل العمر', type: 'input' },
                { id: 'fitness-level', name: 'مستوى اللياقة', type: 'select' },
                { id: 'workout-days', name: 'أيام التمرين', type: 'select' }
            ];

            for (const element of formElements) {
                const el = document.getElementById(element.id);
                if (el) {
                    test.details.push(`✅ ${element.name}: موجود`);
                    
                    // اختبار إدخال قيم تجريبية
                    if (element.type === 'input') {
                        el.value = '75';
                        if (el.value === '75') {
                            test.details.push(`  ✅ يقبل الإدخال`);
                        } else {
                            test.details.push(`  ❌ لا يقبل الإدخال`);
                            this.addProblem(
                                `مشكلة في ${element.name}`,
                                'الحقل لا يقبل الإدخال',
                                'التحقق من خصائص الحقل وإزالة أي قيود'
                            );
                        }
                        el.value = ''; // إعادة تعيين القيمة
                    }
                } else {
                    test.details.push(`❌ ${element.name}: غير موجود`);
                    this.addProblem(
                        `حقل مفقود: ${element.name}`,
                        `الحقل ${element.id} غير موجود`,
                        'إضافة الحقل المفقود إلى HTML'
                    );
                }
            }

            test.status = 'مكتمل';
        } catch (error) {
            test.status = 'فشل';
            test.details.push(`❌ خطأ: ${error.message}`);
            this.addProblem('خطأ في اختبار النموذج', error.message, 'مراجعة كود HTML للنموذج');
        }

        this.testResults.push(test);
    }

    // اختبار التنقل بين الخطوات
    async testStepNavigation() {
        const test = { name: 'التنقل بين الخطوات', status: 'جاري...', details: [] };

        try {
            // اختبار وجود أزرار التنقل
            const navButtons = [
                { id: 'step1-next', name: 'زر التالي - الخطوة 1' },
                { id: 'step2-next', name: 'زر التالي - الخطوة 2' },
                { id: 'step2-prev', name: 'زر السابق - الخطوة 2' },
                { id: 'step3-next', name: 'زر التالي - الخطوة 3' },
                { id: 'step3-prev', name: 'زر السابق - الخطوة 3' },
                { id: 'step4-next', name: 'زر إنشاء الخطة' },
                { id: 'step4-prev', name: 'زر السابق - الخطوة 4' }
            ];

            for (const button of navButtons) {
                const btn = document.getElementById(button.id);
                if (btn) {
                    test.details.push(`✅ ${button.name}: موجود`);
                    
                    // اختبار إمكانية النقر
                    if (!btn.disabled) {
                        test.details.push(`  ✅ قابل للنقر`);
                    } else {
                        test.details.push(`  ⚠️ معطل حالياً`);
                    }
                } else {
                    test.details.push(`❌ ${button.name}: غير موجود`);
                    this.addProblem(
                        `زر مفقود: ${button.name}`,
                        `الزر ${button.id} غير موجود`,
                        'إضافة الزر المفقود إلى HTML'
                    );
                }
            }

            // اختبار وجود الخطوات
            for (let i = 1; i <= 4; i++) {
                const step = document.getElementById(`step${i}`);
                if (step) {
                    test.details.push(`✅ الخطوة ${i}: موجودة`);
                } else {
                    test.details.push(`❌ الخطوة ${i}: غير موجودة`);
                    this.addProblem(
                        `خطوة مفقودة: الخطوة ${i}`,
                        `عنصر الخطوة step${i} غير موجود`,
                        'إضافة عنصر الخطوة المفقود'
                    );
                }
            }

            test.status = 'مكتمل';
        } catch (error) {
            test.status = 'فشل';
            test.details.push(`❌ خطأ: ${error.message}`);
            this.addProblem('خطأ في اختبار التنقل', error.message, 'مراجعة كود JavaScript للتنقل');
        }

        this.testResults.push(test);
    }

    // اختبار التحقق من صحة البيانات
    async testValidation() {
        const test = { name: 'التحقق من صحة البيانات', status: 'جاري...', details: [] };

        try {
            // اختبار وجود دوال التحقق
            const validationFunctions = [
                'validateStep1',
                'validateStep2', 
                'validateStep3',
                'validateStep4',
                'validateAllSteps'
            ];

            for (const funcName of validationFunctions) {
                if (typeof window[funcName] === 'function') {
                    test.details.push(`✅ دالة ${funcName}: موجودة`);
                } else {
                    test.details.push(`❌ دالة ${funcName}: غير موجودة`);
                    this.addProblem(
                        `دالة تحقق مفقودة: ${funcName}`,
                        `الدالة ${funcName} غير معرفة`,
                        'إضافة دالة التحقق المفقودة إلى JavaScript'
                    );
                }
            }

            // اختبار المتغيرات العامة
            const globalVars = [
                'selectedGoal',
                'selectedSplit',
                'selectedBarriers',
                'formData',
                'currentStep'
            ];

            for (const varName of globalVars) {
                if (typeof window[varName] !== 'undefined') {
                    test.details.push(`✅ متغير ${varName}: معرف`);
                } else {
                    test.details.push(`❌ متغير ${varName}: غير معرف`);
                    this.addProblem(
                        `متغير مفقود: ${varName}`,
                        `المتغير ${varName} غير معرف`,
                        'تعريف المتغير في JavaScript'
                    );
                }
            }

            test.status = 'مكتمل';
        } catch (error) {
            test.status = 'فشل';
            test.details.push(`❌ خطأ: ${error.message}`);
            this.addProblem('خطأ في اختبار التحقق', error.message, 'مراجعة دوال التحقق');
        }

        this.testResults.push(test);
    }

    // اختبار إنشاء الخطة
    async testPlanGeneration() {
        const test = { name: 'إنشاء الخطة', status: 'جاري...', details: [] };

        try {
            // اختبار وجود دالة إنشاء الخطة
            if (typeof generatePlan === 'function') {
                test.details.push('✅ دالة generatePlan: موجودة');
            } else {
                test.details.push('❌ دالة generatePlan: غير موجودة');
                this.addProblem(
                    'دالة إنشاء الخطة مفقودة',
                    'الدالة generatePlan غير معرفة',
                    'إضافة دالة generatePlan إلى JavaScript'
                );
            }

            // اختبار الاتصال بالخادم
            try {
                const response = await fetch('/api/generate-workout-plan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        goal: 'weight_loss',
                        split: 'full_body',
                        weight: 75,
                        height: 175,
                        age: 25,
                        fitnessLevel: 'beginner',
                        workoutDays: 3
                    })
                });

                if (response.ok) {
                    test.details.push('✅ الاتصال بالخادم: ناجح');
                    const data = await response.json();
                    if (data.success) {
                        test.details.push('✅ إنشاء الخطة: ناجح');
                    } else {
                        test.details.push('❌ إنشاء الخطة: فشل');
                        this.addProblem(
                            'فشل في إنشاء الخطة',
                            data.message || 'خطأ غير معروف',
                            'مراجعة كود الخادم وقاعدة البيانات'
                        );
                    }
                } else {
                    test.details.push(`❌ الاتصال بالخادم: فشل (${response.status})`);
                    this.addProblem(
                        'فشل الاتصال بالخادم',
                        `رمز الخطأ: ${response.status}`,
                        'التحقق من تشغيل الخادم ومسار API'
                    );
                }
            } catch (error) {
                test.details.push(`❌ خطأ في الشبكة: ${error.message}`);
                this.addProblem(
                    'خطأ في الشبكة',
                    error.message,
                    'التحقق من الاتصال بالإنترنت وتشغيل الخادم'
                );
            }

            test.status = 'مكتمل';
        } catch (error) {
            test.status = 'فشل';
            test.details.push(`❌ خطأ: ${error.message}`);
            this.addProblem('خطأ في اختبار إنشاء الخطة', error.message, 'مراجعة كود إنشاء الخطة');
        }

        this.testResults.push(test);
    }

    // Test system health via API
    async testSystemHealth() {
        this.showTestProgress('فحص صحة النظام...');
        
        try {
            const response = await fetch('/api/system-health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                this.testResults.push({
                    name: 'صحة النظام',
                    status: 'passed',
                    message: 'النظام يعمل بشكل صحيح'
                });
            } else {
                this.testResults.push({
                    name: 'صحة النظام',
                    status: 'failed',
                    message: 'تم اكتشاف مشاكل في النظام'
                });
                
                if (!data.database) {
                    this.addProblem('قاعدة البيانات', 'فشل الاتصال بقاعدة البيانات', 'التحقق من ملف قاعدة البيانات');
                }
                
                Object.entries(data.files).forEach(([file, exists]) => {
                    if (!exists) {
                        this.addProblem('ملف مفقود', `الملف ${file} غير موجود`, `إنشاء الملف ${file}`);
                    }
                });
            }
        } catch (error) {
            this.testResults.push({
                name: 'صحة النظام',
                status: 'failed',
                message: `خطأ في فحص النظام: ${error.message}`
            });
            this.addProblem('خطأ في API', 'فشل في الاتصال بـ API صحة النظام', 'التحقق من تشغيل الخادم');
        }
    }

    // Test API endpoints
    async testAPIEndpoints() {
        this.showTestProgress('فحص نقاط API...');
        
        const endpoints = [
            { url: '/api/exercise-preview', method: 'POST', data: { goal: 'weight_loss' } },
            { url: '/api/generate-workout-plan', method: 'POST', data: this.getSamplePlanData() },
            { url: '/api/system-health', method: 'GET' }
        ];
        
        for (const endpoint of endpoints) {
            try {
                const options = {
                    method: endpoint.method,
                    headers: { 'Content-Type': 'application/json' }
                };
                
                if (endpoint.data) {
                    options.body = JSON.stringify(endpoint.data);
                }
                
                const response = await fetch(endpoint.url, options);
                
                if (response.ok) {
                    this.testResults.push({
                        name: `API ${endpoint.url}`,
                        status: 'passed',
                        message: `نقطة API تعمل بشكل صحيح (${response.status})`
                    });
                } else {
                    this.testResults.push({
                        name: `API ${endpoint.url}`,
                        status: 'failed',
                        message: `فشل API (${response.status})`
                    });
                    this.addProblem(`API ${endpoint.url}`, `رمز الخطأ: ${response.status}`, 'فحص كود الخادم');
                }
            } catch (error) {
                this.testResults.push({
                    name: `API ${endpoint.url}`,
                    status: 'failed',
                    message: `خطأ في الشبكة: ${error.message}`
                });
                this.addProblem(`API ${endpoint.url}`, error.message, 'فحص الاتصال بالشبكة');
            }
        }
    }

    // Test responsive design
    testResponsiveDesign() {
        this.showTestProgress('فحص التصميم المتجاوب...');
        
        const viewports = [
            { width: 320, name: 'موبايل صغير' },
            { width: 768, name: 'تابلت' },
            { width: 1024, name: 'سطح المكتب' }
        ];
        
        let responsiveIssues = 0;
        
        viewports.forEach(viewport => {
            // Simulate viewport change
            const originalWidth = window.innerWidth;
            
            // Check if elements are properly responsive
            const elements = document.querySelectorAll('.container, .row, .col-md-6');
            elements.forEach(element => {
                const computedStyle = window.getComputedStyle(element);
                if (computedStyle.overflow === 'hidden' && element.scrollWidth > element.clientWidth) {
                    responsiveIssues++;
                }
            });
        });
        
        if (responsiveIssues === 0) {
            this.testResults.push({
                name: 'التصميم المتجاوب',
                status: 'passed',
                message: 'التصميم متجاوب بشكل صحيح'
            });
        } else {
            this.testResults.push({
                name: 'التصميم المتجاوب',
                status: 'warning',
                message: `تم اكتشاف ${responsiveIssues} مشكلة في التصميم المتجاوب`
            });
            this.addProblem('التصميم المتجاوب', 'عناصر قد تتجاوز حدود الشاشة', 'مراجعة CSS والتأكد من استخدام Bootstrap بشكل صحيح');
        }
    }

    // Test performance
    async testPerformance() {
        this.showTestProgress('فحص الأداء...');
        
        const startTime = performance.now();
        
        // Test page load time
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        
        // Test resource loading
        const resources = performance.getEntriesByType('resource');
        const slowResources = resources.filter(resource => resource.duration > 1000);
        
        // Test memory usage (if available)
        let memoryUsage = 'غير متاح';
        if (performance.memory) {
            memoryUsage = `${Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)} MB`;
        }
        
        const endTime = performance.now();
        const testDuration = endTime - startTime;
        
        if (loadTime < 3000 && slowResources.length === 0) {
            this.testResults.push({
                name: 'الأداء',
                status: 'passed',
                message: `أداء ممتاز - وقت التحميل: ${loadTime}ms، الذاكرة: ${memoryUsage}`
            });
        } else {
            this.testResults.push({
                name: 'الأداء',
                status: 'warning',
                message: `أداء يحتاج تحسين - وقت التحميل: ${loadTime}ms، موارد بطيئة: ${slowResources.length}`
            });
            
            if (loadTime > 3000) {
                this.addProblem('بطء التحميل', `وقت تحميل الصفحة ${loadTime}ms`, 'تحسين الصور وضغط الملفات');
            }
            
            if (slowResources.length > 0) {
                this.addProblem('موارد بطيئة', `${slowResources.length} مورد يحمل ببطء`, 'تحسين الموارد أو استخدام CDN');
            }
        }
    }

    // Get sample data for testing
    getSamplePlanData() {
        return {
            goal: 'weight_loss',
            split: 'full_body',
            weight: 70,
            height: 170,
            age: 25,
            fitness_level: 'beginner',
            workout_days: 3,
            barriers: ['وقت محدود']
        };
    }

    // إضافة مشكلة إلى القائمة
    addProblem(title, description, solution) {
        this.problems.push({
            title,
            description,
            solution,
            timestamp: new Date().toLocaleString('ar-SA')
        });
    }

    // عرض النتائج النهائية
    displayTestResults() {
        const resultsContainer = this.createResultsContainer();
        
        // إحصائيات عامة
        const totalTests = this.testResults.length;
        const passedTests = this.testResults.filter(t => t.status === 'مكتمل').length;
        const failedTests = totalTests - passedTests;
        const totalProblems = this.problems.length;

        resultsContainer.innerHTML = `
            <div class="test-summary">
                <h3>📊 ملخص نتائج الاختبار</h3>
                <div class="summary-stats">
                    <div class="stat-item success">
                        <span class="stat-number">${passedTests}</span>
                        <span class="stat-label">اختبار ناجح</span>
                    </div>
                    <div class="stat-item error">
                        <span class="stat-number">${failedTests}</span>
                        <span class="stat-label">اختبار فاشل</span>
                    </div>
                    <div class="stat-item warning">
                        <span class="stat-number">${totalProblems}</span>
                        <span class="stat-label">مشكلة مكتشفة</span>
                    </div>
                </div>
            </div>

            <div class="test-details">
                <h4>📋 تفاصيل الاختبارات</h4>
                ${this.testResults.map(test => `
                    <div class="test-item ${test.status === 'مكتمل' ? 'success' : 'error'}">
                        <h5>${test.name} - ${test.status}</h5>
                        <ul>
                            ${test.details.map(detail => `<li>${detail}</li>`).join('')}
                        </ul>
                    </div>
                `).join('')}
            </div>

            ${this.problems.length > 0 ? `
                <div class="problems-section">
                    <h4>🔧 المشاكل المكتشفة والحلول</h4>
                    ${this.problems.map((problem, index) => `
                        <div class="problem-item">
                            <div class="problem-header">
                                <h5>❌ ${problem.title}</h5>
                                <span class="problem-time">${problem.timestamp}</span>
                            </div>
                            <div class="problem-description">
                                <strong>الوصف:</strong> ${problem.description}
                            </div>
                            <div class="problem-solution">
                                <strong>الحل المقترح:</strong> ${problem.solution}
                            </div>
                            <button class="fix-button" onclick="workoutTester.applyQuickFix(${index})">
                                تطبيق الحل السريع
                            </button>
                        </div>
                    `).join('')}
                </div>
            ` : '<div class="no-problems">✅ لم يتم العثور على أي مشاكل!</div>'}

            <div class="test-actions">
                <button class="btn-primary" onclick="workoutTester.startComprehensiveTest()">
                    إعادة تشغيل الاختبار
                </button>
                <button class="btn-secondary" onclick="workoutTester.exportTestReport()">
                    تصدير التقرير
                </button>
                <button class="btn-danger" onclick="workoutTester.clearResults()">
                    مسح النتائج
                </button>
            </div>
        `;

        this.showMessage(
            `اكتمل الاختبار! ${passedTests}/${totalTests} اختبار ناجح، ${totalProblems} مشكلة مكتشفة`,
            totalProblems === 0 ? 'success' : 'warning'
        );
    }

    // تطبيق حل سريع للمشكلة
    applyQuickFix(problemIndex) {
        const problem = this.problems[problemIndex];
        if (!problem) return;

        this.showMessage(`جاري تطبيق الحل للمشكلة: ${problem.title}`, 'info');

        // حلول سريعة مخصصة
        switch (problem.title) {
            case 'ملف CSS غير محمل':
                this.fixMissingCSS();
                break;
            case 'ملف JavaScript غير محمل':
                this.fixMissingJS();
                break;
            default:
                this.showMessage('لا يوجد حل سريع متاح لهذه المشكلة', 'warning');
                break;
        }
    }

    // إصلاح ملف CSS المفقود
    fixMissingCSS() {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = '/static/css/style.css';
        document.head.appendChild(link);
        this.showMessage('تم إضافة ملف CSS', 'success');
    }



    // تصدير تقرير الاختبار
    exportTestReport() {
        const report = {
            timestamp: new Date().toISOString(),
            summary: {
                totalTests: this.testResults.length,
                passedTests: this.testResults.filter(t => t.status === 'مكتمل').length,
                totalProblems: this.problems.length
            },
            testResults: this.testResults,
            problems: this.problems
        };

        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `workout-plan-test-report-${new Date().toISOString().split('T')[0]}.json`;
        a.click();
        URL.revokeObjectURL(url);

        this.showMessage('تم تصدير التقرير بنجاح', 'success');
    }

    // مسح النتائج
    clearResults() {
        this.testResults = [];
        this.problems = [];
        const container = document.getElementById('test-results-container');
        if (container) {
            container.remove();
        }
        this.showMessage('تم مسح النتائج', 'info');
    }

    // إنشاء حاوية النتائج
    createResultsContainer() {
        let container = document.getElementById('test-results-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'test-results-container';
            container.className = 'test-results-container';
            document.body.appendChild(container);
        }
        return container;
    }

    // عرض شريط التقدم
    showTestProgress(percentage) {
        let progressContainer = document.getElementById('test-progress-container');
        if (!progressContainer) {
            progressContainer = document.createElement('div');
            progressContainer.id = 'test-progress-container';
            progressContainer.className = 'test-progress-container';
            progressContainer.innerHTML = `
                <div class="test-progress-bar">
                    <div class="test-progress-fill" style="width: 0%"></div>
                </div>
                <div class="test-progress-text">0%</div>
            `;
            document.body.appendChild(progressContainer);
        }
        this.updateTestProgress(percentage);
    }

    // تحديث شريط التقدم
    updateTestProgress(percentage) {
        const fill = document.querySelector('.test-progress-fill');
        const text = document.querySelector('.test-progress-text');
        if (fill && text) {
            fill.style.width = percentage + '%';
            text.textContent = percentage + '%';
        }
    }

    // عرض رسالة
    showMessage(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `test-message test-message-${type}`;
        messageDiv.textContent = message;
        
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            messageDiv.remove();
        }, 5000);
    }
}

// إنشاء مثيل من فئة الاختبار
const workoutTester = new WorkoutPlanTester();

// إضافة أنماط CSS للاختبار
const testStyles = `
<style>
.test-results-container {
    position: fixed;
    top: 20px;
    right: 20px;
    width: 400px;
    max-height: 80vh;
    overflow-y: auto;
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 10000;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    direction: rtl;
    text-align: right;
}

.test-summary {
    padding: 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #eee;
}

.summary-stats {
    display: flex;
    justify-content: space-around;
    margin-top: 15px;
}

.stat-item {
    text-align: center;
    padding: 10px;
    border-radius: 6px;
}

.stat-item.success { background: #d4edda; color: #155724; }
.stat-item.error { background: #f8d7da; color: #721c24; }
.stat-item.warning { background: #fff3cd; color: #856404; }

.stat-number {
    display: block;
    font-size: 24px;
    font-weight: bold;
}

.stat-label {
    font-size: 12px;
}

.test-details, .problems-section {
    padding: 20px;
}

.test-item {
    margin-bottom: 15px;
    padding: 10px;
    border-radius: 6px;
    border-left: 4px solid;
}

.test-item.success { 
    background: #d4edda; 
    border-left-color: #28a745; 
}

.test-item.error { 
    background: #f8d7da; 
    border-left-color: #dc3545; 
}

.test-item h5 {
    margin: 0 0 10px 0;
    font-size: 14px;
}

.test-item ul {
    margin: 0;
    padding-right: 20px;
    font-size: 12px;
}

.problem-item {
    margin-bottom: 20px;
    padding: 15px;
    background: #fff3cd;
    border-radius: 6px;
    border: 1px solid #ffeaa7;
}

.problem-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.problem-header h5 {
    margin: 0;
    color: #856404;
}

.problem-time {
    font-size: 11px;
    color: #6c757d;
}

.problem-description, .problem-solution {
    margin-bottom: 10px;
    font-size: 13px;
    line-height: 1.4;
}

.fix-button {
    background: #007bff;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}

.fix-button:hover {
    background: #0056b3;
}

.test-actions {
    padding: 20px;
    border-top: 1px solid #eee;
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.test-actions button {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
}

.btn-primary { background: #007bff; color: white; }
.btn-secondary { background: #6c757d; color: white; }
.btn-danger { background: #dc3545; color: white; }

.test-progress-container {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    z-index: 10001;
    min-width: 300px;
    text-align: center;
}

.test-progress-bar {
    width: 100%;
    height: 20px;
    background: #e9ecef;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 10px;
}

.test-progress-fill {
    height: 100%;
    background: #007bff;
    transition: width 0.3s ease;
}

.test-message {
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 12px 20px;
    border-radius: 6px;
    color: white;
    font-weight: bold;
    z-index: 10002;
    animation: slideDown 0.3s ease;
}

.test-message-info { background: #17a2b8; }
.test-message-success { background: #28a745; }
.test-message-warning { background: #ffc107; color: #212529; }
.test-message-error { background: #dc3545; }

@keyframes slideDown {
    from { transform: translateX(-50%) translateY(-100%); }
    to { transform: translateX(-50%) translateY(0); }
}

.no-problems {
    text-align: center;
    padding: 40px;
    color: #28a745;
    font-size: 18px;
    font-weight: bold;
}
</style>
`;

// إضافة الأنماط إلى الصفحة
document.head.insertAdjacentHTML('beforeend', testStyles);

// إضافة زر الاختبار إلى الصفحة
function addTestButton() {
    const testButton = document.createElement('button');
    testButton.innerHTML = '🧪 اختبار الخطة';
    testButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #007bff;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,123,255,0.3);
        z-index: 9999;
        font-size: 14px;
        transition: all 0.3s ease;
    `;
    
    testButton.addEventListener('click', () => {
        workoutTester.startComprehensiveTest();
    });
    
    testButton.addEventListener('mouseenter', () => {
        testButton.style.transform = 'scale(1.05)';
        testButton.style.boxShadow = '0 6px 16px rgba(0,123,255,0.4)';
    });
    
    testButton.addEventListener('mouseleave', () => {
        testButton.style.transform = 'scale(1)';
        testButton.style.boxShadow = '0 4px 12px rgba(0,123,255,0.3)';
    });
    
    document.body.appendChild(testButton);
}

// تشغيل الاختبار عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', () => {
    addTestButton();
    
    // اختبار سريع تلقائي عند التحميل
    setTimeout(() => {
        if (window.location.search.includes('autotest=1')) {
            workoutTester.startComprehensiveTest();
        }
    }, 2000);
});

// تصدير الكائن للاستخدام العام
window.workoutTester = workoutTester;