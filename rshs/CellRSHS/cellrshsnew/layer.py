import openmc
#Perlu membuat geometri dan cell secara otomatis
# 1. Declare plane geometri
#Harapannya agar terbuat detaxz1=-2.4, detaxz2=-2.3, dst
# 2. Declare geometri volume cell
#detax1-45
# 3. Declare cell
# 4. Masukin ke Universe
# 5. Masukin ke Tally

detaxu=openmc.YPlane(5,boundary_type='transmission')
detaxs=openmc.YPlane(-5,boundary_type='transmission')
detaxza=openmc.XPlane(2.5,boundary_type='transmission')
detaxzb=openmc.XPlane(-2.5,boundary_type='transmission')
detaxt=openmc.ZPlane(-128+5,boundary_type='transmission')
detaxb=openmc.ZPlane(-128-5,boundary_type='transmission')

detaxz0=detaxzb

varnamearr=[detaxz0]
varvalarr=[]
geoarr=[]
geovalarr=[]


for i in range(1,51):  # Loop from 1 to 50 (inclusive)
    varname = f"detaxz{i}"  # Generate variable name
    varval = f"openmc.XPlane(-2.5+{i*0.1},boundary_type='transmission')"  # Define the calculation expression 
    varnamearr.append(varname)
    varvalarr.append(varval)
    # Create the variable dynamically using exec()
    exec(f"{varname} = {varval}")

    geoname=f"detax{i}"
    geoval =f"-detaxu & +detaxs & -detaxt & +detaxb & -detaxz{i-1} & +detaxz{i}" 
    geoarr.append(geoname)
    geovalarr.append(geoval)
    exec(f"{geoname} = {geoval}")


for i in range (0,50):
    print(f"test :{varnamearr[i]} = {(varvalarr[i])}")
    print(f"test :{geoarr[i]} = {(geovalarr[i])}")