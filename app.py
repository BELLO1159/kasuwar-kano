import os
import sqlite3
from flask import Flask, request, render_template_string

# Initialize Flask App
app = Flask(__name__)

# Database Setup
DB_NAME = 'kasuwar_kano.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            interest TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Run database creation on startup
init_db()

# Website HTML Template
HOME_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kasuwar Kano Agency</title>
    <style>
        * { box-sizing: border-box; font-family: Arial, sans-serif; }
        body { background-color: #f4f6f8; margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
        .card { background: #ffffff; padding: 30px; border-radius: 12px; max-width: 450px; width: 100%; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; }
        h1 { color: #1a5276; margin-bottom: 5px; font-size: 24px; }
        p { color: #666; font-size: 14px; margin-top: 0; }
        hr { border: 0; height: 1px; background: #eee; margin: 20px 0; }
        label { display: block; text-align: left; font-size: 13px; font-weight: bold; color: #444; margin-bottom: 5px; }
        input, select { width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 6px; border: 1px solid #ccc; font-size: 14px; }
        button { width: 100%; background-color: #1a5276; color: white; font-weight: bold; padding: 12px; border: none; border-radius: 6px; font-size: 16px; cursor: pointer; }
        button:hover { background-color: #113851; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Kasuwar Kano Agency</h1>
        <p>Real Estate & Vendor Marketing Platform</p>
        <hr>
        <h3>Register Your Interest</h3>
        <form action="/submit-lead" method="POST">
            <label>Full Name</label>
            <input type="text" name="name" placeholder="Enter full name" required>
            
            <label>Phone / WhatsApp Number</label>
            <input type="tel" name="phone" placeholder="e.g. 08012345678" required>
            
            <label>Service Category</label>
            <select name="interest">
                <option value="Real Estate / Property">Real Estate & Land Installments</option>
                <option value="Vendor Listing">Vendor Catalog / Product Advertising</option>
            </select>
            
            <button type="submit">Submit Information</button>
        </form>
    </div>
</body>
</html>
"""

# Admin Leads Dashboard Template
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kasuwar Kano - Leads Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f8; padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h2 { color: #1a5276; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; font-size: 14px; }
        th { background-color: #1a5276; color: white; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .back-btn { display: inline-block; margin-bottom: 15px; color: #1a5276; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-btn">← Back to Main Form</a>
        <h2>Submitted Leads</h2>
        {% if leads %}
        <table>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Phone Number</th>
                <th>Interest</th>
                <th>Date Submitted</th>
            </tr>
            {% for lead in leads %}
            <tr>
                <td>{{ lead[0] }}</td>
                <td>{{ lead[1] }}</td>
                <td><a href="https://wa.me/{{ lead[2] }}" target="_blank">{{ lead[2] }}</a></td>
                <td>{{ lead[3] }}</td>
                <td>{{ lead[4] }}</td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No leads submitted yet!</p>
        {% endif %}
    </div>
</body>
</html>
"""

# Homepage Route
@app.route('/')
def home():
    return render_template_string(HOME_HTML)

# Lead Capture Route
@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    name = request.form.get('name')
    phone = request.form.get('phone')
    interest = request.form.get('interest')

    if name and phone:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO leads (name, phone, interest) VALUES (?, ?, ?)", (name, phone, interest))
        conn.commit()
        conn.close()
        
        success_html = f"""
        <!DOCTYPE html>
        <html>
        <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
        <body style="font-family: Arial; text-align: center; padding: 40px; background: #f4f6f8;">
            <div style="background: white; padding: 30px; border-radius: 12px; max-width: 400px; margin: auto;">
                <h2 style="color: #27ae60;">Submission Received!</h2>
                <p>Thank you, <b>{name}</b>. We will contact you at <b>{phone}</b> shortly regarding {interest}.</p>
                <a href="/" style="display: inline-block; margin-top: 15px; text-decoration: none; color: #1a5276; font-weight: bold;">← Return Home</a>
            </div>
        </body>
        </html>
        """
        return render_template_string(success_html)
    
    return "Error: Please fill in all fields.", 400

# Admin Route to View All Submitted Data
@app.route('/admin')
def view_leads():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, interest, created_at FROM leads ORDER BY id DESC")
    leads = cursor.fetchall()
    conn.close()
    return render_template_string(ADMIN_HTML, leads=leads)

# Server Entry Point for Render
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
