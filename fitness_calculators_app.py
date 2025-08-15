from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """الصفحة الرئيسية مع الحاسبات الخمس"""
    return render_template('fitness_calculators.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)