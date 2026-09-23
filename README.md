# 🍱 अन्नसेतू महाराष्ट्र

### Smart Food Rescue Platform

> **Save Food • Serve People • Build a Better Future 🌱**

अन्नसेतू महाराष्ट्र हे एक Smart Food Rescue Platform आहे जे हॉटेल्स, रेस्टॉरंट्स, मेस, कार्यक्रम आणि इतर Food Donors कडील उपलब्ध सुरक्षित अन्न जवळच्या NGOs पर्यंत पोहोचवण्यासाठी तयार केले आहे.

या platform चा उद्देश अन्नाची नासाडी कमी करणे आणि उपलब्ध अन्न गरजू लोकांपर्यंत वेळेत पोहोचवणे हा आहे.

---

## 📌 Project Overview

दररोज मोठ्या प्रमाणावर सुरक्षित आणि वापरण्यायोग्य अन्न उरते. योग्य वेळी योग्य संस्थेशी संपर्क न झाल्यामुळे हे अन्न वाया जाऊ शकते.

**अन्नसेतू महाराष्ट्र** या समस्येसाठी एक digital platform उपलब्ध करून देते.

Food Donor उपलब्ध अन्नाची माहिती platform वर add करतो आणि NGO उपलब्ध donations पाहून योग्य food donation claim करू शकते.

Platform मध्ये location, distance, urgency आणि food information च्या आधारावर **Smart Match** तयार केला जातो.

---

## 🚀 Key Features

### 👤 User Authentication
- User Registration
- Secure Login & Logout
- Password Hashing
- Role-based Access

### 🍱 Food Donation
- Food donation add करणे
- Food name आणि type
- Quantity
- Number of people served
- Prepared time
- Safe until time
- Address आणि location
- Donation status tracking

### 🧠 Smart Food Match
- Available food donations शोधणे
- Location आणि distance आधारित matching
- Urgency based matching
- Quantity related matching
- NGOs साठी suitable food suggestions

### 🤝 Food Claim System
- NGO available food पाहू शकते
- Suitable donation claim करू शकते
- Self-claim protection
- Already claimed donation पुन्हा claim करता येत नाही

### 📍 Location System
- User location update
- Latitude & Longitude support
- Distance calculation
- Location-based food matching

### 🚚 Donation Status
Donation चा status track करता येतो:

