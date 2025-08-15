#!/usr/bin/env python3
"""
ملف اختبار API مولد خطط التمارين
تشغيل الاختبارات: python test_api.py
"""

import requests
import json

BASE_URL = 'http://localhost:5001/api'

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
    print("🚀 بدء اختبارات API مولد خطط التمارين\n")
    
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