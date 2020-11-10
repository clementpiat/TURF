import numpy as np
from ._simulation import Simulation
import random as rd

class GodSimulation(Simulation):
    """
    Pari à chaque course sur un cheval placé avec une probabilité p
    """
    def __init__(self, rapports, course_ids):
        super().__init__(rapports)
        self.course_ids = course_ids

    def simulate(self, p=1):
        self.gain = 0
        self.gains = []
        self.victoires = []

        for course_id in self.course_ids:
            course_id = str(int(course_id))
            rapport = self.rapports[course_id]
            if rapport != "Scraping failed":
                paris_place = list(filter(lambda r: r["typePari"] in ["SIMPLE_PLACE", "SIMPLE_PLACE_INTERNATIONAL"], rapport))
                if paris_place:
                    rapports_places = paris_place[0]["rapports"]
                    pari_places_gagnants = [r["combinaison"] for r in rapports_places if r["combinaison"].isdigit()]
                    if rd.random() < p and pari_places_gagnants:
                        pari = rd.choice(pari_places_gagnants)
                    else:
                        pari = -1 # We lose

                    self.pari_simple_place(pari, course_id)
