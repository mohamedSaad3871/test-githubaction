from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, IntegerField, SelectField, FloatField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, NumberRange, Optional, Length
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import random
import datetime
import requests
import json
from urllib.parse import quote
import os
import time
from werkzeug.utils import secure_filename
from PIL import Image
# from ai_workout_generator import qwen_generator  # Commented out temporarily
from personalized_workout_generator import PersonalizedWorkoutGenerator
from advanced_workout_generator import AdvancedWorkoutGenerator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'jismi-ahsan-secret-key-2024'
app.config['DATABASE'] = 'fitness_app.db'

# Add nl2br filter for line breaks
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks"""
    if text is None:
        return ''
    return text.replace('\n', '<br>')

# Configuration for file uploads
UPLOAD_FOLDER = 'static/images/meals'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path, max_size=(800, 600)):
    """Resize image to optimize file size"""
    with Image.open(image_path) as img:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        img.save(image_path, optimize=True, quality=85)


# Enhanced Weight Loss Form with WhatsApp
class WeightLossForm(FlaskForm):
    name = StringField('الاسم', 
                      validators=[DataRequired(message='الرجاء إدخال الاسم')])
    
    age = IntegerField('العمر', 
                      validators=[
                          DataRequired(message='الرجاء إدخال العمر'),
                          NumberRange(min=16, max=80, message='العمر يجب أن يكون بين 16 و 80 سنة')
                      ])
    
    gender = SelectField('الجنس',
                        choices=[
                            ('male', 'ذكر'),
                            ('female', 'أنثى')
                        ],
                        validators=[DataRequired(message='الرجاء اختيار الجنس')])
    
    weight = FloatField('الوزن الحالي (كجم)',
                       validators=[
                           DataRequired(message='الرجاء إدخال الوزن'),
                           NumberRange(min=30, max=300, message='الوزن يجب أن يكون بين 30 و 300 كجم')
                       ])
    
    height = FloatField('الطول (سم)',
                       validators=[
                           DataRequired(message='الرجاء إدخال الطول'),
                           NumberRange(min=100, max=250, message='الطول يجب أن يكون بين 100 و 250 سم')
                       ])
    
    target_weight = FloatField('الوزن المطلوب (كجم)',
                             validators=[
                                 DataRequired(message='الرجاء إدخال الوزن المطلوب'),
                                 NumberRange(min=30, max=300, message='الوزن المطلوب يجب أن يكون بين 30 و 300 كجم')
                             ])
    
    activity_level = SelectField('مستوى النشاط',
                               choices=[
                                   ('sedentary', 'قليل الحركة - مكتبي معظم اليوم'),
                                   ('light', 'نشاط خفيف - تمشية خفيفة'),
                                   ('moderate', 'نشاط متوسط - تمارين 3 مرات أسبوعياً'),
                                   ('active', 'نشيط - تمارين 5 مرات أسبوعياً'),
                                   ('very_active', 'نشيط جداً - تمارين يومية')
                               ],
                               validators=[DataRequired(message='الرجاء اختيار مستوى النشاط')])
    
    goal = SelectField('الهدف',
                      choices=[
                          ('weight_loss', 'تخسيس وحرق دهون'),
                          ('muscle_gain', 'بناء عضلات'),
                          ('maintenance', 'الحفاظ على الوزن')
                      ],
                      validators=[DataRequired(message='الرجاء اختيار الهدف')])
    
    whatsapp = StringField('رقم الواتساب (اختياري)',
                          validators=[Optional()],
                          render_kw={"placeholder": "مثال: +201234567890", "dir": "ltr"})
    
    submit = SubmitField('اطلع خطتي المخصصة! 💪')

# Admin Forms
class AdminLoginForm(FlaskForm):
    username = StringField('اسم المستخدم', validators=[DataRequired()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])
    submit = SubmitField('تسجيل الدخول')

class ExerciseForm(FlaskForm):
    name_en = StringField('اسم التمرين (إنجليزي)', validators=[DataRequired()])
    name_ar = StringField('اسم التمرين (عربي)', validators=[DataRequired()])
    muscle_group = SelectField('المجموعة العضلية', 
                              choices=[
                                  ('chest', 'صدر'),
                                  ('back', 'ظهر'),
                                  ('legs', 'أرجل'),
                                  ('shoulders', 'أكتاف'),
                                  ('arms', 'ذراعين'),
                                  ('core', 'بطن وجذع'),
                                  ('full_body', 'جسم كامل')
                              ], validators=[DataRequired()])
    equipment_type = SelectField('نوع المعدات',
                                choices=[
                                    ('bodyweight', 'وزن الجسم'),
                                    ('dumbbells', 'دمبل'),
                                    ('machines', 'أجهزة'),
                                    ('bands', 'أحزمة مقاومة'),
                                    ('barbell', 'بار'),
                                    ('kettlebell', 'كيتل بيل'),
                                    ('cable', 'كابل')
                                ], validators=[DataRequired()])
    difficulty_level = SelectField('مستوى الصعوبة',
                                  choices=[
                                      ('beginner', 'مبتدئ'),
                                      ('intermediate', 'متوسط'),
                                      ('advanced', 'متقدم')
                                  ], validators=[DataRequired()])
    goal = SelectField('الهدف',
                      choices=[
                          ('weight_loss', 'إنقاص الوزن'),
                          ('muscle_gain', 'بناء العضلات'),
                          ('maintain', 'المحافظة على الوزن'),
                          ('strength', 'زيادة القوة'),
                          ('endurance', 'تحسين التحمل')
                      ], validators=[DataRequired()])
    split_type = SelectField('نوع التقسيم',
                            choices=[
                                ('full_body', 'Full Body'),
                                ('upper_lower', 'Upper/Lower'),
                                ('push_pull_legs', 'Push/Pull/Legs'),
                                ('bro_split', 'Bro Split'),
                                ('crossfit', 'CrossFit'),
                                ('hiit', 'HIIT')
                            ], validators=[DataRequired()])
    sets = IntegerField('عدد المجموعات', validators=[DataRequired(), NumberRange(min=1, max=10)])
    reps = StringField('عدد التكرارات', validators=[DataRequired()])
    rest_time = StringField('وقت الراحة', validators=[DataRequired()])
    instructions = TextAreaField('التعليمات')
    form_cues = TextAreaField('نصائح الأداء')
    common_mistakes = TextAreaField('الأخطاء الشائعة')
    risk_notes = TextAreaField('ملاحظات المخاطر')
    alternatives = TextAreaField('البدائل')
    video_url = StringField('رابط الفيديو')
    image = FileField('صورة التمرين')
    submit = SubmitField('حفظ التمرين')

# Admin Authentication Functions
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('يجب تسجيل الدخول كمدرب أولاً', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def create_default_admin():
    """إنشاء حساب مدرب افتراضي"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # التحقق من وجود مدرب افتراضي
    cursor.execute('SELECT id FROM admin_users WHERE username = ?', ('admin',))
    if cursor.fetchone():
        conn.close()
        return
    
    # إنشاء مدرب افتراضي
    password_hash = generate_password_hash('admin123')
    cursor.execute('''
        INSERT INTO admin_users (username, password_hash, role, full_name, email)
        VALUES (?, ?, ?, ?, ?)
    ''', ('admin', password_hash, 'admin', 'مدرب افتراضي', 'admin@fitness.com'))
    
    conn.commit()
    conn.close()
    print("تم إنشاء حساب المدرب الافتراضي: admin / admin123")

