from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# DB初期化
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute("INSERT INTO posts (content, timestamp) VALUES (?, ?)", 
                      (content, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()
            return redirect('/')
    
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT content, timestamp FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
