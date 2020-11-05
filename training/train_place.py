# IMPORTS
import pandas as pd
from vectorizer import SimpleVectorizer
from functools import reduce

# CODE
"""
TASK: predire si un cheval va se placer / Binary Classification
"""
date = "2015-01-01_2015-01-03"
df_participants = pd.read_csv(f"data/{date}/participants.csv", low_memory=False)
df_courses = pd.read_csv(f"data/{date}/courses.csv", low_memory=False)

vec = SimpleVectorizer()
X = vec.transform(df_participants)
print(X.shape, X[0])

# Create target labels
restricted_df_participants = df_participants[["course_id", "numPmu"]]
restricted_df_courses = df_courses[["course_id", "ordreArrivee"]]

df = restricted_df_participants.join(restricted_df_courses.set_index("course_id"), on="course_id")
df["places"] = df["ordreArrivee"].apply(lambda l: reduce(lambda i,j: i+j, eval(l)[:3]))
y = df[["numPmu", "places"]].apply(lambda x: (x[0] in x[1]), axis=1).to_list()
print(len(y))

# Train a model