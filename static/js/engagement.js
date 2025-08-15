// Psychological Engagement & Growth Hacking JavaScript

// Global variables
let userProgress = {
    workoutsCompleted: parseInt(localStorage.getItem('workoutsCompleted') || '0'),
    caloriesTracked: parseInt(localStorage.getItem('caloriesTracked') || '0'),
    tipsTried: parseInt(localStorage.getItem('tipsTried') || '0'),
    currentStreak: parseInt(localStorage.getItem('currentStreak') || '0'),
    lastWorkoutDate: localStorage.getItem('lastWorkoutDate') || null,
    totalPoints: parseInt(localStorage.getItem('totalPoints') || '0')
};

let currentChallenge = JSON.parse(localStorage.getItem('currentChallenge') || 'null');
let didYouKnowFacts = [];
let currentFactIndex = 0;

// Initialize engagement features
document.addEventListener('DOMContentLoaded', function() {
    initializeProgressTracker();
    initializeWeeklyChallenge();
    initializeDidYouKnow();
    initializePushNotifications();
    initializeEmailCapture();
    initializeStatsCounter();
    updateProgressDisplay();
    checkDailyWorkout();
    
    // Update progress tracker on scroll
    window.addEventListener('scroll', updateScrollProgress);
    
    // Initialize contextual linking
    initializeContextualLinks();
});

// Progress Tracker Functions
function initializeProgressTracker() {
    // Create progress tracker if it doesn't exist
    if (!document.querySelector('.progress-tracker')) {
        const progressTracker = document.createElement('div');
        progressTracker.className = 'progress-tracker';
        progressTracker.innerHTML = '<div class="progress-tracker-fill"></div>';
        document.body.prepend(progressTracker);
    }
}

function updateScrollProgress() {
    const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    const progressFill = document.querySelector('.progress-tracker-fill');
    if (progressFill) {
        progressFill.style.width = Math.min(scrolled, 100) + '%';
    }
}

function updateUserProgress(type, value = 1) {
    userProgress[type] += value;
    userProgress.totalPoints += value * 10; // 10 points per action
    
    // Save to localStorage
    Object.keys(userProgress).forEach(key => {
        localStorage.setItem(key, userProgress[key].toString());
    });
    
    updateProgressDisplay();
    checkAchievements();
}

function updateProgressDisplay() {
    // Update achievement card if exists
    const achievementCard = document.querySelector('.achievement-card');
    if (achievementCard) {
        const progressText = achievementCard.querySelector('.achievement-text');
        const progressFill = achievementCard.querySelector('.achievement-progress-fill');
        
        if (progressText && progressFill) {
            const totalActions = userProgress.workoutsCompleted + userProgress.caloriesTracked + userProgress.tipsTried;
            const progressPercentage = Math.min((totalActions / 50) * 100, 100); // Goal: 50 total actions
            
            progressText.textContent = `لقد أكملت ${progressPercentage.toFixed(0)}% من خطتك - استمر!`;
            progressFill.style.width = progressPercentage + '%';
        }
    }
    
    // Update stats counter
    updateStatsDisplay();
}

// Weekly Challenge Functions
function initializeWeeklyChallenge() {
    if (!currentChallenge || isChallengePeriodOver()) {
        generateNewChallenge();
    }
    displayCurrentChallenge();
}

function generateNewChallenge() {
    const challenges = [
        {
            title: "تحدي الـ 7 أيام",
            description: "أكمل 7 تمارين متتالية واحصل على خطة PDF مجانية",
            target: 7,
            current: 0,
            type: "workout_streak",
            reward: "خطة تمارين PDF مخصصة",
            endDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
            title: "تحدي حرق السعرات",
            description: "احرق 2000 سعرة حرارية هذا الأسبوع",
            target: 2000,
            current: 0,
            type: "calories_burned",
            reward: "دليل التغذية المتقدم",
            endDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
        },
        {
            title: "تحدي المعرفة",
            description: "اقرأ 10 نصائح صحية واطبق 5 منها",
            target: 10,
            current: 0,
            type: "tips_read",
            reward: "استشارة تغذية مجانية",
            endDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
        }
    ];
    
    currentChallenge = challenges[Math.floor(Math.random() * challenges.length)];
    localStorage.setItem('currentChallenge', JSON.stringify(currentChallenge));
}

