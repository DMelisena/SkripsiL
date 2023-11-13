import openmc
import matplotlib.pyplot as plt
from math import * #type: ignore

particles=10000
phantomRotation=270

air=openmc.Material(name='Air')
air.set_density('g/cm3',0.001205)
air.add_nuclide('N14',0.7)
air.add_nuclide('O16',0.3)
#air.add_s_alpha_beta('c_H_in_Air')
air.add_element('C',0.002)
air.add_element('Fe',0.001)
air.add_element('Si',0.001)
air.add_element('Mn',0.001)

water=openmc.Material(name='Water')
water.set_density('g/cm3',1.0)
water.add_nuclide('H1',2.0)
water.add_nuclide('O16',1.0)
water.add_s_alpha_beta('c_H_in_H2O')

materials=openmc.Materials([air,water])
materials.export_to_xml()

####################################################################################
#Water Phantom 10x10x5
pr=phantomRotation#phantom rotation
detaxu=openmc.YPlane(5,boundary_type='transmission')
detaxs=openmc.YPlane(-5,boundary_type='transmission')
detaxza=openmc.XPlane(2.5,boundary_type='transmission')
detaxzb=openmc.XPlane(-2.5,boundary_type='transmission')
detaxt=openmc.ZPlane(-128+5,boundary_type='transmission')
detaxb=openmc.ZPlane(-128-5,boundary_type='transmission')

####################################################################################

detax= -detaxu & +detaxs & -detaxt & +detaxb & -detaxza & +detaxzb #Air pada water phantom
detaxcell=openmc.Cell(fill=water,region=detax)

#Kotak Udara Pembatas
ymax=openmc.YPlane(300,boundary_type='vacuum')
ymin=openmc.YPlane(-300,boundary_type='vacuum')
xmax=openmc.XPlane(300,boundary_type='vacuum')
xmin=openmc.XPlane(-300,boundary_type='vacuum')
zmaxx=openmc.ZPlane(300,boundary_type='vacuum')
zmin=openmc.ZPlane(-300,boundary_type='vacuum')

#Udara pada sel
void1= +zmin & -zmaxx \
    & +ymin & -ymax & +xmin & -xmax\
    & ~detax


void1cell = openmc.Cell(fill=air, region=void1)

detaxz0=detaxzb
detaxz50=detaxza
varnamearr=[detaxz0]
geoarr=[]
geovalarr=[]
cellarr=[]
cellvalarr=[]

for i in range(1,51):
    varname=f"detaxz{i}"
    varval=f"openmc.XPlane(-2.5+{i*0.1},boundary_type='transmission')"
    exec(f"{varname}={varval}")

    geoname=f"detax{i}"
    geoval=f"-detaxu & +detaxs & -detaxt & +detaxb & -detaxz{i-1} & +detaxz{1}"
    exec(f"{geoname}={geoval}")

    cellname=f"detaxcell{i}"
    cellval=f"openmc.Cell(fill=water,region={geoname})"
    exec(f"{cellname}= {cellval}")

"""
suniv='univ=openmc.Universe(cells=[void1cell\'

for i in range(1,51):
    suniv+=f",detaxcell{i}"

suniv+='])'

exec(suniv)
print(suniv)
"""

univ=openmc.Universe(cells=[void1cell,detaxcell1,detaxcell2,detaxcell3,detaxcell4,detaxcell5,detaxcell6,detaxcell7,detaxcell8,detaxcell9,detaxcell10,detaxcell11,detaxcell12,detaxcell13,detaxcell14,detaxcell15,detaxcell16,detaxcell17,detaxcell18,detaxcell19,detaxcell20,detaxcell21,detaxcell22,detaxcell23,detaxcell24,detaxcell25,detaxcell26,detaxcell27,detaxcell28,detaxcell29,detaxcell30,detaxcell31,detaxcell32,detaxcell33,detaxcell34,detaxcell35,detaxcell36,detaxcell37,detaxcell38,detaxcell39,detaxcell40,detaxcell41,detaxcell42,detaxcell43,detaxcell44,detaxcell45,detaxcell46,detaxcell47,detaxcell48,detaxcell49,detaxcell50])

geometry=openmc.Geometry(univ)
geometry.export_to_xml()

colors= {}
colors[air]='green'
colors[water]='blue'

###############################################
#                Rotation
###############################################
def sposi(d,rot):
    u= (-sin(radians(rot)))
    v= 0
    w= (-cos(radians(rot))) #source position
    uvw = (u,v,w)
    xyz = ( d*(sin(radians(rot))) ), 0, -128+ ( d*(cos(radians(rot)) ))
    return uvw, xyz
    #asumsi tinggi pasien 75cm