# إضافة دالة لتحديث هيكل قاعدة البيانات
def load_data_from_json():
    """تحميل البيانات من ملف arabic_fitness_data.json وإدراجها في قاعدة البيانات"""
    import json
    import os
    
    json_file_path = 'arabic_fitness_data.json'
    if not os.path.exists(json_file_path):
        print(f"ملف {json_file_path} غير موجود")
        return
    
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # مسح البيانات القديمة
        cursor.execute('DELETE FROM exercises')
        cursor.execute('DELETE FROM meals')
        
        # إدراج التمارين
        exercises_data = []
        for exercise in data.get('exercises', []):
            # تحويل مستوى الصعوبة إلى رقم للتوافق مع الكود الحالي
            difficulty_map = {'مبتدئ': 1, 'متوسط': 2, 'متقدم': 3}
            difficulty_num = difficulty_map.get(exercise.get('difficulty', 'مبتدئ'), 1)
            
            # تحديد نوع الهدف بناءً على مجموعة العضلات
            goal_type = 'weight_loss' if exercise.get('muscle_group') == 'كامل الجسم' else 'general'
            
            # تقدير السعرات المحروقة بناءً على مستوى الصعوبة
            calories_map = {'مبتدئ': 50, 'متوسط': 80, 'متقدم': 120}
            calories = calories_map.get(exercise.get('difficulty', 'مبتدئ'), 50)
            
            exercises_data.append((
                exercise.get('name', ''),
                exercise.get('muscle_group', ''),
                difficulty_num,  # للتوافق مع الكود الحالي
                3,  # sets افتراضي
                12,  # reps افتراضي
                calories,
                exercise.get('equipment', 'وزن الجسم'),
                goal_type,
                exercise.get('description', ''),
                exercise.get('video_url', ''),
                exercise.get('difficulty', 'مبتدئ')  # difficulty_text
            ))
        
        cursor.executemany('''
            INSERT INTO exercises (name, muscle_group, difficulty, sets, reps, calories_burned, 
                                 equipment, goal_type, description, video_url, difficulty_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', exercises_data)
        
        # إدراج الوجبات
        meals_data = []
        for meal in data.get('meals', []):
            # تحويل نوع الوجبة
            meal_type_map = {
                'فطار': 'breakfast',
                'غداء': 'lunch', 
                'عشاء': 'dinner',
                'وجبة خفيفة': 'snack'
            }
            category = meal_type_map.get(meal.get('meal_type', 'فطار'), 'breakfast')
            
            # تحديد نوع الهدف بناءً على السعرات
            calories = meal.get('calories', 0)
            if calories < 200:
                goal_type = 'weight_loss'
            elif calories > 400:
                goal_type = 'muscle_gain'
            else:
                goal_type = 'maintenance'
            
            meals_data.append((
                meal.get('name', ''),
                category,
                calories,
                meal.get('protein', 0),
                meal.get('carbs', 0),
                meal.get('fats', 0),
                goal_type,
                'easy',  # difficulty افتراضي
                '/static/images/meals/default.jpg',  # image_url افتراضي
                meal.get('food_preference', 'عادي')
            ))
        
        cursor.executemany('''
            INSERT INTO meals (name, category, calories, protein, carbs, fats, 
                             goal_type, difficulty, image_url, food_preference)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', meals_data)
        
        conn.commit()
        print(f"تم تحميل {len(exercises_data)} تمرين و {len(meals_data)} وجبة من ملف JSON")
        
    except Exception as e:
        print(f"خطأ في تحميل البيانات من JSON: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_database_schema():
    """Update database schema to add missing columns"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # التحقق من أعمدة جدول meals
        cursor.execute("PRAGMA table_info(meals)")
        meals_columns = [column[1] for column in cursor.fetchall()]
        
        # إضافة الأعمدة المفقودة لجدول meals
        if 'image_url' not in meals_columns:
            print("إضافة العمود image_url إلى جدول meals...")
            cursor.execute('ALTER TABLE meals ADD COLUMN image_url TEXT')
            
        if 'food_preference' not in meals_columns:
            print("إضافة العمود food_preference إلى جدول meals...")
            cursor.execute('ALTER TABLE meals ADD COLUMN food_preference TEXT DEFAULT "عادي"')
        
        # التحقق من أعمدة جدول admin_exercises
        cursor.execute("PRAGMA table_info(admin_exercises)")
        exercise_columns = [column[1] for column in cursor.fetchall()]
        
        # إضافة الأعمدة المفقودة لجدول admin_exercises
        if 'goal' not in exercise_columns:
            print("إضافة العمود goal إلى جدول admin_exercises...")
            cursor.execute('ALTER TABLE admin_exercises ADD COLUMN goal TEXT DEFAULT "weight_loss"')
            
        if 'split_type' not in exercise_columns:
            print("إضافة العمود split_type إلى جدول admin_exercises...")
            cursor.execute('ALTER TABLE admin_exercises ADD COLUMN split_type TEXT DEFAULT "full_body"')
            
        if 'risk_notes' not in exercise_columns:
            print("إضافة العمود risk_notes إلى جدول admin_exercises...")
            cursor.execute('ALTER TABLE admin_exercises ADD COLUMN risk_notes TEXT')
            
        if 'alternatives' not in exercise_columns:
            print("إضافة العمود alternatives إلى جدول admin_exercises...")
            cursor.execute('ALTER TABLE admin_exercises ADD COLUMN alternatives TEXT')
        
        # تحديث نوع العمود rest_time إذا كان integer
        cursor.execute("PRAGMA table_info(admin_exercises)")
        columns_info = cursor.fetchall()
        rest_time_column = next((col for col in columns_info if col[1] == 'rest_time'), None)
        if rest_time_column and 'INTEGER' in rest_time_column[2].upper():
            print("تحديث نوع العمود rest_time...")
            # SQLite doesn't support ALTER COLUMN, so we'll handle this in the application logic
            
        # التحقق من أعمدة جدول exercises
        cursor.execute("PRAGMA table_info(exercises)")
        exercises_columns = [column[1] for column in cursor.fetchall()]
        
        # إضافة الأعمدة المفقودة لجدول exercises
        if 'description' not in exercises_columns:
            print("إضافة العمود description إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN description TEXT')
            
        if 'video_url' not in exercises_columns:
            print("إضافة العمود video_url إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN video_url TEXT')
            
        if 'difficulty_text' not in exercises_columns:
            print("إضافة العمود difficulty_text إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN difficulty_text TEXT DEFAULT "مبتدئ"')
            
        if 'level' not in exercises_columns:
            print("إضافة العمود level إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN level TEXT DEFAULT "beginner"')
            
        if 'goal' not in exercises_columns:
            print("إضافة العمود goal إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN goal TEXT DEFAULT "fitness"')
            
        if 'split_type' not in exercises_columns:
            print("إضافة العمود split_type إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN split_type TEXT DEFAULT "full_body"')
            
        if 'rest_time' not in exercises_columns:
            print("إضافة العمود rest_time إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN rest_time INTEGER DEFAULT 60')
            
        if 'risk_notes' not in exercises_columns:
            print("إضافة العمود risk_notes إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN risk_notes TEXT')
            
        if 'alternatives' not in exercises_columns:
            print("إضافة العمود alternatives إلى جدول exercises...")
            cursor.execute('ALTER TABLE exercises ADD COLUMN alternatives TEXT')
            
        conn.commit()
        print("تم تحديث هيكل قاعدة البيانات بنجاح!")
        
    except Exception as e:
        print(f"خطأ في تحديث قاعدة البيانات: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

# Database initialization
# Update the meals table creation in init_db() function
# تعديل دالة init_db لتحميل البيانات من JSON
def init_db():
    conn = sqlite3.connect('fitness_app.db')
    cursor = conn.cursor()
    
    # إنشاء الجداول (نفس الكود الموجود)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            weight REAL NOT NULL,
            height INTEGER NOT NULL,
            target_weight REAL NOT NULL,
            activity_level TEXT NOT NULL,
            goal TEXT NOT NULL,
            whatsapp TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Plans table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            daily_calories INTEGER,
            protein INTEGER,
            carbs INTEGER,
            fats INTEGER,
            water_intake INTEGER,
            bmr INTEGER,
            bmi REAL,
            estimated_weeks INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Enhanced Meals table (matches your specification)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL, -- فطار, غداء, عشاء, وجبة خفيفة
            calories INTEGER NOT NULL,
            protein INTEGER DEFAULT 0,
            carbs INTEGER DEFAULT 0,
            fats INTEGER DEFAULT 0,
            goal_type TEXT DEFAULT 'all', -- weight_loss, muscle_gain, maintenance
            difficulty TEXT,
            image_url TEXT,
            food_preference TEXT DEFAULT 'عادي' -- عادي, نباتي, صحي, سريع
        )
    ''')
    
    # Workouts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            duration INTEGER NOT NULL,
            calories_burned INTEGER NOT NULL,
            difficulty TEXT NOT NULL,
            goal_type TEXT NOT NULL,
            equipment TEXT
        )
    ''')
    
    # Exercises table (for detailed workout plans)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            muscle_group TEXT NOT NULL,
            difficulty TEXT DEFAULT 'مبتدئ', -- مبتدئ, متوسط, متقدم
            sets INTEGER DEFAULT 3,
            reps INTEGER DEFAULT 12,
            calories_burned INTEGER DEFAULT 50,
            equipment TEXT DEFAULT 'وزن الجسم',
            goal_type TEXT DEFAULT 'general',
            description TEXT,
            video_url TEXT
        )
    ''')

    # User plans (meal and workout assignments)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            plan_id INTEGER,
            meal_ids TEXT,
            workout_ids TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (plan_id) REFERENCES plans (id)
        )
    ''')
    
    # Admin users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'trainer', -- admin, trainer
            full_name TEXT,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Enhanced exercises table for admin management
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_exercises (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name_en TEXT NOT NULL,
            name_ar TEXT NOT NULL,
            muscle_group TEXT NOT NULL, -- chest, back, legs, shoulders, arms, core, full_body
            equipment_type TEXT NOT NULL, -- bodyweight, dumbbells, machines, bands, barbell, kettlebell, cable
            difficulty_level TEXT NOT NULL, -- beginner, intermediate, advanced
            goal TEXT NOT NULL, -- weight_loss, muscle_gain, maintain, strength, endurance
            split_type TEXT NOT NULL, -- full_body, upper_lower, push_pull_legs, bro_split, crossfit, hiit
            sets INTEGER DEFAULT 3,
            reps TEXT DEFAULT '8-12', -- Can be range like '8-12' or '30 seconds'
            rest_time TEXT DEFAULT '60 ثانية', -- rest time description
            instructions TEXT,
            form_cues TEXT,
            common_mistakes TEXT,
            risk_notes TEXT,
            alternatives TEXT,
            video_url TEXT,
            image_url TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES admin_users (id)
        )
    ''')
    
    # Workout splits table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_splits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            type TEXT NOT NULL, -- full_body, upper_lower, push_pull_legs, bro_split, crossfit, hiit
            target_goal TEXT, -- weight_loss, muscle_gain, maintenance
            days_per_week INTEGER DEFAULT 3,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Exercise to workout split mapping
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exercise_split_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercise_id INTEGER,
            split_id INTEGER,
            day_number INTEGER, -- 1, 2, 3, etc.
            order_in_day INTEGER, -- Order of exercise in that day
            FOREIGN KEY (exercise_id) REFERENCES admin_exercises (id),
            FOREIGN KEY (split_id) REFERENCES workout_splits (id)
        )
    ''')
    
    # Motivational messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS motivational_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            category TEXT DEFAULT 'general', -- general, weight_loss, muscle_gain, maintenance
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Dashboard settings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dashboard_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT NOT NULL,
            setting_type TEXT DEFAULT 'string', -- string, boolean, integer, json
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_session_id TEXT,
            workout_generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            goal_type TEXT,
            fitness_level TEXT,
            workout_days INTEGER,
            user_weight REAL,
            user_height REAL,
            bmi REAL,
            ip_address TEXT
        )
    ''')
    
    # Workout plans table for smart plan generation
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workout_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            fitness_level TEXT NOT NULL,
            days_per_week INTEGER NOT NULL,
            weight REAL,
            height REAL,
            bmi REAL,
            plan_data TEXT NOT NULL, -- JSON data containing the complete workout plan
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    
    # تحديث هيكل قاعدة البيانات أولاً
    print("تحديث هيكل قاعدة البيانات...")
    update_database_schema()
    
    # التحقق من وجود بيانات في جدول الوجبات
    conn = sqlite3.connect('fitness_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM meals')
    meals_count = cursor.fetchone()[0]
    
    if meals_count == 0:
        print("جدول الوجبات فارغ، سيتم تحميل البيانات من ملف JSON")
        conn.close()
        load_data_from_json()
    else:
        print(f"قاعدة البيانات تحتوي على {meals_count} وجبة")
        conn.close()
    
    # Check and insert admin exercise data
    conn = sqlite3.connect('fitness_app.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM admin_exercises')
    exercises_count = cursor.fetchone()[0]
    
    if exercises_count == 0:
        print("إدراج بيانات التمارين الإدارية...")
        insert_admin_exercise_data(cursor)
        conn.commit()
        print("تم إدراج بيانات التمارين الإدارية بنجاح")
    else:
        print(f"قاعدة البيانات تحتوي على {exercises_count} تمرين إداري")
    
    # Check and insert comprehensive exercise data
    cursor.execute('SELECT COUNT(*) FROM exercises')
    comprehensive_exercises_count = cursor.fetchone()[0]
    
    if comprehensive_exercises_count == 0:
        print("إدراج بيانات التمارين الشاملة...")
        insert_comprehensive_exercise_data(cursor)
        conn.commit()
        print("تم إدراج بيانات التمارين الشاملة بنجاح")
    else:
        print(f"قاعدة البيانات تحتوي على {comprehensive_exercises_count} تمرين شامل")
    
    # Check and insert motivational messages
    cursor.execute('SELECT COUNT(*) FROM motivational_messages')
    messages_count = cursor.fetchone()[0]
    
    if messages_count == 0:
        print("إدراج الرسائل التحفيزية الافتراضية...")
        insert_default_motivational_messages(cursor)
        conn.commit()
        print("تم إدراج الرسائل التحفيزية بنجاح")
    else:
        print(f"قاعدة البيانات تحتوي على {messages_count} رسالة تحفيزية")
    
    # Check and insert dashboard settings
    cursor.execute('SELECT COUNT(*) FROM dashboard_settings')
    settings_count = cursor.fetchone()[0]
    
    if settings_count == 0:
        print("إدراج إعدادات لوحة التحكم الافتراضية...")
        insert_default_dashboard_settings(cursor)
        conn.commit()
        print("تم إدراج إعدادات لوحة التحكم بنجاح")
    else:
        print(f"قاعدة البيانات تحتوي على {settings_count} إعداد")
    
    conn.close()

def insert_admin_exercise_data(cursor):
    """Insert comprehensive admin exercise data"""
    admin_exercises_data = [
        # Chest Exercises
        ('Push-ups', 'تمرين الضغط', 'chest', 'bodyweight', 'beginner', 3, '8-15', 60, 
         'Start in plank position, lower body until chest nearly touches floor, push back up', 
         'Keep core tight, straight line from head to heels', 
         'Sagging hips, flaring elbows too wide', 
         'https://www.youtube.com/watch?v=IODxDxX7oi4', None, 1),
        
        ('Bench Press', 'تمرين البنش برس', 'chest', 'machines', 'intermediate', 4, '6-10', 90, 
         'Lie on bench, grip bar wider than shoulders, lower to chest, press up', 
         'Retract shoulder blades, feet flat on floor', 
         'Bouncing bar off chest, uneven grip', 
         'https://www.youtube.com/watch?v=rT7DgCr-3pg', None, 1),
        
        ('Incline Dumbbell Press', 'تمرين الضغط المائل بالدمبل', 'chest', 'dumbbells', 'intermediate', 3, '8-12', 75, 
         'Set bench to 30-45 degrees, press dumbbells from chest level upward', 
         'Control the weight, squeeze chest at top', 
         'Too steep incline, pressing too wide', 
         'https://www.youtube.com/watch?v=8iPEnn-ltC8', None, 1),
        
        # Back Exercises
        ('Pull-ups', 'تمرين العقلة', 'back', 'bodyweight', 'intermediate', 3, '5-10', 90, 
         'Hang from bar, pull body up until chin over bar, lower with control', 
         'Engage lats, avoid swinging', 
         'Using momentum, partial range of motion', 
         'https://www.youtube.com/watch?v=eGo4IYlbE5g', None, 1),
        
        ('Bent-over Rows', 'تمرين السحب المنحني', 'back', 'dumbbells', 'intermediate', 4, '8-12', 75, 
         'Hinge at hips, pull weights to lower ribs, squeeze shoulder blades', 
         'Keep back straight, pull elbows back', 
         'Rounding back, pulling to wrong area', 
         'https://www.youtube.com/watch?v=FWJR5Ve8bnQ', None, 1),
        
        ('Lat Pulldowns', 'تمرين السحب للأسفل', 'back', 'machines', 'beginner', 3, '10-15', 60, 
         'Sit at machine, pull bar to upper chest, control the return', 
         'Lean back slightly, squeeze lats', 
         'Pulling behind neck, using too much weight', 
         'https://www.youtube.com/watch?v=CAwf7n6Luuc', None, 1),
        
        # Leg Exercises
        ('Squats', 'تمرين السكوات', 'legs', 'bodyweight', 'beginner', 3, '12-20', 60, 
         'Stand with feet shoulder-width apart, lower hips back and down, return to standing', 
         'Keep chest up, knees track over toes', 
         'Knees caving in, not going deep enough', 
         'https://www.youtube.com/watch?v=YaXPRqUwItQ', None, 1),
        
        ('Lunges', 'تمرين الطعنات', 'legs', 'bodyweight', 'beginner', 3, '10-15', 60, 
         'Step forward, lower back knee toward ground, push back to start', 
         'Keep front knee over ankle, torso upright', 
         'Knee going past toes, leaning forward', 
         'https://www.youtube.com/watch?v=QOVaHwm-Q6U', None, 1),
        
        ('Deadlifts', 'تمرين الديد ليفت', 'legs', 'dumbbells', 'advanced', 4, '5-8', 120, 
         'Stand with feet hip-width, hinge at hips, lower weights, drive hips forward', 
         'Keep back straight, bar close to body', 
         'Rounding back, bar drifting away', 
         'https://www.youtube.com/watch?v=ytGaGIn3SjE', None, 1),
        
        # Shoulder Exercises
        ('Shoulder Press', 'تمرين الضغط العسكري', 'shoulders', 'dumbbells', 'intermediate', 3, '8-12', 75, 
         'Press weights overhead from shoulder level, lower with control', 
         'Keep core tight, press straight up', 
         'Arching back excessively, pressing forward', 
         'https://www.youtube.com/watch?v=qEwKCR5JCog', None, 1),
        
        ('Lateral Raises', 'تمرين الرفرفة الجانبية', 'shoulders', 'dumbbells', 'beginner', 3, '12-15', 45, 
         'Raise arms to sides until parallel to floor, lower slowly', 
         'Slight bend in elbows, control the movement', 
         'Using too much weight, swinging arms', 
         'https://www.youtube.com/watch?v=3VcKaXpzqRo', None, 1),
        
        # Arm Exercises
        ('Bicep Curls', 'تمرين الباي بالدمبل', 'arms', 'dumbbells', 'beginner', 3, '10-15', 45, 
         'Curl weights up by flexing biceps, lower slowly', 
         'Keep elbows at sides, squeeze at top', 
         'Swinging weights, using momentum', 
         'https://www.youtube.com/watch?v=ykJmrZ5v0Oo', None, 1),
        
        ('Tricep Dips', 'تمرين التراي بالكرسي', 'arms', 'bodyweight', 'intermediate', 3, '8-12', 60, 
         'Lower body by bending elbows, push back up', 
         'Keep elbows close to body, shoulders down', 
         'Flaring elbows, going too low', 
         'https://www.youtube.com/watch?v=6kALZikXxLc', None, 1),
        
        # Core Exercises
        ('Plank', 'تمرين البلانك', 'core', 'bodyweight', 'beginner', 3, '30-60 seconds', 60, 
         'Hold straight line from head to heels, engage core', 
         'Keep hips level, breathe normally', 
         'Sagging hips, holding breath', 
         'https://www.youtube.com/watch?v=ASdvN_XEl_c', None, 1),
        
        ('Crunches', 'تمرين البطن العادي', 'core', 'bodyweight', 'beginner', 3, '15-25', 45, 
         'Lift shoulders off ground by contracting abs, lower slowly', 
         'Keep lower back on ground, chin off chest', 
         'Pulling on neck, coming up too high', 
         'https://www.youtube.com/watch?v=Xyd_fa5zoEU', None, 1),
        
        ('Russian Twists', 'تمرين الروسي تويست', 'core', 'bodyweight', 'intermediate', 3, '20-30', 45, 
         'Sit with knees bent, lean back, rotate torso side to side', 
         'Keep chest up, engage core throughout', 
         'Moving too fast, not engaging core', 
         'https://www.youtube.com/watch?v=wkD8rjkodUI', None, 1),
        
        # Full Body Exercises
        ('Burpees', 'تمرين البربي', 'full_body', 'bodyweight', 'advanced', 3, '5-10', 90, 
         'Squat down, jump back to plank, do push-up, jump feet forward, jump up', 
         'Maintain form throughout, land softly', 
         'Rushing through movement, poor form', 
         'https://www.youtube.com/watch?v=auBLPXO8Fww', None, 1),
        
        ('Mountain Climbers', 'تمرين الماونتن كلايمبر', 'full_body', 'bodyweight', 'intermediate', 3, '20-30', 45, 
         'Start in plank, alternate bringing knees to chest rapidly', 
         'Keep hips level, maintain plank position', 
         'Bouncing hips, slowing down', 
         'https://www.youtube.com/watch?v=nmwgirgXLYM', None, 1)
    ]
    
    cursor.executemany('''
        INSERT INTO admin_exercises 
        (name_en, name_ar, muscle_group, equipment_type, difficulty_level, 
         sets, reps, rest_time, instructions, form_cues, common_mistakes, 
         video_url, image_url, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', admin_exercises_data)
    
    # Insert workout splits
    workout_splits_data = [
        ('Full Body Beginner', 'Complete workout targeting all major muscle groups', 'full_body', 'weight_loss', 3),
        ('Upper/Lower Split', 'Alternating upper and lower body workouts', 'upper_lower', 'muscle_gain', 4),
        ('Push/Pull/Legs', 'Classic 3-day split focusing on movement patterns', 'push_pull_legs', 'muscle_gain', 6),
        ('HIIT Fat Burner', 'High-intensity interval training for fat loss', 'hiit', 'weight_loss', 4),
        ('Strength Builder', 'Progressive overload program for strength', 'full_body', 'muscle_gain', 3)
    ]
    
    cursor.executemany('''
        INSERT INTO workout_splits (name, description, type, target_goal, days_per_week)
        VALUES (?, ?, ?, ?, ?)
    ''', workout_splits_data)

def insert_default_motivational_messages(cursor):
    """Insert default motivational messages"""
    motivational_messages = [
        ('مرحباً بك في رحلة التغيير!', 'كل خطوة تخطوها اليوم تقربك من هدفك. ابدأ الآن ولا تؤجل!', 'general', 1),
        ('قوتك أكبر من أعذارك', 'لا تدع الأعذار تقف في طريقك. أنت أقوى مما تعتقد!', 'general', 1),
        ('النجاح يحتاج صبر', 'النتائج لا تأتي بين ليلة وضحاها، لكن كل يوم تتمرن فيه يقربك من هدفك.', 'general', 1),
        ('حرق الدهون يبدأ الآن!', 'كل تمرين كارديو يحرق السعرات ويقربك من الوزن المثالي. استمر!', 'weight_loss', 1),
        ('تذكر: الحمية 70% والرياضة 30%', 'اهتم بطعامك بقدر اهتمامك بالتمرين لنتائج أفضل في فقدان الوزن.', 'weight_loss', 1),
        ('كل كيلو تفقده إنجاز!', 'لا تستهن بالتقدم البطيء. كل كيلو تفقده خطوة نحو صحة أفضل.', 'weight_loss', 1),
        ('العضلات تُبنى في المطبخ', 'البروتين هو صديقك الأول في بناء العضلات. تأكد من تناول ما يكفي!', 'muscle_gain', 1),
        ('الراحة جزء من التمرين', 'عضلاتك تنمو أثناء الراحة، لا تهمل النوم والاستشفاء.', 'muscle_gain', 1),
        ('الثقل التدريجي هو المفتاح', 'زد الأوزان تدريجياً لتحفيز نمو العضلات. تحدى نفسك كل أسبوع!', 'muscle_gain', 1),
        ('الاستمرارية أهم من الكمال', 'لا تتوقف إذا فاتك يوم. المهم أن تعود وتستمر في رحلتك.', 'maintenance', 1),
        ('صحتك استثمار طويل المدى', 'كل دقيقة تقضيها في التمرين استثمار في صحتك المستقبلية.', 'maintenance', 1),
        ('التوازن هو السر', 'امزج بين التمارين والتغذية الصحية والراحة للحصول على أفضل النتائج.', 'maintenance', 1)
    ]
    
    cursor.executemany('''
        INSERT INTO motivational_messages (title, message, category, is_active)
        VALUES (?, ?, ?, ?)
    ''', motivational_messages)

def insert_default_dashboard_settings(cursor):
    """Insert default dashboard settings"""
    default_settings = [
        ('show_performance_indicators', 'true', 'boolean', 'عرض مؤشرات الأداء في صفحة النتائج'),
        ('show_motivational_messages', 'true', 'boolean', 'عرض الرسائل التحفيزية'),
        ('show_exercise_videos', 'true', 'boolean', 'عرض فيديوهات التمارين'),
        ('default_workout_goal', 'general_fitness', 'string', 'الهدف الافتراضي للتمرين'),
        ('theme_mode', 'light', 'string', 'وضع الألوان (light/dark)'),
        ('primary_color', '#2563eb', 'string', 'اللون الأساسي للموقع'),
        ('secondary_color', '#10b981', 'string', 'اللون الثانوي للموقع'),
        ('max_workout_days', '7', 'integer', 'أقصى عدد أيام تمرين أسبوعياً'),
        ('min_workout_days', '2', 'integer', 'أقل عدد أيام تمرين أسبوعياً'),
        ('available_fitness_levels', '["beginner", "intermediate", "advanced"]', 'json', 'مستويات اللياقة المتاحة'),
        ('available_workout_splits', '["full_body", "upper_lower", "push_pull_legs"]', 'json', 'أنواع تقسيم التمارين المتاحة'),
        ('enable_statistics', 'true', 'boolean', 'تفعيل جمع الإحصائيات'),
        ('site_title', 'جسمي أحسن - خطط التمرين الذكية', 'string', 'عنوان الموقع'),
        ('contact_email', 'info@jismyahsan.com', 'string', 'البريد الإلكتروني للتواصل'),
        ('social_facebook', 'https://facebook.com/jismyahsan', 'string', 'رابط صفحة الفيسبوك'),
        ('social_instagram', 'https://instagram.com/jismyahsan', 'string', 'رابط صفحة الإنستغرام'),
        ('social_youtube', 'https://youtube.com/jismyahsan', 'string', 'رابط قناة اليوتيوب')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO dashboard_settings (setting_key, setting_value, setting_type, description)
        VALUES (?, ?, ?, ?)
    ''', default_settings)

def insert_comprehensive_exercise_data(cursor):
    """Insert comprehensive exercise data with all required columns"""
    comprehensive_exercises = [
        # Full Body Beginner Exercises for Weight Loss
        ('Push-ups', 'chest', 'beginner', 'weight_loss', 'full_body', 'bodyweight', 
         'https://www.youtube.com/watch?v=IODxDxX7oi4', 3, '8-15', 60,
         'A fundamental upper body exercise that targets chest, shoulders, and triceps while engaging the core.',
         'Avoid if you have wrist or shoulder injuries. Start with knee push-ups if regular push-ups are too difficult.',
         'Knee push-ups, wall push-ups, incline push-ups'),
        
        ('Bodyweight Squats', 'legs', 'beginner', 'weight_loss', 'full_body', 'bodyweight',
         'https://www.youtube.com/watch?v=YaXPRqUwItQ', 3, '12-20', 45,
         'Essential lower body exercise targeting quadriceps, glutes, and hamstrings.',
         'Avoid if you have knee injuries. Stop if you feel knee pain.',
         'Chair squats, wall sits, leg press'),
        
        ('Plank', 'core', 'beginner', 'weight_loss', 'full_body', 'bodyweight',
         'https://www.youtube.com/watch?v=ASdvN_XEl_c', 3, '30-60 seconds', 60,
         'Core strengthening exercise that also engages shoulders and glutes.',
         'Avoid if you have lower back problems. Keep hips level.',
         'Knee plank, wall plank, dead bug'),
        
        ('Jumping Jacks', 'full_body', 'beginner', 'weight_loss', 'full_body', 'bodyweight',
         'https://www.youtube.com/watch?v=c4DAnQ6DtF8', 3, '20-30', 30,
         'Cardiovascular exercise that burns calories and improves coordination.',
         'Avoid if you have joint problems. Land softly to reduce impact.',
         'Step touches, arm circles, marching in place'),
        
        ('Mountain Climbers', 'full_body', 'beginner', 'weight_loss', 'full_body', 'bodyweight',
         'https://www.youtube.com/watch?v=nmwgirgXLYM', 3, '15-25', 45,
         'High-intensity exercise combining cardio and core strengthening.',
         'Avoid if you have wrist or shoulder issues. Keep hips level.',
         'Slow mountain climbers, plank hold, knee-to-elbow'),
        
        ('Lunges', 'legs', 'beginner', 'weight_loss', 'full_body', 'bodyweight',
         'https://www.youtube.com/watch?v=QOVaHwm-Q6U', 3, '10-15', 60,
         'Unilateral leg exercise that improves balance and targets glutes and quads.',
         'Avoid if you have knee injuries. Keep front knee over ankle.',
         'Stationary lunges, step-ups, leg extensions'),
        
        # Intermediate Push/Pull/Legs for Muscle Gain
        ('Bench Press', 'chest', 'intermediate', 'muscle_gain', 'push', 'machines',
         'https://www.youtube.com/watch?v=rT7DgCr-3pg', 4, '6-10', 90,
         'Primary chest exercise for building upper body mass and strength.',
         'Use spotter for heavy weights. Avoid if you have shoulder impingement.',
         'Dumbbell press, push-ups, chest fly'),
        
        ('Pull-ups', 'back', 'intermediate', 'muscle_gain', 'pull', 'bodyweight',
         'https://www.youtube.com/watch?v=eGo4IYlbE5g', 4, '5-10', 90,
         'Compound exercise for building back width and bicep strength.',
         'Avoid if you have shoulder or elbow issues. Use assistance if needed.',
         'Lat pulldowns, assisted pull-ups, rows'),
        
        ('Deadlifts', 'legs', 'intermediate', 'muscle_gain', 'legs', 'dumbbells',
         'https://www.youtube.com/watch?v=ytGaGIn3SjE', 4, '5-8', 120,
         'King of exercises - targets posterior chain and builds overall strength.',
         'Avoid if you have lower back problems. Focus on proper form.',
         'Romanian deadlifts, hip thrusts, good mornings'),
        
        ('Shoulder Press', 'shoulders', 'intermediate', 'muscle_gain', 'push', 'dumbbells',
         'https://www.youtube.com/watch?v=qEwKCR5JCog', 3, '8-12', 75,
         'Primary shoulder exercise for building deltoid mass and strength.',
         'Avoid if you have shoulder impingement. Keep core tight.',
         'Lateral raises, front raises, pike push-ups'),
        
        ('Bent-over Rows', 'back', 'intermediate', 'muscle_gain', 'pull', 'dumbbells',
         'https://www.youtube.com/watch?v=FWJR5Ve8bnQ', 4, '8-12', 75,
         'Essential back exercise for building thickness and improving posture.',
         'Avoid if you have lower back issues. Keep back straight.',
         'Seated rows, T-bar rows, single-arm rows'),
        
        ('Squats', 'legs', 'intermediate', 'muscle_gain', 'legs', 'bodyweight',
         'https://www.youtube.com/watch?v=YaXPRqUwItQ', 4, '8-15', 90,
         'Fundamental leg exercise for building lower body mass and strength.',
         'Avoid if you have knee injuries. Go to comfortable depth.',
         'Leg press, goblet squats, wall sits'),
        
        # Advanced HIIT for Weight Loss
        ('Burpees', 'full_body', 'advanced', 'weight_loss', 'hiit', 'bodyweight',
         'https://www.youtube.com/watch?v=auBLPXO8Fww', 4, '5-10', 60,
         'Ultimate full-body exercise combining strength and cardio.',
         'High impact exercise. Avoid if you have joint problems.',
         'Modified burpees, squat thrusts, jumping jacks'),
        
        ('High Knees', 'full_body', 'advanced', 'weight_loss', 'hiit', 'bodyweight',
         'https://www.youtube.com/watch?v=8opcQdC-V-U', 4, '20-30', 30,
         'High-intensity cardio exercise that improves leg strength and endurance.',
         'High impact on knees. Land softly and maintain good posture.',
         'Marching in place, butt kicks, step-ups'),
        
        ('Jump Squats', 'legs', 'advanced', 'weight_loss', 'hiit', 'bodyweight',
         'https://www.youtube.com/watch?v=A-cFYWvaHr0', 3, '8-15', 60,
         'Explosive leg exercise that builds power and burns calories.',
         'High impact on knees and ankles. Land softly.',
         'Regular squats, squat pulses, calf raises'),
        
        # Upper/Lower Split Exercises
        ('Incline Dumbbell Press', 'chest', 'intermediate', 'muscle_gain', 'upper', 'dumbbells',
         'https://www.youtube.com/watch?v=8iPEnn-ltC8', 3, '8-12', 75,
         'Upper chest focused exercise for balanced chest development.',
         'Avoid if you have shoulder issues. Use moderate incline.',
         'Incline push-ups, chest fly, regular bench press'),
        
        ('Lat Pulldowns', 'back', 'beginner', 'muscle_gain', 'upper', 'machines',
         'https://www.youtube.com/watch?v=CAwf7n6Luuc', 3, '10-15', 60,
         'Beginner-friendly back exercise that mimics pull-up movement.',
         'Avoid pulling behind neck. Focus on lat engagement.',
         'Assisted pull-ups, seated rows, resistance band rows'),
        
        ('Leg Press', 'legs', 'beginner', 'muscle_gain', 'lower', 'machines',
         'https://www.youtube.com/watch?v=IZxyjW7MPJQ', 3, '12-20', 75,
         'Safe leg exercise that allows heavy loading with back support.',
         'Avoid locking knees completely. Keep feet flat.',
         'Squats, goblet squats, wall sits'),
        
        ('Romanian Deadlifts', 'legs', 'intermediate', 'muscle_gain', 'lower', 'dumbbells',
         'https://www.youtube.com/watch?v=jEy_czb3RKA', 3, '8-12', 90,
         'Hamstring and glute focused exercise with less lower back stress.',
         'Avoid if you have lower back issues. Keep weights close.',
         'Good mornings, hip thrusts, leg curls'),
        
        # Maintenance/General Fitness
        ('Walking Lunges', 'legs', 'beginner', 'maintenance', 'full_body', 'bodyweight',
         'https://www.youtube.com/watch?v=L8fvypPrzzs', 3, '10-15', 45,
         'Dynamic leg exercise that improves balance and coordination.',
         'Avoid if you have knee problems. Take controlled steps.',
         'Stationary lunges, step-ups, leg swings'),
        
        ('Tricep Dips', 'arms', 'intermediate', 'maintenance', 'upper', 'bodyweight',
         'https://www.youtube.com/watch?v=6kALZikXxLc', 3, '8-12', 60,
         'Bodyweight exercise targeting triceps and shoulders.',
         'Avoid if you have shoulder or wrist issues. Keep elbows close.',
         'Tricep push-ups, overhead press, resistance band extensions'),
        
        ('Bicycle Crunches', 'core', 'beginner', 'maintenance', 'full_body', 'bodyweight',
         'https://www.youtube.com/watch?v=9FGilxCbdz8', 3, '15-25', 45,
         'Core exercise that targets obliques and improves rotational strength.',
         'Avoid pulling on neck. Keep movements controlled.',
         'Regular crunches, Russian twists, dead bug'),
        
        # Time-Efficient Exercises for Busy People
        ('Kettlebell Swings', 'full_body', 'intermediate', 'weight_loss', 'hiit', 'dumbbells',
         'https://www.youtube.com/watch?v=YSxHifyI6s8', 3, '15-25', 60,
         'Explosive hip-hinge movement that burns calories and builds power.',
         'Avoid if you have lower back issues. Focus on hip drive.',
         'Hip thrusts, Romanian deadlifts, squat jumps'),
        
        ('Thrusters', 'full_body', 'advanced', 'weight_loss', 'hiit', 'dumbbells',
         'https://www.youtube.com/watch?v=L219ltL15zk', 3, '8-15', 75,
         'Compound movement combining squat and overhead press.',
         'Avoid if you have shoulder or knee issues. Use light weight initially.',
         'Squat to press, wall balls, goblet squats'),
        
        # Low Impact Alternatives
        ('Wall Push-ups', 'chest', 'beginner', 'maintenance', 'upper', 'bodyweight',
         'https://www.youtube.com/watch?v=R-9Moke-MvQ', 3, '10-20', 45,
         'Low-impact chest exercise perfect for beginners or those with limitations.',
         'Great for those with wrist or knee issues. Adjust distance for difficulty.',
         'Incline push-ups, chest press, resistance band chest fly'),
        
        ('Chair Squats', 'legs', 'beginner', 'maintenance', 'lower', 'bodyweight',
         'https://www.youtube.com/watch?v=t7Oj8-8rWdM', 3, '10-15', 60,
         'Assisted squat variation that builds confidence and strength.',
         'Perfect for those with balance or mobility issues.',
         'Wall sits, leg press, assisted squats'),
        
        ('Seated Rows', 'back', 'beginner', 'maintenance', 'upper', 'machines',
         'https://www.youtube.com/watch?v=UCXxvVItLoM', 3, '10-15', 60,
         'Back exercise with full support, great for beginners.',
         'Avoid if you have lower back issues. Keep chest up.',
         'Resistance band rows, bent-over rows, lat pulldowns')
    ]
    
    cursor.executemany('''
        INSERT OR REPLACE INTO exercises 
        (name, muscle_group, level, goal, split_type, equipment, video_url, 
         sets, reps, rest_time, description, risk_notes, alternatives)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', comprehensive_exercises)

def insert_sample_data(cursor):
    # Sample meals data with local image paths
    meals_data = [
        # Weight Loss Meals
        ('سلطة تونة بالخضار', 'breakfast', 280, 25, 15, 12, 'weight_loss', 'easy', '/static/images/meals/tuna_salad.jpg'),
        ('شوفان بالفواكه قليل السكر', 'breakfast', 320, 12, 50, 8, 'weight_loss', 'easy', '/static/images/meals/oatmeal.jpg'),
        ('بيض مسلوق مع خبز أسمر', 'breakfast', 250, 18, 20, 10, 'weight_loss', 'easy', '/static/images/meals/boiled_eggs.jpg'),
        ('فراخ مشوية مع سلطة خضراء', 'lunch', 380, 35, 10, 18, 'weight_loss', 'medium', '/static/images/meals/grilled_chicken.jpg'),
        ('سمك مشوي مع خضار سوتيه', 'lunch', 350, 30, 15, 16, 'weight_loss', 'medium', '/static/images/meals/grilled_fish.jpg'),
        ('شوربة عدس بدون خبز', 'lunch', 280, 18, 35, 6, 'weight_loss', 'easy', '/static/images/meals/lentil_soup.jpg'),
        ('زبادي يوناني مع خيار', 'dinner', 150, 15, 8, 6, 'weight_loss', 'easy', '/static/images/meals/greek_yogurt.jpg'),
        ('سلطة خضراء مع جبن قريش', 'dinner', 180, 20, 8, 8, 'weight_loss', 'easy', '/static/images/meals/green_salad.jpg'),
        ('تفاحة مع لوز', 'snack', 120, 3, 20, 6, 'weight_loss', 'easy', '/static/images/meals/apple_almonds.jpg'),
        ('جزر وخيار مع حمص', 'snack', 100, 4, 15, 3, 'weight_loss', 'easy', '/static/images/meals/vegetables_hummus.jpg'),
        
        # Muscle Gain Meals
        ('بيض مقلي مع أفوكادو وخبز', 'breakfast', 450, 20, 25, 28, 'muscle_gain', 'easy', '/static/images/meals/eggs_avocado.jpg'),
        ('شوفان بالموز واللوز والعسل', 'breakfast', 420, 15, 55, 15, 'muscle_gain', 'easy', '/static/images/meals/banana_oatmeal.jpg'),
        ('فول مدمس بالطحينة والسلطة', 'breakfast', 380, 18, 45, 16, 'muscle_gain', 'easy', '/static/images/meals/ful_medames.jpg'),
        ('أرز بالفراخ والخضار', 'lunch', 550, 40, 60, 18, 'muscle_gain', 'medium', '/static/images/meals/chicken_rice.jpg'),
        ('مكرونة بالتونة والطماطم', 'lunch', 480, 25, 65, 12, 'muscle_gain', 'medium', '/static/images/meals/pasta_tuna.jpg'),
        ('لحمة مشوية مع بطاطس مسلوقة', 'lunch', 520, 35, 45, 20, 'muscle_gain', 'medium', '/static/images/meals/grilled_meat.jpg'),
        ('زبادي بالفواكه والمكسرات', 'dinner', 280, 12, 35, 12, 'muscle_gain', 'easy', '/static/images/meals/yogurt_fruits.jpg'),
        ('جبنة مع خبز وطماطم', 'dinner', 320, 18, 30, 15, 'muscle_gain', 'easy', '/static/images/meals/cheese_bread.jpg'),
        ('مكسرات مشكلة', 'snack', 200, 6, 8, 16, 'muscle_gain', 'easy', '/static/images/meals/mixed_nuts.jpg'),
        ('موز مع زبدة الفول السوداني', 'snack', 250, 8, 30, 12, 'muscle_gain', 'easy', '/static/images/meals/banana_peanut.jpg')
    ]
    
    cursor.executemany('''
        INSERT INTO meals (name, category, calories, protein, carbs, fats, goal_type, difficulty, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', meals_data)
    
    # Sample workouts data
    workouts_data = [
        # Weight Loss Workouts
        ('المشي السريع', 'cardio', 30, 200, 'easy', 'weight_loss', 'none'),
        ('جري خفيف', 'cardio', 25, 250, 'medium', 'weight_loss', 'none'),
        ('تمارين الكارديو المنزلية', 'cardio', 20, 180, 'easy', 'weight_loss', 'none'),
        ('تمارين HIIT', 'cardio', 15, 220, 'hard', 'weight_loss', 'none'),
        ('تمارين البطن', 'strength', 15, 100, 'easy', 'weight_loss', 'mat'),
        ('تمارين الجسم الكامل', 'strength', 25, 150, 'medium', 'weight_loss', 'none'),
        
        # Muscle Gain Workouts
        ('تمارين الصدر والقف', 'strength', 45, 300, 'medium', 'muscle_gain', 'weights'),
        ('تمارين الظهر والباي', 'strength', 40, 280, 'medium', 'muscle_gain', 'weights'),
        ('تمارين الأرجل', 'strength', 50, 350, 'hard', 'muscle_gain', 'weights'),
        ('تمارين التراي والقف', 'strength', 35, 250, 'medium', 'muscle_gain', 'weights'),
        ('تمارين البطن والكور', 'strength', 20, 120, 'easy', 'muscle_gain', 'mat'),
        ('تمارين الكارديو الخفيف', 'cardio', 20, 150, 'easy', 'muscle_gain', 'none')
    ]
    
    cursor.executemany('''
        INSERT INTO workouts (name, category, duration, calories_burned, difficulty, goal_type, equipment)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', workouts_data)
    
    # Sample exercises data for detailed workout plans
    exercises_data = [
        # Upper Body Exercises
        ('تمرين الضغط', 'chest', 1, 3, 12, 60, 'none', 'general'),
        ('تمرين الضغط المائل', 'chest', 2, 3, 10, 80, 'none', 'muscle_gain'),
        ('تمرين البنش برس', 'chest', 2, 4, 8, 100, 'weights', 'muscle_gain'),
        ('تمرين العقلة', 'back', 2, 3, 8, 90, 'bar', 'muscle_gain'),
        ('تمرين السحب للأسفل', 'back', 1, 3, 12, 70, 'weights', 'general'),
        ('تمرين الرفرفة', 'shoulders', 1, 3, 15, 50, 'weights', 'general'),
        ('تمرين الضغط العسكري', 'shoulders', 2, 3, 10, 80, 'weights', 'muscle_gain'),
        ('تمرين الباي بالدمبل', 'biceps', 1, 3, 12, 40, 'weights', 'general'),
        ('تمرين التراي بالحبل', 'triceps', 1, 3, 12, 50, 'weights', 'general'),
        
        # Lower Body Exercises
        ('تمرين السكوات', 'legs', 1, 3, 15, 80, 'none', 'general'),
        ('تمرين السكوات بالوزن', 'legs', 2, 4, 12, 120, 'weights', 'muscle_gain'),
        ('تمرين الطعنات', 'legs', 1, 3, 12, 70, 'none', 'general'),
        ('تمرين الديد ليفت', 'legs', 3, 4, 6, 150, 'weights', 'muscle_gain'),
        ('تمرين رفع السمانة', 'calves', 1, 3, 20, 30, 'weights', 'general'),
        ('تمرين الجلوتس بريدج', 'glutes', 1, 3, 15, 60, 'none', 'general'),
        
        # Core Exercises
        ('تمرين البطن العادي', 'core', 1, 3, 20, 40, 'none', 'general'),
        ('تمرين البلانك', 'core', 1, 3, 60, 50, 'none', 'general'),
        ('تمرين الدراجة', 'core', 1, 3, 20, 60, 'none', 'weight_loss'),
        ('تمرين الروسي تويست', 'core', 2, 3, 15, 70, 'none', 'general'),
        
        # Cardio Exercises
        ('الجري في المكان', 'cardio', 1, 1, 300, 200, 'none', 'weight_loss'),
        ('تمرين الجامبينغ جاك', 'cardio', 1, 3, 30, 100, 'none', 'weight_loss'),
        ('تمرين البربي', 'cardio', 2, 3, 10, 120, 'none', 'weight_loss'),
        ('تمرين الماونتن كلايمبر', 'cardio', 2, 3, 20, 90, 'none', 'weight_loss')
    ]
    
    cursor.executemany('''
        INSERT INTO exercises (name, muscle_group, difficulty, sets, reps, calories_burned, equipment, goal_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', exercises_data)

def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def calculate_nutrition_plan(user_data):
    """
    Calculate personalized nutrition plan based on user data using Mifflin-St Jeor equation.
    
    Args:
        user_data (dict): Dictionary containing user information with keys:
                         weight, height, age, gender, activity_level, goal, target_weight
    
    Returns:
        dict: Comprehensive nutrition plan with calories, macros, percentages, and metrics
    """
    weight = user_data['weight']
    height = user_data['height']
    age = user_data['age']
    gender = user_data['gender']
    activity_level = user_data['activity_level']
    goal = user_data['goal']
    target_weight = user_data.get('target_weight', weight)
    
    # Calculate BMR using Mifflin-St Jeor equation (more accurate than Harris-Benedict)
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Activity multipliers for TDEE calculation
    activity_multipliers = {
        'sedentary': 1.2,      # Little to no exercise
        'light': 1.375,        # Light exercise 1-3 days/week
        'moderate': 1.55,      # Moderate exercise 3-5 days/week
        'active': 1.725,       # Heavy exercise 6-7 days/week
        'very_active': 1.9     # Very heavy exercise, physical job
    }
    
    # Calculate TDEE (Total Daily Energy Expenditure)
    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    
    # Adjust calories based on goal with evidence-based deficits/surpluses
    if goal == 'weight_loss':
        daily_calories = tdee - 500  # 500 calorie deficit for ~0.5kg/week loss
        protein_ratio = 0.35  # Higher protein for muscle preservation
        carbs_ratio = 0.35
        fats_ratio = 0.30
    elif goal == 'muscle_gain':
        daily_calories = tdee + 300  # 300 calorie surplus for lean gains
        protein_ratio = 0.30
        carbs_ratio = 0.45  # Higher carbs for performance and recovery
        fats_ratio = 0.25
    elif goal == 'body_recomp':
        daily_calories = tdee - 200  # Small deficit for body recomposition
        protein_ratio = 0.40  # Very high protein for muscle preservation
        carbs_ratio = 0.35
        fats_ratio = 0.25
    else:  # maintenance or general_fitness
        daily_calories = tdee
        protein_ratio = 0.25
        carbs_ratio = 0.45
        fats_ratio = 0.30
    
    # Ensure minimum calorie intake for safety
    min_calories = 1200 if gender == 'female' else 1500
    daily_calories = max(daily_calories, min_calories)
    
    # Calculate macronutrients in grams
    protein_grams = int((daily_calories * protein_ratio) / 4)  # 4 calories per gram
    carbs_grams = int((daily_calories * carbs_ratio) / 4)      # 4 calories per gram
    fats_grams = int((daily_calories * fats_ratio) / 9)        # 9 calories per gram
    
    # Calculate actual percentages based on calculated grams
    total_macro_calories = (protein_grams * 4) + (carbs_grams * 4) + (fats_grams * 9)
    protein_percentage = round((protein_grams * 4 / total_macro_calories) * 100, 1)
    carbs_percentage = round((carbs_grams * 4 / total_macro_calories) * 100, 1)
    fats_percentage = round((fats_grams * 9 / total_macro_calories) * 100, 1)
    
    # Calculate BMI and weight status
    height_meters = height / 100
    bmi = weight / (height_meters * height_meters)
    
    # Calculate water intake (35ml per kg body weight)
    water_intake_ml = weight * 35
    water_intake_liters = round(water_intake_ml / 1000, 1)
    
    # Estimate time to goal
    weight_difference = abs(weight - target_weight)
    
    if goal == 'weight_loss' and weight > target_weight:
        # Safe weight loss: 0.5-1 kg per week
        weeks_to_goal = int(weight_difference / 0.75)  # Conservative 0.75kg/week
    elif goal == 'muscle_gain' and weight < target_weight:
        # Muscle gain: 0.25-0.5 kg per month (mostly muscle)
        weeks_to_goal = int(weight_difference / 0.125)  # Very conservative
    else:
        weeks_to_goal = 12  # Standard 12-week program
    
    # Ensure reasonable timeframe
    weeks_to_goal = max(4, min(weeks_to_goal, 52))  # Between 4-52 weeks
    
    return {
        # Core nutrition data
        'daily_calories': int(daily_calories),
        'protein': protein_grams,
        'carbs': carbs_grams,
        'fats': fats_grams,
        
        # Percentage breakdowns
        'protein_percentage': protein_percentage,
        'carbs_percentage': carbs_percentage,
        'fats_percentage': fats_percentage,
        
        # Metabolic data
        'bmr': int(bmr),
        'tdee': int(tdee),
        'bmi': round(bmi, 1),
        
        # Additional metrics
        'water_intake': water_intake_liters,
        'weeks_to_goal': weeks_to_goal,
        
        # Goal-specific data
        'calorie_adjustment': int(daily_calories - tdee),
        'goal_type': goal,
        
        # Safety checks
        'is_safe_deficit': daily_calories >= min_calories,
        'min_calories_threshold': min_calories
    }

@app.route('/meal-generator', methods=['GET', 'POST'])
def meal_generator():
    if request.method == 'POST':
        # Get user preferences
        goal = request.form.get('goal', 'weight_loss')
        daily_calories = request.form.get('daily_calories')
        dietary_preference = request.form.get('dietary_preference', 'all')
        num_meals = int(request.form.get('num_meals', 4))  # 3-5 meals
        
        # Auto-estimate calories if not provided (TDEE calculation)
        if not daily_calories or daily_calories == '':
            # Basic estimation - you can enhance this with user data
            if goal == 'weight_loss':
                daily_calories = 1800
            elif goal == 'muscle_gain':
                daily_calories = 2500
            else:  # maintenance
                daily_calories = 2200
        else:
            daily_calories = int(daily_calories)
        
        # Generate personalized meal plan
        meal_plan = generate_smart_meal_plan(goal, daily_calories, num_meals)
        
        # Get smart health tips
        health_tips = get_smart_health_tips(goal, daily_calories)
        
        return jsonify({
            'success': True,
            'meal_plan': meal_plan,
            'health_tips': health_tips,
            'daily_calories': daily_calories,
            'goal': goal,
            'dietary_preference': dietary_preference,
            'num_meals': num_meals
        })
    
    return render_template('meal_generator.html')

def generate_smart_meal_plan(goal, daily_calories, num_meals):
    """Generate intelligent meal plan based on user preferences"""
    conn = get_db_connection()
    
    # Smart calorie distribution based on number of meals
    if num_meals == 3:
        distributions = {
            'breakfast': 0.30,
            'lunch': 0.40,
            'dinner': 0.30
        }
    elif num_meals == 4:
        distributions = {
            'breakfast': 0.25,
            'lunch': 0.35,
            'dinner': 0.30,
            'snack': 0.10
        }
    else:  # 5 meals
        distributions = {
            'breakfast': 0.20,
            'lunch': 0.30,
            'dinner': 0.25,
            'snack': 0.15,
            'snack2': 0.10
        }
    
    meal_plan = []
    
    for meal_type, calorie_ratio in distributions.items():
        target_calories = int(daily_calories * calorie_ratio)
        
        # Query meals with image_url
        query = '''
            SELECT id, name, category, calories, protein, carbs, fats, image_url
            FROM meals
            WHERE category = ?
            AND (goal_type = ? OR goal_type = 'all')
            AND calories BETWEEN ? AND ?
            ORDER BY RANDOM()
            LIMIT 1
        '''
        
        # Handle snack2 as snack
        search_type = 'snack' if meal_type.startswith('snack') else meal_type
        
        result = conn.execute(query, (
            search_type,
            goal,
            target_calories - 100,
            target_calories + 100
        )).fetchone()
        
        if result:
            # Use default image if no image_url or file doesn't exist
            image_url = result['image_url']
            if not image_url or not os.path.exists(f"static{image_url}"):
                image_url = f"/static/images/meals/default-{search_type}.jpg"
            
            meal_plan.append({
                'id': result['id'],
                'name': result['name'],
                'type': result['category'],
                'calories': result['calories'],
                'protein': result['protein'],
                'carbs': result['carbs'],
                'fats': result['fats'],
                'image_url': image_url,
                'target_calories': target_calories
            })
    
    conn.close()
    return meal_plan

def get_smart_health_tips(goal, daily_calories):
    """Generate smart health tips based on user input"""
    tips = []
    
    # Goal-based tips
    if goal == 'weight_loss':
        tips.append("💡 Stay hydrated and reduce sugary snacks to boost fat burning.")
        tips.append("🚶‍♀️ Add 30 minutes of walking after meals to enhance metabolism.")
    elif goal == 'muscle_gain':
        tips.append("💪 Add a protein source to every meal and eat post-workout.")
        tips.append("🥛 Consider a protein shake within 30 minutes after training.")
    else:  # maintenance
        tips.append("⚖️ Focus on balanced nutrition and consistent meal timing.")
        tips.append("🥗 Include colorful vegetables in every meal for optimal nutrients.")
    
    # Calorie-based warnings
    if daily_calories < 1200:
        tips.append("⚠️ Warning: Too few calories may cause muscle loss and slow metabolism.")
    elif daily_calories > 3000:
        tips.append("📊 High calorie intake - ensure you're active enough to utilize this energy.")
    
    return tips

def get_meal_tips(meal_name):
    """Get preparation tips for meals"""
    tips_database = {
        'سلطة تونة بالخضار': ['استخدم تونة بالماء بدلاً من الزيت', 'أضف الليمون للنكهة', 'يمكن تحضيرها مسبقاً'],
        'شوفان بالفواكه قليل السكر': ['انقع الشوفان ليلة كاملة', 'استخدم فواكه طازجة', 'أضف القرفة للطعم'],
        'فراخ مشوية مع سلطة خضراء': ['تبل الفراخ قبل الطبخ بساعة', 'اشوي على نار متوسطة', 'قدم مع الخضار الطازجة'],
        'default': ['اتبع التعليمات بعناية', 'استخدم مكونات طازجة', 'قدم فوراً بعد التحضير']
    }
    return tips_database.get(meal_name, tips_database['default'])

def get_personalized_tips(goal):
    """Get personalized nutrition and fitness tips based on user's goal"""
    tips = {
        'weight_loss': [
            {
                'icon': '💧',
                'title': 'اشرب الماء بكثرة',
                'description': 'اشرب 8-10 أكواب ماء يومياً لتحفيز الحرق وتقليل الشهية'
            },
            {
                'icon': '🥬',
                'title': 'أكثر من الألياف',
                'description': 'تناول الخضروات والفواكه الغنية بالألياف لتشعر بالشبع لفترة أطول'
            },
            {
                'icon': '⏰',
                'title': 'الثبات هو المفتاح',
                'description': 'التزم بخطتك الغذائية يومياً وتجنب الوجبات السريعة'
            }
        ],
        'muscle_gain': [
            {
                'icon': '🥩',
                'title': 'توقيت البروتين مهم',
                'description': 'تناول 20-30 جرام بروتين خلال 30 دقيقة بعد التمرين'
            },
            {
                'icon': '📈',
                'title': 'فائض السعرات',
                'description': 'تناول 300-500 سعرة إضافية يومياً لدعم نمو العضلات'
            },
            {
                'icon': '🏋️',
                'title': 'تمارين القوة',
                'description': 'مارس تمارين الأثقال 3-4 مرات أسبوعياً مع زيادة الأوزان تدريجياً'
            }
        ],
        'maintenance': [
            {
                'icon': '⚖️',
                'title': 'توازن السعرات',
                'description': 'حافظ على توازن بين السعرات المتناولة والمحروقة'
            },
            {
                'icon': '🍽️',
                'title': 'وجبات منتظمة',
                'description': 'تناول 3 وجبات رئيسية و2 وجبة خفيفة يومياً'
            },
            {
                'icon': '🚶',
                'title': 'نشاط يومي',
                'description': 'امش 30 دقيقة يومياً أو مارس أي نشاط بدني تحبه'
            }
        ]
    }
    
    return tips.get(goal, tips['maintenance'])

def get_motivational_message(goal):
    """Get motivational message based on user's goal"""
    messages = {
        'weight_loss': {
            'text': 'أنت على الطريق الصحيح! كل خطوة تقربك من هدفك 💪',
            'emoji': '🔥',
            'color': 'success'
        },
        'muscle_gain': {
            'text': 'العضلات تُبنى بالصبر والثبات! استمر وستحقق النتائج 🚀',
            'emoji': '💪',
            'color': 'primary'
        },
        'maintenance': {
            'text': 'الحفاظ على نمط حياة صحي هو استثمار في مستقبلك! 🌟',
            'emoji': '⚖️',
            'color': 'info'
        }
    }
    
    return messages.get(goal, messages['maintenance'])

def get_meal_icon(meal_type):
    """Get appropriate icon for meal type"""
    icons = {
        'breakfast': '🌅',
        'lunch': '☀️',
        'dinner': '🌙',
        'snack': '🍎'
    }
    return icons.get(meal_type, '🍽️')

def send_whatsapp_plan(phone_number, ai_plan_text, user_name):
    """Generate WhatsApp URL for sharing AI-generated personalized plan"""
    try:
        from urllib.parse import quote
        
        # Clean phone number
        phone_number = phone_number.replace('+', '').replace('-', '').replace(' ', '')
        
        # Create WhatsApp message with AI plan
        message = f"🎯 خطتي الشخصية من تطبيق جسمي أحسن\n\n{ai_plan_text}\n\n"
        message += "💪 تم إنشاء هذه الخطة بواسطة الذكاء الاصطناعي المتخصص في اللياقة البدنية والتغذية"
        
        # Create WhatsApp URL
        whatsapp_url = f"https://wa.me/{phone_number}?text={quote(message)}"
        
        return whatsapp_url
        
    except Exception as e:
        print(f"Error creating WhatsApp URL: {str(e)}")
        return None

# Add WhatsApp sharing function
@app.route('/share-meal-plan', methods=['POST'])
def share_meal_plan():
    """Share meal plan via WhatsApp"""
    try:
        meal_plan = request.json.get('meal_plan', [])
        phone_number = request.json.get('phone_number', '')
        
        if not phone_number:
            return jsonify({'success': False, 'message': 'رقم الهاتف مطلوب'})
        
        # Create WhatsApp message
        message = "🍽️ خطتي الغذائية المخصصة\n\n"
        
        for meal in meal_plan:
            message += f"{meal['type'].capitalize()}: {meal['name']}\n"
            message += f"السعرات: {meal['calories']} | البروتين: {meal['protein']}g\n\n"
        
        message += "تم إنشاؤها من تطبيق جسمي أحسن 💪"
        
        whatsapp_url = f"https://wa.me/{phone_number}?text={quote(message)}"
        
        return jsonify({
            'success': True,
            'whatsapp_url': whatsapp_url
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        })

# Add save meal plan function
@app.route('/save-meal-plan', methods=['POST'])
def save_meal_plan():
    """Save meal plan to user's profile"""
    try:
        meal_plan = request.json.get('meal_plan', [])
        user_name = request.json.get('user_name', 'مستخدم')
        
        # Here you would typically save to database
        # For now, just return success
        
        return jsonify({
            'success': True,
            'message': f'تم حفظ خطتك الغذائية بنجاح يا {user_name}! 🎉'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في الحفظ: {str(e)}'
        })



@app.route('/')
def index():
    form = WeightLossForm()
    return render_template('index.html', form=form)

@app.route('/weight-loss-guide')
def weight_loss_guide():
    """صفحة دليل فقدان الوزن التفاعلي"""
    return render_template('weight_loss_guide.html')

@app.route('/api/save-weight-loss-plan', methods=['POST'])
def save_weight_loss_plan():
    """حفظ خطة فقدان الوزن المخصصة"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['goal', 'workout', 'meals', 'habits']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'حقل {field} مطلوب'
                }), 400
        
        # حفظ البيانات في قاعدة البيانات
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        # إنشاء جدول خطط فقدان الوزن إذا لم يكن موجوداً
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weight_loss_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                goal TEXT NOT NULL,
                workout TEXT NOT NULL,
                meals TEXT NOT NULL,
                habits TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # إدراج البيانات
        cursor.execute('''
            INSERT INTO weight_loss_plans (goal, workout, meals, habits)
            VALUES (?, ?, ?, ?)
        ''', (
            data['goal'],
            data['workout'],
            json.dumps(data['meals']),
            json.dumps(data['habits'])
        ))
        
        conn.commit()
        plan_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'تم حفظ خطتك بنجاح',
            'plan_id': plan_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في الحفظ: {str(e)}'
        }), 500

def get_weight_status(bmi):
    """Get weight status based on BMI"""
    if bmi < 18.5:
        return "نحيف"
    elif bmi < 25:
        return "طبيعي"
    elif bmi < 30:
        return "زيادة وزن"
    else:
        return "سمنة"

@app.route('/workout-plans', methods=['GET', 'POST'])
def workout_plans():
    """صفحة خطط التمارين الذكية باستخدام نموذج Qwen 1.8B"""
    
    if request.method == 'POST':
        try:
            # الحصول على بيانات المستخدم من النموذج
            user_data = {
                'age': request.form.get('age', 25),
                'gender': request.form.get('gender', 'male'),
                'weight': request.form.get('weight', 70),
                'height': request.form.get('height', 170),
                'activity_level': request.form.get('activity_level', 'moderate'),
                'goal': request.form.get('goal', 'general_fitness'),
                'schedule': request.form.get('schedule', 'moderate'),
                'equipment': request.form.get('equipment', 'وزن الجسم'),
                'limitations': request.form.getlist('limitations'),
                'preferences': request.form.getlist('preferences')
            }
            
            # توليد خطة تمارين ذكية باستخدام نموذج Qwen
            ai_workout_plan = qwen_generator.generate_smart_workout_plan(user_data)
            
            # حساب إحصائيات الخطة
            total_workouts = sum(1 for day in ai_workout_plan if not day['is_rest_day'])
            total_exercises = sum(len(day['exercises']) for day in ai_workout_plan if not day['is_rest_day'])
            total_calories = sum(day.get('total_calories', 0) for day in ai_workout_plan)
            
            plan_stats = {
                'total_workouts': total_workouts,
                'total_exercises': total_exercises,
                'total_calories': total_calories,
                'rest_days': 7 - total_workouts
            }
            
            return render_template('workout_plans.html', 
                                 ai_plan=ai_workout_plan,
                                 plan_stats=plan_stats,
                                 user_data=user_data,
                                 ai_generated=True)
            
        except Exception as e:
            flash(f'حدث خطأ في توليد الخطة: {str(e)}', 'error')
            return render_template('workout_plans.html', ai_generated=False)
    
    # عرض النموذج للمرة الأولى
    return render_template('workout_plans.html', ai_generated=False)


# Add these calculator functions before the existing routes

@app.route('/calculators', methods=['GET', 'POST'])
def calculators():
    if request.method == 'POST':
        calculator_type = request.form.get('calculator_type')
        
        if calculator_type == 'bmi':
            return calculate_bmi()
        elif calculator_type == 'bmr':
            return calculate_bmr()
        elif calculator_type == 'tdee':
            return calculate_tdee()
        elif calculator_type == 'macros':
            return calculate_macros()
        elif calculator_type == 'ideal_weight':
            return calculate_ideal_weight()
        elif calculator_type == 'calorie_planner':
            return calculate_calorie_planner()
    
    return render_template('calculators.html')

def calculate_bmi():
    """Calculate BMI and provide recommendations"""
    try:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height')) / 100  # Convert cm to meters
        
        bmi = weight / (height * height)
        
        # BMI categories
        if bmi < 18.5:
            category = 'نقص في الوزن'
            category_en = 'Underweight'
            color = 'info'
            recommendation = 'يُنصح بزيادة الوزن تدريجياً من خلال نظام غذائي صحي وممارسة الرياضة'
        elif 18.5 <= bmi < 25:
            category = 'وزن طبيعي'
            category_en = 'Normal Weight'
            color = 'success'
            recommendation = 'وزنك مثالي! حافظ على نمط حياتك الصحي'
        elif 25 <= bmi < 30:
            category = 'زيادة في الوزن'
            category_en = 'Overweight'
            color = 'warning'
            recommendation = 'يُنصح بفقدان الوزن من خلال نظام غذائي متوازن وممارسة الرياضة'
        else:
            category = 'سمنة'
            category_en = 'Obese'
            color = 'danger'
            recommendation = 'يُنصح بشدة بفقدان الوزن واستشارة أخصائي تغذية'
        
        return jsonify({
            'success': True,
            'bmi': round(bmi, 1),
            'category': category,
            'category_en': category_en,
            'color': color,
            'recommendation': recommendation
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'الرجاء إدخال قيم صحيحة'
        })

def calculate_bmr():
    """Calculate Basal Metabolic Rate"""
    try:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        
        # Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        return jsonify({
            'success': True,
            'bmr': round(bmr),
            'recommendation': f'جسمك يحرق {round(bmr)} سعرة حرارية يومياً في حالة الراحة التامة'
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'الرجاء إدخال قيم صحيحة'
        })

def calculate_tdee():
    """Calculate Total Daily Energy Expenditure"""
    try:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        activity_level = request.form.get('activity_level')
        
        # Calculate BMR first
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # Activity multipliers
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        tdee = bmr * activity_multipliers.get(activity_level, 1.2)
        
        activity_names = {
            'sedentary': 'قليل الحركة',
            'light': 'نشاط خفيف',
            'moderate': 'نشاط متوسط',
            'active': 'نشيط',
            'very_active': 'نشيط جداً'
        }
        
        return jsonify({
            'success': True,
            'bmr': round(bmr),
            'tdee': round(tdee),
            'activity_name': activity_names.get(activity_level, 'غير محدد'),
            'recommendation': f'تحتاج إلى {round(tdee)} سعرة حرارية يومياً للحفاظ على وزنك الحالي'
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'الرجاء إدخال قيم صحيحة'
        })

def calculate_macros():
    """Calculate macronutrient distribution based on goal"""
    try:
        calories = float(request.form.get('calories'))
        goal = request.form.get('goal')
        
        # Macro ratios based on goal
        if goal == 'weight_loss':
            protein_ratio = 0.35
            carbs_ratio = 0.35
            fats_ratio = 0.30
            goal_name = 'تخسيس وحرق دهون'
        elif goal == 'muscle_gain':
            protein_ratio = 0.30
            carbs_ratio = 0.45
            fats_ratio = 0.25
            goal_name = 'بناء عضلات'
        elif goal == 'body_recomp':
            protein_ratio = 0.40
            carbs_ratio = 0.35
            fats_ratio = 0.25
            goal_name = 'تحسين تركيب الجسم'
        else:  # maintenance
            protein_ratio = 0.25
            carbs_ratio = 0.45
            fats_ratio = 0.30
            goal_name = 'الحفاظ على الوزن'
        
        # Calculate macros in grams
        protein_grams = round((calories * protein_ratio) / 4)
        carbs_grams = round((calories * carbs_ratio) / 4)
        fats_grams = round((calories * fats_ratio) / 9)
        
        return jsonify({
            'success': True,
            'goal_name': goal_name,
            'protein_grams': protein_grams,
            'carbs_grams': carbs_grams,
            'fats_grams': fats_grams,
            'protein_calories': protein_grams * 4,
            'carbs_calories': carbs_grams * 4,
            'fats_calories': fats_grams * 9,
            'recommendation': f'للوصول لهدف {goal_name}، وزع سعراتك كما هو موضح أعلاه'
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'الرجاء إدخال قيم صحيحة'
        })

def calculate_ideal_weight():
    """Calculate ideal weight range"""
    try:
        height = float(request.form.get('height'))
        gender = request.form.get('gender')
        
        height_m = height / 100
        
        # BMI range for normal weight (18.5 - 24.9)
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 24.9 * (height_m ** 2)
        
        # Hamwi formula for ideal weight
        if gender == 'male':
            ideal_hamwi = 48 + 2.7 * ((height - 152.4) / 2.54)
        else:
            ideal_hamwi = 45.5 + 2.2 * ((height - 152.4) / 2.54)
        
        return jsonify({
            'success': True,
            'min_weight': round(min_weight, 1),
            'max_weight': round(max_weight, 1),
            'ideal_weight': round(ideal_hamwi, 1),
            'recommendation': f'الوزن المثالي لطولك يتراوح بين {round(min_weight, 1)} - {round(max_weight, 1)} كجم'
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'الرجاء إدخال قيم صحيحة'
        })

def calculate_calorie_planner():
    """Calculate calorie deficit/surplus plan"""
    try:
        current_weight = float(request.form.get('current_weight'))
        target_weight = float(request.form.get('target_weight'))
        timeframe = int(request.form.get('timeframe'))  # weeks
        tdee = float(request.form.get('tdee'))
        
        weight_diff = target_weight - current_weight
        total_calories_needed = weight_diff * 7700  # 1kg = 7700 calories
        daily_calorie_change = total_calories_needed / (timeframe * 7)
        
        if weight_diff > 0:
            plan_type = 'زيادة الوزن'
            daily_calories = tdee + abs(daily_calorie_change)
            recommendation = f'تناول {round(daily_calories)} سعرة يومياً لزيادة {abs(weight_diff)} كجم في {timeframe} أسبوع'
        else:
            plan_type = 'فقدان الوزن'
            daily_calories = tdee - abs(daily_calorie_change)
            recommendation = f'تناول {round(daily_calories)} سعرة يومياً لفقدان {abs(weight_diff)} كجم في {timeframe} أسبوع'
        
        # Safety checks
        if daily_calories < 1200:
            daily_calories = 1200
            recommendation += '\n⚠️ تم تعديل السعرات لضمان الحد الأدنى الآمن (1200 سعرة)'
        elif daily_calories > tdee + 1000:
            daily_calories = tdee + 1000
            recommendation += '\n⚠️ تم تعديل السعرات لضمان زيادة آمنة (حد أقصى +1000 سعرة)'
        
        return jsonify({
            'success': True,
            'plan_type': plan_type,
            'daily_calories': round(daily_calories),
            'weekly_change': round(weight_diff / timeframe, 2),
            'calorie_change': round(abs(daily_calorie_change)),
            'recommendation': recommendation
        })
        
    except (ValueError, TypeError):
        return jsonify({
            'success': False,
            'message': 'الرجاء إدخال قيم صحيحة'
        })

@app.route('/tips')
def tips():
    """Tips page with daily fitness and nutrition tips"""
    
    # Sample tips data organized by categories
    tips_data = {
        'workout': [
            {
                'id': 1,
                'title': 'ابدأ بالإحماء دائماً',
                'description': 'الإحماء لمدة 5-10 دقائق يقلل من خطر الإصابة ويحسن الأداء',
                'category': 'تمارين',
                'icon': 'fas fa-fire',
                'image': '/static/images/tips/warmup.svg',
                'full_content': 'الإحماء ضروري قبل أي تمرين لتحضير العضلات والمفاصل. يساعد على زيادة تدفق الدم وتحسين المرونة.',
                'is_tip_of_day': False
            },
            {
                'id': 2,
                'title': 'تمرن 3-4 مرات أسبوعياً',
                'description': 'الانتظام أهم من الشدة - ابدأ بجدول بسيط والتزم به',
                'category': 'تمارين',
                'icon': 'fas fa-calendar-alt',
                'image': '/static/images/tips/schedule.svg',
                'full_content': 'الثبات على جدول تمارين منتظم أهم من التمرن بشدة عالية بشكل متقطع. ابدأ بـ 3 أيام في الأسبوع.',
                'is_tip_of_day': False
            },
            {
                'id': 3,
                'title': 'اشرب مياه أثناء التمرين',
                'description': 'حافظ على ترطيب جسمك لتحسين الأداء ومنع التعب',
                'category': 'تمارين',
                'icon': 'fas fa-tint',
                'image': '/static/images/tips/hydration.svg',
                'full_content': 'شرب الماء أثناء التمرين يحافظ على مستوى الطاقة ويمنع الجفاف الذي يؤثر على الأداء.',
                'is_tip_of_day': True
            },
            {
                'id': 4,
                'title': 'استمع لجسمك',
                'description': 'خذ راحة عند الشعور بالألم أو التعب الشديد',
                'category': 'تمارين',
                'icon': 'fas fa-heart',
                'image': '/static/images/tips/listen_body.svg',
                'full_content': 'جسمك يرسل إشارات مهمة. الألم الحاد أو التعب المفرط علامات على ضرورة أخذ راحة.',
                'is_tip_of_day': False
            }
        ],
        'nutrition': [
            {
                'id': 5,
                'title': 'اشرب 8 أكواب مياه يومياً',
                'description': 'الماء ضروري لحرق الدهون وتحسين عملية الهضم',
                'category': 'تغذية',
                'icon': 'fas fa-glass-water',
                'image': '/static/images/tips/water.svg',
                'full_content': 'شرب كمية كافية من الماء يساعد في عملية الأيض وحرق الدهون وتحسين وظائف الجسم.',
                'is_tip_of_day': False
            },
            {
                'id': 6,
                'title': 'تناول البروتين في كل وجبة',
                'description': 'البروتين يساعد في بناء العضلات والشعور بالشبع',
                'category': 'تغذية',
                'icon': 'fas fa-drumstick-bite',
                'image': '/static/images/tips/protein.svg',
                'full_content': 'البروتين ضروري لبناء وإصلاح العضلات، كما يساعد في الشعور بالشبع لفترة أطول.',
                'is_tip_of_day': False
            },
            {
                'id': 7,
                'title': 'تناول الخضروات الملونة',
                'description': 'الألوان المختلفة تعني فيتامينات ومعادن متنوعة',
                'category': 'تغذية',
                'icon': 'fas fa-carrot',
                'image': '/static/images/tips/vegetables.svg',
                'full_content': 'الخضروات الملونة غنية بالفيتامينات والمعادن ومضادات الأكسدة المهمة للصحة.',
                'is_tip_of_day': False
            },
            {
                'id': 8,
                'title': 'تجنب السكر المضاف',
                'description': 'قلل من المشروبات الغازية والحلويات المصنعة',
                'category': 'تغذية',
                'icon': 'fas fa-ban',
                'image': '/static/images/tips/no_sugar.svg',
                'full_content': 'السكر المضاف يزيد من السعرات الحرارية دون فائدة غذائية ويؤثر على مستوى السكر في الدم.',
                'is_tip_of_day': False
            }
        ],
        'motivation': [
            {
                'id': 9,
                'title': 'ضع أهدافاً قابلة للتحقيق',
                'description': 'الأهداف الصغيرة تؤدي إلى نجاحات كبيرة',
                'category': 'تحفيز',
                'icon': 'fas fa-target',
                'image': '/static/images/tips/goals.svg',
                'full_content': 'تحديد أهداف صغيرة وقابلة للتحقيق يزيد من الثقة بالنفس ويحفز على الاستمرار.',
                'is_tip_of_day': False
            },
            {
                'id': 10,
                'title': 'احتفل بإنجازاتك',
                'description': 'كافئ نفسك عند تحقيق الأهداف الصغيرة',
                'category': 'تحفيز',
                'icon': 'fas fa-trophy',
                'image': '/static/images/tips/celebrate.svg',
                'full_content': 'الاحتفال بالإنجازات الصغيرة يعزز الدافعية ويجعل الرحلة أكثر متعة.',
                'is_tip_of_day': False
            },
            {
                'id': 11,
                'title': 'ابحث عن شريك تمرين',
                'description': 'التمرن مع صديق يزيد من الالتزام والمتعة',
                'category': 'تحفيز',
                'icon': 'fas fa-users',
                'image': '/static/images/tips/workout_partner.svg',
                'full_content': 'وجود شريك تمرين يزيد من الالتزام والمساءلة ويجعل التمرين أكثر متعة.',
                'is_tip_of_day': False
            },
            {
                'id': 12,
                'title': 'تذكر لماذا بدأت',
                'description': 'اكتب أهدافك واقرأها عند فقدان الدافعية',
                'category': 'تحفيز',
                'icon': 'fas fa-lightbulb',
                'image': '/static/images/tips/why.svg',
                'full_content': 'تذكر الأسباب التي دفعتك للبدء في رحلة اللياقة يساعد في استعادة الدافعية.',
                'is_tip_of_day': False
            }
        ],
        'recovery': [
            {
                'id': 13,
                'title': 'نم 7-9 ساعات يومياً',
                'description': 'النوم الكافي ضروري لاستشفاء العضلات وحرق الدهون',
                'category': 'استشفاء',
                'icon': 'fas fa-bed',
                'image': '/static/images/tips/sleep.svg',
                'full_content': 'النوم الجيد ضروري لإصلاح العضلات وإفراز هرمونات النمو وتنظيم الشهية.',
                'is_tip_of_day': False
            },
            {
                'id': 14,
                'title': 'خذ يوم راحة أسبوعياً',
                'description': 'الراحة جزء مهم من برنامج التمرين',
                'category': 'استشفاء',
                'icon': 'fas fa-pause',
                'image': '/static/images/tips/rest_day.svg',
                'full_content': 'أيام الراحة تسمح للعضلات بالاستشفاء والنمو وتمنع الإرهاق والإصابات.',
                'is_tip_of_day': False
            },
            {
                'id': 15,
                'title': 'مارس تمارين الإطالة',
                'description': 'الإطالة تحسن المرونة وتقلل من توتر العضلات',
                'category': 'استشفاء',
                'icon': 'fas fa-expand-arrows-alt',
                'image': '/static/images/tips/stretching.svg',
                'full_content': 'تمارين الإطالة تحسن المرونة وتقلل من توتر العضلات وتساعد في الاسترخاء.',
                'is_tip_of_day': False
            },
            {
                'id': 16,
                'title': 'استمع للموسيقى المهدئة',
                'description': 'الاسترخاء يساعد في تقليل هرمونات التوتر',
                'category': 'استشفاء',
                'icon': 'fas fa-music',
                'image': '/static/images/tips/music.svg',
                'full_content': 'الاسترخاء والموسيقى المهدئة تساعد في تقليل التوتر وتحسين جودة النوم.',
                'is_tip_of_day': False
            }
        ]
    }
    
    # Get tip of the day (randomly or based on date)
    import random
    all_tips = []
    for category_tips in tips_data.values():
        all_tips.extend(category_tips)
    
    # Find tip of the day or select random one
    tip_of_day = next((tip for tip in all_tips if tip.get('is_tip_of_day')), random.choice(all_tips))
    
    return render_template('tips.html', tips_data=tips_data, tip_of_day=tip_of_day)

@app.route('/supplements')
def supplements():
    return render_template('supplements.html')



# إضافة هذا الاستيراد في أعلى الملف
import json
import os

# دالة لقراءة ملف JSON وإدراج البيانات
def load_meals_from_json(json_file_path):
    """Load meals from JSON file and insert into database"""
    try:
        # التحقق من وجود الملف
        if not os.path.exists(json_file_path):
            print(f"ملف JSON غير موجود: {json_file_path}")
            return False
        
        # قراءة ملف JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            meals_data = json.load(file)
        
        # الاتصال بقاعدة البيانات
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # عداد للوجبات المضافة
        added_count = 0
        
        # إدراج كل وجبة في قاعدة البيانات
        for meal in meals_data:
            try:
                # التحقق من عدم وجود الوجبة مسبقاً
                cursor.execute('SELECT id FROM meals WHERE name = ?', (meal['meal_name'],))
                if cursor.fetchone() is None:
                    # إدراج الوجبة الجديدة
                    cursor.execute('''
                        INSERT INTO meals (name, category, calories, protein, carbs, fats, goal_type, difficulty, image_url)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        meal['meal_name'],
                        meal['meal_type'],
                        meal['calories'],
                        meal['protein'],
                        meal['carbs'],
                        meal['fats'],
                        meal['goal'],
                        meal.get('difficulty', 'medium'),
                        meal.get('image_url', '')
                    ))
                    added_count += 1
                    print(f"تم إضافة الوجبة: {meal['meal_name']}")
                else:
                    print(f"الوجبة موجودة مسبقاً: {meal['meal_name']}")
                    
            except Exception as e:
                print(f"خطأ في إضافة الوجبة {meal.get('meal_name', 'غير معروف')}: {str(e)}")
                continue
        
        # حفظ التغييرات
        conn.commit()
        conn.close()
        
        print(f"تم إضافة {added_count} وجبة جديدة إلى قاعدة البيانات")
        return True
        
    except json.JSONDecodeError as e:
        print(f"خطأ في قراءة ملف JSON: {str(e)}")
        return False
    except Exception as e:
        print(f"خطأ عام: {str(e)}")
        return False

# دالة لتحديث قاعدة البيانات من ملف JSON
def update_meals_from_json():
    """Update meals database from JSON file"""
    json_file_path = 'meals_data.json'
    return load_meals_from_json(json_file_path)

# إضافة route جديد لتحديث الوجبات
@app.route('/admin/update-meals', methods=['POST'])
def admin_update_meals():
    """Admin endpoint to update meals from JSON"""
    try:
        success = update_meals_from_json()
        if success:
            return jsonify({
                'success': True,
                'message': 'تم تحديث قاعدة بيانات الوجبات بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'فشل في تحديث قاعدة البيانات'
            }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ: {str(e)}'
        }), 500

@app.route('/admin/fix-database')
def fix_database():
    """Fix database schema issues"""
    try:
        update_database_schema()
        return jsonify({
            'success': True,
            'message': 'تم إصلاح قاعدة البيانات بنجاح'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في إصلاح قاعدة البيانات: {str(e)}'
        }), 500

@app.route('/admin/upload-images')
def admin_upload_images():
    return render_template('admin_upload_images.html')

@app.route('/api/meals')
def api_meals():
    """Get all meals for dropdown"""
    conn = get_db_connection()
    meals = conn.execute('SELECT id, name FROM meals ORDER BY name').fetchall()
    conn.close()
    
    return jsonify({
        'success': True,
        'meals': [{'id': meal['id'], 'name': meal['name']} for meal in meals]
    })

@app.route('/admin/upload-meal-image', methods=['POST'])
def upload_meal_image():
    """Upload image for a specific meal"""
    try:
        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'لم يتم اختيار صورة'})
        
        file = request.files['image']
        meal_id = request.form.get('meal_id')
        
        if file.filename == '':
            return jsonify({'success': False, 'message': 'لم يتم اختيار صورة'})
        
        if not meal_id:
            return jsonify({'success': False, 'message': 'يجب اختيار وجبة'})
        
        if file and allowed_file(file.filename):
            # Create upload directory if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Generate secure filename
            filename = secure_filename(file.filename)
            # Add meal_id to filename to avoid conflicts
            name, ext = os.path.splitext(filename)
            filename = f"meal_{meal_id}_{name}{ext}"
            
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Resize image to optimize size
            resize_image(file_path)
            
            # Update database with image path
            conn = get_db_connection()
            image_url = f"/static/images/meals/{filename}"
            conn.execute(
                'UPDATE meals SET image_url = ? WHERE id = ?',
                (image_url, meal_id)
            )
            conn.commit()
            conn.close()
            
            return jsonify({
                'success': True,
                'message': 'تم رفع الصورة بنجاح',
                'image_url': image_url
            })
        else:
            return jsonify({'success': False, 'message': 'نوع الملف غير مدعوم'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'حدث خطأ: {str(e)}'})


def get_personalized_meals(user_data, nutrition_plan):
    """Generate personalized meal plan based on user data and nutrition requirements with enhanced Arabic data"""
    try:
        conn = get_db_connection()
        
        # الحصول على الوجبات مع البيانات الجديدة
        meals = conn.execute('''
            SELECT name, category, calories, protein, carbs, fats, food_preference, goal_type
            FROM meals 
            WHERE goal_type IN (?, 'general') 
            ORDER BY calories
        ''', (user_data['goal'],)).fetchall()
        
        conn.close()
        
        if not meals:
            return {}
        
        # حساب السعرات المطلوبة لكل وجبة
        daily_calories = nutrition_plan['daily_calories']
        breakfast_calories = daily_calories * 0.25  # 25%
        lunch_calories = daily_calories * 0.35      # 35%
        dinner_calories = daily_calories * 0.30     # 30%
        snack_calories = daily_calories * 0.10      # 10%
        
        # اختيار أفضل وجبة لكل فئة مع البيانات المحسنة
        selected_meals = {
            'breakfast': select_best_meal_enhanced(meals, 'breakfast', breakfast_calories),
            'lunch': select_best_meal_enhanced(meals, 'lunch', lunch_calories),
            'dinner': select_best_meal_enhanced(meals, 'dinner', dinner_calories),
            'snack': select_best_meal_enhanced(meals, 'snack', snack_calories)
        }
        
        return selected_meals
        
    except Exception as e:
        print(f"Error in get_personalized_meals: {str(e)}")
        return {}

def select_best_meal_enhanced(meals, category, target_calories):
    """Select the best meal for a category based on target calories with enhanced data"""
    # تصفية الوجبات حسب الفئة
    category_meals = [meal for meal in meals if meal[1].lower() == category.lower()]
    
    if not category_meals:
        # إذا لم توجد وجبات في الفئة المحددة، اختر أي وجبة قريبة من السعرات المطلوبة
        category_meals = meals
    
    # العثور على الوجبة الأقرب للسعرات المطلوبة
    best_meal = min(category_meals, key=lambda x: abs(x[2] - target_calories))
    
    # إرجاع البيانات المحسنة
    return {
        'name': best_meal[0],
        'category': best_meal[1],
        'calories': best_meal[2],
        'protein': best_meal[3],
        'carbs': best_meal[4],
        'fats': best_meal[5],
        'food_preference': best_meal[6] or 'عام',
        'goal_type': best_meal[7]
    }

def get_personalized_workouts(user_data):
    """Generate personalized workout plan based on user data with enhanced Arabic data"""
    try:
        conn = get_db_connection()
        
        # تحديد مستوى الصعوبة بناءً على مستوى النشاط
        activity_level = user_data.get('activity_level', 'low')
        if activity_level == 'low':
            difficulty = 1  # مبتدئ
        elif activity_level == 'moderate':
            difficulty = 2  # متوسط
        else:
            difficulty = 3  # متقدم
        
        # الحصول على التمارين المناسبة مع البيانات الجديدة
        exercises = conn.execute('''
            SELECT name, muscle_group, difficulty, difficulty_text, sets, reps, 
                   calories_burned, equipment, description, video_url
            FROM exercises 
            WHERE difficulty <= ? 
            ORDER BY RANDOM() 
            LIMIT 15
        ''', (difficulty,)).fetchall()
        
        conn.close()
        
        if not exercises:
            return []
        
        # تنظيم التمارين في خطة أسبوعية
        workout_plan = []
        days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
        
        # توزيع التمارين على الأيام
        exercises_per_day = 3
        for i, day in enumerate(days):
            if i == 6:  # يوم الراحة
                workout_plan.append({
                    'day': day,
                    'workout_type': 'rest',
                    'exercises': [],
                    'is_rest_day': True,
                    'total_calories': 0
                })
            else:
                day_exercises = []
                start_idx = (i * exercises_per_day) % len(exercises)
                
                for j in range(exercises_per_day):
                    exercise_idx = (start_idx + j) % len(exercises)
                    exercise = exercises[exercise_idx]
                    
                    day_exercises.append({
                        'name': exercise[0],
                        'muscle_group': exercise[1],
                        'difficulty': exercise[3] or 'مبتدئ',  # استخدام difficulty_text
                        'sets': exercise[4],
                        'reps': exercise[5],
                        'calories_burned': exercise[6],
                        'equipment': exercise[7],
                        'description': exercise[8] or 'لا يوجد وصف متاح',
                        'video_url': exercise[9] or ''
                    })
                
                total_calories = sum(ex['calories_burned'] for ex in day_exercises)
                
                workout_plan.append({
                    'day': day,
                    'workout_type': f'day_{i+1}',
                    'exercises': day_exercises,
                    'is_rest_day': False,
                    'total_calories': total_calories
                })
        
        return workout_plan
        
    except Exception as e:
        print(f"Error in get_personalized_workouts: {str(e)}")
        return []

def get_difficulty_level(experience):
    """Convert experience level to difficulty number"""
    levels = {
        'beginner': 1,
        'intermediate': 2,
        'advanced': 3
    }
    return levels.get(experience.lower(), 1)

def generate_weekly_workout_plan(exercises_list, available_days, user_data):
    """Generate a weekly workout plan based on available days and user goals"""
    goal = user_data.get('goal', 'general_fitness').lower()
    
    # Define workout splits based on available days
    if available_days <= 2:
        # Full body workouts
        workout_split = ['full_body'] * available_days
    elif available_days == 3:
        # Upper/Lower/Full body
        workout_split = ['upper_body', 'lower_body', 'full_body']
    elif available_days == 4:
        # Upper/Lower/Upper/Lower
        workout_split = ['upper_body', 'lower_body', 'upper_body', 'lower_body']
    elif available_days == 5:
        # Push/Pull/Legs/Upper/Lower
        workout_split = ['push', 'pull', 'legs', 'upper_body', 'lower_body']
    else:
        # 6+ days: Push/Pull/Legs/Push/Pull/Legs
        workout_split = ['push', 'pull', 'legs', 'push', 'pull', 'legs'][:available_days]
    
    weekly_plan = []
    
    for day_num, workout_type in enumerate(workout_split, 1):
        day_exercises = select_exercises_for_workout_type(exercises_list, workout_type, goal)
        
        weekly_plan.append({
            'day': day_num,
            'workout_type': workout_type,
            'exercises': day_exercises[:6]  # Limit to 6 exercises per day
        })
    
    return weekly_plan

def select_exercises_for_workout_type(exercises_list, workout_type, goal):
    """Select appropriate exercises for a specific workout type"""
    muscle_groups = {
        'upper_body': ['chest', 'back', 'shoulders', 'arms', 'biceps', 'triceps'],
        'lower_body': ['legs', 'glutes', 'quadriceps', 'hamstrings', 'calves'],
        'push': ['chest', 'shoulders', 'triceps'],
        'pull': ['back', 'biceps'],
        'legs': ['legs', 'glutes', 'quadriceps', 'hamstrings', 'calves'],
        'full_body': ['chest', 'back', 'shoulders', 'arms', 'legs', 'core']
    }
    
    target_muscles = muscle_groups.get(workout_type, ['chest', 'back', 'legs'])
    
    # Filter exercises by target muscle groups
    suitable_exercises = []
    for exercise in exercises_list:
        muscle_group = exercise.get('muscle_group', '').lower()
        if any(muscle in muscle_group for muscle in target_muscles):
            suitable_exercises.append(exercise)
    
    # If goal is weight loss, prioritize compound movements and cardio
    if 'weight_loss' in goal or 'fat_loss' in goal:
        suitable_exercises.sort(key=lambda x: x.get('calories_burned', 0), reverse=True)
    
    # Shuffle to add variety
    import random
    random.shuffle(suitable_exercises)
    
    return suitable_exercises

def generate_ai_personalized_plan(user_data):
    """Generate a comprehensive AI-powered personalized plan in Arabic with enhanced data from arabic_fitness_data.json"""
    try:
        # Calculate nutrition plan
        nutrition_plan = calculate_nutrition_plan(user_data)
        
        # Get personalized meals and workouts with enhanced data
        meals = get_personalized_meals(user_data, nutrition_plan)
        workouts = get_personalized_workouts(user_data)
        
        # Generate personalized tips
        tips = get_personalized_tips(user_data['goal'])
        
        # Calculate weight difference and timeline
        weight_diff = abs(float(user_data.get('current_weight', 70)) - float(user_data.get('target_weight', 65)))
        timeline_weeks = max(4, int(weight_diff * 2))  # Realistic timeline
        
        # Create comprehensive plan with card-style HTML formatting
        plan_text = f"""<div class="personalized-plan-container">
    <div class="plan-header">
        <h2 class="plan-title">🎯 خطتك الشخصية المتطورة</h2>
        <p style="margin: 0; font-size: 1.1rem; opacity: 0.9;">مرحباً {user_data['name']}! 👋</p>
    </div>
    
    <div class="plan-section goal-info">
        <h3 class="section-title">🔥 هدفك</h3>
        <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">
            {get_goal_arabic(user_data['goal'])} {weight_diff:.0f} كجم خلال {timeline_weeks} أسبوع
        </p>
    </div>
    
    <div class="plan-section nutrition-summary">
        <h3 class="section-title">🥗 ملخص التغذية اليومي</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; margin-top: 1rem;">
            <div style="text-align: center; background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: 900; color: #059669;">{nutrition_plan['daily_calories']}</div>
                <div style="font-size: 0.9rem; color: #6b7280;">سعرة حرارية</div>
            </div>
            <div style="text-align: center; background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: 900; color: #dc2626;">{nutrition_plan['protein']}g</div>
                <div style="font-size: 0.9rem; color: #6b7280;">بروتين</div>
            </div>
            <div style="text-align: center; background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: 900; color: #d97706;">{nutrition_plan['carbs']}g</div>
                <div style="font-size: 0.9rem; color: #6b7280;">كربوهيدرات</div>
            </div>
            <div style="text-align: center; background: rgba(255,255,255,0.8); padding: 1rem; border-radius: 8px;">
                <div style="font-size: 1.5rem; font-weight: 900; color: #7c3aed;">{nutrition_plan['fats']}g</div>
                <div style="font-size: 0.9rem; color: #6b7280;">دهون</div>
            </div>
        </div>
    </div>
    
    <div class="plan-section workout-schedule">
        <h3 class="section-title">💪 برنامج التمارين الأسبوعي</h3>"""
        
        # Add workout schedule with enhanced data formatting
        workout_days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
        for i, workout_day in enumerate(workouts[:3], 1):  # Limit to 3 days
            day_name = workout_days[i-1] if i <= len(workout_days) else f"اليوم {i}"
            
            if workout_day.get('is_rest_day'):
                plan_text += f"""
        <div class="workout-day">
            <strong>📅 {day_name}:</strong> يوم راحة 😴
        </div>"""
            else:
                exercises_list = workout_day.get('exercises', [])
                total_calories = workout_day.get('total_calories', 0)
                
                plan_text += f"""
        <div class="workout-day">
            <strong>📅 {day_name}:</strong> تمارين متنوعة ({total_calories} سعرة)
            <div style="margin-top: 0.5rem; padding-left: 1rem;">"""
                
                # عرض أول 3 تمارين مع التفاصيل
                for j, exercise in enumerate(exercises_list[:3]):
                    equipment = exercise.get('equipment', 'بدون معدات')
                    description = exercise.get('description', '')
                    video_url = exercise.get('video_url', '')
                    
                    plan_text += f"""
                <div style="margin-bottom: 0.3rem; font-size: 0.9rem;">
                    • {exercise.get('name', 'تمرين')} - {exercise.get('sets', 3)} مجموعات × {exercise.get('reps', 12)} تكرار
                    <span style="color: #6b7280; font-size: 0.8rem;">({equipment})</span>
                </div>"""
                
                plan_text += """
            </div>
        </div>"""
        
        plan_text += """
    </div>
    
    <div class="plan-section meal-plan">
        <h3 class="section-title">🍽️ خطة الوجبات اليومية</h3>"""
        
        # Add meal plan with card formatting
        meal_emojis = {
            'breakfast': '🌅',
            'lunch': '☀️', 
            'dinner': '🌙',
            'snack': '🍎'
        }
        
        meal_names = {
            'breakfast': 'الإفطار',
            'lunch': 'الغداء', 
            'dinner': 'العشاء',
            'snack': 'سناك'
        }
        
        total_calories = 0
        for meal_type, meal_name in meal_names.items():
            if meal_type in meals and meals[meal_type]:
                meal = meals[meal_type]
                emoji = meal_emojis.get(meal_type, '🍽️')
                calories = meal.get('calories', 0)
                food_preference = meal.get('food_preference', 'عام')
                protein = meal.get('protein', 0)
                total_calories += calories
                plan_text += f"""
        <div class="meal-item">
            <span style="font-size: 1.5rem;">{emoji}</span>
            <div style="flex: 1;">
                <strong>{meal_name}:</strong> {meal.get('name', 'وجبة')}
                <span class="calories-badge">{calories} سعرة</span>
                <div style="font-size: 0.8rem; color: #6b7280; margin-top: 0.2rem;">
                    🏷️ {food_preference} | 💪 {protein}g بروتين
                </div>
            </div>
        </div>"""
        
        plan_text += f"""
        <div style="text-align: center; margin-top: 1rem; padding: 1rem; background: rgba(255,255,255,0.8); border-radius: 8px;">
            <strong style="color: #059669; font-size: 1.2rem;">📊 إجمالي السعرات: {total_calories} سعرة</strong>
        </div>
    </div>
    
    <div class="plan-section tips-section">
        <h3 class="section-title">💡 نصائحك الذهبية</h3>"""
        
        # Add golden tips with card formatting
        default_tips = [
            {"icon": "💧", "title": "الماء", "description": "اشرب 3 لتر ماء يومياً"},
            {"icon": "🥗", "title": "البروتين", "description": "ركز على البروتين في كل وجبة"},
            {"icon": "😴", "title": "النوم", "description": "نم 7-8 ساعات يومياً للتعافي"}
        ]
        
        tips_to_use = tips[:3] if tips else default_tips[:3]
        
        for tip in tips_to_use:
            plan_text += f"""
        <div class="tip-item">
            <span style="font-size: 1.3rem; margin-left: 0.5rem;">{tip.get('icon', '💡')}</span>
            <strong>{tip.get('description', tip.get('title', 'نصيحة مفيدة'))}</strong>
        </div>"""
        
        plan_text += """
    </div>
    
    <div class="plan-section motivation-section">
        <h3 class="section-title">🎉 رسالة تحفيزية</h3>"""
        
        # Add motivational message with card formatting
        motivational_quotes = [
            "كل يوم ملتزم بخطتك = خطوة أقرب لهدفك",
            "أنت أقوى من أعذارك وأقرب لهدفك مما تتخيل",
            "التغيير يبدأ من اليوم، والنجاح ينتظرك في النهاية",
            "كل تمرين وكل وجبة صحية تقربك خطوة من هدفك",
            "الطريق صعب لكن النتيجة تستحق كل المجهود"
        ]
        
        import random
        selected_quote = random.choice(motivational_quotes)
        
        plan_text += f"""
        <div class="motivation-quote">
            "{selected_quote}"
        </div>
        <div style="margin-top: 1rem; font-size: 0.9rem; color: #6b7280;">
            ⏰ المدة المتوقعة: {timeline_weeks} أسبوع | 💧 اشرب {nutrition_plan.get('water_intake', 3)} لتر ماء يومياً
        </div>
    </div>
</div>"""
        
        return plan_text
        
    except Exception as e:
        print(f"Error generating AI plan: {str(e)}")
        return """<div class="personalized-plan-container">
    <div class="plan-header">
        <h2 class="plan-title">⚠️ خطأ في إنشاء الخطة</h2>
    </div>
    <div class="plan-section">
        <p>عذراً، حدث خطأ في إنشاء الخطة. يرجى المحاولة مرة أخرى.</p>
    </div>
</div>"""

def get_goal_arabic(goal):
    """Convert goal to Arabic"""
    goals = {
        'weight_loss': 'فقدان الوزن',
        'muscle_gain': 'بناء العضلات',
        'body_recomp': 'تحسين تركيب الجسم',
        'maintenance': 'المحافظة على الوزن',
        'general_fitness': 'اللياقة العامة'
    }
    return goals.get(goal, goal)

def get_workout_type_arabic(workout_type):
    """Convert workout type to Arabic"""
    types = {
        'upper_body': 'الجزء العلوي',
        'lower_body': 'الجزء السفلي',
        'full_body': 'الجسم كامل',
        'push': 'تمارين الدفع',
        'pull': 'تمارين السحب',
        'legs': 'تمارين الأرجل'
    }
    return types.get(workout_type, workout_type)

def get_sample_workout_plan():
    """Get a sample workout plan with video links for the workout plans page"""
    try:
        conn = get_db_connection()
        
        # الحصول على التمارين من قاعدة البيانات
        exercises = conn.execute('''
            SELECT name, muscle_group, difficulty, difficulty_text, sets, reps, 
                   calories_burned, equipment, description, video_url
            FROM exercises 
            ORDER BY RANDOM() 
            LIMIT 18
        ''').fetchall()
        
        conn.close()
        
        if not exercises:
            return []
        
        # تنظيم التمارين في خطة أسبوعية
        workout_plan = []
        days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
        
        # توزيع التمارين على الأيام
        exercises_per_day = 3
        for i, day in enumerate(days):
            if i == 6:  # يوم الراحة (السبت)
                workout_plan.append({
                    'day': day,
                    'workout_type': 'rest',
                    'exercises': [],
                    'is_rest_day': True,
                    'total_calories': 0
                })
            else:
                day_exercises = []
                start_idx = (i * exercises_per_day) % len(exercises)
                
                for j in range(exercises_per_day):
                    exercise_idx = (start_idx + j) % len(exercises)
                    exercise = exercises[exercise_idx]
                    
                    day_exercises.append({
                        'name': exercise[0],
                        'muscle_group': exercise[1],
                        'difficulty': exercise[3] or 'مبتدئ',  # استخدام difficulty_text
                        'sets': exercise[4],
                        'reps': exercise[5],
                        'calories_burned': exercise[6],
                        'equipment': exercise[7],
                        'description': exercise[8] or 'لا يوجد وصف متاح',
                        'video_url': exercise[9] or ''
                    })
                
                total_calories = sum(ex['calories_burned'] for ex in day_exercises)
                
                workout_plan.append({
                    'day': day,
                    'workout_type': f'day_{i+1}',
                    'exercises': day_exercises,
                    'is_rest_day': False,
                    'total_calories': total_calories
                })
        
        return workout_plan
        
    except Exception as e:
        print(f"Error in get_sample_workout_plan: {str(e)}")
        return []



@app.route('/gym-injuries')
def gym_injuries():
    """Gym injuries guide page"""
    return render_template('gym_injuries.html')

@app.route('/training-nutrition')
def training_nutrition():
    """Training and Nutrition education page"""
    return render_template('training_nutrition.html')

@app.route('/article/cardio-vs-resistance')
def article_cardio_vs_resistance():
    """Article: Cardio vs Resistance Training"""
    return render_template('article_cardio_vs_resistance.html')

@app.route('/article/protein-types')
def article_protein_types():
    """Article: Animal vs Plant Protein"""
    return render_template('article_protein_types.html')

@app.route('/article/water-importance')
def article_water_importance():
    """Article: Importance of Water"""
    return render_template('article_water_importance.html')

@app.route('/article/consistency-tips')
def article_consistency_tips():
    """Article: Consistency Tips"""
    return render_template('article_consistency_tips.html')

@app.route('/article/beginner-mistakes')
def article_beginner_mistakes():
    """Article: Common Beginner Mistakes"""
    return render_template('article_beginner_mistakes.html')

@app.route('/article/transformation-stories')
def article_transformation_stories():
    """Article: Transformation Stories"""
    return render_template('article_transformation_stories.html')

@app.route('/article/motivation-psychology')
def article_motivation_psychology():
    """Article: Motivation Psychology"""
    return render_template('article_motivation_psychology.html')

@app.route('/article/first-gym-day')
def article_first_gym_day():
    """Article: First Day at the Gym"""
    return render_template('article_first_gym_day.html')

@app.route('/article/workout-systems')
def article_workout_systems():
    """Article: Different Workout Systems"""
    return render_template('article_workout_systems.html')

@app.route('/article/body-muscles')
def article_body_muscles():
    """Article: Complete Body Muscles Guide"""
    return render_template('article_body_muscles.html')

@app.route('/article/fitness-improvement')
def article_fitness_improvement():
    """Article: How to Improve Your Fitness"""
    return render_template('article_fitness_improvement.html')

@app.route('/article/football-exercises')
def article_football_exercises():
    """Article: Exercises for Football Players"""
    return render_template('article_football_exercises.html')

@app.route('/article/walking-benefits')
def article_walking_benefits():
    """Article: Benefits of Walking for Weight Loss"""
    return render_template('article_walking_benefits.html')

@app.route('/article/diet-plan')
def article_diet_plan():
    """Article: How to Create a Diet Plan"""
    return render_template('article_diet_plan.html')

@app.route('/workout-plan-input')
def workout_plan_input():
    """Workout plan input form page"""
    return render_template('workout-plan-input.html')

@app.route('/test-card-design')
def test_card_design():
    """Test page for the new card design"""
    return render_template('card_design_test.html')

# Removed duplicate exercise_preview function - using the newer version below

def get_level_arabic(level):
    """Convert fitness level to Arabic"""
    levels = {
        'beginner': 'مبتدئ',
        'intermediate': 'متوسط',
        'advanced': 'متقدم'
    }
    return levels.get(level, level)

def get_default_exercises(goal, split, level):
    """Get default exercises when database query returns no results"""
    default_exercises = {
        'full_body': [
            {'name_ar': 'القرفصاء', 'name_en': 'Squats', 'muscle_group': 'الأرجل', 'equipment': 'وزن الجسم', 'difficulty': level, 'sets': '3', 'reps': '12-15', 'rest_time': '60 ثانية', 'instructions': 'تمرين ممتاز لتقوية عضلات الأرجل'},
            {'name_ar': 'الضغط', 'name_en': 'Push-ups', 'muscle_group': 'الصدر', 'equipment': 'وزن الجسم', 'difficulty': level, 'sets': '3', 'reps': '10-12', 'rest_time': '60 ثانية', 'instructions': 'تمرين أساسي لتقوية عضلات الصدر'},
            {'name_ar': 'العقلة', 'name_en': 'Pull-ups', 'muscle_group': 'الظهر', 'equipment': 'عقلة', 'difficulty': level, 'sets': '3', 'reps': '8-10', 'rest_time': '90 ثانية', 'instructions': 'تمرين ممتاز لتقوية عضلات الظهر'},
            {'name_ar': 'البلانك', 'name_en': 'Plank', 'muscle_group': 'البطن', 'equipment': 'وزن الجسم', 'difficulty': level, 'sets': '3', 'reps': '30-60 ثانية', 'rest_time': '60 ثانية', 'instructions': 'تمرين ممتاز لتقوية عضلات البطن'}
        ],
        'upper_lower': [
            {'name_ar': 'البنش برس', 'name_en': 'Bench Press', 'muscle_group': 'الصدر', 'equipment': 'بار', 'difficulty': level, 'sets': '4', 'reps': '8-10', 'rest_time': '90 ثانية', 'instructions': 'تمرين أساسي لبناء عضلات الصدر'},
            {'name_ar': 'السحب بالبار', 'name_en': 'Barbell Rows', 'muscle_group': 'الظهر', 'equipment': 'بار', 'difficulty': level, 'sets': '4', 'reps': '8-10', 'rest_time': '90 ثانية', 'instructions': 'تمرين ممتاز لتقوية عضلات الظهر'},
            {'name_ar': 'الديدليفت', 'name_en': 'Deadlift', 'muscle_group': 'الأرجل', 'equipment': 'بار', 'difficulty': level, 'sets': '4', 'reps': '6-8', 'rest_time': '120 ثانية', 'instructions': 'تمرين شامل لتقوية عضلات الجسم السفلي'},
            {'name_ar': 'القرفصاء الأمامي', 'name_en': 'Front Squats', 'muscle_group': 'الأرجل', 'equipment': 'بار', 'difficulty': level, 'sets': '4', 'reps': '10-12', 'rest_time': '90 ثانية', 'instructions': 'تمرين ممتاز لتقوية عضلات الأرجل الأمامية'}
        ],
        'push_pull_legs': [
            {'name_ar': 'البنش برس', 'name_en': 'Bench Press', 'muscle_group': 'الصدر', 'equipment': 'بار', 'difficulty': level, 'sets': '4', 'reps': '8-10', 'rest_time': '90 ثانية', 'instructions': 'تمرين أساسي لبناء عضلات الصدر'},
            {'name_ar': 'الضغط العلوي', 'name_en': 'Overhead Press', 'muscle_group': 'الأكتاف', 'equipment': 'بار', 'difficulty': level, 'sets': '3', 'reps': '10-12', 'rest_time': '90 ثانية', 'instructions': 'تمرين ممتاز لتقوية عضلات الأكتاف'},
            {'name_ar': 'السحب بالكيبل', 'name_en': 'Cable Rows', 'muscle_group': 'الظهر', 'equipment': 'كيبل', 'difficulty': level, 'sets': '4', 'reps': '10-12', 'rest_time': '90 ثانية', 'instructions': 'تمرين ممتاز لتقوية عضلات الظهر الوسطى'},
            {'name_ar': 'القرفصاء', 'name_en': 'Squats', 'muscle_group': 'الأرجل', 'equipment': 'بار', 'difficulty': level, 'sets': '4', 'reps': '12-15', 'rest_time': '90 ثانية', 'instructions': 'تمرين أساسي لتقوية عضلات الأرجل'}
        ]
    }
    
    return default_exercises.get(split, default_exercises['full_body'])

@app.route('/your-plan-your-goal', methods=['GET', 'POST'])
def your_plan_your_goal():
    """Interactive fitness planner page"""
    if request.method == 'POST':
        try:
            # Get form data
            data = request.get_json()
            
            # Extract user selections
            goal = data.get('goal', '')
            split = data.get('split', '')
            fitness_level = data.get('fitnessLevel', '')
            barriers = data.get('barriers', [])
            age = int(data.get('age', 25))
            weight = float(data.get('weight', 70))
            height = float(data.get('height', 170))
            workout_days = int(data.get('workoutDays', 3))
            gender = data.get('gender', '')
            injuries = data.get('injuries', '')
            workout_location = data.get('workoutLocation', '')
            
            # Validate required fields
            required_fields = ['goal', 'split', 'weight', 'height', 'fitnessLevel', 'workoutDays']
            missing_fields = [field for field in required_fields if not data.get(field)]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'message': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
            
            # Generate workout plan data
            plan_title = f"خطة {get_goal_arabic(goal)} - نظام {get_split_arabic(split)}"
            plan_description = f"خطة تمرين شخصية مصممة خصيصاً لك لتحقيق هدف {get_goal_arabic(goal)} باستخدام نظام {get_split_arabic(split)}"
            
            # Generate sample exercises based on goal and split
            exercises = generate_sample_exercises(goal, split, fitness_level)
            
            # Calculate BMI and other metrics
            height_m = height / 100
            bmi = round(weight / (height_m * height_m), 1)
            
            # Generate personalized motivational message based on barriers
            motivational_message = generate_motivational_message(barriers, goal, fitness_level)
            
            # Filter exercises based on injuries
            if injuries:
                exercises = filter_exercises_by_injuries(exercises, injuries)
            
            # Generate weekly schedule
            weekly_schedule = generate_weekly_schedule(split, exercises, workout_days)
            
            # Generate exercise notes based on user data
            exercises_with_notes = add_exercise_notes(exercises, barriers, goal, fitness_level, injuries)
            
            # Generate personalized tips
            personalized_tips = generate_personalized_tips(goal, fitness_level, barriers, injuries)
            
            # Generate plan response
            response_data = {
                'success': True,
                'message': 'تم إنشاء الخطة بنجاح',
                'plan': {
                    'title': plan_title,
                    'description': plan_description,
                    'goal': goal,
                    'split': split,
                    'fitnessLevel': fitness_level,
                    'workoutDays': workout_days,
                    'weight': weight,
                    'height': height,
                    'age': age,
                    'gender': gender,
                    'injuries': injuries,
                    'workoutLocation': workout_location,
                    'barriers': barriers,
                    'bmi': bmi,
                    'motivationalMessage': motivational_message,
                    'exercises': exercises_with_notes,
                    'weeklySchedule': weekly_schedule,
                    'personalizedTips': personalized_tips
                }
            }
            
            return jsonify(response_data)
            
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'خطأ في إنشاء الخطة: {str(e)}'
            }), 500
    
    # Check if this is a results page request
    result = request.args.get('result')
    if result == '1':
        # This is a results page request
        return render_template('your_plan_your_goal.html')
    else:
        # Redirect to input form
        return redirect(url_for('workout_plan_input'))

def get_goal_arabic(goal):
    """Convert goal to Arabic"""
    goals = {
        'weight_loss': 'إنقاص الوزن',
        'weight_gain': 'زيادة الوزن',
        'muscle_building': 'بناء العضلات',
        'maintain_weight': 'المحافظة على الوزن'
    }
    return goals.get(goal, goal)

def get_split_arabic(split):
    """Convert split to Arabic"""
    splits = {
        'full_body': 'الجسم كامل',
        'upper_lower': 'علوي/سفلي',
        'push_pull_legs': 'دفع/سحب/أرجل',
        'bro_split': 'عضلة واحدة يومياً',
        'crossfit': 'كروس فيت',
        'hiit': 'تمارين عالية الكثافة'
    }
    return splits.get(split, split)

def generate_motivational_message(barriers, goal, fitness_level):
    """Generate personalized motivational message based on user barriers and goals"""
    messages = {
        'time': [
            "لقد اتخذت الخطوة الأولى — إليك خطة مصممة خصيصاً لوقتك وأهدافك! ⏰",
            "الوقت ليس عذراً بعد اليوم — خطتك القصيرة والفعالة جاهزة! 💪",
            "15-30 دقيقة فقط يومياً كافية لتحقيق أهدافك — ابدأ الآن! 🚀"
        ],
        'motivation': [
            "لا مزيد من الأعذار — خطتك الشخصية تبدأ اليوم! 🔥",
            "كل خطوة صغيرة تقربك من هدفك — دعنا نحتفل بكل تقدم! 🎉",
            "أنت أقوى مما تعتقد — خطتك ستثبت لك ذلك! 💪"
        ],
        'injuries': [
            "حتى مع الإصابات، سنساعدك على التدرب بأمان والتقدم خطوة بخطوة 🏥",
            "سلامتك أولويتنا — خطة آمنة ومصممة خصيصاً لحالتك 🛡️",
            "الإصابة لن تمنعك من تحقيق أهدافك — لدينا البدائل المناسبة! 💚"
        ],
        'results': [
            "النتائج قادمة — خطتك الجديدة ستظهر لك التقدم الواضح! 📈",
            "كل تمرين محسوب بدقة لضمان رؤية النتائج بسرعة ⚡",
            "صبر قليل وستندهش من التغيير — خطتك العلمية ستحقق المعجزات! 🌟"
        ],
        'boredom': [
            "لا مزيد من الملل — خطة متنوعة وممتعة تنتظرك! 🎯",
            "كل أسبوع تمارين جديدة ومثيرة — استعد للمتعة! 🎪",
            "التنويع هو سر النجاح — خطتك مليئة بالمفاجآت الممتعة! 🎨"
        ],
        'social': [
            "تدرب بثقة وراحة — خطتك مصممة لتناسب خصوصيتك 🏠",
            "لا حاجة للقلق من نظرات الآخرين — ركز على نفسك وأهدافك! 🎯",
            "قوتك الداخلية أهم من آراء الآخرين — ابدأ رحلتك بثقة! 💪"
        ],
        'knowledge': [
            "لا تقلق — كل تمرين مشروح بالتفصيل مع فيديوهات توضيحية! 📚",
            "من المبتدئ إلى المحترف — سنعلمك كل ما تحتاجه خطوة بخطوة! 🎓",
            "المعرفة قوة — وأنت الآن تملك كل ما تحتاجه للنجاح! 🧠"
        ],
        'none': [
            "ممتاز! أنت مستعد ومتحمس — خطة شاملة ومتوازنة لتحقيق أفضل النتائج! 🚀",
            "طاقتك الإيجابية ستقودك للنجاح — خطتك المثالية جاهزة! ⭐",
            "بدون عوائق، بدون حدود — استعد لتحقيق أهدافك بسرعة! 🏆"
        ]
    }
    
    # Select message based on primary barrier
    if barriers:
        primary_barrier = barriers[0]
        if primary_barrier in messages:
            return random.choice(messages[primary_barrier])
    
    # Default motivational message based on goal
    goal_messages = {
        'weight_loss': "رحلة إنقاص الوزن تبدأ بخطوة واحدة — وأنت تخطوها الآن! 🔥",
        'muscle_building': "بناء العضلات يحتاج صبر وإصرار — وأنت تملك كليهما! 💪",
        'weight_gain': "زيادة الوزن الصحية هدف رائع — خطتك ستحققه بذكاء! 📈",
        'maintain_weight': "الحفاظ على الوزن فن — وأنت ستتقنه مع خطتك! ⚖️"
    }
    
    return goal_messages.get(goal, "أنت على الطريق الصحيح — خطتك الشخصية ستقودك للنجاح! 🌟")

def add_exercise_notes(exercises, barriers, goal, fitness_level, injuries):
    """Add personalized notes to exercises based on user data"""
    exercises_with_notes = []
    
    for exercise in exercises:
        exercise_copy = exercise.copy()
        notes = []
        
        # Goal-based notes
        if goal == 'weight_loss':
            notes.append("💡 ركز على الوتيرة الثابتة والاستمرارية لحرق دهون أفضل")
        elif goal == 'muscle_building':
            notes.append("💡 زد الأوزان تدريجياً كل أسبوع لنمو عضلي أفضل")
        elif goal == 'weight_gain':
            notes.append("💡 ركز على التمارين المركبة لزيادة الكتلة العضلية")
        
        # Fitness level notes
        if fitness_level == 'beginner':
            notes.append("💡 ابدأ بأوزان خفيفة وزد تدريجياً لتجنب الإصابات")
        elif fitness_level == 'advanced':
            notes.append("💡 تحدى نفسك بتقنيات متقدمة وأوزان أثقل")
        
        # Barrier-based notes
        if 'time' in barriers:
            notes.append("⏰ تمرين سريع وفعال — مثالي لجدولك المزدحم")
        
        if 'injuries' in barriers:
            if 'قرفصاء' in exercise.get('name', '').lower() or 'squat' in exercise.get('name', '').lower():
                notes.append("🤕 تجنب النزول العميق — استخدم نطاق حركة جزئي للأمان")
            elif 'ضغط' in exercise.get('name', '').lower() or 'press' in exercise.get('name', '').lower():
                notes.append("🤕 ابدأ بأوزان خفيفة وركز على الشكل الصحيح")
        
        if 'motivation' in barriers:
            notes.append("🎯 تذكر: كل تكرار يقربك من هدفك — أنت تستطيع!")
        
        if 'boredom' in barriers:
            notes.append("🎪 جرب تغيير الزوايا أو السرعة لإضافة التنويع")
        
        if 'knowledge' in barriers:
            notes.append("📚 شاهد الفيديو التوضيحي قبل البدء للتأكد من الشكل الصحيح")
        
        # Injury-specific notes
        if injuries and 'ركبة' in injuries.lower():
            if 'قرفصاء' in exercise.get('name', '').lower():
                notes.append("⚠️ تجنب القرفصاء العميق — استخدم كرسي للدعم")
        
        if injuries and 'ظهر' in injuries.lower():
            if 'ديدليفت' in exercise.get('name', '').lower():
                notes.append("⚠️ ركز على استقامة الظهر وابدأ بأوزان خفيفة جداً")
        
        # Add notes to exercise
        if notes:
            exercise_copy['notes'] = notes
        
        exercises_with_notes.append(exercise_copy)
    
    return exercises_with_notes

def generate_sample_exercises(goal, split, fitness_level):
    """Generate exercises from database based on goal, split, and fitness level"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Query exercises from database based on criteria
        query = """
        SELECT id, name_ar as name, name_en, muscle_group, equipment_type, 
               sets, reps, rest_time, instructions, video_url, image_url,
               goal, split_type, risk_notes, alternatives, difficulty_level
        FROM admin_exercises 
        WHERE 1=1
        """
        params = []
        
        # Filter by goal if specified
        if goal and goal != 'maintain_weight':
            if goal == 'weight_loss':
                query += " AND (goal = 'weight_loss' OR goal = 'general')"
            elif goal == 'muscle_building':
                query += " AND (goal = 'muscle_building' OR goal = 'general')"
            elif goal == 'weight_gain':
                query += " AND (goal = 'weight_gain' OR goal = 'muscle_building' OR goal = 'general')"
        
        # Filter by split type if specified
        if split:
            split_mapping = {
                'full_body': 'Full Body',
                'upper_lower': 'Upper Lower',
                'push_pull_legs': 'PPL',
                'bro_split': 'Bro Split',
                'crossfit': 'CrossFit',
                'hiit': 'HIIT'
            }
            mapped_split = split_mapping.get(split, split)
            query += " AND (split_type = ? OR split_type = 'General')"
            params.append(mapped_split)
        
        # Filter by fitness level
        if fitness_level:
            if fitness_level == 'beginner':
                query += " AND difficulty_level IN ('beginner', 'intermediate')"
            elif fitness_level == 'intermediate':
                query += " AND difficulty_level IN ('beginner', 'intermediate', 'advanced')"
            elif fitness_level == 'advanced':
                query += " AND difficulty_level IN ('intermediate', 'advanced')"
        
        query += " ORDER BY muscle_group, name_ar LIMIT 12"
        
        cursor.execute(query, params)
        db_exercises = cursor.fetchall()
        
        # Convert to list of dictionaries
        exercises = []
        for exercise in db_exercises:
            exercise_dict = {
                'id': exercise['id'],
                'name': exercise['name'],
                'name_en': exercise['name_en'],
                'muscle': exercise['muscle_group'],
                'muscle_group': exercise['muscle_group'],
                'equipment': exercise['equipment_type'],
                'sets': str(exercise['sets']) if exercise['sets'] else '3',
                'reps': exercise['reps'] if exercise['reps'] else '10-12',
                'rest_time': exercise['rest_time'] if exercise['rest_time'] else '60-90 ثانية',
                'instructions': exercise['instructions'],
                'video_url': exercise['video_url'],
                'image_url': exercise['image_url'],
                'goal': exercise['goal'],
                'split_type': exercise['split_type'],
                'risk_notes': exercise['risk_notes'],
                'alternatives': exercise['alternatives'],
                'difficulty_level': exercise['difficulty_level']
            }
            exercises.append(exercise_dict)
        
        # If no exercises found, return fallback exercises
        if not exercises:
            exercises = get_fallback_exercises(split)
        
        conn.close()
        return exercises
        
    except Exception as e:
        conn.close()
        print(f"Error generating exercises: {e}")
        return get_fallback_exercises(split)

def get_fallback_exercises(split):
    """Fallback exercises if database query fails"""
    if split == 'full_body':
        return [
            {'name': 'القرفصاء', 'sets': '3', 'reps': '12-15', 'muscle': 'الأرجل'},
            {'name': 'الضغط', 'sets': '3', 'reps': '10-12', 'muscle': 'الصدر'},
            {'name': 'السحب', 'sets': '3', 'reps': '8-10', 'muscle': 'الظهر'},
            {'name': 'الضغط العلوي', 'sets': '3', 'reps': '10-12', 'muscle': 'الأكتاف'}
        ]
    elif split == 'upper_lower':
        return [
            {'name': 'البنش برس', 'sets': '4', 'reps': '8-10', 'muscle': 'الصدر'},
            {'name': 'السحب بالبار', 'sets': '4', 'reps': '8-10', 'muscle': 'الظهر'},
            {'name': 'الديدليفت', 'sets': '4', 'reps': '6-8', 'muscle': 'الأرجل'},
            {'name': 'القرفصاء الأمامي', 'sets': '4', 'reps': '10-12', 'muscle': 'الأرجل'}
        ]
    elif split == 'push_pull_legs':
        return [
            {'name': 'البنش برس', 'sets': '4', 'reps': '8-10', 'muscle': 'الصدر'},
            {'name': 'الضغط العلوي', 'sets': '3', 'reps': '10-12', 'muscle': 'الأكتاف'},
            {'name': 'السحب بالكيبل', 'sets': '4', 'reps': '10-12', 'muscle': 'الظهر'},
            {'name': 'القرفصاء', 'sets': '4', 'reps': '12-15', 'muscle': 'الأرجل'}
        ]
    else:
        return [
            {'name': 'تمرين أساسي 1', 'sets': '3', 'reps': '10-12', 'muscle': 'عام'},
            {'name': 'تمرين أساسي 2', 'sets': '3', 'reps': '10-12', 'muscle': 'عام'},
            {'name': 'تمرين أساسي 3', 'sets': '3', 'reps': '10-12', 'muscle': 'عام'}
        ]

@app.route('/api/exercise-preview', methods=['POST'])
def exercise_preview():
    """API endpoint for dynamic exercise preview"""
    try:
        data = request.get_json()
        goal = data.get('goal', '')
        split = data.get('split', '')
        fitness_level = data.get('fitnessLevel', 'beginner')
        
        # Get 2 sample exercises for preview
        exercises = generate_sample_exercises(goal, split, fitness_level)
        preview_exercises = exercises[:2] if exercises else []
        
        return jsonify({
            'success': True,
            'exercises': preview_exercises
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب التمارين: {str(e)}'
        }), 500

@app.route('/api/generate-workout-plan', methods=['POST'])
def generate_workout_plan():
    """API endpoint for generating complete workout plan from database"""
    try:
        data = request.get_json()
        
        # Extract user selections
        goal = data.get('goal', '')
        split = data.get('split', '')
        fitness_level = data.get('fitnessLevel', '')
        barriers = data.get('barriers', [])
        age = int(data.get('age', 25))
        weight = float(data.get('weight', 70))
        height = float(data.get('height', 170))
        workout_days = int(data.get('workoutDays', 3))
        gender = data.get('gender', '')
        injuries = data.get('injuries', '')
        workout_location = data.get('workoutLocation', '')
        
        # Validate required fields
        required_fields = ['goal', 'split', 'weight', 'height', 'fitnessLevel', 'workoutDays']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Generate exercises from database
        exercises = generate_sample_exercises(goal, split, fitness_level)
        
        # Filter exercises based on injuries
        if injuries:
            exercises = filter_exercises_by_injuries(exercises, injuries)
        
        # Generate weekly schedule
        weekly_schedule = generate_weekly_schedule(split, exercises, workout_days)
        
        # Calculate BMI and other metrics
        height_m = height / 100
        bmi = round(weight / (height_m * height_m), 1)
        
        # Generate personalized motivational message
        motivational_message = generate_motivational_message(barriers, goal, fitness_level)
        
        # Add exercise notes based on user data
        exercises_with_notes = add_exercise_notes(exercises, barriers, goal, fitness_level, injuries)
        
        # Generate personalized tips
        personalized_tips = generate_personalized_tips(goal, fitness_level, barriers, injuries)
        
        # Generate plan response
        response_data = {
            'success': True,
            'message': 'تم إنشاء الخطة بنجاح',
            'plan': {
                'title': f"خطة {get_goal_arabic(goal)} - نظام {get_split_arabic(split)}",
                'description': f"خطة تمرين شخصية مصممة خصيصاً لك لتحقيق هدف {get_goal_arabic(goal)} باستخدام نظام {get_split_arabic(split)}",
                'goal': goal,
                'split': split,
                'fitnessLevel': fitness_level,
                'workoutDays': workout_days,
                'weight': weight,
                'height': height,
                'age': age,
                'gender': gender,
                'injuries': injuries,
                'workoutLocation': workout_location,
                'barriers': barriers,
                'bmi': bmi,
                'motivationalMessage': motivational_message,
                'exercises': exercises_with_notes,
                'weeklySchedule': weekly_schedule,
                'personalizedTips': personalized_tips
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في إنشاء الخطة: {str(e)}'
        }), 500

def filter_exercises_by_injuries(exercises, injuries):
    """Filter out exercises that might aggravate injuries"""
    if not injuries:
        return exercises
    
    filtered_exercises = []
    injuries_lower = injuries.lower()
    
    for exercise in exercises:
        exercise_name = exercise.get('name', '').lower()
        risk_notes = exercise.get('risk_notes', '').lower()
        
        # Skip exercises that might be risky for specific injuries
        skip_exercise = False
        
        if 'ركبة' in injuries_lower or 'knee' in injuries_lower:
            if any(word in exercise_name for word in ['قرفصاء', 'squat', 'lunge', 'jump']):
                skip_exercise = True
        
        if 'ظهر' in injuries_lower or 'back' in injuries_lower:
            if any(word in exercise_name for word in ['ديدليفت', 'deadlift', 'row']):
                skip_exercise = True
        
        if 'كتف' in injuries_lower or 'shoulder' in injuries_lower:
            if any(word in exercise_name for word in ['ضغط علوي', 'overhead', 'press']):
                skip_exercise = True
        
        if not skip_exercise:
            filtered_exercises.append(exercise)
        else:
            # Add alternative exercise if available
            alternatives = exercise.get('alternatives', '')
            if alternatives:
                alternative_exercise = exercise.copy()
                alternative_exercise['name'] = alternatives
                alternative_exercise['notes'] = alternative_exercise.get('notes', []) + [f"⚠️ بديل آمن لـ {exercise['name']}"]
                filtered_exercises.append(alternative_exercise)
    
    return filtered_exercises

def generate_weekly_schedule(split, exercises, workout_days):
    """Generate weekly workout schedule based on split type"""
    days = ['الأحد', 'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت']
    schedule = []
    
    if split == 'full_body':
        # Full body 3x per week
        workout_pattern = ['تمرين كامل', 'راحة', 'تمرين كامل', 'راحة', 'تمرين كامل', 'راحة', 'راحة']
        for i, day in enumerate(days):
            if i < workout_days and workout_pattern[i] != 'راحة':
                schedule.append({
                    'day': day,
                    'type': 'تمرين كامل',
                    'exercises': exercises[:4] if exercises else []
                })
            else:
                schedule.append({
                    'day': day,
                    'type': 'راحة',
                    'exercises': []
                })
    
    elif split == 'upper_lower':
        # Upper/Lower split
        workout_pattern = ['علوي', 'سفلي', 'راحة', 'علوي', 'سفلي', 'راحة', 'راحة']
        upper_exercises = [ex for ex in exercises if ex.get('muscle_group') in ['الصدر', 'الظهر', 'الأكتاف', 'البايسبس', 'الترايسبس']]
        lower_exercises = [ex for ex in exercises if ex.get('muscle_group') in ['الأرجل', 'المؤخرة', 'السمانة']]
        
        for i, day in enumerate(days):
            if i < len(workout_pattern):
                if workout_pattern[i] == 'علوي':
                    schedule.append({
                        'day': day,
                        'type': 'تمرين علوي',
                        'exercises': upper_exercises[:4] if upper_exercises else exercises[:4]
                    })
                elif workout_pattern[i] == 'سفلي':
                    schedule.append({
                        'day': day,
                        'type': 'تمرين سفلي',
                        'exercises': lower_exercises[:4] if lower_exercises else exercises[4:8]
                    })
                else:
                    schedule.append({
                        'day': day,
                        'type': 'راحة',
                        'exercises': []
                    })
            else:
                schedule.append({
                    'day': day,
                    'type': 'راحة',
                    'exercises': []
                })
    
    elif split == 'push_pull_legs':
        # Push/Pull/Legs split
        workout_pattern = ['دفع', 'سحب', 'أرجل', 'راحة', 'دفع', 'سحب', 'راحة']
        push_exercises = [ex for ex in exercises if ex.get('muscle_group') in ['الصدر', 'الأكتاف', 'الترايسبس']]
        pull_exercises = [ex for ex in exercises if ex.get('muscle_group') in ['الظهر', 'البايسبس']]
        leg_exercises = [ex for ex in exercises if ex.get('muscle_group') in ['الأرجل', 'المؤخرة', 'السمانة']]
        
        for i, day in enumerate(days):
            if i < len(workout_pattern):
                if workout_pattern[i] == 'دفع':
                    schedule.append({
                        'day': day,
                        'type': 'تمرين دفع',
                        'exercises': push_exercises[:4] if push_exercises else exercises[:4]
                    })
                elif workout_pattern[i] == 'سحب':
                    schedule.append({
                        'day': day,
                        'type': 'تمرين سحب',
                        'exercises': pull_exercises[:4] if pull_exercises else exercises[4:8]
                    })
                elif workout_pattern[i] == 'أرجل':
                    schedule.append({
                        'day': day,
                        'type': 'تمرين أرجل',
                        'exercises': leg_exercises[:4] if leg_exercises else exercises[8:12]
                    })
                else:
                    schedule.append({
                        'day': day,
                        'type': 'راحة',
                        'exercises': []
                    })
            else:
                schedule.append({
                    'day': day,
                    'type': 'راحة',
                    'exercises': []
                })
    
    else:
        # Default schedule
        for i, day in enumerate(days):
            if i < workout_days:
                schedule.append({
                    'day': day,
                    'type': 'تمرين',
                    'exercises': exercises[:4] if exercises else []
                })
            else:
                schedule.append({
                    'day': day,
                    'type': 'راحة',
                    'exercises': []
                })
    
    return schedule

def generate_personalized_tips(goal, fitness_level, barriers, injuries):
    """Generate personalized tips based on user profile"""
    tips = []
    
    # Goal-based tips
    if goal == 'weight_loss':
        tips.append({
            'icon': '🔥',
            'title': 'نصيحة لحرق الدهون',
            'content': 'ركز على التمارين المركبة والكارديو عالي الكثافة لحرق أكبر عدد من السعرات الحرارية'
        })
    elif goal == 'muscle_building':
        tips.append({
            'icon': '💪',
            'title': 'نصيحة لبناء العضلات',
            'content': 'زد الأوزان تدريجياً كل أسبوع واحرص على تناول البروتين بعد التمرين مباشرة'
        })
    elif goal == 'weight_gain':
        tips.append({
            'icon': '📈',
            'title': 'نصيحة لزيادة الوزن',
            'content': 'ركز على التمارين المركبة الثقيلة وتناول وجبات متكررة غنية بالسعرات الصحية'
        })
    
    # Fitness level tips
    if fitness_level == 'beginner':
        tips.append({
            'icon': '🎯',
            'title': 'نصيحة للمبتدئين',
            'content': 'ابدأ بأوزان خفيفة وركز على تعلم الشكل الصحيح قبل زيادة الأوزان'
        })
    elif fitness_level == 'advanced':
        tips.append({
            'icon': '🏆',
            'title': 'نصيحة للمتقدمين',
            'content': 'جرب تقنيات متقدمة مثل Drop Sets و Supersets لكسر الثبات'
        })
    
    # Barrier-based tips
    if 'time' in barriers:
        tips.append({
            'icon': '⏰',
            'title': 'نصيحة لتوفير الوقت',
            'content': 'استخدم التمارين المركبة والدوائر التدريبية لتحقيق أقصى استفادة في وقت قصير'
        })
    
    if 'motivation' in barriers:
        tips.append({
            'icon': '🎯',
            'title': 'نصيحة للتحفيز',
            'content': 'ضع أهدافاً صغيرة أسبوعية واحتفل بكل إنجاز مهما كان صغيراً'
        })
    
    # Injury-based tips
    if injuries:
        tips.append({
            'icon': '🛡️',
            'title': 'نصيحة للأمان',
            'content': 'استشر طبيباً مختصاً قبل البدء وتوقف فوراً عند الشعور بأي ألم'
        })
    
    return tips

@app.route('/workout-guide')
def workout_guide():
    """Workout Guide & Splits - Exercise library with filtering"""
    # Get filter parameters
    muscle_group = request.args.get('muscle_group', '')
    equipment = request.args.get('equipment', '')
    difficulty = request.args.get('difficulty', '')
    search = request.args.get('search', '')
    
    # Connect to database
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Build query with filters
    query = "SELECT * FROM admin_exercises WHERE 1=1"
    params = []
    
    if muscle_group:
        query += " AND muscle_group = ?"
        params.append(muscle_group)
    
    if equipment:
        query += " AND equipment_type = ?"
        params.append(equipment)
    
    if difficulty:
        query += " AND difficulty_level = ?"
        params.append(difficulty)
    
    if search:
        query += " AND (name_ar LIKE ? OR name_en LIKE ?)"
        params.extend([f'%{search}%', f'%{search}%'])
    
    query += " ORDER BY muscle_group, name_ar"
    
    cursor.execute(query, params)
    exercises = cursor.fetchall()
    
    # Get unique values for filters
    cursor.execute("SELECT DISTINCT muscle_group FROM admin_exercises ORDER BY muscle_group")
    muscle_groups = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT equipment_type FROM admin_exercises ORDER BY equipment_type")
    equipment_types = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT DISTINCT difficulty_level FROM admin_exercises ORDER BY difficulty_level")
    difficulty_levels = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('workout_guide.html', 
                         exercises=exercises,
                         muscle_groups=muscle_groups,
                         equipment_types=equipment_types,
                         difficulty_levels=difficulty_levels,
                         current_muscle_group=muscle_group,
                         current_equipment=equipment,
                         current_difficulty=difficulty,
                         current_search=search)

@app.route('/food-calories-guide')
def food_calories_guide():
    """Food & Calories Guide - Comprehensive food library"""
    return render_template('food_calories_guide.html')

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    form = AdminLoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, password_hash, role, full_name FROM admin_users WHERE username = ?', 
                      (form.username.data,))
        admin = cursor.fetchone()
        conn.close()
        
        if admin and check_password_hash(admin[1], form.password.data):
            session['admin_id'] = admin[0]
            session['admin_role'] = admin[2]
            session['admin_name'] = admin[3]
            flash('تم تسجيل الدخول بنجاح', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('اسم المستخدم أو كلمة المرور غير صحيحة', 'error')
    
    return render_template('admin/login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_id', None)
    session.pop('admin_role', None)
    session.pop('admin_name', None)
    flash('تم تسجيل الخروج بنجاح', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    conn = sqlite3.connect('fitness_app.db')
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM admin_exercises')
    total_exercises = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM workout_splits')
    total_splits = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    conn.close()
    
    stats = {
        'total_exercises': total_exercises,
        'total_splits': total_splits,
        'total_users': total_users
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/exercises')
@admin_required
def admin_exercises():
    """List all exercises"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    muscle_group = request.args.get('muscle_group', '')
    difficulty = request.args.get('difficulty', '')
    
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Build query with filters
    query = 'SELECT * FROM admin_exercises WHERE 1=1'
    params = []
    
    if search:
        query += ' AND (name_en LIKE ? OR name_ar LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if muscle_group:
        query += ' AND muscle_group = ?'
        params.append(muscle_group)
    
    if difficulty:
        query += ' AND difficulty_level = ?'
        params.append(difficulty)
    
    query += ' ORDER BY created_at DESC LIMIT 20 OFFSET ?'
    params.append((page - 1) * 20)
    
    cursor.execute(query, params)
    exercises = cursor.fetchall()
    
    # Get total count for pagination
    count_query = query.replace('SELECT * FROM admin_exercises', 'SELECT COUNT(*) FROM admin_exercises').split('ORDER BY')[0]
    cursor.execute(count_query, params[:-1])
    total = cursor.fetchone()[0]
    
    conn.close()
    
    # Create pagination object
    per_page = 20
    total_pages = (total + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    prev_num = page - 1 if has_prev else None
    next_num = page + 1 if has_next else None
    
    # Simple pagination object
    class Pagination:
        def __init__(self, page, per_page, total, has_prev, has_next, prev_num, next_num, pages):
            self.page = page
            self.per_page = per_page
            self.total = total
            self.has_prev = has_prev
            self.has_next = has_next
            self.prev_num = prev_num
            self.next_num = next_num
            self.pages = pages
            
        def iter_pages(self, left_edge=2, left_current=2, right_current=3, right_edge=2):
            last = self.pages
            for num in range(1, last + 1):
                if num <= left_edge or \
                   (self.page - left_current - 1 < num < self.page + right_current) or \
                   num > last - right_edge:
                    yield num
    
    pagination = Pagination(page, per_page, total, has_prev, has_next, prev_num, next_num, total_pages)
    
    return render_template('admin/exercises.html', 
                         exercises=exercises, 
                         pagination=pagination,
                         search=search,
                         muscle_group=muscle_group,
                         difficulty=difficulty)

@app.route('/admin/exercises/add', methods=['GET', 'POST'])
@admin_required
def admin_add_exercise():
    """Add new exercise"""
    form = ExerciseForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        # Handle image upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = str(int(time.time()))
                image_url = f"exercise_{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_url))
        
        cursor.execute('''
            INSERT INTO admin_exercises 
            (name_en, name_ar, muscle_group, equipment_type, difficulty_level, goal, split_type,
             sets, reps, rest_time, instructions, form_cues, common_mistakes, risk_notes, alternatives,
             video_url, image_url, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (form.name_en.data, form.name_ar.data, form.muscle_group.data,
              form.equipment_type.data, form.difficulty_level.data, form.goal.data, form.split_type.data,
              form.sets.data, form.reps.data, form.rest_time.data, form.instructions.data,
              form.form_cues.data, form.common_mistakes.data, form.risk_notes.data, form.alternatives.data,
              form.video_url.data, image_url, session['admin_id']))
        
        conn.commit()
        conn.close()
        
        flash('تم إضافة التمرين بنجاح', 'success')
        return redirect(url_for('admin_exercises'))
    
    return render_template('admin/add_exercise.html', form=form)

@app.route('/admin/exercises/edit/<int:exercise_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_exercise(exercise_id):
    """Edit exercise"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM admin_exercises WHERE id = ?', (exercise_id,))
    exercise = cursor.fetchone()
    
    if not exercise:
        flash('التمرين غير موجود', 'error')
        return redirect(url_for('admin_exercises'))
    
    form = ExerciseForm()
    
    if form.validate_on_submit():
        # Handle image upload
        image_url = exercise[13]  # Keep existing image
        if 'image' in request.files:
            file = request.files['image']
            if file and allowed_file(file.filename):
                # Delete old image
                if exercise[13]:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER'], exercise[13])
                    if os.path.exists(old_path):
                        os.remove(old_path)
                
                filename = secure_filename(file.filename)
                timestamp = str(int(time.time()))
                image_url = f"exercise_{timestamp}_{filename}"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_url))
        
        cursor.execute('''
            UPDATE admin_exercises SET
            name_en=?, name_ar=?, muscle_group=?, equipment_type=?, difficulty_level=?, goal=?, split_type=?,
            sets=?, reps=?, rest_time=?, instructions=?, form_cues=?, common_mistakes=?, risk_notes=?, alternatives=?,
            video_url=?, image_url=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        ''', (form.name_en.data, form.name_ar.data, form.muscle_group.data,
              form.equipment_type.data, form.difficulty_level.data, form.goal.data, form.split_type.data,
              form.sets.data, form.reps.data, form.rest_time.data, form.instructions.data,
              form.form_cues.data, form.common_mistakes.data, form.risk_notes.data, form.alternatives.data,
              form.video_url.data, image_url, exercise_id))
        
        conn.commit()
        conn.close()
        
        flash('تم تحديث التمرين بنجاح', 'success')
        return redirect(url_for('admin_exercises'))
    
    # Pre-populate form with existing data
    if request.method == 'GET':
        form.name_en.data = exercise[1]
        form.name_ar.data = exercise[2]
        form.muscle_group.data = exercise[3]
        form.equipment_type.data = exercise[4]
        form.difficulty_level.data = exercise[5]
        form.sets.data = exercise[6]
        form.reps.data = exercise[7]
        form.rest_time.data = exercise[8]
        form.instructions.data = exercise[9]
        form.form_cues.data = exercise[10]
        form.common_mistakes.data = exercise[11]
        form.video_url.data = exercise[12]
        # New fields (will be None if not present in old records)
        if len(exercise) > 14:
            form.goal.data = exercise[14] if exercise[14] else 'weight_loss'
        if len(exercise) > 15:
            form.split_type.data = exercise[15] if exercise[15] else 'full_body'
        if len(exercise) > 16:
            form.risk_notes.data = exercise[16]
        if len(exercise) > 17:
            form.alternatives.data = exercise[17]
    
    conn.close()
    return render_template('admin/edit_exercise.html', form=form, exercise=exercise)

@app.route('/admin/exercises/delete/<int:exercise_id>', methods=['POST'])
@admin_required
def admin_delete_exercise(exercise_id):
    """Delete exercise"""
    conn = sqlite3.connect('fitness_app.db')
    cursor = conn.cursor()
    
    # Get exercise info for image deletion
    cursor.execute('SELECT image_url FROM admin_exercises WHERE id = ?', (exercise_id,))
    exercise = cursor.fetchone()
    
    if exercise:
        # Delete image file
        if exercise[0]:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], exercise[0])
            if os.path.exists(image_path):
                os.remove(image_path)
        
        # Delete from database
        cursor.execute('DELETE FROM admin_exercises WHERE id = ?', (exercise_id,))
        cursor.execute('DELETE FROM exercise_split_mapping WHERE exercise_id = ?', (exercise_id,))
        
        conn.commit()
        flash('تم حذف التمرين بنجاح', 'success')
    else:
        flash('التمرين غير موجود', 'error')
    
    conn.close()
    return redirect(url_for('admin_exercises'))

