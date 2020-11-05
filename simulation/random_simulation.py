from functools import reduce
import random
from simulation import Simulation

class RandomSimulation(Simulation):
    """
    Pari à chaque course sur un cheval aléatoire en simple placé
    """
    def __init__(self, rapports, ordres):
        super().__init__(rapports)
        self.ordres = ordres
        
    def simulate(self):
        self.gain = 0
        self.gains = []
        self.victoires = []

        for course_id, ordreArrivee in self.ordres:
            course_id = course_id
            ordreArrivee = eval(ordreArrivee)
            if ordreArrivee: 
                pari = random.choice(reduce(lambda i,j: i+j, ordreArrivee))
                self.pari_simple_place(pari, course_id)
