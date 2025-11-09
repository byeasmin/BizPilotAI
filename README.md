<h1 align="center">🚀 BizPilot - Your AI Co-Pilot for Business Success 🤖</h1>

<p align="center">
  <b>An AI-powered platform to validate your business ideas, generate roadmaps, and guide you through the entrepreneurial journey.</b><br/>
  <i>Built with React, FastAPI, and the Google Gemini API.</i>
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

### 🧩 Backend (FastAPI + SQLModel)

- FastAPI – REST API endpoints  
- SQLModel / SQLite – Database for Users, Transactions, Investors, Business Scores  
- Pydantic – Data validation  
- JWT – Authentication  
- CORS Middleware – Allow frontend requests  
- OpenAI / Google Gemini API – AI integration  

**Backend workflow:**  
Receives requests from frontend (`/auth`, `/transactions`, `/dashboard`, `/investors`, `/tax`, `/ai/chat`) → Validates input → Performs database operations → Generates AI responses → Returns JSON.

---

### 🤖 AI Integration (Google Gemini / LLM)

- **Endpoint:** `/ai/chat`  
- **Backend:** Sends user messages to Google Gemini API (or dummy AI)  
- **Frontend:** Receives streaming response and renders progressively  

**Flow:**  
`React Frontend -> POST /ai/chat -> FastAPI Backend -> Google Gemini API -> Response -> Frontend`

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
---
### Server runs at: http://localhost:8000
---

---

### 2️⃣ Frontend:
```bash
cd frontend
npm install
npm run dev
```
---
### Frontend runs at: http://localhost:5173
---

---

## ⚙️ How It Works

1.  User logs in / signs up → JWT token stored in localStorage
2.  Frontend sends API requests → Backend endpoints: `/transactions`, `/dashboard/summary`, `/investors`, `/tax/calculate`, `/ai/chat`
3.  Backend authenticates, validates, fetches data from SQLite
4.  AI Chat requests forwarded to Google Gemini API → Response streamed back to frontend
5.  Frontend updates UI in real-time (dashboard cards, charts, chat bubbles, notifications)

---

## ✅ Summary

- Frontend: React, Vite, Tailwind, Axios, JWT, Recharts
- Backend: FastAPI, SQLModel/SQLite, JWT, Pydantic, CORS
- AI: Google Gemini API / LLM integration for idea validation & business advice
- Workflow: Frontend ↔ Backend ↔ AI API

<p align="center"><i>BizPilot – AI-powered co-pilot for entrepreneurs, bridging ideas to execution.</i></p>









