class rectangle:
    def __init__(self,p=None,l=None):
        self.p=p
        self.l=l
    def luas(self):
        print(f"Luas kotak ini adalah {self.l*self.p}")
kotakA=rectangle()
kotakA.p=4
kotakA.l=3
kotakA.luas()

#Masih gapaham perbedaan antara ada init dan ga ada init