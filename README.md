# Insurance Premium Predictor

A machine learning app that predicts a person's **insurance premium category** (e.g. Low / Medium / High) from basic personal and lifestyle details. It has a **FastAPI** backend that serves the trained model and a **Streamlit** frontend for entering details and viewing the result.

## Features

- Predicts the premium category from a trained model (`model.pkl`)
- REST API built with FastAPI
- Clean Streamlit interface with a live BMI preview
- Returns the predicted category (and confidence / class probabilities when the API provides them)

## Project structure

```
.
├── app.py          # FastAPI backend (serves the model)
├── frontend.py     # Streamlit frontend
├── insurance.csv   # Dataset used to train the model
├── model.pkl       # Trained model
└── .gitignore
```

## Inputs

| Field        | Description                                   |
| ------------ | --------------------------------------------- |
| `age`        | Age in years                                  |
| `weight`     | Weight in kg                                  |
| `height`     | Height in metres                              |
| `income_lpa` | Annual income in lakhs per annum              |
| `smoker`     | Whether the person smokes (true / false)      |
| `city`       | City of residence                             |
| `occupation` | retired, freelancer, student, government_job, business_owner, unemployed, private_job |

## Getting started

### 1. Clone and set up

```bash
git clone https://github.com/Suryanxh/Insurance-Premium-Predictor.git
cd Insurance-Premium-Predictor

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install fastapi uvicorn streamlit requests scikit-learn pandas pydantic
```

### 2. Start the API

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Interactive API docs are available at `http://localhost:8000/docs`.

### 3. Start the frontend

In `frontend.py`, set `API_URL` to your API address, for example `http://localhost:8000/predict`. Then run:

```bash
streamlit run frontend.py
```

## Example request

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "weight": 65,
    "height": 1.7,
    "income_lpa": 10,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "private_job"
  }'
```

## Tech stack

Python, FastAPI, Streamlit, scikit-learn, pandas

## Notes

- Predictions are estimates and not an official insurance quote.
- The model file depends on the scikit-learn version it was trained with, so use the same version when running the API.
