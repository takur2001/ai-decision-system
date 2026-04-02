# 🚀 Autonomous Risk & Decision Intelligence System

An end-to-end AI-powered platform for fraud detection, risk scoring, and intelligent decision-making with a full-stack deployment.

---

## 🔥 Live Demo

- 🌐 Frontend: https://YOUR-STREAMLIT-URL
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

### Frontend
- Streamlit
- Plotly (visualizations)

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

---

## 📊 Example Output
```json
{
  "entities": {
    "amount": "$5000",
    "date": "March 28"
  },
  "risk_level": "high",
  "decision": "Escalate for manual review"
}
