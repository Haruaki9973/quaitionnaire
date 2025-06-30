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

def save_all(responses):
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(responses)
        
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

@app.route('/edit/<int:index>', methods=['GET', 'POST'])
def edit(index):
    responses = load_responses()
    if index < 0 or index >= len(responses):
        return redirect(url_for('index'))

    if request.method == 'POST':
        responses[index][0] = request.form['name']
        responses[index][1] = request.form['faculty']
        responses[index][2] = request.form['department']
        responses[index][3] = request.form['experience']
        responses[index][4] = request.form['interest']
        save_all(responses)
        return redirect(url_for('index'))

    response = {
        'name': responses[index][0],
        'faculty': responses[index][1],
        'department': responses[index][2],
        'experience': responses[index][3],
        'interest': responses[index][4]
    }
    return render_template('edit.html', response=response, index=index)



if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