function isChallengePeriodOver() {
    if (!currentChallenge || !currentChallenge.endDate) return true;
    return new Date() > new Date(currentChallenge.endDate);
}

function displayCurrentChallenge() {
    const challengeContainer = document.querySelector('.challenge-card');
    if (challengeContainer && currentChallenge) {
        const timeLeft = getTimeLeft(currentChallenge.endDate);
        const progressPercentage = (currentChallenge.current / currentChallenge.target) * 100;
        
        challengeContainer.innerHTML = `
            <h4><i class="fas fa-trophy me-2"></i>${currentChallenge.title}</h4>
            <p>${currentChallenge.description}</p>
            <div class="challenge-progress">
                <div class="achievement-progress">
                    <div class="achievement-progress-fill" style="width: ${progressPercentage}%"></div>
                </div>
                <small>${currentChallenge.current}/${currentChallenge.target}</small>
            </div>
            <div class="challenge-timer">
                <i class="fas fa-clock me-2"></i>متبقي: ${timeLeft}
            </div>
            <div class="mt-3">
                <strong>المكافأة:</strong> ${currentChallenge.reward}
            </div>
        `;
    }
}

function getTimeLeft(endDate) {
    const now = new Date();
    const end = new Date(endDate);
    const diff = end - now;
    
    if (diff <= 0) return "انتهى الوقت";
    
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    
    if (days > 0) return `${days} يوم و ${hours} ساعة`;
    return `${hours} ساعة`;
}

function updateChallengeProgress(type, value = 1) {
    if (currentChallenge && currentChallenge.type === type) {
        currentChallenge.current = Math.min(currentChallenge.current + value, currentChallenge.target);
        localStorage.setItem('currentChallenge', JSON.stringify(currentChallenge));
        displayCurrentChallenge();
        
        if (currentChallenge.current >= currentChallenge.target) {
            showChallengeCompleted();
        }
    }
}

function showChallengeCompleted() {
    showNotification('🎉 تهانينا! لقد أكملت التحدي الأسبوعي!', 'success');
    // Here you could trigger reward delivery
}

// Did You Know Functions
function initializeDidYouKnow() {
    didYouKnowFacts = [
        {
            icon: "💪",
            fact: "هل تعلم أن العضلات تحرق سعرات حرارية حتى أثناء الراحة؟ كل كيلو عضلات يحرق 13 سعرة يومياً!",
            link: "/calculators",
            linkText: "احسب معدل الحرق"
        },
        {
            icon: "🥤",
            fact: "شرب الماء البارد يحرق سعرات إضافية! جسمك يحتاج طاقة لتدفئة الماء لدرجة حرارة الجسم.",
            link: "/meal-generator",
            linkText: "خطط وجباتك"
        },
        {
            icon: "😴",
            fact: "النوم أقل من 7 ساعات يزيد هرمون الجوع ويقلل هرمون الشبع، مما يصعب فقدان الوزن.",
            link: "/tips",
            linkText: "نصائح النوم"
        },
        {
            icon: "🏃‍♂️",
            fact: "المشي لمدة 30 دقيقة يومياً يقلل خطر أمراض القلب بنسبة 35%!",
            link: "/workout-plans",
            linkText: "خطط التمارين"
        },
        {
            icon: "🥗",
            fact: "الألياف تجعلك تشعر بالشبع لفترة أطول وتحرق 10% سعرات إضافية أثناء الهضم.",
            link: "/food-calories-guide",
            linkText: "دليل السعرات"
        }
    ];
    
    displayDidYouKnow();
    
    // Change fact every 30 seconds
    setInterval(rotateDidYouKnow, 30000);
}

function displayDidYouKnow() {
    const container = document.querySelector('.did-you-know');
    if (container && didYouKnowFacts.length > 0) {
        const fact = didYouKnowFacts[currentFactIndex];
        container.innerHTML = `
            <div class="did-you-know-icon">${fact.icon}</div>
            <h5>هل تعلم؟</h5>
            <p>${fact.fact}</p>
            <a href="${fact.link}" class="btn btn-outline-primary btn-sm">
                ${fact.linkText} <i class="fas fa-arrow-left ms-2"></i>
            </a>
        `;
        
        container.addEventListener('click', () => {
            updateUserProgress('tipsTried');
            updateChallengeProgress('tips_read');
        });
    }
}