# إضافة الدالة إلى context processors لتكون متاحة في جميع القوالب
@app.context_processor
def inject_workout_plan():
    return dict(get_sample_workout_plan=get_sample_workout_plan)

# صفحة الاستبيان التفاعلي
@app.route('/interactive-quiz')
def interactive_quiz():
    """صفحة الاستبيان التفاعلي لتحديد الخطة المثالية"""
    return render_template('interactive_quiz.html')

# صفحة خطة الوجبات المخصصة
@app.route('/meal-plan')
def meal_plan():
    """صفحة عرض خطة الوجبات المخصصة"""
    # الحصول على البيانات من URL parameters
    calories = request.args.get('calories', 2000, type=int)
    protein = request.args.get('protein', 150, type=int)
    carbs = request.args.get('carbs', 200, type=int)
    fats = request.args.get('fats', 70, type=int)
    goal = request.args.get('goal', 'maintenance')
    
    return render_template('meal_plan.html', 
                         calories=calories, 
                         protein=protein, 
                         carbs=carbs, 
                         fats=fats,
                         goal=goal)

# معالجة نتائج الاستبيان
@app.route('/quiz-results', methods=['POST'])
def quiz_results():
    """معالجة نتائج الاستبيان وإرجاع التوصيات"""
    try:
        data = request.get_json()
        
        # التحقق من صحة البيانات
        required_fields = ['age', 'currentWeight', 'height', 'targetWeight', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # حساب BMR و TDEE
        weight = float(data['currentWeight'])
        height = int(data['height'])
        age = int(data['age'])
        gender = data['gender']
        
        # حساب BMR باستخدام معادلة Mifflin-St Jeor
        if gender == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        
        # حساب TDEE بناءً على مستوى النشاط
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        
        activity_level = data.get('activityLevel', 'sedentary')
        tdee = bmr * activity_multipliers.get(activity_level, 1.2)
        
        # حساب هدف السعرات بناءً على الهدف
        goal = data.get('goal', 'maintain')
        weight_change_speed = data.get('weightChangeSpeed', 'moderate')
        
        calorie_adjustments = {
            'lose_weight': {
                'fast': -700,
                'moderate': -500,
                'slow': -300
            },
            'gain_weight': {
                'fast': 500,
                'moderate': 300,
                'slow': 200
            },
            'maintain': {
                'fast': 0,
                'moderate': 0,
                'slow': 0
            }
        }
        
        target_weight = float(data['targetWeight'])
        current_weight = weight
        
        if target_weight > current_weight:
            goal_type = 'gain_weight'
        elif target_weight < current_weight:
            goal_type = 'lose_weight'
        else:
            goal_type = 'maintain'
        
        calorie_goal = tdee + calorie_adjustments[goal_type].get(weight_change_speed, 0)
        
        # حساب توزيع الماكروز
        protein_ratio = 0.25  # 25% بروتين
        carbs_ratio = 0.45    # 45% كربوهيدرات
        fats_ratio = 0.30     # 30% دهون
        
        protein_grams = (calorie_goal * protein_ratio) / 4
        carbs_grams = (calorie_goal * carbs_ratio) / 4
        fats_grams = (calorie_goal * fats_ratio) / 9
        
        # تحليل الإجابات وتحديد التوصيات
        recommendations = analyze_quiz_answers(data)
        
        # إنشاء الاستجابة
        response_data = {
            'success': True,
            'message': 'تم حفظ النتائج بنجاح',
            'calculations': {
                'bmr': round(bmr),
                'tdee': round(tdee),
                'calorie_goal': round(calorie_goal),
                'bmi': round(weight / ((height/100) ** 2), 1),
                'macros': {
                    'protein': round(protein_grams),
                    'carbs': round(carbs_grams),
                    'fats': round(fats_grams)
                },
                'weight_difference': target_weight - current_weight
            },
            'recommendations': recommendations,
            'goal_info': {
                'goal_type': goal_type,
                'estimated_weeks': abs(target_weight - current_weight) * 2 if goal_type != 'maintain' else 0
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في معالجة النتائج: {str(e)}'
        }), 500

def analyze_quiz_answers(answers):
    """تحليل إجابات الاستبيان وإرجاع التوصيات المخصصة"""
    recommendations = {
        'workout_plan': '',
        'nutrition_plan': '',
        'duration': '',
        'intensity': '',
        'tips': [],
        'meal_suggestions': [],
        'exercise_suggestions': [],
        'weekly_plan': {}
    }
    
    # تحليل الهدف الأساسي
    goal = answers.get('goal', '')
    activity_level = answers.get('activityLevel', 'sedentary')
    time_available = answers.get('timeAvailable', '30')
    food_preferences = answers.get('foodPreferences', [])
    allergies = answers.get('allergies', [])
    health_conditions = answers.get('healthConditions', [])
    budget = answers.get('budget', 'medium')
    cooking_time = answers.get('cookingTime', 'medium')
    
    # تحديد خطة التمارين بناءً على الهدف
    if goal == 'lose_weight':
        recommendations['workout_plan'] = 'خطة حرق الدهون والتنحيف'
        recommendations['nutrition_plan'] = 'نظام غذائي منخفض السعرات مع توازن الماكروز'
        recommendations['tips'].extend([
            'ركز على التمارين الهوائية (كارديو) 4-5 مرات أسبوعياً',
            'أضف تمارين المقاومة 2-3 مرات أسبوعياً للحفاظ على العضلات',
            'اشرب 2-3 لتر من الماء يومياً',
            'تناول وجبات صغيرة ومتكررة كل 3-4 ساعات',
            'احرص على النوم 7-8 ساعات يومياً'
        ])
        recommendations['exercise_suggestions'] = [
            'المشي السريع أو الجري الخفيف (30-45 دقيقة)',
            'تمارين HIIT (20-30 دقيقة)',
            'تمارين القوة بالأوزان الخفيفة',
            'السباحة أو ركوب الدراجة'
        ]
    elif goal == 'gain_weight':
        recommendations['workout_plan'] = 'خطة بناء العضلات وزيادة الوزن'
        recommendations['nutrition_plan'] = 'نظام غذائي عالي السعرات والبروتين'
        recommendations['tips'].extend([
            'ركز على تمارين المقاومة الثقيلة 4-5 مرات أسبوعياً',
            'قلل من التمارين الهوائية إلى 2-3 مرات أسبوعياً فقط',
            'تناول وجبة كل 2-3 ساعات',
            'احرص على تناول البروتين بعد التمرين مباشرة',
            'النوم والراحة أساسيان لنمو العضلات'
        ])
        recommendations['exercise_suggestions'] = [
            'تمارين الأوزان الحرة (باربل ودمبل)',
            'تمارين مركبة (سكوات، ديدليفت، بنش برس)',
            'تمارين العزل للعضلات الصغيرة',
            'تمارين الجذع والاستقرار'
        ]
    elif goal == 'maintain':
        recommendations['workout_plan'] = 'خطة الحفاظ على اللياقة والوزن'
        recommendations['nutrition_plan'] = 'نظام غذائي متوازن للحفاظ على الوزن'
        recommendations['tips'].extend([
            'امزج بين تمارين القوة والكارديو',
            'حافظ على روتين ثابت 3-4 مرات أسبوعياً',
            'تناول نظام غذائي متوازن ومتنوع',
            'راقب وزنك أسبوعياً'
        ])
    else:  # fitness
        recommendations['workout_plan'] = 'خطة تحسين اللياقة العامة'
        recommendations['nutrition_plan'] = 'نظام غذائي متوازن لدعم الأداء'
        recommendations['tips'].extend([
            'نوع في التمارين لتجنب الملل',
            'ادمج تمارين المرونة والتوازن',
            'حافظ على الانتظام في التمرين',
            'استمع لجسمك وخذ أيام راحة عند الحاجة'
        ])
    
    # تحديد شدة التمرين بناءً على مستوى النشاط
    intensity_map = {
        'sedentary': 'منخفضة - ابدأ تدريجياً (50-60% من أقصى معدل ضربات القلب)',
        'light': 'منخفضة إلى متوسطة (60-70% من أقصى معدل ضربات القلب)',
        'moderate': 'متوسطة (70-80% من أقصى معدل ضربات القلب)',
        'active': 'متوسطة إلى عالية (80-85% من أقصى معدل ضربات القلب)',
        'very_active': 'عالية - تحدي متقدم (85-90% من أقصى معدل ضربات القلب)'
    }
    recommendations['intensity'] = intensity_map.get(activity_level, 'متوسطة')
    
    # تحديد مدة التمرين
    time_recommendations = {
        '15': 'تمارين قصيرة ومكثفة (HIIT)',
        '30': 'تمارين متوسطة المدة',
        '45': 'تمارين شاملة',
        '60': 'تمارين مفصلة وشاملة',
        '90': 'تمارين متقدمة ومكثفة'
    }
    recommendations['duration'] = time_recommendations.get(time_available, 'حسب الوقت المتاح')
    
    # اقتراحات الوجبات المصرية بناءً على التفضيلات
    meal_base = []
    if 'vegetarian' in food_preferences:
        meal_base.extend([
            'فول مدمس بالطحينة والسلطة البلدي',
            'كشري مصري بالعدس والأرز والمكرونة',
            'ملوخية بالخضار مع الأرز الأبيض',
            'فاصوليا خضراء بالطماطم والأرز',
            'شوربة عدس مصرية مع الخبز البلدي',
            'طحينة بالعسل مع الخبز البلدي'
        ])
    else:
        meal_base.extend([
            'فراخ مشوية مع الأرز الأبيض والسلطة',
            'سمك بلطي مشوي مع الخضار السوتيه',
            'كباب مشوي مع الخبز البلدي والطحينة',
            'بيض مقلي مع الجبنة البيضاء والطحينة',
            'لحمة مفرومة بالبصل مع الأرز',
            'فراخ بانيه مع البطاطس المسلوقة'
        ])
    
    # إضافة الوجبات المصرية التقليدية بناءً على الحساسية
    if 'lactose' not in allergies:
        meal_base.extend([
            'زبادي بالخيار والنعناع',
            'جبنة قريش مع الطماطم والخيار',
            'لبن رايب مع العسل والمكسرات'
        ])
    
    if 'gluten' not in allergies:
        meal_base.extend([
            'عيش بلدي بالجبنة البيضاء والطحينة',
            'فطار مصري تقليدي بالفول والطعمية',
            'خبز بلدي محمص مع الطحينة والعسل'
        ])
    
    recommendations['meal_suggestions'] = meal_base[:6]  # أول 6 اقتراحات
    
    # خطة أسبوعية مبسطة
    recommendations['weekly_plan'] = {
        'الأحد': 'تمارين الجزء العلوي + كارديو خفيف',
        'الاثنين': 'تمارين الجزء السفلي',
        'الثلاثاء': 'كارديو متوسط الشدة',
        'الأربعاء': 'تمارين الجذع والاستقرار',
        'الخميس': 'تمارين شاملة للجسم',
        'الجمعة': 'كارديو عالي الشدة (HIIT)',
        'السبت': 'راحة أو تمارين خفيفة (يوغا/مشي)'
    }
    
    # نصائح إضافية بناءً على الحالات الصحية
    if 'diabetes' in health_conditions:
        recommendations['tips'].append('راقب مستوى السكر قبل وبعد التمرين')
        recommendations['tips'].append('تجنب التمارين عالية الشدة إذا كان السكر غير مستقر')
    
    if 'hypertension' in health_conditions:
        recommendations['tips'].append('تجنب حبس النفس أثناء رفع الأوزان')
        recommendations['tips'].append('ركز على التمارين الهوائية المعتدلة')
    
    if 'joint_problems' in health_conditions:
        recommendations['tips'].append('اختر تمارين قليلة التأثير على المفاصل')
        recommendations['tips'].append('احرص على الإحماء والتبريد')
    
    return recommendations

@app.route('/community')
def community():
    return render_template('community.html')

@app.route('/api/exercises')
def get_exercises():
    """API endpoint to get exercises for workout plans"""
    muscle_group = request.args.get('muscle_group', '')
    difficulty = request.args.get('difficulty', '')
    limit = request.args.get('limit', 50, type=int)
    
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Build query with filters
    query = 'SELECT * FROM admin_exercises WHERE 1=1'
    params = []
    
    if muscle_group:
        query += ' AND muscle_group = ?'
        params.append(muscle_group)
    
    if difficulty:
        query += ' AND difficulty_level = ?'
        params.append(difficulty)
    
    query += ' ORDER BY name_ar LIMIT ?'
    params.append(limit)
    
    cursor.execute(query, params)
    exercises = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    exercises_list = []
    for exercise in exercises:
        exercises_list.append({
            'id': exercise['id'],
            'name_ar': exercise['name_ar'],
            'name_en': exercise['name_en'],
            'muscle_group': exercise['muscle_group'],
            'difficulty_level': exercise['difficulty_level'],
            'instructions_ar': exercise['instructions_ar'],
            'instructions_en': exercise['instructions_en'],
            'sets': exercise['sets'] if exercise['sets'] else '3',
            'reps': exercise['reps'] if exercise['reps'] else '10-12',
            'rest_time': exercise['rest_time'] if exercise['rest_time'] else '60 ثانية'
        })
    
    return jsonify(exercises_list)

@app.route('/admin/messages')
@admin_required
def admin_messages():
    """Admin messages management"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM motivational_messages ORDER BY created_at DESC')
    messages = cursor.fetchall()
    conn.close()
    
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/add', methods=['POST'])
@admin_required
def admin_add_message():
    """Add new motivational message"""
    try:
        data = request.get_json()
        title = data.get('title')
        message = data.get('message')
        category = data.get('category')
        is_active = data.get('is_active', True)
        
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO motivational_messages (title, message, category, is_active)
            VALUES (?, ?, ?, ?)
        ''', (title, message, category, is_active))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم إضافة الرسالة بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في إضافة الرسالة: {str(e)}'})

@app.route('/admin/messages/edit/<int:message_id>', methods=['POST'])
@admin_required
def admin_edit_message(message_id):
    """Edit motivational message"""
    try:
        data = request.get_json()
        title = data.get('title')
        message = data.get('message')
        category = data.get('category')
        is_active = data.get('is_active', True)
        
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE motivational_messages 
            SET title = ?, message = ?, category = ?, is_active = ?
            WHERE id = ?
        ''', (title, message, category, is_active, message_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم تحديث الرسالة بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في تحديث الرسالة: {str(e)}'})

@app.route('/admin/messages/delete/<int:message_id>', methods=['POST'])
@admin_required
def admin_delete_message(message_id):
    """Delete motivational message"""
    try:
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM motivational_messages WHERE id = ?', (message_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم حذف الرسالة بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في حذف الرسالة: {str(e)}'})

@app.route('/admin/settings')
@admin_required
def admin_settings():
    """Admin settings management"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all settings
    cursor.execute('SELECT * FROM dashboard_settings')
    settings_rows = cursor.fetchall()
    
    # Convert to dictionary
    settings = {}
    for setting in settings_rows:
        settings[setting['setting_key']] = setting['setting_value']
    
    conn.close()
    
    return render_template('admin/settings.html', settings=settings)

@app.route('/admin/settings/update', methods=['POST'])
@admin_required
def admin_update_settings():
    """Update dashboard settings"""
    try:
        data = request.get_json()
        
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        # Update each setting
        for key, value in data.items():
            cursor.execute('''
                INSERT OR REPLACE INTO dashboard_settings (setting_key, setting_value)
                VALUES (?, ?)
            ''', (key, str(value)))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'تم حفظ الإعدادات بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في حفظ الإعدادات: {str(e)}'})

