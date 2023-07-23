################################################################################
#|----------------------------------------------------------------------------|#
#| OpenMC Python API Input |#
#| Evaluasi Desain Ruangan Bunker LINAC 10 MV RS JIH |#
#|----------------------------------------------------------------------------|#
################################################################################
import openmc
import matplotlib.pyplot as plt
from math import pi, sin, cos
################################################################################
# Materials #
################################################################################
m001 = openmc.Material(name='Air')
m001.set_density('g/cm3', 0.001205)
m001.add_element('C', 0.000124, 'wo')
m001.add_element('N', 0.755268, 'wo')
m001.add_element('O', 0.231781, 'wo')
m001.add_element('Ar', 0.012827, 'wo')

m002 = openmc.Material(name='Collimator')
m002.set_density('g/cm3', 17)
m002.add_nuclide('W184', 0.905, 'ao')
m002.add_nuclide('Ni58', 0.065, 'ao')
m002.add_nuclide('Fe56', 0.03, 'ao')

m003 = openmc.Material(name='Soft Tissue')
m003.set_density('g/cm3', 1)
m003.add_element('C', 0.232190, 'wo')
m003.add_element('Mg', 0.00013, 'wo')
m003.add_element('S', 0.001990, 'wo')
m003.add_element('Cl', 0.001340, 'wo')
m003.add_element('K', 0.001990, 'wo')
m003.add_element('Ca', 0.000230, 'wo')
m003.add_element('Fe', 0.000050, 'wo')
m003.add_element('Zn', 0.000030, 'wo')
m003.add_element('H', 0.104472, 'wo')
m003.add_element('N', 0.024880, 'wo')
m003.add_element('O', 0.630238, 'wo')
m003.add_element('Na', 0.001130, 'wo')
m003.add_element('P', 0.001330, 'wo')

m004 = openmc.Material(name='Borated Polyethylene')
m004.set_density('g/cm3', 1)
m004.add_element('H', 0.125355, 'wo')
m004.add_element('C', 0.774645, 'wo')
m004.add_element('B', 0.1, 'wo')
m005 = openmc.Material(name='Lead')
m005.set_density('g/cm3', 11.35)
m005.add_element('Pb',1.00, 'wo')

m999 = openmc.Material(name='Concrete, Ordinary')
m999.set_density('g/cm3', 2.35)
m999.add_element('H', 0.005558, 'wo')
m999.add_element('O', 0.498076, 'wo')
m999.add_element('Na', 0.017101, 'wo')
m999.add_element('Mg', 0.002565, 'wo')
m999.add_element('Al', 0.045746, 'wo')
m999.add_element('Si', 0.315092, 'wo')
m999.add_element('S', 0.001283, 'wo')
m999.add_element('K', 0.019239, 'wo')
m999.add_element('Ca', 0.082941, 'wo')
m999.add_element('Fe', 0.012398, 'wo')

mat = openmc.Materials([m001, m002, m003, m004, m005, m999])
mat.export_to_xml()

################################################################################
# Geometry #
################################################################################
####################################################
rot = 270 # Degree of Rotation (0 - 360) ##
####################################################
# Pasien (Titik Referensi), kuning tengah
x00 = -94.0
y00 = -44.5
z00 = -75.0

# Total Dimensi Ruangan, kotak hitam utama
x = 840
y = 735
z = 250

# Tebal Dinding
F = 209
F1 = 120
#209 - 93 = 89
I = 226
I1 = 147
#226 - 147 = 79
E = 85
G = 74
H = 90
# Dimensi Dinding, Gap, Lorong, dll
L1 = 120
L2 = 195
Q1 = 90
Q2 = 300

# Kolimator
xk = 34.0
yk = 35.0
zk1 = 7
zk2 = 21
zg = 10
zkol = 100 - zk1 - zk2 - zg # Jarak Kolimator Sekunder ke Pasien
hole1 = 4/2
hole1h = 6.1
hole2 = 3.7

# Door
pb = 1.5
bpe = 8.7

#fe=
# Patient
xa = 32
yb = 152
zc = 20

# Detector
xdet = 50
ydet = 50
zdet = 50

