# app.py
from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3
import pandas as pd
from datetime import datetime

app = Flask(__name__)
DATABASE = 'materials.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS materials
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  quantity INTEGER NOT NULL,
                  unit TEXT NOT NULL,
                  description TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM materials ORDER BY name')
    materials = c.fetchall()
    conn.close()
    return render_template('index.html', materials=materials)

@app.route('/add', methods=['POST'])
def add_material():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    unit = request.form['unit']
    description = request.form.get('description', '')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO materials (name, quantity, unit, description) VALUES (?, ?, ?, ?)',
              (name, quantity, unit, description))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit_material(id):
    quantity = int(request.form['quantity'])
    description = request.form.get('description', '')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE materials SET quantity = ?, description = ? WHERE id = ?',
              (quantity, description, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_material(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM materials WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/export')
def export_to_excel():
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query('SELECT * FROM materials', conn)
    conn.close()
    
    filename = f'materials_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
    df.to_excel(filename, index=False)
    
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
