import os
import time, sys
from vt_rrfc import *
import pdb
import glob
import csv
import pdb


view = False # This controls if the GDS is viewed after each creation 
write = True # Control whether output files are written or not
pixelSize = 1 # the size of the randomized pixel
layoutUnit = 1e-4 # Pixel Size is 100um




# Get pixel maps
PixelpathName = '/home/local/ace/hy7593/ML_PA/Pixels' # pathname of folder to store the generated pixel maps 
pixelfile_list = glob.glob(PixelpathName+'/*.csv', recursive=True)


pixelfile_list.sort()
pdb.set_trace()


#pdb.set_trace()

for name in pixelfile_list:
   filePath=name
   #pdb.set_trace()

   fileName=filePath.split('/')[-1]

      
   #pdb.set_trace()
   gds_file='/home/local/ace/hy7593/ML_PA/gds/'+fileName.replace('csv','gds')
   rrfc_gds=rfc(pixelSize=pixelSize,outF=filePath,unit=1e-4, corner='overlap', layoutRes=100, scale=1, sim=0,view=0,write=0,gdsfile=gds_file)
   #pdb.set_trace()
   recreateGDS_file_2layer(rrfc_gds)





