import numpy as np
import os
import time, sys
from vt_rrfc import *
import pdb
import glob


fc  = 6e9
fc2 = 2e9

pixelSize = 10 # the size of the randomized pixel in mils. Typically contrained by a PCB manufacturer.

pathName = '/home/local/millipede/hy7593/predictedData/0905_solutions/pixels' # pathname of folder to store generated pixel maps 

pixelfile_list = glob.glob(pathName+'/*.csv', recursive=True)



#mapName = pathName + 'pixelSize=' + str(pixelSize) + '_randomGenerated_sol_' + str(x) + '.csv'

pdb.set_trace()
mapName = '/home/local/millipede/hy7593/0915_solutions/pixels/09-15-18-20-27_port_17_1__10_20_sol_0.csv'
    #pdb.set_trace()
gds_file = '/home/local/millipede/hy7593/0915_solutions/pixels/09-15-18-20-27_port_17_1__10_20_sol_0.gds'
rrfc1 = rfc(pixelSize=pixelSize,outF=mapName,unit=25.4e-6, corner='overlap', layoutRes=100, scale=1, sim=0,view=1,write=0,gdsfile=gds_file)
    

#rrfc1 = rfc(pixelSize=pixelSize,outF=mapName,unit=25.4e-6,sim=0,view=0,write=0)
#os.chdir(pathName)

recreateGDS_file(rrfc1)


