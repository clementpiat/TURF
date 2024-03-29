from functools import reduce
import random
from ._simulation import Simulation

class RandomSimulation(Simulation):
    """
    Pari à chaque course sur un cheval aléatoire en simple placé
    """
    def __init__(self, rapports, participants):
        super().__init__(rapports)
        self.participants = participants
        
    def simulate(self):
        self.gain = 0
        self.gains = []
        self.victoires = []

        prev_course_id = self.participants[0,0]
        numPmus = []
        for course_id, numPmu in self.participants:
            if course_id == prev_course_id:
                numPmus.append(numPmu)
            else:
                pari = random.choice(numPmus)
                self.pari_simple_place(pari, prev_course_id)

                numPmus = [numPmu]
                prev_course_id = course_id