# IMPORTS
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
from tqdm import tqdm

from random_simulation import RandomSimulation
from dumb_simulation import DumbSimulation

# CODE
date = "2017-01-02_2019-01-01"

# Load data
df_courses = pd.read_csv(f"data/{date}/courses.csv", low_memory=False)
df_participants = pd.read_csv(f"data/{date}/participants.csv", low_memory=False)
with open(f"data/{date}/rapports_definitifs.json", "r") as f:
    rapports = json.load(f)

ordres = np.array(df_courses[["course_id", "ordreArrivee"]])
assert(len(ordres) == len(rapports))

participants = np.array(df_participants[["course_id", "numPmu", "dernierRapportDirect"]])

# Simulate
legends = []

rs = RandomSimulation(rapports, ordres)
k = 3
for k in tqdm(range(k)):
    rs.simulate()
    plt.plot(rs.gains)
    legends.append("Paris Random")

ds = DumbSimulation(rapports, participants)
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


