from sklearn.preprocessing import LabelEncoder
import numpy as np
import re

NUMERICAL_COLUMNS = ["nombreCourses", "nombreVictoires", "nombrePlaces", "handicapPoids", "tauxReclamation", "placeCorde", 
"poidsConditionMonte", "nombrePlacesSecond", "nombrePlacesTroisieme", "handicapValeur"]
CATEGORICAL_COLUMNS = ["oeilleres", "deferre", "sexe", "race", "age", "numPmu", "statut"]

class SimpleVectorizer():
    def __init__(self):
        self.label_encoders = [None] * len(CATEGORICAL_COLUMNS)
        self.columns = []

    def transform(self, df):
        n,_ = df.shape

        df[NUMERICAL_COLUMNS] = df[NUMERICAL_COLUMNS].fillna(df[NUMERICAL_COLUMNS].mean())
        l = [df[col].to_list() for col in NUMERICAL_COLUMNS]
        self.columns += NUMERICAL_COLUMNS

        for i, col in enumerate(CATEGORICAL_COLUMNS):
            le = LabelEncoder()
            l.append(le.fit_transform(df[col].to_list()))
            self.label_encoders[i] = le
            self.columns.append(col)

        # musique
        l.append(df["musique"].apply(self.musique_to_score).to_list())
        self.columns.append("musique")
        # gains
        l.append(df["gainsParticipant"].apply(lambda d: eval(d)["gainsCarriere"] if eval(d) else 0).to_list())
        l.append(df["gainsParticipant"].apply(lambda d: eval(d)["gainsAnneeEnCours"] if eval(d) else 0).to_list())
        self.columns += ["gainsCarriere", "gainsAnneeEnCours"]

        X = np.array(l).T
        return X

    def musique_to_score(self, musique, default_score=6):
        if not isinstance(musique, str) or musique in ["-", "couru afasec"]:
            return default_score

        resultats = re.split("[a-z]+", musique)[:-1]

        def resultats_to_score(resultat):
            # (2019)8 becomes 8
            resultat = re.sub("\(\d+\)", "", resultat)
            if resultat in ["D", "R", "I", "é"]:
                return 6
            elif resultat in ["A", "T"]:
                return 11
            elif int(resultat) in range(1,9):
                return int(resultat)
            else:
                return 11

        scores = list(map(resultats_to_score, resultats))
        return np.mean(scores)
