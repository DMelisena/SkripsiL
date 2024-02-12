lateral-cal update :
Water phantom dimension creation 
1.  PDD on 40x40x50 for 50_000 slice
2.  Through the center of water phantom
    1.  X (50x0.1x0.1) on 1 2.5 5 10 15 20 25 30
    2.  Y (50x0.1x0.1) on 1 2.5 5 10 15 20 25 30
    3.  X (50x50x0.1) on 1 2.5 5 10 15 20 25 30
    4.  Y (50x50x0.1) on 1 2.5 5 10 15 20 25 30
3.  Heatmap on  1 2.5 5 10 15 20 25 30


To Do List :
Make a lateral reading for LINAC callibration
- Make a slice on x and y on a certain LINAC distancee
Find a way to read phsp file?
Find a way to modify the output of linac? using electron simulation?

#Directory Guide:
- Perhitungan Analitik
    - Primer
    - Sekunder
    - Pintu
- Simulasi OPENMC
    - CellRSHS (Listing final deteksi rotasi linac)
        - cellRSHSFIX.py
        - doseplotcell.py
    - Kalibrasi (600 MU/min to uSv/h pada dmax water phantom)
        - kalibrasiSimpel
            - 1kalibrasiSimpel.py
            - reader.py
-   - hasilServer (Output dari running server)
        -Kalibrasi
            -reader.py
        -270deg
            -doseplotcell.py

# SkripsiL
Perhitungan analitik dan openmc untuk skripsi

Todolist:
-Ngetes kode cell filter dose
    -Masih kurang paham bentuk output openmc
-Post Processing Cell Filter
-Pembandingan dengan nilai deteksi
-Pembuatan formula laju dosis analitik
-Pembandingan hasil perhitungan laju dosis dengan nilai deteksi
-Penulisan pembahasan untuk simulasi dan perhitungan

File Tree Directory :
linac  -> File JIH
openmc -> File Eksperimental
rshs   -> Simulasi RSHS
Program untuk NCRP no.151:
RSHSPrimer.py
RSHSSekunder.py
auto2darray.py
RSHSPintu.py


########## Update 300723
Hasil Dosis nya aneh, beda jauh. Sepertinya masalah di konversi flux ke dose rate. Harus buat 
branch baru :
1. Bikin Tally di tengah (Buat tally grid juga) V
2. Buat Post Processing
3. Cek Dose ratenya sesuai dari ICRP atau tidak 
4. Run simulation 3mil particles 2 batch (Simpan Hasil)
5. Bandngkan dengan dosis analitik
6. Konsul ke Mbak Oksel soal s_rate
BUAT : cek dosis analitik
Haruskah buat fungsi untuk nentuin sumbu x?

########## Update 270723
Simulasi sudah benar, tapi belum dicoba untuk cell tally. Konversi flux ke dose rate sudah dilakukan.

########## Update 280623 ##########
Saat ini nilai2 yang dimasukkan ke berkasnya sudah menghasilkan hasil yang benar
Should I just make it load an external txt file instead so i would be able to make it automatically convert the value on the text?
To make it fully automated, what i need to consider is whether it's plausible to have a conceivable input method.
What are the variables and what are the repeatable constant.
Var   : 
W = The number of patient and Gy could be varied 
U = The number of use factor, I still don't understand it yet
T = Occupancy Factor tergantung dengan ruangan di sekitar, jadi tergantung
Const : 
F = Seharusnya sekitar 41^2 cm kan? gatau sih jenis linac lain gimana
a = Dari regresi linear