function rotateDidYouKnow() {
    currentFactIndex = (currentFactIndex + 1) % didYouKnowFacts.length;
    displayDidYouKnow();
}

// Push Notifications
function initializePushNotifications() {
    if ('Notification' in window && 'serviceWorker' in navigator) {
        requestNotificationPermission();
        scheduleNotifications();
    }
}

function requestNotificationPermission() {
    if (Notification.permission === 'default') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                showNotification('🎉 رائع! ستحصل على تذكيرات يومية لمساعدتك في رحلتك الصحية', 'success');
            }
        });
    }
}

function scheduleNotifications() {
    // Schedule daily workout reminder
    const now = new Date();
    const tomorrow = new Date(now);
    tomorrow.setDate(tomorrow.getDate() + 1);
    tomorrow.setHours(9, 0, 0, 0); // 9 AM
    
    const timeUntilTomorrow = tomorrow.getTime() - now.getTime();
    
    setTimeout(() => {
        sendNotification('💪 وقت التمرين!', 'ابدأ يومك بتمرين قصير لمدة 10 دقائق');
        // Schedule for next day
        setInterval(() => {
            sendNotification('💪 وقت التمرين!', 'ابدأ يومك بتمرين قصير لمدة 10 دقائق');
        }, 24 * 60 * 60 * 1000);
    }, timeUntilTomorrow);
}

function sendNotification(title, body) {
    if (Notification.permission === 'granted') {
        new Notification(title, {
            body: body,
            icon: '/static/images/logo.png',
            badge: '/static/images/badge.png'
        });
    }
}

// Email Capture
function initializeEmailCapture() {
    const emailForm = document.querySelector('.email-form');
    if (emailForm) {
        emailForm.addEventListener('submit', handleEmailSubmit);
    }
}

function handleEmailSubmit(e) {
    e.preventDefault();
    const emailInput = e.target.querySelector('.email-input');
    const email = emailInput.value.trim();
    
    if (email && isValidEmail(email)) {
        // Save email to localStorage (in real app, send to server)
        localStorage.setItem('userEmail', email);
        
        showNotification('🎉 شكراً! ستحصل على خطة مجانية ونصائح أسبوعية', 'success');
        
        // Hide email capture form
        const emailCapture = document.querySelector('.email-capture');
        if (emailCapture) {
            emailCapture.style.display = 'none';
        }
        
        // Award points
        updateUserProgress('totalPoints', 50);
    } else {
        showNotification('⚠️ الرجاء إدخال بريد إلكتروني صحيح', 'warning');
    }
}

function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Stats Counter
function initializeStatsCounter() {
    updateStatsDisplay();
    animateCounters();
}

function updateStatsDisplay() {
    const statsContainer = document.querySelector('.stats-counter');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <h4 class="mb-4">إنجازاتك</h4>
            <div class="row">
                <div class="col-4">
                    <div class="stat-item">
                        <span class="stat-number" data-target="${userProgress.workoutsCompleted}">0</span>
                        <div class="stat-label">تمرين مكتمل</div>
                    </div>
                </div>
                <div class="col-4">
                    <div class="stat-item">
                        <span class="stat-number" data-target="${userProgress.caloriesTracked}">0</span>
                        <div class="stat-label">سعرة متتبعة</div>
                    </div>
                </div>
                <div class="col-4">
                    <div class="stat-item">
                        <span class="stat-number" data-target="${userProgress.tipsTried}">0</span>
                        <div class="stat-label">نصيحة مطبقة</div>
                    </div>
                </div>
            </div>
            <div class="mt-4">
                <h5>النقاط الإجمالية: <span class="text-warning">${userProgress.totalPoints}</span></h5>
            </div>
        `;
        
        animateCounters();
    }
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const increment = target / 50;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.floor(current);
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target;
            }
        };
        
        updateCounter();
    });
}

// Contextual Links
function initializeContextualLinks() {
    const contextualLinks = [
        {
            trigger: "تخسيس",
            title: "تريد حرق الدهون؟",
            description: "شاهد تمارين الكارديو المتخصصة",
            link: "/workout-plans",
            icon: "🔥"
        },
        {
            trigger: "عضلات",
            title: "تريد بناء العضلات؟",
            description: "اكتشف الأطعمة عالية البروتين",
            link: "/food-calories-guide",
            icon: "💪"
        },
        {
            trigger: "سعرات",
            title: "تريد حساب السعرات؟",
            description: "استخدم حاسبة السعرات المتقدمة",
            link: "/calculators",
            icon: "🧮"
        }
    ];
    
    // Add contextual links based on page content
    const pageContent = document.body.textContent.toLowerCase();
    contextualLinks.forEach(link => {
        if (pageContent.includes(link.trigger)) {
            addContextualLink(link);
        }
    });
}

function addContextualLink(linkData) {
    const container = document.querySelector('.container');
    if (container) {
        const contextualDiv = document.createElement('div');
        contextualDiv.className = 'contextual-link';
        contextualDiv.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="me-3" style="font-size: 2rem;">${linkData.icon}</div>
                <div>
                    <h6 class="mb-1">${linkData.title}</h6>
                    <p class="mb-0">${linkData.description}</p>
                </div>
                <div class="ms-auto">
                    <a href="${linkData.link}" class="btn btn-outline-primary btn-sm">
                        اكتشف <i class="fas fa-arrow-left ms-1"></i>
                    </a>
                </div>
            </div>
        `;
        
        container.appendChild(contextualDiv);
    }
}

