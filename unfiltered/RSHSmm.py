import openmc
import matplotlib.pyplot as plt
from math import *

air=openmc.Material(name='Air')
air.set_density('g/cm3',0.001205)
air.add_nuclide('N14',0.7)
air.add_nuclide('O16',0.3)
#air.add_s_alpha_beta('c_H_in_Air')
air.add_element('C',0.002)
air.add_element('Fe',0.001)
air.add_element('Si',0.001)
air.add_element('Mn',0.001)

air2=openmc.Material(name='Air')
air2.set_density('g/cm3',0.001205)
air2.add_nuclide('N14',0.7)
air2.add_nuclide('O16',0.3)
#air.add_s_alpha_beta('c_H_in_Air')
air2.add_element('C',0.002)
air2.add_element('Fe',0.001)
air2.add_element('Si',0.001)
air2.add_element('Mn',0.001)





soft=openmc.Material(name='Soft Tissue')
soft.set_density('g/cm3',1.0)
soft.add_element('H', 10.4472, percent_type='ao')#1
soft.add_element('C', 23.219, percent_type='ao')#6
soft.add_element('N', 2.388, percent_type='ao')#7
soft.add_element('O', 63.0238, percent_type='ao')#8
soft.add_element('Na', 0.113, percent_type='ao')#11
soft.add_element('Mg', 0.013, percent_type='ao')#12
soft.add_element('S',  0.199, percent_type='ao')#16
soft.add_element('Cl', 0.134, percent_type='ao')#17
soft.add_element('K',  0.199, percent_type='ao')#19
soft.add_element('Ca', 0.023, percent_type='ao')#20
#https://physics.nist.gov/cgi-bin/Star/compos.pl?matno=261

bpe=openmc.Material(name='Borate Polyethylene')
bpe.set_density('g/cm3',1.0)
bpe.add_element('H', 0.111, percent_type='ao')#1
bpe.add_element('C', 0.856, percent_type='ao')#6
bpe.add_element('B', 0.143, percent_type='ao')#5
bpe.add_element('O', 0.889, percent_type='ao')#8

lead=openmc.Material(name='Lead')
lead.set_density('g/cm3',11.35)
lead.add_element('Pb',1.0)

concrete=openmc.Material(name='Concrete')
concrete.set_density('g/cm3',2.3) #Harus disesuaikan dengan uji beton
concrete.add_element('H', 0.01, percent_type='ao')#1
concrete.add_element('C', 0.01, percent_type='ao')#6
concrete.add_element('O', 0.52, percent_type='ao')#8
concrete.add_element('Na', 0.01, percent_type='ao')#11
concrete.add_element('Mg', 0.01, percent_type='ao')#12
concrete.add_element('Al', 0.01, percent_type='ao')#13
concrete.add_element('Si', 0.25, percent_type='ao')#14
concrete.add_element('S',  0.01, percent_type='ao')#16
concrete.add_element('K',  0.01, percent_type='ao')#19
concrete.add_element('Ca', 0.01, percent_type='ao')#20
concrete.add_element('Fe', 0.01, percent_type='ao')#26
concrete.add_element('Pb', 0.01, percent_type='ao')#82

materials=openmc.Materials([air,air2,soft,bpe,lead,concrete])
materials.export_to_xml()

################################################

############# Geometry ########################
#x
t1=openmc.XPlane(6320,boundary_type='transmission')
t2=openmc.XPlane(6320-765,boundary_type='transmission')
t3=openmc.XPlane(6320-765-1550,boundary_type='transmission')
t4=openmc.XPlane(6320-765-1550-765,boundary_type='transmission')
t5=openmc.XPlane(6320-765-1550-765,boundary_type='transmission')

b1=openmc.XPlane(-6320,boundary_type='transmission')
b2=openmc.XPlane(-6320+765,boundary_type='transmission')
b3=openmc.XPlane(-6320+765+1550,boundary_type='transmission')
b4=openmc.XPlane(-6320+765+1550+765,boundary_type='transmission')
b5=openmc.XPlane(-6320+765+2505,boundary_type='transmission')

#y #Di berkas 125, tapi ga make sense jadi diubah ke 1200 biar masuk angkanya
u1=openmc.YPlane(1900+2500+1200+1850+810,boundary_type='transmission')
u2=openmc.YPlane(1900+2500+1200+1850,boundary_type='transmission')
u3=openmc.YPlane(1900+2500+1200,boundary_type='transmission')
u4=openmc.YPlane(1900+2500,boundary_type='transmission')
u5=openmc.YPlane(1900,boundary_type='transmission')

