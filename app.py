import os
import sqlite3
from flask import Flask, request, render_template_string, redirect, url_for

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
            whatsapp TEXT,
            property_type TEXT,
            location TEXT,
            budget TEXT,
            message TEXT,
            status TEXT DEFAULT 'New',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Main Homepage Template (Pink, Black, White Theme)
HOME_HTML = """
<!DOCTYPE html>
<html lang="ha">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kasuwar Kano Estate Agency</title>
    <style>
        :root {
            --pink: #ff1493;
            --pink-hover: #e00b82;
            --black: #0a0a0a;
            --dark-card: #161616;
            --white: #ffffff;
            --gray: #f5f5f5;
        }
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--black); color: var(--white); margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; }
        
        .hero { text-align: center; padding: 50px 20px; max-width: 700px; width: 100%; }
        .hero h1 { color: var(--white); font-size: 32px; margin-bottom: 10px; letter-spacing: 1px; }
        .hero h1 span { color: var(--pink); }
        .hero p { color: #dddddd; font-size: 18px; margin-bottom: 30px; font-weight: 300; }
        
        .cta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px; }
        .cta-btn { background: var(--dark-card); border: 2px solid var(--pink); color: var(--white); padding: 18px 10px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; text-align: center; transition: 0.3s; box-shadow: 0 4px 15px rgba(255,20,147,0.2); }
        .cta-btn:hover { background: var(--pink); color: var(--black); }

        .container { max-width: 600px; width: 92%; background: var(--dark-card); padding: 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(255,20,147,0.15); margin-bottom: 40px; border: 1px solid #333; }
        h2 { color: var(--pink); text-align: center; margin-top: 0; font-size: 22px; }
        
        label { display: block; text-align: left; font-size: 13px; font-weight: bold; color: #ccc; margin-bottom: 6px; }
        input, select, textarea { width: 100%; padding: 14px; margin-bottom: 16px; border-radius: 8px; border: 1px solid #444; background: #000; color: var(--white); font-size: 15px; }
        input:focus, select:focus, textarea:focus { border-color: var(--pink); outline: none; }
        
        .submit-btn { width: 100%; background-color: var(--pink); color: var(--black); font-weight: 800; padding: 16px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; }
        .submit-btn:hover { background-color: var(--pink-hover); color: var(--white); }

        .footer-info { text-align: center; padding: 30px 20px 60px 20px; color: #aaa; font-size: 14px; border-top: 1px solid #222; width: 100%; max-width: 600px; }
        .footer-info p { margin: 8px 0; }
        .footer-info a { color: var(--pink); text-decoration: none; }

        .whatsapp-float { position: fixed; bottom: 25px; right: 25px; background-color: #25d366; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); z-index: 1000; text-decoration: none; transition: transform 0.3s; }
        .whatsapp-float:hover { transform: scale(1.1); }
    </style>
</head>
<body>

    <div class="hero">
        <h1>Kasuwar Kano <span>Estate Agency</span></h1>
        <p>Mallaki Gida Ko Fili Cikin Sauƙin Biya</p>
        
        <div class="cta-grid">
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='House'">🏡 Ina Neman Gida</a>
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='Land'">🌍 Ina Neman Fili</a>
        </div>
    </div>

    <div class="container" id="request-form">
        <h2>Tura Buƙatar Gida Ko Fili</h2>
        <form action="/submit-lead" method="POST">
            <label>Full Name (Cikakken Sunanka)</label>
            <input type="text" name="name" placeholder="Misali: Ibrahim Sani" required>
            
            <label>Phone Number (Lambar Wayar Kira)</label>
            <input type="tel" name="phone" placeholder="Misali: 09066073407" required>
            
            <label>WhatsApp Number (Lambar WhatsApp)</label>
            <input type="tel" name="whatsapp" placeholder="Misali: 09066073407">
            
            <label>Property Type (Nau'in Abin da Kake Nema)</label>
            <select name="property_type" id="property_type" required>
                <option value="House">Gida (House)</option>
                <option value="Land">Fili (Land)</option>
            </select>
            
            <label>Preferred Location (Wurin da Kake So)</label>
            <input type="text" name="location" placeholder="Misali: Goron Dutse, Kano">
            
            <label>Budget (Kudin da Kake Da Shi)</label>
            <input type="text" name="budget" placeholder="Misali: ₦2,000,000">
            
            <label>Additional Message (Bayani Ƙari)</label>
            <textarea name="message" rows="3" placeholder="Rubuta duk wani bayani da kake buƙata..."></textarea>
            
            <button type="submit" class="submit-btn">TURA BUKATA</button>
        </form>
    </div>

    <div class="container" style="border: 1px dashed var(--pink); text-align: center;">
        <h3 style="color: var(--pink); margin-top:0;">Diyar Kayayyaki & Tsarin Biya</h3>
        <p style="font-size: 13px; color: #bbb;">Ba da jimawa ba za a sanya cikakkun hotuna, Farashin Gidaje/Filaye, da kuma tsarin biyar kason wata-wata (Monthly Payment Plans) a nan kai tsaye.</p>
    </div>

    <div class="footer-info">
        <p>📞 <b>09066073407</b></p>
        <p>📍 <b>Goron Dutse, Maiyari Plaza, Kano</b></p>
        <p style="margin-top: 15px;"><a href="/admin" style="color: var(--pink); font-size: 13px; font-weight: bold;">🔐 Admin Panel Dashboard</a></p>
    </div>

    <a href="https://wa.me/2349066073407?text=Assalamu%20Alaikum,%20Ina%20son%20neman%20bayani%20game%20da%20Gidaje%20ko%20Filaye." class="whatsapp-float" target="_blank" title="Chat on WhatsApp">
        💬
    </a>

</body>
</html>
"""

