from sklearn.preprocessing import LabelEncoder
import numpy as np

NUMERICAL_COLUMNS = ["nombreCourses", "nombreVictoires", "nombrePlaces"]
CATEGORICAL_COLUMNS = ["oeilleres", "deferre"]

class SimpleVectorizer():
    def __init__(self):
        self.label_encoders = [None] * len(CATEGORICAL_COLUMNS)

    def transform(self, df):
        n,_ = df.shape

        l = [df[col].to_list() for col in NUMERICAL_COLUMNS]

        for i, col in enumerate(CATEGORICAL_COLUMNS):
            le = LabelEncoder()
            l.append(le.fit_transform(df[col].to_list()))
            self.label_encoders[i] = le
            print(le.classes_)

        X = np.array(l).T
        return X