################################# SURFACE ##################################
#dengan x sebagai sumbu x total dari ruangan
s01 = openmc.XPlane((x/2), boundary_type='transmission')
s02 = openmc.XPlane((-x/2), boundary_type='transmission')
s03 = openmc.YPlane((y/2), boundary_type='transmission')
s04 = openmc.YPlane((-y/2), boundary_type='transmission')
s05 = openmc.XPlane((x/2)-E, boundary_type='transmission')
s06 = openmc.YPlane((y/2)-G, boundary_type='transmission')
s07 = openmc.YPlane((-y/2)+H, boundary_type='transmission')
s08 = openmc.XPlane((-x/2)+I1, boundary_type='transmission')
s09 = openmc.XPlane((x/2)-E-L1, boundary_type='transmission')
s10 = openmc.XPlane((x/2)-E-L1-F1, boundary_type='transmission')
s11 = openmc.YPlane((y/2)-G-L2, boundary_type='transmission')
s12 = openmc.YPlane((-y/2)+H+Q1, boundary_type='transmission')
s13 = openmc.YPlane((-y/2)+H+Q1+Q2, boundary_type='transmission')

#Surface Dinding Primer
s14 = openmc.XPlane((x/2)-E-L1-F, boundary_type='transmission')
s15 = openmc.XPlane((-x/2)+I, boundary_type='transmission')

# Surface Sumbu Z
s16 = openmc.ZPlane(z/2, boundary_type='vacuum')
s17 = openmc.ZPlane(-z/2, boundary_type='vacuum')

# Kolimator Sekunder
s21 = openmc.XPlane(x00+(xk/2.0), boundary_type='transmission')
s22 = openmc.XPlane(x00-(xk/2.0), boundary_type='transmission')
s23 = openmc.YPlane(y00+(yk/2.0), boundary_type='transmission')
s24 = openmc.YPlane(y00-(yk/2.0), boundary_type='transmission')
s25 = openmc.ZPlane(z00+zkol+zk2, boundary_type='transmission')
s26 = openmc.ZPlane(z00+zkol, boundary_type='transmission')
s31 = openmc.XPlane(x00+(hole2/2.0), boundary_type='transmission')
s32 = openmc.XPlane(x00-(hole2/2.0), boundary_type='transmission')
s33 = openmc.YPlane(y00+(hole2/2.0), boundary_type='transmission')
s34 = openmc.YPlane(y00-(hole2/2.0), boundary_type='transmission')

#Kolimator Primer
s41 = openmc.XPlane(x00+(xk/2.0), boundary_type='transmission')
s42 = openmc.XPlane(x00-(xk/2.0), boundary_type='transmission')
s43 = openmc.YPlane(y00+(yk/2.0), boundary_type='transmission')
s44 = openmc.YPlane(y00-(yk/2.0), boundary_type='transmission')
s45 = openmc.ZPlane(z00+zkol+zk2+zg+zk1, boundary_type='transmission')
s46 = openmc.ZPlane(z00+zkol+zk2+zg, boundary_type='transmission')
s47 = openmc.ZCone(x0=x00, y0=y00, z0=(z00+zkol+zk2+zg+hole1h),\
                r2=(0.052377301357642*2),\
                boundary_type='transmission')
s48 = openmc.ZPlane(z00+zkol+zk2+zg+hole1h, boundary_type='transmission')

#Surface Door
s49 = openmc.YPlane((-y/2)-pb, boundary_type='transmission')
s50 = openmc.YPlane((-y/2)-pb-bpe, boundary_type='transmission')
s51 = openmc.YPlane((-y/2)-pb-bpe-pb, boundary_type='transmission')

#soft Tissue
s52 = openmc.XPlane(x00+(xa/2), boundary_type='transmission')
s53 = openmc.XPlane(x00-(xa/2), boundary_type='transmission')
s54 = openmc.YPlane(y00+(yb/2), boundary_type='transmission')
s55 = openmc.YPlane(y00-(yb/2), boundary_type='transmission')
s56 = openmc.ZPlane(z00+(zc/2), boundary_type='transmission')
s57 = openmc.ZPlane(z00-(zc/2), boundary_type='transmission')

