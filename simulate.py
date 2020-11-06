# IMPORTS
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from tqdm import tqdm
from joblib import load
import os
import json

from simulation import *

from training.vectorizer import SimpleVectorizer
from training.preprocesser import Preprocesser

# CODE
date = "2017-01-02_2019-01-01"
model_folder = "06_11_2020-10h58m07s"

# Load data
df_courses = pd.read_csv(f"data/{date}/courses.csv", low_memory=False)
df_participants = pd.read_csv(f"data/{date}/participants.csv", low_memory=False)
with open(f"data/{date}/rapports_definitifs.json", "r") as f:
    rapports = json.load(f)

# Prepare data for the simulations
# TODO: we should preprocess even without model
if model_folder:
    model = load(os.path.join("models", model_folder, "clf.joblib"))
    with open(os.path.join("models", model_folder, "config.json"), "r") as f:
        d = json.load(f)
    preprocesser = Preprocesser(d["specialite"], needed_columns=d["needed_columns"])
    df_participants = preprocesser.filter_rows(df_participants, df_courses)

random_participants = np.array(df_participants[["course_id", "numPmu"]])
dumb_participants = np.array(df_participants[["course_id", "numPmu", "dernierRapportDirect"]])
if model_folder:
    X = SimpleVectorizer().transform(df_participants)
    df_participants["winning_probability"] = model.predict_proba(X)[:,1]
    model_participants = np.array(df_participants[["course_id", "numPmu", "winning_probability"]])

# Simulate
legends = []

if model_folder:
    ms = ModelSimulation(rapports, model_participants)
    ms.simulate()
    plt.plot(ms.gains)
    legends.append(f"Paris selon modèle")
    
rs = RandomSimulation(rapports, random_participants)
k = 3
for k in tqdm(range(k)):
    rs.simulate()
    plt.plot(rs.gains)
    legends.append("Paris Random")

ds = DumbSimulation(rapports, dumb_participants)
for p in tqdm(range(3)):
    ds.simulate(p=p)
    plt.plot(ds.gains)
    legends.append(f"Paris {p+1}ème côte la plus faible")

plt.legend(legends)

plt.ylabel("Gains en euros")
plt.xlabel("Nombre de paris")
plt.title(f"Evolution du gains pour la stratégie pari aléatoire à chaque course ({k} simulations aléatoires)")

plt.text(0,-4000,f"Nombre de victoires aléatoires: {sum(rs.victoires)}\nNombre de victoires naives: {sum(ds.victoires)}")

plt.show()


