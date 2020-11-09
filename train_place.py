# IMPORTS
import pandas as pd
import numpy as np
from joblib import dump
from functools import reduce
import os
import json
from datetime import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate
from sklearn.ensemble import RandomForestClassifier

from training.vectorizer import SimpleVectorizer
from training.preprocesser import Preprocesser
from utils.utils import plot_confusion_matrix

# CODE
"""
TASK: predire si un cheval va se placer / Binary Classification
"""
# Constants
date = "2015-01-01_2017-01-01"
specialite = "PLAT"
needed_columns = ["ordreArrivee"]

# Load
df_participants = pd.read_csv(f"data/{date}/participants.csv", low_memory=False)
df_courses = pd.read_csv(f"data/{date}/courses.csv", low_memory=False)

# Filter
preprocesser = Preprocesser(specialite, needed_columns = needed_columns)
df = preprocesser.filter_rows(df_participants, df_courses)

# Vectorize / Create X
vec = SimpleVectorizer()
X = vec.transform(df)

# Create target labels / Create y
y = df["ordreArrivee"].apply(lambda x: int(x) in [1,2,3]).to_list()
print(f"Number of samples: {len(y)}")

# Train simple models
models = [
    LogisticRegression(),
    RandomForestClassifier(class_weight="balanced")
]
for model in models:
    print(f"\n***** {type(model).__name__} *****")
    cv_results = cross_validate(model, X, y, scoring=["accuracy", "roc_auc", "f1_weighted"])
    print(f"Accuracy: {cv_results['test_accuracy']}")
    print(f"AUC: {cv_results['test_roc_auc']}")
    print(f"F1: {cv_results['test_f1_weighted']}\n")

    model.fit(X, y)
    y_pred = model.predict(X)
    plot_confusion_matrix(y, y_pred)
    print(f"\nPourcentage de victoires prédites: {np.mean(y_pred)}")
    print(f"Pourcentage réelle: {np.mean(y)}")

# Optionally save model
if False:
    name = datetime.now().strftime("%d_%m_%Y-%Hh%Mm%Ss")
    model = models[-1]

    model_folder = os.path.join("models", name)
    os.mkdir(model_folder)
    dump(model, os.path.join(model_folder, "clf.joblib"))
    with open(os.path.join(model_folder, "config.json"), "w+") as f:
        d = {
            "typePari": "SIMPLE_PLACE",
            "date": date,
            "specialite": specialite,
            "needed_columns": needed_columns,
            "columns": vec.columns,
            "X_shape": X.shape,
            "model": type(model).__name__
        }
        json.dump(d, f)
