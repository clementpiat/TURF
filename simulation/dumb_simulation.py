import numpy as np
from ._simulation import Simulation

class DumbSimulation(Simulation):
    """
    Pari à chaque course sur la côte la plus basse
    """
    def __init__(self, rapports, participants):
        super().__init__(rapports)
        self.participants = participants

    def simulate(self, p=0):
        self.gain = 0
        self.gains = []
        self.victoires = []

        prev_course_id = self.participants[0,0]
        rapports = []
        for course_id, numPmu, rapport in self.participants:
            rapport = eval(rapport)
            if rapport:
                rapport = float(rapport["rapport"])
                if course_id == prev_course_id:
                    rapports.append((rapport, numPmu))
                else:
                    if len(rapports) >= p+1:
                        pari = sorted(rapports)[p][1]
                        self.pari_simple_place(pari, prev_course_id)

                    rapports = [(rapport, numPmu)]
                    prev_course_id = course_id



