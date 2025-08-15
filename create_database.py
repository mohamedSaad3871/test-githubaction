"""
سكريبت إنشاء قاعدة البيانات وإدراج البيانات التجريبية
لمولد خطط التمارين

تشغيل السكريبت: python create_database.py
"""

import sqlite3
import json
from datetime import datetime

DATABASE_NAME = 'workout_generator.db'

def create_database():
    """إنشاء قاعدة البيانات والجداول"""
    print("🔧 إنشاء قاعدة البيانات...")
    
    conn = sqlite3.connect(DATABASE_NAME)
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
    print("✅ تم إنشاء قاعدة البيانات والجداول بنجاح")

def insert_sample_exercises():
    """إدراج تمارين تجريبية شاملة"""
    print("💪 إدراج التمارين التجريبية...")
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # تمارين شاملة لجميع المجموعات العضلية
    exercises_data = [
        # تمارين الصدر
        ('تمرين الضغط', 'صدر', 'beginner', 'وزن الجسم', 'https://youtube.com/watch?v=IODxDxX7oi4', 'حافظ على استقامة الجسم من الرأس إلى القدمين، انزل ببطء حتى يلامس الصدر الأرض تقريباً'),
        ('ضغط الدمبل على البنش', 'صدر', 'intermediate', 'دمبل، بنش', 'https://youtube.com/watch?v=QcY11Uht6s0', 'اخفض الدمبل ببطء حتى مستوى الصدر، ثم ادفع لأعلى مع الزفير'),
        ('ضغط البار على البنش', 'صدر', 'intermediate', 'بار، بنش', 'https://youtube.com/watch?v=rT7DgCr-3pg', 'امسك البار بقبضة أوسع من الكتفين، اخفض البار إلى الصدر ثم ادفع لأعلى'),
        ('تمرين الضغط المائل', 'صدر', 'advanced', 'وزن الجسم', 'https://youtube.com/watch?v=cfns4B1h_Ys', 'ضع القدمين على سطح مرتفع، نفذ تمرين الضغط العادي'),
        
        # تمارين الظهر
        ('العقلة', 'ظهر', 'intermediate', 'بار عقلة', 'https://youtube.com/watch?v=eGo4IYlbE5g', 'امسك البار بقبضة أوسع من الكتفين، اسحب الجسم لأعلى حتى يتجاوز الذقن البار'),
        ('تمرين السوبرمان', 'ظهر', 'beginner', 'وزن الجسم', 'https://youtube.com/watch?v=cc6UVRS7PW4', 'استلق على البطن، ارفع الصدر والساقين عن الأرض في نفس الوقت'),
        ('سحب الدمبل بذراع واحدة', 'ظهر', 'intermediate', 'دمبل، بنش', 'https://youtube.com/watch?v=roCP6wCXPqo', 'ضع ركبة واحدة على البنش، اسحب الدمبل إلى جانب الجسم'),
        ('الرفعة الميتة', 'ظهر', 'advanced', 'بار', 'https://youtube.com/watch?v=ytGaGIn3SjE', 'حافظ على استقامة الظهر، ارفع البار من الأرض بقوة الساقين والظهر'),
        
        # تمارين الساقين
        ('السكوات', 'ساقين', 'beginner', 'وزن الجسم', 'https://youtube.com/watch?v=Dy28eq2PjcM', 'انزل حتى تصبح الفخذان موازيتان للأرض، حافظ على استقامة الظهر'),
        ('السكوات بالدمبل', 'ساقين', 'intermediate', 'دمبل', 'https://youtube.com/watch?v=Uv_DKDl7EjA', 'امسك الدمبل أمام الصدر، نفذ السكوات العادي'),
        ('الطعنات', 'ساقين', 'intermediate', 'وزن الجسم', 'https://youtube.com/watch?v=QOVaHwm-Q6U', 'اتخذ خطوة كبيرة للأمام، انزل حتى تلامس الركبة الخلفية الأرض تقريباً'),
        ('السكوات بالبار', 'ساقين', 'advanced', 'بار', 'https://youtube.com/watch?v=ultWZbUMPL8', 'ضع البار على الكتفين، نفذ السكوات مع الحفاظ على توازن الجسم'),
        
        # تمارين الأكتاف
        ('الضغط العسكري بالدمبل', 'أكتاف', 'intermediate', 'دمبل', 'https://youtube.com/watch?v=qEwKCR5JCog', 'ادفع الدمبل من مستوى الكتف إلى أعلى الرأس'),
        ('رفع جانبي بالدمبل', 'أكتاف', 'beginner', 'دمبل', 'https://youtube.com/watch?v=3VcKaXpzqRo', 'ارفع الدمبل من جانب الجسم حتى مستوى الكتف'),
        ('رفع أمامي بالدمبل', 'أكتاف', 'beginner', 'دمبل', 'https://youtube.com/watch?v=qzaKUHI8Zt8', 'ارفع الدمبل من أمام الجسم حتى مستوى الكتف'),
        ('الضغط العسكري بالبار', 'أكتاف', 'advanced', 'بار', 'https://youtube.com/watch?v=2yjwXTZQDDI', 'ادفع البار من مستوى الكتف إلى أعلى الرأس مع الحفاظ على استقامة الجسم'),
        
        # تمارين الذراعين
        ('تمرين العضلة ذات الرأسين بالدمبل', 'ذراعين', 'beginner', 'دمبل', 'https://youtube.com/watch?v=ykJmrZ5v0Oo', 'ارفع الدمبل من وضع الذراع المستقيم إلى الكتف'),
        ('تمرين الترايسبس بالدمبل', 'ذراعين', 'intermediate', 'دمبل', 'https://youtube.com/watch?v=YbX7Wd8jQ-Q', 'امسك الدمبل بكلتا اليدين خلف الرأس، ارفع وأخفض الدمبل'),
        ('تمرين الضغط الضيق', 'ذراعين', 'intermediate', 'وزن الجسم', 'https://youtube.com/watch?v=cfns4B1h_Ys', 'نفذ تمرين الضغط مع وضع اليدين قريباً من بعضهما'),
        ('تمرين العضلة ذات الرأسين بالبار', 'ذراعين', 'advanced', 'بار', 'https://youtube.com/watch?v=kwG2ipFRgfo', 'امسك البار بقبضة سفلية، ارفع البار إلى الصدر'),
        
        # تمارين البطن والجذع
        ('تمرين البطن العادي', 'بطن', 'beginner', 'وزن الجسم', 'https://youtube.com/watch?v=1fbU_MkV7NE', 'استلق على الظهر، ارفع الجذع العلوي نحو الركبتين'),
        ('تمرين البلانك', 'بطن', 'beginner', 'وزن الجسم', 'https://youtube.com/watch?v=ASdvN_XEl_c', 'حافظ على وضع اللوح الخشبي لأطول فترة ممكنة'),
        ('تمرين الدراجة', 'بطن', 'intermediate', 'وزن الجسم', 'https://youtube.com/watch?v=9FGilxCbdz8', 'استلق على الظهر، حرك الساقين كأنك تقود دراجة'),
        ('تمرين رفع الساقين', 'بطن', 'intermediate', 'وزن الجسم', 'https://youtube.com/watch?v=JB2oyawG9KI', 'استلق على الظهر، ارفع الساقين المستقيمتين إلى أعلى'),
        
        # تمارين كامل الجسم
        ('البيربي', 'كامل الجسم', 'advanced', 'وزن الجسم', 'https://youtube.com/watch?v=auBLPXO8Fww', 'انزل إلى وضع السكوات، اقفز إلى وضع البلانك، نفذ ضغطة، اقفز للخلف ثم لأعلى'),
        ('تمرين الجبل المتسلق', 'كامل الجسم', 'intermediate', 'وزن الجسم', 'https://youtube.com/watch?v=nmwgirgXLYM', 'من وضع البلانك، حرك الركبتين بالتناوب نحو الصدر بسرعة'),
        ('القفز مع فتح الساقين', 'كامل الجسم', 'beginner', 'وزن الجسم', 'https://youtube.com/watch?v=c4DAnQ6DtF8', 'اقفز مع فتح الساقين ورفع الذراعين، ثم العودة للوضع الأصلي'),
        ('تمرين الكيتل بيل سوينغ', 'كامل الجسم', 'intermediate', 'كيتل بيل', 'https://youtube.com/watch?v=YSxHifyI6s8', 'أرجح الكيتل بيل من بين الساقين إلى مستوى الكتف'),
        
        # تمارين الكارديو
        ('الجري في المكان', 'كارديو', 'beginner', 'وزن الجسم', 'https://youtube.com/watch?v=8opcQdC-V-U', 'اجر في المكان مع رفع الركبتين عالياً'),
        ('تمرين الصندوق', 'كارديو', 'intermediate', 'صندوق أو درج', 'https://youtube.com/watch?v=5MYiM_8_-5E', 'اصعد وانزل من الصندوق بالتناوب'),
        ('تمرين الحبل', 'كارديو', 'intermediate', 'حبل القفز', 'https://youtube.com/watch?v=1BZM2Vre5oc', 'اقفز بالحبل بإيقاع ثابت'),
        ('تمرين HIIT', 'كارديو', 'advanced', 'وزن الجسم', 'https://youtube.com/watch?v=ml6cT4AZdqI', 'تناوب بين تمارين عالية الكثافة وفترات راحة قصيرة'),
    ]
    
    cursor.executemany('''
        INSERT INTO exercises (name, muscle_group, difficulty, equipment_needed, video_url, tips)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', exercises_data)
    
    conn.commit()
    conn.close()
    print(f"✅ تم إدراج {len(exercises_data)} تمرين بنجاح")

def insert_sample_users():
    """إدراج مستخدمين تجريبيين"""
    print("👥 إدراج المستخدمين التجريبيين...")
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    users_data = [
        ('أحمد محمد', 25, 75.5, 175.0, 'muscle_gain', 'intermediate', 4, 'دمبل، بار', ''),
        ('سارة أحمد', 28, 65.0, 165.0, 'lose_weight', 'beginner', 3, 'وزن الجسم', ''),
        ('محمد علي', 30, 80.0, 180.0, 'lose_weight', 'intermediate', 5, 'أجهزة الجيم', 'ألم في الركبة'),
        ('فاطمة محمود', 22, 55.0, 160.0, 'muscle_gain', 'beginner', 4, 'دمبل', ''),
        ('خالد حسن', 35, 90.0, 185.0, 'lose_weight', 'advanced', 6, 'جميع المعدات', ''),
        ('نور الدين', 26, 70.0, 170.0, 'weight_gain', 'intermediate', 3, 'بار، دمبل', 'ألم في الظهر'),
    ]
    
    cursor.executemany('''
        INSERT INTO users (name, age, weight, height, goal, level, days_per_week, equipment, health_issues)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', users_data)
    
    conn.commit()
    conn.close()
    print(f"✅ تم إدراج {len(users_data)} مستخدم تجريبي بنجاح")

def display_database_info():
    """عرض معلومات قاعدة البيانات"""
    print("\n📊 معلومات قاعدة البيانات:")
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # عدد المستخدمين
    cursor.execute('SELECT COUNT(*) FROM users')
    users_count = cursor.fetchone()[0]
    print(f"👥 عدد المستخدمين: {users_count}")
    
    # عدد التمارين
    cursor.execute('SELECT COUNT(*) FROM exercises')
    exercises_count = cursor.fetchone()[0]
    print(f"💪 عدد التمارين: {exercises_count}")
    
    # توزيع التمارين حسب المجموعة العضلية
    cursor.execute('SELECT muscle_group, COUNT(*) FROM exercises GROUP BY muscle_group')
    muscle_groups = cursor.fetchall()
    print("\n🎯 توزيع التمارين حسب المجموعة العضلية:")
    for group, count in muscle_groups:
        print(f"   {group}: {count} تمرين")
    
    # توزيع التمارين حسب مستوى الصعوبة
    cursor.execute('SELECT difficulty, COUNT(*) FROM exercises GROUP BY difficulty')
    difficulties = cursor.fetchall()
    print("\n📈 توزيع التمارين حسب مستوى الصعوبة:")
    for difficulty, count in difficulties:
        print(f"   {difficulty}: {count} تمرين")
    
    conn.close()

def create_api_test_file():
    """إنشاء ملف اختبار للـ API"""
    print("🧪 إنشاء ملف اختبار API...")
    
    test_content = '''#!/usr/bin/env python3
"""
ملف اختبار API مولد خطط التمارين
تشغيل الاختبارات: python test_api.py
"""

import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_health_check():
    """اختبار فحص حالة API"""
    print("🔍 اختبار فحص حالة API...")
    response = requests.get(f'{BASE_URL}/health')
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_add_user():
    """اختبار إضافة مستخدم جديد"""
    print("👤 اختبار إضافة مستخدم جديد...")
    user_data = {
        "name": "اختبار المستخدم",
        "age": 25,
        "weight": 70.0,
        "height": 175.0,
        "goal": "muscle_gain",
        "level": "beginner",
        "days_per_week": 3,
        "equipment": "دمبل",
        "health_issues": ""
    }
    
    response = requests.post(f'{BASE_URL}/users', json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_add_exercise():
    """اختبار إضافة تمرين جديد"""
    print("💪 اختبار إضافة تمرين جديد...")
    exercise_data = {
        "name": "تمرين اختبار",
        "muscle_group": "صدر",
        "difficulty": "beginner",
        "equipment_needed": "وزن الجسم",
        "video_url": "https://youtube.com/watch?v=test",
        "tips": "نصائح تمرين الاختبار"
    }
    
    response = requests.post(f'{BASE_URL}/exercises', json=exercise_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_generate_workout_plan():
    """اختبار توليد خطة تمارين"""
    print("📋 اختبار توليد خطة تمارين...")
    plan_data = {
        "name": "مستخدم الاختبار",
        "age": 28,
        "weight": 65.0,
        "height": 165.0,
        "goal": "lose_weight",
        "level": "beginner",
        "days_per_week": 3,
        "equipment": "وزن الجسم",
        "health_issues": ""
    }
    
    response = requests.post(f'{BASE_URL}/generate-workout-plan', json=plan_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Goal: {result['goal']}")
        print(f"Plan days: {len(result['plan'])}")
        print(f"General tips: {len(result['general_tips'])}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_get_exercises():
    """اختبار جلب التمارين"""
    print("📝 اختبار جلب التمارين...")
    response = requests.get(f'{BASE_URL}/exercises')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total exercises: {result['total']}")
    else:
        print(f"Error: {response.json()}")
    print()

def test_get_users():
    """اختبار جلب المستخدمين"""
    print("👥 اختبار جلب المستخدمين...")
    response = requests.get(f'{BASE_URL}/users')
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Total users: {result['total']}")
    else:
        print(f"Error: {response.json()}")
    print()

if __name__ == '__main__':
    print("🚀 بدء اختبارات API مولد خطط التمارين\\n")
    
    try:
        test_health_check()
        test_add_user()
        test_add_exercise()
        test_generate_workout_plan()
        test_get_exercises()
        test_get_users()
        
        print("✅ تم إنهاء جميع الاختبارات")
        
    except requests.exceptions.ConnectionError:
        print("❌ خطأ: لا يمكن الاتصال بالخادم")
        print("تأكد من تشغيل الخادم أولاً: python workout_api.py")
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
'''
    
    with open('test_api.py', 'w', encoding='utf-8') as f:
        f.write(test_content)
    
    print("✅ تم إنشاء ملف test_api.py")

def main():
    """الدالة الرئيسية"""
    print("🚀 بدء إنشاء قاعدة البيانات لمولد خطط التمارين")
    print("=" * 50)
    
    # إنشاء قاعدة البيانات
    create_database()
    
    # إدراج البيانات التجريبية
    insert_sample_exercises()
    insert_sample_users()
    
    # عرض معلومات قاعدة البيانات
    display_database_info()
    
    # إنشاء ملف اختبار API
    create_api_test_file()
    
    print("\n" + "=" * 50)
    print("✅ تم إنشاء قاعدة البيانات بنجاح!")
    print(f"📁 اسم قاعدة البيانات: {DATABASE_NAME}")
    print("🚀 يمكنك الآن تشغيل API: python workout_api.py")
    print("🧪 لاختبار API: python test_api.py")

if __name__ == '__main__':
    main()