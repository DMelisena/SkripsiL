import openmc # type: ignore
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import pandas as pd


x=500#harus sama dengan resolusi pada file utama
y=500
#s_rate=3.293648066139751e+17 #src/s
s_rate= 16368352439.27938
v=(2000/x)*(2000/y)*1000 #volume of room dose distribution
vcell=10.8*50*200 #cm3

# 0 degree cell tally result {{{

sp = openmc.StatePoint('./0/statepoint.100.h5')

celltally = sp.tallies[3]
celldosevalues = celltally.get_values() #pSvcm3/src;dosevolume per source
celldosestddev = celltally.std_dev 
celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

dose_psvs=celldosevalues * s_rate / vcell
usvh_dose=dose_psvs

stddev_psvs=celldosestddev*s_rate/vcell
usvh_stddev=stddev_psvs

dose1=usvh_dose
dosestddev1=usvh_stddev

# }}}

# 90 degree cell tally result {{{

sp = openmc.StatePoint('./90/statepoint.100.h5')

celltally = sp.tallies[3]
celldosevalues = celltally.get_values() #pSvcm3/src;dosevolume per source
celldosestddev = celltally.std_dev 
celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

dose_psvs=celldosevalues * s_rate / vcell
usvh_dose=dose_psvs

stddev_psvs=celldosestddev*s_rate/vcell
usvh_stddev=stddev_psvs

dose2=usvh_dose
dosestddev2=usvh_stddev

# }}}

# 180 degree cell tally result {{{

sp = openmc.StatePoint('./180/statepoint.100.h5')

celltally = sp.tallies[3]
celldosevalues = celltally.get_values() #psvcm3/src;dosevolume per source
celldosestddev = celltally.std_dev 
celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

dose_psvs=celldosevalues * s_rate / vcell
usvh_dose=dose_psvs

stddev_psvs=celldosestddev*s_rate/vcell
usvh_stddev=stddev_psvs

dose3=usvh_dose
dosestddev3=usvh_stddev

# }}}

# 270 degree cell tally result {{{

sp = openmc.StatePoint('./270/statepoint.100.h5')

celltally = sp.tallies[3]
celldosevalues = celltally.get_values() #psvcm3/src;dosevolume per source
celldosestddev = celltally.std_dev 
celldosevalues.shape = celldosevalues.shape[0]
celldosestddev.shape = celldosestddev.shape[0]

dose_psvs=celldosevalues * s_rate / vcell
usvh_dose=dose_psvs

stddev_psvs=celldosestddev*s_rate/vcell
usvh_stddev=stddev_psvs

dose4=usvh_dose
dosestddev4=usvh_stddev

# }}}

data = {'0 dose': dose1, '0 dose stddev': dosestddev1 ,'90 dose': dose2, '90 dose stddev': dosestddev2,'180 dose': dose3, '180 dose stddev': dosestddev3,'270 dose': dose4, '270 dose stddev': dosestddev4}
# create a dictionary with column names as keys and data as values

# create a dataframe from the dictionary
df = pd.DataFrame(data)
df.to_csv("cellTallyDose.csv")