###############################################
#        Input (linac distance,rotation)      #
linacuvw, linacxyz=sposi(100,270)
###############################################
print(linacuvw, linacxyz)


###############################################
#            Penampil Geometri                #
###############################################
univ.plot(width=(400,400),basis='xy',color_by='material',colors=colors)
plt.savefig('xyRSHS.png')
univ.plot(width=(400,400),basis='xz',color_by='material',colors=colors)
plt.savefig('xzRSHS.png')
univ.plot(width=(400,400),basis='yz',color_by='material',colors=colors)
plt.savefig('yzRSHS.png')
plt.show()


###############################################
#                 Setting                     #
###############################################
settings=openmc.Settings()
source  =openmc.Source()
#source.space=openmc.stats.Points(xyz=)
source.space=openmc.stats.Point(xyz=linacxyz) # type: ignore
#phi2=openmc.stats.Isotropic() #isotropic ato uniform?
#phi1=openmc.stats.Monodirectional((0,0,1))
phi =openmc.stats.Uniform(0.0,2*pi) # type: ignore
#mu= distribution of the cosine of the polar angle
#phi=distribution of the azimuthal angle in radians

#tan theta = r/SAD=20/1000; theta = atan(20/100)=0.19739555984988; cos theta=0.98058
mu=openmc.stats.Uniform(0.98058,1) # type: ignore

source.angle = openmc.stats.PolarAzimuthal(mu,phi,reference_uvw=linacuvw) # type: ignore
source.energy = openmc.stats.Discrete([10e6],[1]) #10MeV # type: ignore
source.particle = 'photon'
#source.particle = 'neutron'
settings.source = source
settings.batches= 5
settings.particles = particles
#Asumsi 36e8 partikel pada mula, pada 600MU=600cGy/m=6Gy/m=6Sv/m=6e6uSv/m=360e6uSv/h
#maka, apabila dosis yang diekspektasi pada dinding sekitar 0.1uSv/h. Maka perlu 36e8 agar dapat muncul
#36e8; 3.600.000.000
settings.run_mode = 'fixed source'
settings.photon_transport = True
settings.export_to_xml()

###############################################
#                 Tallies                     #
###############################################
tally = openmc.Tallies()

#Tally Dose Distribution
mesh = openmc.RegularMesh() # type: ignore
mesh.dimension = [500, 500]
xlen = 2000;ylen = 2000
mesh.lower_left = [-xlen/2, -xlen/2]
mesh.upper_right = [ylen/2, ylen/2]
mesh_filter = openmc.MeshFilter(mesh)

tally1 = openmc.Tally(name = 'Room Dose Distribution')
tally1.scores = ['flux']
particle1 = openmc.ParticleFilter('photon')

energy, dose = openmc.data.dose_coefficients('photon', 'RLAT') #Data konve # type: ignore
dose_filter = openmc.EnergyFunctionFilter(energy, dose) #konvert partikel energi tertentu ke deskripsi icrp116 partikelcm/src->pSvcm3/srcwphantom_cell,particle3,dose_filter

tally1.filters=[mesh_filter,particle1,dose_filter]
tally.append(tally1)

#Tally Detektor
particle2 = openmc.ParticleFilter('photon')
#Tally Water Phantom
"""
s="wphantom_cell=openmc.CellFilter(("
for i in range(1,51):
    s+=f"detaxcell{i}"
    if i<50:
        s+=','
s+="))"
exec(s)
print(s)
"""
wphantom_cell=openmc.CellFilter((detaxcell1,detaxcell2,detaxcell3,detaxcell4,detaxcell5,detaxcell6,detaxcell7,detaxcell8,detaxcell9,detaxcell10,detaxcell11,detaxcell12,detaxcell13,detaxcell14,detaxcell15,detaxcell16,detaxcell17,detaxcell18,detaxcell19,detaxcell20,detaxcell21,detaxcell22,detaxcell23,detaxcell24,detaxcell25,detaxcell26,detaxcell27,detaxcell28,detaxcell29,detaxcell30,detaxcell31,detaxcell32,detaxcell33,detaxcell34,detaxcell35,detaxcell36,detaxcell37,detaxcell38,detaxcell39,detaxcell40,detaxcell41,detaxcell42,detaxcell43,detaxcell44,detaxcell45,detaxcell46,detaxcell47,detaxcell48,detaxcell49,detaxcell50))
tally3=openmc.Tally(name='wphantom')
#tally3.filters=[wphantom_cell,particle3]
#Energy_filter = openmc.EnergyFilter([1e-3, 1e13])
tally3.filters=[wphantom_cell,particle2,dose_filter]  #output pSvcm3/src 
tally3.scores = ['flux']
tally.append(tally3)

tally.export_to_xml()
openmc.run()