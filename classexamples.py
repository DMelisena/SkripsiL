class rectangle:
    def __init__(kotak,p,l):
        kotak.p=p
        kotak.l=l
    def luas(kotak):
        print(f"Luas kotak ini adalah {kotak.l*kotak.p}")
kotakA=rectangle()
kotakA.p=4
kotakA.l=3
kotakA.luas()

#Masih gapaham perbedaan antara ada init dan ga ada init