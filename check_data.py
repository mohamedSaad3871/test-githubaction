import sqlite3

# فحص قاعدة البيانات
conn = sqlite3.connect('fitness_app.db')
cursor = conn.cursor()

# فحص التمارين
cursor.execute('SELECT name, muscle_group, difficulty, equipment FROM exercises LIMIT 5')
exercises = cursor.fetchall()
print('عينة من التمارين:')
for ex in exercises:
    print(f'- {ex[0]} | {ex[1]} | صعوبة: {ex[2]} | معدات: {ex[3]}')

print('\n' + '='*50 + '\n')

# فحص الوجبات
cursor.execute('SELECT name, category, calories, protein FROM meals LIMIT 5')
meals = cursor.fetchall()
print('عينة من الوجبات:')
for meal in meals:
    print(f'- {meal[0]} | {meal[1]} | سعرات: {meal[2]} | بروتين: {meal[3]}g')

conn.close()