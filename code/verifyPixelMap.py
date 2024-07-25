import numpy as np
import os
import time, sys
from vt_rrfc import *
import pdb
import glob

## This script will auto generate the gds files based on the pixel maps adn then run em simulation in ADS automatically. To make the script work properly,
## The pixel map folder should only contain pixel map file. PixelpathName is the loacation of the pixel map folder.


PixelpathName = '/home/local/millipede/hy7593/Pixels_verification' # pathname of folder to store the generated pixel maps 

pixelfile_list = glob.glob(PixelpathName+'/*.csv', recursive=True)

# The number of ports for the generated pixelmap for verification is 2.
ports=2
sim=1
libName = 'em_sim_automation'
pathName = '/home/local/millipede/hy7593/pixelatedRF_verification/' # Base path for file creation
cell = 'RANDOM'

y_size=20
x_size=20  # pixel size, useful when dertermining which side the port locate.

for name in pixelfile_list:
    port1_pos=[]
    port2_pos=[]
    filePath=name
    #pdb.set_trace()

    fileName=filePath.split('/')[-1]
    #pdb.set_trace()
    #The port position is contained in the file name and it's denoted in the way to reflect the portposition in the pixel map. So the indice starts from 1.
    #For example, the column 1st, row 15 will be expressed as [1,15] instead of [0,14]
    port1_pos.append(int(fileName.split('_')[2]))
    port1_pos.append(int(fileName.split('_')[3]))

    port2_pos.append(int(fileName.split('_')[5]))
    port2_pos.append(int(fileName.split('_')[6]))
    #pdb.set_trace()
    portPos_pixel=[port1_pos[0],port1_pos[1],port2_pos[0],port2_pos[1]]

    if port1_pos[0] ==1:  ## port on the west side
        port1_pos[0]=port1_pos[0]-1
        port1_pos[1]=port1_pos[1]-0.5
        
    if port1_pos[0]==x_size: ## port on the east side
        port1_pos[0]=port1_pos[0]
        port1_pos[1]=port1_pos[1]-0.5

    if port1_pos[1]==1: ## port on the south side
        port1_pos[0]=port1_pos[0]-0.5
        port1_pos[1]=port1_pos[1]-1
    
    if port1_pos[1]==y_size: ## port on the north side
        port1_pos[0]=port1_pos[0]-0.5
        port1_pos[1]=port1_pos[1]

    if port2_pos[0] ==1:  ## port on the west side
        port2_pos[0]=port2_pos[0]-1
        port2_pos[1]=port2_pos[1]-0.5
        
    if port2_pos[0]==x_size: ## port on the east side
        port2_pos[0]=port2_pos[0]
        port2_pos[1]=port2_pos[1]-0.5

    if port2_pos[1]==1: ## port on the south side
        port2_pos[0]=port2_pos[0]-0.5
        port2_pos[1]=port2_pos[1]-1
    
    if port2_pos[1]==y_size: ## port on the north side
        port2_pos[0]=port2_pos[0]-0.5
        port2_pos[1]=port2_pos[1]
    


    pixelSize=10
    portPosition=[(port1_pos[0])*pixelSize,port1_pos[1]*pixelSize,port2_pos[0]*pixelSize,port2_pos[1]*pixelSize]

    
    #pdb.set_trace()

    gds_file='/home/local/millipede/hy7593/pixelatedRF_verification/data/gds/'+fileName.replace('csv','gds')

    rrfc_gds=rfc(pixelSize=pixelSize,outF=filePath,unit=25.4e-6, corner='overlap', layoutRes=100, scale=1, sim=0,view=0,write=0,gdsfile=gds_file)

    recreateGDS_file(rrfc_gds)

    csv_file=filePath
    

    dataF=fileName.replace('.csv','')
    #pdb.set_trace()


    #pdb.set_trace()
    if sim == True:
    # Import GDS into ADS environment and setup environment for simulation
        em1 = emSim_2port_verification(workingPath = pathName, adsLibName = libName, gdsFile = gds_file,\
              csvFile = csv_file, numPorts = ports, portPositions = portPosition,\
              gdsCellName = cell, dataFile = dataF, portPos_pixel=portPos_pixel)
        emSim_2port_verification.momRun_2port(em1)

#mapName = pathName + 'pixelSize=' + str(pixelSize) + '_randomGenerated_sol_' + str(x) + '.csv'