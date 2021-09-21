# IMPORTS
import pandas as pd
import numpy as np
from joblib import dump
from functools import reduce
import os
import json
from datetime import datetime

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import cross_validate
from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler

from training.simple_vectorizer import SimpleVectorizer
from training.preprocesser import Preprocesser
from utils.utils import plot_confusion_matrix

# CODE
"""
TASK: predire si un cheval va se placer / Binary Classification
"""
# Constants
date = "2015-01-01_2017-01-01"
specialite = "PLAT"
needed_columns = ["ordreArrivee", "gainsParticipant"]

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

# Undersampling
X,y = RandomUnderSampler().fit_resample(X,y)
print(f"Number of samples: {len(y)}")

# Train simple models
models = [
    LogisticRegression(class_weight="balanced"), # fast
    # KNeighborsClassifier(5), # long
    # MLPClassifier(hidden_layer_sizes=(20,20)), # long
    RandomForestClassifier(class_weight="balanced", max_depth=5, n_estimators=20, max_features=1), # fast
    AdaBoostClassifier(), # medium
]

scoring = ["accuracy", "roc_auc", "precision", "recall", "f1_weighted"]
for model in models:
    print(f"\n***** {type(model).__name__} *****\n")
    cv_results = cross_validate(model, X, y, scoring=scoring)
    for score in scoring:
        results = cv_results[f"test_{score}"]
        print(f"{score.upper()}: {np.mean(results)} - {results}")

    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print("")
    plot_confusion_matrix(y_test, y_pred)
    print(f"\nPourcentage de victoires prédites: {np.mean(y_pred)}")
    print(f"Pourcentage de victoires réelles: {np.mean(y_test)}")

    if type(model).__name__ != "RandomForestClassifier":
        continue 

    feature_importances = model.feature_importances_
    sum_ = sum(feature_importances)
    sorted_f = sorted([(-imp/sum_*100, vec.columns[i]) for i, imp in enumerate(feature_importances)])
    print("\nFeature Importances")
    for score, col in sorted_f:
        print(f"{col}: {-int(score)}%")

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
