# 🌾 Smart Agri Guide – AI Powered Agriculture Platform

Smart Agri Guide is a **modern AI-powered agriculture web application** that helps farmers and agriculture students make **data-driven farming decisions** using **Machine Learning, AI chatbot, weather intelligence, and a modern PWA-based interface**.

This project is suitable for:
- Final Year Engineering Project
- AI / ML Demonstration
- Smart Agriculture Prototype
- Startup MVP

---

## 🚀 Features

### 🤖 Artificial Intelligence & Machine Learning
- **ML-Based Crop Recommendation**
  - Predicts the best crop based on **soil type** and **soil pH**
  - Trained using a **CSV dataset** representing Indian soil conditions
- **AI Agriculture Chatbot**
  - Powered by **Gemma 3 1B Instruct**
  - Answers agriculture-related questions such as:
    - Best crop for soil
    - Fertilizer usage
    - Farming best practices

---

### 🌦️ Weather Intelligence
- Real-time temperature data using **OpenWeather API**
- Smart weather-based advisories:
  - High temperature → Increase irrigation
  - Normal temperature → Suitable for farming

---

### 🧪 Fertilizer Recommendation
- AI-assisted fertilizer suggestions based on:
  - Predicted crop
  - Crop growth stage
- Simple and farmer-friendly recommendations

---

### 👨‍🌾 Farmer Authentication
- Secure **Login & Registration system**
- Passwords stored using **hashing (Werkzeug)**
- Session-based authentication

---

### 🎨 Modern User Interface
- Dark futuristic **IoT-style dashboard**
- Floating labels
- Animated form validation
- Error message UI
- Fully mobile responsive design

---

### 📱 Progressive Web App (PWA)
- Installable on mobile devices
- Offline caching support
- App-like experience on Android

---

### 🌍 Multi-Language Support
- English 🇬🇧
- Kannada 🇮🇳
- Hindi 🇮🇳

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3 (Modern Dark UI)
- JavaScript
- PWA (Service Worker & Manifest)

### Backend
- Python
- Flask

### AI / ML
- Scikit-learn (Decision Tree Classifier)
- Pandas
- Joblib
- Gemma 3 1B Instruct (Google / OpenRouter)

### Database
- SQLite

### APIs
- OpenWeather API
- Google Gemini API / OpenRouter

---

## 📁 Project Structure
AgriWebsite/
│
├── app.py
├── train_model.py
├── crop_model.pkl
├── soil_encoder.pkl
├── users.db
│
├── data/
│ └── crop_data.csv
│
├── static/
│ ├── style.css

└── templates/
├── login.html
├── register.html
└── dashboard.html

---

## ⚙️ Installation & Setup

###  Clone the Repository
```bash
git clone https://github.com/your-username/smart-agri-guide.git
cd smart-agri-guide

pip install flask requests pandas joblib scikit-learn werkzeug

setx GEMINI_API_KEY "YOUR_GOOGLE_API_KEY"
setx OPENWEATHER_API_KEY "YOUR_OPENWEATHER_API_KEY"

python app.py

http://127.0.0.1:5000



