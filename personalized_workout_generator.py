"""
Personalized Workout Plan Generator
Professional fitness trainer and certified nutritionist system
"""

import json
import sqlite3
from datetime import datetime
import random

class PersonalizedWorkoutGenerator:
    def __init__(self, db_path='fitness_app.db'):
        self.db_path = db_path
        self.exercise_database = self._load_exercise_database()
        
    def _load_exercise_database(self):
        """Load exercises from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name_ar, name_en, muscle_group, equipment_type, 
                       difficulty_level, sets, reps, rest_time, 
                       instructions_ar, video_url
                FROM admin_exercises
            """)
            
            exercises = cursor.fetchall()
            conn.close()
            
            # Convert to dictionary format
            exercise_dict = {}
            for exercise in exercises:
                muscle_group = exercise['muscle_group']
                if muscle_group not in exercise_dict:
                    exercise_dict[muscle_group] = []
                
                exercise_dict[muscle_group].append({
                    'name_ar': exercise['name_ar'],
                    'name_en': exercise['name_en'],
                    'muscle_group': exercise['muscle_group'],
                    'equipment_type': exercise['equipment_type'],
                    'difficulty_level': exercise['difficulty_level'],
                    'sets': exercise['sets'],
                    'reps': exercise['reps'],
                    'rest_time': exercise['rest_time'],
                    'instructions': exercise['instructions_ar'],
                    'video_url': exercise['video_url'] or "https://www.youtube.com/watch?v=example"
                })
            
            return exercise_dict
            
        except Exception as e:
            print(f"Error loading exercise database: {e}")
            return self._get_default_exercises()
    
    def _get_default_exercises(self):
        """Fallback exercise database if DB is not available"""
        return {
            'chest': [
                {
                    'name_ar': 'تمرين الضغط',
                    'name_en': 'Push Ups',
                    'muscle_group': 'chest',
                    'equipment_type': 'bodyweight',
                    'difficulty_level': 'beginner',
                    'sets': '3-4',
                    'reps': '8-12',
                    'rest_time': '60-90 seconds',
                    'instructions': 'حافظ على استقامة الجسم وتجنب تقوس الظهر',
                    'video_url': 'https://www.youtube.com/watch?v=IODxDxX7oi4'
                }
            ],
            'back': [
                {
                    'name_ar': 'تمرين العقلة',
                    'name_en': 'Pull Ups',
                    'muscle_group': 'back',
                    'equipment_type': 'gym',
                    'difficulty_level': 'intermediate',
                    'sets': '3-4',
                    'reps': '6-10',
                    'rest_time': '90-120 seconds',
                    'instructions': 'اسحب جسمك لأعلى حتى يصل ذقنك فوق العارضة',
                    'video_url': 'https://www.youtube.com/watch?v=eGo4IYlbE5g'
                }
            ],
            'legs': [
                {
                    'name_ar': 'تمرين القرفصاء',
                    'name_en': 'Squats',
                    'muscle_group': 'legs',
                    'equipment_type': 'bodyweight',
                    'difficulty_level': 'beginner',
                    'sets': '3-4',
                    'reps': '12-15',
                    'rest_time': '60-90 seconds',
                    'instructions': 'انزل حتى تصبح فخذيك موازية للأرض',
                    'video_url': 'https://www.youtube.com/watch?v=YaXPRqUwItQ'
                }
            ],
            'shoulders': [
                {
                    'name_ar': 'تمرين الضغط العسكري',
                    'name_en': 'Military Press',
                    'muscle_group': 'shoulders',
                    'equipment_type': 'gym',
                    'difficulty_level': 'intermediate',
                    'sets': '3-4',
                    'reps': '8-12',
                    'rest_time': '90 seconds',
                    'instructions': 'ادفع الوزن لأعلى مع الحفاظ على استقامة الظهر',
                    'video_url': 'https://www.youtube.com/watch?v=2yjwXTZQDDI'
                }
            ],
            'arms': [
                {
                    'name_ar': 'تمرين العضلة ذات الرأسين',
                    'name_en': 'Bicep Curls',
                    'muscle_group': 'arms',
                    'equipment_type': 'gym',
                    'difficulty_level': 'beginner',
                    'sets': '3',
                    'reps': '10-12',
                    'rest_time': '60 seconds',
                    'instructions': 'ارفع الوزن ببطء مع تثبيت المرفقين',
                    'video_url': 'https://www.youtube.com/watch?v=ykJmrZ5v0Oo'
                }
            ],
            'core': [
                {
                    'name_ar': 'تمرين البلانك',
                    'name_en': 'Plank',
                    'muscle_group': 'core',
                    'equipment_type': 'bodyweight',
                    'difficulty_level': 'beginner',
                    'sets': '3',
                    'reps': '30-60 seconds',
                    'rest_time': '60 seconds',
                    'instructions': 'حافظ على استقامة الجسم من الرأس إلى القدمين',
                    'video_url': 'https://www.youtube.com/watch?v=pSHjTRCQxIw'
                }
            ]
        }

    def generate_workout_plan(self, user_data):
        """Generate personalized 4-week workout plan"""
        
        # Validate user data
        required_fields = ['name', 'age', 'gender', 'weight', 'height', 'goal', 'level', 'days_per_week', 'equipment']
        missing_fields = [field for field in required_fields if not user_data.get(field)]
        
        if missing_fields:
            return {
                'error': f'Missing required data: {", ".join(missing_fields)}',
                'required_fields': required_fields
            }
        
        # Extract user data
        goal = user_data.get('goal', '').lower()
        level = user_data.get('level', '').lower()
        days_per_week = int(user_data.get('days_per_week', 3))
        equipment = user_data.get('equipment', '').lower()
        health_issues = user_data.get('health_issues', '')
        selected_reasons = user_data.get('selected_reasons', [])
        
        # Generate workout plan
        plan = self._create_weekly_plan(goal, level, days_per_week, equipment, health_issues)
        
        # Generate general tips
        general_tips = self._generate_general_tips(goal, level, equipment, health_issues)
        
        # Generate quit reasons and solutions
        quit_reasons = self._generate_quit_solutions(selected_reasons, goal, level, days_per_week)
        
        return {
            'user_info': {
                'name': user_data.get('name'),
                'age': user_data.get('age'),
                'gender': user_data.get('gender'),
                'weight': user_data.get('weight'),
                'height': user_data.get('height')
            },
            'goal': self._translate_goal(goal),
            'level': self._translate_level(level),
            'training_days': days_per_week,
            'equipment': self._translate_equipment(equipment),
            'plan': plan,
            'general_tips': general_tips,
            'reasons_for_quitting': quit_reasons,
            'created_at': datetime.now().isoformat()
        }
    
    def _create_weekly_plan(self, goal, level, days_per_week, equipment, health_issues):
        """Create weekly workout plan based on user parameters"""
        
        # Define muscle group splits based on training days
        splits = {
            2: [['chest', 'arms'], ['legs', 'back']],
            3: [['chest', 'arms'], ['legs'], ['back', 'shoulders']],
            4: [['chest'], ['back'], ['legs'], ['arms', 'shoulders']],
            5: [['chest'], ['back'], ['legs'], ['shoulders'], ['arms', 'core']],
            6: [['chest', 'arms'], ['back'], ['legs'], ['shoulders'], ['arms'], ['core']]
        }
        
        # Get appropriate split
        if days_per_week <= 2:
            muscle_split = splits[2]
        elif days_per_week >= 6:
            muscle_split = splits[6]
        else:
            muscle_split = splits[days_per_week]
        
        plan = []
        
        for day_num, muscle_groups in enumerate(muscle_split, 1):
            day_exercises = []
            
            for muscle_group in muscle_groups:
                if muscle_group in self.exercise_database:
                    # Filter exercises by equipment and level
                    suitable_exercises = [
                        ex for ex in self.exercise_database[muscle_group]
                        if self._is_suitable_exercise(ex, equipment, level, health_issues)
                    ]
                    
                    if suitable_exercises:
                        # Select 2-3 exercises per muscle group
                        selected = random.sample(suitable_exercises, min(2, len(suitable_exercises)))
                        
                        for exercise in selected:
                            day_exercises.append({
                                'name': exercise['name_en'],
                                'name_ar': exercise['name_ar'],
                                'target_muscle': self._translate_muscle(muscle_group),
                                'sets': self._adjust_sets(exercise['sets'], level, goal),
                                'reps': self._adjust_reps(exercise['reps'], level, goal),
                                'difficulty': self._translate_level(exercise['difficulty_level']),
                                'video': exercise['video_url'],
                                'tips': self._generate_exercise_tips(exercise, health_issues, level)
                            })
            
            plan.append({
                'day': day_num,
                'muscle_groups': [self._translate_muscle(mg) for mg in muscle_groups],
                'exercises': day_exercises
            })
        
        return plan
    
    def _is_suitable_exercise(self, exercise, equipment, level, health_issues):
        """Check if exercise is suitable for user"""
        
        # Equipment check
        if equipment == 'home' and exercise['equipment_type'] == 'gym':
            return False
        
        # Level check
        exercise_level = exercise['difficulty_level'].lower()
        if level == 'beginner' and exercise_level == 'advanced':
            return False
        
        # Health issues check
        if health_issues:
            health_lower = health_issues.lower()
            exercise_name_lower = exercise['name_en'].lower()
            
            # Basic injury considerations
            if 'back' in health_lower and 'deadlift' in exercise_name_lower:
                return False
            if 'knee' in health_lower and 'squat' in exercise_name_lower:
                return False
            if 'shoulder' in health_lower and 'press' in exercise_name_lower:
                return False
        
        return True
    
    def _adjust_sets(self, base_sets, level, goal):
        """Adjust sets based on level and goal"""
        try:
            if '-' in str(base_sets):
                sets_range = base_sets.split('-')
                min_sets = int(sets_range[0])
                max_sets = int(sets_range[1])
            else:
                min_sets = max_sets = int(base_sets)
        except:
            min_sets, max_sets = 3, 4
        
        # Adjust based on level
        if level == 'beginner':
            return min_sets
        elif level == 'advanced':
            return max_sets
        else:
            return (min_sets + max_sets) // 2
    
    def _adjust_reps(self, base_reps, level, goal):
        """Adjust reps based on level and goal"""
        
        # Goal-based adjustments
        if goal in ['fat_loss', 'weight_loss']:
            if 'seconds' in str(base_reps):
                return base_reps
            return "12-15"  # Higher reps for fat loss
        elif goal in ['muscle_gain', 'muscle_building']:
            return "8-12"   # Moderate reps for muscle gain
        elif goal == 'strength':
            return "5-8"    # Lower reps for strength
        
        return base_reps
    
    def _generate_exercise_tips(self, exercise, health_issues, level):
        """Generate personalized tips for each exercise"""
        tips = [exercise['instructions']]
        
        # Level-based tips
        if level == 'beginner':
            tips.append("ابدأ بوزن خفيف وركز على التقنية الصحيحة")
        elif level == 'advanced':
            tips.append("يمكنك زيادة الوزن تدريجياً أو إضافة تقنيات متقدمة")
        
        # Health-based tips
        if health_issues:
            tips.append(f"انتبه لـ {health_issues} واستشر مدرب مختص إذا شعرت بألم")
        
        return " | ".join(tips)
    
    def _generate_general_tips(self, goal, level, equipment, health_issues):
        """Generate general tips based on user profile"""
        tips = [
            "اشرب 2-3 لتر ماء يومياً لتحسين الأداء والتعافي",
            "التزم بجدول تمارين ثابت لتحقيق أفضل النتائج",
            "احصل على 7-8 ساعات نوم يومياً للتعافي العضلي",
            "قم بالإحماء 5-10 دقائق قبل التمرين"
        ]
        
        # Goal-specific tips
        if goal in ['fat_loss', 'weight_loss']:
            tips.extend([
                "اتبع نظام غذائي متوازن مع عجز سعرات حرارية 300-500 سعرة",
                "أضف تمارين الكارديو 3-4 مرات أسبوعياً",
                "تناول البروتين في كل وجبة للحفاظ على العضلات"
            ])
        elif goal in ['muscle_gain', 'muscle_building']:
            tips.extend([
                "تناول 1.6-2.2 جرام بروتين لكل كيلو من وزن الجسم",
                "زد السعرات الحرارية بـ 300-500 سعرة عن احتياجك اليومي",
                "ركز على التمارين المركبة لبناء العضلات بفعالية"
            ])
        elif goal == 'weight_gain':
            tips.extend([
                "تناول 5-6 وجبات صغيرة بدلاً من 3 وجبات كبيرة",
                "أضف الدهون الصحية مثل المكسرات والأفوكادو",
                "اشرب العصائر الطبيعية والحليب بين الوجبات"
            ])
        
        # Equipment-specific tips
        if equipment == 'home':
            tips.extend([
                "استخدم وزن الجسم بفعالية لتحقيق نتائج ممتازة",
                "يمكنك استخدام أدوات منزلية كأوزان (زجاجات ماء، حقائب)",
                "احرص على وجود مساحة آمنة للتمرين"
            ])
        else:
            tips.extend([
                "استخدم الأوزان الحرة والآلات بالتناوب",
                "لا تتردد في طلب المساعدة من المدربين",
                "نظف الأجهزة قبل وبعد الاستخدام"
            ])
        
        # Level-specific tips
        if level == 'beginner':
            tips.extend([
                "ابدأ ببطء ولا تتعجل النتائج",
                "تعلم التقنية الصحيحة قبل زيادة الأوزان",
                "استمع لجسمك وخذ راحة عند الحاجة"
            ])
        elif level == 'advanced':
            tips.extend([
                "غير روتين التمارين كل 4-6 أسابيع",
                "استخدم تقنيات متقدمة مثل الدروب سيت والسوبر سيت",
                "راقب تقدمك بدقة وسجل الأوزان والتكرارات"
            ])
        
        return tips[:10]  # Return top 10 tips
    
    def _generate_quit_solutions(self, selected_reasons, goal, level, days_per_week):
        """Generate personalized solutions for potential quitting reasons"""
        
        solutions_database = {
            'lack_of_time': {
                'reason': 'قلة الوقت',
                'solutions': [
                    'استخدم تمارين HIIT لمدة 15-20 دقيقة فقط',
                    'مارس التمارين في المنزل لتوفير وقت الانتقال',
                    'قسم التمرين إلى جلسات قصيرة على مدار اليوم'
                ]
            },
            'boredom': {
                'reason': 'الملل من الروتين',
                'solutions': [
                    'غير التمارين كل أسبوعين',
                    'أضف موسيقى محفزة أو بودكاست',
                    'جرب أنواع تمارين جديدة (يوجا، رقص، سباحة)',
                    'مارس مع صديق أو مجموعة'
                ]
            },
            'no_results': {
                'reason': 'عدم ظهور نتائج',
                'solutions': [
                    'كن صبوراً، النتائج تحتاج 4-6 أسابيع للظهور',
                    'التقط صوراً لمتابعة التقدم بدلاً من الميزان فقط',
                    'راجع نظامك الغذائي - 70% من النتائج تأتي من الطعام',
                    'زد الأوزان تدريجياً كل أسبوع'
                ]
            },
            'injuries': {
                'reason': 'الخوف من الإصابات',
                'solutions': [
                    'ابدأ بتمارين بسيطة وتعلم التقنية الصحيحة',
                    'قم بالإحماء دائماً قبل التمرين',
                    'استشر مدرب مختص في البداية',
                    'استمع لجسمك وتوقف عند الشعور بألم'
                ]
            },
            'motivation': {
                'reason': 'ضعف الدافعية',
                'solutions': [
                    'ضع أهدافاً قصيرة المدى وكافئ نفسك عند تحقيقها',
                    'ابحث عن شريك تمرين للمساءلة المتبادلة',
                    'اتبع حسابات تحفيزية على وسائل التواصل',
                    'تذكر أسباب بدايتك في الرياضة'
                ]
            },
            'social_pressure': {
                'reason': 'الضغط الاجتماعي',
                'solutions': [
                    'اشرح لأصدقائك وعائلتك أهمية الرياضة لك',
                    'ابحث عن مجتمع رياضي داعم',
                    'مارس في أوقات تناسبك دون ضغط خارجي',
                    'ركز على صحتك وسعادتك الشخصية'
                ]
            },
            'financial': {
                'reason': 'القيود المالية',
                'solutions': [
                    'مارس تمارين وزن الجسم في المنزل مجاناً',
                    'استخدم تطبيقات مجانية للتمارين',
                    'ابحث عن عروض وخصومات في الصالات الرياضية',
                    'استثمر في معدات بسيطة ومتعددة الاستخدامات'
                ]
            }
        }
        
        quit_reasons = []
        
        # Add solutions for selected reasons
        for reason in selected_reasons:
            if reason in solutions_database:
                solution_data = solutions_database[reason]
                # Customize solutions based on user profile
                customized_solutions = self._customize_solutions(
                    solution_data['solutions'], goal, level, days_per_week
                )
                
                quit_reasons.append({
                    'reason': solution_data['reason'],
                    'solutions': customized_solutions
                })
        
        # Add default solutions if no specific reasons selected
        if not quit_reasons:
            quit_reasons = [
                {
                    'reason': 'التحديات العامة',
                    'solutions': [
                        'ضع خطة واقعية ومرنة',
                        'ابدأ بخطوات صغيرة وزد تدريجياً',
                        'احتفل بالإنجازات الصغيرة',
                        'تذكر أن التقدم ليس خطاً مستقيماً'
                    ]
                }
            ]
        
        return quit_reasons
    
    def _customize_solutions(self, base_solutions, goal, level, days_per_week):
        """Customize solutions based on user profile"""
        customized = base_solutions.copy()
        
        # Add goal-specific solutions
        if goal in ['fat_loss', 'weight_loss']:
            customized.append('ركز على تمارين الكارديو عالية الكثافة لحرق أكثر')
        elif goal in ['muscle_gain', 'muscle_building']:
            customized.append('اهتم بالتغذية والراحة بقدر اهتمامك بالتمرين')
        
        # Add level-specific solutions
        if level == 'beginner':
            customized.append('لا تقارن نفسك بالآخرين، كل شخص له رحلته الخاصة')
        
        # Add frequency-specific solutions
        if days_per_week <= 2:
            customized.append('حتى يومين أسبوعياً أفضل من لا شيء، الاستمرارية هي المفتاح')
        
        return customized[:4]  # Return top 4 solutions
    
    def _translate_goal(self, goal):
        """Translate goal to Arabic"""
        translations = {
            'fat_loss': 'حرق الدهون',
            'weight_loss': 'إنقاص الوزن',
            'muscle_gain': 'بناء العضلات',
            'muscle_building': 'بناء العضلات',
            'weight_gain': 'زيادة الوزن',
            'strength': 'زيادة القوة',
            'endurance': 'تحسين التحمل',
            'general_fitness': 'اللياقة العامة'
        }
        return translations.get(goal, 'اللياقة العامة')
    
    def _translate_level(self, level):
        """Translate level to Arabic"""
        translations = {
            'beginner': 'مبتدئ',
            'intermediate': 'متوسط',
            'advanced': 'متقدم'
        }
        return translations.get(level, 'متوسط')
    
    def _translate_equipment(self, equipment):
        """Translate equipment to Arabic"""
        translations = {
            'gym': 'صالة رياضية',
            'home': 'منزل',
            'bodyweight': 'وزن الجسم',
            'minimal': 'أدوات بسيطة'
        }
        return translations.get(equipment, 'صالة رياضية')
    
    def _translate_muscle(self, muscle):
        """Translate muscle group to Arabic"""
        translations = {
            'chest': 'الصدر',
            'back': 'الظهر',
            'legs': 'الأرجل',
            'shoulders': 'الأكتاف',
            'arms': 'الذراعين',
            'core': 'البطن',
            'cardio': 'الكارديو'
        }
        return translations.get(muscle, muscle)

# Example usage and testing
if __name__ == "__main__":
    # Sample user data
    sample_user_data = {
        'name': 'أحمد محمد',
        'age': 25,
        'gender': 'male',
        'weight': 75,
        'height': 175,
        'goal': 'muscle_gain',
        'level': 'intermediate',
        'days_per_week': 4,
        'equipment': 'gym',
        'health_issues': '',
        'selected_reasons': ['lack_of_time', 'boredom']
    }
    
    # Create generator instance
    generator = PersonalizedWorkoutGenerator()
    
    # Generate workout plan
    workout_plan = generator.generate_workout_plan(sample_user_data)
    
    # Print formatted JSON
    print(json.dumps(workout_plan, ensure_ascii=False, indent=2))