#Directory Guide:
kk

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
Radiation dose Calculation using analytical method and Monte Carlo Particle simulation for Medical Linear Accelerator Bunker

TODO: Make a 3d heatmap and a bit of interface for the analytical method

Result Example:
![alt text](https://github.com/DMelisena/SkripsiL/blob/main/2simulasi/CellRSHS/10kk/270/RoomDoseDistribution.png?raw=true)
This is a heatmap of Radiation Dose on and at the surrounding of a Medical Linear Accelerator Bunker
more of this is available in bahasa on https://bit.ly/NPMAryaH

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