@app.route('/admin/statistics')
@admin_required
def admin_statistics():
    """Admin statistics dashboard"""
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get total workout plans
    cursor.execute('SELECT COUNT(*) as count FROM workout_plans')
    total_plans = cursor.fetchone()['count']
    
    # Get today's plans
    cursor.execute('''
        SELECT COUNT(*) as count FROM workout_plans 
        WHERE DATE(created_at) = DATE('now')
    ''')
    today_plans = cursor.fetchone()['count']
    
    # Get this week's plans
    cursor.execute('''
        SELECT COUNT(*) as count FROM workout_plans 
        WHERE DATE(created_at) >= DATE('now', '-7 days')
    ''')
    week_plans = cursor.fetchone()['count']
    
    # Calculate daily average
    cursor.execute('''
        SELECT COUNT(*) as count FROM workout_plans 
        WHERE DATE(created_at) >= DATE('now', '-30 days')
    ''')
    month_plans = cursor.fetchone()['count']
    avg_daily = round(month_plans / 30, 1)
    
    # Get goal statistics
    cursor.execute('''
        SELECT goal, COUNT(*) as count 
        FROM workout_plans 
        GROUP BY goal 
        ORDER BY count DESC
    ''')
    goal_stats = cursor.fetchall()
    
    # Calculate percentages
    goal_stats_with_percentage = []
    for stat in goal_stats:
        percentage = (stat['count'] / total_plans * 100) if total_plans > 0 else 0
        goal_stats_with_percentage.append({
            'goal': stat['goal'],
            'count': stat['count'],
            'percentage': percentage
        })
    
    # Get fitness level statistics
    cursor.execute('''
        SELECT fitness_level, COUNT(*) as count 
        FROM workout_plans 
        GROUP BY fitness_level 
        ORDER BY count DESC
    ''')
    fitness_stats = cursor.fetchall()
    
    # Get recent activity
    cursor.execute('''
        SELECT goal, fitness_level, bmi, created_at 
        FROM workout_plans 
        ORDER BY created_at DESC 
        LIMIT 10
    ''')
    recent_activity = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin/statistics.html',
                         total_plans=total_plans,
                         today_plans=today_plans,
                         week_plans=week_plans,
                         avg_daily=avg_daily,
                         goal_stats=goal_stats_with_percentage,
                         fitness_stats=fitness_stats,
                         recent_activity=recent_activity)

