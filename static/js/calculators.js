// حاسبات اللياقة البدنية - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // BMR Calculator
    document.getElementById('bmrForm').addEventListener('submit', function(e) {
        e.preventDefault();
        calculateBMR();
    });

    // TDEE Calculator
    document.getElementById('tdeeForm').addEventListener('submit', function(e) {
        e.preventDefault();
        calculateTDEE();
    });

    // Macros Calculator
    document.getElementById('macrosForm').addEventListener('submit', function(e) {
        e.preventDefault();
        calculateMacros();
    });

    // Ideal Weight Calculator
    document.getElementById('idealWeightForm').addEventListener('submit', function(e) {
        e.preventDefault();
        calculateIdealWeight();
    });

    // Water Intake Calculator
    document.getElementById('waterForm').addEventListener('submit', function(e) {
        e.preventDefault();
        calculateWaterIntake();
    });
});

// BMR Calculation (Mifflin-St Jeor Equation)
function calculateBMR() {
    const age = parseInt(document.getElementById('bmrAge').value);
    const gender = document.getElementById('bmrGender').value;
    const weight = parseFloat(document.getElementById('bmrWeight').value);
    const height = parseInt(document.getElementById('bmrHeight').value);

    if (!age || !gender || !weight || !height) {
        alert('الرجاء ملء جميع الحقول');
        return;
    }

    let bmr;
    if (gender === 'male') {
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5;
    } else {
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161;
    }

    showResult('bmrResult', 'bmrValue', 
        `معدل الأيض الأساسي الخاص بك هو: <strong>${Math.round(bmr)} سعرة حرارية/يوم</strong><br>
        <small>هذا هو عدد السعرات التي يحرقها جسمك في حالة الراحة التامة</small>`
    );
}

// TDEE Calculation
function calculateTDEE() {
    const age = parseInt(document.getElementById('tdeeAge').value);
    const gender = document.getElementById('tdeeGender').value;
    const weight = parseFloat(document.getElementById('tdeeWeight').value);
    const height = parseInt(document.getElementById('tdeeHeight').value);
    const activity = parseFloat(document.getElementById('tdeeActivity').value);

    if (!age || !gender || !weight || !height || !activity) {
        alert('الرجاء ملء جميع الحقول');
        return;
    }

    // Calculate BMR first
    let bmr;
    if (gender === 'male') {
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5;
    } else {
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161;
    }

    const tdee = bmr * activity;

    const activityLevels = {
        '1.2': 'قليل الحركة',
        '1.375': 'نشاط خفيف',
        '1.55': 'نشاط متوسط',
        '1.725': 'نشاط عالي',
        '1.9': 'نشاط شديد'
    };

    showResult('tdeeResult', 'tdeeValue', 
        `إجمالي الطاقة المستهلكة يومياً: <strong>${Math.round(tdee)} سعرة حرارية/يوم</strong><br>
        <small>مستوى النشاط: ${activityLevels[activity.toString()]}</small><br>
        <small>للتخسيس: ${Math.round(tdee - 500)} سعرة | للزيادة: ${Math.round(tdee + 500)} سعرة</small>`
    );
}

// Macros Calculation
function calculateMacros() {
    const calories = parseInt(document.getElementById('macrosCalories').value);
    const goal = document.getElementById('macrosGoal').value;
    const weight = parseFloat(document.getElementById('macrosWeight').value);

    if (!calories || !goal || !weight) {
        alert('الرجاء ملء جميع الحقول');
        return;
    }

    let proteinRatio, carbRatio, fatRatio;

    switch(goal) {
        case 'weight_loss':
            proteinRatio = 0.35; // 35% protein
            carbRatio = 0.30;    // 30% carbs
            fatRatio = 0.35;     // 35% fats
            break;
        case 'maintenance':
            proteinRatio = 0.25; // 25% protein
            carbRatio = 0.45;    // 45% carbs
            fatRatio = 0.30;     // 30% fats
            break;
        case 'muscle_gain':
            proteinRatio = 0.30; // 30% protein
            carbRatio = 0.50;    // 50% carbs
            fatRatio = 0.20;     // 20% fats
            break;
    }

    const proteinCalories = calories * proteinRatio;
    const carbCalories = calories * carbRatio;
    const fatCalories = calories * fatRatio;

    const proteinGrams = Math.round(proteinCalories / 4);
    const carbGrams = Math.round(carbCalories / 4);
    const fatGrams = Math.round(fatCalories / 9);

    const goalNames = {
        'weight_loss': 'تخسيس',
        'maintenance': 'الحفاظ على الوزن',
        'muscle_gain': 'بناء عضلات'
    };

    showResult('macrosResult', 'macrosValue', 
        `<div class="macro-item">
            <strong>البروتين:</strong> ${proteinGrams} جرام (${Math.round(proteinCalories)} سعرة)
        </div>
        <div class="macro-item">
            <strong>الكربوهيدرات:</strong> ${carbGrams} جرام (${Math.round(carbCalories)} سعرة)
        </div>
        <div class="macro-item">
            <strong>الدهون:</strong> ${fatGrams} جرام (${Math.round(fatCalories)} سعرة)
        </div>
        <small>الهدف: ${goalNames[goal]}</small>`
    );
}

