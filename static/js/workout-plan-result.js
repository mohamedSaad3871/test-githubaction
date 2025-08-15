// Workout Plan Result - Dynamic Content Generator

// Motivational Tips Data
const goalTips = {
    weight_loss: {
        title: 'نصائح حرق الدهون وإنقاص الوزن 🔥',
        tips: [
            {
                icon: '🏃‍♀️',
                title: 'تمارين الكارديو هي سلاحك السري',
                content: 'امشي 30 دقيقة يومياً أو اعمل تمارين HIIT لمدة 15 دقيقة. الكارديو يحرق السعرات ويقوي القلب!'
            },
            {
                icon: '🥗',
                title: 'اتبع قاعدة الطبق الصحي',
                content: 'نصف طبقك خضار، ربع بروتين، ربع كربوهيدرات معقدة. هذا يضمن الشبع مع سعرات أقل!'
            },
            {
                icon: '💧',
                title: 'الماء شريكك في الرحلة',
                content: 'اشرب كوب ماء قبل كل وجبة بـ30 دقيقة. هذا يساعد على الشبع ويسرع الحرق!'
            },
            {
                icon: '😴',
                title: 'النوم الجيد = حرق أفضل',
                content: 'نم 7-8 ساعات يومياً. قلة النوم تزيد هرمون الجوع وتبطئ عملية الحرق!'
            },
            {
                icon: '🎯',
                title: 'فكر في التقدم وليس الكمال',
                content: 'كل خطوة صغيرة تقربك من هدفك. لا تستسلم إذا أخطأت يوماً، المهم تكمل الرحلة!'
            }
        ],
        avoidTip: {
            icon: '⚠️',
            title: 'تجنب هذا الخطأ الشائع',
            content: 'لا تقلل السعرات بشكل مفرط! هذا يبطئ الحرق ويفقدك العضلات. اهدف لنقص 500 سعرة يومياً فقط.'
        }
    },
    weight_gain: {
        title: 'نصائح زيادة الوزن الصحية 💪',
        tips: [
            {
                icon: '🍽️',
                title: 'كل وجبات صغيرة ومتكررة',
                content: '5-6 وجبات صغيرة أفضل من 3 وجبات كبيرة. هذا يساعد جسمك على امتصاص العناصر الغذائية بشكل أفضل!'
            },
            {
                icon: '🥜',
                title: 'اختر الدهون الصحية',
                content: 'المكسرات، الأفوكادو، زيت الزيتون. هذه مصادر ممتازة للسعرات الصحية والفيتامينات!'
            },
            {
                icon: '🏋️‍♂️',
                title: 'ركز على تمارين القوة',
                content: 'تمارين الأثقال تبني العضلات وتزيد الوزن الصحي. ابدأ بأوزان خفيفة وزد تدريجياً!'
            },
            {
                icon: '🥛',
                title: 'البروتين بعد التمرين مباشرة',
                content: 'اشرب شيك البروتين خلال 30 دقيقة من التمرين. هذا يساعد على بناء العضلات بسرعة!'
            }
        ],
        avoidTip: {
            icon: '⚠️',
            title: 'تجنب هذا الخطأ الشائع',
            content: 'لا تأكل الوجبات السريعة فقط لزيادة الوزن! ركز على الطعام الصحي الغني بالعناصر الغذائية.'
        }
    },
    muscle_gain: {
        title: 'نصائح بناء العضلات 💪',
        tips: [
            {
                icon: '🏋️‍♂️',
                title: 'التحميل التدريجي هو المفتاح',
                content: 'زد الوزن أو التكرارات كل أسبوع. عضلاتك تحتاج تحدي مستمر لتنمو!'
            },
            {
                icon: '🥩',
                title: 'البروتين في كل وجبة',
                content: 'اهدف لـ 1.6-2.2 جرام بروتين لكل كيلو من وزنك. البيض، الدجاج، السمك، البقوليات كلها خيارات ممتازة!'
            },
            {
                icon: '😴',
                title: 'العضلات تنمو أثناء الراحة',
                content: 'نم 7-9 ساعات يومياً واترك يوم راحة بين تمرين نفس العضلة. الراحة جزء من التمرين!'
            },
            {
                icon: '📈',
                title: 'سجل تقدمك',
                content: 'اكتب أوزانك وتكراراتك. رؤية التقدم تحفزك وتساعدك على التخطيط للتمارين القادمة!'
            },
            {
                icon: '💧',
                title: 'الماء يبني العضلات',
                content: 'اشرب 3-4 لتر ماء يومياً. الجفاف يقلل الأداء ويبطئ نمو العضلات!'
            }
        ],
        avoidTip: {
            icon: '⚠️',
            title: 'تجنب هذا الخطأ الشائع',
            content: 'لا تتمرن نفس العضلة يومياً! العضلات تحتاج 48-72 ساعة راحة للنمو والتعافي.'
        }
    },
    general_fitness: {
        title: 'نصائح الحفاظ على الوزن المثالي ⚖️',
        tips: [
            {
                icon: '🔄',
                title: 'التوازن هو السر',
                content: 'وازن بين السعرات المستهلكة والمحروقة. لا إفراط ولا تفريط!'
            },
            {
                icon: '🏃‍♂️',
                title: 'نوع التمارين',
                content: 'امزج بين الكارديو وتمارين القوة. هذا يحافظ على اللياقة ويمنع فقدان العضلات!'
            },
            {
                icon: '📊',
                title: 'راقب وزنك أسبوعياً',
                content: 'زن نفسك مرة واحدة أسبوعياً في نفس الوقت. التقلبات اليومية طبيعية!'
            },
            {
                icon: '🍎',
                title: 'اتبع قاعدة 80/20',
                content: '80% طعام صحي، 20% متعة. هذا يساعدك على الاستمرار دون حرمان!'
            }
        ],
        avoidTip: {
            icon: '⚠️',
            title: 'تجنب هذا الخطأ الشائع',
            content: 'لا تهمل التمارين عند الوصول للوزن المثالي! النشاط المستمر ضروري للحفاظ على الصحة.'
        }
    }
};

