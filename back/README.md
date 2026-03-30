## Backend (FastAPI + Motor + MongoDB)

### Requisitos
- Python 3.11+
- MongoDB local (ej: mongodb://localhost:27017)

### Setup
```bash
cd back
python -m venv .venv 
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip
pip install -e .
```

- run command
uvicorn app.main:app --reload
