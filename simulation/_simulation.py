# TODO: refactor even more since they all have participants attributes
class Simulation():
    def __init__(self, rapports):
        self.rapports = rapports

    def simulate(self):
        pass

    def pari_simple_place(self, pari, course_id):
        pari, course_id = str(int(pari)), str(int(course_id))
        if self.rapports[course_id] != "Scraping failed":
            paris_place = list(filter(lambda r: r["typePari"] in ["SIMPLE_PLACE", "SIMPLE_PLACE_INTERNATIONAL"], self.rapports[course_id]))
            if paris_place:
                rapports_places = paris_place[0]["rapports"]
                victoire = list(filter(lambda r: r["combinaison"] == pari, rapports_places))

                if victoire:
                    self.victoires.append(1)
                    self.gain += -1 + victoire[0]["dividende"]/100
                else:
                    self.victoires.append(0)
                    self.gain += -1

                self.gains.append(self.gain)