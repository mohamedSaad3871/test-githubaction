# 🏋️ مولد خطط التمارين - Flask REST API

## 📋 نظرة عامة

تطبيق Flask REST API متكامل لتوليد خطط تمارين مخصصة للمستخدمين. يوفر التطبيق إمكانيات شاملة لإدارة المستخدمين والتمارين وتوليد خطط تمارين ذكية بناءً على أهداف المستخدم ومستوى لياقته.

## ✨ الميزات الرئيسية

- 🔐 **إدارة المستخدمين**: إضافة وإدارة بيانات المستخدمين مع التحقق من صحة البيانات
- 💪 **إدارة التمارين**: إضافة وتصنيف التمارين حسب المجموعة العضلية ومستوى الصعوبة
- 🎯 **توليد خطط ذكية**: إنشاء خطط تمارين مخصصة بناءً على:
  - الهدف (إنقاص الوزن، بناء العضلات، زيادة الوزن)
  - مستوى اللياقة (مبتدئ، متوسط، متقدم)
  - المعدات المتاحة
  - المشاكل الصحية
  - عدد أيام التمرين في الأسبوع
- 🛡️ **الحماية من التكرار**: منع تكرار التمارين في نفس اليوم
- 📊 **فلترة ذكية**: استبعاد التمارين الضارة بناءً على المشاكل الصحية
- 🎨 **استجابات JSON منظمة**: جميع الاستجابات في صيغة JSON مع رسائل خطأ واضحة

## 🗄️ هيكل قاعدة البيانات

### جدول المستخدمين (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    weight REAL NOT NULL,
    height REAL NOT NULL,
    goal TEXT NOT NULL CHECK (goal IN ('lose_weight', 'muscle_gain', 'weight_gain')),
    level TEXT NOT NULL CHECK (level IN ('beginner', 'intermediate', 'advanced')),
    days_per_week INTEGER NOT NULL,
    equipment TEXT NOT NULL,
    health_issues TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول التمارين (exercises)
```sql
CREATE TABLE exercises (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    muscle_group TEXT NOT NULL,
    difficulty TEXT NOT NULL CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
    equipment_needed TEXT NOT NULL,
    video_url TEXT NOT NULL,
    tips TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 التثبيت والتشغيل

### 1. متطلبات النظام
```bash
pip install flask requests
```

### 2. إنشاء قاعدة البيانات
```bash
python create_database.py
```

### 3. تشغيل الخادم
```bash
python workout_api.py
```

التطبيق سيعمل على: `http://localhost:5001`

### 4. اختبار API
```bash
python test_api.py
```

## 📡 نقاط النهاية (API Endpoints)

### 1. فحص حالة API
```http
GET /api/health
```

**الاستجابة:**
```json
{
    "status": "healthy",
    "message": "API يعمل بشكل طبيعي",
    "timestamp": "2024-01-01T12:00:00",
    "version": "1.0.0"
}
```

### 2. إضافة مستخدم جديد
```http
POST /api/users
Content-Type: application/json
```

**البيانات المطلوبة:**
```json
{
    "name": "أحمد محمد",
    "age": 25,
    "weight": 75.5,
    "height": 175.0,
    "goal": "muscle_gain",
    "level": "intermediate",
    "days_per_week": 4,
    "equipment": "دمبل، بار",
    "health_issues": ""
}
```

**الاستجابة الناجحة (201):**
```json
{
    "message": "تم إضافة المستخدم بنجاح",
    "user_id": 1,
    "status": "success"
}
```

**استجابة الخطأ (400):**
```json
{
    "error": "يرجى إكمال جميع البيانات الشخصية قبل المتابعة"
}
```

### 3. إضافة تمرين جديد
```http
POST /api/exercises
Content-Type: application/json
```

**البيانات المطلوبة:**
```json
{
    "name": "تمرين الضغط",
    "muscle_group": "صدر",
    "difficulty": "beginner",
    "equipment_needed": "وزن الجسم",
    "video_url": "https://youtube.com/watch?v=example",
    "tips": "حافظ على استقامة الجسم وتنفس بانتظام"
}
```

### 4. توليد خطة تمارين
```http
POST /api/generate-workout-plan
Content-Type: application/json
```

**البيانات المطلوبة:**
```json
{
    "name": "سارة أحمد",
    "age": 28,
    "weight": 65.0,
    "height": 165.0,
    "goal": "lose_weight",
    "level": "beginner",
    "days_per_week": 3,
    "equipment": "وزن الجسم",
    "health_issues": ""
}
```

**الاستجابة:**
```json
{
    "goal": "إنقاص الوزن وحرق الدهون",
    "plan": [
        {
            "day": 1,
            "exercises": [
                {
                    "name": "تمرين الضغط",
                    "target_muscle": "صدر",
                    "sets": 3,
                    "reps": "12-15",
                    "video": "https://youtube.com/watch?v=example",
                    "tips": "حافظ على استقامة الجسم"
                }
            ]
        }
    ],
    "general_tips": [
        "اشرب الماء بكثرة قبل وأثناء وبعد التمرين",
        "ركز على التمارين الهوائية مع تمارين المقاومة"
    ],
    "reasons_for_quitting": [
        {
            "reason": "عدم وجود وقت كافي",
            "solution": "ابدأ بتمارين قصيرة 15-20 دقيقة"
        }
    ],
    "user_info": {
        "name": "سارة أحمد",
        "level": "beginner",
        "days_per_week": 3,
        "equipment": "وزن الجسم"
    },
    "generated_at": "2024-01-01T12:00:00",
    "status": "success"
}
```

