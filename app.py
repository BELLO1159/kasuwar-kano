import os
import sqlite3
import csv
import io
from flask import Flask, request, render_template_string, redirect, url_for, Response

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

# Main Homepage Template - Complete Ultimate Edition
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

        .container { max-width: 650px; width: 92%; background: var(--dark-card); padding: 30px; border-radius: 16px; box-shadow: 0 10px 30px rgba(255,20,147,0.15); margin-bottom: 40px; border: 1px solid #333; }
        h2 { color: var(--pink); text-align: center; margin-top: 0; font-size: 22px; }
        
        .property-box { background: #111; border: 1px solid #333; border-radius: 10px; padding: 18px; margin-bottom: 15px; }
        .property-box h4 { color: var(--white); margin: 0 0 8px 0; font-size: 16px; }
        .property-box p { color: #aaa; margin: 4px 0; font-size: 13px; line-height: 1.4; }
        .price-tag { color: #2ecc71; font-weight: bold; font-size: 15px; }
        .badge-plan { background: rgba(255,20,147,0.15); color: var(--pink); padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; display: inline-block; margin-top: 6px; }

        /* Search Filter Input Bar */
        .search-bar { width: 100%; padding: 12px 15px; margin-bottom: 15px; border-radius: 8px; border: 1px solid var(--pink); background: #000; color: #fff; font-size: 14px; }
        .search-bar:focus { outline: none; box-shadow: 0 0 8px rgba(255,20,147,0.4); }

        /* Location Price Grid */
        .location-grid { display: grid; grid-template-columns: 1fr; gap: 10px; margin-bottom: 20px; max-height: 300px; overflow-y: auto; padding-right: 5px; }
        .loc-item { background: #111; border: 1px solid #333; padding: 12px 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .loc-name { font-weight: bold; color: #fff; font-size: 14px; }
        .loc-details { text-align: right; }
        .loc-price { color: #2ecc71; font-weight: bold; font-size: 14px; display: block; }
        .loc-size { color: #888; font-size: 12px; }

        /* Calculator Styles */
        .calc-box { background: #000; border: 1px solid var(--pink); border-radius: 12px; padding: 20px; margin-top: 20px; }
        .calc-result { background: #1a1a1a; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center; border-left: 4px solid var(--pink); }
        .calc-result h4 { color: var(--pink); margin: 0 0 5px 0; font-size: 15px; }
        .calc-result p { color: #fff; margin: 0; font-size: 14px; font-weight: bold; line-height: 1.6; }

        /* FAQ Section */
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

        /* Floating Contact Buttons */
        .floating-buttons { position: fixed; bottom: 25px; right: 25px; display: flex; flex-direction: column; gap: 12px; z-index: 1000; }
        .float-btn { width: 55px; height: 55px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 26px; box-shadow: 0 4px 15px rgba(0,0,0,0.4); text-decoration: none; transition: transform 0.3s; }
        .float-btn:hover { transform: scale(1.1); }
        .whatsapp-float { background-color: #25d366; color: white; }
        .call-float { background-color: #3498db; color: white; }
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
        <h1>Kasuwar Kano <span>Estate Agency</span></h1>
        <p>Mallaki Gida Ko Fili Cikin Sauƙin Biya</p>
        
        <div class="cta-grid">
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='House';">🏡 Ina Neman Gida</a>
            <a href="#request-form" class="cta-btn" onclick="document.getElementById('property_type').value='Land';">🌍 Ina Neman Fili</a>
        </div>
    </div>

    <!-- Active Properties & Price Calculator Section -->
    <div class="container">
        <h2>Farashin Filaye da Gidaje & Lissafi</h2>
        
        <!-- House Card -->
        <div class="property-box">
            <h4>🏡 Gidaje a Kureken Sani / Hotoro</h4>
            <p><b>Farashi:</b> <span class="price-tag">₦17,500,000</span></p>
            <p><b>Tsarin Biya:</b> Biya 50% (₦8,750,000) ka karɓi maɓallin gidanka nan take, sannan ka ci gaba da biyan sauran a kowane wata.</p>
            <span class="badge-plan">50% Key Handover Plan</span>
        </div>

        <!-- Location Pricing List with Live Search Bar -->
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

        <!-- Interactive Calculator Widget -->
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
            
            <div class="calc-result" id="calc_output">
                <!-- Javascript fills this -->
            </div>
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
            
            <label>Preferred Location / Wuri (Za a cika shi ta atomatik)</label>
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

    <!-- Floating Action Buttons -->
    <div class="floating-buttons">
        <a href="tel:09066073407" class="float-btn call-float" title="Kira Kai Tsaye">
            📞
        </a>
        <a href="https://wa.me/2349066073407?text=Assalamu%20Alaikum,%20Ina%20son%20neman%20bayani%20game%20da%20Gidaje%20ko%20Filaye." class="float-btn whatsapp-float" target="_blank" title="Chat on WhatsApp">
            💬
        </a>
    </div>

</body>
</html>
"""

SUCCESS_HTML = """
<!DOCTYPE html>
<html lang="ha">
<head>
    <meta charset="UTF-8">
    <title>An Tura Buƙata</title>
</head>
<body>
    <p>Saved successfully</p>
</body>
</html>
"""

# Admin Panel Template with CSV/Excel Export
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
        
        .admin-header { background: var(--dark-card); padding: 25px; border-radius: 16px; border: 1px solid #333; box-shadow: 0 10px 30px rgba(255,20,147,0.1); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; margin-bottom: 25px; }
        .admin-header h1 { color: var(--pink); margin: 0; font-size: 24px; }
        .admin-header p { color: #aaa; margin: 5px 0 0 0; font-size: 14px; }
        
        .header-btns { display: flex; gap: 10px; flex-wrap: wrap; }
        .back-btn, .export-btn { background: #222; border: 1px solid var(--pink); color: var(--white); padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 13px; transition: 0.3s; display: inline-block; }
        .back-btn:hover, .export-btn:hover { background: var(--pink); color: var(--black); }
        .export-btn { background: #2ecc71; border-color: #2ecc71; color: #000; }
        .export-btn:hover { background: #27ae60; color: #fff; }

        .table-card { background: var(--dark-card); padding: 20px; border-radius: 16px; border: 1px solid #333; overflow-x: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h3 { color: var(--white); margin-top: 0; border-bottom: 1px solid #333; padding-bottom: 12px; font-size: 18px; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; min-width: 800px; }
        th, td { border: 1px solid #2a2a2a; padding: 14px; text-align: left; }
        th { background-color: #222; color: var(--pink); text-transform: uppercase; font-size: 11px; letter-spacing: 1px; }
        tr:nth-child(even) { background-color: #121212; }
        tr:hover { background-color: #1a1a1a; }
        
        .actions a { display: inline-block; padding: 6px 12px; margin: 3px 2px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 11px; transition: 0.2s; }
        .btn-contacted { background: #f39c12; color: #000; }
        .btn-completed { background: #27ae60; color: #fff; }
        .btn-delete { background: #c0392b; color: #fff; }
        
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
            <div class="header-btns">
                <a href="/admin/export" class="export-btn">📥 Download Excel / CSV</a>
                <a href="/" class="back-btn">← View Live Website</a>
            </div>
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
                    <th>Budget / Price Plan</th>
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

@app.route('/admin/export')
def export_csv():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, whatsapp, property_type, location, budget, message, status, created_at FROM leads ORDER BY id DESC")
    leads = cursor.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Customer Name', 'Phone', 'WhatsApp', 'Property Type', 'Location', 'Budget/Plan', 'Message', 'Status', 'Date'])
    
    for lead in leads:
        writer.writerow(lead)
        
    output.seek(0)
    
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=kasuwar_kano_leads.csv"}
    )

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