#Detector I
s58 = openmc.XPlane((-x/2)-(xdet), boundary_type='vacuum')
s59 = openmc.YPlane(y00+(ydet/2), boundary_type='transmission')
s60 = openmc.YPlane(y00-(ydet/2), boundary_type='transmission')
s61 = openmc.ZPlane(z00+(zdet/2), boundary_type='transmission')
s62 = openmc.ZPlane(z00-(zdet/2), boundary_type='transmission')
#Detector G
s63 = openmc.XPlane(x00+(xdet/2), boundary_type='transmission')
s64 = openmc.XPlane(x00-(xdet/2), boundary_type='transmission')
s65 = openmc.YPlane(y/2+(ydet), boundary_type='vacuum')
#Detector H
s68 = openmc.YPlane((-y/2)-(ydet), boundary_type='transmission')
#Detector F
s69 = openmc.XPlane(((x/2)-E-L1)+xdet, boundary_type='transmission')
#Detector I'
s70 = openmc.YPlane((-y/2)+H+ydet, boundary_type='transmission')
#Detector E'
s71 = openmc.XPlane((x/2)+xdet, boundary_type='vacuum')
s72 = openmc.YPlane((y/2)-ydet, boundary_type='transmission')
#Detector Door
s73 = openmc.XPlane(((x/2)-E)-(L1/2)+(xdet/2), boundary_type='transmission')
s74 = openmc.XPlane(((x/2)-E)-(L1/2)-(xdet/2), boundary_type='transmission')
s75 = openmc.YPlane((-y/2)-pb-bpe-pb-ydet, boundary_type='vacuum')
# Surface of Primary Collimator WITH ROTATION
s211 = s21.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s221 = s22.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s231 = s23.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s241 = s24.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s251 = s25.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s261 = s26.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s311 = s31.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s321 = s32.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s331 = s33.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s341 = s34.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
# Surface of Secondary Collimator WITH ROTATION
s411 = s41.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s421 = s42.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s431 = s43.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s441 = s44.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s451 = s45.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s461 = s46.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s471 = s47.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
s481 = s48.rotate(rotation=([0.0,rot,0.0]), pivot=[x00,y00,z00], order='yxz')
################################### CELL ###################################
r01 = -s01 & +s05 & +s04 & -s03 & -s16 & +s17
c01 = openmc.Cell(fill=m999, region=r01)
r02 = -s03 & +s06 & +s02 & -s05 & -s16 & +s17
c02 = openmc.Cell(fill=m999, region= r02)
r03 = -s08 & +s02 & +s07 & -s06 & -s16 & +s17
c03 = openmc.Cell(fill=m999, region= r03)
r04 = -s15 & +s08 & +s12 & -s13 & -s16 & +s17
c04 = openmc.Cell(fill=m999, region=r04)
r05 = -s07 & +s04 & +s02 & -s09 & -s16 & +s17
c05 = openmc.Cell(fill=m999, region=r05)
r06 = -s09 & +s10 & +s07 & -s11 & -s16 & +s17
c06 = openmc.Cell(fill=m999, region=r06)
r07 = +s14 & -s10 & +s12 & -s11 & -s16 & +s17
c07 = openmc.Cell(fill=m999, region=r07)
# Kolimator Sekunder
r08 = -s311 & +s321 & -s331 & +s341 & -s251 & +s261
c08 = openmc.Cell(fill=m001, region=r08)
r09 = -s211 & +s221 & -s231 & +s241 & -s251 & +s261
c09 = openmc.Cell(fill=m002, region=r09 & ~r08)
# Kolimator Primer
r10 = -s471 & +s461 & -s481
c10 = openmc.Cell(fill=m001, region=r10)
r11 = -s411 & +s421 & -s431 & +s441 & -s451 & +s461
c11 = openmc.Cell(fill=m002, region=r11 & ~r10)
#patient
r15 = -s52 & +s53 & -s54 & +s55 & -s56 & +s57
c15 = openmc.Cell(fill=m003, region = r15)
#Detector I'
r23 = +s58 & -s02 & -s70 & +s07 & -s61 & +s62
c23 = openmc.Cell(fill=m003, region = r23)
#Detector I
r16 = +s58 & -s02 & -s59 & +s60 & -s61 & +s62
c16 = openmc.Cell(fill=m003, region = r16)
r17 = -s02 & +s58 & -s65 & +s75 &-s16 & +s17
c17 = openmc.Cell(fill=m001, region = r17 & ~r16 & ~r23)
#Detector G
r18 = -s63 & +s64 & +s03 & -s65 & -s61 & +s62
c18 = openmc.Cell(fill=m003, region = r18)
r19 = +s02 & -s01 & +s03 & -s65 &-s16 & +s17
c19 = openmc.Cell(fill=m001, region = r19 & ~r18)
#Detector H
r21 = -s63 & +s64 & +s68 & -s04 & -s61 & +s62
c21 = openmc.Cell(fill=m003, region = r21)
#Detector F
r22 = +s09 & -s69 & -s59 & +s60 & -s61 & +s62
c22 = openmc.Cell(fill=m003, region = r22)
#Detector F'
r24 = +s09 & -s69 & -s70 & +s07 & -s61 & +s62
c24 = openmc.Cell(fill=m003, region = r24)

#Detector E'
r25 = -s71 & +s01 & -s03 & +s72 & -s61 & +s62
c25 = openmc.Cell(fill=m003, region = r25)
r26 = -s71 & +s01 & -s65 & +s75 &-s16 & +s17
c26 = openmc.Cell(fill=m001, region = r26 & ~r25)

