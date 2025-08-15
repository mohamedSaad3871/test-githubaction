"""
Flask API لمولد خطط التمارين
مطور بواسطة: مبرمج Python محترف
التاريخ: 2024

هذا التطبيق يوفر REST API كامل لإدارة المستخدمين والتمارين وتوليد خطط التمارين المخصصة
"""

from flask import Flask, request, jsonify
import sqlite3
import random
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'workout-generator-secret-key-2024'
app.config['DATABASE'] = 'workout_generator.db'

# إعداد قاعدة البيانات
def init_database():
    """إنشاء قاعدة البيانات والجداول المطلوبة"""
    conn = sqlite3.connect(app.config['DATABASE'])
    cursor = conn.cursor()
    
    # جدول المستخدمين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
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
        )
    ''')
    
    # جدول التمارين
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            difficulty TEXT NOT NULL CHECK (difficulty IN ('beginner', 'intermediate', 'advanced')),
            equipment_needed TEXT NOT NULL,
            video_url TEXT NOT NULL,
            tips TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ تم إنشاء قاعدة البيانات بنجاح")

def get_db_connection():
    """الحصول على اتصال بقاعدة البيانات"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def validate_user_data(data):
    """التحقق من صحة بيانات المستخدم"""
    required_fields = ['name', 'age', 'weight', 'height', 'goal', 'level', 'days_per_week', 'equipment']
    
    # التحقق من وجود جميع الحقول المطلوبة
    for field in required_fields:
        if field not in data or not data[field] or str(data[field]).strip() == '':
            return False, f"الحقل {field} مطلوب ولا يمكن أن يكون فارغاً"
    
    # التحقق من صحة القيم
    if data['goal'] not in ['lose_weight', 'muscle_gain', 'weight_gain']:
        return False, "الهدف يجب أن يكون أحد القيم: lose_weight, muscle_gain, weight_gain"
    
    if data['level'] not in ['beginner', 'intermediate', 'advanced']:
        return False, "المستوى يجب أن يكون أحد القيم: beginner, intermediate, advanced"
    
    try:
        age = int(data['age'])
        weight = float(data['weight'])
        height = float(data['height'])
        days = int(data['days_per_week'])
        
        if not (16 <= age <= 80):
            return False, "العمر يجب أن يكون بين 16 و 80 سنة"
        if not (30 <= weight <= 300):
            return False, "الوزن يجب أن يكون بين 30 و 300 كجم"
        if not (100 <= height <= 250):
            return False, "الطول يجب أن يكون بين 100 و 250 سم"
        if not (1 <= days <= 7):
            return False, "عدد أيام التمرين يجب أن يكون بين 1 و 7 أيام"
            
    except (ValueError, TypeError):
        return False, "يرجى التأكد من صحة القيم الرقمية"
    
    return True, "البيانات صحيحة"

def filter_exercises_by_health_issues(exercises, health_issues):
    """فلترة التمارين بناءً على المشاكل الصحية"""
    if not health_issues:
        return exercises
    
    health_issues_lower = health_issues.lower()
    filtered_exercises = []
    
    for exercise in exercises:
        exercise_name_lower = exercise['name'].lower()
        
        # استبعاد التمارين الضارة للركبة
        if 'ركبة' in health_issues_lower or 'knee' in health_issues_lower:
            if any(word in exercise_name_lower for word in ['سكوات', 'squat', 'lunge', 'jump']):
                continue
        
        # استبعاد التمارين الضارة للظهر
        if 'ظهر' in health_issues_lower or 'back' in health_issues_lower:
            if any(word in exercise_name_lower for word in ['deadlift', 'رفعة ميتة', 'bent over']):
                continue
        
        # استبعاد التمارين الضارة للكتف
        if 'كتف' in health_issues_lower or 'shoulder' in health_issues_lower:
            if any(word in exercise_name_lower for word in ['overhead', 'press', 'ضغط علوي']):
                continue
        
        filtered_exercises.append(exercise)
    
    return filtered_exercises

def distribute_exercises_across_days(exercises, days_per_week, goal):
    """توزيع التمارين على أيام الأسبوع"""
    if not exercises:
        return []
    
    # تجميع التمارين حسب المجموعة العضلية
    muscle_groups = {}
    for exercise in exercises:
        muscle_group = exercise['muscle_group']
        if muscle_group not in muscle_groups:
            muscle_groups[muscle_group] = []
        muscle_groups[muscle_group].append(exercise)
    
    workout_plan = []
    muscle_group_list = list(muscle_groups.keys())
    
    # توزيع التمارين حسب عدد الأيام
    for day in range(1, days_per_week + 1):
        day_exercises = []
        used_exercises = set()
        
        # اختيار مجموعات عضلية مختلفة لكل يوم
        if days_per_week <= 3:
            # تمارين الجسم كامل
            for muscle_group in muscle_group_list:
                available_exercises = [ex for ex in muscle_groups[muscle_group] 
                                     if ex['name'] not in used_exercises]
                if available_exercises:
                    selected = random.choice(available_exercises)
                    day_exercises.append(selected)
                    used_exercises.add(selected['name'])
        else:
            # تقسيم العضلات على الأيام
            muscles_per_day = max(1, len(muscle_group_list) // days_per_week)
            start_idx = ((day - 1) * muscles_per_day) % len(muscle_group_list)
            
            for i in range(muscles_per_day + 1):
                muscle_idx = (start_idx + i) % len(muscle_group_list)
                muscle_group = muscle_group_list[muscle_idx]
                
                available_exercises = [ex for ex in muscle_groups[muscle_group] 
                                     if ex['name'] not in used_exercises]
                if available_exercises:
                    selected = random.choice(available_exercises)
                    day_exercises.append(selected)
                    used_exercises.add(selected['name'])
        
        # تحديد عدد المجموعات والتكرارات حسب الهدف
        for exercise in day_exercises:
            if goal == 'lose_weight':
                exercise['sets'] = random.randint(3, 4)
                exercise['reps'] = f"{random.randint(12, 20)}-{random.randint(15, 25)}"
            elif goal == 'muscle_gain':
                exercise['sets'] = random.randint(4, 5)
                exercise['reps'] = f"{random.randint(6, 10)}-{random.randint(8, 12)}"
            else:  # weight_gain
                exercise['sets'] = random.randint(3, 4)
                exercise['reps'] = f"{random.randint(8, 12)}-{random.randint(10, 15)}"
        
        if day_exercises:
            workout_plan.append({
                "day": day,
                "exercises": day_exercises
            })
    
    return workout_plan

def generate_general_tips(goal, level):
    """توليد نصائح عامة حسب الهدف والمستوى"""
    tips = []
    
    # نصائح حسب الهدف
    if goal == 'lose_weight':
        tips.extend([
            "اشرب الماء بكثرة قبل وأثناء وبعد التمرين",
            "ركز على التمارين الهوائية مع تمارين المقاومة",
            "حافظ على نظام غذائي متوازن مع عجز في السعرات",
            "تمرن 4-5 مرات في الأسبوع لأفضل النتائج"
        ])
    elif goal == 'muscle_gain':
        tips.extend([
            "تناول البروتين بكمية كافية (1.6-2.2 جم لكل كجم من وزن الجسم)",
            "ركز على التمارين المركبة مثل السكوات والرفعة الميتة",
            "احصل على راحة كافية بين التمارين (48-72 ساعة للعضلة الواحدة)",
            "تناول وجبة غنية بالبروتين والكربوهيدرات بعد التمرين"
        ])
    else:  # weight_gain
        tips.extend([
            "تناول سعرات حرارية أكثر مما تحرق",
            "ركز على الوجبات الغنية بالبروتين والكربوهيدرات الصحية",
            "تمرن بانتظام لبناء العضلات وليس فقط زيادة الدهون",
            "تناول وجبات صغيرة ومتكررة على مدار اليوم"
        ])
    
    # نصائح حسب المستوى
    if level == 'beginner':
        tips.extend([
            "ابدأ بأوزان خفيفة وركز على الأداء الصحيح",
            "لا تتمرن كل يوم، امنح جسمك وقتاً للراحة والتعافي",
            "استعن بمدرب في البداية لتعلم الحركات الصحيحة"
        ])
    elif level == 'intermediate':
        tips.extend([
            "نوع في تمارينك كل 4-6 أسابيع لتجنب الثبات",
            "زد الأوزان تدريجياً عندما تصبح التمارين سهلة",
            "اهتم بتمارين الإحماء والتبريد"
        ])
    else:  # advanced
        tips.extend([
            "استخدم تقنيات متقدمة مثل Drop sets و Supersets",
            "راقب تقدمك بدقة وسجل أوزانك وتكراراتك",
            "فكر في دورات التدريب المختلفة (Periodization)"
        ])
    
    return tips

def generate_reasons_for_quitting_solutions():
    """توليد أسباب التوقف عن التمرين والحلول"""
    return [
        {
            "reason": "عدم وجود وقت كافي",
            "solution": "ابدأ بتمارين قصيرة 15-20 دقيقة، يمكنك التمرن في المنزل أو في استراحة العمل"
        },
        {
            "reason": "الملل من التمارين",
            "solution": "نوع في تمارينك، جرب رياضات جديدة، تمرن مع أصدقاء أو استمع للموسيقى"
        },
        {
            "reason": "عدم رؤية نتائج سريعة",
            "solution": "كن صبوراً، النتائج تحتاج 4-6 أسابيع لتظهر، ركز على التحسن في القوة والتحمل"
        },
        {
            "reason": "التعب والإرهاق",
            "solution": "تأكد من النوم الكافي، تناول طعام صحي، ابدأ بتمارين خفيفة وزد التدريج"
        },
        {
            "reason": "عدم المعرفة بالتمارين الصحيحة",
            "solution": "استعن بمدرب، شاهد فيديوهات تعليمية، ابدأ بتمارين بسيطة وآمنة"
        }
    ]

# ==================== API ENDPOINTS ====================

@app.route('/api/users', methods=['POST'])
def add_user():
    """إضافة مستخدم جديد"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "يرجى إرسال البيانات في صيغة JSON"}), 400
        
        # التحقق من صحة البيانات
        is_valid, message = validate_user_data(data)
        if not is_valid:
            return jsonify({"error": "يرجى إكمال جميع البيانات الشخصية قبل المتابعة"}), 400
        
        # إدراج المستخدم في قاعدة البيانات
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (name, age, weight, height, goal, level, days_per_week, equipment, health_issues)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'].strip(),
            int(data['age']),
            float(data['weight']),
            float(data['height']),
            data['goal'],
            data['level'],
            int(data['days_per_week']),
            data['equipment'],
            data.get('health_issues', '')
        ))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "message": "تم إضافة المستخدم بنجاح",
            "user_id": user_id,
            "status": "success"
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"خطأ في إضافة المستخدم: {str(e)}"}), 500

@app.route('/api/exercises', methods=['POST'])
def add_exercise():
    """إضافة تمرين جديد"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "يرجى إرسال البيانات في صيغة JSON"}), 400
        
        # التحقق من الحقول المطلوبة
        required_fields = ['name', 'muscle_group', 'difficulty', 'equipment_needed', 'video_url', 'tips']
        for field in required_fields:
            if field not in data or not data[field] or str(data[field]).strip() == '':
                return jsonify({"error": f"الحقل {field} مطلوب ولا يمكن أن يكون فارغاً"}), 400
        
        # التحقق من صحة مستوى الصعوبة
        if data['difficulty'] not in ['beginner', 'intermediate', 'advanced']:
            return jsonify({"error": "مستوى الصعوبة يجب أن يكون أحد القيم: beginner, intermediate, advanced"}), 400
        
        # إدراج التمرين في قاعدة البيانات
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO exercises (name, muscle_group, difficulty, equipment_needed, video_url, tips)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['name'].strip(),
            data['muscle_group'].strip(),
            data['difficulty'],
            data['equipment_needed'].strip(),
            data['video_url'].strip(),
            data['tips'].strip()
        ))
        
        exercise_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            "message": "تم إضافة التمرين بنجاح",
            "exercise_id": exercise_id,
            "status": "success"
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"خطأ في إضافة التمرين: {str(e)}"}), 500

@app.route('/api/generate-workout-plan', methods=['POST'])
def generate_workout_plan():
    """توليد خطة تمارين مخصصة"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "يرجى إرسال البيانات في صيغة JSON"}), 400
        
        # التحقق من صحة البيانات
        is_valid, message = validate_user_data(data)
        if not is_valid:
            return jsonify({"error": "يرجى إكمال جميع البيانات الشخصية قبل المتابعة"}), 400
        
        # جلب التمارين من قاعدة البيانات
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # فلترة التمارين حسب المستوى والمعدات
        query = '''
            SELECT name, muscle_group, difficulty, equipment_needed, video_url, tips
            FROM exercises 
            WHERE difficulty = ? OR difficulty = 'beginner'
        '''
        params = [data['level']]
        
        # إضافة فلتر المعدات إذا كان محدداً
        if data['equipment'] and data['equipment'].strip():
            query += ' AND (equipment_needed LIKE ? OR equipment_needed = "وزن الجسم")'
            params.append(f"%{data['equipment']}%")
        
        cursor.execute(query, params)
        exercises_raw = cursor.fetchall()
        conn.close()
        
        # تحويل النتائج إلى قائمة من القواميس
        exercises = []
        for row in exercises_raw:
            exercises.append({
                'name': row['name'],
                'target_muscle': row['muscle_group'],
                'muscle_group': row['muscle_group'],
                'difficulty': row['difficulty'],
                'equipment_needed': row['equipment_needed'],
                'video': row['video_url'],
                'tips': row['tips']
            })
        
        # فلترة التمارين حسب المشاكل الصحية
        exercises = filter_exercises_by_health_issues(exercises, data.get('health_issues', ''))
        
        if not exercises:
            return jsonify({
                "error": "لم يتم العثور على تمارين مناسبة لمعاييرك. يرجى تعديل المعايير أو إضافة المزيد من التمارين"
            }), 404
        
        # توزيع التمارين على أيام الأسبوع
        workout_plan = distribute_exercises_across_days(
            exercises, 
            int(data['days_per_week']), 
            data['goal']
        )
        
        # توليد النصائح العامة
        general_tips = generate_general_tips(data['goal'], data['level'])
        
        # توليد أسباب التوقف والحلول
        reasons_for_quitting = generate_reasons_for_quitting_solutions()
        
        # تحديد اسم الهدف بالعربية
        goal_names = {
            'lose_weight': 'إنقاص الوزن وحرق الدهون',
            'muscle_gain': 'بناء العضلات وزيادة الكتلة العضلية',
            'weight_gain': 'زيادة الوزن بطريقة صحية'
        }
        
        response = {
            "goal": goal_names.get(data['goal'], data['goal']),
            "plan": workout_plan,
            "general_tips": general_tips,
            "reasons_for_quitting": reasons_for_quitting,
            "user_info": {
                "name": data['name'],
                "level": data['level'],
                "days_per_week": data['days_per_week'],
                "equipment": data['equipment']
            },
            "generated_at": datetime.now().isoformat(),
            "status": "success"
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في توليد خطة التمارين: {str(e)}"}), 500

@app.route('/api/exercises', methods=['GET'])
def get_exercises():
    """جلب جميع التمارين"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # إضافة فلاتر اختيارية
        muscle_group = request.args.get('muscle_group')
        difficulty = request.args.get('difficulty')
        equipment = request.args.get('equipment')
        
        query = 'SELECT * FROM exercises WHERE 1=1'
        params = []
        
        if muscle_group:
            query += ' AND muscle_group = ?'
            params.append(muscle_group)
        
        if difficulty:
            query += ' AND difficulty = ?'
            params.append(difficulty)
        
        if equipment:
            query += ' AND equipment_needed LIKE ?'
            params.append(f'%{equipment}%')
        
        query += ' ORDER BY created_at DESC'
        
        cursor.execute(query, params)
        exercises = cursor.fetchall()
        conn.close()
        
        exercises_list = []
        for exercise in exercises:
            exercises_list.append({
                'id': exercise['id'],
                'name': exercise['name'],
                'muscle_group': exercise['muscle_group'],
                'difficulty': exercise['difficulty'],
                'equipment_needed': exercise['equipment_needed'],
                'video_url': exercise['video_url'],
                'tips': exercise['tips'],
                'created_at': exercise['created_at']
            })
        
        return jsonify({
            "exercises": exercises_list,
            "total": len(exercises_list),
            "status": "success"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في جلب التمارين: {str(e)}"}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    """جلب جميع المستخدمين"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        users = cursor.fetchall()
        conn.close()
        
        users_list = []
        for user in users:
            users_list.append({
                'id': user['id'],
                'name': user['name'],
                'age': user['age'],
                'weight': user['weight'],
                'height': user['height'],
                'goal': user['goal'],
                'level': user['level'],
                'days_per_week': user['days_per_week'],
                'equipment': user['equipment'],
                'health_issues': user['health_issues'],
                'created_at': user['created_at']
            })
        
        return jsonify({
            "users": users_list,
            "total": len(users_list),
            "status": "success"
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"خطأ في جلب المستخدمين: {str(e)}"}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """فحص حالة الـ API"""
    return jsonify({
        "status": "healthy",
        "message": "API يعمل بشكل طبيعي",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }), 200

@app.errorhandler(404)
def not_found(error):
    """معالج الأخطاء 404"""
    return jsonify({
        "error": "الصفحة المطلوبة غير موجودة",
        "status": "error",
        "code": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """معالج الأخطاء 500"""
    return jsonify({
        "error": "خطأ داخلي في الخادم",
        "status": "error",
        "code": 500
    }), 500

if __name__ == '__main__':
    # إنشاء قاعدة البيانات عند بدء التطبيق
    init_database()
    
    print("🚀 بدء تشغيل Flask API لمولد خطط التمارين")
    print("📊 قاعدة البيانات: workout_generator.db")
    print("🌐 الخادم: http://localhost:5001")
    print("📖 التوثيق: راجع الأمثلة في نهاية الملف")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

"""
=== أمثلة CURL للاختبار ===

1. إضافة مستخدم جديد:
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

2. إضافة تمرين جديد:
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

3. توليد خطة تمارين:
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

4. جلب جميع التمارين:
curl -X GET http://localhost:5001/api/exercises

5. جلب التمارين مع فلترة:
curl -X GET "http://localhost:5001/api/exercises?muscle_group=صدر&difficulty=beginner"

6. جلب جميع المستخدمين:
curl -X GET http://localhost:5001/api/users

7. فحص حالة الـ API:
curl -X GET http://localhost:5001/api/health

=== أمثلة Postman ===

1. POST /api/users
   Body (JSON):
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

2. POST /api/exercises
   Body (JSON):
   {
     "name": "السكوات",
     "muscle_group": "أرجل",
     "difficulty": "intermediate",
     "equipment_needed": "وزن الجسم أو بار",
     "video_url": "https://youtube.com/watch?v=example2",
     "tips": "انزل حتى تصبح الفخذان موازيتان للأرض"
   }

3. POST /api/generate-workout-plan
   Body (JSON):
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
"""