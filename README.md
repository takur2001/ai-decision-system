# 🚀 Autonomous Risk & Decision Intelligence System

An end-to-end AI-powered platform for **fraud detection, risk scoring, and intelligent decision-making**, deployed with a full-stack architecture.

---

## 🔥 Live Demo

* 🌐 **Frontend**: https://ai-decision-system-kvqfav59tmfhjgcmtvkskh.streamlit.app
* ⚙️ **Backend API**: https://ai-decision-system-mw63.onrender.com
* 📄 **API Docs**: https://ai-decision-system-mw63.onrender.com/docs

---

## 🧠 Overview

This system processes **unstructured fraud case descriptions**, extracts key entities, evaluates risk levels, and generates actionable decisions.

### 🎯 What it does:

* Converts raw text → structured insights
* Detects fraud patterns
* Assigns risk scores
* Recommends actions (e.g., escalation)

---

## 🏗️ Architecture

```text
User Input → Streamlit UI → FastAPI Backend → AI Processing Engine → Database (SQLite)
```

---

## 🧰 Tech Stack

### 🔧 Backend

* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication

### 🎨 Frontend

* Streamlit
* Plotly (Data Visualization)

### ☁️ Deployment

* Render (Backend)
* Streamlit Cloud (Frontend)

---

## 🔐 Features

### 🔑 Authentication

* Secure Signup & Login
* JWT-based authentication
* Protected API routes

---

### 🧠 Case Analysis

* Analyze fraud-related text
* Entity extraction (amount, date)
* Risk classification (low / medium / high)
* Decision recommendation engine

---

### 📊 Dashboard

* Total cases overview
* High-risk case tracking
* Average risk score
* Latest decision insights

---

### 📁 Case History

* User-specific records
* Persistent database storage
* Real-time refresh

---

## 📊 Example Input

```json
{
  "text": "Unauthorized transaction of $5000 detected on March 28"
}
```

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
```

---

## 📸 Screenshots

###🔧 Backend

<img width="1919" height="966" alt="image" src="https://github.com/user-attachments/assets/1b86b26f-0513-4806-9483-863b8f14e327" />

### 🔐 Login Page

<img width="1919" height="692" alt="image" src="https://github.com/user-attachments/assets/852ba7ee-ed78-40cd-b137-b041e703e2ed" />


### 📊 Dashboard

<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/4c1ac38e-3fdf-4237-8f4b-ae19992829ec" />
<img width="1919" height="963" alt="image" src="https://github.com/user-attachments/assets/be0ee5f7-2969-4c1f-a651-2b289d250ec2" />


---

## 🚀 How to Run Locally

```bash
# Clone repo
git clone https://github.com/takur2001/ai-decision-system.git

# Go into project
cd ai-decision-system

# Install dependencies
pip install -r requirements.txt

# Run backend
uvicorn app.main:app --reload

# Run frontend
streamlit run dashboard.py
```

---

## 💡 Future Improvements

* Add real ML/NLP model (BERT / LLM)
* PostgreSQL instead of SQLite
* Docker containerization
* Role-based access control
* API rate limiting

---

## 👨‍💻 Author

**Karthik Chalamalasetty**
AI Engineer | Data Scientist

---
