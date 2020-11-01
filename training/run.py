# IMPORTS
import pandas as pd
from vectorizer import SimpleVectorizer

# CODE
date = "2015-01-01_2017-01-01"
df = pd.read_csv(f"data/{date}/participants.csv", low_memory=False)

vec = SimpleVectorizer()
X = vec.transform(df)
print(X.shape, X[0])