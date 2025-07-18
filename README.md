# ☀️ Helioshakti – Solar Energy Management Platform

> **Empowering users to estimate savings, manage installations, and monitor solar energy through an intelligent, interactive web dashboard.**

![Helioshakti Banner](static/images/banner5.png)
![Helioshakti Banner](static/images/banner4.png)

---

## 🚀 Overview

**Helioshakti** is a full-stack web application that simplifies solar energy management. From calculating savings to exploring government subsidies, it delivers everything a user needs to confidently switch to solar.

🔒 **Secure Login** | 📊 **ROI Calculator** | 💵 **Subsidy Estimator** | ⚡ **Panel Viewer** | 🧾 **EMI Breakdown** | 🔧 **Maintenance Alerts**

---

## 📦 Features

| Feature                   | Description |
|---------------------------|-------------|
| 🔐 **User Auth**          | Secure registration & login with session handling |
| 🧮 **Solar Dashboard**    | Estimate output, savings, payback period & ROI |
| 🛠️ **Maintenance Logs**  | Track scheduled maintenance with alert reminders |
| 💸 **Subsidy Calculator** | Get cost reduction based on capacity using Govt norms |
| 🏦 **EMI Planner**        | Calculate loan EMI with down payment & interest |
| ☀️ **Panel Models**       | Choose from low/medium/high panels with output & cost |
| 🔁 **ROI Notifications**  | Background thread that sends ROI updates to users |
| 🌍 **Location Input**     | Accepts pincode to tailor estimates by sunlight hours |

---

## 🧑‍💻 Technologies Used

### 🧠 Backend  
- **Python 3.10+**
- **Flask** (routing, templating, session)
- **SQLite** with **SQLAlchemy ORM**
- **WTForms** (form validation)
- **Geopy** (pincode geolocation)
- **Threading** (background ROI notifier)

### 🎨 Frontend  
- **Jinja2 Templates**
- **Bootstrap 5**
- **Custom CSS**
- **Static Images**

---

## 🗂️ Directory Structure
helioshakthi/
├── app.py # Main Flask application

├── forms.py # Form definitions (Login, Register, Dashboard)

├── models.py # DB Models: User, UsageData, Maintenance

├── templates/ # HTML templates

│ ├── base.html

│ ├── dashboard.html

│ └── ... etc

├── static/

│ ├── css/global.css

│ └── images/ # 02.jpeg, 03.jpeg, 04.jpeg, etc.

├── solar.db # SQLite DB (auto-generated)

└── README.md

---

## 🛠️ Setup & Installation

### ✅ Prerequisites:
- Python 3.10+
- pip (Python package installer)

### 📥 Steps to Run:

```bash
# 1. Clone the repo
git clone https://github.com/manii5228/helioshakthi.git
cd helioshakthi

# 2. Create & activate a virtual environment
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
python app.py

```


## 👥 Group Members 
- **Soma Prathibha** (Backend)
- **Dasari Vasu** (Frontend, R&D)
- **Innamuri Sai Ram** (Frontend, R&D)
- **Mani Manjunath.V** (Backend)

GitHub: github.com/manii5228
Project Repo: Helioshakti 🔗


