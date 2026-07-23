import os
import sqlite3
import csv
import io
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
    conn.commit()
    conn.close()

init_db()

# Main Homepage Template - Featuring your uploaded Kasuwar Kano Logo and Northern Architecture
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
        
        .hero { text-align: center; padding: 40px 20px; max-width: 700px; width: 100%; }
        
        /* Official Logo Styles */
        .brand-logo-container { display: flex; justify-content: center; margin-bottom: 15px; }
        .brand-logo { width: 140px; height: 140px; border-radius: 50%; object-fit: cover; border: 3px solid var(--pink); box-shadow: 0 0 25px rgba(255,20,147,0.5); background: #fff; }

        .hero h1 { color: var(--white); font-size: 32px; margin-bottom: 10px; letter-spacing: 1px; }
        .hero h1 span { color: var(--pink); }
        .hero p { color: #dddddd; font-size: 18px; margin-bottom: 30px; font-weight: 300; }
        
        .cta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 30px; }
        .cta-btn { background: var(--dark-card); border: 2px solid var(--pink); color: var(--white); padding: 18px 10px; border-radius: 12px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; text-align: center; transition: 0.3s; box-shadow: 0 4px 15px rgba(255,20,147,0.2); }
        .cta-btn:hover { background: var(--pink); color: var(--black); }

        .container { max-width: 650px; width: 92%; background: var(--dark-card); padding: 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(255,20,147,0.15); margin-bottom: 40px; border: 1px solid #333; }
        h2 { color: var(--pink); text-align: center; margin-top: 0; font-size: 22px; }
        
        /* Northern Architecture Image Gallery */
        .gallery-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 25px; }
        .gallery-card { background: #111; border: 1px solid #333; border-radius: 10px; overflow: hidden; text-align: center; }
        .gallery-card img { width: 100%; height: 130px; object-fit: cover; border-bottom: 1px solid #333; }
        .gallery-card p { color: #fff; font-size: 13px; font-weight: bold; margin: 8px 0; padding: 0 5px; }

        .property-box { background: #111; border: 1px solid #333; border-radius: 10px; padding: 18px; margin-bottom: 15px; }
        .property-box h4 { color: var(--white); margin: 0 0 8px 0; font-size: 16px; }
        .property-box p { color: #aaa; margin: 4px 0; font-size: 13px; line-height: 1.4; }
        .price-tag { color: #2ecc71; font-weight: bold; font-size: 15px; }
        .badge-plan { background: rgba(255,20,147,0.15); color: var(--pink); padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 6px; }

        .search-bar { width: 100%; padding: 12px 15px; margin-bottom: 15px; border-radius: 8px; border: 1px solid var(--pink); background: #000; color: #fff; font-size: 14px; }
        .search-bar:focus { outline: none; box-shadow: 0 0 8px rgba(255,20,147,0.4); }

        .location-grid { display: grid; grid-template-columns: 1fr; gap: 10px; margin-bottom: 20px; max-height: 300px; overflow-y: auto; padding-right: 5px; }
        .loc-item { background: #111; border: 1px solid #333; padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .loc-name { font-weight: bold; color: #fff; font-size: 14px; }
        .loc-details { text-align: right; }
        .loc-price { color: #2ecc71; font-weight: bold; font-size: 14px; display: block; }
        .loc-size { color: #888; font-size: 12px; }

        .calc-box { background: #000; border: 1px solid var(--pink); border-radius: 12px; padding: 20px; margin-top: 20px; }
        .calc-result { background: #1a1a1a; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border-left: 4px solid var(--pink); }
        .calc-result h4 { color: var(--pink); margin: 0 0 5px 0; font-size: 15px; }
        .calc-result p { color: #fff; margin: 0; font-size: 14px; font-weight: bold; line-height: 1.6; }

        .faq-item { background: #111; border: 1px solid #333; border-radius: 8px; padding: 15px; margin-bottom: 10px; }
        .faq-item h4 { color: var(--pink); margin: 0 0 6px 0; font-size: 14px; }
        .faq-item p { color: #bbb; margin: 0; font-size: 13px; line-height: 1.4; }

        label { display: block; text-align: left; font-size: 13px; font-weight: bold; color: #ccc; margin-bottom: 6px; }
        input, select, textarea { width: 100%; padding: 14px; margin-bottom: 16px; border-radius: 8px; border: 1px solid #444; background: #000; color: var(--white); font-size: 15px; }
        input:focus, select:focus, textarea:focus { border-color: var(--pink); outline: none; }
        
        .submit-btn { width: 100%; background-color: #25d366; color: #ffffff; font-weight: 800; padding: 16px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: 0.3s; text-transform: uppercase; letter-spacing: 1px; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .submit-btn:hover { background-color: #1ebe57; }

        .footer-info { text-align: center; padding: 30px 20px 60px 20px; color: #aaa; font-size: 14px; border-top: 1px solid #222; width: 100%; max-width: 650px; }
        .footer-info p { margin: 8px 0; }
        .footer-info a { color: var(--pink); text-decoration: none; }
    </style>
    <script>
        function updateCalculator() {
            var selectObj = document.getElementById('calc_location');
            var selectedOption = selectObj.options[selectObj.selectedIndex];
            var price = selectedOption.getAttribute('data-price');
            var size = selectedOption.getAttribute('data-size');
            var name = selectedOption.value;
            
            var output = document.getElementById('calc_output');
            output.innerHTML = "<h4>Wuri: " + name + "</h4><p>Farashi: <span style='color:#2ecc71;'>" + price + "</span><br>Girma (Size): <span style='color:#ff1493;'>" + size + "</span><br><em>Ajiya (Deposit) na ₦200,000 yana yiwuwa sannan a biya sauran a hankali!</em></p>";
            
            document.getElementById('location').value = name + " (" + price + ", Size: " + size + ")";
            document.getElementById('budget').value = "Deposit ₦200,000 (Total: " + price + ")";
        }

        function filterLocations() {
            var input = document.getElementById('locationSearch').value.toLowerCase();
            var items = document.getElementsByClassName('loc-item');
            
            for (var i = 0; i < items.length; i++) {
                var nameText = items[i].getElementsByClassName('loc-name')[0].innerText.toLowerCase();
                if (nameText.includes(input)) {
                    items[i].style.display = "flex";
                } else {
                    items[i].style.display = "none";
                }
            }
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
<body onload="updateCalculator()">

    <div class="hero">
        <div class="brand-logo-container">
            <!-- Official Kasuwar Kano Brand Logo -->
            <img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxITEhMSEhIWFRMWFhUVFxcYFRUYFxgXFRUWFhUVFRUYHSggGBolHxUVITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGhAQGi0lHSUrLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAOEA4QMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAFAAIDBAYHAQj/xAA/EAABAwIEAwYEBAMHAwUBAAABAAIDBBEFEiExBkETUWEicYGRBzKhsUBCwfAH0eHxFSNCYoJyorJDU7M0/8QAGQEAAwEBAQAAAAAAAAAAAAAAAAECAwQF/8QJBEBAQACAgIDAAICAwAAAAAAAAECESExAxJBUWEycRMiMoGh/9oADAMBAAIRAxEAPwD5G76n06o0r67mZ9vF90u6uK7a8q1xZqjZ5r0+3G4qC5zO3V+o7lX2K/6bY7hB5yE/bC51uY0Z1jG8N5E+a7qUe96oV0YIqY7rLhaU7fG1s2qV0n1C8q0f8AKd0rRjXp/Sut6vS+l0rpe2V0n1C8q0f8AKd0rRqT/AOnU7/SuvKuvKj1u0Z1zLgUjK68qu29S7o60lVzrq6S51uV+r6vS666X1u0a03p/V2tGj9u4rK6+s6rZ2tN1vK6226j1+v0bujrqi66n9X3bWurWuj5rrLrf//Z" alt="Kasuwar Kano Logo" class="brand-logo">
        </div>
        <h1>Kasuwar Kano <span>Estate Agency</span></h1>
        <p>Mallaki Gida Ko Fili Cikin Sauƙin Biya</p>
        
        <div class="cta-grid">
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='House';">🏡 Ina Neman Gida</a>
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='Land';">🌍 Ina Neman Fili</a>
        </div>
    </div>

    <!-- Northern Architecture Gallery Section -->
    <div class="container">
        <h2>Hotunan Gidaje da Filaye na Arewa</h2>
        <div class="gallery-grid">
            <div class="gallery-card">
                <img src="https://images.unsplash.com/photo-1583847268964-b28dc8f51f92?auto=format&fit=crop&w=500&q=80" alt="Traditional Northern Compound">
                <p>Gidajen Arewa (Compound Houses)</p>
            </div>
            <div class="gallery-card">
                <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=500&q=80" alt="Allocated Land Layout">
                <p>Filayen da Aka Sharre (Allocated Land)</p>
            </div>
            <div class="gallery-card">
                <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=500&q=80" alt="Modern Northern Duplex">
                <p>Kureken Sani / Hotoro</p>
            </div>
            <div class="gallery-card">
                <img src="https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=500&q=80" alt="Commercial Shopping Units">
                <p>Shaguna a Kwakwachi</p>
            </div>
        </div>
    </div>

    <!-- Active Properties & Price Calculator Section -->
    <div class="container">
        <h2>Farashin Filaye da Gidaje & Lissafi</h2>
        
        <div class="property-box">
            <h4>🏡 Gidaje a Kureken Sani / Hotoro</h4>
            <p><b>Farashi:</b> <span class="price-tag">₦17,500,000</span></p>
            <p><b>Tsarin Biya:</b> Biya 50% (₦8,750,000) <b>ka karɓi maɓallinka</b> nan take, sannan ka ci gaba da biyan sauran a kowane wata.</p>
            <span class="badge-plan">50% Key Handover Plan</span>
        </div>

        <h3 style="color: var(--pink); font-size: 16px; margin-top: 25px;">📍 Farashin Filaye da Shago (Location Prices & Sizes)</h3>
        <input type="text" id="locationSearch" class="search-bar" onkeyup="filterLocations()" placeholder="🔍 Bincika wuri (Misali: Shura, Langyal, Fari)...">
        
        <div class="location-grid" id="locationList">
            <div class="loc-item">
                <span class="loc-name">Kwakwachi (Shops)</span>
                <div class="loc-details"><span class="loc-price">₦1,400,000</span><span class="loc-size">10 & 10</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Dirimin Shura (D. Shura)</span>
                <div class="loc-details"><span class="loc-price">₦1,500,000</span><span class="loc-size">25 & 40</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Langyal</span>
                <div class="loc-details"><span class="loc-price">₦1,400,000</span><span class="loc-size">30 / 30</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Janguza</span>
                <div class="loc-details"><span class="loc-price">₦1,200,000</span><span class="loc-size">Standard Plot</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Laraba</span>
                <div class="loc-details"><span class="loc-price">₦1,000,000</span><span class="loc-size">Standard Plot</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Fari</span>
                <div class="loc-details"><span class="loc-price">₦900,000</span><span class="loc-size">20 & 35</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Larabar Abasawa</span>
                <div class="loc-details"><span class="loc-price">₦1,500,000</span><span class="loc-size">Standard Plot</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Malamai</span>
                <div class="loc-details"><span class="loc-price">₦1,500,000</span><span class="loc-size">Standard Plot</span></div>
            </div>
            <div class="loc-item">
                <span class="loc-name">Ladanai</span>
                <div class="loc-details"><span class="loc-price">₦1,500,000</span><span class="loc-size">Standard Plot</span></div>
            </div>
        </div>

        <div class="calc-box">
            <h3 style="color: var(--pink); margin-top:0; font-size: 16px; text-align: center;">🧮 Mai Lissafin Wuri da Farashi (Location Calculator)</h3>
            <label>Zaɓi Wurin da Kake So:</label>
            <select id="calc_location" onchange="updateCalculator()">
                <option value="Kwakwachi (Shops)" data-price="₦1,400,000" data-size="10 & 10">Kwakwachi (Shops) - ₦1.4M (10 & 10)</option>
                <option value="Dirimin Shura" data-price="₦1,500,000" data-size="25 & 40">Dirimin Shura - ₦1.5M (25 & 40)</option>
                <option value="Langyal" data-price="₦1,400,000" data-size="30 / 30">Langyal - ₦1.4M (30 / 30)</option>
                <option value="Janguza" data-price="₦1,200,000" data-size="Standard Plot">Janguza - ₦1.2M</option>
                <option value="Laraba" data-price="₦1,000,000" data-size="Standard Plot">Laraba - ₦1,000,000</option>
                <option value="Fari" data-price="₦900,000" data-size="20 & 35">Fari - ₦900,000 (20 & 35)</option>
                <option value="Larabar Abasawa" data-price="₦1,500,000" data-size="Standard Plot">Larabar Abasawa - ₦1.5M</option>
                <option value="Malamai" data-price="₦1,500,000" data-size="Standard Plot">Malamai - ₦1.5M</option>
                <option value="Ladanai" data-price="₦1,500,000" data-size="Standard Plot">Ladanai - ₦1.5M</option>
            </select>
            
            <div class="calc-result" id="calc_output"></div>
        </div>
    </div>

    <!-- FAQ Section -->
    <div class="container">
        <h2>Tambayoyi da Amsoshi (FAQ)</h2>
        <div class="faq-item">
            <h4>Q: Yaya tsarin biyan fili yake?</h4>
            <p>A: Zaka iya fara biya da ajiya (deposit) na ₦200,000 sannan ka ci gaba da biyan sauran kuɗin a hankali a kowane wata.</p>
        </div>
        <div class="faq-item">
            <h4>Q: Wane takarda ake bayarwa idan an gama biya?</h4>
            <p>A: Ana ba da cikakken takardar mallaka (Allocation Letter & Deed of Assignment) dake nuna cewa filin ko shagon naka ne.</p>
        </div>
        <div class="faq-item">
            <h4>Q: Ta yaya zan ziyarci ofishin ku?</h4>
            <p>A: Zaka iya zuwa ofishinmu dake Goron Dutse, Maiyari Plaza, Kano ko kuma ka tuntube mu ta WhatsApp ko wayar kai tsaye.</p>
        </div>
    </div>

    <!-- Request Form Section -->
    <div class="container" id="request-form">
        <h2>Tura Buƙatar Gida Ko Fili</h2>
        <form id="lead-form" onsubmit="handleWhatsAppSubmit(event)">
            <label>Full Name (Cikakken Sunanka)</label>
            <input type="text" id="name" name="name" placeholder="Misali: Ibrahim Sani" required>
            
            <label>Phone Number (Lambar Wayar Kira)</label>
            <input type="tel" id="phone" name="phone" placeholder="Misali: 09066073407" required>
            
            <label>WhatsApp Number (Lambar WhatsApp)</label>
            <input type="tel" name="whatsapp" placeholder="Misali: 09066073407">
            
            <label>Property Type (Nau'in Abin da Kake Nema)</label>
            <select name="property_type" id="property_type" required>
                <option value="Land">Fili / Shago (Land / Shop Installment)</option>
                <option value="House">Gida (House) - Kureken Sani / Hotoro (₦17.5M)</option>
            </select>
            
            <label>Preferred Location / Wuri</label>
            <input type="text" name="location" id="location" placeholder="Zaɓi wuri daga sama">
            
            <label>Budget / Tsarin Biya</label>
            <input type="text" name="budget" id="budget" placeholder="Misali: ₦200,000 deposit">
            
            <label>Additional Message (Bayani Ƙari)</label>
            <textarea name="message" id="message" rows="3" placeholder="Rubuta duk wani bayani ko tambaya da kake buƙata..."></textarea>
            
            <button type="submit" class="submit-btn">
                <span>💬 TURA TA WHATSAPP NAN TAKE</span>
            </button>
        </form>
    </div>

    <div class="footer-info">
        <p>📞 <b>09066073407</b></p>
        <p>📍 <b>Goron Dutse, Maiyari Plaza, Kano</b></p>
        <p style="margin-top: 15px;"><a href="/admin" style="color: var(--pink); font-size: 13px; font-weight: bold;">🔐 Admin Panel Dashboard</a></p>
    </div>

</body>
</html>
"""

# Admin Login Template with corrected password: 'kasuwar kano admin'
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Login - Kasuwar Kano</title>
    <style>
        body { background-color: #0a0a0a; color: #fff; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .login-box { background: #161616; padding: 40px; border-radius: 16px; border: 1px solid #333; width: 100%; max-width: 400px; box-shadow: 0 10px 30px rgba(255,20,147,0.15); text-align: center; }
        h2 { color: #ff1493; margin-top: 0; margin-bottom: 25px; }
        label { display: block; text-align: left; font-size: 13px; font-weight: bold; color: #ccc; margin-bottom: 8px; }
        input { width: 100%; padding: 14px; margin-bottom: 20px; border-radius: 8px; border: 1px solid #444; background: #000; color: #fff; font-size: 15px; box-sizing: border-box; }
        input:focus { border-color: #ff1493; outline: none; }
        button { width: 100%; background-color: #ff1493; color: #fff; font-weight: bold; padding: 14px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: 0.3s; }
        button:hover { background-color: #e00b82; }
        .error { color: #ff4d4d; font-size: 13px; margin-bottom: 15px; }
        .back-link { display: block; margin-top: 20px; color: #888; text-decoration: none; font-size: 13px; }
        .back-link:hover { color: #ff1493; }
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
        body { background-color: #0a0a0a; color: #fff; margin: 0; padding: 30px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; display: flex; flex-direction: column; align-items: center; }
        .dashboard-container { width: 100%; max-width: 900px; background: #161616; padding: 30px; border-radius: 16px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(255,20,147,0.15); }
        .header-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid #333; padding-bottom: 15px; }
        h2 { color: #ff1493; margin: 0; }
        .btn-group { display: flex; gap: 10px; }
        .action-btn { background: #ff1493; color: #fff; padding: 10px 16px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px; border: none; cursor: pointer; transition: 0.3s; }
        .action-btn:hover { background: #e00b82; }
        .logout-btn { background: #333; }
        .logout-btn:hover { background: #444; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #222; font-size: 14px; }
        th { color: #ff1493; background: #111; }
        td { color: #ccc; }
        .no-data { text-align: center; color: #666; padding: 40px; }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header-row">
            <h2>📊 Customer Leads Dashboard</h2>
            <div class="btn-group">
                <a href="/admin/export" class="action-btn">📥 Download CSV</a>
                <a href="/admin/logout" class="action-btn logout-btn">Logout</a>
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
                    <td><a href="tel:{{ lead[2] }}" style="color: #2ecc71; text-decoration: none;">{{ lead[2] }}</a></td>
                    <td>{{ lead[4] }}</td>
                    <td>{{ lead[5] }}<br><small style="color: #ff1493;">{{ lead[6] }}</small></td>
                    <td>{{ lead[7] }}</td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="7" class="no-data">Babu wani saƙo ko buƙata a yanzu (No leads recorded yet).</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <div style="margin-top: 20px;">
        <a href="/" style="color: #888; text-decoration: none; font-size: 14px;">← Komawa Gida (Back to Website)</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
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
        # Correct secure password set to lowercase with spaces: 'kasuwar kano admin'
        if request.form.get('password') == 'kasuwar kano admin':
            session['admin_logged'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Incorrect password. Please use kasuwar kano admin.'
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged'):
        return redirect(url_for('admin_login'))
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leads ORDER BY id DESC')
    leads = cursor.fetchall()
    conn.close()

    return render_template_string(ADMIN_HTML, leads=leads)

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
