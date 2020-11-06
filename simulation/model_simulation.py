from functools import reduce
from ._simulation import Simulation

class ModelSimulation(Simulation):
    """
    Pari à chaque course sur le cheval le plus probable selon un modèle
    """
    def __init__(self, rapports, participants):
        super().__init__(rapports)
        self.participants = participants

    def simulate(self):
        self.gain = 0
        self.gains = []
        self.victoires = []

        prev_course_id = self.participants[0,0]
        probas = []
        for course_id, numPmu, winning_probability in self.participants:
            if course_id == prev_course_id:
                probas.append((winning_probability, numPmu))
            else:
                pari = max(probas)[1]
                self.pari_simple_place(pari, prev_course_id)

                probas = [(winning_probability, numPmu)]
                prev_course_id = course_id