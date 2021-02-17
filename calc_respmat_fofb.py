
import numpy as np
import pickle
from pymodels import si
from apsuite.commissioning_scripts.calc_orbcorr_mat import OrbRespmat

mod = si.create_accelerator()
famdata = si.get_family_data(mod)
respmat = OrbRespmat(mod, 'SI', dim='6d')

# Change corretors indices to fast correctors:
respmat.ch_idx = np.array(famdata['FCH']['index']).ravel()
respmat.cv_idx = np.array(famdata['FCV']['index']).ravel()
mat = respmat.get_respm()


# the unit of the matrix elements are um/urad
# It is organized as folows:
# M = | Mxx Mxy |
#     | Myx Myy |
# where
# Mxx --> FCH BPMx
# Mxy --> FCV BPMx
# Myx --> FCH BPMy
# Myy --> FCV BPMy
# which means the dimension of M is (320, 160)
mat = mat[:,:-1]  # remove RF line from matrix

with open('Rmat.pickle', 'wb') as filehandle:
	pickle.dump(mat, filehandle)

