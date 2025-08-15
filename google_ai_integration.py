"""
نظام دمج Google AI (Gemini) لتوليد خطط اللياقة البدنية والتغذية المخصصة
"""

import os
import json
import requests
from typing import Dict, List, Optional

class GoogleAIFitnessGenerator:
    def __init__(self, api_key: str = None):
        """Initialize Google AI client with API key"""
        try:
            # استخدام متغير البيئة إذا لم يتم تمرير المفتاح
            self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
            
            if not self.api_key:
                print("⚠️ لم يتم تعيين مفتاح Google AI API")
                self.client = None
            else:
                # تهيئة Google AI
                self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
                self.headers = {
                    'Content-Type': 'application/json',
                }
                
                # اختبار الاتصال
                try:
                    test_response = self._make_request("test")
                    if test_response:
                        print("✅ تم تهيئة Google AI بنجاح!")
                        self.client = True
                    else:
                        print("❌ فشل في اختبار Google AI API")
                        self.client = None
                except Exception as test_error:
                    print(f"❌ فشل في اختبار Google AI API: {str(test_error)}")
                    self.client = None
            
        except Exception as e:
            print(f"❌ خطأ في تهيئة Google AI: {str(e)}")
            self.client = None
    
    def _make_request(self, prompt: str, max_tokens: int = 1500) -> Optional[str]:
        """إرسال طلب إلى Google AI API"""
        try:
            url = f"{self.base_url}?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 1,
                    "topP": 1,
                    "maxOutputTokens": max_tokens,
                    "stopSequences": []
                },
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    return result['candidates'][0]['content']['parts'][0]['text']
            else:
                print(f"Google AI API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"خطأ في طلب Google AI: {str(e)}")
            return None
    
    def generate_unified_plan(self, user_data: Dict) -> Optional[str]:
        """توليد خطة موحدة شاملة باستخدام Google AI"""
        try:
            if not self.client:
                print("⚠️ عميل Google AI غير متاح")
                return None
                
            prompt = self._create_unified_prompt(user_data)
            
            system_prompt = """أنت مدرب لياقة بدنية وخبير تغذية محترف متخصص في إنشاء خطط شاملة ومخصصة. 
            تقوم بإنشاء خطط متكاملة تشمل التغذية والتمارين واستراتيجيات التحفيز المخصصة لكل شخص.
            خبرتك تشمل معالجة أسباب عدم الاستمرارية وتقديم حلول عملية لكل حالة.
            تكتب بأسلوب ودود ومحفز باللغة العربية مع استخدام HTML بسيط للتنسيق.
            
            """ + prompt
            
            response = self._make_request(system_prompt, max_tokens=4000)
            
            if response:
                formatted_plan = self._format_unified_plan(response, user_data)
                print("✅ تم توليد الخطة باستخدام Google AI")
                return formatted_plan
            else:
                return None
                
        except Exception as e:
            print(f"خطأ في توليد الخطة باستخدام Google AI: {str(e)}")
            return None
    
    def _create_unified_prompt(self, user_data: Dict) -> str:
        """إنشاء prompt للخطة الموحدة المحسنة"""
        name = user_data.get('name', 'صديقي')
        age = user_data.get('age', 25)
        gender = 'ذكر' if user_data.get('gender') == 'male' else 'أنثى'
        weight = user_data.get('weight', 70)
        height = user_data.get('height', 170)
        goal = user_data.get('goal', 'تحسين اللياقة العامة')
        activity_level = user_data.get('activity_level', 'متوسط')
        health_conditions = user_data.get('health_conditions', [])
        dietary_preferences = user_data.get('dietary_preferences', [])
        available_time = user_data.get('available_time', '30-60 دقيقة')
        equipment = user_data.get('equipment', [])
        experience_level = user_data.get('experience_level', 'مبتدئ')
        motivation_level = user_data.get('motivation_level', 'متوسط')
        barriers = user_data.get('barriers', [])
        preferred_activities = user_data.get('preferred_activities', [])
        
        # حساب BMI
        height_m = height / 100
        bmi = round(weight / (height_m ** 2), 1)
        
        prompt = f"""
        أريد منك إنشاء خطة لياقة بدنية وتغذية شاملة ومخصصة للشخص التالي:

        📊 **المعلومات الشخصية:**
        - الاسم: {name}
        - العمر: {age} سنة
        - الجنس: {gender}
        - الوزن: {weight} كيلو
        - الطول: {height} سم
        - مؤشر كتلة الجسم (BMI): {bmi}

        🎯 **الأهداف والتفضيلات:**
        - الهدف الرئيسي: {goal}
        - مستوى النشاط الحالي: {activity_level}
        - مستوى الخبرة: {experience_level}
        - الوقت المتاح للتمرين: {available_time}
        - مستوى التحفيز: {motivation_level}

        🏋️ **المعدات المتاحة:**
        {', '.join(equipment) if equipment else 'لا توجد معدات خاصة'}

        🍽️ **التفضيلات الغذائية:**
        {', '.join(dietary_preferences) if dietary_preferences else 'لا توجد قيود غذائية'}

        🏃 **الأنشطة المفضلة:**
        {', '.join(preferred_activities) if preferred_activities else 'مفتوح لجميع الأنشطة'}

        ⚠️ **الحالات الصحية:**
        {', '.join(health_conditions) if health_conditions else 'لا توجد حالات صحية خاصة'}

        🚧 **العوائق والتحديات:**
        {', '.join(barriers) if barriers else 'لا توجد عوائق محددة'}

        أريد خطة شاملة تتضمن:

        1. **تحليل شخصي مفصل** مع تقييم الوضع الحالي
        2. **خطة تغذية أسبوعية** مع وجبات محددة وبدائل
        3. **برنامج تمارين مفصل** لمدة 4 أسابيع مع التدرج
        4. **استراتيجيات التحفيز** المخصصة لمستوى التحفيز
        5. **حلول للعوائق** المحددة مع خطط بديلة
        6. **نصائح للاستمرارية** وتكوين عادات صحية
        7. **مؤشرات التقدم** وكيفية قياس النجاح
        8. **خطة الطوارئ** للأيام الصعبة

        يرجى تنسيق الإجابة بـ HTML بسيط مع استخدام العناوين والقوائم والألوان لجعلها جذابة ومنظمة.
        """
        
        return prompt
    
    def _format_unified_plan(self, plan_text: str, user_data: Dict) -> str:
        """تنسيق الخطة الموحدة مع HTML"""
        name = user_data.get('name', 'صديقي')
        
        # إضافة تنسيق HTML أساسي إذا لم يكن موجوداً
        if '<h' not in plan_text and '<div' not in plan_text:
            # تحويل النص العادي إلى HTML منسق
            formatted_plan = f"""
            <div class="unified-plan-container">
                <div class="plan-header">
                    <h2 style="color: #2c5aa0; text-align: center;">🎯 خطة اللياقة الشاملة المخصصة لـ {name}</h2>
                    <p style="text-align: center; color: #666; font-style: italic;">تم إنشاؤها بواسطة Google AI</p>
                </div>
                
                <div class="plan-content">
                    {plan_text.replace('\n\n', '</p><p>').replace('\n', '<br>')}
                </div>
                
                <div class="plan-footer" style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <h4 style="color: #28a745;">💪 رسالة تحفيزية:</h4>
                    <p style="font-weight: bold; color: #495057;">
                        تذكر أن النجاح في اللياقة البدنية رحلة وليس وجهة. كل يوم تلتزم فيه بخطتك هو خطوة نحو النسخة الأفضل من نفسك!
                    </p>
                </div>
            </div>
            """
        else:
            # إضافة header و footer للخطة المنسقة مسبقاً
            formatted_plan = f"""
            <div class="unified-plan-container">
                <div class="plan-header">
                    <h2 style="color: #2c5aa0; text-align: center;">🎯 خطة اللياقة الشاملة المخصصة لـ {name}</h2>
                    <p style="text-align: center; color: #666; font-style: italic;">تم إنشاؤها بواسطة Google AI</p>
                </div>
                
                {plan_text}
                
                <div class="plan-footer" style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    <h4 style="color: #28a745;">💪 رسالة تحفيزية:</h4>
                    <p style="font-weight: bold; color: #495057;">
                        تذكر أن النجاح في اللياقة البدنية رحلة وليس وجهة. كل يوم تلتزم فيه بخطتك هو خطوة نحو النسخة الأفضل من نفسك!
                    </p>
                </div>
            </div>
            """
        
        return formatted_plan