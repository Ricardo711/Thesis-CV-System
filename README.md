# Computer Vision System for Meat Marbling Classification

This repository contains a **computer vision–based educational system** developed as part of a Master's thesis project.  
The system integrates a backend API, a frontend web application, and a machine learning inference service to support interactive learning through image-based classification tasks.

The application is designed around a **game-based learning environment** composed of three mini-games that guide students through classification, comparison, and AI-assisted decision-making tasks.

---

## System Overview

The system consists of **three main components**:

1. **Backend API**
   - Handles authentication, sessions, game logic, and database operations
   - Built with FastAPI and MongoDB

2. **Frontend Application**
   - Provides the user interface for gameplay and interaction
   - Built with Vue 3 and Vite

3. **ML Service**
   - Performs image classification using a trained deep learning model
   - Built with FastAPI and PyTorch

These components run as independent services that communicate through HTTP requests.

---

## Game Structure

The learning system is organized into **games** composed of multiple interactions.

- One **game** consists of **12 interactions**
- Each game includes **three mini-games**

### Mini-Game 1 — Classification

- Students are shown a single image
- Students select the correct marbling class
- Students provide a confidence level
- Immediate feedback is provided

### Mini-Game 2 — Image Comparison

- Students compare multiple images
- Students select the image that matches a target class
- Difficulty is dynamically adjusted based on class similarity

### Mini-Game 3 — AI-Assisted Prediction

- Students upload an image
- A deep learning model generates a prediction
- Students can revise their answer after seeing the AI prediction
- Students rate their trust in the AI system

Mini-game 3 uses a **deep learning model** as the primary backbone to generate predictions.

---

## System Architecture

```
Frontend (Vue + Vite)
        |
        v
Backend API (FastAPI + MongoDB)
        |
        v
ML Service (FastAPI + PyTorch)
```

---

## Project Structure

```
Thesis-CV-System/
│
├── back/                 # Backend API
├── frontend/             # Frontend application
├── ml_service/           # Machine learning inference service
│
├── .env.example          # Environment configuration template
├── .gitignore
└── README.md
```

---

## Requirements

### General

- Python 3.9 or higher
- Node.js 18 or higher
- MongoDB
- Git

---

## Environment Configuration

Create a `.env` file in the root directory using the provided template:

```
.env.example
```

Example:

```
cp .env.example .env
```

Then update the values according to your local environment.

---

# Running the System

Each component must be started separately.

---

# 1. Backend — FastAPI + MongoDB

## Requirements

- Python 3.11+
- MongoDB running locally or remotely

Example local MongoDB:

```
mongodb://localhost:27017
```

---

## Setup

Navigate to the backend directory:

```bash
cd back
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

Linux / Mac:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -U pip
pip install -e .
```

---

## Run Backend

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

# 2. Frontend — Vue 3 + Vite

## Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

## Run Frontend

```bash
npm run dev
```

Frontend will run at:

```
http://localhost:5173
```

---

# 3. ML Service — Model Inference API

This service loads a trained deep learning model and exposes prediction endpoints.

---

## Requirements

- Python 3.9+
- PyTorch
- FastAPI
- Uvicorn

---

## Model Setup

Before running the service, place the trained model file inside:

```
ml_service/models/
```

Expected:

```
ml_service/
│
├── main.py
├── models/
│   └── best.pt
```

Important:

- The model must be a trained PyTorch `.pt` file
- The filename should be:

```
best.pt
```

---

## Setup

```bash
cd ml_service
python -m venv .venv
```

Activate:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Run ML Service

```bash
uvicorn main:app --reload
```

Service will run at:

```
http://localhost:8001
```

API documentation:

```
http://localhost:8001/docs
```

---

## Recommended Startup Order

1. Start MongoDB
2. Start Backend
3. Start ML Service
4. Start Frontend

---

## Notes

- The trained model file is not included in the repository
- Users must provide their own trained model
- The system is designed for research and educational use
- The ML service performs inference only (no training)

---

## Troubleshooting

### Model file not found

```
FileNotFoundError: best.pt
```

Solution:

Ensure the file exists:

```
ml_service/models/best.pt
```

---

## Author

Ricardo Manjarrez Retes  
Master's Thesis — Computer Vision System for Meat Marbling Classification  
New Mexico State University

---

## License

This project is intended for academic and research purposes.
