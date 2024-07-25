import os
import time, sys
from vt_rrfc import *
import pdb
import glob
import csv
import pandas as pd


simulator = 'ADS' # This controls the simulation to be used. Right now there are two valid values 'ADS' or 'EMX'
libName = 'em_sim_automation' # This is the name of the ADS workspace that was created to run sims in
sim = True # This controls whether a simulation is run or not.
view = False # This controls if the GDS is viewed after each creation 
write = True # Control whether output files are written or not
pixelSize = 1 # the size of the randomized pixel in mil Typically constrained by a PCB manufacturer.
layoutUnit = 1e-4 # Set the layout unit to mils




# Get reference design pixel maps
PortpathName = '/home/local/ace/hy7593/ML_PA/port_info' 
PixelpathName = '/home/local/ace/hy7593/ML_PA/pixels'
gdspathName = '/home/local/ace/hy7593/ML_PA/gds'
Mirror_PixelpathName='/home/local/ace/hy7593/ML_PA/mirror_pixels'

portfile_list = glob.glob(PortpathName+'/*.csv', recursive=True)


# The number of ports for the generated pixelmap is 2.
ports=3
sim=1
libName = 'em_sim_automation'
pathName = '/home/local/ace/hy7593/ML_PA/ADS_lib/' # Base path for file creation
cell = 'RANDOM'

y_size=200
x_size=300

unit_size=50*layoutUnit/(1e-6)

#pdb.set_trace()

for num in range(0,1): 
    # get the port info from the port csv file
    port_file_name=PortpathName + '/port_for_design_'+ str(num) + '.csv'
    pixel_file_name=PixelpathName + '/pixel_for_design_'+ str(num) + '.csv'
    gds_file_name=gdspathName + '/gds_for_design_'+ str(num) + '.gds'  # target gds file location
    mirror_pixel_file_name=Mirror_PixelpathName + '/mirror_pixel_for_design_'+ str(num) + '.csv'
    
    # the original pixel map needs to be mirrored with respect to x aix as the gds generation function uses a mirror coordinate
    with open(pixel_file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        rows = list(reader)
    
    rows.reverse()

    with open(mirror_pixel_file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)


    df_pin=pd.read_csv(port_file_name)

    port_in_pos=df_pin['port_in_x'].iloc[0],df_pin['port_in_y'].iloc[0]
    port_out_pos=df_pin['port_out_x'].iloc[0],df_pin['port_out_y'].iloc[0]
    port_short_pos=df_pin['port_short_x'].iloc[0],df_pin['port_short_y'].iloc[0]
    
    #pdb.set_trace()


    portPosition=[(port_in_pos[0])*unit_size,port_in_pos[1]*unit_size,port_out_pos[0]*unit_size,port_out_pos[1]*unit_size,port_short_pos[0]*unit_size,port_short_pos[1]*unit_size]  
    

    rrfc_gds=rfc(pixelSize=pixelSize,outF=mirror_pixel_file_name,unit=layoutUnit, corner='nonoverlap', layoutRes=100, scale=1, sim=0,view=0,write=0,gdsfile=gds_file_name)
    recreateGDS_file(rrfc_gds)

    csv_file=[]
    dataF='port_for_design_'+ str(num)


    #pdb.set_trace()
    if sim == True:
    # Import GDS into ADS environment and setup environment for simulation
        em1 = emSim_2port(workingPath = pathName, adsLibName = libName, gdsFile = gds_file_name,\
            csvFile = csv_file, numPorts = ports, portPositions = portPosition,\
            gdsCellName = cell, dataFile = dataF, portPos_pixel=portPosition)
        emSim_2port.momRun_2port(em1)



