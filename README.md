# 🚀 Autonomous Risk & Decision Intelligence System

An end-to-end AI-powered platform for fraud detection, risk scoring, and intelligent decision-making with a full-stack deployment.

---

## 🔥 Live Demo

- 🌐 Frontend: https://ai-decision-system-kvqfav59tmfhjgcmtvkskh.streamlit.app
- ⚙️ Backend API: https://ai-decision-system-mw63.onrender.com
- 📄 API Docs: https://ai-decision-system-mw63.onrender.com/docs

---

## 🧠 Overview

This system analyzes unstructured case descriptions (like fraud reports), extracts key entities, assigns risk scores, and recommends actions such as escalation.

It includes:

- Secure user authentication (JWT)
- Case analysis engine
- File upload + text processing
- User-specific case history
- Real-time analytics dashboard

---

## 🏗️ Tech Stack

### Backend
- FastAPI
- SQLite
- JWT Authentication
- SQLAlchemy
<img width="1919" height="975" alt="image" src="https://github.com/user-attachments/assets/39b12091-df09-42ad-93ec-6032832dd4e7" />

### Frontend
- Streamlit
- Plotly (visualizations)
<img width="1919" height="967" alt="image" src="https://github.com/user-attachments/assets/03c7b4c1-80d7-4814-b4e1-04c2c6f43eff" />
<img width="1919" height="962" alt="image" src="https://github.com/user-attachments/assets/a08aaf39-325e-49f7-9463-e92c603c14e7" />

### Deployment
- Render (Backend)
- Streamlit Cloud (Frontend)

---

## 🔐 Features

### Authentication
- Signup & Login
- JWT-based secure APIs

### Case Analysis
- Analyze fraud-related text
- Extract entities (amount, date)
- Risk scoring (low / medium / high)
- Decision recommendation

### Dashboard
- Total cases
- High-risk cases
- Average risk score
- Latest decision

### Case History
- User-specific data
- Stored in database
- Real-time refresh

---

## 📊 Example Input

```json
{
  "text": "Unauthorized transaction of $5000 detected on March 28"
}


## 📊 Example Output
{
  "entities": {
    "amount": "$5000",
    "date": "March 28"
  },
  "risk_level": "high",
  "decision": "Escalate for manual review"
}
