// متغيرات عامة
let currentStep = 1;
let userSelections = {
    goal: '',
    workout: '',
    meals: [],
    habits: []
};

// تهيئة الصفحة
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Weight Loss Guide initialized');
    setupEventListeners();
    updateProgress();
});

// إعداد مستمعي الأحداث
function setupEventListeners() {
    // مستمعي أحداث اختيار الخيارات
    document.querySelectorAll('.card-option').forEach(card => {
        card.addEventListener('click', function() {
            handleCardSelection(this);
        });
    });
}

// التعامل مع اختيار البطاقات
function handleCardSelection(selectedCard) {
    const step = getCurrentStepNumber();
    
    if (step === 1) {
        // اختيار الهدف (اختيار واحد فقط)
        document.querySelectorAll('#step1 .card-option').forEach(card => {
            card.classList.remove('selected');
        });
        selectedCard.classList.add('selected');
        userSelections.goal = selectedCard.dataset.goal;
        document.getElementById('nextBtn1').disabled = false;
        
    } else if (step === 2) {
        // اختيار نظام التمرين (اختيار واحد فقط)
        document.querySelectorAll('#step2 .card-option').forEach(card => {
            card.classList.remove('selected');
        });
        selectedCard.classList.add('selected');
        userSelections.workout = selectedCard.dataset.workout;
        document.getElementById('nextBtn2').disabled = false;
        
    } else if (step === 3) {
        // اختيار الوجبات (اختيارات متعددة)
        selectedCard.classList.toggle('selected');
        
        const mealType = selectedCard.dataset.meal;
        if (selectedCard.classList.contains('selected')) {
            if (!userSelections.meals.includes(mealType)) {
                userSelections.meals.push(mealType);
            }
        } else {
            userSelections.meals = userSelections.meals.filter(meal => meal !== mealType);
        }
        
        document.getElementById('nextBtn3').disabled = userSelections.meals.length === 0;
        
    } else if (step === 4) {
        // اختيار العادات (اختيارات متعددة)
        selectedCard.classList.toggle('selected');
        
        const habitType = selectedCard.dataset.habit;
        if (selectedCard.classList.contains('selected')) {
            if (!userSelections.habits.includes(habitType)) {
                userSelections.habits.push(habitType);
            }
        } else {
            userSelections.habits = userSelections.habits.filter(habit => habit !== habitType);
        }
        
        document.getElementById('nextBtn4').disabled = userSelections.habits.length === 0;
    }
    
    console.log('User selections updated:', userSelections);
}

// الحصول على رقم الخطوة الحالية
function getCurrentStepNumber() {
    return currentStep;
}

