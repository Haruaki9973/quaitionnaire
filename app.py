from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'responses.csv'

# 保存用の関数
def save_response(data):
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# 読み込み用の関数
def load_responses():
    try:
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            return list(csv.reader(f))
    except FileNotFoundError:
        return []

@app.route('/')
def index():
    responses = load_responses()
    return render_template('index.html', responses=responses)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    faculty = request.form['faculty']
    department = request.form['department']
    experience = request.form['experience']
    interest = request.form['interest']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    save_response([name, faculty, department, experience, interest, timestamp])
    return redirect(url_for('index'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
