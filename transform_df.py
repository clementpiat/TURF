# IMPORTS
from backward_transformer import BackwardTransformer
import pandas as pd

# CODE
"""
Create new features
"""
# Constants
date = "2015-01-01_2017-01-01"

# Load
df_participants = pd.read_csv(f"data/{date}/participants.csv", low_memory=False)
df_courses = pd.read_csv(f"data/{date}/courses.csv", low_memory=False)

bt = BackwardTransformer(df_participants, df_courses)
bt.get_previous_course_ids()
bt.get_X()
print(bt.X.shape)