s1=openmc.YPlane(-1900-1850-1280,boundary_type='transmission')
s2=openmc.YPlane(-1900-1850,boundary_type='transmission')
s3=openmc.YPlane(-1900,boundary_type='transmission')

#z total tinggi = 6000, lantai 1 setebal 480

zm1=openmc.ZPlane(-3000,boundary_type='vacuum')
zmax=openmc.ZPlane(3000,boundary_type='vacuum')
z3=openmc.ZPlane(-3000+480+1240+1860+1170+1250,boundary_type='transmission')#1250 ATO 2500???
z2=openmc.ZPlane(-3000+480+1240+1860+1170,boundary_type='transmission')
z1=openmc.ZPlane(-3000+480+1240+1860,boundary_type='transmission')
z0=openmc.ZPlane(-3000+480,boundary_type='transmission')

#pintu utara, pintu barat, pintu selatan geometri nya
pu=openmc.YPlane(1900+2500+1200+1850+400,boundary_type='transmission') 
#                                    ^^^ asumsi pintu lebih lebar 40cm dibandingkan lubang pintunya
pb0=b5
pb1=openmc.XPlane(-6320+765+2505-158,boundary_type='transmission') #Angkanya ini masih ngarang karena gatau tebal pintu, ada kemungkinan formulanya di RHSPintu.py salah
pb2=openmc.XPlane(-6320+765+2505-158-1020,boundary_type='transmission')
pb3=openmc.XPlane(-6320+765+2505-158-1020-158,boundary_type='transmission')
ps=u3


###############################################
dt1 = -t1 & +t2 & +s3 & -u5 & +z0 & -z2  
dt2 = -t2 & +t3 & +s1 & -u1 & +z0 & -z2
dt3 = -t3 & +t4 & +s3 & -u5 & +z0 & -z2

db1 = +b1 & -b2 & +s3 & -u5 & +z0 & -z2
db2 = +b2 & -b3 & +s1 & -u3 & +z0 & -z2
db3 = +b3 & -b4 & +s3 & -u5 & +z0 & -z2

du1 = +b5 & -t3 & -u1 & +u2 & +z0 & -z2
du2 = +b3 & -t5 & -u3 & +u4 & +z0 & -z2

ds1 = +b3 & -t3 & +s1 & -s2 & +z0 & -z2

datas= +b1 & -t1 & +s1 & -u1 & +z2 & -z3 #celing
datte= +b4 & -t4 & -u5 & +s3 & +z1 & -z2 #linac's middle wall
dbaw = +b1 & -t1 & +s1 & -u1 & +zm1 & -z0 #flooring
###############################################
#pintu
ppb = -pu & +ps & -pb0 & +pb1 & +z0 & -z2#pintu Pb
pbpe= -pu & +ps & -pb1 & +pb2 & +z0 & -z2#pintu BPE
ppb2= -pu & +ps & -pb2 & +pb3 & +z0 & -z2#pintu Pb

#Udara
#void1= -dt1 & +dt2 & -dt3 & +db1 & -db2 & +db3 & -du1 & +du2 & -ds1 & +ppb & -pbpe & +ppb2 & +datas & -dbaw 
#void1cell=openmc.Cell(fill=air,region=void1)

#Cell =

dt1cell=openmc.Cell(fill=concrete,region=dt1)
dt2cell=openmc.Cell(fill=concrete,region=dt2)
dt3cell=openmc.Cell(fill=concrete,region=dt3)
db1cell=openmc.Cell(fill=concrete,region=db1)
db2cell=openmc.Cell(fill=concrete,region=db2)
db3cell=openmc.Cell(fill=concrete,region=db3)
du1cell=openmc.Cell(fill=concrete,region=du1)
du2cell=openmc.Cell(fill=concrete,region=du2)
ds1cell=openmc.Cell(fill=concrete,region=ds1)

ppbcell=openmc.Cell(fill=lead,region=ppb)
pbpecell=openmc.Cell(fill=bpe,region=pbpe)
ppb2cell=openmc.Cell(fill=lead,region=ppb2)

datascell=openmc.Cell(fill=concrete,region=datas)
dattecell=openmc.Cell(fill=concrete,region=datte)
dbawcell=openmc.Cell(fill=concrete,region=dbaw)


###############################################
#                Detektor/Tally               #
#                          Utara              #
deu1=openmc.YPlane (1900+2500+1200+1850+810+300,boundary_type='transmission')
deu1t=openmc.YPlane(1900+2500+1200+1850+810+300+108,boundary_type='transmission') #+tebal detektor
deu2=openmc.YPlane (1900+2500+1200+1850+810+1000,boundary_type='transmission')
deu2t=openmc.YPlane(1900+2500+1200+1850+810+1000+108,boundary_type='transmission')
deu3=openmc.YPlane (1900+2500+1200+1850+810+2000,boundary_type='transmission')
deu3t=openmc.YPlane(1900+2500+1200+1850+810+2000+108,boundary_type='transmission')