@app.route('/admin/api/notifications')
def admin_api_notifications():
    """API endpoint for admin notifications"""
    # Check if user is authenticated
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Authentication required', 'authenticated': False}), 401
    
    # For now, return empty notifications
    return jsonify({
        'notifications': [],
        'count': 0
    })

@app.route('/admin/api/statistics')
def admin_api_statistics():
    """API endpoint for real-time statistics"""
    # Check if user is authenticated
    if 'admin_logged_in' not in session:
        return jsonify({'error': 'Authentication required', 'authenticated': False}), 401
    
    conn = sqlite3.connect('fitness_app.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get basic statistics
    cursor.execute('SELECT COUNT(*) as count FROM workout_plans')
    total_plans = cursor.fetchone()['count']
    
    cursor.execute('''
        SELECT COUNT(*) as count FROM workout_plans 
        WHERE DATE(created_at) = DATE('now')
    ''')
    today_plans = cursor.fetchone()['count']
    
    cursor.execute('''
        SELECT COUNT(*) as count FROM workout_plans 
        WHERE DATE(created_at) >= DATE('now', '-7 days')
    ''')
    week_plans = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM admin_exercises')
    total_exercises = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM motivational_messages WHERE is_active = 1')
    active_messages = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total_plans': total_plans,
        'today_plans': today_plans,
        'week_plans': week_plans,
        'total_exercises': total_exercises,
        'active_messages': active_messages
    })

