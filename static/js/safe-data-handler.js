/**
 * Safe Data Handler for Workout APIs
 * يوفر دوال آمنة للتعامل مع البيانات من مختلف APIs
 */

class SafeDataHandler {
    
    /**
     * التحقق من أن البيانات مصفوفة وإرجاع مصفوفة آمنة
     * @param {any} data - البيانات المراد فحصها
     * @param {string} fallbackMessage - رسالة بديلة في حالة عدم وجود بيانات
     * @returns {Array} مصفوفة آمنة
     */
    static ensureArray(data, fallbackMessage = 'لا توجد بيانات متاحة') {
        if (Array.isArray(data)) {
            return data;
        }
        
        if (data && typeof data === 'object') {
            // إذا كان كائن، حاول تحويله لمصفوفة
            return Object.values(data);
        }
        
        if (data && typeof data === 'string') {
            return [data];
        }
        
        // إرجاع مصفوفة فارغة مع رسالة بديلة
        return [{ message: fallbackMessage, type: 'info' }];
    }
    
    /**
     * معالجة آمنة لخطة التغذية
     * @param {any} nutritionPlan - خطة التغذية
     * @returns {Array} مصفوفة آمنة من النصائح الغذائية
     */
    static processNutritionPlan(nutritionPlan) {
        if (!nutritionPlan) {
            return [{
                category: 'معلومة',
                advice: 'لم يتم تضمين خطة تغذية مخصصة في هذه الخطة',
                type: 'info'
            }];
        }
        
        // إذا كانت مصفوفة، أرجعها كما هي
        if (Array.isArray(nutritionPlan)) {
            return nutritionPlan.map(tip => ({
                category: tip.category || 'نصيحة غذائية',
                advice: tip.advice || tip.message || tip,
                foods: tip.foods || [],
                type: tip.type || 'tip'
            }));
        }
        
        // إذا كان كائن، حوله لمصفوفة
        if (typeof nutritionPlan === 'object') {
            return Object.entries(nutritionPlan).map(([key, value]) => ({
                category: key,
                advice: typeof value === 'string' ? value : JSON.stringify(value),
                type: 'tip'
            }));
        }
        
        // إذا كان نص، أرجعه كعنصر واحد
        if (typeof nutritionPlan === 'string') {
            return [{
                category: 'نصيحة غذائية',
                advice: nutritionPlan,
                type: 'tip'
            }];
        }
        
        return [{
            category: 'خطأ',
            advice: 'تعذر معالجة بيانات خطة التغذية',
            type: 'error'
        }];
    }
    
    /**
     * معالجة آمنة للتمارين
     * @param {any} exercises - التمارين
     * @returns {Array} مصفوفة آمنة من التمارين
     */
    static processExercises(exercises) {
        return this.ensureArray(exercises, 'لا توجد تمارين متاحة');
    }
    
    /**
     * معالجة آمنة للنصائح العامة
     * @param {any} tips - النصائح
     * @returns {Array} مصفوفة آمنة من النصائح
     */
    static processGeneralTips(tips) {
        return this.ensureArray(tips, 'لا توجد نصائح متاحة');
    }
    
    /**
     * معالجة آمنة لأسباب عدم الاستمرار وحلولها
     * @param {any} reasons - أسباب عدم الاستمرار
     * @returns {Array} مصفوفة آمنة من الأسباب والحلول
     */
    static processQuitReasons(reasons) {
        if (!reasons) return [];
        
        const safeReasons = this.ensureArray(reasons);
        
        return safeReasons.map(item => ({
            reason: item.reason || item.title || 'سبب غير محدد',
            solutions: this.ensureArray(item.solutions || item.solution, 'لا توجد حلول متاحة'),
            type: item.type || 'solution'
        }));
    }
    
    /**
     * التحقق من نوع API المستخدم بناءً على هيكل البيانات
     * @param {Object} planData - بيانات الخطة
     * @returns {string} نوع API
     */
    static detectApiType(planData) {
        if (!planData) return 'unknown';
        
        // التحقق من وجود خصائص مميزة لكل API
        if (planData.user_analysis && planData.weekly_plans) {
            return 'advanced';
        }
        
        if (planData.plan && planData.general_tips && planData.reasons_for_quitting) {
            return 'personalized';
        }
        
        return 'unknown';
    }
    
    /**
     * معالجة شاملة لبيانات الخطة بناءً على نوع API
     * @param {Object} planData - بيانات الخطة
     * @returns {Object} بيانات معالجة ومنظمة
     */
    static processWorkoutPlan(planData) {
        const apiType = this.detectApiType(planData);
        
        const processedData = {
            apiType: apiType,
            userInfo: planData.user_info || planData.user_profile || {},
            nutritionPlan: this.processNutritionPlan(planData.nutrition_plan),
            generalTips: this.processGeneralTips(planData.general_tips),
            quitReasons: this.processQuitReasons(planData.reasons_for_quitting || planData.quit_solutions),
            exercises: [],
            weeklyPlans: []
        };
        
        // معالجة التمارين حسب نوع API
        if (apiType === 'personalized') {
            processedData.exercises = this.processExercises(planData.plan);
            processedData.goal = planData.goal;
            processedData.level = planData.level;
            processedData.trainingDays = planData.training_days;
            processedData.equipment = planData.equipment;
        } else if (apiType === 'advanced') {
            processedData.weeklyPlans = this.ensureArray(planData.weekly_plans);
            processedData.userAnalysis = planData.user_analysis;
            processedData.alternativeExercises = this.ensureArray(planData.alternative_exercises);
            processedData.personalizedMotivation = this.ensureArray(planData.personalized_motivation);
        }
        
        return processedData;
    }
    
    /**
     * تسجيل معلومات تشخيصية للمطورين
     * @param {string} context - السياق
     * @param {any} data - البيانات
     */
    static debugLog(context, data) {
        if (window.console && console.log) {
            console.group(`🔍 Safe Data Handler - ${context}`);
            console.log('Data type:', typeof data);
            console.log('Is Array:', Array.isArray(data));
            console.log('Data:', data);
            console.groupEnd();
        }
    }
}

// تصدير الكلاس للاستخدام العام
window.SafeDataHandler = SafeDataHandler;