// Function to generate motivational tips HTML
function generateMotivationalTips(goal) {
    const tips = goalTips[goal];
    if (!tips) return '';

    return `
        <div class="result-card tips-section fade-in">
            <div class="card-header">
                <div class="card-icon">
                    <i class="fas fa-lightbulb"></i>
                </div>
                <h2 class="card-title">${tips.title}</h2>
            </div>
            
            <div class="row">
                ${tips.tips.map(tip => `
                    <div class="col-md-6 mb-3">
                        <div class="tip-card">
                            <div class="tip-icon">${tip.icon}</div>
                            <div class="tip-content">
                                <h5 class="tip-title">${tip.title}</h5>
                                <p class="tip-text">${tip.content}</p>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
            
            <div class="avoid-tip-card mt-4">
                <div class="avoid-tip-icon">${tips.avoidTip.icon}</div>
                <div class="avoid-tip-content">
                    <h5 class="avoid-tip-title">${tips.avoidTip.title}</h5>
                    <p class="avoid-tip-text">${tips.avoidTip.content}</p>
                </div>
            </div>
        </div>
    `;
}

class WorkoutPlanResult {
    constructor() {
        this.userData = this.getUserData();
        this.workoutPlans = this.initializeWorkoutPlans();
        this.init();
    }

    async init() {
        try {
            console.log('🚀 Initializing WorkoutPlanResult...');
            
            // Add loading indicator
            this.showLoadingIndicator();
            
            // Validate data first
            const isValid = this.validateAndProcessData();
            if (!isValid) {
                console.log('❌ Data validation failed, showing error message');
                this.hideLoadingIndicator();
                return;
            }
            
            console.log('✅ Data validation successful, generating content...');
            
            // Initialize workout plans with retry mechanism
            await this.initializeWorkoutPlansWithRetry();
            await this.generatePlanContent();
            this.hideLoadingIndicator();
            
        } catch (error) {
            console.error('❌ Error during initialization:', error);
            this.hideLoadingIndicator();
            this.showErrorMessage();
        }
    }

    // إضافة مؤشر التحميل
    showLoadingIndicator() {
        const loadingHTML = `
            <div id="loadingIndicator" class="loading-indicator">
                <div class="loading-content">
                    <div class="loading-spinner"></div>
                    <h3>🏋️‍♂️ جاري إعداد خطتك الشخصية...</h3>
                    <p>يرجى الانتظار بينما نقوم بتخصيص أفضل التمارين لك</p>
                </div>
            </div>
        `;
        
        const planContent = document.getElementById('planContent');
        if (planContent) {
            planContent.innerHTML = loadingHTML;
        }
    }

    hideLoadingIndicator() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }

    // آلية إعادة المحاولة لتحميل بيانات التمارين
    async initializeWorkoutPlansWithRetry(maxRetries = 3) {
        for (let attempt = 1; attempt <= maxRetries; attempt++) {
            try {
                console.log(`🔄 Attempt ${attempt} to load workout plans...`);
                
                // محاولة تحميل التمارين من قاعدة البيانات
                this.workoutPlans = await this.loadExercisesFromDatabase();
                
                if (!this.workoutPlans) {
                    console.log('⚠️ Database load failed, using static data...');
                    this.workoutPlans = this.getStaticWorkoutPlans();
                }
                
                console.log('✅ Workout plans loaded successfully');
                return;
                
            } catch (error) {
                console.error(`❌ Attempt ${attempt} failed:`, error);
                
                if (attempt === maxRetries) {
                    console.log('🔄 All attempts failed, using static data as fallback');
                    this.workoutPlans = this.getStaticWorkoutPlans();
                } else {
                    // انتظار قبل المحاولة التالية
                    await new Promise(resolve => setTimeout(resolve, 1000 * attempt));
                }
            }
        }
    }

    getUserData() {
        // Get data from URL parameters or localStorage
        const urlParams = new URLSearchParams(window.location.search);
        return {
            name: urlParams.get('name') || localStorage.getItem('userName') || 'المتدرب',
            goal: urlParams.get('goal') || localStorage.getItem('userGoal') || '',
            split: urlParams.get('split') || localStorage.getItem('userSplit') || '',
            weight: parseFloat(urlParams.get('weight')) || parseFloat(localStorage.getItem('userWeight')) || null,
            height: parseFloat(urlParams.get('height')) || parseFloat(localStorage.getItem('userHeight')) || null,
            fitnessLevel: urlParams.get('fitnessLevel') || localStorage.getItem('userFitnessLevel') || 'beginner',
            workoutDays: parseInt(urlParams.get('workoutDays')) || parseInt(localStorage.getItem('userWorkoutDays')) || null,
            barriers: (urlParams.get('barriers') || localStorage.getItem('userBarriers') || '').split(',').filter(b => b),
            injuries: urlParams.get('injuries') || localStorage.getItem('userInjuries') || ''
        };
    }

    validateAndProcessData() {
        console.log('🔍 Validating user data:', this.userData);
        
        // Handle missing critical values
        if (!this.userData.weight || !this.userData.height || !this.userData.workoutDays) {
            console.log('❌ Missing critical data - showing enhanced error message');
            this.showEnhancedErrorMessage();
            return false;
        }

        // Calculate BMI if missing
        if (!this.userData.bmi) {
            this.userData.bmi = this.calculateBMI(this.userData.weight, this.userData.height);
            console.log('📊 Calculated BMI:', this.userData.bmi);
        }

        // Set default fitness level if missing
        if (!this.userData.fitnessLevel) {
            this.userData.fitnessLevel = 'beginner';
            console.log('⚙️ Set default fitness level: beginner');
        }

        // Set default goal if missing
        if (!this.userData.goal) {
            this.userData.goal = 'general_fitness';
            console.log('⚙️ Set default goal: general_fitness');
        }

        // Set default split if missing
        if (!this.userData.split) {
            this.userData.split = 'full_body';
            console.log('⚙️ Set default split: full_body');
        }

        // Validate and adjust workout days based on fitness level
        this.adjustWorkoutDaysForLevel();
        
        // Add user preferences based on goal and BMI
        this.addUserPreferences();
        
        console.log('✅ Data validation and processing complete:', this.userData);
        return true;
    }

    // تعديل أيام التمرين بناءً على مستوى اللياقة
    adjustWorkoutDaysForLevel() {
        const { fitnessLevel, workoutDays } = this.userData;
        
        if (fitnessLevel === 'beginner' && workoutDays > 4) {
            this.userData.workoutDays = 3;
            console.log('⚠️ Adjusted workout days for beginner: 3 days');
        } else if (fitnessLevel === 'advanced' && workoutDays < 4) {
            this.userData.workoutDays = 5;
            console.log('⚠️ Adjusted workout days for advanced: 5 days');
        }
    }

    // إضافة تفضيلات المستخدم بناءً على الهدف ومؤشر كتلة الجسم
    addUserPreferences() {
        const { goal, bmi } = this.userData;
        
        // تحديد شدة التمرين
        if (goal === 'weight_loss' || bmi > 25) {
            this.userData.intensity = 'high';
            this.userData.cardioFocus = true;
        } else if (goal === 'muscle_gain') {
            this.userData.intensity = 'moderate';
            this.userData.strengthFocus = true;
        } else {
            this.userData.intensity = 'moderate';
            this.userData.balancedFocus = true;
        }
        
        // تحديد نوع التمارين المفضلة
        if (bmi < 18.5) {
            this.userData.preferredExercises = ['strength', 'compound'];
        } else if (bmi > 30) {
            this.userData.preferredExercises = ['cardio', 'low_impact'];
        } else {
            this.userData.preferredExercises = ['mixed', 'functional'];
        }
        
        console.log('🎯 Added user preferences:', {
            intensity: this.userData.intensity,
            preferredExercises: this.userData.preferredExercises
        });
    }

    calculateBMI(weight, height) {
        const heightInMeters = height / 100;
        return (weight / (heightInMeters * heightInMeters)).toFixed(1);
    }

    getBMIStatus(bmi) {
        if (bmi < 18.5) return { status: 'نقص في الوزن', class: 'bmi-underweight' };
        if (bmi < 25) return { status: 'وزن طبيعي', class: 'bmi-normal' };
        if (bmi < 30) return { status: 'زيادة في الوزن', class: 'bmi-overweight' };
        return { status: 'سمنة', class: 'bmi-obese' };
    }

    getGoalArabic(goal) {
        const goals = {
            'weight_loss': 'فقدان الوزن',
            'muscle_gain': 'بناء العضلات',
            'general_fitness': 'اللياقة العامة',
            'strength': 'زيادة القوة',
            'endurance': 'تحسين التحمل'
        };
        return goals[goal] || 'اللياقة العامة';
    }

    getSplitArabic(split) {
        const splits = {
            'full_body': 'تمرين الجسم كامل',
            'upper_lower': 'علوي وسفلي',
            'push_pull_legs': 'دفع، سحب، أرجل',
            'bro_split': 'عضلة واحدة يومياً',
            'crossfit': 'تمارين وظيفية',
            'hiit': 'عالي الكثافة'
        };
        return splits[split] || 'تمرين الجسم كامل';
    }

    getFitnessLevelArabic(level) {
        const levels = {
            'beginner': 'مبتدئ',
            'intermediate': 'متوسط',
            'advanced': 'متقدم'
        };
        return levels[level] || 'مبتدئ';
    }

    async loadExercisesFromDatabase() {
        try {
            // Load exercises for different difficulty levels
            const [beginnerExercises, intermediateExercises, advancedExercises] = await Promise.all([
                fetch('/api/exercises?difficulty=مبتدئ&limit=20').then(r => r.json()),
                fetch('/api/exercises?difficulty=متوسط&limit=25').then(r => r.json()),
                fetch('/api/exercises?difficulty=متقدم&limit=30').then(r => r.json())
            ]);

            // Organize exercises by muscle groups
            const organizeByMuscleGroup = (exercises) => {
                const groups = {
                    chest: exercises.filter(ex => ex.muscle_group === 'الصدر'),
                    back: exercises.filter(ex => ex.muscle_group === 'الظهر'),
                    legs: exercises.filter(ex => ex.muscle_group === 'الأرجل'),
                    shoulders: exercises.filter(ex => ex.muscle_group === 'الأكتاف'),
                    arms: exercises.filter(ex => ex.muscle_group === 'الذراعين'),
                    abs: exercises.filter(ex => ex.muscle_group === 'البطن'),
                    full_body: exercises.filter(ex => ex.muscle_group === 'الجسم كامل')
                };
                return groups;
            };

            const beginnerGroups = organizeByMuscleGroup(beginnerExercises);
            const intermediateGroups = organizeByMuscleGroup(intermediateExercises);
            const advancedGroups = organizeByMuscleGroup(advancedExercises);

            // Create workout plans structure
            return {
                full_body: {
                    beginner: {
                        exercises: this.selectExercisesForFullBody(beginnerGroups, 'beginner')
                    },
                    intermediate: {
                        exercises: this.selectExercisesForFullBody(intermediateGroups, 'intermediate')
                    },
                    advanced: {
                        exercises: this.selectExercisesForFullBody(advancedGroups, 'advanced')
                    }
                },
                upper_lower: {
                    beginner: {
                        upper: this.selectExercisesForUpperBody(beginnerGroups, 'beginner'),
                        lower: this.selectExercisesForLowerBody(beginnerGroups, 'beginner')
                    },
                    intermediate: {
                        upper: this.selectExercisesForUpperBody(intermediateGroups, 'intermediate'),
                        lower: this.selectExercisesForLowerBody(intermediateGroups, 'intermediate')
                    },
                    advanced: {
                        upper: this.selectExercisesForUpperBody(advancedGroups, 'advanced'),
                        lower: this.selectExercisesForLowerBody(advancedGroups, 'advanced')
                    }
                }
            };
        } catch (error) {
            console.error('Error loading exercises from database:', error);
            return null; // Will fallback to static data
        }
    }

    selectExercisesForFullBody(groups, level) {
        const exercises = [];
        
        // تحسين اختيار التمارين بناءً على مستوى اللياقة والهدف
        const { goal, bmi } = this.userData;
        
        // اختيار التمارين الأساسية لكل مجموعة عضلية
        const muscleGroupPriority = this.getMuscleGroupPriority(goal, bmi);
        
        muscleGroupPriority.forEach(groupName => {
            const group = groups[groupName];
            if (group && group.length > 0) {
                // فلترة التمارين حسب مستوى اللياقة
                const suitableExercises = this.filterExercisesByLevel(group, level);
                if (suitableExercises.length > 0) {
                    // اختيار أفضل تمرين للمجموعة العضلية
                    const selectedExercise = this.selectBestExercise(suitableExercises, goal);
                    exercises.push(this.formatExercise(selectedExercise, level));
                }
            }
        });
        
        // إضافة تمارين إضافية للمستويات المتقدمة
        if (level !== 'beginner' && exercises.length < 6) {
            this.addSupplementaryExercises(exercises, groups, level, goal);
        }
        
        return exercises;
    }

    selectExercisesForUpperBody(groups, level) {
        const exercises = [];
        
        if (groups.chest.length > 0) exercises.push(this.formatExercise(groups.chest[0], level));
        if (groups.back.length > 0) exercises.push(this.formatExercise(groups.back[0], level));
        if (groups.shoulders.length > 0) exercises.push(this.formatExercise(groups.shoulders[0], level));
        if (groups.arms.length > 0) exercises.push(this.formatExercise(groups.arms[0], level));
        
        if (level !== 'beginner' && groups.chest.length > 1) {
            exercises.push(this.formatExercise(groups.chest[1], level));
        }
        
        return exercises;
    }

    selectExercisesForLowerBody(groups, level) {
        const exercises = [];
        
        if (groups.legs.length > 0) exercises.push(this.formatExercise(groups.legs[0], level));
        if (groups.abs.length > 0) exercises.push(this.formatExercise(groups.abs[0], level));
        
        if (level !== 'beginner' && groups.legs.length > 1) {
            exercises.push(this.formatExercise(groups.legs[1], level));
        }
        
        return exercises;
    }

    formatExercise(exercise, level) {
        // تحسين تنسيق التمرين بناءً على المستوى
        const levelMultipliers = {
            'beginner': { sets: 0.8, reps: 0.8, rest: 1.2 },
            'intermediate': { sets: 1.0, reps: 1.0, rest: 1.0 },
            'advanced': { sets: 1.2, reps: 1.1, rest: 0.9 }
        };
        
        const multiplier = levelMultipliers[level] || levelMultipliers['intermediate'];
        
        return {
            id: exercise.id,
            name: exercise.name_ar,
            name_en: exercise.name_en,
            sets: this.calculateSets(exercise.sets || '3', multiplier.sets),
            reps: this.calculateReps(exercise.reps || '10-12', multiplier.reps),
            rest: this.calculateRest(exercise.rest_time || '60 ثانية', multiplier.rest),
            muscle_group: exercise.muscle_group,
            difficulty: exercise.difficulty_level,
            instructions: exercise.instructions_ar,
            equipment: exercise.equipment || 'أوزان حرة'
        };
    }

    getMuscleGroupPriority(goal, bmi) {
        // ترتيب أولوية المجموعات العضلية حسب الهدف ومؤشر كتلة الجسم
        const basePriority = ['legs', 'chest', 'back', 'shoulders', 'abs', 'arms'];
        
        if (goal === 'خسارة الوزن' || bmi > 25) {
            // التركيز على التمارين التي تحرق سعرات أكثر
            return ['legs', 'back', 'chest', 'abs', 'shoulders', 'arms'];
        } else if (goal === 'زيادة الكتلة العضلية') {
            // التركيز على العضلات الكبيرة
            return ['chest', 'back', 'legs', 'shoulders', 'arms', 'abs'];
        } else if (goal === 'تحسين اللياقة') {
            // توازن شامل
            return ['legs', 'chest', 'back', 'abs', 'shoulders', 'arms'];
        }
        
        return basePriority;
    }

    filterExercisesByLevel(exercises, level) {
        return exercises.filter(exercise => {
            const difficulty = exercise.difficulty_level || 'متوسط';
            
            if (level === 'beginner') {
                return difficulty === 'مبتدئ' || difficulty === 'سهل';
            } else if (level === 'intermediate') {
                return difficulty === 'متوسط' || difficulty === 'مبتدئ';
            } else {
                return difficulty === 'متقدم' || difficulty === 'متوسط';
            }
        });
    }

    selectBestExercise(exercises, goal) {
        // اختيار أفضل تمرين بناءً على الهدف
        if (goal === 'خسارة الوزن') {
            // التركيز على التمارين المركبة التي تحرق سعرات أكثر
            const compoundExercises = exercises.filter(ex => 
                ex.name_ar.includes('قرفصاء') || 
                ex.name_ar.includes('رفعة') || 
                ex.name_ar.includes('عقلة') ||
                ex.name_ar.includes('ضغط')
            );
            return compoundExercises.length > 0 ? compoundExercises[0] : exercises[0];
        } else if (goal === 'زيادة الكتلة العضلية') {
            // التركيز على التمارين الثقيلة
            const heavyExercises = exercises.filter(ex => 
                ex.name_ar.includes('بار') || 
                ex.name_ar.includes('دمبل') ||
                ex.name_ar.includes('أوزان')
            );
            return heavyExercises.length > 0 ? heavyExercises[0] : exercises[0];
        }
        
        // للأهداف الأخرى، اختيار عشوائي من التمارين المناسبة
        return exercises[Math.floor(Math.random() * exercises.length)];
    }

    addSupplementaryExercises(exercises, groups, level, goal) {
        const currentMuscleGroups = exercises.map(ex => ex.muscle_group);
        const availableGroups = Object.keys(groups).filter(group => 
            !currentMuscleGroups.includes(group) && groups[group].length > 0
        );
        
        // إضافة تمارين إضافية حتى نصل للعدد المطلوب
        const targetCount = level === 'advanced' ? 7 : 6;
        
        while (exercises.length < targetCount && availableGroups.length > 0) {
            const groupName = availableGroups.shift();
            const group = groups[groupName];
            const suitableExercises = this.filterExercisesByLevel(group, level);
            
            if (suitableExercises.length > 0) {
                const selectedExercise = this.selectBestExercise(suitableExercises, goal);
                exercises.push(this.formatExercise(selectedExercise, level));
            }
        }
    }

    calculateSets(originalSets, multiplier) {
        const sets = parseInt(originalSets) || 3;
        return Math.max(2, Math.round(sets * multiplier)).toString();
    }

    calculateReps(originalReps, multiplier) {
        if (originalReps.includes('-')) {
            const [min, max] = originalReps.split('-').map(r => parseInt(r.trim()));
            const newMin = Math.max(5, Math.round(min * multiplier));
            const newMax = Math.round(max * multiplier);
            return `${newMin}-${newMax}`;
        }
        
        const reps = parseInt(originalReps) || 10;
        return Math.max(5, Math.round(reps * multiplier)).toString();
    }

    calculateRest(originalRest, multiplier) {
        const seconds = parseInt(originalRest) || 60;
        const newSeconds = Math.round(seconds * multiplier);
        return `${newSeconds} ثانية`;
    }

    async initializeWorkoutPlans() {
        // Load exercises from database
        const exercisesData = await this.loadExercisesFromDatabase();
        if (exercisesData) {
            return exercisesData;
        }
        
        // Fallback to static data if API fails
        return {
            full_body: {
                beginner: {
                    exercises: [
                        { name: 'تمرين القرفصاء', sets: '3', reps: '10-12', rest: '60-90 ثانية' },
                        { name: 'تمرين الضغط', sets: '3', reps: '8-10', rest: '60-90 ثانية' },
                        { name: 'تمرين العقلة', sets: '3', reps: '5-8', rest: '60-90 ثانية' },
                        { name: 'تمرين البلانك', sets: '3', reps: '30-45 ثانية', rest: '60 ثانية' },
                        { name: 'تمرين الطعنات', sets: '3', reps: '10 لكل رجل', rest: '60 ثانية' }
                    ]
                },
                intermediate: {
                    exercises: [
                        { name: 'تمرين القرفصاء بالأوزان', sets: '4', reps: '10-12', rest: '60-90 ثانية' },
                        { name: 'تمرين البنش برس', sets: '4', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين الديدليفت', sets: '4', reps: '6-8', rest: '90-120 ثانية' },
                        { name: 'تمرين العقلة المرجحة', sets: '3', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين الكتف العسكري', sets: '3', reps: '10-12', rest: '60 ثانية' },
                        { name: 'تمرين البطن المتقدم', sets: '3', reps: '15-20', rest: '45 ثانية' }
                    ]
                },
                advanced: {
                    exercises: [
                        { name: 'تمرين القرفصاء الأمامي', sets: '5', reps: '6-8', rest: '90-120 ثانية' },
                        { name: 'تمرين البنش برس المائل', sets: '4', reps: '6-8', rest: '90-120 ثانية' },
                        { name: 'تمرين الديدليفت السومو', sets: '5', reps: '5-6', rest: '120 ثانية' },
                        { name: 'تمرين العقلة بالوزن', sets: '4', reps: '6-8', rest: '90-120 ثانية' },
                        { name: 'تمرين الكتف بالدمبل', sets: '4', reps: '8-10', rest: '60-90 ثانية' },
                        { name: 'تمرين البطن بالوزن', sets: '4', reps: '12-15', rest: '60 ثانية' }
                    ]
                }
            },
            upper_lower: {
                beginner: {
                    upper: [
                        { name: 'تمرين الضغط', sets: '3', reps: '8-10', rest: '60-90 ثانية' },
                        { name: 'تمرين العقلة المساعدة', sets: '3', reps: '5-8', rest: '90 ثانية' },
                        { name: 'تمرين الكتف بالدمبل', sets: '3', reps: '10-12', rest: '60 ثانية' },
                        { name: 'تمرين البايسبس', sets: '3', reps: '10-12', rest: '45 ثانية' },
                        { name: 'تمرين الترايسبس', sets: '3', reps: '10-12', rest: '45 ثانية' }
                    ],
                    lower: [
                        { name: 'تمرين القرفصاء', sets: '3', reps: '10-12', rest: '60-90 ثانية' },
                        { name: 'تمرين الطعنات', sets: '3', reps: '10 لكل رجل', rest: '60 ثانية' },
                        { name: 'تمرين رفع الساق الخلفي', sets: '3', reps: '12-15', rest: '45 ثانية' },
                        { name: 'تمرين السمانة', sets: '3', reps: '15-20', rest: '45 ثانية' },
                        { name: 'تمرين البطن', sets: '3', reps: '15-20', rest: '45 ثانية' }
                    ]
                },
                intermediate: {
                    upper: [
                        { name: 'تمرين البنش برس', sets: '4', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين العقلة', sets: '4', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين الكتف العسكري', sets: '3', reps: '10-12', rest: '60 ثانية' },
                        { name: 'تمرين التجديف', sets: '3', reps: '10-12', rest: '60 ثانية' },
                        { name: 'تمرين البايسبس بالبار', sets: '3', reps: '10-12', rest: '45 ثانية' },
                        { name: 'تمرين الترايسبس بالحبل', sets: '3', reps: '10-12', rest: '45 ثانية' }
                    ],
                    lower: [
                        { name: 'تمرين القرفصاء بالبار', sets: '4', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين الديدليفت الروماني', sets: '4', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين الطعنات بالدمبل', sets: '3', reps: '12 لكل رجل', rest: '60 ثانية' },
                        { name: 'تمرين رفع الساق', sets: '3', reps: '12-15', rest: '45 ثانية' },
                        { name: 'تمرين السمانة بالوزن', sets: '4', reps: '15-20', rest: '45 ثانية' },
                        { name: 'تمرين البطن المتقدم', sets: '3', reps: '15-20', rest: '45 ثانية' }
                    ]
                },
                advanced: {
                    upper: [
                        { name: 'تمرين البنش برس المائل', sets: '5', reps: '6-8', rest: '120 ثانية' },
                        { name: 'تمرين العقلة بالوزن', sets: '4', reps: '6-8', rest: '90-120 ثانية' },
                        { name: 'تمرين الكتف بالبار', sets: '4', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين التجديف بالبار', sets: '4', reps: '8-10', rest: '90 ثانية' },
                        { name: 'تمرين البايسبس المطرقة', sets: '3', reps: '10-12', rest: '60 ثانية' },
                        { name: 'تمرين الترايسبس فرنسي', sets: '3', reps: '10-12', rest: '60 ثانية' }
                    ],
                    lower: [
                        { name: 'تمرين القرفصاء الأمامي', sets: '5', reps: '6-8', rest: '120 ثانية' },
                        { name: 'تمرين الديدليفت السومو', sets: '5', reps: '5-6', rest: '120 ثانية' },
                        { name: 'تمرين الطعنات البلغارية', sets: '4', reps: '10 لكل رجل', rest: '90 ثانية' },
                        { name: 'تمرين رفع الساق بالوزن', sets: '4', reps: '10-12', rest: '60 ثانية' },
                        { name: 'تمرين السمانة واقف', sets: '4', reps: '15-20', rest: '45 ثانية' },
                        { name: 'تمرين البطن بالوزن', sets: '4', reps: '12-15', rest: '60 ثانية' }
                    ]
                }
            }
        };
    }

    async generateWorkoutSchedule() {
        const { split, fitnessLevel, workoutDays } = this.userData;
        
        // Initialize workout plans from database
        if (!this.workoutPlans) {
            this.workoutPlans = await this.initializeWorkoutPlans();
        }
        
        const plan = this.workoutPlans[split] || this.workoutPlans.full_body;
        const levelPlan = plan[fitnessLevel] || plan.beginner;

        let schedule = [];
        const days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت'];

        if (split === 'full_body') {
            for (let i = 0; i < workoutDays; i++) {
                schedule.push({
                    day: days[i],
                    type: 'تمرين الجسم كامل',
                    exercises: levelPlan.exercises
                });
                if (i < workoutDays - 1) {
                    schedule.push({
                        day: days[i + 1],
                        type: 'راحة',
                        exercises: []
                    });
                }
            }
        } else if (split === 'upper_lower') {
            let dayIndex = 0;
            for (let i = 0; i < Math.ceil(workoutDays / 2); i++) {
                schedule.push({
                    day: days[dayIndex++],
                    type: 'الجزء العلوي',
                    exercises: levelPlan.upper
                });
                if (dayIndex < 7) {
                    schedule.push({
                        day: days[dayIndex++],
                        type: 'الجزء السفلي',
                        exercises: levelPlan.lower
                    });
                }
                if (dayIndex < 7 && i < Math.ceil(workoutDays / 2) - 1) {
                    schedule.push({
                        day: days[dayIndex++],
                        type: 'راحة',
                        exercises: []
                    });
                }
            }
        }

        return schedule.slice(0, 7); // Limit to 7 days
    }

    calculatePerformanceIndicators() {
        const { workoutDays, fitnessLevel, goal, weight, height, bmi } = this.userData;
        
        // حساب أكثر دقة للسعرات المحروقة بناءً على عوامل متعددة
        let baseCaloriesPerSession = this.calculateBaseCalories(weight, height, fitnessLevel);
        
        // تعديل السعرات حسب الهدف
        if (goal === 'خسارة الوزن') {
            baseCaloriesPerSession *= 1.2; // زيادة كثافة التمرين
        } else if (goal === 'زيادة الكتلة العضلية') {
            baseCaloriesPerSession *= 0.9; // تركيز أكثر على القوة
        }
        
        // تعديل حسب مؤشر كتلة الجسم
        if (bmi > 30) {
            baseCaloriesPerSession *= 1.15; // حرق أكثر للوزن الزائد
        } else if (bmi < 18.5) {
            baseCaloriesPerSession *= 0.85; // حرق أقل للوزن المنخفض
        }

        const weeklyCalories = Math.round(workoutDays * baseCaloriesPerSession);
        const sessionDuration = this.calculateSessionDuration(fitnessLevel, goal);
        const weeklyTime = workoutDays * sessionDuration;
        
        // حساب النتائج المتوقعة بدقة أكبر
        const expectedResults = this.calculateExpectedResults(goal, fitnessLevel, workoutDays, bmi);
        
        // حساب فترات الراحة المناسبة
        const restBetweenSets = this.calculateOptimalRest(goal, fitnessLevel);
        
        // تحديد مدة البرنامج بناءً على الهدف والمستوى
        const programDuration = this.calculateProgramDuration(goal, fitnessLevel);

        return {
            weeklyCalories,
            weeklyTime,
            expectedResults,
            sessionDuration: `${sessionDuration} دقيقة`,
            restBetweenSets,
            programDuration,
            caloriesPerSession: Math.round(baseCaloriesPerSession),
            intensityLevel: this.getIntensityLevel(fitnessLevel, goal)
        };
    }

    calculateBaseCalories(weight, height, fitnessLevel) {
        // حساب معدل الأيض الأساسي (BMR) مبسط
        const bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * 25); // افتراض عمر 25
        
        // معامل النشاط للتمرين
        const activityMultipliers = {
            'مبتدئ': 0.4,
            'متوسط': 0.5,
            'متقدم': 0.6
        };
        
        const multiplier = activityMultipliers[fitnessLevel] || 0.5;
        return bmr * multiplier / 24; // تحويل لكل ساعة تمرين
    }

    calculateSessionDuration(fitnessLevel, goal) {
        const baseDurations = {
            'مبتدئ': 45,
            'متوسط': 60,
            'متقدم': 75
        };
        
        let duration = baseDurations[fitnessLevel] || 60;
        
        // تعديل حسب الهدف
        if (goal === 'خسارة الوزن') {
            duration += 15; // إضافة كارديو
        } else if (goal === 'زيادة الكتلة العضلية') {
            duration += 10; // فترات راحة أطول
        }
        
        return duration;
    }

    calculateExpectedResults(goal, fitnessLevel, workoutDays, bmi) {
        const baseResults = {
            'خسارة الوزن': {
                'مبتدئ': '0.3-0.6 كيلو أسبوعياً',
                'متوسط': '0.5-0.8 كيلو أسبوعياً', 
                'متقدم': '0.6-1 كيلو أسبوعياً'
            },
            'زيادة الكتلة العضلية': {
                'مبتدئ': '0.2-0.4 كيلو أسبوعياً',
                'متوسط': '0.15-0.3 كيلو أسبوعياً',
                'متقدم': '0.1-0.25 كيلو أسبوعياً'
            },
            'تحسين اللياقة': {
                'مبتدئ': 'تحسن ملحوظ خلال 2-3 أسابيع',
                'متوسط': 'تحسن كبير خلال 3-4 أسابيع',
                'متقدم': 'تحسن متقدم خلال 4-6 أسابيع'
            }
        };
        
        let result = baseResults[goal]?.[fitnessLevel] || 'نتائج إيجابية خلال 4-6 أسابيع';
        
        // تعديل حسب عدد أيام التمرين
        if (workoutDays >= 5) {
            result += ' (نتائج أسرع مع التمرين المكثف)';
        } else if (workoutDays <= 2) {
            result += ' (نتائج أبطأ مع التمرين المحدود)';
        }
        
        return result;
    }

    calculateOptimalRest(goal, fitnessLevel) {
        if (goal === 'زيادة الكتلة العضلية') {
            return fitnessLevel === 'متقدم' ? '90-120 ثانية' : '60-90 ثانية';
        } else if (goal === 'خسارة الوزن') {
            return fitnessLevel === 'مبتدئ' ? '45-60 ثانية' : '30-45 ثانية';
        } else {
            return '60-75 ثانية';
        }
    }

    calculateProgramDuration(goal, fitnessLevel) {
        const durations = {
            'خسارة الوزن': {
                'مبتدئ': '8-10 أسابيع',
                'متوسط': '6-8 أسابيع',
                'متقدم': '4-6 أسابيع'
            },
            'زيادة الكتلة العضلية': {
                'مبتدئ': '12-16 أسبوع',
                'متوسط': '10-12 أسبوع',
                'متقدم': '8-10 أسابيع'
            },
            'تحسين اللياقة': {
                'مبتدئ': '6-8 أسابيع',
                'متوسط': '4-6 أسابيع',
                'متقدم': '4-5 أسابيع'
            }
        };
        
        return durations[goal]?.[fitnessLevel] || '6-8 أسابيع';
    }

    getIntensityLevel(fitnessLevel, goal) {
        if (goal === 'خسارة الوزن') {
            return fitnessLevel === 'متقدم' ? 'عالية جداً' : fitnessLevel === 'متوسط' ? 'عالية' : 'متوسطة';
        } else if (goal === 'زيادة الكتلة العضلية') {
            return fitnessLevel === 'متقدم' ? 'عالية' : 'متوسطة إلى عالية';
        } else {
            return 'متوسطة';
        }
    }

    generateMotivationalMessage() {
        const { goal, fitnessLevel, workoutDays, bmi } = this.userData;
        
        let message = '';
        let icon = '💪';
        let title = 'رسالة تحفيزية';
        
        // رسائل مخصصة حسب الهدف والمستوى
        if (goal === 'خسارة الوزن') {
            icon = '🔥';
            title = 'رحلة التحول تبدأ الآن';
            if (bmi > 30) {
                message = 'أنت على وشك تغيير حياتك للأفضل! كل خطوة تخطوها اليوم ستقربك من هدفك. تذكر أن الرحلة الطويلة تبدأ بخطوة واحدة.';
            } else {
                message = 'هدفك قريب المنال! مع الالتزام والصبر، ستحقق الوزن المثالي وتشعر بالثقة والطاقة.';
            }
        } else if (goal === 'زيادة الكتلة العضلية') {
            icon = '🏆';
            title = 'بناء القوة والعضلات';
            if (fitnessLevel === 'مبتدئ') {
                message = 'كل محترف كان مبتدئاً يوماً ما. جسمك سيتكيف ويصبح أقوى مع كل تمرين. استمر والنتائج ستأتي!';
            } else {
                message = 'أنت في الطريق الصحيح لبناء جسم قوي ومتناسق. كل مجموعة تكملها تقربك من هدفك.';
            }
        } else {
            icon = '⚡';
            title = 'تحسين اللياقة والصحة';
            message = 'اللياقة البدنية استثمار في صحتك ومستقبلك. كل يوم تمرين هو يوم تضيفه لحياتك بصحة أفضل.';
        }
        
        // إضافة تحفيز إضافي حسب عدد أيام التمرين
        if (workoutDays >= 5) {
            message += ' التزامك المكثف سيحقق نتائج مذهلة!';
        } else if (workoutDays <= 2) {
            message += ' حتى لو كان وقتك محدود، الثبات هو المفتاح للنجاح.';
        }
        
        return `
            <div class="motivational-message fade-in">
                <div class="message-header">
                    <div class="message-icon">${icon}</div>
                    <h3 class="message-title">${title}</h3>
                </div>
                <p class="message-content">${message}</p>
                <div class="message-quote">
                    <i class="fas fa-quote-left"></i>
                    <span>"النجاح ليس نهاية، والفشل ليس قاتلاً، إنما الشجاعة للاستمرار هي ما يهم"</span>
                    <i class="fas fa-quote-right"></i>
                </div>
            </div>
        `;
    }

    getTailoredTips() {
        const { barriers, goal, fitnessLevel } = this.userData;
        let tips = [];

        // General tips based on goal
        if (goal === 'weight_loss') {
            tips.push({
                title: 'نصائح لفقدان الوزن',
                content: 'ركز على تمارين الكارديو وتناول سعرات أقل من احتياجك اليومي'
            });
        } else if (goal === 'muscle_gain') {
            tips.push({
                title: 'نصائح لبناء العضلات',
                content: 'تناول 2.2 جرام بروتين لكل كيلو من وزنك ونم 7-8 ساعات يومياً'
            });
        }

        // Tips based on barriers
        if (barriers.includes('time')) {
            tips.push({
                title: 'حل مشكلة قلة الوقت',
                content: 'قلل فترات الراحة إلى 45-60 ثانية أو جرب تمارين HIIT لمدة 15-20 دقيقة'
            });
        }

        if (barriers.includes('motivation')) {
            tips.push({
                title: 'زيادة الدافعية',
                content: 'صور تقدمك أسبوعياً وحدد أهداف صغيرة قابلة للتحقيق كل أسبوع'
            });
        }

        if (barriers.includes('results')) {
            tips.push({
                title: 'تسريع النتائج',
                content: 'راجع نظامك الغذائي وتأكد من زيادة الأوزان تدريجياً كل أسبوع'
            });
        }

        if (barriers.includes('boredom')) {
            tips.push({
                title: 'كسر الملل',
                content: 'غير التمارين كل 4-6 أسابيع وجرب أنواع تمارين جديدة'
            });
        }

        // Default tips if no specific barriers
        if (tips.length === 0) {
            tips.push(
                {
                    title: 'الثبات هو المفتاح',
                    content: 'التزم بخطتك لمدة 4 أسابيع على الأقل لترى النتائج'
                },
                {
                    title: 'التغذية مهمة',
                    content: 'التمرين وحده لا يكفي، اهتم بنظامك الغذائي أيضاً'
                }
            );
        }

        return tips;
    }

    // دالة لإنشاء ملاحظات التمارين المخصصة
    generateExerciseNotes(exerciseName) {
        const { goal, fitnessLevel, barriers, injuries } = this.userData;
        let notes = [];

        // ملاحظات حسب الهدف
        if (goal === 'خسارة الوزن') {
            if (exerciseName.includes('كارديو') || exerciseName.includes('جري')) {
                notes.push('ركز على الوتيرة الثابتة والاستمرارية لحرق الدهون بشكل أفضل');
            } else {
                notes.push('حافظ على معدل ضربات القلب مرتفع لزيادة حرق السعرات');
            }
        } else if (goal === 'زيادة الكتلة العضلية') {
            if (exerciseName.includes('ضغط') || exerciseName.includes('سحب')) {
                notes.push('ركز على الحركة البطيئة والمتحكم بها لتحفيز نمو العضلات');
            } else {
                notes.push('استخدم أوزان تتحداك في آخر 2-3 تكرارات');
            }
        }

        // ملاحظات حسب مستوى اللياقة
        if (fitnessLevel === 'مبتدئ') {
            notes.push('ابدأ بأوزان خفيفة وزد تدريجياً لتجنب الإصابات');
        } else if (fitnessLevel === 'متقدم') {
            notes.push('تحدى نفسك بتقنيات متقدمة مثل Drop Sets أو Super Sets');
        }

        // ملاحظات حسب التحديات
        if (barriers && barriers.includes('time')) {
            notes.push('قلل فترات الراحة إلى 45-60 ثانية لتوفير الوقت');
        }

        if (barriers && barriers.includes('injury')) {
            if (exerciseName.includes('قرفصاء') || exerciseName.includes('لونجز')) {
                notes.push('تجنب النزول العميق إذا كان لديك مشاكل في الركبة');
            }
            if (exerciseName.includes('رفعة ميتة') || exerciseName.includes('صف')) {
                notes.push('حافظ على استقامة الظهر وتجنب الانحناء المفرط');
            }
        }

        // ملاحظات حسب الإصابات المحددة
        if (injuries) {
            if (injuries.includes('knee') && (exerciseName.includes('قرفصاء') || exerciseName.includes('لونجز'))) {
                notes.push('استخدم نطاق حركة جزئي لحماية الركبة');
            }
            if (injuries.includes('back') && exerciseName.includes('رفعة ميتة')) {
                notes.push('ابدأ بأوزان خفيفة جداً وركز على التقنية الصحيحة');
            }
            if (injuries.includes('shoulder') && exerciseName.includes('ضغط كتف')) {
                notes.push('تجنب الضغط خلف الرأس واستخدم نطاق حركة مريح');
            }
        }

        // ملاحظة افتراضية إذا لم تكن هناك ملاحظات محددة
        if (notes.length === 0) {
            notes.push('حافظ على التقنية الصحيحة وتنفس بانتظام أثناء التمرين');
        }

        return notes;
    }

    showErrorMessage() {
        const content = `
            <div class="error-message fade-in">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3 class="error-title">معلومات ناقصة</h3>
                <p class="error-text">يرجى إكمال بياناتك لإنشاء خطتك الشخصية</p>
                <a href="${window.location.origin}/your-plan-your-goal" class="btn-primary-custom">
                    <i class="fas fa-arrow-right"></i> إكمال البيانات
                </a>
            </div>
        `;
        
        document.getElementById('planContent').innerHTML = content;
    }

    showEnhancedErrorMessage() {
        const missingFields = [];
        if (!this.userData.weight) missingFields.push('الوزن');
        if (!this.userData.height) missingFields.push('الطول');
        if (!this.userData.workoutDays) missingFields.push('أيام التمرين');
        
        const content = `
            <div class="error-message enhanced-error fade-in">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3 class="error-title">🚨 بيانات مفقودة مطلوبة</h3>
                <p class="error-text">لإنشاء خطة تمرين دقيقة ومخصصة لك، نحتاج إلى البيانات التالية:</p>
                
                <div class="missing-fields">
                    <h4>البيانات المفقودة:</h4>
                    <ul class="missing-list">
                        ${missingFields.map(field => `<li><i class="fas fa-times-circle"></i> ${field}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="error-actions">
                    <a href="${window.location.origin}/your-plan-your-goal" class="btn-primary-custom">
                        <i class="fas fa-edit"></i> إكمال البيانات الآن
                    </a>
                    <button onclick="workoutPlan.tryWithDefaults()" class="btn-secondary-custom">
                        <i class="fas fa-magic"></i> استخدام قيم افتراضية
                    </button>
                </div>
                
                <div class="debug-info">
                    <details>
                        <summary>معلومات تقنية للمطورين</summary>
                        <pre>${JSON.stringify(this.userData, null, 2)}</pre>
                    </details>
                </div>
            </div>
        `;
        
        document.getElementById('planContent').innerHTML = content;
    }

    // دالة لاستخدام القيم الافتراضية
    tryWithDefaults() {
        console.log('🔧 Trying with default values...');
        
        // تعيين قيم افتراضية للبيانات المفقودة
        if (!this.userData.weight) {
            this.userData.weight = 70; // وزن افتراضي
            console.log('⚙️ Set default weight: 70kg');
        }
        
        if (!this.userData.height) {
            this.userData.height = 170; // طول افتراضي
            console.log('⚙️ Set default height: 170cm');
        }
        
        if (!this.userData.workoutDays) {
            this.userData.workoutDays = 3; // 3 أيام افتراضي
            console.log('⚙️ Set default workout days: 3');
        }
        
        // إعادة التحقق من البيانات وإنشاء المحتوى
         const isValid = this.validateAndProcessData();
         if (isValid) {
             this.generatePlanContent();
         } else {
             console.error('❌ Still invalid after setting defaults');
             this.showErrorMessage();
         }
     }

     // دالة لتعديل أيام التمرين حسب مستوى اللياقة
     adjustWorkoutDaysForLevel() {
         const { fitnessLevel, workoutDays } = this.userData;
         
         console.log(`🔧 Adjusting workout days for ${fitnessLevel} level`);
         
         if (fitnessLevel === 'beginner' && workoutDays > 4) {
             this.userData.workoutDays = 3;
             console.log('⚙️ Reduced workout days to 3 for beginner');
         } else if (fitnessLevel === 'advanced' && workoutDays < 4) {
             this.userData.workoutDays = 5;
             console.log('⚙️ Increased workout days to 5 for advanced');
         }
         
         return this.userData.workoutDays;
     }

     // دالة لإضافة تفضيلات المستخدم
     addUserPreferences() {
         const { goal, bmi } = this.userData;
         
         console.log('🎯 Adding user preferences based on goal and BMI');
         
         // تحديد شدة التمرين
         if (goal === 'weight_loss') {
             this.userData.exerciseIntensity = 'high';
             this.userData.preferredExerciseTypes = ['cardio', 'hiit', 'circuit'];
         } else if (goal === 'muscle_gain') {
             this.userData.exerciseIntensity = 'moderate';
             this.userData.preferredExerciseTypes = ['strength', 'compound', 'isolation'];
         } else {
             this.userData.exerciseIntensity = 'moderate';
             this.userData.preferredExerciseTypes = ['mixed', 'functional', 'bodyweight'];
         }
         
         // تعديل حسب BMI
         if (bmi > 30) {
             this.userData.preferredExerciseTypes.push('low-impact');
             console.log('⚙️ Added low-impact exercises for high BMI');
         }
         
         // إضافة تفضيلات إضافية
         this.userData.restPreference = this.calculateOptimalRest();
         this.userData.progressionRate = this.getProgressionRate();
         
         console.log('✅ User preferences added:', {
             intensity: this.userData.exerciseIntensity,
             types: this.userData.preferredExerciseTypes,
             rest: this.userData.restPreference
         });
     }

     // دالة لحساب معدل التقدم المناسب
     getProgressionRate() {
         const { fitnessLevel, age } = this.userData;
         
         if (fitnessLevel === 'beginner') {
             return age > 40 ? 'slow' : 'moderate';
         } else if (fitnessLevel === 'intermediate') {
             return 'moderate';
         } else {
             return age > 35 ? 'moderate' : 'fast';
         }
     }

    async generatePlanContent() {
        try {
            console.log('🎯 Starting generatePlanContent with data:', this.userData);
            
            // Double check validation (should already be done in init)
            if (!this.userData.weight || !this.userData.height || !this.userData.workoutDays) {
                console.log('❌ Critical data missing in generatePlanContent');
                this.showErrorMessage();
                return;
            }

            console.log('📊 Getting BMI status...');
            const bmiStatus = this.getBMIStatus(this.userData.bmi);
            
            console.log('🏋️ Generating workout schedule...');
            const workoutSchedule = await this.generateWorkoutSchedule();
            
            console.log('📈 Calculating performance indicators...');
            const performance = this.calculatePerformanceIndicators();
            
            console.log('💡 Getting tailored tips...');
            const tips = this.getTailoredTips();
            
            console.log('✅ All data prepared, generating HTML content...');

        const content = `
            <!-- User Summary -->
            <div class="result-card user-summary fade-in">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-user"></i>
                    </div>
                    <h2 class="card-title">ملخص بياناتك</h2>
                </div>
                <div class="summary-grid">
                    <div class="summary-item">
                        <div class="summary-value">${this.getGoalArabic(this.userData.goal)}</div>
                        <div class="summary-label">الهدف</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">${this.getSplitArabic(this.userData.split)}</div>
                        <div class="summary-label">نوع التمرين</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">${this.userData.weight} كيلو</div>
                        <div class="summary-label">الوزن</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">${this.userData.height} سم</div>
                        <div class="summary-label">الطول</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">${this.userData.bmi}</div>
                        <div class="summary-label">مؤشر كتلة الجسم</div>
                        <div class="bmi-status ${bmiStatus.class}">${bmiStatus.status}</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">${this.getFitnessLevelArabic(this.userData.fitnessLevel)}</div>
                        <div class="summary-label">مستوى اللياقة</div>
                    </div>
                    <div class="summary-item">
                        <div class="summary-value">${this.userData.workoutDays} أيام</div>
                        <div class="summary-label">أيام التمرين أسبوعياً</div>
                    </div>
                </div>
            </div>

            <!-- Workout Plan -->
            <div class="result-card workout-plan fade-in">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-dumbbell"></i>
                    </div>
                    <h2 class="card-title">خطة التمرين المقترحة</h2>
                </div>
                
                <div class="plan-overview">
                    <div class="plan-stats">
                        <div class="plan-stat">
                            <div class="stat-number">${performance.programDuration}</div>
                            <div class="stat-label">مدة البرنامج</div>
                        </div>
                        <div class="plan-stat">
                            <div class="stat-number">${performance.sessionDuration}</div>
                            <div class="stat-label">مدة الجلسة</div>
                        </div>
                        <div class="plan-stat">
                            <div class="stat-number">${performance.restBetweenSets}</div>
                            <div class="stat-label">الراحة بين المجموعات</div>
                        </div>
                    </div>
                </div>

                <div class="workout-schedule-modern">
                    ${workoutSchedule.map((day, index) => `
                        <div class="workout-day-card ${day.exercises.length === 0 ? 'rest-day' : ''}" data-day="${index + 1}">
                            <div class="day-card-header">
                                <div class="day-number">${index + 1}</div>
                                <div class="day-info">
                                    <h3 class="day-title">${day.day}</h3>
                                    <span class="day-type">${day.type}</span>
                                </div>
                                <div class="day-status">
                                    ${day.exercises.length > 0 ? 
                                        `<span class="workout-badge"><i class="fas fa-dumbbell"></i> ${day.exercises.length} تمارين</span>` : 
                                        `<span class="rest-badge"><i class="fas fa-bed"></i> راحة</span>`
                                    }
                                </div>
                            </div>
                            
                            ${day.exercises.length > 0 ? `
                                <div class="exercises-grid">
                                    ${day.exercises.map((exercise, exerciseIndex) => {
                                        const exerciseNotes = this.generateExerciseNotes(exercise.name);
                                        return `
                                        <div class="exercise-card" data-exercise="${exerciseIndex}">
                                            <div class="exercise-card-header">
                                                <div class="exercise-icon">
                                                    ${getExerciseIcon(exercise.name)}
                                                </div>
                                                <div class="exercise-difficulty">
                                                    ${getExerciseDifficulty(exercise.name)}
                                                </div>
                                            </div>
                                            
                                            <div class="exercise-content">
                                                <h4 class="exercise-title">${exercise.name}</h4>
                                                <div class="exercise-stats">
                                                    <div class="stat-item">
                                                        <i class="fas fa-repeat"></i>
                                                        <span>${exercise.sets} مجموعات</span>
                                                    </div>
                                                    <div class="stat-item">
                                                        <i class="fas fa-hashtag"></i>
                                                        <span>${exercise.reps}</span>
                                                    </div>
                                                    <div class="stat-item">
                                                        <i class="fas fa-clock"></i>
                                                        <span>${exercise.rest}</span>
                                                    </div>
                                                </div>
                                                
                                                <!-- ملاحظات التمرين المخصصة -->
                                                <div class="exercise-notes">
                                                    ${exerciseNotes.map(note => `
                                                        <div class="exercise-note">
                                                            <i class="fas fa-lightbulb note-icon"></i>
                                                            <span class="note-text">${note}</span>
                                                        </div>
                                                    `).join('')}
                                                </div>
                                            </div>
                                            
                                            <div class="exercise-actions">
                                                <button class="action-btn demo-btn" onclick="showExerciseDemo('${exercise.name}')">
                                                    <i class="fas fa-play"></i> شرح
                                                </button>
                                                <button class="action-btn complete-btn" onclick="markExerciseComplete(${index}, ${exerciseIndex})">
                                                    <i class="fas fa-check"></i> تم
                                                </button>
                                            </div>
                                        </div>
                                        `;
                                    }).join('')}
                                </div>
                            ` : `
                                <div class="rest-day-content">
                                    <div class="rest-icon">
                                        <i class="fas fa-spa"></i>
                                    </div>
                                    <h4>يوم الراحة والاستشفاء</h4>
                                    <p>استرح جيداً، اشرب الماء، ومارس تمارين الإطالة الخفيفة</p>
                                    <div class="rest-activities">
                                        <span class="activity-tag"><i class="fas fa-walking"></i> مشي خفيف</span>
                                        <span class="activity-tag"><i class="fas fa-leaf"></i> تأمل</span>
                                        <span class="activity-tag"><i class="fas fa-tint"></i> ترطيب</span>
                                    </div>
                                </div>
                            `}
                        </div>
                    `).join('')}
                </div>
            </div>

            <!-- Performance Indicators -->
            <div class="result-card performance fade-in">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h2 class="card-title">مؤشرات الأداء المتوقعة</h2>
                </div>
                
                <div class="performance-grid">
                    <div class="performance-item">
                        <div class="performance-icon">🔥</div>
                        <div class="performance-value">${performance.weeklyCalories}</div>
                        <div class="performance-label">سعرة حرارية أسبوعياً</div>
                    </div>
                    <div class="performance-item">
                        <div class="performance-icon">⏰</div>
                        <div class="performance-value">${performance.weeklyTime} دقيقة</div>
                        <div class="performance-label">وقت التمرين أسبوعياً</div>
                    </div>
                    <div class="performance-item">
                        <div class="performance-icon">📈</div>
                        <div class="performance-value">${performance.expectedResults}</div>
                        <div class="performance-label">النتائج المتوقعة</div>
                    </div>
                </div>
            </div>

            <!-- Motivational Message -->
            ${this.generateMotivationalMessage()}

            <!-- Motivational Tips -->
            ${generateMotivationalTips(this.userData.goal)}

            <!-- Tailored Tips -->
            <div class="result-card tips fade-in">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-lightbulb"></i>
                    </div>
                    <h2 class="card-title">نصائح مخصصة لك</h2>
                </div>
                
                <div class="tips-grid">
                    ${tips.map(tip => `
                        <div class="tip-item">
                            <div class="tip-title">${tip.title}</div>
                            <div class="tip-content">${tip.content}</div>
                        </div>
                    `).join('')}
                </div>
            </div>

            <!-- Resource Links -->
            <div class="result-card resources fade-in">
                <div class="card-header">
                    <div class="card-icon">
                        <i class="fas fa-external-link-alt"></i>
                    </div>
                    <h2 class="card-title">مصادر مفيدة</h2>
                </div>
                
                <div class="resource-links">
                    <a href="/workout-plans" class="resource-link">
                        <div class="resource-icon">🏃‍♂️</div>
                        <div>أفضل 5 تمارين للمبتدئين</div>
                    </a>
                    <a href="/meal-generator" class="resource-link">
                        <div class="resource-icon">🥗</div>
                        <div>كيفية حساب احتياجك من البروتين</div>
                    </a>
                    <a href="/fitness-calculators" class="resource-link">
                        <div class="resource-icon">🧮</div>
                        <div>احسب مؤشر كتلة الجسم والسعرات</div>
                    </a>
                    <a href="/tips" class="resource-link">
                        <div class="resource-icon">💡</div>
                        <div>نصائح ذهبية للوصول لهدفك</div>
                    </a>
                    <a href="/community" class="resource-link">
                        <div class="resource-icon">👥</div>
                        <div>انضم لمجتمع اللياقة البدنية</div>
                    </a>
                    <a href="/gym-injuries" class="resource-link">
                        <div class="resource-icon">🛡️</div>
                        <div>كيفية تجنب إصابات الجيم</div>
                    </a>
                    <a href="/tips" class="resource-link">
                        <div class="resource-icon">📹</div>
                        <div>فيديو: شرح أنواع التمارين</div>
                    </a>
                </div>
            </div>
        `;

        console.log('🎨 Setting HTML content...');
        document.getElementById('planContent').innerHTML = content;
        console.log('✅ HTML content set successfully!');
        
        // Initialize modern features after content is loaded
        setTimeout(() => {
            console.log('🚀 Initializing modern features...');
            initializeModernFeatures();
        }, 100);
        
        console.log('🎉 generatePlanContent completed successfully!');
    } catch (error) {
        console.error('❌ Error generating plan content:', error);
        this.showEnhancedErrorMessage();
    }
}

// Action Functions
function startPlan() {
    // Save plan start date
    localStorage.setItem('planStartDate', new Date().toISOString());
    
    // Show success message
    showNotification({
        title: '🎉 مبروك! بدأت رحلتك',
        message: 'تم حفظ خطتك وبدء التتبع. ستجد تقدمك في صفحة المجتمع',
        action: 'اذهب للمجتمع',
        link: '/community'
    });
    
    // Update engagement data
    const engagement = JSON.parse(localStorage.getItem('workoutPlanEngagement') || '{}');
    engagement.planStarted = true;
    engagement.startDate = new Date().toISOString();
    localStorage.setItem('workoutPlanEngagement', JSON.stringify(engagement));
}

function downloadPDF() {
    // Simple PDF generation using window.print()
    const originalTitle = document.title;
    document.title = 'خطتي الشخصية - جسمي أحسن';
    
    // Hide action buttons for printing
    const actionButtons = document.querySelector('.action-buttons');
    if (actionButtons) actionButtons.style.display = 'none';
    
    window.print();
    
    // Restore original state
    document.title = originalTitle;
    if (actionButtons) actionButtons.style.display = 'block';
}

// Helper functions for exercise cards
function getExerciseIcon(exerciseName) {
    const imageMap = {
        'ضغط صدر': '/static/images/workouts/chest_press.svg',
        'سحب علوي': '/static/images/workouts/pull_ups.svg',
        'قرفصاء': '/static/images/workouts/squats.svg',
        'رفعة ميتة': '/static/images/workouts/deadlift.svg',
        'ضغط كتف': '/static/images/workouts/shoulder_press.svg',
        'عقلة': '/static/images/workouts/pull_ups.svg',
        'ديبس': '/static/images/workouts/dips.svg',
        'لونجز': '/static/images/workouts/lunges.svg',
        'بلانك': '/static/images/workouts/plank.svg',
        'كرانش': '/static/images/workouts/crunches.svg',
        'بايسبس': '/static/images/workouts/bicep_curls.svg',
        'ترايسبس': '/static/images/workouts/tricep_dips.svg',
        'كارديو': '/static/images/workouts/cardio.svg',
        'جري': '/static/images/workouts/running.svg',
        'دراجة': '/static/images/workouts/cycling.svg'
    };
    
    for (let key in imageMap) {
        if (exerciseName.includes(key)) {
            return `<img src="${imageMap[key]}" alt="${exerciseName}" class="exercise-thumbnail" loading="lazy" onerror="this.style.display='none'; this.nextElementSibling.style.display='inline';">
                    <span class="exercise-emoji" style="display:none;">🏋️‍♂️</span>`;
        }
    }
    return '<span class="exercise-emoji">🏋️‍♂️</span>'; // Default icon
}

function getExerciseDifficulty(exerciseName) {
    const difficultyMap = {
        'مبتدئ': ['ضغط صدر بالدمبل', 'سحب أمامي', 'قرفصاء بوزن الجسم'],
        'متوسط': ['ضغط صدر بالبار', 'سحب علوي', 'قرفصاء بالأوزان'],
        'متقدم': ['عقلة', 'ديبس', 'رفعة ميتة']
    };
    
    for (let level in difficultyMap) {
        if (difficultyMap[level].some(exercise => exerciseName.includes(exercise))) {
            const colors = {
                'مبتدئ': 'var(--success-color)',
                'متوسط': 'var(--warning-color)', 
                'متقدم': 'var(--danger-color)'
            };
            return `<span class="difficulty-badge" style="background: ${colors[level]}">${level}</span>`;
        }
    }
    return '<span class="difficulty-badge" style="background: var(--primary-color)">عادي</span>';
}

function showExerciseDemo(exerciseName) {
    // Show exercise demonstration modal
    const modal = document.createElement('div');
    modal.className = 'exercise-demo-modal';
    modal.innerHTML = `
        <div class="demo-content">
            <div class="demo-header">
                <h3>${exerciseName}</h3>
                <button class="close-demo" onclick="this.parentElement.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="demo-body">
                <div class="demo-video">
                    <div class="video-placeholder">
                        <i class="fas fa-play-circle"></i>
                        <p>فيديو توضيحي لتمرين ${exerciseName}</p>
                    </div>
                </div>
                <div class="demo-instructions">
                    <h4>خطوات التمرين:</h4>
                    <ul>
                        <li>تأكد من الإحماء قبل البدء</li>
                        <li>حافظ على الوضعية الصحيحة</li>
                        <li>تنفس بشكل منتظم</li>
                        <li>لا تتسرع في الحركة</li>
                    </ul>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function markExerciseComplete(dayIndex, exerciseIndex) {
    const exerciseCard = document.querySelector(`[data-day="${dayIndex + 1}"] [data-exercise="${exerciseIndex}"]`);
    if (exerciseCard) {
        exerciseCard.classList.add('completed');
        const completeBtn = exerciseCard.querySelector('.complete-btn');
        completeBtn.innerHTML = '<i class="fas fa-check-circle"></i> مكتمل';
        completeBtn.disabled = true;
        
        // Save progress to localStorage
        const progress = JSON.parse(localStorage.getItem('workoutProgress') || '{}');
        const today = new Date().toDateString();
        if (!progress[today]) progress[today] = [];
        progress[today].push({ day: dayIndex, exercise: exerciseIndex, timestamp: new Date().toISOString() });
        localStorage.setItem('workoutProgress', JSON.stringify(progress));
        
        // Show completion animation
        showCompletionAnimation(exerciseCard);
    }
}

function showCompletionAnimation(element) {
    const celebration = document.createElement('div');
    celebration.className = 'completion-celebration';
    celebration.innerHTML = '🎉';
    element.appendChild(celebration);
    
    setTimeout(() => {
        celebration.remove();
    }, 2000);
}

// Enhanced functionality for modern workout plan results
function initializeModernFeatures() {
    // Add interactive animations to action cards
    const actionCards = document.querySelectorAll('.action-card');
    actionCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Add hover effects to exercise cards
    const exerciseCards = document.querySelectorAll('.exercise-card');
    exerciseCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
            this.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
        });
    });
    
    // Add progress tracking for user engagement
    trackUserEngagement();
    
    // Initialize contextual recommendations
    initializeRecommendations();
    
    // Add social sharing functionality
    initializeSocialSharing();
    
    // Load saved progress
    loadWorkoutProgress();
}

function loadWorkoutProgress() {
    const progress = JSON.parse(localStorage.getItem('workoutProgress') || '{}');
    const today = new Date().toDateString();
    
    if (progress[today]) {
        progress[today].forEach(item => {
            markExerciseComplete(item.day, item.exercise);
        });
    }
}

// Track user engagement and provide personalized suggestions
function trackUserEngagement() {
    const startTime = Date.now();
    
    // Track time spent on page
    window.addEventListener('beforeunload', function() {
        const timeSpent = Date.now() - startTime;
        localStorage.setItem('workoutPlanEngagement', JSON.stringify({
            timeSpent: timeSpent,
            timestamp: new Date().toISOString(),
            planViewed: true
        }));
    });
    
    // Show engagement tips after 30 seconds
    setTimeout(() => {
        showEngagementTip();
    }, 30000);
}

// Show contextual engagement tips
function showEngagementTip() {
    const tips = [
        {
            title: "💡 نصيحة سريعة",
            message: "هل تعلم أن تتبع تقدمك يزيد من فرص نجاحك بنسبة 70%؟",
            action: "ابدأ التتبع الآن",
            link: "/community"
        },
        {
            title: "🥗 تذكير مهم",
            message: "التغذية السليمة تمثل 70% من نجاح خطة اللياقة البدنية",
            action: "احصل على خطة التغذية",
            link: "/meal-generator"
        },
        {
            title: "📊 احسب احتياجك",
            message: "معرفة احتياجك من السعرات الحرارية يساعدك على تحقيق هدفك بشكل أسرع",
            action: "احسب الآن",
            link: "/fitness-calculators"
        }
    ];
    
    const randomTip = tips[Math.floor(Math.random() * tips.length)];
    showNotification(randomTip);
}

// Show notification with tip
function showNotification(tip) {
    const notification = document.createElement('div');
    notification.className = 'engagement-notification';
    notification.innerHTML = `
        <div class="notification-content">
            <h4>${tip.title}</h4>
            <p>${tip.message}</p>
            <div class="notification-actions">
                <a href="${tip.link}" class="notification-btn primary">${tip.action}</a>
                <button class="notification-btn secondary" onclick="closeNotification(this)">لاحقاً</button>
            </div>
        </div>
    `;
    
    // Add notification styles
    const style = document.createElement('style');
    style.textContent = `
        .engagement-notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            z-index: 1000;
            max-width: 350px;
            animation: slideInUp 0.5s ease;
            border-left: 4px solid var(--primary-color);
        }
        
        .notification-content h4 {
            margin: 0 0 0.5rem 0;
            color: var(--primary-color);
            font-size: 1.1rem;
        }
        
        .notification-content p {
            margin: 0 0 1rem 0;
            color: #666;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        
        .notification-actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .notification-btn {
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.85rem;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .notification-btn.primary {
            background: var(--primary-color);
            color: white;
        }
        
        .notification-btn.secondary {
            background: #f8f9fa;
            color: #666;
            border: 1px solid #ddd;
        }
        
        @keyframes slideInUp {
            from {
                transform: translateY(100%);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
    `;
    
    document.head.appendChild(style);
    document.body.appendChild(notification);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 10000);
}

// Close notification
function closeNotification(button) {
    const notification = button.closest('.engagement-notification');
    notification.style.animation = 'slideInUp 0.3s ease reverse';
    setTimeout(() => {
        notification.remove();
    }, 300);}

    // دالة لإظهار مؤشر التحميل
    showLoadingIndicator() {
        const loadingHTML = `
            <div class="loading-indicator" id="loadingIndicator">
                <div class="loading-content">
                    <div class="loading-spinner"></div>
                    <p class="loading-text">جاري إنشاء خطتك الشخصية...</p>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', loadingHTML);
        console.log('🔄 Loading indicator shown');
    }

    // دالة لإخفاء مؤشر التحميل
    hideLoadingIndicator() {
        const indicator = document.getElementById('loadingIndicator');
        if (indicator) {
            indicator.remove();
            console.log('✅ Loading indicator hidden');
        }
    }

    // دالة للحصول على البيانات الثابتة كبديل
    getStaticWorkoutPlans() {
        return {
            full_body: {
                beginner: {
                    exercises: [
                        {
                            name: 'تمرين القرفصاء',
                            muscle: 'الأرجل والمؤخرة',
                            sets: 3,
                            reps: '12-15',
                            rest: '60-90 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'وزن الجسم'
                        },
                        {
                            name: 'تمرين الضغط',
                            muscle: 'الصدر والذراعين',
                            sets: 3,
                            reps: '8-12',
                            rest: '60-90 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'وزن الجسم'
                        },
                        {
                            name: 'تمرين البلانك',
                            muscle: 'البطن والجذع',
                            sets: 3,
                            reps: '30-45 ثانية',
                            rest: '60 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'وزن الجسم'
                        },
                        {
                            name: 'تمرين الطعنات',
                            muscle: 'الأرجل والمؤخرة',
                            sets: 3,
                            reps: '10-12 لكل رجل',
                            rest: '60-90 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'وزن الجسم'
                        }
                    ]
                },
                intermediate: {
                    exercises: [
                        {
                            name: 'تمرين القرفصاء بالأوزان',
                            muscle: 'الأرجل والمؤخرة',
                            sets: 4,
                            reps: '10-12',
                            rest: '90-120 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'دمبل أو باربل'
                        },
                        {
                            name: 'تمرين الضغط المائل',
                            muscle: 'الصدر والذراعين',
                            sets: 4,
                            reps: '8-10',
                            rest: '90-120 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'مقعد'
                        },
                        {
                            name: 'تمرين السحب',
                            muscle: 'الظهر والذراعين',
                            sets: 4,
                            reps: '6-8',
                            rest: '90-120 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'عقلة'
                        },
                        {
                            name: 'تمرين الضغط على الكتف',
                            muscle: 'الأكتاف',
                            sets: 3,
                            reps: '10-12',
                            rest: '90 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'دمبل'
                        }
                    ]
                },
                advanced: {
                    exercises: [
                        {
                            name: 'تمرين القرفصاء الأمامي',
                            muscle: 'الأرجل والجذع',
                            sets: 5,
                            reps: '6-8',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'باربل'
                        },
                        {
                            name: 'تمرين الضغط بذراع واحدة',
                            muscle: 'الصدر والذراعين والجذع',
                            sets: 4,
                            reps: '5-8 لكل ذراع',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'وزن الجسم'
                        },
                        {
                            name: 'تمرين الرفعة الميتة',
                            muscle: 'الظهر والأرجل',
                            sets: 5,
                            reps: '5-6',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'باربل'
                        },
                        {
                            name: 'تمرين الضغط العسكري',
                            muscle: 'الأكتاف والذراعين',
                            sets: 4,
                            reps: '6-8',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'باربل'
                        }
                    ]
                }
            },
            upper_lower: {
                beginner: {
                    upper: [
                        {
                            name: 'تمرين الضغط',
                            muscle: 'الصدر',
                            sets: 3,
                            reps: '8-12',
                            rest: '60-90 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'وزن الجسم'
                        },
                        {
                            name: 'تمرين الضغط على الكتف',
                            muscle: 'الأكتاف',
                            sets: 3,
                            reps: '10-12',
                            rest: '60-90 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'دمبل'
                        }
                    ],
                    lower: [
                        {
                            name: 'تمرين القرفصاء',
                            muscle: 'الأرجل',
                            sets: 3,
                            reps: '12-15',
                            rest: '60-90 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'وزن الجسم'
                        },
                        {
                            name: 'تمرين الطعنات',
                            muscle: 'الأرجل والمؤخرة',
                            sets: 3,
                            reps: '10-12 لكل رجل',
                            rest: '60-90 ثانية',
                            difficulty: 'مبتدئ',
                            equipment: 'وزن الجسم'
                        }
                    ]
                },
                intermediate: {
                    upper: [
                        {
                            name: 'تمرين الضغط بالدمبل',
                            muscle: 'الصدر',
                            sets: 4,
                            reps: '8-10',
                            rest: '90-120 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'دمبل'
                        },
                        {
                            name: 'تمرين السحب',
                            muscle: 'الظهر',
                            sets: 4,
                            reps: '6-8',
                            rest: '90-120 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'عقلة'
                        }
                    ],
                    lower: [
                        {
                            name: 'تمرين القرفصاء بالأوزان',
                            muscle: 'الأرجل',
                            sets: 4,
                            reps: '10-12',
                            rest: '90-120 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'دمبل'
                        },
                        {
                            name: 'تمرين الرفعة الميتة الرومانية',
                            muscle: 'الأرجل الخلفية',
                            sets: 4,
                            reps: '10-12',
                            rest: '90-120 ثانية',
                            difficulty: 'متوسط',
                            equipment: 'دمبل'
                        }
                    ]
                },
                advanced: {
                    upper: [
                        {
                            name: 'تمرين الضغط بالباربل',
                            muscle: 'الصدر',
                            sets: 5,
                            reps: '6-8',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'باربل'
                        },
                        {
                            name: 'تمرين السحب بالأوزان',
                            muscle: 'الظهر',
                            sets: 5,
                            reps: '5-6',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'أوزان إضافية'
                        }
                    ],
                    lower: [
                        {
                            name: 'تمرين القرفصاء الخلفي',
                            muscle: 'الأرجل',
                            sets: 5,
                            reps: '6-8',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'باربل'
                        },
                        {
                            name: 'تمرين الرفعة الميتة',
                            muscle: 'الأرجل والظهر',
                            sets: 5,
                            reps: '5-6',
                            rest: '2-3 دقائق',
                            difficulty: 'متقدم',
                            equipment: 'باربل'
                        }
                    ]
                }
            }
        };
    }
}

// Initialize contextual recommendations based on user goal
function initializeRecommendations() {
    const userData = JSON.parse(localStorage.getItem('workoutPlanData') || '{}');
    
    if (userData.goal) {
        addContextualRecommendations(userData.goal);
    }
}

// Add contextual recommendations
function addContextualRecommendations(goal) {
    const recommendations = {
        'weight_loss': [
            { text: 'احسب احتياجك من السعرات', link: '/fitness-calculators', icon: '🧮' },
            { text: 'وجبات صحية لفقدان الوزن', link: '/meal-generator', icon: '🥗' },
            { text: 'نصائح حرق الدهون', link: '/tips', icon: '🔥' }
        ],
        'muscle_gain': [
            { text: 'احسب احتياجك من البروتين', link: '/fitness-calculators', icon: '💪' },
            { text: 'وجبات لبناء العضلات', link: '/meal-generator', icon: '🍖' },
            { text: 'مكملات غذائية مفيدة', link: '/supplements', icon: '💊' }
        ],
        'weight_gain': [
            { text: 'احسب السعرات المطلوبة', link: '/fitness-calculators', icon: '📊' },
            { text: 'وجبات عالية السعرات', link: '/meal-generator', icon: '🍽️' },
            { text: 'نصائح زيادة الوزن الصحي', link: '/tips', icon: '📈' }
        ]
    };
    
    const goalRecommendations = recommendations[goal] || recommendations['weight_loss'];
    
    // Add recommendations to quick links if they don't exist
    const quickLinksGrid = document.querySelector('.quick-links-grid');
    if (quickLinksGrid) {
        goalRecommendations.forEach(rec => {
            const existingLink = quickLinksGrid.querySelector(`a[href="${rec.link}"]`);
            if (!existingLink) {
                const linkElement = document.createElement('a');
                linkElement.href = rec.link;
                linkElement.className = 'quick-link recommended';
                linkElement.innerHTML = `
                    <i class="fas fa-star"></i>
                    <span>${rec.text}</span>
                    <span class="rec-badge">مُوصى</span>
                `;
                quickLinksGrid.appendChild(linkElement);
            }
        });
    }
}

// Initialize social sharing
function initializeSocialSharing() {
    // Add share button to action section
    const actionGrid = document.querySelector('.action-grid');
    if (actionGrid && !document.querySelector('.share-card')) {
        const shareCard = document.createElement('div');
        shareCard.className = 'action-card share-card';
        shareCard.innerHTML = `
            <div class="action-icon">
                <i class="fas fa-share-alt"></i>
            </div>
            <h3>شارك إنجازك</h3>
            <p>شارك خطتك مع الأصدقاء وحفزهم للبدء</p>
            <div class="action-badge">مجاني</div>
        `;
        
        shareCard.onclick = function() {
            shareWorkoutPlan();
        };
        
        actionGrid.appendChild(shareCard);
    }
}

// Share workout plan
function shareWorkoutPlan() {
    const shareData = {
        title: 'خطة التمرين المخصصة لي',
        text: 'حصلت على خطة تمرين مخصصة من موقع اللياقة البدنية! انضم إلي وابدأ رحلتك نحو اللياقة',
        url: window.location.href
    };
    
    if (navigator.share) {
        navigator.share(shareData);
    } else {
        // Fallback for browsers that don't support Web Share API
        const shareText = `${shareData.text} ${shareData.url}`;
        navigator.clipboard.writeText(shareText).then(() => {
            showNotification({
                title: '✅ تم النسخ',
                message: 'تم نسخ رابط خطتك! يمكنك مشاركته مع أصدقائك',
                action: 'رائع',
                link: '#'
            });
        });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', async function() {
    const workoutPlan = new WorkoutPlanResult();
    await workoutPlan.init();
    
    // Initialize modern features
    initializeModernFeatures();
});

// Add some dynamic effects
document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.result-card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.6s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        }, index * 200);
    });
    
    // Add CSS for exercise thumbnails
    const style = document.createElement('style');
    style.textContent = `
        .exercise-thumbnail {
            width: 40px;
            height: 40px;
            border-radius: 8px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }
        
        .exercise-thumbnail:hover {
            transform: scale(1.1);
        }
        
        .exercise-emoji {
            font-size: 24px;
            display: inline-block;
        }
        
        .exercise-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            margin-bottom: 10px;
        }
        
        .exercise-card:hover .exercise-thumbnail {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
    `;
    document.head.appendChild(style);
});