# Success Response Template
SUCCESS_HTML = """
<!DOCTYPE html>
<html lang="ha">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>An Tura Buƙata - Kasuwar Kano</title>
    <style>
        body { background-color: #0a0a0a; color: #fff; font-family: sans-serif; text-align: center; padding: 60px 20px; }
        .card { background: #161616; padding: 40px; border-radius: 16px; max-width: 450px; margin: auto; border: 1px solid #ff1493; }
        h2 { color: #ff1493; }
        p { color: #ccc; font-size: 16px; line-height: 1.5; }
        a { display: inline-block; margin-top: 20px; background: #ff1493; color: #000; padding: 12px 25px; border-radius: 8px; text-decoration: none; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Mun Karɓi Buƙatarka!</h2>
        <p>Mun karɓi buƙatarka. Za mu tuntube ka nan ba da jimawa ba.</p>
        <a href="/">Koma Shafin Farko</a>
    </div>
</body>
</html>
"""

# Upgraded Professional Admin Panel Template (Pink, Black, White Theme with Welcome Header)
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Kasuwar Kano Estate Agency</title>
    <style>
        :root {
            --pink: #ff1493;
            --pink-hover: #e00b82;
            --black: #0a0a0a;
            --dark-card: #161616;
            --white: #ffffff;
        }
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--black); color: var(--white); padding: 20px; margin: 0; }
        .wrapper { max-width: 1100px; margin: auto; }
        
        /* Admin Header */
        .admin-header { background: var(--dark-card); padding: 25px; border-radius: 16px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(255,20,147,0.1); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 25px; }
        .admin-header h1 { color: var(--pink); margin: 0; font-size: 24px; }
        .admin-header p { color: #aaa; margin: 5px 0 0 0; font-size: 14px; }
        .back-btn { background: #222; border: 1px solid var(--pink); color: var(--white); padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 13px; transition: 0.3s; }
        .back-btn:hover { background: var(--pink); color: var(--black); }

        /* Content Table Card */
        .table-card { background: var(--dark-card); padding: 20px; border-radius: 16px; border: 1px solid #333; overflow-x: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h3 { color: var(--white); margin-top: 0; border-bottom: 1px solid #333; padding-bottom: 12px; font-size: 18px; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; min-width: 800px; }
        th, td { border: 1px solid #2a2a2a; padding: 14px; text-align: left; }
        th { background-color: #222; color: var(--pink); text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }
        tr:nth-child(even) { background-color: #121212; }
        tr:hover { background-color: #1a1a1a; }
        
        .actions a { display: inline-block; padding: 6px 12px; margin: 3px 2px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 11px; transition: 0.2s; }
        .btn-contacted { background: #f39c12; color: #000; }
        .btn-contacted:hover { opacity: 0.8; }
        .btn-completed { background: #27ae60; color: #fff; }
        .btn-completed:hover { opacity: 0.8; }
        .btn-delete { background: #c0392b; color: #fff; }
        .btn-delete:hover { opacity: 0.8; }
        
        .badge { padding: 5px 10px; border-radius: 6px; font-weight: bold; font-size: 11px; display: inline-block; text-align: center; }
        .status-New { background: #3498db; color: #fff; }
        .status-Contacted { background: #f39c12; color: #000; }
        .status-Completed { background: #27ae60; color: #fff; }
        
        .empty-state { text-align: center; padding: 40px; color: #777; font-size: 15px; }
    </style>
</head>
<body>
    <div class="wrapper">
        <div class="admin-header">
            <div>
                <h1>Kasuwar Kano Dashboard</h1>
                <p>Welcome to Admin Panel — Goron Dutse, Maiyari Plaza, Kano</p>
            </div>
            <a href="/" class="back-btn">← View Live Website</a>
        </div>

        <div class="table-card">
            <h3>Customer Requests & Inquiries</h3>
            {% if leads %}
            <table>
                <tr>
                    <th>ID</th>
                    <th>Customer Name</th>
                    <th>Phone / WhatsApp</th>
                    <th>Type</th>
                    <th>Location</th>
                    <th>Budget</th>
                    <th>Message</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Actions</th>
                </tr>
                {% for lead in leads %}
                <tr>
                    <td><b>#{{ lead[0] }}</b></td>
                    <td><span style="font-size: 15px; font-weight: bold; color: var(--white);">{{ lead[1] }}</span></td>
                    <td>
                        Phone: <a href="tel:{{ lead[2] }}" style="color: var(--pink); text-decoration: none;">{{ lead[2] }}</a><br>
                        WA: <a href="https://wa.me/234{{ lead[3] }}" target="_blank" style="color: #25d366; text-decoration: none;">{{ lead[3] }}</a>
                    </td>
                    <td><span style="color: var(--pink); font-weight: bold;">{{ lead[4] }}</span></td>
                    <td>{{ lead[5] }}</td>
                    <td><b style="color: #2ecc71;">{{ lead[6] }}</b></td>
                    <td style="color: #ccc; max-width: 180px;">{{ lead[7] }}</td>
                    <td><span class="badge status-{{ lead[8] }}">{{ lead[8] }}</span></td>
                    <td style="color: #888; font-size: 11px;">{{ lead[9] }}</td>
                    <td class="actions">
                        <a href="/admin/status/{{ lead[0] }}/Contacted" class="btn-contacted">Contacted</a>
                        <a href="/admin/status/{{ lead[0] }}/Completed" class="btn-completed">Completed</a>
                        <a href="/admin/delete/{{ lead[0] }}" class="btn-delete" onclick="return confirm('Are you sure you want to delete this customer request?');">Delete</a>
                    </td>
                </tr>
                {% endfor %}
            </table>
            {% else %}
            <div class="empty-state">
                <p>No customer requests received yet. Inquiries submitted from your website will appear here instantly!</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# Routes
@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    name = request.form.get('name')
    phone = request.form.get('phone')
    whatsapp = request.form.get('whatsapp')
    property_type = request.form.get('property_type')
    location = request.form.get('location')
    budget = request.form.get('budget')
    message = request.form.get('message')

    if name and phone:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO leads (name, phone, whatsapp, property_type, location, budget, message) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, whatsapp, property_type, location, budget, message))
        conn.commit()
        conn.close()
        return render_template_string(SUCCESS_HTML)
    
    return "Error: Please fill in all required fields.", 400

@app.route('/admin')
def admin_panel():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, whatsapp, property_type, location, budget, message, status, created_at FROM leads ORDER BY id DESC")
    leads = cursor.fetchall()
    conn.close()
    return render_template_string(ADMIN_HTML, leads=leads)

@app.route('/admin/status/<int:lead_id>/<status>')
def update_status(lead_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (status, lead_id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

@app.route('/admin/delete/<int:lead_id>')
def delete_lead(lead_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
