from collections import defaultdict
import numpy as np
from tqdm import tqdm

# WARNING: WE NEED THIS EXACT ORDER
COURSES_FEATURES = ["montantPrix", "distance"]
PARTICIPANTS_FEATURES = ["nom", "driver", "course_id", "ordreArrivee"]

class BackwardTransformer():
    """
    Create new features for a given dataset.
    Look backward in the database to create features based on the previous races of a participant.
    """
    def __init__(self, df_participants, df_courses, window_horse=10, window_driver=100):
        """
        window: how far away we look at in the past (in number of races for the sake of simplicity but could be in number of days - TODO)
        """
        self.window_driver = window_driver
        self.window_horse = window_horse

        self.driver_statistics_p = len(COURSES_FEATURES) + 1 # +1 because of "number_of_places" feature, a bit CRAPPY - TODO
        self.courses = np.array(df_courses[COURSES_FEATURES])

        self.ordreArrivee_index = 3 # CRAPPY
        self.participants = np.array(df_participants[PARTICIPANTS_FEATURES])

    def get_previous_course_ids(self):
        """
        Create a dataframe that maps each participant (corresponding to a couple (horse, race)) to the previous races this horse has done
        """
        print("> Getting previous course ids...")
        self.previous_course_ids_driver = []
        self.previous_course_ids_horse = []

        d_horses = defaultdict(list)
        d_drivers = defaultdict(list)

        for participant_id, args in enumerate(tqdm(self.participants[:,:3])):
            horse, driver, course_id = args
            self.previous_course_ids_horse.append(np.array(d_horses[horse][-self.window_horse:])) # current race is not a previous race
            d_horses[horse].append([participant_id, course_id])

            self.previous_course_ids_driver.append(np.array(d_drivers[driver][-self.window_driver:]))
            d_drivers[driver].append([participant_id, course_id])



    def get_driver_statistics(self, ids):
        if ids.size < 30:
            return np.full(self.driver_statistics_p, 0)

        victoire = np.mean([place in [1,2,3] for place in self.participants[ids[:,0], self.ordreArrivee_index]])
        return np.concatenate((np.sum(self.courses[ids[:,1], :], axis=0), [victoire]))

    def get_X(self):
        print("> Getting driver statistics...")
        self.X = np.array(list(map(
            self.get_driver_statistics, tqdm(self.previous_course_ids_driver)
        )))

        indexes = list(map(lambda x: x[1], sorted([(score, i) for i,score in enumerate(self.X[:,2])])[-100:]))
        print("Best drivers:")
        print(np.unique(self.participants[indexes, 1]))