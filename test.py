
class Arbre_Tache():
    def __init__(self):
        self.arbre = [[{}]]

    def lastIndex(self) -> int:
        print(f"index : {len(self.arbre)}")
        return (len(self.arbre) - 1)

    def add(self, tache_id, tache_nom, tache_duree, tache_anterieur):
        lastIndex = self.lastIndex()
        try:
            self.arbre[lastIndex][tache_id]["nom"] = tache_nom
            self.arbre[lastIndex][tache_id]["duree"] = tache_duree
            self.arbre[lastIndex][tache_id]["tache_a"] = tache_anterieur
        except IndexError:
            self.arbre.append(self.arbre[lastIndex][tache_id]["nom"])
            self.arbre.append(self.arbre[lastIndex][tache_id]["duree"])
            self.arbre.append(self.arbre[lastIndex][tache_id]["tache_a"])
            self.arbre[lastIndex][tache_id]["nom"] = tache_nom
            self.arbre[lastIndex][tache_id]["duree"] = tache_duree
            self.arbre[lastIndex][tache_id]["tache_a"] = tache_anterieur

    # def supprimer_tache(self, tache_id):
    #     for n in self.arbre:
    #         if n[tache_id] == tache_id:
    #             popitem(self.arbre[n])

    def calculSuccesseur(self):
        pass

    def afficher_tableau(self):
        for n in self.arbre:
            print(f"{n}\n")


arbre1 = Arbre_Tache()

arbre1.add(0, "A", 22, "NULL")
arbre1.add(1, "B", 90, ["A", "C"])

arbre1.afficher_tableau()