#Detector Door
r27 = -s73 & +s74 & -s51 & +s75 & -s61 & +s62
c27 = openmc.Cell(fill=m003, region = r27)

#Door
r12 = -s49 & +s50 & -s05 & +s09 & -s16 & +s17
c12 = openmc.Cell(fill=m004, region = r12)
r13 = -s04 & +s51 & -s05 & +s09 & -s16 & +s17
c13 = openmc.Cell(fill=m005, region = r13 & ~r12)
r14 = +s02 & -s01 & -s04 & +s75 & -s16 & +s17
c14 = openmc.Cell (fill=m001, region = r14 & ~r13 & ~r21 & ~r27)

beton = r01 | r02 | r03 | r04 | r05 | r06 | r07 | r08 | r09 | r10 | r11 | r15 \
        | r22 | r24
c99 = openmc.Cell(fill=m001, region=(-s01 & -s03 & +s02 & +s04 & -s16 & +s17 & \
                                    (~beton)))
universe = openmc.Universe(cells=(c01,c02,c03,c04,c05,c06,c07,\
                                c08,c09,c10,c11,c99,c12,c13,c14,c15,c16,c17,\
                                c18,c19,\
                                c21,c22,c23,c24,c25,c26,c27))
colors = {}
colors[m001] = 'pink'
colors[m002] = 'green'
colors[m003] = 'yellow'
colors[m004] = 'darkorange'
colors[m005] = 'indigo'
colors[m999] = 'gray'
ooxy = (0.0, 0.0, z00+zkol+(zk2/2)) # Plot XY di Kolimator Sekunder
ooxy2 = (0.0, 0.0, z00) # Plot XY di Soft Tissue
ooxz = (0.0, y00, 0.0) # Plot XZ
ooxz2 = (x00, y00, z00) # Plot Kolimator
universe.plot(
    origin=ooxy2,
    # width=(x+100+10, x+100+10),
    width=(x+2*xdet, y+2*ydet),
    pixels=(500, 500),
    basis='xy',
    color_by='material',
    colors=colors)
plt.savefig('fig1.png')
plt.show()

geom = openmc.Geometry(universe)
geom.export_to_xml()
################################################################################
# Settings #
################################################################################
d = (zkol+zk2+zg+hole1h-0.1+1) #62+21+10+6.1-0.1+1=100

pos_source = 
            """
            ( d*(sin(radians(rot))) ), \
             0, \
             75+( d*(cos(radians(rot)) ) \
             
            """
            (
                x00 + ( d*(sin(rot)) ), \
                y00, \
                z00 + ( d*(cos(rot)) ) \
            )



settings = openmc.Settings()
source = openmc.Source()
source.space = openmc.stats.Point(xyz=pos_source)
phi =openmc.stats.Uniform(0.0,2*pi)
mu =openmc.stats.Uniform(0.989,1.0)
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(-1.0,0.0,0.0))
source.energy = openmc.stats.Discrete([10.0e6],[1.0])
source.particle = 'photon'
settings.source = source
settings.batches = 11
settings.inactive = 1
settings.particles = 5_000 #2_000_000
settings.run_mode = 'fixed source'
settings.photon_transport = True
settings.export_to_xml()
################################################################################
# Tally #
################################################################################
tally = openmc.Tallies()
#filter_cell = openmc.CellFilter((c15, c16,c23, c22,c24,c25, c18,c21, c27))
mesh = openmc.RegularMesh() # type: ignore
mesh.dimension = [100, 100]
xlen = x + 2*xdet
ylen = y + 2*ydet
mesh.lower_left = [-xlen/2, -xlen/2]
mesh.upper_right = [ylen/2, ylen/2]
mesh_filter = openmc.MeshFilter(mesh)

#tally1 = openmc.Tally()
tally1 = openmc.Tally(name = 'dose')
particle1 = openmc.ParticleFilter('photon')
tally1.scores = ['flux']
energy, dose = openmc.data.dose_coefficients('photon', 'RLAT')
dose_filter = openmc.EnergyFunctionFilter(energy, dose)
#tally1.filters = [filter_cell, particle1, dose_filter]
tally1.filters = [mesh_filter, particle1, dose_filter]
tally.append(tally1)
tally2 = openmc.Tally(name = 'flux')
#tally2 = openmc.Tally(
particle2 = openmc.ParticleFilter('photon')
tally2.filters = [mesh_filter, particle2]
#tally2.filters = [filter_cell, particle2]
tally2.scores = ['flux']
tally.append(tally2)

tally.export_to_xml()
openmc.run()