// Ideal Weight Calculation (Multiple formulas)
function calculateIdealWeight() {
    const height = parseInt(document.getElementById('idealHeight').value);
    const gender = document.getElementById('idealGender').value;
    const currentWeight = parseFloat(document.getElementById('currentWeight').value);

    if (!height || !gender) {
        alert('الرجاء ملء الحقول المطلوبة');
        return;
    }

    const heightInMeters = height / 100;

    // BMI-based ideal weight (BMI 22)
    const idealWeightBMI = 22 * (heightInMeters * heightInMeters);

    // Robinson Formula
    let idealWeightRobinson;
    if (gender === 'male') {
        idealWeightRobinson = 52 + (1.9 * ((height - 152.4) / 2.54));
    } else {
        idealWeightRobinson = 49 + (1.7 * ((height - 152.4) / 2.54));
    }

    // Miller Formula
    let idealWeightMiller;
    if (gender === 'male') {
        idealWeightMiller = 56.2 + (1.41 * ((height - 152.4) / 2.54));
    } else {
        idealWeightMiller = 53.1 + (1.36 * ((height - 152.4) / 2.54));
    }

    const averageIdeal = (idealWeightBMI + idealWeightRobinson + idealWeightMiller) / 3;

    let resultText = `
        <div class="macro-item">
            <strong>الوزن المثالي (متوسط):</strong> ${Math.round(averageIdeal)} كجم
        </div>
        <div class="macro-item">
            <strong>النطاق الصحي:</strong> ${Math.round(averageIdeal - 5)} - ${Math.round(averageIdeal + 5)} كجم
        </div>
    `;

    if (currentWeight) {
        const difference = currentWeight - averageIdeal;
        if (Math.abs(difference) <= 5) {
            resultText += `<div class="macro-item" style="border-right-color: #28a745;">
                <strong>وضعك الحالي:</strong> وزنك مثالي! 🎉
            </div>`;
        } else if (difference > 5) {
            resultText += `<div class="macro-item" style="border-right-color: #dc3545;">
                <strong>وضعك الحالي:</strong> تحتاج لتخسيس ${Math.round(difference)} كجم
            </div>`;
        } else {
            resultText += `<div class="macro-item" style="border-right-color: #ffc107;">
                <strong>وضعك الحالي:</strong> تحتاج لزيادة ${Math.round(Math.abs(difference))} كجم
            </div>`;
        }
    }

    showResult('idealWeightResult', 'idealWeightValue', resultText);
}

// Water Intake Calculation
function calculateWaterIntake() {
    const weight = parseFloat(document.getElementById('waterWeight').value);
    const activity = document.getElementById('waterActivity').value;
    const climate = document.getElementById('waterClimate').value;

    if (!weight || !activity || !climate) {
        alert('الرجاء ملء جميع الحقول');
        return;
    }

    // Base calculation: 35ml per kg of body weight
    let baseWater = weight * 35;

    // Activity multiplier
    const activityMultipliers = {
        'low': 1.0,
        'moderate': 1.2,
        'high': 1.5
    };

    // Climate multiplier
    const climateMultipliers = {
        'normal': 1.0,
        'hot': 1.3,
        'humid': 1.2
    };

    const totalWater = baseWater * activityMultipliers[activity] * climateMultipliers[climate];
    const liters = totalWater / 1000;
    const glasses = Math.round(totalWater / 250); // 250ml per glass

    const activityNames = {
        'low': 'قليل الحركة',
        'moderate': 'نشاط متوسط',
        'high': 'نشاط عالي'
    };

    const climateNames = {
        'normal': 'معتدل',
        'hot': 'حار',
        'humid': 'رطب'
    };

    showResult('waterResult', 'waterValue', 
        `<div class="macro-item">
            <strong>احتياجك اليومي من الماء:</strong> ${liters.toFixed(1)} لتر
        </div>
        <div class="macro-item">
            <strong>عدد الأكواب:</strong> ${glasses} كوب (250 مل)
        </div>
        <div class="macro-item">
            <strong>بالمليلتر:</strong> ${Math.round(totalWater)} مل
        </div>
        <small>مستوى النشاط: ${activityNames[activity]} | المناخ: ${climateNames[climate]}</small>`
    );
}

// Helper function to show results
function showResult(resultId, valueId, content) {
    const resultDiv = document.getElementById(resultId);
    const valueDiv = document.getElementById(valueId);
    
    valueDiv.innerHTML = content;
    resultDiv.style.display = 'block';
    
    // Smooth scroll to result
    resultDiv.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'nearest' 
    });
}

// Add loading animation to buttons
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const button = this.querySelector('button[type="submit"]');
        button.classList.add('loading');
        
        setTimeout(() => {
            button.classList.remove('loading');
        }, 1000);
    });
});

// Add smooth animations on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all calculator cards
document.querySelectorAll('.calculator-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});