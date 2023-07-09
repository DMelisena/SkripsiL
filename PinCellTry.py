import openmc
uo2 = openmc.Material(1,"uo2")
print(uo2)

mat = openmc.Material()
print(mat)

uo2.add_nuclide('U235',0.03)
uo2.add_nuclide('U238',0.97)
uo2.add_nuclide('O16',2)

print(uo2)