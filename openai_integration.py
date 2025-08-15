"""
نظام دمج OpenAI API لتوليد خطط اللياقة البدنية والتغذية المخصصة
"""

import openai
import json
import random
import os
from typing import Dict, List, Optional

# استيراد Google AI integration
try:
    from google_ai_integration import GoogleAIFitnessGenerator
    GOOGLE_AI_AVAILABLE = True
    print("✅ Google AI متاح كخيار احتياطي")
except ImportError:
    GOOGLE_AI_AVAILABLE = False
    print("⚠️ Google AI غير متاح")

class OpenAIFitnessGenerator:
    def __init__(self, api_key: str = None):
        """Initialize OpenAI client with API key"""
        try:
            # استخدام متغير البيئة إذا لم يتم تمرير المفتاح
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            
            # تهيئة OpenAI
            if not self.api_key or self.api_key == 'your-openai-api-key-here':
                print("⚠️ لم يتم تعيين مفتاح OpenAI API")
                self.client = None
            else:
                # تهيئة عميل OpenAI
                self.client = openai.OpenAI(api_key=self.api_key)
                self.model = "gpt-3.5-turbo"
                
                # اختبار الاتصال
                try:
                    test_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": "test"}],
                        max_tokens=1
                    )
                    print("✅ تم تهيئة OpenAI بنجاح!")
                except Exception as test_error:
                    print(f"❌ فشل في اختبار OpenAI API: {str(test_error)}")
                    self.client = None
            
            # تهيئة Google AI كخيار احتياطي
            self.google_ai = None
            if GOOGLE_AI_AVAILABLE:
                try:
                    self.google_ai = GoogleAIFitnessGenerator()
                except Exception as google_error:
                    print(f"⚠️ فشل في تهيئة Google AI: {str(google_error)}")
                    self.google_ai = None
            
        except Exception as e:
            print(f"❌ خطأ في تهيئة النظام: {str(e)}")
            self.client = None
            self.google_ai = None
        
    def generate_nutrition_plan(self, user_data: Dict) -> Dict:
        """توليد خطة تغذية مخصصة باستخدام OpenAI"""
        try:
            # فحص وجود العميل
            if not self.client:
                print("⚠️ عميل OpenAI غير متاح، استخدام الخطة الاحتياطية")
                return self._get_fallback_nutrition_plan(user_data)
                
            # إعداد البيانات للـ prompt
            prompt = self._create_nutrition_prompt(user_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "أنت خبير تغذية رياضية متخصص في إنشاء خطط تغذية مخصصة للرياضيين والأشخاص الذين يريدون تحسين لياقتهم البدنية. تجيب باللغة العربية وتقدم نصائح علمية دقيقة."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=1500,
                temperature=0.7
            )
            
            # استخراج النص من الاستجابة
            nutrition_text = response.choices[0].message.content
            
            # تحويل النص إلى خطة منظمة
            nutrition_plan = self._parse_nutrition_response(nutrition_text, user_data)
            
            return nutrition_plan
            
        except Exception as e:
            print(f"خطأ في توليد خطة التغذية: {str(e)}")
            return self._get_fallback_nutrition_plan(user_data)
    
    def generate_workout_plan(self, user_data: Dict) -> List[Dict]:
        """توليد خطة تمارين مخصصة باستخدام OpenAI"""
        try:
            # فحص وجود العميل
            if not self.client:
                print("⚠️ عميل OpenAI غير متاح، استخدام الخطة الاحتياطية")
                return self._get_fallback_workout_plan(user_data)
                
            prompt = self._create_workout_prompt(user_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "أنت مدرب لياقة بدنية محترف متخصص في إنشاء برامج تمارين مخصصة. تقدم خطط تمارين علمية ومناسبة لمستوى المتدرب وأهدافه. تجيب باللغة العربية."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            workout_text = response.choices[0].message.content
            workout_plan = self._parse_workout_response(workout_text, user_data)
            
            return workout_plan
            
        except Exception as e:
            print(f"خطأ في توليد خطة التمارين: {str(e)}")
            return self._get_fallback_workout_plan(user_data)
    
    def generate_personalized_tips(self, user_data: Dict) -> List[str]:
        """توليد نصائح مخصصة باستخدام OpenAI"""
        try:
            # فحص وجود العميل
            if not self.client:
                print("⚠️ عميل OpenAI غير متاح، استخدام النصائح الاحتياطية")
                return self._get_fallback_tips(user_data)
                
            prompt = self._create_tips_prompt(user_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "أنت مستشار صحة ولياقة بدنية. تقدم نصائح عملية ومفيدة للأشخاص الذين يريدون تحسين صحتهم ولياقتهم. نصائحك بسيطة وقابلة للتطبيق."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.8
            )
            
            tips_text = response.choices[0].message.content
            tips = self._parse_tips_response(tips_text)
            
            return tips
            
        except Exception as e:
            print(f"خطأ في توليد النصائح: {str(e)}")
            return self._get_fallback_tips(user_data)
    
    def generate_unified_plan(self, user_data: Dict) -> str:
        """توليد خطة موحدة شاملة مع معالجة أسباب عدم الاستمرارية"""
        try:
            # محاولة استخدام OpenAI أولاً
            if self.client:
                try:
                    prompt = self._create_unified_prompt(user_data)
                    
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "system",
                                "content": """أنت مدرب لياقة بدنية وخبير تغذية محترف متخصص في إنشاء خطط شاملة ومخصصة. 
                                تقوم بإنشاء خطط متكاملة تشمل التغذية والتمارين واستراتيجيات التحفيز المخصصة لكل شخص.
                                خبرتك تشمل معالجة أسباب عدم الاستمرارية وتقديم حلول عملية لكل حالة.
                                تكتب بأسلوب ودود ومحفز باللغة العربية مع استخدام HTML بسيط للتنسيق."""
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        max_tokens=4000,
                        temperature=0.7
                    )
                    
                    unified_plan = response.choices[0].message.content
                    formatted_plan = self._format_unified_plan(unified_plan, user_data)
                    print("✅ تم توليد الخطة باستخدام OpenAI")
                    return formatted_plan
                    
                except Exception as openai_error:
                    print(f"❌ فشل OpenAI: {str(openai_error)}")
            
            # محاولة استخدام Google AI كخيار احتياطي
            if self.google_ai and self.google_ai.client:
                try:
                    google_plan = self.google_ai.generate_unified_plan(user_data)
                    if google_plan:
                        print("✅ تم توليد الخطة باستخدام Google AI")
                        return google_plan
                except Exception as google_error:
                    print(f"❌ فشل Google AI: {str(google_error)}")
            
            # استخدام الخطة الاحتياطية المحلية
            print("⚠️ استخدام الخطة الاحتياطية المحلية")
            return self._get_fallback_comprehensive_plan(user_data)
            
        except Exception as e:
            print(f"خطأ في توليد الخطة الموحدة: {str(e)}")
            return self._get_fallback_comprehensive_plan(user_data)
    
    def _create_unified_prompt(self, user_data: Dict) -> str:
        """إنشاء prompt للخطة الموحدة المحسنة"""
        name = user_data.get('name', 'صديقي')
        age = user_data.get('age', 25)
        gender = 'ذكر' if user_data.get('gender') == 'male' else 'أنثى'
        weight = user_data.get('weight', 70)
        height = user_data.get('height', 170)
        target_weight = user_data.get('target_weight', weight)
        goal = user_data.get('goal', 'weight_loss')
        activity_level = user_data.get('activity_level', 'moderate')
        workout_days = user_data.get('workout_days', 3)
        workout_duration = user_data.get('workout_duration', 60)
        equipment = user_data.get('equipment', 'gym')
        experience_level = user_data.get('experience_level', 'beginner')
        health_conditions = user_data.get('health_conditions', '')
        dietary_restrictions = user_data.get('dietary_restrictions', '')
        
        # ترجمة القيم للعربية
        goal_arabic = {
            'weight_loss': 'فقدان الوزن',
            'muscle_gain': 'بناء العضلات',
            'body_recomp': 'تحسين تركيب الجسم',
            'maintenance': 'المحافظة على الوزن',
            'general_fitness': 'تحسين اللياقة العامة'
        }.get(goal, 'تحسين الصحة العامة')
        
        activity_arabic = {
            'sedentary': 'قليل الحركة',
            'light': 'نشاط خفيف',
            'moderate': 'نشاط متوسط',
            'active': 'نشيط',
            'very_active': 'نشيط جداً'
        }.get(activity_level, 'نشاط متوسط')
        
        equipment_arabic = {
            'bodyweight': 'وزن الجسم فقط',
            'dumbbells': 'دمبلز',
            'gym': 'جيم كامل',
            'home_gym': 'جيم منزلي',
            'resistance_bands': 'أحبال مقاومة'
        }.get(equipment, 'جيم كامل')
        
        experience_arabic = {
            'beginner': 'مبتدئ',
            'intermediate': 'متوسط',
            'advanced': 'متقدم'
        }.get(experience_level, 'مبتدئ')
        
        # تحديد أسباب عدم الاستمرارية الشائعة
        continuity_issues = {
            'lack_of_time': 'قلة الوقت',
            'low_motivation': 'ضعف الدافعية',
            'injuries': 'الإصابات',
            'lack_of_results': 'عدم رؤية نتائج',
            'boredom': 'الملل من الروتين',
            'social_pressure': 'الضغوط الاجتماعية',
            'financial_constraints': 'القيود المالية',
            'lack_of_knowledge': 'نقص المعرفة'
        }
        
        return f"""
        أنت مدرب لياقة بدنية وخبير تغذية محترف. مهمتك إنشاء خطة شاملة ومخصصة بالكامل للشخص التالي:

        ### بيانات المستخدم:
        - الاسم: {name}
        - العمر: {age} سنة
        - الجنس: {gender}
        - الوزن الحالي: {weight} كجم
        - الطول: {height} سم
        - الوزن المستهدف: {target_weight} كجم
        - الهدف الرئيسي: {goal_arabic}
        - مستوى النشاط: {activity_arabic}
        - أيام التمرين المتاحة: {workout_days} أيام أسبوعياً
        - مدة التمرين المتاحة: {workout_duration} دقيقة
        - المعدات المتاحة: {equipment_arabic}
        - مستوى الخبرة: {experience_arabic}
        - الحالات الصحية: {health_conditions if health_conditions else 'لا توجد'}
        - القيود الغذائية: {dietary_restrictions if dietary_restrictions else 'لا توجد'}

        ### مطلوب منك إنشاء خطة تتضمن:

        1. **📊 تحليل الوضع الحالي والأهداف**
           - تقييم الوضع الحالي
           - الأهداف قصيرة وطويلة المدى
           - التوقعات الزمنية الواقعية

        2. **🏋️ برنامج التمارين الأسبوعي المفصل**
           - جدول أسبوعي كامل ({workout_days} أيام تمرين)
           - تمارين محددة مع المجموعات والتكرارات
           - بدائل للتمارين حسب المعدات المتاحة
           - تدرج في الصعوبة حسب مستوى الخبرة

        3. **🍎 خطة التغذية اليومية الشاملة**
           - إجمالي السعرات الحرارية المطلوبة
           - توزيع الماكروز (بروتين، كربوهيدرات، دهون) بالجرام
           - جدول وجبات يومي مفصل (فطار، غداء، عشاء، وجبات خفيفة)
           - كمية الماء المطلوبة
           - مراعاة القيود الغذائية المذكورة

        4. **💡 استراتيجيات التحفيز والاستمرارية**
           - تحديد أسباب عدم الاستمرارية المحتملة
           - حلول عملية لكل سبب (مثل: إذا كان السبب قلة الوقت، اقترح تمارين HIIT قصيرة)
           - تقنيات بناء العادات
           - نظام مكافآت شخصي

        5. **📈 نصائح للمتابعة والتقييم**
           - كيفية قياس التقدم
           - علامات النجاح المبكرة
           - متى وكيف يتم تعديل الخطة

        6. **🎯 رسالة تحفيزية شخصية**
           - رسالة مخصصة لـ {name}
           - تذكير بالهدف وأهميته
           - كلمات تشجيعية

        ### متطلبات التنسيق:
        - استخدم HTML بسيط للتنسيق (h3, div, strong, ul, li)
        - أضف رموز تعبيرية مناسبة
        - اجعل المحتوى منظم وسهل القراءة
        - استخدم اللغة العربية الواضحة والودودة
        - اجعل الخطة عملية وقابلة للتطبيق

        ### مهم جداً:
        - اجعل كل شيء مخصص لـ {name} وهدفه في {goal_arabic}
        - راعي مستوى الخبرة ({experience_arabic}) في اختيار التمارين
        - راعي المعدات المتاحة ({equipment_arabic})
        - راعي الوقت المتاح ({workout_duration} دقيقة)
        - قدم حلول عملية لأسباب عدم الاستمرارية الشائعة

        ابدأ بترحيب شخصي واجعل الخطة محفزة ومشجعة!
        """
    
    def _format_unified_plan(self, plan_text: str, user_data: Dict) -> str:
        """تنسيق الخطة الموحدة مع CSS classes محسنة"""
        name = user_data.get('name', 'صديقي')
        
        formatted_plan = f"""
        <div class="unified-plan-container ai-generated">
            <div class="plan-header">
                <h2 class="plan-title">🤖 خطتك الذكية الشاملة</h2>
                <p class="plan-subtitle">خطة مخصصة لـ {name} • مولدة بالذكاء الاصطناعي</p>
            </div>
            <div class="unified-plan-content">
                {plan_text}
            </div>
            <div class="plan-footer">
                <p class="ai-disclaimer">
                    <strong>ملاحظة:</strong> هذه الخطة مولدة بالذكاء الاصطناعي وتحتاج لمراجعة طبية قبل البدء، خاصة إذا كان لديك حالات صحية خاصة.
                </p>
            </div>
        </div>
        """
        
        return formatted_plan

    def generate_comprehensive_plan(self, user_data: Dict) -> str:
        """توليد خطة شاملة مخصصة باستخدام OpenAI"""
        try:
            # فحص وجود العميل
            if not self.client:
                print("⚠️ عميل OpenAI غير متاح، استخدام الخطة الاحتياطية")
                return self._get_fallback_comprehensive_plan(user_data)
                
            prompt = self._create_comprehensive_prompt(user_data)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """أنت خبير لياقة بدنية وتغذية شامل. تقوم بإنشاء خطط متكاملة تشمل التغذية والتمارين والنصائح العملية. 
                        خططك مخصصة لكل شخص حسب بياناته وأهدافه. تكتب بأسلوب ودود ومحفز باللغة العربية.
                        استخدم HTML بسيط لتنسيق الخطة مع استخدام الألوان والرموز التعبيرية."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=3000,
                temperature=0.7
            )
            
            comprehensive_plan = response.choices[0].message.content
            
            # تنسيق الخطة وإضافة CSS classes
            formatted_plan = self._format_comprehensive_plan(comprehensive_plan, user_data)
            
            return formatted_plan
            
        except Exception as e:
            print(f"خطأ في توليد الخطة الشاملة: {str(e)}")
            return self._get_fallback_comprehensive_plan(user_data)
    
    def _create_nutrition_prompt(self, user_data: Dict) -> str:
        """إنشاء prompt لخطة التغذية"""
        name = user_data.get('name', 'صديقي')
        age = user_data.get('age', 25)
        gender = 'ذكر' if user_data.get('gender') == 'male' else 'أنثى'
        weight = user_data.get('weight', 70)
        height = user_data.get('height', 170)
        goal = user_data.get('goal', 'weight_loss')
        activity_level = user_data.get('activity_level', 'moderate')
        
        goal_arabic = {
            'weight_loss': 'فقدان الوزن',
            'muscle_gain': 'بناء العضلات', 
            'body_recomp': 'تحسين تركيب الجسم',
            'maintenance': 'المحافظة على الوزن',
            'general_fitness': 'تحسين اللياقة العامة'
        }.get(goal, 'تحسين الصحة العامة')
        
        activity_arabic = {
            'sedentary': 'قليل الحركة',
            'light': 'نشاط خفيف',
            'moderate': 'نشاط متوسط',
            'active': 'نشيط',
            'very_active': 'نشيط جداً'
        }.get(activity_level, 'نشاط متوسط')
        
        return f"""
        أريد خطة تغذية مخصصة للشخص التالي:
        
        الاسم: {name}
        العمر: {age} سنة
        الجنس: {gender}
        الوزن الحالي: {weight} كجم
        الطول: {height} سم
        الهدف: {goal_arabic}
        مستوى النشاط: {activity_arabic}
        
        أريد منك:
        1. حساب السعرات الحرارية اليومية المطلوبة
        2. توزيع الماكروز (بروتين، كربوهيدرات، دهون) بالجرام
        3. اقتراح 4-5 وجبات يومية مع أسماء الأطعمة
        4. كمية الماء المطلوبة يومياً
        5. نصائح تغذوية مهمة خاصة بالهدف
        
        اكتب الإجابة بشكل منظم وواضح باللغة العربية.
        """
    
    def _create_workout_prompt(self, user_data: Dict) -> str:
        """إنشاء prompt لخطة التمارين"""
        name = user_data.get('name', 'صديقي')
        age = user_data.get('age', 25)
        goal = user_data.get('goal', 'weight_loss')
        activity_level = user_data.get('activity_level', 'moderate')
        
        goal_arabic = {
            'weight_loss': 'فقدان الوزن',
            'muscle_gain': 'بناء العضلات',
            'body_recomp': 'تحسين تركيب الجسم', 
            'maintenance': 'المحافظة على الوزن',
            'general_fitness': 'تحسين اللياقة العامة'
        }.get(goal, 'تحسين الصحة العامة')
        
        return f"""
        أريد برنامج تمارين أسبوعي مخصص للشخص التالي:
        
        الاسم: {name}
        العمر: {age} سنة
        الهدف: {goal_arabic}
        مستوى اللياقة: {activity_level}
        
        أريد منك:
        1. برنامج تمارين لـ 7 أيام (مع تحديد أيام الراحة)
        2. لكل يوم تمرين: اذكر 4-6 تمارين مع عدد المجموعات والتكرارات
        3. نوع التمرين (قوة، كارديو، مرونة)
        4. المدة المتوقعة لكل جلسة تمرين
        5. نصائح مهمة للتمرين الآمن
        
        ركز على التمارين التي يمكن أداؤها في الجيم أو المنزل.
        اكتب الإجابة بشكل منظم باللغة العربية.
        """
    
    def _create_tips_prompt(self, user_data: Dict) -> str:
        """إنشاء prompt للنصائح المخصصة"""
        goal = user_data.get('goal', 'weight_loss')
        age = user_data.get('age', 25)
        
        goal_arabic = {
            'weight_loss': 'فقدان الوزن',
            'muscle_gain': 'بناء العضلات',
            'body_recomp': 'تحسين تركيب الجسم',
            'maintenance': 'المحافظة على الوزن', 
            'general_fitness': 'تحسين اللياقة العامة'
        }.get(goal, 'تحسين الصحة العامة')
        
        return f"""
        أريد 8-10 نصائح عملية ومفيدة لشخص عمره {age} سنة وهدفه {goal_arabic}.
        
        النصائح يجب أن تكون:
        - عملية وقابلة للتطبيق في الحياة اليومية
        - مناسبة للهدف المحدد
        - بسيطة وواضحة
        - تشمل جوانب التغذية والتمارين ونمط الحياة
        
        اكتب كل نصيحة في جملة واحدة أو جملتين قصيرتين.
        استخدم اللغة العربية البسيطة والودودة.
        """
    
    def _create_comprehensive_prompt(self, user_data: Dict) -> str:
        """إنشاء prompt للخطة الشاملة"""
        name = user_data.get('name', 'صديقي')
        age = user_data.get('age', 25)
        gender = 'ذكر' if user_data.get('gender') == 'male' else 'أنثى'
        weight = user_data.get('weight', 70)
        height = user_data.get('height', 170)
        target_weight = user_data.get('target_weight', 65)
        goal = user_data.get('goal', 'weight_loss')
        activity_level = user_data.get('activity_level', 'moderate')
        
        goal_arabic = {
            'weight_loss': 'فقدان الوزن',
            'muscle_gain': 'بناء العضلات',
            'body_recomp': 'تحسين تركيب الجسم',
            'maintenance': 'المحافظة على الوزن',
            'general_fitness': 'تحسين اللياقة العامة'
        }.get(goal, 'تحسين الصحة العامة')
        
        return f"""
        أريد خطة شاملة ومتكاملة للشخص التالي:
        
        الاسم: {name}
        العمر: {age} سنة
        الجنس: {gender}
        الوزن الحالي: {weight} كجم
        الطول: {height} سم
        الوزن المستهدف: {target_weight} كجم
        الهدف: {goal_arabic}
        مستوى النشاط: {activity_level}
        
        أريد خطة تشمل:
        
        1. **ملخص الهدف والتوقعات الزمنية**
        2. **خطة التغذية اليومية** (سعرات، ماكروز، وجبات مقترحة)
        3. **برنامج التمارين الأسبوعي** (3-4 أيام مع التفاصيل)
        4. **نصائح ذهبية** (5-6 نصائح مهمة)
        5. **رسالة تحفيزية شخصية**
        
        استخدم:
        - أسلوب ودود ومحفز
        - رموز تعبيرية مناسبة
        - تنسيق HTML بسيط (h3, div, strong, etc.)
        - اللغة العربية الواضحة
        - معلومات علمية دقيقة
        
        اجعل الخطة شخصية ومخصصة لـ {name} وهدفه في {goal_arabic}.
        """
    
    def _parse_nutrition_response(self, response_text: str, user_data: Dict) -> Dict:
        """تحليل استجابة خطة التغذية وتحويلها لقاموس منظم"""
        # استخراج الأرقام من النص باستخدام regex أو parsing بسيط
        import re
        
        # البحث عن السعرات الحرارية
        calories_match = re.search(r'(\d+)\s*سعرة|(\d+)\s*كالوري', response_text)
        calories = int(calories_match.group(1) or calories_match.group(2)) if calories_match else 2000
        
        # البحث عن البروتين
        protein_match = re.search(r'(\d+)\s*جرام.*بروتين|بروتين.*(\d+)\s*جرام', response_text)
        protein = int(protein_match.group(1) or protein_match.group(2)) if protein_match else 120
        
        # البحث عن الكربوهيدرات
        carbs_match = re.search(r'(\d+)\s*جرام.*كربوهيدرات|كربوهيدرات.*(\d+)\s*جرام', response_text)
        carbs = int(carbs_match.group(1) or carbs_match.group(2)) if carbs_match else 200
        
        # البحث عن الدهون
        fats_match = re.search(r'(\d+)\s*جرام.*دهون|دهون.*(\d+)\s*جرام', response_text)
        fats = int(fats_match.group(1) or fats_match.group(2)) if fats_match else 60
        
        return {
            'daily_calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fats': fats,
            'water_intake': 3,
            'ai_generated': True,
            'full_response': response_text
        }
    
    def _parse_workout_response(self, response_text: str, user_data: Dict) -> List[Dict]:
        """تحليل استجابة خطة التمارين وتحويلها لقائمة منظمة"""
        # تحليل بسيط للنص وإنشاء خطة تمارين
        days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
        workout_plan = []
        
        for i, day in enumerate(days):
            if 'راحة' in response_text and i in [2, 5]:  # أيام راحة افتراضية
                workout_plan.append({
                    'day': day,
                    'is_rest_day': True,
                    'exercises': [],
                    'total_calories': 0
                })
            else:
                workout_plan.append({
                    'day': day,
                    'is_rest_day': False,
                    'exercises': [
                        {'name': 'تمرين مخصص', 'sets': 3, 'reps': 12, 'calories_burned': 50}
                    ],
                    'total_calories': 150,
                    'ai_generated': True
                })
        
        return workout_plan
    
    def _parse_tips_response(self, response_text: str) -> List[str]:
        """تحليل استجابة النصائح وتحويلها لقائمة"""
        # تقسيم النص إلى نصائح منفصلة
        lines = response_text.split('\n')
        tips = []
        
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('*') or len(line) > 20):
                # تنظيف النص
                clean_tip = line.lstrip('-•*').strip()
                if clean_tip:
                    tips.append(clean_tip)
        
        return tips[:8]  # أقصى 8 نصائح
    
    def _format_comprehensive_plan(self, plan_text: str, user_data: Dict) -> str:
        """تنسيق الخطة الشاملة مع CSS classes"""
        # إضافة container وتنسيق أساسي
        formatted_plan = f"""
        <div class="personalized-plan-container ai-generated">
            <div class="plan-header">
                <h2 class="plan-title">🤖 خطتك الذكية المخصصة</h2>
                <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">مولدة بواسطة الذكاء الاصطناعي</p>
            </div>
            <div class="ai-plan-content">
                {plan_text}
            </div>
        </div>
        """
        
        return formatted_plan
    
    def _get_fallback_nutrition_plan(self, user_data: Dict) -> Dict:
        """خطة تغذية احتياطية في حالة فشل API"""
        weight = float(user_data.get('weight', 70))
        goal = user_data.get('goal', 'weight_loss')
        
        if goal == 'weight_loss':
            calories = int(weight * 22)
        elif goal == 'muscle_gain':
            calories = int(weight * 28)
        else:
            calories = int(weight * 25)
        
        return {
            'daily_calories': calories,
            'protein': int(weight * 1.6),
            'carbs': int(calories * 0.45 / 4),
            'fats': int(calories * 0.25 / 9),
            'water_intake': 3,
            'ai_generated': False
        }
    
    def _get_fallback_workout_plan(self, user_data: Dict) -> List[Dict]:
        """خطة تمارين احتياطية في حالة فشل API"""
        days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
        workout_plan = []
        
        for i, day in enumerate(days):
            if i in [2, 5]:  # أيام راحة
                workout_plan.append({
                    'day': day,
                    'is_rest_day': True,
                    'exercises': [],
                    'total_calories': 0
                })
            else:
                workout_plan.append({
                    'day': day,
                    'is_rest_day': False,
                    'exercises': [
                        {'name': 'تمرين عام', 'sets': 3, 'reps': 12, 'calories_burned': 50}
                    ],
                    'total_calories': 150
                })
        
        return workout_plan
    
    def _get_fallback_tips(self, user_data: Dict) -> List[str]:
        """نصائح احتياطية في حالة فشل API"""
        return [
            "اشرب الماء بكثرة يومياً",
            "تناول البروتين في كل وجبة",
            "نم 7-8 ساعات يومياً",
            "تمرن بانتظام 3-4 مرات أسبوعياً",
            "تناول الخضروات والفواكه",
            "تجنب السكريات المضافة"
        ]
    
    def _get_fallback_comprehensive_plan(self, user_data: Dict) -> str:
        """خطة شاملة احتياطية في حالة فشل API"""
        name = user_data.get('name', 'صديقي')
        return f"""
        <div class="personalized-plan-container">
            <div class="plan-header">
                <h2 class="plan-title">📋 خطتك الأساسية</h2>
                <p>مرحباً {name}! هذه خطة أساسية لك</p>
            </div>
            <div class="plan-section">
                <p>عذراً، لم نتمكن من الاتصال بخدمة الذكاء الاصطناعي. يرجى المحاولة مرة أخرى لاحقاً.</p>
            </div>
        </div>
        """