@app.route('/system-tester')
def system_tester():
    """صفحة اختبار النظام الشامل"""
    return render_template('system_tester.html')

# تحقق البيانات في الخادم (Back-End): دالة التحقق من صحة البيانات
def validate_user_data(data):
    """التحقق من أن كل الحقول المطلوبة ليست None أو فارغة أو نصوص تحتوي فقط على مسافات"""
    required_fields = ['name', 'age', 'gender', 'goal', 'weight', 'height', 'level', 'days_per_week', 'workout_split']
    
    for field in required_fields:
        if field not in data:
            return False, f'الحقل مفقود: {field}'
        
        value = data[field]
        
        # التحقق من القيم الفارغة أو None
        if value is None:
            return False, f'الحقل فارغ: {field}'
        
        # التحقق من النصوص الفارغة أو التي تحتوي على مسافات فقط
        if isinstance(value, str) and value.strip() == '':
            return False, f'الحقل فارغ: {field}'
        
        # التحقق من القيم الرقمية
        if field in ['age', 'weight', 'height', 'days_per_week']:
            try:
                num_value = float(value)
                if num_value <= 0:
                    return False, f'قيمة غير صحيحة للحقل: {field}'
            except (ValueError, TypeError):
                return False, f'قيمة غير رقمية للحقل: {field}'
    
    # التحقق من النطاقات المقبولة
    try:
        age = int(data['age'])
        if age < 16 or age > 80:
            return False, 'العمر يجب أن يكون بين 16 و 80 سنة'
        
        weight = float(data['weight'])
        if weight < 30 or weight > 300:
            return False, 'الوزن يجب أن يكون بين 30 و 300 كيلو'
        
        height = float(data['height'])
        if height < 120 or height > 250:
            return False, 'الطول يجب أن يكون بين 120 و 250 سم'
        
        days = int(data['days_per_week'])
        if days < 1 or days > 7:
            return False, 'عدد أيام التمرين يجب أن يكون بين 1 و 7'
            
    except (ValueError, TypeError):
        return False, 'قيم غير صحيحة في البيانات الرقمية'
    
    return True, 'البيانات صحيحة'

