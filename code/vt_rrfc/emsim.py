import meep as mp
import meep.adjoint as mpa
import autograd.numpy as npa
#import meep_materials
from meep.materials import Cu

from autograd import tensor_jacobian_product, grad
import gdspy
import os
exec(open(os.path.join(os.environ["MODULESHOME"],"init/python")).read())
import time, sys
from vt_rrfc import *
import matplotlib.pyplot as plt
import pdb
import keyboard
#from pynput.keyboard import Controller




class emSim:
  def __init__(self, 
               workingPath: str,
               adsLibName: str,
               gdsFile: str,
               csvFile: str,
               numPorts: int,
               portPositions,
               gdsCellName: str,
               dataFile: str,
               portPos_pixel,
               Substrate = None):
    self.pathName = workingPath
    self.libName = adsLibName
    self.gds_file = gdsFile
    self.csv_file = csvFile
    self.ports = numPorts
    self.portPosition = portPositions
    self.portPos_pixel=portPos_pixel
    self.cell = gdsCellName
    self.dataF = dataFile
    self.sub = Substrate
  """
  This code assumes that in your path, you will have an ADS workspace created amd that at 
  the same level of hierarchy you will have a data folder to collect simulation results 
  and design results in. The structure should be:
    ./YOUR_ADS_Workspace_wrk
    ./data
    ./data/gds
    ./data/pixelMaps
    ./data/spfiles
    ./data/spfiles/afs
  This is necessary because of how the simulation environment is created in ADS, and is not
  necessary for EMX simulations.

  WorkingPath --> base path where files will be placed
  adsLibName --> name of the ADS library that the simulation will be loaded. This library 
                 must exist before simulations can be called and run. Working to see if it
                 is possible to create a library using AEL, but no luck so far
  gdsFile --> This is the artwork file that will be loaded into ADS to be simulated
  csvFile --> This is a binary pixel map that shows the pixels that are pop'd (1) and 
              unpop'd (0)
  numPorts --> The number of ports that ADS will add to the drawing. 
  portPositions --> Vector that has the location of up to four ports...will work to expand 
                    possible port positions
  cell --> The cell name of the layout in the GDS file. For now, there needs to be a cell 
           name in the library with an emSetup located under the cell for the simulation 
           to be launched. Working to see if this can be automated, but no luck so far.
  dataFile --> This is the name of the data file that will be created at the end of the
               simulation. 
  """
  def momRun(self):
    # Import GDS into ADS environment and setup environment for simulation
    aelName = 'autoloadEMSim.dem'
    createOpenAel(self.pathName, self.libName, self.gds_file, self.ports, \
                      self.portPosition, aelName, self.cell)
    
    #pdb.set_trace()
    # This is must setup ADS tools to be on the path. It points to a setup script for the ECE
    # department at Virginia Tech. The script for CAD tools is used by the RFIC group in MICS 
    # at Virginia Tech. From a basic perspective, all that is needed for this script is to
    # setup $HPEESOF according to Keysights instructions and to add ADS binaries (e.g., ads, 
    # adsMomWrapper, etc.) onto the path. It must also provide a path to the license server, 
    # if the tools and license are setup by default in your system, this command can be
    # bypassed. Once the tools are on the path, ads is launched with
    # the AEL script that is created above the ADS setup (HPEESOF) which will put ads and 
    # adsMomWrapper on the path and setup the licensing. Future variants of the script will 
    # add hooks for EMX simulation   
    # 
     
    #command = 'source /home/local/millipede/hy7593/pixelatedRF_final/em_sim_automation_wrk/autoloadEMSim.dem &'
    #exec(open(os.path.join(os.environ["MODULESHOME"],"init/python")).read())
    #module("load ads")

    #os.system('export AGLMERR=expiring')
    
    
   
  

    



    
    command='ads -m /home/local/millipede/hy7593/pixelatedRF_final/'+self.libName+'_wrk/'+ aelName 
    #command='cd /home/local/millipede/hy7593/pixelatedRF_final/em_sim_automation_wrk; module load ads'
    #command = 'module load ads'#; ads -m ' \
              #+ self.pathName + self.libName + '_wrk/' + aelName + ' &'
    os.system(command)
    #pdb.set_trace()

    # Import of the gds and automation of port addition takes a few seconds. I add a pause 
    # to ensure that the import is fully done before starting the sim (can probably be 
    # shortened. Will later look to just add feature to only proceed when the execution 
    # above is complete
    time.sleep(25)
    print('We are still working')

    dataSet = self.dataF.replace(self.pathName + 'data/','') 
    print(dataSet)
    #pdb.set_trace()
    # Run Momentum Simulation
    os.chdir(self.pathName + self.libName + '_wrk/simulation/' + self.libName + '_lib/' + \
             self.cell + '/layout/emSetup_MoM/')
    command = 'adsMomWrapper -O -3D proj proj'
              #adsMomWrapper -O -3D proj proj'
    os.system(command)
    #pdb.set_trace()
    # Create the ADS Dataset
    #os.chdir(self.pathName + self.libName + '_wrk/simulation/' + self.libName + '_lib/' + \
            # self.cell + '/layout/emSetup_MoM/')
    #command = 'source /software/RFIC/cadtools/cadence/setups/setup-tools; \
              #adsMomWrapper -CD proj proj'
    #os.system(command)
    
    # Clean up after Momentum Simulation to prepare for next simulation
    aelCloseName = 'autoCloseEMSim.dem'
    createCloseAel(self.pathName,self.libName,aelCloseName, self.cell)
    
    

    #pdb.set_trace()
  
    os.chdir(self.pathName)
    # Eveything in its right place :)
    """
    command = 'mv ' + self.libName + '_wrk/simulation/' + \
              self.libName + '_lib/' + self.cell + '/layout/emSetup_MoM/proj.afs ' + \
              'data/spfiles/afs/' + dataSet + \
              '.afs; mv ' + self.csv_file + ' ' + self.pathName + \
              '/data/pixelMaps/.; mv ' + self.gds_file + ' ' + self.pathName + \
              '/data/gds/.'
              """
    
    command = 'mv ' + self.libName + '_wrk/simulation/' + \
              self.libName + '_lib/' + self.cell + '/layout/emSetup_MoM/proj.afs ' + \
              'data/spfiles/afs/' + dataSet + \
              '.afs'
    os.system(command)

    command = 'mv ' + self.libName + '_wrk/simulation/' + \
              self.libName + '_lib/' + self.cell + '/layout/emSetup_MoM/proj.cti ' + \
              'data/spfiles/cti/' + dataSet + \
              '.cti'
    
    os.system(command)

    # This will delete the layout view, leaving the emSetup so that the environment
    # is preparted for the next simulation
    command = 'ads -m /home/local/millipede/hy7593/pixelatedRF_final/em_sim_automation_wrk/'+ aelCloseName
    os.system(command)
    # This removes the simulation path so the environment can create a fresh one for 
    # the next simulation. All data should have been moved in steps above.
    #command = 'rm -rf ' + self.pathName + self.libName + '_wrk/simulation/*'
    #os.system(command)
    #pdb.set_trace()

    time.sleep(15)
    print('Cleaning up!')

    ctiFileName='/home/local/millipede/hy7593/pixelatedRF_final/data/spfiles/cti/' + dataSet + '.cti'
    csvFileName='/home/local/millipede/hy7593/pixelatedRF_final/data/spfiles/csv/' + dataSet + '.csv'

    read_c = open(ctiFileName)
    data = read_c.read()
    read_c.close()
    data = data.split("BEGIN\n")

    #freq_str= data[1].split("END")

    s_str = data[2].split("END")
    s11_str = s_str[0].replace("\t", "")
    s11_str = s11_str.split("\n")

    s_str = data[3].split("END")
    s12_str = s_str[0].replace("\t", "")
    s12_str = s12_str.split("\n")
    
    '''
    s_str = data[4].split("END")
    s21_str = s_str[0].replace("\t", "")
    s21_str = s21_str.split("\n")

    s_str = data[5].split("END")
    s22_str = s_str[0].replace("\t", "")
    s22_str = s22_str.split("\n")

    '''
    

    s_str = data[4].split("END")
    s13_str = s_str[0].replace("\t", "")
    s13_str = s13_str.split("\n")

    s_str = data[5].split("END")
    s14_str = s_str[0].replace("\t", "")
    s14_str = s14_str.split("\n")

    

    s_str = data[6].split("END")
    s21_str = s_str[0].replace("\t", "")
    s21_str = s21_str.split("\n")

    s_str = data[7].split("END")
    s22_str = s_str[0].replace("\t", "")
    s22_str = s22_str.split("\n")

    s_str = data[8].split("END")
    s23_str = s_str[0].replace("\t", "")
    s23_str = s23_str.split("\n")

    s_str = data[9].split("END")
    s24_str = s_str[0].replace("\t", "")
    s24_str = s24_str.split("\n")

    s_str = data[10].split("END")
    s31_str = s_str[0].replace("\t", "")
    s31_str = s31_str.split("\n")

    s_str = data[11].split("END")
    s32_str = s_str[0].replace("\t", "")
    s32_str = s32_str.split("\n")

    s_str = data[12].split("END")
    s33_str = s_str[0].replace("\t", "")
    s33_str = s33_str.split("\n")

    s_str = data[13].split("END")
    s34_str = s_str[0].replace("\t", "")
    s34_str = s34_str.split("\n")

    s_str = data[14].split("END")
    s41_str = s_str[0].replace("\t", "")
    s41_str = s41_str.split("\n")

    s_str = data[15].split("END")
    s42_str = s_str[0].replace("\t", "")
    s42_str = s42_str.split("\n")

    s_str = data[16].split("END")
    s43_str = s_str[0].replace("\t", "")
    s43_str = s43_str.split("\n")

    s_str = data[17].split("END")
    s44_str = s_str[0].replace("\t", "")
    s44_str = s44_str.split("\n")
    



    freq=[]

    s11_r = []
    s11_i = []
    

    s12_r = []
    s12_i = []

    s13_r = []
    s13_i = []

    s14_r = []
    s14_i = []
    

    s21_r = []
    s21_i = []
    

    s22_r = []
    s22_i = []

    s23_r = []
    s23_i = []

    s24_r = []
    s24_i = []

    s31_r = []
    s31_i = []

    s32_r = []
    s32_i = []
    
    s33_r = []
    s33_i = []

    s34_r = []
    s34_i = []

    s41_r = []
    s41_i = []

    s42_r = []
    s42_i = []
    
    s43_r = []
    s43_i = []
    
    s44_r = []
    s44_i = []

    port1_pos=[]
    port2_pos=[]
    port3_pos=[]
    port4_pos=[]


    

    a=[]
    rows=[['freq','s11_real','s11_imag','s12_real','s12_imag','s13_real','s13_imag','s14_real','s14_imag','s21_real','s21_imag','s22_real','s22_imag','s23_real','s23_imag','s24_real','s24_imag','s31_real','s31_imag','s32_real','s32_imag','s33_real','s33_imag','s34_real','s34_imag','s41_real','s41_imag','s42_real','s42_imag','s43_real','s43_imag','s44_real','s44_imag','port1_pos','port2_pos','port3_pos','port4_pos']]
    #rows=[['freq','s11_real','s11_imag','s12_real','s12_imag','s21_real','s21_imag','s22_real','s22_imag','port1_pos','port2_pos']]

    for i in range(len(s11_str) - 1):
        s11_ri = s11_str[i].split(",")
        s12_ri = s12_str[i].split(",")
        s13_ri = s13_str[i].split(",")
        s14_ri = s14_str[i].split(",")
        s21_ri = s21_str[i].split(",")
        s22_ri = s22_str[i].split(",")
        
        s23_ri = s23_str[i].split(",")
        s24_ri = s24_str[i].split(",")
        s31_ri = s31_str[i].split(",")
        s32_ri = s32_str[i].split(",")
        s33_ri = s33_str[i].split(",")
        s34_ri = s34_str[i].split(",")
        s41_ri = s41_str[i].split(",")
        s42_ri = s42_str[i].split(",")
        s43_ri = s43_str[i].split(",")
        s44_ri = s44_str[i].split(",")
        

        s11_r.append(float(s11_ri[0]))
        s11_i.append(float(s11_ri[1]))
        s12_r.append(float(s12_ri[0]))
        s12_i.append(float(s12_ri[1]))
        
        s13_r.append(float(s13_ri[0]))
        s13_i.append(float(s13_ri[1]))
        s14_r.append(float(s14_ri[0]))
        s14_i.append(float(s14_ri[1]))
        
        s21_r.append(float(s21_ri[0]))
        s21_i.append(float(s21_ri[1]))
        s22_r.append(float(s22_ri[0]))
        s22_i.append(float(s22_ri[1]))
        
        s23_r.append(float(s23_ri[0]))
        s23_i.append(float(s23_ri[1]))
        s24_r.append(float(s24_ri[0]))
        s24_i.append(float(s24_ri[1]))
        s31_r.append(float(s31_ri[0]))
        s31_i.append(float(s31_ri[1]))
        s32_r.append(float(s32_ri[0]))
        s32_i.append(float(s32_ri[1]))
        s33_r.append(float(s33_ri[0]))
        s33_i.append(float(s33_ri[1]))
        s34_r.append(float(s34_ri[0]))
        s34_i.append(float(s34_ri[1]))
        s41_r.append(float(s41_ri[0]))
        s41_i.append(float(s41_ri[1]))
        s42_r.append(float(s42_ri[0]))
        s42_i.append(float(s42_ri[1]))
        s43_r.append(float(s43_ri[0]))
        s43_i.append(float(s43_ri[1]))
        s44_r.append(float(s44_ri[0]))
        s44_i.append(float(s44_ri[1]))
        

        if i==0:
          port1_pos.append([self.portPos_pixel[0],self.portPos_pixel[1]])
          port2_pos.append([self.portPos_pixel[2],self.portPos_pixel[3]])
          port3_pos.append([self.portPos_pixel[4],self.portPos_pixel[5]])
          port4_pos.append([self.portPos_pixel[6],self.portPos_pixel[7]])
        else:
          port1_pos.append('NaN')
          port2_pos.append('NaN')
          port3_pos.append('NaN')
          port4_pos.append('NaN')

        

    

        freq.append(20+1*i)
        #pdb.set_trace()
        
        #a=[s11_db(i-1)]
        #a.append(s11_db(i),s11_phase(i),s12_db(i),s12_phase(i),s21_db(i),s21_phase(i),s22_db(i),s22_phase(i))
        a=[str(freq[i]),str(s11_r[i]),str(s11_i[i]),str(s12_r[i]),str(s12_i[i]),str(s13_r[i]),str(s13_i[i]),str(s14_r[i]),str(s14_i[i]),str(s21_r[i]),str(s21_i[i]),str(s22_r[i]),str(s22_i[i]),str(s23_r[i]),str(s23_i[i]),str(s24_r[i]),str(s24_i[i]),str(s31_r[i]),str(s31_i[i]),str(s32_r[i]),str(s32_i[i]),str(s33_r[i]),str(s33_i[i]),str(s34_r[i]),str(s34_i[i]),str(s41_r[i]),str(s41_i[i]),str(s42_r[i]),str(s42_i[i]),str(s43_r[i]),str(s43_i[i]),str(s44_r[i]),str(s44_i[i]),port1_pos[i],port2_pos[i],port3_pos[i],port4_pos[i]]
        #a=[str(freq[i]),str(s11_r[i]),str(s11_i[i]),str(s12_r[i]),str(s12_i[i]),str(s21_r[i]),str(s21_i[i]),str(s22_r[i]),str(s22_i[i]),port1_pos[i],port2_pos[i]]
        #a=[str(freq[i]),str(s11_r[i]),str(s11_i[i]),str(s12_r[i]),str(s12_i[i]),str(s21_r[i]),str(s21_i[i]),str(s22_r[i]),str(s22_i[i])]

        rows.append(a)
        #pdb.set_trace()
        

    #pdb.set_trace()

    # name of csv file 
    
    
    # writing to csv file 
    with open(csvFileName, 'w') as csvfile: 
    # creating a csv writer object
        writer = csv.writer(csvfile, delimiter=',') 
        for line in rows:

            writer.writerow(line)

            
  
  def emxRun(self, procFile):
    # Call EMX Simulation

    if self.ports == 1:
      emsPorts = '-p P000=p1 -p P001=p2 -i P000 '
      sports = '.s1p'
    elif self.ports == 2:
      emsPorts = '-p P000=p1 -p P001=p2 -p P002=p3 -p P003=p4 -i P000 -i P001 '
      sports = '.s2p'
    elif self.ports == 3:
      emsPorts = '-p P000=p1 -p P001=p2 -p P002=p3 -p P003=p4 -p P004=p5 ' + \
                 '-p P005=p6 -i P000 -i P001 -i P002 '
      sports = '.s3p'
    elif self.ports == 4:
      emsPorts = '-p P000=p1 -p P001=p2 -p P002=p3 -p P003=p4 -p P004=p5 ' + \
                 '-p P005=p6 -p P006=p7 -p P007=p8 -i P000 -i P001 -i P002 ' + \
                 '-i P003 '
      sports = '.s4p'
    else:
      print('Only 1, 2, 3, or 4 ports are currently supported')

    # An example setup-tools is included in the repository. This is an example of the tool setup
    # script for CAD tools used by the RFIC group in MICS at Virginia Tech. All that is needed 
    # for this script is the EMX setup which will put emx on the path. You also need a
    # pointer to the proc file you are using.     
    #+ self.gds_file + ' RANDOM ' + procFile + ' -e 0.2 -t 0.2 -v 0.2 --3d=* ' \
    command = 'source /software/RFIC/cadtools/cadence/setups/setup-tools; emx ' \
              + self.gds_file + ' ' + self.cell + ' ' + procFile + ' -e 1 -t 1 -v 0.5 --3d=* ' \
              + emsPorts + '--sweep 0 1e+11 --sweep-stepsize 1e+08 --verbose=3 --print-command-line -l ' \
              + '2 --dump-connectivity --quasistatic --dump-connectivity ' \
              + '--parallel=0 --simultaneous-frequencies=0 --recommended-memory ' \
              + '--key=EMXkey --format=touchstone -s ' + self.dataF + sports

    os.system(command)

    # Clean up after sim
    # '.s2p ' + self.pathName + '/data/spfiles/.'
    os.chdir(self.pathName)
    command = 'mv ' + self.csv_file + ' ' + self.pathName + '/data/pixelMaps/.; mv ' + \
              self.gds_file + ' ' + self.pathName + '/data/gds/.; mv ' + self.dataF + \
              sports + ' ' + self.pathName + '/data/spfiles/.'
    os.system(command)

  def meepRun(self):
    
    # Define specific boundary conditions for meep
    res = 50 # number of pixels per mil
    three_d = False # Do a full 3D calculation or no
    gds = gdspy.GdsLibrary(infile=self.gds_file) # load the GDS file
    pml_size = 1.0
    CELL_LAYER = 0
    PORT1_LAYER = 1
    PORT2_LAYER = 2
    PORT3_LAYER = 3
    PORT4_LAYER = 4
    SOURCE_LAYER = 5
    METAL_LAYER = 11
    
    # Define materials and frequencies
    fr4 = mp.Medium(epsilon=4.5)
    freq = 5e9
    dpml = 0
    cell_thickness = dpml + self.sub.t_metal + self.sub.t_sub + self.sub.t_metal + 2*(self.sub.t_metal+self.sub.t_sub) + dpml
    cell_zmin = 0
    cell_zmax = cell_zmin + cell_thickness
    cu_zmax = 0.5*self.sub.t_metal
    cu_zmin = -0.5*self.sub.t_metal

    # Read the cell size and volumes for the sources and monitors from the GDS file
    rrc = mp.get_GDSII_prisms(Cu, self.gds_file, METAL_LAYER, cu_zmin, cu_zmax)
    gnd = mp.get_GDSII_prisms(Cu, self.gds_file, CELL_LAYER, cu_zmin-self.sub.t_sub, cu_zmax-self.sub.t_sub-self.sub.t_metal)
    cell = mp.GDSII_vol(self.gds_file, CELL_LAYER, 0, 0)
    src_vol = mp.GDSII_vol(self.gds_file, SOURCE_LAYER, cu_zmax-self.sub.t_sub-self.sub.t_metal, cu_zmin)
    p1 = mp.GDSII_vol(self.gds_file, PORT1_LAYER, zmin=cu_zmin, zmax=cu_zmax)
    p2 = mp.GDSII_vol(self.gds_file, PORT2_LAYER, zmin=cu_zmin, zmax=cu_zmax)

    for np in range(len(rrc)):
      rrc[np].center -= gnd.center
      for nv in range(len(rrc[np].vertices)):
        rrc[np].vertices[nv] -= gnd.center
    src_vol.center -= gnd.center
    geometry = rrc + gnd
    sources = [mp.Source(mp.GaussianSource(freq, fwidth=0.5*freq),
                         component=mp.Ey,
                         center = src_vol.center,
                         size = src_vol.size)]
    sim = mp.Simulation(cell_size=gnd.size,
                        geometry=geometry,
                        sources=sources,
                        resolution=res)
    freqs = np.linspace(0,10e9,101)
    s_params = sim.get_S_parameters(freqs, 1)
    plt.plot(freqs/1e9, np.abs(s_params[0, 0, :]), label='S11')
    print("hello world")
    #p3 = mp.GDSII_vol(gds_file, PORT3_LAYER, zmin=cu_zmin, zmax=cu_zmax)
    #p4 = mp.GDSII_vol(gds_file, PORT4_LAYER, zmin=cu_zmin, zmax=cu_zmax)
