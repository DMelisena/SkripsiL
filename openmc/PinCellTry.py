import openmc

mat = openmc.Material()
print(mat)

#Uranium Dioksida, Seperti H2O tapi pakai U bukannya H.
uo2 = openmc.Material(1,"uo2") 
uo2.add_nuclide('U235',0.03)
uo2.add_nuclide('U238',0.97)
uo2.add_nuclide('O16',2)
uo2.set_density('g/cm3',10)
print("uo2 =",uo2)

#Pure Zirconium
zirconium =  openmc.Material(2,"Zirconium")
zirconium.add_nuclide('Zr',1.0)
zirconium.set_density('g/cm3',6.6)
print("Zirconium =",zirconium)

#Just Water, H2O
water=openmc.Material(3,"H2O")
water.add_nuclide('H1',2)
water.add_nuclide('O16',1)
water.set_density('g/cm3',1)

water.add_s_alpha_beta('c_H_in_H20')

mats=openmc.Materials([uo2,zirconium,water])
#It's an array that could be used as this
#mats=openmc.Materials()
#mats.append(uo2)
#mats +=[zirconium,water]
#isinstance(mats,list)
mats.export_to_xml()

######################################
########### Material Mix #############
#mixture of 0.97 uo2 and 0.03 puo2

uo2_3 = openmc.Material()
uo2_3.add_element('U',1,enrichment=3)
uo2_3.add_element('O',2)
uo2_3.set_density('g/cm3',10) #g/cc = g/cm3

#instead of u or H, Here we use Pu
puo2=openmc.Material()
puo2.add_nuclide('Pu239',0.94)
puo2.add_nuclide('Pu240',0.06)
puo2.add_nuclide('O16',2)
puo2.set_density('g/cm3',11.5)

mox=openmc.Material.mix_materials([uo2,puo2],[0.97,0.03],'wo')
######################################

"""
zircaloy =  openmc.Material(name='Zircaloy')
zircaloy.set_density('g/cm3',6.55)
zircaloy.add_nuclide('Zr90',7.2758e-3)
"""

print(uo2)
"""
      ,"\n",zircaloy,"\n",zirconium
      
      )"""