@app.route('/api/generate-smart-workout-plan', methods=['POST'])
def generate_smart_workout_plan():
    """API endpoint لتوليد خطة تمارين ذكية مخصصة"""
    try:
        data = request.get_json()
        
        # تحقق البيانات في الخادم (Back-End): التحقق من صحة البيانات المرسلة
        is_valid, error_message = validate_user_data(data)
        if not is_valid:
            return jsonify({
                "error": "يرجى إكمال جميع البيانات الشخصية قبل المتابعة"
            }), 400
        
        # إنشاء خطة التمارين المخصصة
        workout_plan = create_personalized_workout_plan(data)
        
        # حفظ الخطة في قاعدة البيانات
        save_workout_plan_to_db(data, workout_plan)
        
        return jsonify({
            'success': True,
            'plan': workout_plan,
            'message': 'تم إنشاء خطة التمارين بنجاح'
        })
        
    except Exception as e:
        print(f"Error generating workout plan: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في إنشاء خطة التمارين: {str(e)}'
        }), 500

def create_personalized_workout_plan(user_data):
    """إنشاء خطة تمارين مخصصة بناءً على بيانات المستخدم"""
    
    # قاعدة بيانات التمارين
    exercises_db = {
        'weight_loss': {
            'beginner': [
                {'name': 'المشي السريع', 'target_muscle': 'كامل الجسم', 'sets': 1, 'reps': '20-30 دقيقة', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=kLh-uczlPLg', 'tips': 'ابدأ ببطء وزد السرعة تدريجياً'},
                {'name': 'تمرين القرفصاء', 'target_muscle': 'الأرجل والمؤخرة', 'sets': 3, 'reps': '10-12', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=aclHkVaku9U', 'tips': 'حافظ على استقامة الظهر'},
                {'name': 'تمرين الضغط المعدل', 'target_muscle': 'الصدر والذراعين', 'sets': 3, 'reps': '8-10', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=IODxDxX7oi4', 'tips': 'ابدأ من الركبتين إذا كان صعباً'},
                {'name': 'تمرين البلانك', 'target_muscle': 'البطن والجذع', 'sets': 3, 'reps': '20-30 ثانية', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=pSHjTRCQxIw', 'tips': 'حافظ على استقامة الجسم'},
                {'name': 'تمرين الجسر', 'target_muscle': 'المؤخرة والظهر', 'sets': 3, 'reps': '12-15', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=OUgsJ8-Vi0E', 'tips': 'اضغط على المؤخرة في الأعلى'}
            ],
            'intermediate': [
                {'name': 'الجري المتقطع', 'target_muscle': 'كامل الجسم', 'sets': 1, 'reps': '25-35 دقيقة', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=6wfKdBr8pGE', 'tips': 'تناوب بين الجري السريع والبطيء'},
                {'name': 'تمرين القرفصاء بالقفز', 'target_muscle': 'الأرجل والمؤخرة', 'sets': 4, 'reps': '12-15', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=A2jzBMNrXyY', 'tips': 'اهبط بهدوء بعد القفز'},
                {'name': 'تمرين الضغط العادي', 'target_muscle': 'الصدر والذراعين', 'sets': 4, 'reps': '12-15', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=IODxDxX7oi4', 'tips': 'حافظ على استقامة الجسم'},
                {'name': 'تمرين الجبل المتسلق', 'target_muscle': 'البطن والجذع', 'sets': 4, 'reps': '20-30', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=kLh-uczlPLg', 'tips': 'حافظ على سرعة ثابتة'},
                {'name': 'تمرين البيربي', 'target_muscle': 'كامل الجسم', 'sets': 3, 'reps': '8-12', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=dZgVxmf6jkA', 'tips': 'خذ راحة قصيرة بين التكرارات'}
            ]
        },
        'muscle_building': {
            'beginner': [
                {'name': 'تمرين القرفصاء', 'target_muscle': 'الأرجل والمؤخرة', 'sets': 4, 'reps': '8-12', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=aclHkVaku9U', 'tips': 'ابدأ بوزن خفيف وزد تدريجياً'},
                {'name': 'تمرين الضغط', 'target_muscle': 'الصدر والذراعين', 'sets': 4, 'reps': '8-12', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=IODxDxX7oi4', 'tips': 'ركز على الحركة البطيئة والمتحكم بها'},
                {'name': 'تمرين السحب', 'target_muscle': 'الظهر والذراعين', 'sets': 4, 'reps': '6-10', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=eGo4IYlbE5g', 'tips': 'استخدم مساعدة إذا لزم الأمر'},
                {'name': 'تمرين الديدليفت', 'target_muscle': 'الظهر والأرجل', 'sets': 4, 'reps': '8-10', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=op9kVnSso6Q', 'tips': 'حافظ على استقامة الظهر'},
                {'name': 'تمرين الضغط العلوي', 'target_muscle': 'الأكتاف والذراعين', 'sets': 3, 'reps': '8-12', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=qEwKCR5JCog', 'tips': 'لا تضغط الأوزان خلف الرأس'}
            ],
            'intermediate': [
                {'name': 'تمرين القرفصاء بالبار', 'target_muscle': 'الأرجل والمؤخرة', 'sets': 4, 'reps': '6-10', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=ultWZbUMPL8', 'tips': 'استخدم حزام الأمان للأوزان الثقيلة'},
                {'name': 'تمرين البنش برس', 'target_muscle': 'الصدر والذراعين', 'sets': 4, 'reps': '6-10', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=rT7DgCr-3pg', 'tips': 'استخدم مساعد للأمان'},
                {'name': 'تمرين السحب بالبار', 'target_muscle': 'الظهر والذراعين', 'sets': 4, 'reps': '6-10', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=eGo4IYlbE5g', 'tips': 'ركز على عضلات الظهر'},
                {'name': 'تمرين الديدليفت بالبار', 'target_muscle': 'الظهر والأرجل', 'sets': 4, 'reps': '5-8', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=op9kVnSso6Q', 'tips': 'ابدأ بوزن خفيف وتعلم التقنية'},
                {'name': 'تمرين الضغط العلوي بالدمبل', 'target_muscle': 'الأكتاف والذراعين', 'sets': 4, 'reps': '8-12', 'difficulty': 'متوسط', 'video': 'https://www.youtube.com/watch?v=qEwKCR5JCog', 'tips': 'حافظ على ثبات الجذع'}
            ]
        },
        'weight_gain': {
            'beginner': [
                {'name': 'تمرين القرفصاء', 'target_muscle': 'الأرجل والمؤخرة', 'sets': 4, 'reps': '10-15', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=aclHkVaku9U', 'tips': 'ركز على زيادة الوزن تدريجياً'},
                {'name': 'تمرين الضغط', 'target_muscle': 'الصدر والذراعين', 'sets': 4, 'reps': '10-15', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=IODxDxX7oi4', 'tips': 'أضف تكرارات إضافية كلما أمكن'},
                {'name': 'تمرين الصفوف', 'target_muscle': 'الظهر والذراعين', 'sets': 4, 'reps': '10-15', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=poa_kAQ5J8s', 'tips': 'اسحب إلى الصدر وليس البطن'},
                {'name': 'تمرين الطعنات', 'target_muscle': 'الأرجل والمؤخرة', 'sets': 3, 'reps': '12-15 لكل رجل', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=QOVaHwm-Q6U', 'tips': 'حافظ على التوازن'},
                {'name': 'تمرين الضغط العلوي', 'target_muscle': 'الأكتاف والذراعين', 'sets': 3, 'reps': '10-15', 'difficulty': 'مبتدئ', 'video': 'https://www.youtube.com/watch?v=qEwKCR5JCog', 'tips': 'ابدأ بأوزان خفيفة'}
            ]
        }
    }
    
    # اختيار التمارين المناسبة
    goal = user_data.get('goal', 'weight_loss')
    level = user_data.get('level', 'beginner')
    days_per_week = int(user_data.get('days_per_week', 3))
    
    # الحصول على قائمة التمارين
    available_exercises = exercises_db.get(goal, {}).get(level, exercises_db['weight_loss']['beginner'])
    
    # إنشاء خطة أسبوعية
    weekly_plan = []
    exercises_per_day = len(available_exercises) // days_per_week if days_per_week > 0 else 3
    exercises_per_day = max(3, min(5, exercises_per_day))  # بين 3-5 تمارين في اليوم
    
    for day in range(days_per_week):
        day_exercises = []
        start_idx = (day * exercises_per_day) % len(available_exercises)
        
        for i in range(exercises_per_day):
            exercise_idx = (start_idx + i) % len(available_exercises)
            exercise = available_exercises[exercise_idx].copy()
            
            # تعديل التكرارات حسب المستوى
            if level == 'beginner':
                if 'sets' in exercise:
                    exercise['sets'] = max(2, exercise['sets'] - 1)
            elif level == 'advanced':
                if 'sets' in exercise:
                    exercise['sets'] = exercise['sets'] + 1
            
            day_exercises.append(exercise)
        
        weekly_plan.append({
            'day': day + 1,
            'exercises': day_exercises
        })
    
    # إنشاء النصائح العامة
    general_tips = generate_general_tips(goal, level)
    
    # إنشاء أسباب عدم الاستمرار والحلول
    reasons_for_quitting = generate_quit_reasons_and_solutions(user_data)
    
    return {
        'goal': goal,
        'level': level,
        'days_per_week': days_per_week,
        'plan': weekly_plan,
        'general_tips': general_tips,
        'reasons_for_quitting': reasons_for_quitting
    }

def generate_general_tips(goal, level):
    """إنشاء نصائح عامة حسب الهدف والمستوى"""
    tips = {
        'weight_loss': [
            'اشرب 2-3 لتر ماء يومياً لتحفيز عملية الحرق',
            'تناول وجبات صغيرة ومتكررة كل 3-4 ساعات',
            'مارس الكارديو 3-4 مرات أسبوعياً لمدة 20-30 دقيقة',
            'احصل على 7-8 ساعات نوم يومياً',
            'تجنب السكريات والمشروبات الغازية',
            'تناول البروتين في كل وجبة للشعور بالشبع'
        ],
        'muscle_building': [
            'تناول 1.6-2.2 جرام بروتين لكل كيلو من وزن الجسم',
            'احصل على راحة كافية بين التمارين (48-72 ساعة)',
            'زد الأوزان تدريجياً كل أسبوع',
            'تناول وجبة غنية بالبروتين والكربوهيدرات بعد التمرين',
            'احصل على 7-9 ساعات نوم للتعافي العضلي',
            'اشرب الماء بكثرة قبل وأثناء وبعد التمرين'
        ],
        'weight_gain': [
            'تناول سعرات حرارية أكثر مما تحرق بـ 300-500 سعرة',
            'تناول 5-6 وجبات صغيرة بدلاً من 3 وجبات كبيرة',
            'أضف الدهون الصحية مثل المكسرات والأفوكادو',
            'اشرب العصائر الطبيعية والحليب بين الوجبات',
            'مارس تمارين القوة لبناء العضلات وليس الدهون',
            'تجنب شرب الماء قبل الوجبات مباشرة'
        ]
    }
    
    base_tips = tips.get(goal, tips['weight_loss'])
    
    # إضافة نصائح خاصة بالمستوى
    if level == 'beginner':
        base_tips.extend([
            'ابدأ ببطء ولا تتعجل النتائج',
            'تعلم التقنية الصحيحة قبل زيادة الأوزان',
            'استمع لجسمك وخذ راحة عند الحاجة'
        ])
    elif level == 'advanced':
        base_tips.extend([
            'غير روتين التمارين كل 4-6 أسابيع',
            'استخدم تقنيات متقدمة مثل الدروب سيت',
            'راقب تقدمك بدقة وسجل الأوزان'
        ])
    
    return base_tips[:8]  # إرجاع أول 8 نصائح

def generate_quit_reasons_and_solutions(user_data):
    """إنشاء أسباب عدم الاستمرار والحلول المناسبة"""
    common_reasons = [
        {
            'reason': 'قلة الوقت',
            'solution': 'اختر تمارين سريعة وعالية الكثافة (15-20 دقيقة) أو مارس التمرين في المنزل'
        },
        {
            'reason': 'الملل من التمارين',
            'solution': 'غير التمارين كل أسبوعين أو أضف موسيقى محفزة أو مارس مع صديق'
        },
        {
            'reason': 'عدم رؤية نتائج سريعة',
            'solution': 'كن صبوراً، النتائج تحتاج 4-6 أسابيع للظهور، التقط صوراً لمتابعة التقدم'
        },
        {
            'reason': 'التعب والإرهاق',
            'solution': 'احصل على نوم كافي، تناول طعاماً صحياً، وابدأ بتمارين خفيفة'
        },
        {
            'reason': 'عدم وجود دافع',
            'solution': 'ضع أهدافاً قصيرة المدى، كافئ نفسك عند تحقيقها، وابحث عن شريك تمرين'
        }
    ]
    
    # إضافة أسباب خاصة حسب البيانات
    level = user_data.get('level', 'beginner')
    if level == 'beginner':
        common_reasons.append({
            'reason': 'الخوف من الإصابة',
            'solution': 'ابدأ بتمارين بسيطة، تعلم التقنية الصحيحة، واطلب المساعدة من مدرب'
        })
    
    days_per_week = int(user_data.get('days_per_week', 3))
    if days_per_week >= 5:
        common_reasons.append({
            'reason': 'الإفراط في التمرين',
            'solution': 'خذ يوم راحة كامل أسبوعياً، واستمع لجسمك لتجنب الإرهاق'
        })
    
    return common_reasons[:6]  # إرجاع أول 6 أسباب

def save_workout_plan_to_db(user_data, workout_plan):
    """حفظ خطة التمارين في قاعدة البيانات"""
    try:
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        
        # حساب BMI
        weight = float(user_data.get('weight', 70))
        height = float(user_data.get('height', 170)) / 100  # تحويل إلى متر
        bmi = round(weight / (height * height), 1)
        
        # إدراج البيانات
        cursor.execute('''
            INSERT INTO workout_plans (
                goal, fitness_level, days_per_week, weight, height, bmi,
                plan_data, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_data.get('goal'),
            user_data.get('level'),
            user_data.get('days_per_week'),
            weight,
            user_data.get('height'),
            bmi,
            json.dumps(workout_plan, ensure_ascii=False),
            datetime.datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Error saving workout plan to database: {str(e)}")

@app.route('/api/save-workout-plan', methods=['POST'])
def save_workout_plan():
    """API endpoint لحفظ خطة التمارين"""
    try:
        data = request.get_json()
        plan = data.get('plan')
        user_data = data.get('userData')
        
        if not plan or not user_data:
            return jsonify({
                'success': False,
                'message': 'بيانات غير مكتملة'
            }), 400
        
        # حفظ الخطة في قاعدة البيانات
        save_workout_plan_to_db(user_data, plan)
        
        return jsonify({
            'success': True,
            'message': 'تم حفظ خطة التمارين بنجاح'
        })
        
    except Exception as e:
        print(f"Error saving workout plan: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في حفظ الخطة: {str(e)}'
        }), 500

@app.route('/personalized-workout-test')
def personalized_workout_test():
    """Test page for the personalized workout plan generator"""
    return render_template('personalized_workout_test.html')

@app.route('/advanced-workout-test')
def advanced_workout_test():
    """Test page for the advanced workout plan generator"""
    return render_template('advanced_workout_test.html')

@app.route('/advanced-workout-test-simple')
def advanced_workout_test_simple():
    """Simple test page for the advanced workout plan generator with default data"""
    return render_template('advanced_workout_test_simple.html')

@app.route('/unified-workout-test')
def unified_workout_test():
    """Unified test page for both personalized and advanced workout plan generators"""
    return render_template('unified_workout_test.html')

@app.route('/api/generate-personalized-workout-plan', methods=['POST'])
def generate_personalized_workout_plan():
    """
    Professional fitness trainer and certified nutritionist endpoint
    Creates personalized 4-week workout plans based on comprehensive user data
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'age', 'gender', 'weight', 'height', 'goal', 'level', 'days_per_week', 'equipment']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'البيانات المطلوبة مفقودة: {", ".join(missing_fields)}',
                'missing_fields': missing_fields
            }), 400
        
        # Initialize the personalized workout generator
        generator = PersonalizedWorkoutGenerator()
        
        # Generate the personalized workout plan
        workout_plan = generator.generate_workout_plan(data)
        
        # Check if there was an error in generation
        if 'error' in workout_plan:
            return jsonify({
                'success': False,
                'message': workout_plan['error'],
                'required_fields': workout_plan.get('required_fields', [])
            }), 400
        
        # Save the plan to database for tracking
        try:
            save_workout_plan_to_db(data, workout_plan)
        except Exception as save_error:
            print(f"Warning: Could not save workout plan to database: {save_error}")
            # Continue without failing the request
        
        return jsonify({
            'success': True,
            'message': 'تم إنشاء خطة التمارين الشخصية بنجاح',
            'plan': workout_plan
        })
        
    except Exception as e:
        print(f"Error generating personalized workout plan: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في إنشاء الخطة الشخصية: {str(e)}'
        }), 500

@app.route('/api/generate-advanced-workout-plan', methods=['POST'])
def generate_advanced_workout_plan():
    """
    Advanced AI-powered fitness trainer and nutritionist endpoint
    Creates comprehensive personalized workout and nutrition plans with weekly modifications
    """
    print("=== Advanced Workout Plan Request Received ===")
    try:
        data = request.get_json()
        print(f"Received data: {data}")
        
        # Validate required fields for advanced plan
        required_fields = [
            'name', 'age', 'gender', 'weight', 'height', 'goal', 'level', 
            'days_per_week', 'equipment', 'activity_level', 'sleep_hours',
            'stress_level', 'dietary_preferences'
        ]
        
        missing_fields = [field for field in required_fields if not data.get(field)]
        print(f"Missing fields: {missing_fields}")
        
        if missing_fields:
            print("Returning error for missing fields")
            return jsonify({
                'success': False,
                'message': f'البيانات المطلوبة مفقودة للنظام المطور: {", ".join(missing_fields)}',
                'missing_fields': missing_fields,
                'note': 'النظام المطور يتطلب بيانات أكثر تفصيلاً لتقديم خطة شاملة'
            }), 400
        
        print("All required fields present, generating plan...")
        
        # Initialize the advanced workout generator
        generator = AdvancedWorkoutGenerator()
        
        # Generate the comprehensive plan
        print("Calling generate_comprehensive_plan...")
        advanced_plan = generator.generate_comprehensive_plan(data)
        print(f"Generated plan keys: {list(advanced_plan.keys()) if isinstance(advanced_plan, dict) else 'Not a dict'}")
        
        # Check if there was an error in generation
        if 'error' in advanced_plan:
            print(f"Error in plan generation: {advanced_plan['error']}")
            return jsonify({
                'success': False,
                'message': advanced_plan['error'],
                'required_fields': advanced_plan.get('required_fields', [])
            }), 400
        
        # Save the advanced plan to database
        try:
            save_workout_plan_to_db(data, advanced_plan)
            print("Plan saved to database successfully")
        except Exception as save_error:
            print(f"Warning: Could not save advanced workout plan to database: {save_error}")
        
        print("Returning successful response...")
        response_data = {
            'success': True,
            'message': 'تم إنشاء الخطة المطورة الشاملة بنجاح',
            'plan': advanced_plan,
            'features': [
                'خطة تمارين مع تعديل أسبوعي',
                'نصائح غذائية مخصصة',
                'تمارين بديلة',
                'تحفيز شخصي',
                'تحليل مؤشرات الصحة',
                'اقتراحات المكملات الغذائية'
            ]
        }
        print(f"Response data prepared, size: {len(str(response_data))}")
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Exception in generate_advanced_workout_plan: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': f'حدث خطأ في إنشاء الخطة المطورة: {str(e)}'
        }), 500

@app.route('/api/system-health')
def system_health():
    """API endpoint لفحص صحة النظام"""
    try:
        # فحص قاعدة البيانات
        conn = sqlite3.connect('fitness_app.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        db_status = True
        conn.close()
    except:
        db_status = False
    
    # فحص الملفات الأساسية
    essential_files = [
        'templates/index.html',
        'templates/your_plan_your_goal.html',
        'static/css/style.css'
    ]
    
    files_status = {}
    for file_path in essential_files:
        files_status[file_path] = os.path.exists(file_path)
    
    return jsonify({
        'database': db_status,
        'files': files_status,
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'healthy' if db_status and all(files_status.values()) else 'issues_detected'
    })

if __name__ == '__main__':
    init_db()
    create_default_admin()
    app.run(debug=True)
