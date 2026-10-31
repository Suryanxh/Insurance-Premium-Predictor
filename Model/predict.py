import pickle
from pathlib import Path
import pandas as pd

# import the ml model
with (Path(__file__).resolve().parent / 'model.pkl').open('rb') as f:
    model = pickle.load(f)

# MLFlow
MODEL_VERSION = '1.0.0'

# get class labels from model(important for matching probabilities to class name)
class_labels = model.classes_.tolist()

def predict_output(user_input : dict):

    df = pd.DataFrame([user_input])

    # predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    # create mapping : {class_name : probability}
    class_probs = dict(zip(class_labels, map(lambda p : round(p, 4), probabilities)))

    return {
        "predictes_category" : predicted_class,
        "confidence" : round(confidence, 4),
        "class_probabilities" : class_probs
    }