// الانتقال للخطوة التالية
function nextStep() {
    if (currentStep < 5) {
        // إخفاء الخطوة الحالية
        document.getElementById(`step${currentStep}`).classList.remove('active');
        
        // الانتقال للخطوة التالية
        currentStep++;
        
        // إظهار الخطوة الجديدة
        document.getElementById(`step${currentStep}`).classList.add('active');
        
        // تحديث شريط التقدم
        updateProgress();
        
        // إذا وصلنا للخطوة الأخيرة، إنشاء الخطة
        if (currentStep === 5) {
            generateFinalPlan();
        }
        
        // التمرير لأعلى الصفحة
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// العودة للخطوة السابقة
function prevStep() {
    if (currentStep > 1) {
        // إخفاء الخطوة الحالية
        document.getElementById(`step${currentStep}`).classList.remove('active');
        
        // العودة للخطوة السابقة
        currentStep--;
        
        // إظهار الخطوة السابقة
        document.getElementById(`step${currentStep}`).classList.add('active');
        
        // تحديث شريط التقدم
        updateProgress();
        
        // التمرير لأعلى الصفحة
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// تحديث شريط التقدم
function updateProgress() {
    const progress = (currentStep / 5) * 100;
    document.getElementById('progressBar').style.width = `${progress}%`;
    document.getElementById('progressText').textContent = `الخطوة ${currentStep} من 5`;
}

// إنشاء الخطة النهائية
function generateFinalPlan() {
    console.log('🎯 Generating final plan with selections:', userSelections);
    
    const planContainer = document.getElementById('finalPlan');
    
    // إنشاء محتوى الخطة
    const planHTML = `
        <div class="text-center mb-4">
            <h3 class="text-primary"><i class="fas fa-trophy me-2"></i>تهانينا! خطتك جاهزة</h3>
            <p class="lead">${getMotivationalMessage()}</p>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card h-100" style="border: none; border-radius: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <div class="card-body">
                        <h5><i class="fas fa-target me-2"></i>هدفك</h5>
                        <p class="mb-0">${getGoalDescription(userSelections.goal)}</p>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="card h-100" style="border: none; border-radius: 15px; background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white;">
                    <div class="card-body">
                        <h5><i class="fas fa-dumbbell me-2"></i>نظام التمرين</h5>
                        <p class="mb-0">${getWorkoutDescription(userSelections.workout)}</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-4">
                <div class="card h-100" style="border: none; border-radius: 15px; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);">
                    <div class="card-body">
                        <h5><i class="fas fa-utensils me-2"></i>وجباتك المختارة</h5>
                        <ul class="list-unstyled">
                            ${userSelections.meals.map(meal => `<li><i class="fas fa-check text-success me-2"></i>${getMealDescription(meal)}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="col-md-6 mb-4">
                <div class="card h-100" style="border: none; border-radius: 15px; background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);">
                    <div class="card-body">
                        <h5><i class="fas fa-leaf me-2"></i>عاداتك الجديدة</h5>
                        <ul class="list-unstyled">
                            ${userSelections.habits.map(habit => `<li><i class="fas fa-star text-warning me-2"></i>${getHabitDescription(habit)}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card" style="border: none; border-radius: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <div class="card-body text-center">
                <h5><i class="fas fa-calendar-alt me-2"></i>خطة أسبوعية مقترحة</h5>
                ${getWeeklyPlan()}
            </div>
        </div>
        
        <div class="motivational-quote mt-4" style="background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); color: #333;">
            <h4><i class="fas fa-heart me-2"></i>رسالة تحفيزية خاصة</h4>
            <p class="mb-0">${getPersonalizedMotivation()}</p>
        </div>
    `;
    
    planContainer.innerHTML = planHTML;
    
    // إرسال البيانات للخادم (اختياري)
    savePlanToServer();
}

// الحصول على وصف الهدف
function getGoalDescription(goal) {
    const descriptions = {
        'health': 'تحسين الصحة العامة والتخلص من المشاكل الصحية',
        'appearance': 'تحسين المظهر والحصول على جسم متناسق',
        'fitness': 'زيادة اللياقة البدنية وتحسين الأداء الرياضي'
    };
    return descriptions[goal] || 'هدف صحي عام';
}

// الحصول على وصف نظام التمرين
function getWorkoutDescription(workout) {
    const descriptions = {
        'hiit': 'تمارين عالية الكثافة (HIIT) - 15-25 دقيقة، 3-4 مرات أسبوعياً',
        'liss': 'تمارين منخفضة الكثافة (LISS) - 30-60 دقيقة، 4-6 مرات أسبوعياً',
        'combined': 'تمارين مقاومة + كارديو - 45-60 دقيقة، 4-5 مرات أسبوعياً'
    };
    return descriptions[workout] || 'نظام تمرين متوازن';
}

// الحصول على وصف الوجبة
function getMealDescription(meal) {
    const descriptions = {
        'breakfast-1': 'شوفان بالفواكه (300 سعرة)',
        'breakfast-2': 'بيض مسلوق مع خبز أسمر (280 سعرة)',
        'lunch-1': 'سلطة دجاج مشوي (400 سعرة)',
        'lunch-2': 'سمك مع أرز بني (450 سعرة)',
        'snack-1': 'مكسرات وفواكه (200 سعرة)',
        'snack-2': 'عصير أخضر (150 سعرة)'
    };
    return descriptions[meal] || 'وجبة صحية';
}

// الحصول على وصف العادة
function getHabitDescription(habit) {
    const descriptions = {
        'water': 'شرب الماء قبل الوجبات',
        'sleep': 'النوم 7-8 ساعات يومياً',
        'walking': 'المشي بعد الأكل',
        'portions': 'التحكم في حجم الحصص',
        'planning': 'تخطيط الوجبات مسبقاً',
        'mindful': 'الأكل الواعي'
    };
    return descriptions[habit] || 'عادة صحية';
}

// الحصول على رسالة تحفيزية
function getMotivationalMessage() {
    const messages = [
        'أنت على بعد خطوة واحدة من تحقيق هدفك!',
        'رحلة الألف ميل تبدأ بخطوة واحدة، وأنت بدأت بالفعل!',
        'كل يوم تلتزم فيه بخطتك هو استثمار في صحتك ومستقبلك!',
        'النجاح ليس وجهة، بل رحلة من العادات الصحية اليومية!'
    ];
    return messages[Math.floor(Math.random() * messages.length)];
}

// الحصول على خطة أسبوعية
function getWeeklyPlan() {
    const workoutPlans = {
        'hiit': `
            <div class="row text-start">
                <div class="col-md-6">
                    <p><strong>الأحد:</strong> HIIT كامل الجسم (20 دقيقة)</p>
                    <p><strong>الاثنين:</strong> راحة أو مشي خفيف</p>
                    <p><strong>الثلاثاء:</strong> HIIT الجزء العلوي (15 دقيقة)</p>
                    <p><strong>الأربعاء:</strong> راحة</p>
                </div>
                <div class="col-md-6">
                    <p><strong>الخميس:</strong> HIIT الجزء السفلي (20 دقيقة)</p>
                    <p><strong>الجمعة:</strong> راحة أو يوجا</p>
                    <p><strong>السبت:</strong> HIIT كارديو (15 دقيقة)</p>
                </div>
            </div>
        `,
        'liss': `
            <div class="row text-start">
                <div class="col-md-6">
                    <p><strong>الأحد:</strong> مشي سريع (45 دقيقة)</p>
                    <p><strong>الاثنين:</strong> سباحة أو دراجة (30 دقيقة)</p>
                    <p><strong>الثلاثاء:</strong> مشي أو جري خفيف (40 دقيقة)</p>
                    <p><strong>الأربعاء:</strong> يوجا أو تمدد (30 دقيقة)</p>
                </div>
                <div class="col-md-6">
                    <p><strong>الخميس:</strong> دراجة أو إليبتيكال (35 دقيقة)</p>
                    <p><strong>الجمعة:</strong> مشي في الطبيعة (50 دقيقة)</p>
                    <p><strong>السبت:</strong> راحة أو نشاط خفيف</p>
                </div>
            </div>
        `,
        'combined': `
            <div class="row text-start">
                <div class="col-md-6">
                    <p><strong>الأحد:</strong> مقاومة الجزء العلوي + كارديو (50 دقيقة)</p>
                    <p><strong>الاثنين:</strong> كارديو خفيف (30 دقيقة)</p>
                    <p><strong>الثلاثاء:</strong> مقاومة الجزء السفلي + كارديو (50 دقيقة)</p>
                    <p><strong>الأربعاء:</strong> راحة أو يوجا</p>
                </div>
                <div class="col-md-6">
                    <p><strong>الخميس:</strong> مقاومة كامل الجسم (45 دقيقة)</p>
                    <p><strong>الجمعة:</strong> كارديو متوسط الكثافة (40 دقيقة)</p>
                    <p><strong>السبت:</strong> راحة أو نشاط ترفيهي</p>
                </div>
            </div>
        `
    };
    
    return workoutPlans[userSelections.workout] || '<p>خطة تمرين متوازنة حسب اختيارك</p>';
}

// الحصول على رسالة تحفيزية شخصية
function getPersonalizedMotivation() {
    const goalMotivations = {
        'health': 'صحتك هي أغلى ما تملك، وكل خطوة تخطوها اليوم هي استثمار في مستقبل أكثر صحة وحيوية. تذكر أن التغيير الحقيقي يحدث من الداخل!',
        'appearance': 'الجمال الحقيقي يأتي من الثقة بالنفس والصحة الجيدة. أنت تستحق أن تشعر بالرضا عن نفسك، وكل يوم تلتزم فيه بخطتك يقربك أكثر من هدفك!',
        'fitness': 'القوة الحقيقية تأتي من الإصرار والمثابرة. أنت تبني ليس فقط عضلات أقوى، بل شخصية أقوى وإرادة لا تقهر!'
    };
    
    return goalMotivations[userSelections.goal] || 'أنت قادر على تحقيق أي شيء تضع عقلك عليه. ثق بنفسك والتزم بخطتك!';
}

// حفظ الخطة في الخادم
function savePlanToServer() {
    const planData = {
        goal: userSelections.goal,
        workout: userSelections.workout,
        meals: userSelections.meals,
        habits: userSelections.habits,
        timestamp: new Date().toISOString()
    };
    
    fetch('/api/save-weight-loss-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(planData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('✅ Plan saved successfully:', data);
    })
    .catch(error => {
        console.error('❌ Error saving plan:', error);
    });
}

// تحميل الخطة
function downloadPlan() {
    window.print();
}

// البدء من جديد
function startOver() {
    if (confirm('هل أنت متأكد من أنك تريد البدء من جديد؟')) {
        // إعادة تعيين المتغيرات
        currentStep = 1;
        userSelections = {
            goal: '',
            workout: '',
            meals: [],
            habits: []
        };
        
        // إخفاء جميع الخطوات
        document.querySelectorAll('.step-container').forEach(step => {
            step.classList.remove('active');
        });
        
        // إظهار الخطوة الأولى
        document.getElementById('step1').classList.add('active');
        
        // إزالة جميع التحديدات
        document.querySelectorAll('.card-option').forEach(card => {
            card.classList.remove('selected');
        });
        
        // تعطيل أزرار التالي
        document.querySelectorAll('[id^="nextBtn"]').forEach(btn => {
            btn.disabled = true;
        });
        
        // تحديث شريط التقدم
        updateProgress();
        
        // التمرير لأعلى الصفحة
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// دوال مساعدة إضافية
function showStep(stepNumber) {
    // إخفاء جميع الخطوات
    document.querySelectorAll('.step-container').forEach(step => {
        step.classList.remove('active');
    });
    
    // إظهار الخطوة المطلوبة
    document.getElementById(`step${stepNumber}`).classList.add('active');
    currentStep = stepNumber;
    updateProgress();
}

// تصدير الدوال للاستخدام العام
window.nextStep = nextStep;
window.prevStep = prevStep;
window.downloadPlan = downloadPlan;
window.startOver = startOver;