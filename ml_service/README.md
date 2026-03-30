# ML Service – Computer Vision Model API

This service provides a machine learning inference API for the Computer Vision system developed as part of a Master's thesis project.  
The service loads a trained PyTorch model and exposes prediction endpoints using **FastAPI**.

The API is designed to run independently from the main backend and handle model inference requests.

---

## Requirements

- Python 3.9 or higher
- PyTorch
- FastAPI
- Uvicorn

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Model Setup

Before running the service, you must place the trained model file in the `models/` directory.

Expected structure:

```
ml_service/
│
├── main.py
├── models/
│   └── best.pt
├── requirements.txt
└── README.md
```

### Important Notes

- The model file must be a trained PyTorch `.pt` file.
- The expected filename is:

```
best.pt
```

- If you use a different filename, update the model loading path inside:

```
main.py
```

---

## Running the ML Service

To start the FastAPI server, run the following command from inside the `ml_service` directory:

```bash
uvicorn main:app --reload
```

The service will start locally at:

```
http://localhost:8000
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

After starting the service, open:

```
http://localhost:8000/docs
```

This interface allows you to:

- Send prediction requests
- Test endpoints
- Inspect request and response schemas

---

## Project Structure

```
ml_service/
│
├── main.py                 # FastAPI application
├── models/                 # Directory for trained model
│   └── best.pt             # Trained model file (not included in repository)
├── requirements.txt
└── README.md
```

---

## Notes

- The trained model file is **not included** in the repository.
- Users must place their own trained model inside the `models/` folder before running the service.
- This service is intended for **inference only**.
- Training is performed separately from this service.

---

## Example Workflow

```bash
cd ml_service

# Install dependencies
pip install -r requirements.txt

# Place trained model
# ml_service/models/best.pt

# Run the service
uvicorn main:app --reload
```

---

## Troubleshooting

### Model file not found

Error:

```
FileNotFoundError: best.pt
```

Solution:

Ensure the model file exists at:

```
ml_service/models/best.pt
```

and that the filename matches exactly.

---

## Author

Ricardo Manjarrez Retes  
Master's Thesis – Computer Vision System for Meat Marbling Classification