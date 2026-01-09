from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests
import joblib

# ================== APP CONFIG ==================
app = Flask(__name__)
app.secret_key = "b38091bcb71a9864b39317b5fc09624a"

API_KEY = "b38091bcb71a9864b39317b5fc09624a"   # <-- PUT YOUR API KEY HERE

# ================== LOAD ML MODEL ==================
model = joblib.load("crop_model.pkl")
soil_encoder = joblib.load("soil_encoder.pkl")

# ================== LANGUAGE TEXT ==================
LANG_TEXT = {
    "en": {
        "title": "Smart Agri Guide",
        "form": "Enter Farm Details",
        "soil": "Soil Type",
        "ph": "Soil pH",
        "stage": "Growth Stage",
        "city": "City / Village",
        "submit": "Get Smart Recommendation",
        "crop": "AI Recommended Crop",
        "fert": "AI Fertilizer Advice",
        "weather": "Weather Advisory",
        "schemes": "Government Schemes"
    },
    "kn": {
        "title": "ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಮಾರ್ಗದರ್ಶಿ",
        "form": "ಕೃಷಿ ವಿವರಗಳನ್ನು ನಮೂದಿಸಿ",
        "soil": "ಮಣ್ಣಿನ ಪ್ರಕಾರ",
        "ph": "ಮಣ್ಣಿನ pH",
        "stage": "ಬೆಳೆ ಹಂತ",
        "city": "ನಗರ / ಗ್ರಾಮ",
        "submit": "ಶಿಫಾರಸು ಪಡೆಯಿರಿ",
        "crop": "AI ಬೆಳೆ ಶಿಫಾರಸು",
        "fert": "AI ರಸಗೊಬ್ಬರ ಸಲಹೆ",
        "weather": "ಹವಾಮಾನ ಮಾಹಿತಿ",
        "schemes": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು"
    },
    "hi": {
        "title": "स्मार्ट कृषि गाइड",
        "form": "खेती विवरण दर्ज करें",
        "soil": "मिट्टी का प्रकार",
        "ph": "मिट्टी pH",
        "stage": "फसल अवस्था",
        "city": "शहर / गाँव",
        "submit": "सिफारिश प्राप्त करें",
        "crop": "AI फसल सिफारिश",
        "fert": "AI उर्वरक सलाह",
        "weather": "मौसम जानकारी",
        "schemes": "सरकारी योजनाएं"
    }
}

# ================== DATABASE ==================
def get_db():
    return sqlite3.connect("users.db")

