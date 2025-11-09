<h1 align="center">🚀 BizPilot - Your AI Co-Pilot for Business Success 🤖</h1>

<p align="center">
  <b>An AI-powered platform to validate your business ideas, generate roadmaps, and guide you through the entrepreneurial journey.</b><br/>
  <i>Built with React, FastAPI, Python AI/ML, and Google Gemini API.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-Complete-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/frontend-React-blue?style=for-the-badge&logo=react"/>
  <img src="https://img.shields.io/badge/backend-FastAPI-green?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/AI-Gemini%20API-yellow?style=for-the-badge&logo=google-gemini"/>
  <img src="https://img.shields.io/badge/styling-Tailwind%20CSS-cyan?style=for-the-badge&logo=tailwindcss"/>
</p>

---

## 📸 App Screenshot

<p align="center" style="margin: 20px 0;">
 <img src="Website_preview/Screenshot 2025-11-07 200322.png" alt="Home Page" width="800"/>
</p>
<p align="center"><i>BizPilot AI Homepage</i></p>

<p align="center" style="margin: 20px 0;">
 <img src="Website_preview/Screenshot 2025-11-07 200408.png" alt="Home Page" width="800"/>
</p>
<p align="center"><i>BizPilot AI Homepage</i></p>

<p align="center" style="margin: 20px 0;">
 <img src="Website_preview/Screenshot 2025-11-07 200613.png" alt="Home Page" width="800"/>
</p>
<p align="center"><i>BizPilot AI Homepage</i></p>

<p align="center" style="margin: 20px 0;">
 <img src="Website_preview/Screenshot 2025-11-07 200636.png" alt="Home Page" width="800"/>
</p>
<p align="center"><i>BizPilot AI Footer Section</i></p>

<p align="center" style="margin: 20px 0;">
 <img src="Website_preview/Screenshot 2025-11-07 200820.png" alt="feature Page" width="800"/>
</p>
<p align="center"><i>BizPilot AI Feature page</i></p>

<p align="center" style="margin: 20px 0;">
 <img src="Website_preview/Screenshot 2025-11-07 200835.png" alt="Feature Page" width="800"/>
</p>
<p align="center"><i>BizPilot AI Feature page</i></p>

<p align="center" style="margin: 20px 0;">
 <img src="Website_preview/Screenshot 2025-11-07 200851.png" alt="Feature Page" width="800"/>
</p>
<p align="center"><i>BizPilot AI Feature page</i></p>


---

<img width="1892" height="870" alt="image" src="https://github.com/user-attachments/assets/104b932a-4a92-4135-ae04-ae387db1b318" />


---

## 🧠 Project Overview

BizPilot is a full-stack web application that acts as an AI-powered co-pilot for entrepreneurs.  

It simplifies starting and growing a business by providing:

- AI-based idea validation  
- Financial guidance and tax calculations  
- Investor matching  
- Startup learning resources  
- An interactive chat interface powered by Google Gemini API  

**Initial focus:** SMEs and startups in Bangladesh.

---

## 👥 The Team

- Mohammad Hossain – Software Developer  
- Mohammed Minul Islam – App & Web Developer  
- Kazi Namira Meyheg Sanam – Frontend & UI/UX Designer  
- Umme Benin Yeasmin Meem – Backend & ML Developer  

---

## 🎯 Project Objective

BizPilot aims to:

- Generate actionable business roadmaps using AI  
- Provide interactive chat support for refining business strategies  
- Simplify complex topics like taxes, registration, and market research  
- Serve as a complete tool from idea validation → financial planning → investor matching  

---

## ✨ Features

- 🔐 **User Authentication** – JWT-based login/signup  
- 🤖 **AI-Powered Idea Validation** – AI generates step-by-step business roadmaps  
- 💬 **Interactive Chat** – Ask follow-up questions to BizBot  
- 🎤 **Speech-to-Text** (Web Speech API placeholder)  
- 📊 **Dashboard with Charts** – Income, Expense, Profit, Tax Due  
- 📱 **Responsive Design** – Clean UI built with Tailwind CSS  
- 🚀 **Future Features** – Smart Finance, Investor Matching, Learning Hub  

---

## 🛠️ Tech Stack

### 🎯 Frontend (React + Vite + Tailwind)

- React.js – Component-based UI  
- Vite – Fast development server  
- Tailwind CSS – Styling framework  
- React Router DOM – Client-side routing  
- Recharts – Charts and visualizations  
- Axios – API calls to backend  
- JWT – Store tokens in localStorage for authentication  

**Frontend workflow:**  
User interacts with UI (Dashboard, AI Chat, Investors, Tax, Learning Hub) → Requests sent via Axios to FastAPI backend → JWT tokens sent in headers → Responses displayed dynamically.

---

### 🧩 Backend (FastAPI + Python AI/ML)

- FastAPI – REST API endpoints
- Transformers (Hugging Face) – AI text generation for roadmaps
- Scikit-learn – ML-based feasibility scoring
- Pydantic – Data validation
- CORS Middleware – Allow frontend requests
- Google Gemini API – AI integration

**Backend workflow:**
Receives requests from frontend (`/generate-roadmap`) → Validates input → Uses AI/ML models to generate roadmaps and scores → Returns JSON with roadmap and feasibility score.

---

### 🤖 AI Integration (Python AI/ML + Google Gemini)

- **Endpoint:** `/generate-roadmap`
- **Backend:** Uses Hugging Face Transformers for AI text generation and scikit-learn for ML feasibility scoring
- **Frontend:** Sends idea details, receives roadmap with feasibility score

**Flow:**
`React Frontend -> POST /generate-roadmap -> FastAPI Backend -> AI/ML Models -> Roadmap + Score -> Frontend`

---

## 📝 Setup Instructions

### 1️⃣ Backend
```bash
cd backend
python -m venv .venv
```

### Activate environment:
```
# Windows: .\.venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
```
```
pip install -r requirements.txt
```
### Create .env 
```
SECRET_KEY=your_jwt_secret
DATABASE_URL=sqlite:///./bizpilot.db
OPENAI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

### Start backend server:
```
uvicorn main:app --reload
```
### Backend runs at: 
`http://localhost:8000`

---

### 2️⃣ Frontend:
```bash
cd frontend
npm install
npm run dev
```
---
### Frontend runs at:
`http://localhost:5173
`

---

## ⚙️ How It Works

1.  User enters business idea details on the AI-powered idea validation page
2.  Frontend sends POST request to `/generate-roadmap` with idea, category, target audience
3.  Backend uses AI/ML models (Transformers for text generation, scikit-learn for scoring) to generate roadmap and feasibility score
4.  Backend returns JSON with roadmap text and feasibility score
5.  Frontend displays the AI-generated roadmap with feasibility score to the user

---

## ✅ Summary

- Frontend: React, Vite, Tailwind, Axios, JWT, Recharts
- Backend: FastAPI, Transformers, Scikit-learn, Pydantic, CORS
- AI/ML: Python-based AI text generation and ML feasibility scoring for business roadmaps
- Workflow: Frontend ↔ FastAPI Backend ↔ AI/ML Models

<p align="center"><i>BizPilot – AI-powered co-pilot for entrepreneurs, bridging ideas to execution.</i></p>