### 5. جلب جميع التمارين
```http
GET /api/exercises
```

**مع فلترة (اختياري):**
```http
GET /api/exercises?muscle_group=صدر&difficulty=beginner&equipment=دمبل
```

### 6. جلب جميع المستخدمين
```http
GET /api/users
```

## 🧪 أمثلة CURL

### إضافة مستخدم جديد
```bash
curl -X POST http://localhost:5001/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "أحمد محمد",
    "age": 25,
    "weight": 75.5,
    "height": 175.0,
    "goal": "muscle_gain",
    "level": "intermediate",
    "days_per_week": 4,
    "equipment": "دمبل، بار",
    "health_issues": ""
  }'
```

### إضافة تمرين جديد
```bash
curl -X POST http://localhost:5001/api/exercises \
  -H "Content-Type: application/json" \
  -d '{
    "name": "تمرين الضغط",
    "muscle_group": "صدر", 
    "difficulty": "beginner",
    "equipment_needed": "وزن الجسم",
    "video_url": "https://youtube.com/watch?v=example",
    "tips": "حافظ على استقامة الجسم وتنفس بانتظام"
  }'
```

### توليد خطة تمارين
```bash
curl -X POST http://localhost:5001/api/generate-workout-plan \
  -H "Content-Type: application/json" \
  -d '{
    "name": "سارة أحمد",
    "age": 28,
    "weight": 65.0,
    "height": 165.0,
    "goal": "lose_weight", 
    "level": "beginner",
    "days_per_week": 3,
    "equipment": "وزن الجسم",
    "health_issues": ""
  }'
```

### جلب التمارين مع فلترة
```bash
curl -X GET "http://localhost:5001/api/exercises?muscle_group=صدر&difficulty=beginner"
```

## أمثلة Postman

- Base URL: `http://localhost:5001/api`

### 1. إعداد Collection جديد
- اسم Collection: "Workout Plan Generator API"
- Base URL: `http://localhost:5000/api`

### 2. إضافة Requests

#### فحص حالة API
- Method: `GET`
- URL: `{{base_url}}/health`

#### إضافة مستخدم
- Method: `POST`
- URL: `{{base_url}}/users`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "name": "محمد علي",
  "age": 30,
  "weight": 80.0,
  "height": 180.0,
  "goal": "lose_weight",
  "level": "intermediate",
  "days_per_week": 5,
  "equipment": "أجهزة الجيم",
  "health_issues": "ألم في الركبة"
}
```

#### توليد خطة تمارين
- Method: `POST`
- URL: `{{base_url}}/generate-workout-plan`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
  "name": "فاطمة محمود",
  "age": 22,
  "weight": 55.0,
  "height": 160.0,
  "goal": "muscle_gain",
  "level": "beginner",
  "days_per_week": 4,
  "equipment": "دمبل",
  "health_issues": ""
}
```

## 🔧 التخصيص والتطوير

### إضافة تمارين جديدة
يمكنك إضافة تمارين جديدة عبر API أو مباشرة في قاعدة البيانات:

```python
# إضافة تمرين مخصص
exercise_data = {
    "name": "تمرين مخصص",
    "muscle_group": "ظهر",
    "difficulty": "intermediate",
    "equipment_needed": "بار",
    "video_url": "https://youtube.com/custom",
    "tips": "نصائح مخصصة للتمرين"
}
```

### تخصيص خوارزمية التوزيع
يمكنك تعديل دالة `distribute_exercises_across_days()` لتخصيص كيفية توزيع التمارين:

```python
def distribute_exercises_across_days(exercises, days_per_week, goal):
    # منطق التوزيع المخصص
    pass
```

### إضافة فلاتر جديدة للمشاكل الصحية
```python
def filter_exercises_by_health_issues(exercises, health_issues):
    # إضافة فلاتر جديدة
    if 'مفصل' in health_issues_lower:
        # استبعاد تمارين معينة
        pass
```

## 🛡️ الأمان والتحقق

### التحقق من البيانات
- جميع الحقول المطلوبة يتم التحقق منها
- التحقق من نطاقات القيم (العمر، الوزن، الطول)
- التحقق من القيم المسموحة للأهداف والمستويات

### معالجة الأخطاء
- جميع الأخطاء ترجع في صيغة JSON
- رسائل خطأ واضحة باللغة العربية
- أكواد HTTP مناسبة

## 📊 الإحصائيات والمراقبة

### معلومات قاعدة البيانات
```bash
python -c "
import sqlite3
conn = sqlite3.connect('workout_generator.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM users')
print(f'المستخدمين: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM exercises')
print(f'التمارين: {cursor.fetchone()[0]}')
conn.close()
"
```

## 🔄 التحديثات المستقبلية

- [ ] إضافة نظام المصادقة والتفويض
- [ ] تتبع تقدم المستخدمين
- [ ] إحصائيات مفصلة للتمارين
- [ ] دعم الصور للتمارين
- [ ] API للتغذية الراجعة من المستخدمين
- [ ] تكامل مع أجهزة اللياقة البدنية

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:
1. Fork المشروع
2. إنشاء branch جديد للميزة
3. Commit التغييرات
4. Push إلى Branch
5. إنشاء Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف LICENSE للتفاصيل.

## 📞 الدعم

للدعم والاستفسارات:
- إنشاء Issue في GitHub
- التواصل عبر البريد الإلكتروني

---

**تم تطويره بواسطة:** مبرمج Python محترف  
**التاريخ:** 2024  
**الإصدار:** 1.0.0