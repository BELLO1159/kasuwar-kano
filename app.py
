import os
import sqlite3
import csv
import io
import base64
from flask import Flask, request, render_template_string, redirect, url_for, Response, session

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'kasuwar_kano_secret_key_change_this'

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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_content (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_content(key, default=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT value FROM site_content WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else default

def set_content(key, value):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO site_content (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

# Main Homepage Template with Strict Black & White Brand Styling
HOME_HTML = """
<!DOCTYPE html>
<html lang="ha">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kasuwar Kano Estate Agency</title>
    <style>
        :root {
            --primary: #ffffff;
            --secondary: #cccccc;
            --black: #000000;
            --dark-card: #111111;
            --border-color: #333333;
        }
        * { box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--black); color: var(--primary); margin: 0; padding: 0; display: flex; flex-direction: column; align-items: center; }
        
        .hero { text-align: center; padding: 40px 20px; max-width: 700px; width: 100%; }
        
        .brand-logo-container { display: flex; justify-content: center; margin-bottom: 15px; }
        .brand-logo { width: 160px; height: 160px; border-radius: 50%; object-fit: cover; border: 3px solid var(--primary); box-shadow: 0 0 25px rgba(255,255,255,0.2); background: #000; }

        .hero h1 { color: var(--primary); font-size: 32px; margin-bottom: 10px; letter-spacing: 1px; }
        .hero h1 span { color: var(--secondary); border-bottom: 2px solid var(--primary); }
        .hero p { color: var(--secondary); font-size: 18px; margin-bottom: 30px; font-weight: 300; }
        
        .cta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px; }
        .cta-btn { background: var(--dark-card); border: 2px solid var(--primary); color: var(--primary); padding: 18px 10px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; text-align: center; transition: 0.3s; }
        .cta-btn:hover { background: var(--primary); color: var(--black); }

        .container { max-width: 650px; width: 92%; background: var(--dark-card); padding: 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); margin-bottom: 40px; border: 1px solid var(--border-color); }
        h2 { color: var(--primary); text-align: center; margin-top: 0; font-size: 22px; border-bottom: 1px solid var(--border-color); padding-bottom: 10px; }
        
        .gallery-grid { display: grid; grid-template-columns: 1fr; gap: 15px; margin-bottom: 25px; }
        .gallery-card { background: #080808; border: 1px solid var(--border-color); border-radius: 10px; overflow: hidden; text-align: center; }
        .gallery-card img { width: 100%; height: 220px; object-fit: cover; border-bottom: 1px solid var(--border-color); }
        .gallery-card p { color: var(--primary); font-size: 15px; font-weight: bold; margin: 12px 0; padding: 0 10px; }

        /* Calculator & Slider Styles */
        .calc-box { background: #000; border: 1px solid var(--primary); border-radius: 12px; padding: 20px; margin-top: 15px; }
        .calc-box label { color: var(--secondary); font-size: 13px; margin-bottom: 8px; display: block; }
        .calc-box input[type="range"] { width: 100%; accent-color: var(--primary); cursor: pointer; margin-bottom: 15px; }
        .calc-result { background: #1a1a1a; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid var(--primary); }
        .calc-result h4 { color: var(--primary); margin: 0 0 5px 0; font-size: 15px; }
        .calc-result p { color: var(--primary); margin: 0; font-size: 14px; font-weight: bold; line-height: 1.6; }

        label { display: block; text-align: left; font-size: 13px; font-weight: bold; color: var(--secondary); margin-bottom: 6px; }
        input, select, textarea { width: 100%; padding: 14px; margin-bottom: 16px; border-radius: 8px; border: 1px solid var(--border-color); background: #000; color: var(--primary); font-size: 15px; }
        input:focus, select:focus, textarea:focus { border-color: var(--primary); outline: none; }
        
        .submit-btn { width: 100%; background-color: var(--primary); color: var(--black); font-weight: 800; padding: 16px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .submit-btn:hover { background-color: var(--secondary); }

        .footer-info { text-align: center; padding: 30px 20px 60px 20px; color: var(--secondary); font-size: 14px; border-top: 1px solid var(--border-color); width: 100%; max-width: 650px; }
        .footer-info p { margin: 8px 0; }
        .footer-info a { color: var(--primary); text-decoration: underline; }
    </style>
    <script>
        function calculateInstallment() {
            var months = document.getElementById('monthsRange').value;
            var propertyType = document.getElementById('calc_property').value;
            var totalPrice = propertyType === 'land' ? 1500000 : 17500000;
            var deposit = propertyType === 'land' ? 200000 : 8750000;
            var remaining = totalPrice - deposit;
            var monthlyPayment = Math.round(remaining / months);

            var formattedTotal = totalPrice.toLocaleString();
            var formattedDeposit = deposit.toLocaleString();
            var formattedMonthly = monthlyPayment.toLocaleString();

            var outputText = "Jimlar Farashi: ₦" + formattedTotal + "<br>" +
                             "Ajiya (Deposit): ₦" + formattedDeposit + "<br>" +
                             "Tsawon Lokaci: " + months + " Watanni<br>" +
                             "Biya kowane wata: <span style='color:#ffffff; text-decoration:underline;'>₦" + formattedMonthly + " / wata</span>";
            
            document.getElementById('calcResultText').innerHTML = outputText;
            document.getElementById('budget').value = "Deposit + ₦" + formattedMonthly + "/wata (" + months + " months)";
        }

        function handleWhatsAppSubmit(event) {
            event.preventDefault();
            
            var name = document.getElementById('name').value;
            var phone = document.getElementById('phone').value;
            var propertyType = document.getElementById('property_type').value;
            var location = document.getElementById('location').value;
            var budget = document.getElementById('budget').value;
            var message = document.getElementById('message').value;

            var text = "Assalamu Alaikum Kasuwar Kano Estate Agency,%0A%0A" +
                       "Ina son tura wannan buƙatar ne:%0A" +
                       "👤 Sunana: " + encodeURIComponent(name) + "%0A" +
                       "📞 Wayar Kira: " + encodeURIComponent(phone) + "%0A" +
                       "🏡 Nau'i: " + encodeURIComponent(propertyType) + "%0A" +
                       "📍 Wuri: " + encodeURIComponent(location) + "%0A" +
                       "💰 Tsarin Biya: " + encodeURIComponent(budget) + "%0A" +
                       "💬 Bayani: " + encodeURIComponent(message);

            var formData = new FormData(document.getElementById('lead-form'));
            fetch('/submit-lead', {
                method: 'POST',
                body: formData
            }).then(response => {
                window.location.href = "https://wa.me/2349066073407?text=" + text;
            }).catch(error => {
                window.location.href = "https://wa.me/2349066073407?text=" + text;
            });
        }
    </script>
</head>
<body onload="calculateInstallment()">

    <div class="hero">
        <div class="brand-logo-container">
            {% if logo_url %}
                <img src="{{ logo_url }}" alt="Kasuwar Kano Logo" class="brand-logo">
            {% else %}
                <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=300&q=80" alt="Default Logo" class="brand-logo">
            {% endif %}
        </div>
        <h1>Kasuwar Kano <span>Estate Agency</span></h1>
        <p>Mallaki Gida Ko Fili Cikin Sauƙin Biya</p>
        
        <div class="cta-grid">
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='House (Hotoro Kureken Sani)'; document.getElementById('location').value='Hotoro Kureken Sani';">🏡 Gida (Hotoro)</a>
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='Land (Larabar Abasawa)'; document.getElementById('location').value='Larabar Abasawa';">🌍 Fili (Larabar Abasawa)</a>
        </div>
    </div>

    <!-- Featured Property 1: Land -->
    <div class="container">
        <h2>Featured Property: Fili a Larabar Abasawa</h2>
        <div class="gallery-grid">
            <div class="gallery-card">
                <img src="{{ img1 or 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=600&q=80' }}" alt="Larabar Abasawa Land">
                <p>{{ caption1 or 'Larabar Abasawa - Tsayayyun Filaye masu kyau (₦1,500,000)' }}</p>
            </div>
        </div>
    </div>

    <!-- Featured Property 2: House -->
    <div class="container">
        <h2>Featured Property: Gida a Hotoro Kureken Sani</h2>
        <div class="gallery-grid">
            <div class="gallery-card">
                <img src="{{ img2 or 'https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=600&q=80' }}" alt="Hotoro Kureken Sani House">
                <p>{{ caption2 or 'Hotoro Kureken Sani - Gidajen Zamani (₦17,500,000)' }}</p>
            </div>
        </div>
    </div>

    <!-- Interactive Installment & Payment Calculator Section -->
    <div class="container">
        <h2>🧮 Mai Lissafin Biyan Tsari (Installment Calculator)</h2>
        <p style="color: var(--secondary); font-size: 13px; text-align: center; margin-top: -10px;">Ka zabi wata nawa kake so ka biya a hankali:</p>
        
        <div class="calc-box">
            <label>Zaɓi Abin da Kake So:</label>
            <select id="calc_property" onchange="calculateInstallment()">
                <option value="land">Fili a Larabar Abasawa (Total: ₦1,500,000 | Deposit: ₦200,000)</option>
                <option value="house">Gida a Hotoro Kureken Sani (Total: ₦17,500,000 | Deposit: ₦8,750,000)</option>
            </select>

            <label>Tsawon Watanni (Months): <span id="monthsVal" style="color:#fff; text-decoration:underline;">12</span> Watanni</label>
            <input type="range" id="monthsRange" min="3" max="24" value="12" step="1" oninput="document.getElementById('monthsVal').innerText=this.value; calculateInstallment();">
            
            <div class="calc-result" id="calc_output">
                <h4>Sakamakon Lissafi:</h4>
                <p id="calcResultText">Loading...</p>
            </div>
        </div>
    </div>

    <!-- Request Form Section with direct WhatsApp Trigger & Instant Reservation Lock-in -->
    <div class="container" id="request-form">
        <h2>Tura Buƙatar Gida Ko Fili (Reservation Form)</h2>
        <form id="lead-form" onsubmit="handleWhatsAppSubmit(event)">
            <label>Full Name (Cikakken Sunanka)</label>
            <input type="text" id="name" name="name" placeholder="Misali: Ibrahim Sani" required>
            
            <label>Phone Number (Lambar Wayar Kira)</label>
            <input type="tel" id="phone" name="phone" placeholder="Misali: 09066073407" required>
            
            <label>WhatsApp Number (Lambar WhatsApp)</label>
            <input type="tel" name="whatsapp" placeholder="Misali: 09066073407">
            
            <label>Property Type (Nau'in Abin da Kake Nema)</label>
            <select name="property_type" id="property_type" required>
                <option value="Land (Larabar Abasawa)">Fili a Larabar Abasawa</option>
                <option value="House (Hotoro Kureken Sani)">Gida a Hotoro Kureken Sani</option>
            </select>
            
            <label>Preferred Location / Wuri</label>
            <input type="text" name="location" id="location" value="Larabar Abasawa" placeholder="Misali: Larabar Abasawa">
            
            <label>Budget / Tsarin Biya (Auto-Calculated)</label>
            <input type="text" name="budget" id="budget" placeholder="Misali: Deposit + Monthly plan">
            
            <label>Additional Message (Bayani Ƙari ko Ajiyar Wuri)</label>
            <textarea name="message" id="message" rows="3" placeholder="Ina son a yi mini ajiyar wannan wuri (Lock-in reservation)..."></textarea>
            
            <button type="submit" class="submit-btn">
                <span>🔒 LOCK-IN & TURA TA WHATSAPP</span>
            </button>
        </form>
    </div>

    <div class="footer-info">
        <p>📞 <b>09066073407</b></p>
        <p>📍 <b>Goron Dutse, Maiyari Plaza, Kano</b></p>
        <p style="margin-top: 15px;"><a href="/admin" style="color: var(--primary); font-size: 13px; font-weight: bold;">🔐 Admin Panel Dashboard</a></p>
    </div>

</body>
</html>
"""

# Admin Login Template
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - Kasuwar Kano</title>
    <style>
        body { background-color: #000; color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .login-box { background: #111; padding: 40px; border-radius: 16px; border: 1px solid #333; width: 100%; max-width: 400px; box-shadow: 0 10px 30px rgba(0,0,0,0.9); text-align: center; }
        h2 { color: #fff; margin-top: 0; margin-bottom: 25px; border-bottom: 1px solid #333; padding-bottom: 10px; }
        label { display: block; text-align: left; font-size: 13px; font-weight: bold; color: #ccc; margin-bottom: 8px; }
        input { width: 100%; padding: 14px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #444; background: #000; color: #fff; font-size: 15px; box-sizing: border-box; }
        input:focus { border-color: #fff; outline: none; }
        button { width: 100%; background-color: #fff; color: #000; font-weight: bold; padding: 14px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: 0.3s; }
        button:hover { background-color: #ccc; }
        .error { color: #ff4d4d; font-size: 13px; margin-bottom: 15px; }
        .back-link { display: block; margin-top: 20px; color: #888; text-decoration: none; font-size: 13px; }
        .back-link:hover { color: #fff; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>🔐 Admin Portal</h2>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="POST">
            <label>Admin Password</label>
            <input type="password" name="password" placeholder="Enter password" required autofocus>
            <button type="submit">Login</button>
        </form>
        <a href="/" class="back-link">← Komawa Gida (Back to Home)</a>
    </div>
</body>
</html>
"""

# Admin Dashboard Template
ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - Kasuwar Kano</title>
    <style>
        body { background-color: #000; color: #fff; margin: 0; padding: 30px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; }
        .dashboard-container { width: 100%; max-width: 900px; background: #111; padding: 30px; border-radius: 16px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(0,0,0,0.9); margin-bottom: 30px; }
        .header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; border-bottom: 1px solid #333; padding-bottom: 15px; }
        h2 { color: #fff; margin: 0; }
        .btn-group { display: flex; gap: 10px; }
        .action-btn { background: #fff; color: #000; padding: 10px 16px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px; border: none; cursor: pointer; transition: 0.3s; }
        .action-btn:hover { background: #ccc; }
        .logout-btn { background: #333; color: #fff; }
        .logout-btn:hover { background: #444; }
        
        .upload-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
        .upload-card { background: #080808; border: 1px solid #333; padding: 20px; border-radius: 10px; }
        .upload-card h3 { color: #fff; margin-top: 0; font-size: 16px; border-bottom: 1px solid #222; padding-bottom: 8px; }
        label { display: block; font-size: 12px; font-weight: bold; color: #ccc; margin-bottom: 6px; }
        input[type="file"], input[type="text"] { width: 100%; padding: 10px; margin-bottom: 12px; border-radius: 6px; border: 1px solid #444; background: #000; color: #fff; font-size: 13px; box-sizing: border-box; }
        input[type="file"] { padding: 6px; }
        .preview-img { width: 60px; height: 60px; object-fit: cover; border-radius: 50%; border: 2px solid #fff; margin-top: 5px; }
        .preview-box { width: 100%; height: 80px; object-fit: cover; border-radius: 6px; border: 1px solid #444; margin-top: 5px; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #222; font-size: 14px; }
        th { color: #fff; background: #080808; }
        td { color: #ccc; }
        .no-data { text-align: center; color: #666; padding: 40px; }
        .success-msg { background: rgba(255, 255, 255, 0.1); color: #fff; padding: 12px; border-radius: 6px; margin-bottom: 20px; font-weight: bold; text-align: center; border: 1px solid #fff; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header-row">
            <h2>🖼️ Upload Properties (Larabar Abasawa & Hotoro)</h2>
            <div class="btn-group">
                <a href="/admin/logout" class="action-btn logout-btn">Logout</a>
            </div>
        </div>

        {% if msg %}
            <div class="success-msg">{{ msg }}</div>
        {% endif %}

        <form method="POST" enctype="multipart/form-data">
            <div class="upload-grid">
                <!-- Logo Upload -->
                <div class="upload-card">
                    <h3>Brand Logo</h3>
                    <label>Upload Logo</label>
                    <input type="file" name="logo">
                    {% if logo_url %}
                        <img src="{{ logo_url }}" class="preview-img" alt="Logo">
                    {% endif %}
                </div>

                <!-- Land Upload (Larabar Abasawa) -->
                <div class="upload-card">
                    <h3>Land (Larabar Abasawa)</h3>
                    <label>Upload Land Image</label>
                    <input type="file" name="img1">
                    <label>Description / Details</label>
                    <input type="text" name="caption1" value="{{ caption1 }}">
                    {% if img1 %}
                        <img src="{{ img1 }}" class="preview-box" alt="Land">
                    {% endif %}
                </div>

                <!-- House Upload (Hotoro Kureken Sani) -->
                <div class="upload-card" style="grid-column: span 2;">
                    <h3>House (Hotoro Kureken Sani)</h3>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                        <div>
                            <label>Upload House Image</label>
                            <input type="file" name="img2">
                            <label>Description / Details</label>
                            <input type="text" name="caption2" value="{{ caption2 }}">
                        </div>
                        <div>
                            {% if img2 %}
                                <img src="{{ img2 }}" class="preview-box" alt="House" style="height: 100px;">
                            {% endif %}
                        </div>
                    </div>
                </div>
            </div>

            <button type="submit" class="action-btn" style="width: 100%; padding: 14px; font-size: 16px; margin-top: 10px;">💾 Save & Update Properties</button>
        </form>
    </div>

    <div class="dashboard-container">
        <div class="header-row">
            <h2>📊 Customer Leads & Reservations Dashboard</h2>
            <div class="btn-group">
                <a href="/admin/export" class="action-btn">📥 Download CSV</a>
            </div>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Date</th>
                    <th>Name</th>
                    <th>Phone</th>
                    <th>Property Type</th>
                    <th>Location / Budget</th>
                    <th>Message</th>
                </tr>
            </thead>
            <tbody>
                {% for lead in leads %}
                <tr>
                    <td>{{ lead[0] }}</td>
                    <td>{{ lead[9] }}</td>
                    <td style="color: #fff; font-weight: bold;">{{ lead[1] }}</td>
                    <td><a href="tel:{{ lead[2] }}" style="color: #fff; text-decoration: underline;">{{ lead[2] }}</a></td>
                    <td>{{ lead[4] }}</td>
                    <td>{{ lead[5] }}<br><small style="color: #888;">{{ lead[6] }}</small></td>
                    <td>{{ lead[7] }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="7" class="no-data">Babu wani saƙo ko buƙata a yanzu.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div style="margin-bottom: 40px;">
        <a href="/" style="color: #888; text-decoration: none; font-size: 14px;">← Komawa Gida (Back to Website)</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        HOME_HTML,
        logo_url=get_content('logo_url'),
        img1=get_content('img1'),
        caption1=get_content('caption1'),
        img2=get_content('img2'),
        caption2=get_content('caption2')
    )

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    name = request.form.get('name')
    phone = request.form.get('phone')
    whatsapp = request.form.get('whatsapp')
    property_type = request.form.get('property_type')
    location = request.form.get('location')
    budget = request.form.get('budget')
    message = request.form.get('message')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO leads (name, phone, whatsapp, property_type, location, budget, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, phone, whatsapp, property_type, location, budget, message))
    conn.commit()
    conn.close()

    return '', 204

@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        if request.form.get('password') == 'kasuwar kano admin':
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Incorrect password. Please use kasuwar kano admin.'
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    
    msg = None
    if request.method == 'POST':
        logo_file = request.files.get('logo')
        if logo_file and logo_file.filename:
            logo_data = base64.b64encode(logo_file.read()).decode('utf-8')
            logo_mime = logo_file.mimetype or 'image/jpeg'
            set_content('logo_url', f"data:{logo_mime};base64,{logo_data}")

        for i in range(1, 3):
            img_file = request.files.get(f'img{i}')
            if img_file and img_file.filename:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
                img_mime = img_file.mimetype or 'image/jpeg'
                set_content(f'img{i}', f"data:{img_mime};base64,{img_data}")
            
            caption_text = request.form.get(f'caption{i}')
            if caption_text is not None:
                set_content(f'caption{i}', caption_text)

        msg = "An nasara ɗora hotuna da gyara shafin!"

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    leads = cursor.fetchall()
    conn.close()

    return render_template_string(
        ADMIN_HTML,
        leads=leads,
        msg=msg,
        logo_url=get_content('logo_url'),
        img1=get_content('img1'),
        caption1=get_content('caption1'),
        img2=get_content('img2'),
        caption2=get_content('caption2')
    )

@app.route('/admin/export')
def export_csv():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    leads = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Phone', 'WhatsApp', 'Property Type', 'Location', 'Budget', 'Message', 'Status', 'Created At'])
    for lead in leads:
        writer.writerow(lead)

    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=kasuwar_kano_leads.csv'
    return response

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