with get_db() as db:
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            password TEXT
        )
    """)

# ================== LOGIN ==================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        db = get_db()
        cur = db.execute(
            "SELECT * FROM users WHERE phone=? AND password=?",
            (phone, password)
        )
        user = cur.fetchone()

        if user:
            session["user"] = user[1]
            session["phone"] = user[2]
            return redirect("/dashboard")

    return render_template("login.html")

# ================== REGISTER ==================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        db = get_db()
        db.execute(
            "INSERT INTO users (name, phone, password) VALUES (?,?,?)",
            (request.form["name"], request.form["phone"], request.form["password"])
        )
        db.commit()
        return redirect("/")

    return render_template("register.html")

# ================== MOCK DATA ==================
MARKET_PRICES = [
    {"crop": "Tomato", "price": "45/kg", "trend": "up"},
    {"crop": "Rice", "price": "60/kg", "trend": "stable"},
    {"crop": "Cotton", "price": "85/kg", "trend": "down"},
    {"crop": "Wheat", "price": "35/kg", "trend": "up"},
    {"crop": "Onion", "price": "25/kg", "trend": "stable"}
]

# ================== DASHBOARD ==================
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/")

    crop_ml = ""
    fertilizer = ""
    weather = None
    advice = ""
    disease = ""
    lang = "en"
    text = LANG_TEXT[lang]

    if request.method == "POST":
        # ---------- LANGUAGE ----------
        lang = request.form.get("lang", "en")
        text = LANG_TEXT.get(lang, LANG_TEXT["en"])

        # ---------- INPUTS ----------
        soil = request.form.get("soil", "Black")
        ph_val = request.form.get("ph")
        ph = float(ph_val) if ph_val else 6.5
        stage = request.form.get("stage", "Seedling")
        city = request.form.get("city", "Hassan")

        # ---------- ML CROP PREDICTION ----------
        try:
            soil_enc = soil_encoder.transform([soil])[0]
            crop_ml = model.predict([[soil_enc, ph]])[0]
        except:
            crop_ml = "Unknown"

        # ---------- AI FERTILIZER ----------
        if crop_ml == "Tomato" and stage == "Flowering":
            fertilizer = "Urea 45 kg + Potash 20 kg per acre"
        elif crop_ml == "Rice":
            fertilizer = "DAP 25 kg + Urea 50 kg per acre"
        elif crop_ml == "Cotton":
            fertilizer = "Urea 60 kg + Potash 25 kg per acre"
        else:
            fertilizer = "Compost 300 kg + NPK 20 kg per acre"

        # ---------- WEATHER ----------
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            data = requests.get(url).json()

            if data.get("cod") == 200:
                weather = {
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "wind": data["wind"]["speed"],
                    "desc": data["weather"][0]["description"].capitalize(),
                    "city": data["name"]
                }
                
                temp = weather["temp"]
                if temp > 35:
                    advice = f"🔥 Heatwave in {weather['city']}! Increase irrigation frequency."
                elif temp < 15:
                    advice = f"❄ Chilly in {weather['city']}. Protect young seedlings."
                else:
                    advice = f"✅ Ideal conditions in {weather['city']} for growth."
            else:
                advice = f"City '{city}' not found."
                weather = None
        except:
            advice = "Weather service unreachable."
            weather = None

        # ---------- IMPROVED DISEASE DETECTION ----------
        if 'leaf_image' in request.files:
            file = request.files['leaf_image']
            if file.filename != '':
                fname = file.filename.lower()
                # Simulate a more dynamic detection based on crop and filename keywords
                if "tomato" in fname or crop_ml == "Tomato":
                    diseases = [
                        "Late Blight detected. Advice: Apply Copper-based fungicide.",
                        "Tomato Leaf Curl Virus. Advice: Control whiteflies using neem oil.",
                        "Bacterial Spot. Advice: Remove infected plants and reduce humidity."
                    ]
                elif "rice" in fname or crop_ml == "Rice":
                    diseases = [
                        "Rice Blast. Advice: Use resistant varieties and avoid excessive nitrogen.",
                        "Bacterial Leaf Blight. Advice: Use balanced fertilizers and drain the field.",
                        "Sheath Blight. Advice: Remove weeds and use valid fungicides."
                    ]
                else:
                    diseases = [
                        "Healthy Leaf. Advice: Keep up the good work!",
                        "Nutrient Deficiency detected. Advice: Add organic compost.",
                        "General Pest Attack. Advice: Use organic pesticides."
                    ]
                
                # Pick a disease based on the hash of the filename for "predictability" during demo
                idx = len(fname) % len(diseases)
                disease = diseases[idx]

    return render_template(
        "dashboard.html",
        user=session["user"],
        crop_ml=crop_ml,
        fertilizer=fertilizer,
        weather=weather,
        advice=advice,
        text=text,
        lang=lang,
        market_prices=MARKET_PRICES,
        disease=disease
    )

# ================== LOGOUT ==================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ================== AI CHATBOT ENGINE ==================
def get_ai_response(query):
    query = query.lower()
    
    # Intent: Crop Recommendation Context
    if any(word in query for word in ["recommend", "grow", "suitable", "which crop"]):
        return "Based on your soil and region, my ML model can predict the best crop. Please fill the 'Farm Inputs' form for a precise analysis!"
    
    # Intent: Specific Crop Knowledge
    if "tomato" in query:
        return "Tomatoes thrive in deep, well-drained soil with 6.0-7.0 pH. Watch out for 'Late Blight' during humid weather."
    if "rice" in query or "paddy" in query:
        return "Rice requires consistent flooding (2-5cm) and nitrogen-rich fertilizers. Clayey soil is ideal for water retention."
    if "cotton" in query:
        return "Cotton needs a long frost-free period and moderate rainfall. It grows best in Black (Regur) soil."
    
    # Intent: Fertilizer Advice
    if any(word in query for word in ["fertilizer", "urea", "npk", "manure"]):
        return "Regular use of Organic Manure improves soil health. For chemical fertilizers, always follow the N-P-K ratio advised in your dashboard."
    
    # Intent: Disease & Pests
    if any(word in query for word in ["sick", "disease", "pest", "spot", "insects", "yellow"]):
        return "I recommend using the 'AI Leaf Scanner' feature on the dashboard. Upload a photo of the affected leaf for a quick diagnosis!"
    
    # Intent: Weather
    if any(word in query for word in ["weather", "rain", "temp", "cold", "hot"]):
        return "Weather affects irrigation needs. If it's above 35°C, increase watering. If rain is predicted, delay fertilization."
    
    # Intent: Market
    if any(word in query for word in ["price", "market", "sell", "rate", "cost"]):
        return "Currently, Tomato prices are trending UP. Rice prices are STABLE. Check the Market Trends card for live updates."
    
    # Fallback
    return "That's a great question! While I'm still learning about that specific topic, I recommend checking our 'AI Insights' dashboard for relevant farming data."

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    response = get_ai_response(user_msg)
    return {"response": response}

# ================== RUN ==================
if __name__ == "__main__":
    app.run(debug=True)
