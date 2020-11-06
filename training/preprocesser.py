class Preprocesser():
    def __init__(self, specialite, needed_columns=[]):
        self.specialite = specialite
        self.needed_columns = needed_columns

    def filter_rows(self, df_participants, df_courses):
        restricted_df_courses = df_courses[["course_id", "specialite"]]
        df = df_participants.join(restricted_df_courses.set_index("course_id"), on="course_id", rsuffix="courses")

        df.drop(df[df["specialite"] != self.specialite].index, inplace=True)
        df.dropna(subset=self.needed_columns, inplace=True)

        return df