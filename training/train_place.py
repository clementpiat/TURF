# IMPORTS
import pandas as pd
import numpy as np
from vectorizer import SimpleVectorizer
from functools import reduce
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_validate

# CODE
"""
TASK: predire si un cheval va se placer / Binary Classification
"""
# Constants
date = "2015-01-01_2017-01-01"
specialite = "PLAT"

# Load
df_participants = pd.read_csv(f"data/{date}/participants.csv", low_memory=False)
df_courses = pd.read_csv(f"data/{date}/courses.csv", low_memory=False)

# Join
restricted_df_courses = df_courses[["course_id", "specialite"]]
df = df_participants.join(restricted_df_courses.set_index("course_id"), on="course_id")

# Filter
df.drop(df[df["specialite"] != specialite].index, inplace=True)
df.dropna(subset=["ordreArrivee"], inplace=True)

# Vectorize / Create X
vec = SimpleVectorizer()
X = vec.transform(df)

# Create target labels / Create y
y = df["ordreArrivee"].apply(lambda x: int(x) in [1,2,3]).to_list()
print(f"Number of samples: {len(y)}")

# Train a simple model
lr = LogisticRegression()
cv_results = cross_validate(lr, X, y, scoring=["accuracy", "roc_auc"])
print(f"Accuracy: {cv_results['test_accuracy']}")
print(f"AUC: {cv_results['test_roc_auc']}")

lr.fit(X, y)
print(f"Pourcentage de victoires prédites: {np.mean(lr.predict(X))}")
print(f"Pourcentage réelle: {np.mean(y)}")