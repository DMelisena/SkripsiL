import openmc

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


for i in range(1,50):  # Loop from 3 to 4 (inclusive)
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

for i in range (3,39):
    print(f"{varnamearr[i]} = {(varvalarr[i])}")
    print(f"{geoarr[i]} = {(geovalarr[i])}")