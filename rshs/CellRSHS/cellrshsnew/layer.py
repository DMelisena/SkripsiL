import openmc
#Perlu membuat geometri dan cell secara otomatis
# 1. Declare plane geometri
#Harapannya agar terbuat detaxz1=-2.4, detaxz2=-2.3, dst
# 2. Declare geometri volume cell
#detax1-45
# 3. Declare cell (Fill)
# 4. Masukin ke Universe
# 5. Masukin ke Tally

detaxu=openmc.YPlane(5,boundary_type='transmission')
detaxs=openmc.YPlane(-5,boundary_type='transmission')
detaxza=openmc.XPlane(2.5,boundary_type='transmission')
detaxzb=openmc.XPlane(-2.5,boundary_type='transmission')
detaxt=openmc.ZPlane(-128+5,boundary_type='transmission')
detaxb=openmc.ZPlane(-128-5,boundary_type='transmission')


water=openmc.Material(name='Water')
water.set_density('g/cm3',1.0)
water.add_nuclide('H1',2.0)
water.add_nuclide('O16',1.0)
water.add_s_alpha_beta('c_H_in_H2O')

detaxz0=detaxzb

varnamearr=[detaxz0]
varvalarr=[]
geoarr=[]
geovalarr=[]
cellarr=[]
cellvalarr=[]

for i in range(1,51):  #
    
    #X Plane Maker
    varname = f"detaxz{i}"  # Generate variable name
    varval = f"openmc.XPlane(-2.5+{i*0.1},boundary_type='transmission')"  # Define the calculation expression 
    varnamearr.append(varname)# type: ignore
    varvalarr.append(varval)
    # Create the variable dynamically using exec()
    exec(f"{varname} = {varval}")

    #Cell volume geometry maker
    geoname=f"detax{i}"
    geoval =f"-detaxu & +detaxs & -detaxt & +detaxb & -detaxz{i-1} & +detaxz{i}" 
    geoarr.append(geoname)
    geovalarr.append(geoval)
    exec(f"{geoname} = {geoval}")

    cellname=f"detaxcell{i}"
    cellval=f"openmc.Cell(fill=water,region={geoname})"
    cellarr.append(cellname)
    cellvalarr.append(cellval)
    exec(f"{cellname} = {cellval}")

for i in range (0,50):
    print(f"test :{varnamearr[i]} = {(varvalarr[i])}")
    print(f"test :{geoarr[i]} = {(geovalarr[i])}")
    print(f"test :{cellarr[i]} = {(cellvalarr[i])}")
#univ=openmc.universe(cells=[])
#univ.cells.append({detaxcell{i}})
for i in range (1,51):
    #exec(f"univ.cells.append(detaxcell{i})")
    print(f"univ.cells.append(detaxcell{i})")


#Tally Water Phantom
s="wphantom_cell=openmc.CellFilter("
for i in range (1,51):
    s+=f"detaxcell{i},"
s+=")"
#exec(s)
print(s)
tally3=openmc.Tally(name='wphantom')
particle3= openmc.ParticleFilter('photon')
#tally3.filters=[wphantom_cell,particle3]
#Energy_filter = openmc.EnergyFilter([1e-3, 1e13])
tally3.filters=[wphantom_cell,particle3,dose_filter]  #output pSvcm3/src 
tally3.scores = ['flux']
tally.append(tally3)
tally.export_to_xml()
openmc.run()