// Daily Workout Video
function checkDailyWorkout() {
    const today = new Date().toDateString();
    const lastVideoDate = localStorage.getItem('lastVideoDate');
    
    if (lastVideoDate !== today) {
        loadDailyWorkoutVideo();
        localStorage.setItem('lastVideoDate', today);
    }
}

function loadDailyWorkoutVideo() {
    const workoutVideos = [
        {
            title: "تمرين الصباح - 10 دقائق",
            description: "ابدأ يومك بطاقة إيجابية",
            thumbnail: "/static/images/workout1.jpg",
            duration: "10:00"
        },
        {
            title: "تمرين البطن السريع",
            description: "5 دقائق لعضلات بطن قوية",
            thumbnail: "/static/images/workout2.jpg",
            duration: "05:00"
        },
        {
            title: "تمرين الكارديو المنزلي",
            description: "احرق السعرات في المنزل",
            thumbnail: "/static/images/workout3.jpg",
            duration: "15:00"
        }
    ];
    
    const todayVideo = workoutVideos[new Date().getDay() % workoutVideos.length];
    displayDailyVideo(todayVideo);
}

function displayDailyVideo(video) {
    const videoContainer = document.querySelector('.daily-workout-video');
    if (videoContainer) {
        videoContainer.innerHTML = `
            <div class="card border-0 shadow-lg">
                <div class="position-relative">
                    <img src="${video.thumbnail}" class="card-img-top" alt="${video.title}" style="height: 200px; object-fit: cover;">
                    <div class="position-absolute top-50 start-50 translate-middle">
                        <button class="btn btn-primary btn-lg rounded-circle" onclick="playWorkoutVideo()">
                            <i class="fas fa-play"></i>
                        </button>
                    </div>
                    <span class="badge bg-dark position-absolute bottom-0 end-0 m-2">${video.duration}</span>
                </div>
                <div class="card-body">
                    <h5 class="card-title">${video.title}</h5>
                    <p class="card-text">${video.description}</p>
                    <button class="btn btn-primary" onclick="startWorkout()">
                        ابدأ التمرين <i class="fas fa-play ms-2"></i>
                    </button>
                </div>
            </div>
        `;
    }
}

function startWorkout() {
    updateUserProgress('workoutsCompleted');
    updateChallengeProgress('workout_streak');
    showNotification('💪 رائع! لقد بدأت تمرين اليوم', 'success');
}

// Utility Functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function checkAchievements() {
    const achievements = [
        { threshold: 5, message: '🎉 أول 5 تمارين! أنت في الطريق الصحيح' },
        { threshold: 10, message: '🔥 10 تمارين مكتملة! استمر في التقدم' },
        { threshold: 25, message: '⭐ 25 تمرين! أنت بطل حقيقي' },
        { threshold: 50, message: '👑 50 تمرين! لقد أصبحت خبيراً' }
    ];
    
    achievements.forEach(achievement => {
        if (userProgress.workoutsCompleted === achievement.threshold) {
            showNotification(achievement.message, 'success');
        }
    });
}

// Export functions for global use
window.engagementFunctions = {
    updateUserProgress,
    updateChallengeProgress,
    startWorkout,
    showNotification
};