deuz0=openmc.ZPlane(-3000+480+1000,boundary_type='transmission')#Tinggi detektor, default untuk semua detektor kecuali atas
deuz1=openmc.ZPlane(-3000+480+1000+2000,boundary_type='transmission')

deubb=openmc.XPlane(-6320+765+2505+1000,boundary_type='transmission') #Koordinat x nya masih ngasal
deubt=openmc.XPlane(-6320+765+2505+1000+500,boundary_type='transmission')

deucb=openmc.XPlane(2500,boundary_type='transmission') #koordinat x nya masih ngasal
deuct=openmc.XPlane(2500+500,boundary_type='transmission')

detb1= +deu1 & -deu1t & +deuz0 & -deuz1 & +deubb & -deubt #detektor utara barat, x nya ngasal
detb2= +deu2 & -deu2t & +deuz0 & -deuz1 & +deubb & -deubt 
detb3= +deu3 & -deu3t & +deuz0 & -deuz1 & +deubb & -deubt
dett1= +deu1 & -deu1t & +deuz0 & -deuz1 & +deucb & -deuct #detektor utara timur, x nya ngasal
dett2= +deu2 & -deu2t & +deuz0 & -deuz1 & +deucb & -deuct
dett3= +deu3 & -deu3t & +deuz0 & -deuz1 & +deucb & -deuct

#Detektor
detub1cell=openmc.Cell(fill=air2,region=detb1) #sel detektor barat 1
detub2cell=openmc.Cell(fill=air2,region=detb2) 
detub3cell=openmc.Cell(fill=air2,region=detb3) 
detut1cell=openmc.Cell(fill=air2,region=dett1)
detut2cell=openmc.Cell(fill=air2,region=dett2)
detut3cell=openmc.Cell(fill=air2,region=dett3)


#                          Timur              #
det1=openmc.XPlane(6320+300,boundary_type='transmission')
det1t=openmc.XPlane(6320+300+108,boundary_type='transmission')
det2=openmc.XPlane(6320+1000,boundary_type='transmission')
det2t=openmc.XPlane(6320+1000+108,boundary_type='transmission')
det3=openmc.XPlane(6320+2000,boundary_type='transmission')
det3t=openmc.XPlane(6320+2000+108,boundary_type='transmission')

detu=openmc.YPlane(250,boundary_type='transmission')
dets=openmc.YPlane(-250,boundary_type='transmission')

dett1= +det1 & -det1t & +deuz0 & -deuz1 & -detu & +dets
dett2= +det2 & -det2t & +deuz0 & -deuz1 & -detu & +dets
dett3= +det3 & -det3t & +deuz0 & -deuz1 & -detu & +dets

dett1cell=openmc.Cell(fill=air2,region=dett1)
dett2cell=openmc.Cell(fill=air2,region=dett2)
dett3cell=openmc.Cell(fill=air2,region=dett3)

#                          Barat              #

deb1=openmc.XPlane(-6320+765+2505-158-1020-158-300,boundary_type='transmission')
deb1t=openmc.XPlane(-6320+765+2505-158-1020-158-300-108,boundary_type='transmission')
deb2=openmc.XPlane(-6320+765+2505-158-1020-158-1000,boundary_type='transmission')
deb2t=openmc.XPlane(-6320+765+2505-158-1020-158-1000-108,boundary_type='transmission')
deb3=openmc.XPlane(-6320+765+2505-158-1020-158-2000,boundary_type='transmission')
deb3t=openmc.XPlane(-6320+765+2505-158-1020-158-2000-108,boundary_type='transmission')

debu=openmc.YPlane(1900+2500+1200+1850-675,boundary_type='transmission') 
debs=openmc.YPlane(1900+2500+1200+1850-675-500,boundary_type='transmission') 

detb1= -deb1 & +deb1t & +deuz0 & -deuz1 & -debu & +debs
detb2= -deb2 & +deb2t & +deuz0 & -deuz1 & -debu & +debs
detb3= -deb3 & +deb3t & +deuz0 & -deuz1 & -debu & +debs

detb1cell=openmc.Cell(fill=air2,region=detb1)
detb2cell=openmc.Cell(fill=air2,region=detb2)
detb3cell=openmc.Cell(fill=air2,region=detb3)

#                          Atas               #
deau=openmc.XPlane(250,boundary_type='transmission')
deas=openmc.XPlane(-250,boundary_type='transmission')

