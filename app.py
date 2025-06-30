from flask import Flask, render_template, request, redirect, url_for, abort
import csv
from datetime import datetime

app = Flask(__name__)

# CSV file path
DATA_FILE = 'responses.csv'

# CSV columns
FIELDNAMES = [
    'id', 'name', 'faculty', 'department', 'experience',
    'interest', 'timestamp', 'likes'
]

# 保存用の関数
def save_response(data):
     exists = os.path.isfile(DATA_FILE)
    with open(DATA_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not exists:
            writer.writeheader()
        writer.writerow(data)

# 読み込み用の関数
def load_responses():
    try:
        with open(DATA_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        return []

# 全データを書き出す関数
def write_responses(responses):
    with open(DATA_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(responses)

# 次のIDを取得する
def get_next_id(responses):
    if not responses:
        return '1'
    return str(max(int(r['id']) for r in responses) + 1)


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
    
    responses = load_responses()
    data = {
        'id': get_next_id(responses),
        'name': name,
        'faculty': faculty,
        'department': department,
        'experience': experience,
        'interest': interest,
        'timestamp': timestamp,
        'likes': '0'
    }
    save_response(data)
    return redirect(url_for('index'))


@app.route('/like/<id>')
def like(id):
    responses = load_responses()
    for r in responses:
        if r['id'] == id:
            r['likes'] = str(int(r.get('likes', 0)) + 1)
            break
    else:
        abort(404)
    write_responses(responses)
    return redirect(url_for('index'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    responses = load_responses()
    target = None
    for r in responses:
        if r['id'] == id:
            target = r
            break
    if target is None:
        abort(404)

    if request.method == 'POST':
        target['name'] = request.form['name']
        target['faculty'] = request.form['faculty']
        target['department'] = request.form['department']
        target['experience'] = request.form['experience']
        target['interest'] = request.form['interest']
        target['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write_responses(responses)
        return redirect(url_for('index'))

    return render_template('edit.html', response=target)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
