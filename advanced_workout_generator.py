import sqlite3
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import math

class AdvancedWorkoutGenerator:
    def __init__(self, db_path: str = "fitness_app.db"):
        self.db_path = db_path
        self.arabic_translations = {
            'chest': 'صدر', 'back': 'ظهر', 'shoulders': 'أكتاف', 'biceps': 'بايسبس',
            'triceps': 'ترايسبس', 'legs': 'أرجل', 'abs': 'بطن', 'cardio': 'كارديو',
            'glutes': 'مؤخرة', 'calves': 'سمانة', 'forearms': 'ساعد', 'core': 'جذع',
            'beginner': 'مبتدئ', 'intermediate': 'متوسط', 'advanced': 'متقدم',
            'weight_loss': 'فقدان الوزن', 'muscle_gain': 'بناء العضلات', 
            'strength': 'القوة', 'endurance': 'التحمل', 'flexibility': 'المرونة'
        }
        
    def load_exercises_from_db(self) -> List[Dict]:
        """تحميل التمارين من قاعدة البيانات"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, target_muscle, equipment, difficulty_level, 
                       instructions, video_url, calories_per_minute
                FROM exercises
            """)
            exercises = []
            for row in cursor.fetchall():
                exercises.append({
                    'name': row[0],
                    'target_muscle': row[1],
                    'equipment': row[2] or 'bodyweight',
                    'difficulty': row[3] or 'beginner',
                    'instructions': row[4] or '',
                    'video_url': row[5] or '',
                    'calories_per_minute': row[6] or 5
                })
            conn.close()
            return exercises if exercises else self.get_default_exercises()
        except:
            return self.get_default_exercises()

    def get_default_exercises(self) -> List[Dict]:
        """التمارين الافتراضية في حالة عدم توفر قاعدة البيانات"""
        return [
            {
                'name': 'Push-ups', 'target_muscle': 'chest', 'equipment': 'bodyweight',
                'difficulty': 'beginner', 'instructions': 'تمرين الضغط الكلاسيكي',
                'video_url': 'https://example.com/pushups', 'calories_per_minute': 8
            },
            {
                'name': 'Squats', 'target_muscle': 'legs', 'equipment': 'bodyweight',
                'difficulty': 'beginner', 'instructions': 'تمرين القرفصاء',
                'video_url': 'https://example.com/squats', 'calories_per_minute': 10
            },
            {
                'name': 'Plank', 'target_muscle': 'core', 'equipment': 'bodyweight',
                'difficulty': 'beginner', 'instructions': 'تمرين البلانك',
                'video_url': 'https://example.com/plank', 'calories_per_minute': 6
            },
            {
                'name': 'Burpees', 'target_muscle': 'cardio', 'equipment': 'bodyweight',
                'difficulty': 'intermediate', 'instructions': 'تمرين البيربي',
                'video_url': 'https://example.com/burpees', 'calories_per_minute': 15
            }
        ]

    def calculate_user_metrics(self, user_data: Dict) -> Dict:
        """حساب المؤشرات الصحية للمستخدم"""
        # تحويل البيانات إلى أرقام لتجنب أخطاء العمليات الحسابية
        height = float(user_data['height'])
        weight = float(user_data['weight'])
        age = int(user_data['age'])
        gender = user_data['gender']
        
        height_m = height / 100
        
        # حساب BMI
        bmi = weight / (height_m ** 2)
        
        # حساب BMR (معدل الأيض الأساسي)
        if gender.lower() == 'male':
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        
        # حساب TDEE (إجمالي الطاقة المستهلكة يومياً)
        activity_multipliers = {
            'sedentary': 1.2, 'lightly_active': 1.375, 'moderately_active': 1.55, 
            'very_active': 1.725, 'extremely_active': 1.9
        }
        activity_level = user_data.get('activity_level', 'moderately_active')
        tdee = bmr * activity_multipliers.get(activity_level, 1.55)
        
        # تحديد الوزن المثالي
        if gender.lower() == 'male':
            ideal_weight = 50 + 2.3 * ((height / 2.54) - 60)
        else:
            ideal_weight = 45.5 + 2.3 * ((height / 2.54) - 60)
        
        return {
            'bmi': round(bmi, 1),
            'bmr': round(bmr),
            'tdee': round(tdee),
            'ideal_weight': round(ideal_weight, 1),
            'weight_difference': round(weight - ideal_weight, 1),
            'bmi_category': self.get_bmi_category(bmi)
        }

    def get_bmi_category(self, bmi: float) -> str:
        """تصنيف BMI"""
        if bmi < 18.5:
            return 'نقص في الوزن'
        elif bmi < 25:
            return 'وزن طبيعي'
        elif bmi < 30:
            return 'زيادة في الوزن'
        else:
            return 'سمنة'

    def analyze_user_progress(self, user_data: Dict, week_number: int) -> Dict:
        """تحليل تقدم المستخدم وتعديل الخطة"""
        base_intensity = 1.0
        
        # تعديل الشدة حسب الأسبوع
        weekly_progression = {
            1: 1.0,    # الأسبوع الأول - شدة أساسية
            2: 1.15,   # زيادة 15%
            3: 1.3,    # زيادة 30%
            4: 1.45    # زيادة 45%
        }
        
        intensity_multiplier = weekly_progression.get(week_number, 1.0)
        
        # تعديل حسب مستوى اللياقة
        fitness_adjustments = {
            'beginner': 0.8,
            'intermediate': 1.0,
            'advanced': 1.2
        }
        
        fitness_level = user_data.get('level', 'beginner')
        fitness_multiplier = fitness_adjustments.get(fitness_level, 1.0)
        
        # تعديل حسب الهدف
        goal_adjustments = {
            'weight_loss': {'cardio_boost': 1.3, 'strength_ratio': 0.7},
            'muscle_gain': {'cardio_boost': 0.8, 'strength_ratio': 1.4},
            'strength': {'cardio_boost': 0.9, 'strength_ratio': 1.3},
            'endurance': {'cardio_boost': 1.4, 'strength_ratio': 0.9}
        }
        
        goal = user_data.get('goal', 'weight_loss')
        goal_adjustment = goal_adjustments.get(goal, goal_adjustments['weight_loss'])
        
        return {
            'intensity_multiplier': intensity_multiplier * fitness_multiplier,
            'cardio_boost': goal_adjustment['cardio_boost'],
            'strength_ratio': goal_adjustment['strength_ratio'],
            'recommended_rest_days': max(1, 3 - (week_number - 1)),
            'progression_notes': self.get_progression_notes(week_number, fitness_level)
        }

    def get_progression_notes(self, week: int, fitness_level: str) -> List[str]:
        """ملاحظات التقدم الأسبوعي"""
        notes = {
            1: [
                "ركز على تعلم الحركات الصحيحة",
                "ابدأ بأوزان خفيفة أو وزن الجسم",
                "استمع لجسمك ولا تجبر نفسك"
            ],
            2: [
                "زد الشدة تدريجياً",
                "حافظ على الانتظام في التمارين",
                "راقب تحسن قوتك وتحملك"
            ],
            3: [
                "تحدى نفسك بتمارين أكثر صعوبة",
                "زد عدد التكرارات أو الأوزان",
                "ركز على التقنية مع زيادة الشدة"
            ],
            4: [
                "اختبر حدودك بحذر",
                "قيم تقدمك منذ البداية",
                "خطط للمرحلة التالية من التدريب"
            ]
        }
        return notes.get(week, notes[1])

    def generate_nutrition_advice(self, user_data: Dict, metrics: Dict) -> Dict:
        """توليد النصائح الغذائية المخصصة"""
        goal = user_data.get('goal', 'weight_loss')
        weight = float(user_data.get('weight', 70))  # تحويل الوزن إلى رقم
        tdee = metrics['tdee']
        
        # حساب السعرات المطلوبة حسب الهدف
        calorie_adjustments = {
            'weight_loss': -500,    # عجز 500 سعرة
            'muscle_gain': +300,    # فائض 300 سعرة
            'strength': +200,       # فائض 200 سعرة
            'endurance': 0          # توازن
        }
        
        target_calories = tdee + calorie_adjustments.get(goal, -500)
        
        # توزيع المغذيات الكبرى
        if goal == 'muscle_gain':
            protein_ratio, carb_ratio, fat_ratio = 0.3, 0.4, 0.3
        elif goal == 'weight_loss':
            protein_ratio, carb_ratio, fat_ratio = 0.35, 0.35, 0.3
        else:
            protein_ratio, carb_ratio, fat_ratio = 0.25, 0.45, 0.3
        
        protein_grams = (target_calories * protein_ratio) / 4
        carb_grams = (target_calories * carb_ratio) / 4
        fat_grams = (target_calories * fat_ratio) / 9
        
        # نصائح مخصصة
        general_tips = [
            "اشرب 8-10 أكواب من الماء يومياً",
            "تناول 5-6 وجبات صغيرة بدلاً من 3 وجبات كبيرة",
            "أكثر من الخضروات والفواكه الطازجة"
        ]
        
        goal_specific_tips = {
            'weight_loss': [
                "تجنب السكريات المضافة والمشروبات الغازية",
                "اختر البروتينات الخالية من الدهون",
                "تناول الألياف لزيادة الشبع"
            ],
            'muscle_gain': [
                "تناول البروتين خلال 30 دقيقة بعد التمرين",
                "لا تهمل الكربوهيدرات المعقدة",
                "أضف المكسرات والأفوكادو لزيادة السعرات"
            ]
        }
        
        return {
            'target_calories': round(target_calories),
            'macros': {
                'protein_grams': round(protein_grams),
                'carb_grams': round(carb_grams),
                'fat_grams': round(fat_grams)
            },
            'meal_timing': self.get_meal_timing(user_data),
            'general_tips': general_tips,
            'goal_specific_tips': goal_specific_tips.get(goal, general_tips),
            'hydration_goal': f"{max(8, round(weight * 0.035))} أكواب من الماء يومياً"
        }

    def get_meal_timing(self, user_data: Dict) -> List[Dict]:
        """توقيت الوجبات المقترح"""
        training_days = user_data.get('training_days', 3)
        
        if training_days >= 5:
            return [
                {'meal': 'الإفطار', 'time': '7:00', 'notes': 'وجبة متوازنة لبدء اليوم'},
                {'meal': 'وجبة خفيفة', 'time': '10:00', 'notes': 'فاكهة أو مكسرات'},
                {'meal': 'الغداء', 'time': '13:00', 'notes': 'وجبة رئيسية متكاملة'},
                {'meal': 'قبل التمرين', 'time': '16:00', 'notes': 'كربوهيدرات سريعة'},
                {'meal': 'بعد التمرين', 'time': '18:30', 'notes': 'بروتين + كربوهيدرات'},
                {'meal': 'العشاء', 'time': '20:00', 'notes': 'وجبة خفيفة غنية بالبروتين'}
            ]
        else:
            return [
                {'meal': 'الإفطار', 'time': '8:00', 'notes': 'وجبة متوازنة'},
                {'meal': 'الغداء', 'time': '13:00', 'notes': 'وجبة رئيسية'},
                {'meal': 'وجبة خفيفة', 'time': '16:00', 'notes': 'حسب جدول التمرين'},
                {'meal': 'العشاء', 'time': '19:00', 'notes': 'وجبة خفيفة'}
            ]

    def generate_alternative_exercises(self, exercise: Dict, user_data: Dict) -> List[Dict]:
        """توليد تمارين بديلة"""
        exercises = self.load_exercises_from_db()
        target_muscle = exercise['target_muscle']
        equipment = user_data.get('available_equipment', ['bodyweight'])
        
        alternatives = []
        for ex in exercises:
            if (ex['target_muscle'] == target_muscle and 
                ex['name'] != exercise['name'] and
                ex['equipment'] in equipment):
                alternatives.append({
                    'name': ex['name'],
                    'reason': 'نفس العضلة المستهدفة',
                    'difficulty': ex['difficulty'],
                    'equipment': ex['equipment']
                })
        
        # إضافة بدائل حسب الإصابات
        injuries = user_data.get('injuries', [])
        if injuries:
            safe_alternatives = self.get_injury_safe_alternatives(exercise, injuries)
            alternatives.extend(safe_alternatives)
        
        return alternatives[:3]  # أفضل 3 بدائل

    def get_injury_safe_alternatives(self, exercise: Dict, injuries: List[str]) -> List[Dict]:
        """بدائل آمنة للإصابات"""
        injury_alternatives = {
            'knee': [
                {'name': 'Wall Sits', 'reason': 'آمن للركبة', 'difficulty': 'beginner'},
                {'name': 'Leg Extensions (seated)', 'reason': 'تقوية بدون ضغط', 'difficulty': 'beginner'}
            ],
            'back': [
                {'name': 'Bird Dog', 'reason': 'تقوية الظهر بأمان', 'difficulty': 'beginner'},
                {'name': 'Dead Bug', 'reason': 'تقوية الجذع', 'difficulty': 'beginner'}
            ],
            'shoulder': [
                {'name': 'Wall Push-ups', 'reason': 'أقل ضغطاً على الكتف', 'difficulty': 'beginner'},
                {'name': 'Resistance Band Exercises', 'reason': 'حركة محكومة', 'difficulty': 'beginner'}
            ]
        }
        
        alternatives = []
        for injury in injuries:
            if injury.lower() in injury_alternatives:
                alternatives.extend(injury_alternatives[injury.lower()])
        
        return alternatives

    def generate_personalized_motivation(self, user_data: Dict, week: int) -> Dict:
        """توليد التحفيز الشخصي"""
        name = user_data.get('name', 'البطل')
        goal = user_data.get('goal', 'weight_loss')
        fitness_level = user_data.get('level', 'beginner')
        
        # رسائل تحفيزية حسب الأسبوع
        weekly_motivation = {
            1: f"مرحباً {name}! أنت تبدأ رحلة رائعة نحو تحقيق هدفك. كل خطوة تحسب!",
            2: f"أحسنت {name}! أسبوع واحد مضى وأنت على الطريق الصحيح. استمر!",
            3: f"رائع {name}! أنت في منتصف الطريق. قوتك وعزيمتك تزداد كل يوم!",
            4: f"مذهل {name}! الأسبوع الأخير - أظهر كل ما تعلمته وحققته!"
        }
        
        # نصائح حسب الهدف
        goal_motivation = {
            'weight_loss': [
                "تذكر: كل تمرين يحرق سعرات ويقربك من هدفك",
                "النتائج تحتاج وقت، لكن كل يوم تصبح أقوى",
                "ركز على كيف تشعر، ليس فقط على الميزان"
            ],
            'muscle_gain': [
                "كل تكرار يبني عضلة أقوى",
                "الراحة جزء مهم من بناء العضلات",
                "تناول البروتين واشرب الماء لأفضل النتائج"
            ]
        }
        
        # تحديات أسبوعية
        weekly_challenges = {
            1: "تحدي هذا الأسبوع: أكمل جميع التمارين المقررة",
            2: "تحدي هذا الأسبوع: زد 5 تكرارات في تمرين واحد",
            3: "تحدي هذا الأسبوع: جرب تمريناً جديداً",
            4: "تحدي هذا الأسبوع: اختبر تحسن قوتك منذ البداية"
        }
        
        return {
            'weekly_message': weekly_motivation.get(week, weekly_motivation[1]),
            'daily_motivation': goal_motivation.get(goal, goal_motivation['weight_loss']),
            'weekly_challenge': weekly_challenges.get(week, weekly_challenges[1]),
            'progress_reminder': f"أنت في الأسبوع {week} من 4 - استمر!",
            'success_tips': [
                "احتفل بالانجازات الصغيرة",
                "لا تقارن نفسك بالآخرين",
                "الثبات أهم من الكمال"
            ]
        }

    def generate_weekly_plan(self, user_data: Dict, week_number: int) -> Dict:
        """توليد خطة أسبوعية مفصلة"""
        exercises = self.load_exercises_from_db()
        metrics = self.calculate_user_metrics(user_data)
        progress_analysis = self.analyze_user_progress(user_data, week_number)
        
        # تحديد أيام التدريب
        training_days = user_data.get('training_days', 3)
        available_equipment = user_data.get('available_equipment', ['bodyweight'])
        injuries = user_data.get('injuries', [])
        
        # فلترة التمارين
        suitable_exercises = self.filter_exercises(
            exercises, available_equipment, injuries, user_data.get('level', 'beginner')
        )
        
        # توليد الخطة اليومية
        weekly_schedule = {}
        days = ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']
        
        training_pattern = self.get_training_pattern(training_days)
        
        for i, day in enumerate(days):
            if i in training_pattern:
                daily_exercises = self.select_daily_exercises(
                    suitable_exercises, user_data, progress_analysis, i
                )
                weekly_schedule[day] = {
                    'type': 'تدريب',
                    'exercises': daily_exercises,
                    'estimated_duration': self.calculate_workout_duration(daily_exercises),
                    'calories_burned': self.estimate_calories_burned(daily_exercises, user_data),
                    'focus': self.get_daily_focus(i, training_days)
                }
            else:
                weekly_schedule[day] = {
                    'type': 'راحة',
                    'activities': self.get_rest_day_activities(user_data),
                    'recovery_tips': [
                        "خذ حماماً دافئاً لاسترخاء العضلات",
                        "اشرب كمية كافية من الماء",
                        "احصل على نوم جيد (7-9 ساعات)"
                    ]
                }
        
        return {
            'week_number': week_number,
            'schedule': weekly_schedule,
            'weekly_goals': self.get_weekly_goals(week_number, user_data),
            'progress_tracking': {
                'measurements_to_track': ['الوزن', 'محيط الخصر', 'مستوى الطاقة', 'جودة النوم'],
                'performance_metrics': ['عدد التكرارات', 'مدة التمرين', 'مستوى الصعوبة المحتمل']
            }
        }

    def filter_exercises(self, exercises: List[Dict], equipment: List[str], 
                        injuries: List[str], fitness_level: str) -> List[Dict]:
        """فلترة التمارين حسب المعدات والإصابات والمستوى"""
        filtered = []
        
        for exercise in exercises:
            # فلترة حسب المعدات
            if exercise['equipment'] not in equipment and exercise['equipment'] != 'bodyweight':
                continue
            
            # فلترة حسب الإصابات
            if self.is_exercise_safe_for_injuries(exercise, injuries):
                # فلترة حسب مستوى اللياقة
                if self.is_exercise_appropriate_for_level(exercise, fitness_level):
                    filtered.append(exercise)
        
        return filtered

    def is_exercise_safe_for_injuries(self, exercise: Dict, injuries: List[str]) -> bool:
        """فحص أمان التمرين للإصابات"""
        unsafe_combinations = {
            'knee': ['squats', 'lunges', 'jumping'],
            'back': ['deadlifts', 'rows', 'heavy_lifting'],
            'shoulder': ['overhead_press', 'pull_ups', 'heavy_pushing'],
            'ankle': ['jumping', 'running', 'plyometric']
        }
        
        exercise_name_lower = exercise['name'].lower()
        
        for injury in injuries:
            injury_lower = injury.lower()
            if injury_lower in unsafe_combinations:
                for unsafe_movement in unsafe_combinations[injury_lower]:
                    if unsafe_movement in exercise_name_lower:
                        return False
        
        return True

    def is_exercise_appropriate_for_level(self, exercise: Dict, fitness_level: str) -> bool:
        """فحص مناسبة التمرين لمستوى اللياقة"""
        level_hierarchy = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        user_level = level_hierarchy.get(fitness_level, 1)
        exercise_level = level_hierarchy.get(exercise['difficulty'], 1)
        
        # السماح بتمارين من نفس المستوى أو أقل
        return exercise_level <= user_level + 1

    def get_training_pattern(self, training_days: int) -> List[int]:
        """تحديد نمط أيام التدريب"""
        patterns = {
            2: [1, 4],  # الثلاثاء والجمعة
            3: [0, 2, 5],  # الاثنين والأربعاء والسبت
            4: [0, 2, 4, 6],  # الاثنين والأربعاء والجمعة والأحد
            5: [0, 1, 3, 4, 6],  # الاثنين والثلاثاء والخميس والجمعة والأحد
            6: [0, 1, 2, 4, 5, 6]  # كل الأيام عدا الأربعاء
        }
        return patterns.get(training_days, patterns[3])

    def select_daily_exercises(self, exercises: List[Dict], user_data: Dict, 
                             progress_analysis: Dict, day_index: int) -> List[Dict]:
        """اختيار تمارين اليوم"""
        goal = user_data.get('goal', 'weight_loss')
        training_days = user_data.get('training_days', 3)
        
        # تحديد التركيز اليومي
        if training_days <= 3:
            # تمارين شاملة
            muscle_groups = ['chest', 'back', 'legs', 'core']
        else:
            # تقسيم العضلات
            muscle_split = {
                0: ['chest', 'triceps'],  # الاثنين
                1: ['back', 'biceps'],    # الثلاثاء
                2: ['legs', 'glutes'],    # الأربعاء
                3: ['shoulders', 'core'], # الخميس
                4: ['chest', 'back'],     # الجمعة
                5: ['legs', 'cardio'],    # السبت
                6: ['core', 'cardio']     # الأحد
            }
            muscle_groups = muscle_split.get(day_index, ['chest', 'back'])
        
        selected_exercises = []
        intensity = progress_analysis['intensity_multiplier']
        
        # اختيار التمارين لكل مجموعة عضلية
        for muscle_group in muscle_groups:
            muscle_exercises = [ex for ex in exercises if ex['target_muscle'] == muscle_group]
            if muscle_exercises:
                exercise = random.choice(muscle_exercises)
                
                # تحديد المجموعات والتكرارات
                sets, reps = self.calculate_sets_reps(exercise, user_data, intensity)
                
                exercise_plan = {
                    'name': exercise['name'],
                    'target_muscle': self.arabic_translations.get(exercise['target_muscle'], exercise['target_muscle']),
                    'sets': sets,
                    'reps': reps,
                    'rest_seconds': self.calculate_rest_time(exercise, user_data),
                    'difficulty': exercise['difficulty'],
                    'instructions': exercise['instructions'],
                    'video_url': exercise['video_url'],
                    'alternatives': self.generate_alternative_exercises(exercise, user_data),
                    'injury_prevention_tips': self.get_injury_prevention_tips(exercise),
                    'progression_notes': f"الأسبوع القادم: زد {random.randint(1, 3)} تكرارات"
                }
                selected_exercises.append(exercise_plan)
        
        # إضافة تمارين كارديو حسب الهدف
        if goal == 'weight_loss' or 'cardio' in muscle_groups:
            cardio_exercise = self.get_cardio_exercise(exercises, user_data, intensity)
            if cardio_exercise:
                selected_exercises.append(cardio_exercise)
        
        return selected_exercises

    def calculate_sets_reps(self, exercise: Dict, user_data: Dict, intensity: float) -> tuple:
        """حساب المجموعات والتكرارات"""
        goal = user_data.get('goal', 'weight_loss')
        fitness_level = user_data.get('level', 'beginner')
        
        base_sets = {'beginner': 2, 'intermediate': 3, 'advanced': 4}
        base_reps = {
            'weight_loss': {'beginner': 12, 'intermediate': 15, 'advanced': 18},
            'muscle_gain': {'beginner': 8, 'intermediate': 10, 'advanced': 12},
            'strength': {'beginner': 6, 'intermediate': 8, 'advanced': 10},
            'endurance': {'beginner': 15, 'intermediate': 20, 'advanced': 25}
        }
        
        sets = base_sets.get(fitness_level, 2)
        reps = base_reps.get(goal, base_reps['weight_loss']).get(fitness_level, 12)
        
        # تطبيق مضاعف الشدة
        reps = max(5, int(reps * float(intensity)))
        
        return sets, reps

    def calculate_rest_time(self, exercise: Dict, user_data: Dict) -> int:
        """حساب وقت الراحة بين المجموعات"""
        goal = user_data.get('goal', 'weight_loss')
        difficulty = exercise.get('difficulty', 'beginner')
        
        base_rest = {
            'weight_loss': 45,
            'muscle_gain': 90,
            'strength': 120,
            'endurance': 30
        }
        
        # دعم القيم العربية والإنجليزية
        difficulty_multiplier = {
            'beginner': 1.0,
            'intermediate': 1.2,
            'advanced': 1.5,
            'مبتدئ': 1.0,
            'متوسط': 1.2,
            'متقدم': 1.5
        }
        
        rest_time = base_rest.get(goal, 45)
        # التأكد من أن rest_time رقم
        rest_time = float(rest_time)
        multiplier = difficulty_multiplier.get(difficulty, 1.0)
        rest_time *= multiplier
        
        return int(rest_time)

    def get_cardio_exercise(self, exercises: List[Dict], user_data: Dict, intensity: float) -> Dict:
        """الحصول على تمرين كارديو"""
        cardio_exercises = [ex for ex in exercises if ex['target_muscle'] == 'cardio']
        
        if not cardio_exercises:
            # تمرين كارديو افتراضي
            cardio_exercise = {
                'name': 'Jumping Jacks',
                'target_muscle': 'cardio',
                'difficulty': 'beginner',
                'instructions': 'تمرين القفز مع فتح الذراعين والساقين',
                'video_url': 'https://example.com/jumping-jacks',
                'calories_per_minute': 12
            }
        else:
            cardio_exercise = random.choice(cardio_exercises)
        
        duration = max(10, int(20 * float(intensity)))  # 10-30 دقيقة
        
        return {
            'name': cardio_exercise['name'],
            'target_muscle': 'كارديو',
            'duration_minutes': duration,
            'intensity': 'متوسطة' if intensity < 1.2 else 'عالية',
            'instructions': cardio_exercise['instructions'],
            'video_url': cardio_exercise['video_url'],
            'alternatives': ['المشي السريع', 'الجري في المكان', 'تمارين الرقص'],
            'calories_estimate': int(duration * cardio_exercise.get('calories_per_minute', 10))
        }

    def calculate_workout_duration(self, exercises: List[Dict]) -> int:
        """حساب مدة التمرين المتوقعة"""
        total_minutes = 10  # وقت الإحماء والتبريد
        
        for exercise in exercises:
            if 'duration_minutes' in exercise:
                # تمرين كارديو
                total_minutes += int(exercise['duration_minutes'])
            else:
                # تمرين قوة
                sets = int(exercise.get('sets', 3))
                reps = int(exercise.get('reps', 12))
                rest_seconds = int(exercise.get('rest_seconds', 60))
                
                # تقدير وقت التمرين (ثانيتان لكل تكرار)
                exercise_time = (sets * reps * 2) + (sets * rest_seconds)
                total_minutes += exercise_time / 60
        
        return int(total_minutes)

    def estimate_calories_burned(self, exercises: List[Dict], user_data: Dict) -> int:
        """تقدير السعرات المحروقة"""
        weight = float(user_data.get('weight', 70))
        total_calories = 0
        
        # معدل حرق السعرات حسب نوع التمرين (سعرة/دقيقة/كيلو)
        calorie_rates = {
            'strength': 0.1,  # تمارين القوة
            'cardio': 0.15    # تمارين الكارديو
        }
        
        for exercise in exercises:
            if 'duration_minutes' in exercise:
                # تمرين كارديو
                duration = int(exercise['duration_minutes'])
                calories = duration * weight * calorie_rates['cardio']
            else:
                # تمرين قوة - تقدير المدة
                sets = int(exercise.get('sets', 3))
                reps = int(exercise.get('reps', 12))
                estimated_minutes = (sets * reps) / 10  # تقدير تقريبي
                calories = estimated_minutes * weight * calorie_rates['strength']
            
            total_calories += calories
        
        return int(total_calories)

    def get_daily_focus(self, day_index: int, training_days: int) -> str:
        """تحديد تركيز اليوم"""
        if training_days <= 3:
            focuses = ['الجسم كاملاً', 'القوة والتحمل', 'الكارديو والمرونة']
        else:
            focuses = ['الصدر والذراعين', 'الظهر والبايسبس', 'الأرجل والمؤخرة', 
                      'الأكتاف والجذع', 'القوة العامة', 'الكارديو', 'التعافي النشط']
        
        return focuses[day_index % len(focuses)]

    def get_rest_day_activities(self, user_data: Dict) -> List[str]:
        """أنشطة يوم الراحة"""
        activities = [
            'المشي الخفيف لمدة 20-30 دقيقة',
            'تمارين الإطالة والمرونة',
            'اليوغا أو التأمل',
            'السباحة الخفيفة',
            'التدليك الذاتي بالفوم رولر'
        ]
        
        # تخصيص حسب الهدف
        goal = user_data.get('goal', 'weight_loss')
        if goal == 'weight_loss':
            activities.extend(['المشي في الطبيعة', 'الأنشطة المنزلية'])
        elif goal == 'muscle_gain':
            activities.extend(['النوم الإضافي', 'تمارين التنفس العميق'])
        
        return random.sample(activities, 3)

    def get_weekly_goals(self, week: int, user_data: Dict) -> List[str]:
        """أهداف الأسبوع"""
        base_goals = [
            'إكمال جميع التمارين المجدولة',
            'شرب كمية كافية من الماء يومياً',
            'الحصول على نوم جيد (7-9 ساعات)'
        ]
        
        weekly_specific = {
            1: ['تعلم التقنية الصحيحة لكل تمرين', 'بناء عادة التمرين اليومي'],
            2: ['زيادة الشدة تدريجياً', 'تتبع التقدم في دفتر التمارين'],
            3: ['تحدي النفس بتمارين جديدة', 'تحسين التوازن الغذائي'],
            4: ['اختبار التحسن منذ البداية', 'التخطيط للمرحلة التالية']
        }
        
        goals = base_goals + weekly_specific.get(week, weekly_specific[1])
        
        # إضافة أهداف حسب الهدف الشخصي
        goal = user_data.get('goal', 'weight_loss')
        if goal == 'weight_loss':
            goals.append('تتبع السعرات المستهلكة')
        elif goal == 'muscle_gain':
            goals.append('تناول البروتين بعد كل تمرين')
        
        return goals

    def get_injury_prevention_tips(self, exercise: Dict) -> List[str]:
        """نصائح منع الإصابات"""
        general_tips = [
            'ابدأ بإحماء مناسب لمدة 5-10 دقائق',
            'ركز على التقنية الصحيحة قبل زيادة الشدة',
            'توقف فوراً إذا شعرت بألم حاد'
        ]
        
        exercise_specific = {
            'squats': ['حافظ على استقامة الظهر', 'لا تدع الركبتين تتجاوزان أصابع القدمين'],
            'push-ups': ['حافظ على خط مستقيم من الرأس للكعبين', 'لا تدع الوركين يهبطان'],
            'deadlifts': ['ارفع بساقيك وليس بظهرك', 'حافظ على قرب الوزن من جسمك'],
            'plank': ['لا تحبس أنفاسك', 'حافظ على وضعية محايدة للرقبة']
        }
        
        exercise_name = exercise['name'].lower()
        for key, tips in exercise_specific.items():
            if key in exercise_name:
                general_tips.extend(tips)
                break
        
        return general_tips

    def generate_comprehensive_plan(self, user_data: Dict) -> Dict:
        """توليد الخطة الشاملة لـ 4 أسابيع"""
        # حساب المؤشرات الصحية
        metrics = self.calculate_user_metrics(user_data)
        
        # توليد النصائح الغذائية
        nutrition_advice = self.generate_nutrition_advice(user_data, metrics)
        
        # توليد الخطط الأسبوعية
        weekly_plans = {}
        for week in range(1, 5):
            weekly_plans[f'week_{week}'] = self.generate_weekly_plan(user_data, week)
        
        # توليد التحفيز الشخصي لكل أسبوع
        motivation = {}
        for week in range(1, 5):
            motivation[f'week_{week}'] = self.generate_personalized_motivation(user_data, week)
        
        return {
            'user_profile': {
                'name': user_data.get('name', 'المتدرب'),
                'metrics': metrics,
                'goal': user_data.get('goal', 'weight_loss'),
                'fitness_level': user_data.get('level', 'beginner'),
                'training_days': user_data.get('training_days', 3)
            },
            'nutrition_plan': nutrition_advice,
            'workout_plans': weekly_plans,
            'motivation_system': motivation,
            'general_guidelines': {
                'safety_rules': [
                    'استشر طبيباً قبل بدء أي برنامج تمرين جديد',
                    'توقف فوراً إذا شعرت بألم أو دوخة',
                    'اشرب الماء قبل وأثناء وبعد التمرين',
                    'احصل على راحة كافية بين التمارين'
                ],
                'success_factors': [
                    'الثبات أهم من الكمال',
                    'التقدم التدريجي يمنع الإصابات',
                    'التغذية السليمة 70% من النجاح',
                    'النوم الجيد ضروري للتعافي'
                ],
                'tracking_recommendations': [
                    'سجل تمارينك في دفتر أو تطبيق',
                    'التقط صوراً للتقدم كل أسبوعين',
                    'قس وزنك في نفس الوقت كل أسبوع',
                    'راقب مستوى طاقتك ومزاجك'
                ]
            },
            'emergency_contacts': {
                'when_to_stop': [
                    'ألم حاد في الصدر أو صعوبة في التنفس',
                    'دوخة شديدة أو غثيان',
                    'ألم مفاجئ في المفاصل أو العضلات'
                ],
                'modification_signs': [
                    'تعب مستمر لأكثر من 3 أيام',
                    'فقدان الدافعية لأكثر من أسبوع',
                    'عدم رؤية أي تقدم بعد 3 أسابيع'
                ]
            }
        }