```text
Available
   ↓
Claimed
   ↓
Picked Up
   ↓
Delivered
🔔 Notification System
Food donation claim झाल्यावर Donor ला notification
Pickup status update notification
Delivery status update notification
Read / Unread notification system
Mark all notifications as read
📊 Role-Based Dashboard
🍱 Donor Dashboard
Food donations
Available donations
Claimed donations
Donation status
Recent activity
Notifications
🏢 NGO Dashboard
Available food
Smart matched food
Claimed food
Pickup / Delivery status
Notifications
Location
🙋 Volunteer
Volunteer role support
Platform participation
🧠 Smart Matching

अन्नसेतू महाराष्ट्रमध्ये Smart Match system उपलब्ध food donations आणि NGO requirements यांच्यामध्ये suitable matching करण्यासाठी वापरला जातो.

Matching मध्ये खालील factors चा वापर केला जातो:

📍 Distance
⏰ Food urgency
🍱 Food availability
👥 Required quantity
📊 Matching score

यामुळे NGO ला उपलब्ध food donations मधून योग्य donation शोधणे सोपे होते.

👥 User Roles
🍱 Donor

Donor platform वर:

Register / Login करू शकतो
Food donation add करू शकतो
स्वतःच्या donations पाहू शकतो
Donation status track करू शकतो
Claim आणि delivery notifications पाहू शकतो
🏢 NGO

NGO:

Available food पाहू शकते
Smart Match recommendations पाहू शकते
Food donation claim करू शकते
Claimed food track करू शकते
Pickup आणि delivery status update करू शकते
🙋 Volunteer

Volunteer role platform मध्ये support आणि participation साठी उपलब्ध आहे.

🛠️ Technology Stack
Backend
Python
Flask
Flask-SQLAlchemy
Flask-Login
Flask-WTF
Frontend
HTML5
CSS3
JavaScript
Jinja2 Templates
Database
SQLite
SQLAlchemy ORM
Development Tools
Git
GitHub
Python Virtual Environment
📂 Project Structure
anna-setu-maharashtra/
│
├── database/
│
├── migrations/
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/
│
├── app.py
├── config.py
├── location_utils.py
├── quantity_utils.py
├── urgency_utils.py
├── utils.py
├── test_match.py
│
├── requirements.txt
├── .gitignore
└── README.md
⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/yogibhokare18/anna-setu-maharashtra.git
2. Navigate to Project Folder
cd anna-setu-maharashtra
3. Create Virtual Environment

Windows:

python -m venv venv
4. Activate Virtual Environment

Windows:

venv\Scripts\activate
5. Install Dependencies
pip install -r requirements.txt
6. Run the Application
python app.py
7. Open in Browser
http://127.0.0.1:5000
🔐 Security

The application includes:

Secure password hashing
Login authentication
Role-based authorization
Protected routes
User-specific notifications
Donation ownership checks
Donation status validation
Environment files excluded through .gitignore
📋 Main Application Flow
                ┌──────────────────┐
                │      User        │
                │   Registration   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │      Login       │
                └────────┬─────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      ┌──────────────┐        ┌──────────────┐
      │    Donor     │        │     NGO      │
      └──────┬───────┘        └──────┬───────┘
             │                       │
             ▼                       ▼
      Add Food Donation       View Available Food
             │                       │
             │                       ▼
             │                Smart Food Match
             │                       │
             │                       ▼
             │                Claim Donation
             │                       │
             └───────────┬───────────┘
                         ▼
                  Pickup / Delivery
                         │
                         ▼
                  Notification
🔔 Notification Flow
Donor adds Food
       ↓
NGO views Food
       ↓
NGO claims Food
       ↓
Donor receives Notification
       ↓
Food Picked Up
       ↓
Status Updated
       ↓
Food Delivered
       ↓
Donor receives Notification
🧪 Testing

The project includes matching-related testing through:

test_match.py

The application can be tested through:

User registration
Login / Logout
Food donation
Food listing
Smart matching
Food claiming
Pickup status
Delivery status
Notifications
Location updates
Role-based access
🌱 Social Impact

अन्नसेतू महाराष्ट्रचा उद्देश technology च्या मदतीने:

🍚 Food Waste कमी करणे
🤝 Donors आणि NGOs connect करणे
📍 Nearby food availability शोधणे
⏰ Food वेळेत rescue करणे
❤️ गरजू लोकांपर्यंत अन्न पोहोचवणे

हा आहे.

🔮 Future Scope

भविष्यात platform मध्ये खालील features जोडता येतील:

📱 Android / iOS Mobile Application
🗺️ Advanced Google Maps Integration
📊 Food Rescue Analytics Dashboard
🤖 Advanced Recommendation System
📧 Email Notifications
📲 SMS Notifications
🔔 Push Notifications
🌐 Multi-city Food Rescue Network
📈 NGO & Donor Performance Analytics
🏆 Volunteer Recognition System
🎯 Project Goal

"उरलेले अन्न वाया जाऊ नये, योग्य व्यक्तीपर्यंत पोहोचावे."

अन्नसेतू महाराष्ट्र technology च्या माध्यमातून Food Donors, NGOs आणि Volunteers यांना एका platform वर connect करण्याचा प्रयत्न करते.

👨‍💻 Team

Team Name: FoodTech Heroes

Project Name: अन्नसेतू महाराष्ट्र

Category: Smart Food Rescue Platform

📜 License

This project is developed for educational and project demonstration purposes.

🌱 Save Food • Serve People • Build a Better Future 🚀

