# 🧠 Plan & Act Agent – Intern Project (Implementation)

**Developer:** Chris 
**Tech Stack:** React (Vite), FastAPI, LangGraph, LangChain
**Status:** MVP + Streaming + Tools Completed

---

## 📌 Project Overview

Αυτό το repository περιέχει την υλοποίηση του **Plan & Act Agent**. Πρόκειται για ένα πλήρως λειτουργικό, Full-Stack agentic σύστημα που δεν απαντά απλά σαν chatbot, αλλά σκέφτεται, σχεδιάζει και εκτελεί βήματα χρησιμοποιώντας εξωτερικά εργαλεία.

---

## 🎯 Core Capabilities Implemented

### ✅ 1. Plan Creation & Visibility
- Ο **Planner Agent** αναλύει το ερώτημα και επιστρέφει ένα αυστηρό JSON πλάνο.
- Το πλάνο εμφανίζεται στο Frontend **πριν** και **κατά τη διάρκεια** της εκτέλεσης.

### ✅ 2. Dynamic Execution & Tool Usage
- Ο **Executor Agent** αναλαμβάνει να "τρέξει" το πλάνο.
- Επιλέγει αυτόματα το σωστό εργαλείο για το κάθε βήμα.
- **Error Handling:** Έχει ενσωματωμένο σύστημα **Max 2 Retries** σε περίπτωση που ένα εργαλείο αποτύχει.

### ✅ 3. Real-Time Streaming (SSE)
- Μηδενικός χρόνος αναμονής (White screen).
- Το backend χρησιμοποιεί **Server-Sent Events** για να στέλνει ζωντανά updates στη React (δημιουργία πλάνου -> in progress -> completed -> τελική απάντηση).

### ⏳ 4. Conversation Memory (In Progress)
- Προετοιμασία υποδομής για μνήμη των τελευταίων 10 μηνυμάτων (Phase 4).

---

## 🧰 Tools System

Το σύστημα υποστηρίζει επεκτάσιμα εργαλεία. Αυτή τη στιγμή είναι ενσωματωμένα τα εξής:

- 🌐 **web_search:** Για real-time αναζήτηση στο ίντερνετ (μέσω DuckDuckGo).
- 🧮 **calculator:** Για μαθηματικούς υπολογισμούς.
- 📄 **file_reader:** Για ανάγνωση τοπικών αρχείων κειμένου.
- 🧠 **none:** Ειδικό fallback για βήματα που απαιτούν απλή λογική (π.χ. σύνταξη κειμένου), αποτρέποντας τα LLM hallucinations.

---

## 🧠 Architecture (Multi-Agent Pattern)

Το Backend είναι χτισμένο πάνω στο **LangGraph** και ακολουθεί αρχιτεκτονική πολλαπλών κόμβων (Nodes):

1. **Planner Node:** Παράγει το JSON Plan.
2. **Executor Node:** Καλεί τα Tools και ανανεώνει το status.
3. **Finalizer Node:** Συνθέτει το τελικό Markdown κείμενο αυστηρά στα Ελληνικά.

### 📁 Mini File Structure
```text
agentic-planner/
├── backend/                  
│   ├── core/                 # LangGraph Logic (Agents, Graph, Tools)
│   └── main.py               # FastAPI Streaming Server (Port 8001)
└── frontend/                 
    └── src/App.jsx           # React UI & SSE Fetch Logic (Port 5173)
```

---

## 💻 How to Run Locally

### 1. Backend (FastAPI)
Από τον φάκελο `backend/`:
```bash
python -m venv venv
# Ενεργοποίηση venv (Windows: .\venv\Scripts\activate)
pip install -r requirements.txt
```
*Φτιάξτε ένα `.env` αρχείο και προσθέστε το API key*
```bash
uvicorn main:app --reload --port 8001
```

### 2. Frontend (React/Vite)
Από τον φάκελο `frontend/`:
```bash
npm install
npm run dev
```
Ανοίξτε τον browser στο **http://localhost:5173**