deat=openmc.YPlane(250,boundary_type='transmission')
deab=openmc.YPlane(-250,boundary_type='transmission')

dea1=openmc.ZPlane(3000+300,boundary_type='transmission') #1250 ATO 2500???
dea1t=openmc.ZPlane(3000+300+108,boundary_type='transmission') #1250 ATO 2500???
dea2=openmc.ZPlane(3000+1000,boundary_type='transmission')
dea2t=openmc.ZPlane(3000+1000+108,boundary_type='transmission')
dea3=openmc.ZPlane(3000+2000,boundary_type='transmission') 
dea3t=openmc.ZPlane(3000+2000+108,boundary_type='transmission')

deta1= +dea1 & -dea1t & -deau & +deas & +deab & -deat
deta2= +dea2 & -dea2t & -deau & +deas & +deab & -deat
deta3= +dea3 & -dea3t & -deau & +deas & +deab & -deat

deta1cell=openmc.Cell(fill=air2,region=deta1)
deta2cell=openmc.Cell(fill=air2,region=deta2)
deta3cell=openmc.Cell(fill=air2,region=deta3)
#void1cell = openmc.Cell(fill=air, region= (-datascell.region) & (-dt1cell.region) & (-dt2cell.region) & (-dt3cell.region) & (-db1cell.region) & (-db2cell.region) & (-db3cell.region) & (-du1cell.region) & (-du2cell.region) & (-ds1cell.region))
void1= +z0 & -zmax \
    & ~dt1cell.region & ~dt2cell.region & ~dt3cell.region \
        & ~db1cell.region & ~db2cell.region & ~db3cell.region \
            & ~du1cell.region & ~du2cell.region & ~ds1cell.region

void1cell = openmc.Cell(fill=air, region=void1)

univ=openmc.Universe(cells=[dt1cell,dt2cell,dt3cell,
                            db1cell,db2cell,db3cell,
                            du1cell,du2cell,ds1cell,
                            ppbcell,pbpecell,ppb2cell,
                            datascell,dbawcell,dattecell,
                            void1cell,
                            detub1cell,detub2cell,detub3cell,
                            detut1cell,detut2cell,detut3cell,
                            dett1cell,dett2cell,dett3cell,
                            deta1cell,deta2cell,deta3cell])
geometry=openmc.Geometry(univ)

geometry.export_to_xml()

colors= {}
colors[lead]='black'
colors[bpe]='lightblue'
colors[concrete]='grey'
colors[air]='white'
colors[air2]='blue'
###############################################
#                Rotation
###############################################
def sposi(d,rot):  #source position
    return ( d*(sin(radians(rot))) ), \
     0, \
     -1280+( d*(cos(radians(rot)) ) \
    )#asumsi tinggi pasien 75cm

###############################################
#        Input (linac distance,rotation)      #
linacpos=sposi(1000,270)
###############################################
print(linacpos)


###############################################
#            Penampil Geometri                #
###############################################
univ.plot(width=(18000,21000),basis='xy',color_by='material',colors=colors)
plt.savefig('xyRSHS.png')
univ.plot(width=(14000,10400),basis='xz',color_by='material',colors=colors)
plt.savefig('xzRSHS.png')
univ.plot(width=(18000,10400),basis='yz',color_by='material',colors=colors)
plt.savefig('yzRSHS.png')
plt.show()


###############################################
#                 Setting                     #
###############################################
settings=openmc.Settings()
source  =openmc.Source()
#source.space=openmc.stats.Points(xyz=)
source.space=openmc.stats.Point(xyz=linacpos)
#phi2=openmc.stats.Isotropic() #isotropic ato uniform?
#phi1=openmc.stats.Monodirectional((0,0,1))
phi =openmc.stats.Uniform(0.0,2*pi)
mu=openmc.stats.Uniform(0.989,1)

#source.particle = 'neutron'
source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=(-1,0,0))
#mu= distribution of the cosine of the polar angle
#phi=distribution of the azimuthal angle in radians

source.energy = openmc.stats.Discrete([10e6],[1]) #10MeV
#Sepertinya Resource
source.particle = 'photon'
settings.source = source
settings.batches= 11
settings.inactive=1
settings.particles = 1000
settings.run_mode = 'fixed source'
settings.photon_transport = True
settings.export_to_xml()

###############################################
#                 Tallies                     #
###############################################


################################################################################
# Tally #
################################################################################
tally = openmc.Tallies()
#filter_cell = openmc.CellFilter((c15, c16,c23, c22,c24,c25, c18,c21, c27))
mesh = openmc.RegularMesh() # type: ignore
mesh.dimension = [100, 100]
xdet=50
ydet=50

xlen = 14000
ylen = 14000
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
