##import ezdxf
import math   
import numpy as np
import pandas as pd
import random
import os
import csv
import matplotlib.pyplot as plt
import shutil


# Decodes 1-layer map to 2-layer
def func_decode_pixel_top(encoded_pixel):
    
    decoded_top = np.zeros((40, 40), dtype='int')
    decoded_bot = np.zeros((40, 40), dtype='int')

    # bottom layer: 2, 3, 6, 7
    decoded_bot[(encoded_pixel%4 == 2) | (encoded_pixel%4 == 3)] = 1
    
    # top layer: 1, 3, 5, 7
    decoded_top[(encoded_pixel%2 == 1)] = 1

    return decoded_bot, decoded_top


def func_encode_pixel_top(rawdata, encoded_top, encoded_bot):
    
    encoded_pixel = np.zeros((40, 40))

    encoded_pixel[(rawdata < 4) & (encoded_top == 0) & (encoded_bot == 0)] = 0
    encoded_pixel[(rawdata < 4) & (encoded_top == 1) & (encoded_bot == 0)] = 1
    encoded_pixel[(rawdata < 4) & (encoded_top == 0) & (encoded_bot == 1)] = 2
    encoded_pixel[(rawdata < 4) & (encoded_top == 1) & (encoded_bot == 1)] = 3
    encoded_pixel[(rawdata >= 4) & (encoded_top == 0) & (encoded_bot == 0)] = 4
    encoded_pixel[(rawdata >= 4) & (encoded_top == 1) & (encoded_bot == 0)] = 5
    encoded_pixel[(rawdata >= 4) & (encoded_top == 0) & (encoded_bot == 1)] = 6
    encoded_pixel[(rawdata >= 4) & (encoded_top == 1) & (encoded_bot == 1)] = 7

    return encoded_pixel


def find_lead_positions(matrix, layer='top'):

    leads = []
    search_row = 39 if layer == 'top' else 0
    lead_start = None

    for j in range(matrix.shape[1]):
        current_value = matrix[search_row][j]
        if current_value == 1 and lead_start is None:
            lead_start = j  # Found the start of a new lead
        elif current_value == 0 and lead_start is not None:
            leads.append((search_row, lead_start))
            leads.append((search_row, j - 1))# Found the end of the current lead
            lead_start = None  # Reset for the next lead

    # If the last column is part of a lead and it hasn't ended, include it
    if lead_start is not None:
        leads.append((lead_start, matrix.shape[1] - 1))

    return leads

    
def process_leads(leads, is_top):

    #set default indices based on top or bottom layer
    i1 = i2 = 39 if is_top else 0

    #initialize column indices to None
    j1 = j2 = None

    #check if there are at least 2 tuples in the leads list
    if len(leads) >= 2:
        #extract and adjust column indices from tuples
        j1 = leads[0][1] - 1
        j2 = leads[1][1]
    else:
        #default values
        i1 = i2 = j1 = j2 = 0

    return (i1, j1, i2, j2)

def adjust_i(matrix, i, j, increment, condition_value):
    if i < 0 or i >= 40:  # Ensure within bounds
        return i
    if matrix[i][j] == condition_value:
        return i - (1 if increment else 0)
    # Determine direction based on is_top
    return adjust_i(matrix, i + (1 if increment else -1), j, increment, condition_value)

def adjust_j(matrix, i, j, condition_value, on_edge_increment):
    if j < 0 or j >= 40:  # Ensure within bounds
        return j
    if matrix[i][j] == condition_value or j == 0:
        if j != 0 and on_edge_increment:
            return j + 1
        return j
    return adjust_j(matrix, i, j - 1, condition_value, on_edge_increment)

def traverse_matrix(matrix, i1, j1, i2, j2, is_top):
    if is_top:
        i1 = adjust_i(matrix, i1, j1, False, 1)  # Decrement i until condition
        i2 = adjust_i(matrix, i2, j2, False, 0)  # Decrement i until condition
    else:
        i1 = adjust_i(matrix, i1, j1, True, 1)   # Increment i until condition
        i2 = adjust_i(matrix, i2, j2, True, 0)   # Increment i until condition
    
    # Adjust j1 and j2 are similar for both top and bot
    j1 = adjust_j(matrix, i1, j1, 0, True)
    j2 = adjust_j(matrix, i2, j2, 1, False)
    j2 += 1

    # Align i1 with i2 and adjust i2 based on top or bot
    i1 = i2
    if is_top:
        i2 = adjust_i(matrix, i2, j2, False, 1)  # Decrement i for top
    else:
        i2 = adjust_i(matrix, i2, j2, True, 1)   # Increment i for bot
    i2 += 1
    j2 = max(min(j2 - 1, 39), 0)  # Ensure j2 within bounds after final adjustment

    return i1, j1, i2, j2

def adjust_horizontal(matrix, i, j, condition_value, is_top):
    if matrix[i][j] == condition_value or j == 39:
        return i + (-1 if is_top else 1), j - 1
    return adjust_horizontal(matrix, i, j + 1, condition_value, is_top)

def adjust_vertical(matrix, i, j, condition_value, adjust_i, adjust_j, is_top):
    marker = 0
    if (matrix[i][j] == 0 or i == condition_value) if is_top else (matrix[i][j] == 0 or i == condition_value):
        if i != condition_value:
            i += adjust_i
            marker = 1
        return i, j + 1
    if marker == 0:
        return adjust_vertical(matrix, i + (-1 if is_top else 1), j, condition_value, adjust_i, adjust_j, is_top)
    return

def move_leads(matrix, i1, j1, i2, j2, is_top, is_side):
    if not is_side:
        # Side condition adjustments
        i1, j1 = adjust_vertical(matrix, i1, j1, 0 if is_top else 39, 1 if is_top else -1, 1, is_top)  # Adjust i2 vertically and then j2
        j2 += 1
        i2, j2 = adjust_horizontal(matrix, i2, j2, 1, is_top)  # Adjust j1 horizontally
    #else:
        # Non-side condition adjustments
       # i1, j1 = adjust_vertical(matrix, i1, j1, 0, 1 if is_top else -1, 1, is_top)  # Adjust i1 vertically and then j1
       # j2 += 1  # Pre-adjust j2 based on provided logic
       # i2, j2 = adjust_horizontal(matrix, i2, j2, 39, 1, False)  # Adjust j2 horizontally for both top and bot

    return i1, j1, i2, j2


'''
def place_boxes(matrix, i, j, num_boxes, length_box, height_box, subdividh):
    """
    Places boxes within the matrix based on specified dimensions and starting position.
    
    Parameters:
    - matrix (np.array): The matrix where boxes will be placed.
    - i (int): Row index in the matrix to start placing boxes.
    - j (int): Column index in the matrix to start placing boxes.
    - num_boxes (int): Number of boxes to place.
    - length_box (int): Length of each box to be placed.
    - height_box (int): Height of each box to be placed.
    - subdividh (float): Subdivision height, used to calculate spacing between boxes.
    
    This function iteratively places a specified number of boxes within the matrix, starting from a given position. Each box is placed according to its length and height, with appropriate spacing determined by `subdividh`. It ensures that boxes are placed within the matrix boundaries and adjusts the position for each box to avoid overlap.
    """

    for box_num in range(num_boxes):
        for length_index in range(length_box):
            for height_index in range(height_box):
                # Calculate the indices for the cell to place the box
                target_row = i - 1 - height_index
                target_col = j + (box_num + 1) * math.ceil(subdividh - length_box / 2) + length_index
                
                # Check if the calculated indices are within the bounds of the matrix
                if 0 <= target_row < len(matrix) and 0 <= target_col < len(matrix[0]):
                    # Check if the target cell is empty (contains 0)
                    if matrix[target_row][target_col] == 0:
                        # Place the box (set the cell value to 1)
                        matrix[target_row][target_col] = 1
'''                        


directory = r'/home/local/millipede/hy7593/test_pixel'
newdir=r'/home/local/millipede/hy7593/new_pixel/new_pixel'
dimensions=([[" " for i in range(14)] for j in range(1)])

"""
numboxes1bot=1
numboxes2bot=1
numboxes3bot=1
lengthbox1bot=1
lengthbox2bot=1
lengthbox3bot=1
heightbox1bot=1
heightbox2bot=1
heightbox3bot=1
"""
dimensions[0][0]="filename"
dimensions[0][1]='numberboxesleftright_top'
dimensions[0][2]='numberboxestop_top'
dimensions[0][3]='lengthboxleftright_top'
dimensions[0][4]='lengthboxtop_top'
dimensions[0][5]='heightboxleftright_top'
dimensions[0][6]='heightboxtop_top'
dimensions[0][7]='numberboxesleftright_bot'
dimensions[0][8]='numberboxestop_bot'
dimensions[0][9]='lengthboxleftright_bot'
dimensions[0][10]='lengthboxtop_bot'
dimensions[0][11]='heightboxleftright_bot'
dimensions[0][12]='heightboxtop_bot'
dimensions[0][13]='seed'

seed=234567
random.seed(a=seed, version=2)

#data indexing 0-39
    #PixMap==0: no top, no bottom, no gnd
    #PixMap==1: top, no bottom, no gnd
    #PixMap==2: no top, bottom, no gnd
    #PixMap==3: top, bottom, no gnd
    #PixMap==4: no top, no bottom, gnd
    #PixMap==5: top, no bottom, gnd
    #PixMap==6: no top, bottom, gnd
    #PixMap==7: top, bottom, gnd

filenum = 0
for filename in os.listdir(directory):
    filenum+=1
    file = os.path.join(directory, filename)
    print("\n\n" + filename)

    dimensions.append([" " for i in range(14)])
    dimensions[filenum][0]=filename

    rawdata = list(csv.reader(open(file)))
    #rawdata = np.array(pd.read_csv(filename, header=None), dtype=)
    rawdata = np.array(pd.read_csv(file, header=None), dtype='int')


    topleadscount=0
    botleadscount=0
    rows=40
    cols=40
    bot = np.asarray([[0 for i in range(cols)] for j in range(rows)])
    top = np.asarray([[0 for i in range(cols)] for j in range(rows)])

    bot, top = func_decode_pixel_top(rawdata)

    bot=np.rot90(bot)
    bot=np.rot90(bot)
    #flip the array to reapply top functions

    #col, row = 2, 1
    #fig, axes = plt.subplots(row, col, figsize=(col*3, rows*3))
    #axes[0].imshow(np.rot90(top, k=-1), cmap='Greys', origin='lower')
    #axes[1].imshow(np.rot90(bot, k=-1), cmap='Greys', origin='lower')
    #plt.show()

    
    botleads=np.asarray([0]*4)
    topleads=np.asarray([0]*4)
    
    #finding lead positions for both top and bottom layers
    topleads = find_lead_positions(top, 'top')
    botleads = find_lead_positions(bot, 'top')
                
    #process data into top and bot 2d lists for changing operations                
    lengthbox1 = 1
    heightbox1 = 2
    numboxes1 = 2
    lengthbox2 = 2
    #no odd numbers in length 2 as it will break symmetry
    heightbox2 = 2
    numboxes2 = 1
    lengthbox3 = 5
    heightbox3 = 2
    numboxes3 = 1

    lengthbox1bot = 5
    heightbox1bot = 2
    numboxes1bot = 1
    lengthbox2bot = 2
    #no odd numbers in length 2 as it will break symmetry
    heightbox2bot = 2
    numboxes2bot = 1
    lengthbox3bot = 5
    heightbox3bot = 2
    numboxes3bot = 1

    #height is distance off the coil on each side, length is distance along the coil
    #numboxes is the number of boxes along each individual length of coil
    #the number is which part of the coil we are on
    #1 corresponds to the left in the excel
    #2 corresponds to the top, opposite the leads
    #3 corresponds to the right in the excel

    i1, j1, i2, j2 = process_leads(topleads, True)
    i1bot, j1bot, i2bot, j2bot = process_leads(botleads, True)

    i2copy=i2
    j2copy=j2
    i2copybot=i2bot
    j2copybot=j2bot
    print(i2,j2,i2bot,j2bot)
    while 1==1:
        if top[i2copy][j2copy]==0 or i2copy==0:
            i2copy+=1
            break
        i2copy-=1
    if top[i2copy][j2copy+1]==1 or i2copy==0:
        dimensions[filenum][1]=0
        dimensions[filenum][2]=0
        dimensions[filenum][3]=0
        dimensions[filenum][4]=0
        dimensions[filenum][5]=0
        dimensions[filenum][6]=0
        dimensions[filenum][7]=1
        dimensions[filenum][8]=1
        dimensions[filenum][9]=1
        dimensions[filenum][10]=1
        dimensions[filenum][11]=1
        dimensions[filenum][12]=1
        dimensions[filenum][13]=seed
        print("here")
        continue
    while 1==1:
        if bot[i2copybot][j2copybot]==0 or i2copybot==0:
            i2copybot+=1
            break
        i2copybot-=1
    if bot[i2copybot][j2copybot+1]==1 or i2copybot==0:
        dimensions[filenum][1]=1
        dimensions[filenum][2]=1
        dimensions[filenum][3]=1
        dimensions[filenum][4]=1
        dimensions[filenum][5]=1
        dimensions[filenum][6]=1
        dimensions[filenum][7]=0
        dimensions[filenum][8]=0
        dimensions[filenum][9]=0
        dimensions[filenum][10]=0
        dimensions[filenum][11]=0
        dimensions[filenum][12]=0
        dimensions[filenum][13]=seed
        print("here2")
        continue

    i1, j1, i2, j2 = traverse_matrix(top, i1, j1, i2, j2, True)
    i1bot, j1bot, i2bot, j2bot = traverse_matrix(bot, i1bot, j1bot, i2bot, j2bot, True)


    availableh1=i1-i2
    availablew1=j2-j1

    numboxes1=1
    numboxes2=1
    numboxes3=1
    lengthbox1=1
    lengthbox2=1
    lengthbox3=1
    heightbox1=1
    heightbox2=1
    heightbox3=1
    #initialization and seeding

    
    if availableh1>10 and availableh1<20 and random.randint(1,4)>=2:
        numboxes1=2
    elif availableh1>=20 and random.randint(1,4)>=2:
        numboxes1=3
    lengthbox1=random.randint(1,math.floor(availableh1/numboxes1/2))
    heightbox1=random.randint(1,math.ceil(availablew1/2/2))

    numboxes3=numboxes1
    lengthbox3=lengthbox1
    heightbox3=heightbox1

    #print(str(numboxes3))
    #print(str(lengthbox3))
    #print(str(heightbox3))
    
    availableh1bot=abs(i1bot-i2bot)
    availablew1bot=j2bot-j1bot

    numboxes1bot=1
    numboxes2bot=1
    numboxes3bot=1
    lengthbox1bot=1
    lengthbox2bot=1
    lengthbox3bot=1
    heightbox1bot=1
    heightbox2bot=1
    heightbox3bot=1
    #initialization and seeding

    if availableh1bot>10 and availableh1bot<20 and random.randint(1,4)>=2:
        numboxes1bot=2
    elif availableh1bot>=20 and random.randint(1,4)>=2:
        numboxes1bot=3
    lengthbox1bot=random.randint(1,math.floor(availableh1bot/numboxes1bot/2))
    heightbox1bot=random.randint(1,math.ceil(availablew1bot/2/2))

    numboxes3bot=numboxes1bot
    lengthbox3bot=lengthbox1bot
    heightbox3bot=heightbox1bot

    #print(str(numboxes3bot))
    #print(str(lengthbox3bot))
    #print(str(heightbox3bot))

    #available length on left side to place protrusions

    subdividh1=availableh1/(numboxes1+1)
    subdividh1bot=availableh1bot/(numboxes1bot+1)
    for i in range(numboxes1):
        for ii in range(lengthbox1):
            for iii in range(heightbox1):
                #iterate every cell i wish to place on left side of left top coil
                #conditional to check out of bounds
                if i1-(i+1)*math.ceil(subdividh1-lengthbox1/2)-ii>=0 and i1-(i+1)*math.ceil(subdividh1-lengthbox1/2)-ii<40 and j1-1-iii>=0 and j1-1-iii<40:
                    top[i1-(i+1)*math.ceil(subdividh1-lengthbox1/2)-ii][j1-1-iii]=1
    for i in range(numboxes1bot):
        for ii in range(lengthbox1bot):
            for iii in range(heightbox1bot):
                #iterate every cell i wish to place on left side of left top coil
                #conditional to check out of bounds
                if i1bot-(i+1)*math.ceil(subdividh1bot-lengthbox1bot/2)-ii>=0 and i1bot-(i+1)*math.ceil(subdividh1bot-lengthbox1bot/2)-ii<40 and j1bot-1-iii>=0 and j1bot-1-iii<40:
                    bot[i1bot-(i+1)*math.ceil(subdividh1bot-lengthbox1bot/2)-ii][j1bot-1-iii]=1

    for i in range(numboxes1):
        for ii in range(lengthbox1):
            for iii in range(heightbox1):
                #iterate every cell i wish to place on right side of left top coil
                #conditional to check out of bounds
                if i1-(i+1)*math.ceil(subdividh1-lengthbox1/2)-ii>=0 and i1-(i+1)*math.ceil(subdividh1-lengthbox1/2)-ii<40 and j2+1+iii>=0 and j2+1+iii<40:
                    top[i1-(i+1)*math.ceil(subdividh1-lengthbox1/2)-ii][j2+1+iii]=1
    for i in range(numboxes1bot):
        for ii in range(lengthbox1bot):
            for iii in range(heightbox1bot):
                #iterate every cell i wish to place on right side of left top coil
                #conditional to check out of bounds
                if i1bot-(i+1)*math.ceil(subdividh1bot-lengthbox1bot/2)-ii>=0 and i1bot-(i+1)*math.ceil(subdividh1bot-lengthbox1bot/2)-ii<40 and j2bot+1+iii>=0 and j2bot+1+iii<40:
                    bot[i1bot-(i+1)*math.ceil(subdividh1bot-lengthbox1bot/2)-ii][j2bot+1+iii]=1

    i1=i2
    j1=j2
    i1bot=i2bot
    j1bot=j2bot
 
    i1, j1, i2, j2 = move_leads(top, i1, j1, i2, j2, True, False)
    i1bot, j1bot, i2bot, j2bot = move_leads(bot, i1bot, j1bot, i2bot, j2bot, True, False)
    print(i1, j1, i2, j2, i1bot, j1bot, i2bot, j2bot)
    
    availableh2=abs(i2-i1)
    availablew2=abs(j2-j1)

    availableh2bot=abs(i2bot-i1bot)
    availablew2bot=abs(j2bot-j1bot)

    if availablew2>10 and availablew2%2==0:
        numboxes2=random.randint(1,2)
    lengthbox2=random.randint(1,math.floor(availablew2/numboxes2/2/2)+1)*2
    heightbox2=random.randint(1,math.ceil(availableh2/2))

    if availablew2bot>10:
        numboxes2bot=random.randint(1,2)
    lengthbox2bot=random.randint(1,math.floor(availablew2bot/numboxes2bot/2/2)+1)*2
    heightbox2bot=random.randint(1,math.ceil(availableh2bot/2))
    #print(str(numboxes2))
    #print(str(lengthbox2))
    #print(str(heightbox2))
    #print(str(numboxes2bot))
    #print(str(lengthbox2bot))
    #print(str(heightbox2bot))

    #available length on top side to place protrusions

    subdividh2=availablew2/(numboxes2+1)
    subdividh2bot=availablew2bot/(numboxes2bot+1)

    #record the dimensions of everything in each file
    """
    numboxes1bot=1
    numboxes2bot=1
    numboxes3bot=1
    lengthbox1bot=1
    lengthbox2bot=1
    lengthbox3bot=1
    heightbox1bot=1
    heightbox2bot=1
    heightbox3bot=1
    """
    
    dimensions[filenum][1]=numboxes1
    dimensions[filenum][2]=numboxes2
    dimensions[filenum][3]=lengthbox1
    dimensions[filenum][4]=lengthbox2
    dimensions[filenum][5]=heightbox1
    dimensions[filenum][6]=heightbox2
    dimensions[filenum][7]=numboxes1bot
    dimensions[filenum][8]=numboxes2bot
    dimensions[filenum][9]=lengthbox1bot
    dimensions[filenum][10]=lengthbox2bot
    dimensions[filenum][11]=heightbox1bot
    dimensions[filenum][12]=heightbox2bot
    dimensions[filenum][13]=seed


    
    for i in range(numboxes2):
        for ii in range(lengthbox2):
            for iii in range(heightbox2):
                #iterate every cell i wish to place on left side of top top coil
                #conditional to check out of bounds
                if i1-1-iii>=0 and i1-1-iii<40 and j1+(i+1)*math.ceil(subdividh2-lengthbox2/2)+ii>=0 and j1+(i+1)*math.ceil(subdividh2-lengthbox2/2)+ii<40:
                    top[i1-1-iii][j1+(i+1)*math.ceil(subdividh2-lengthbox2/2)+ii+((i)%2)*math.floor(lengthbox2/2)]=1
    for i in range(numboxes2bot):
        for ii in range(lengthbox2bot):
            for iii in range(heightbox2bot):
                #iterate every cell i wish to place on left side of top top coil
                #conditional to check out of bounds
                if i1bot-1-iii>=0 and i1bot-1-iii<40 and j1bot+(i+1)*math.ceil(subdividh2bot-lengthbox2bot/2)+ii>=0 and j1bot+(i+1)*math.ceil(subdividh2bot-lengthbox2bot/2)+ii<40:
                    bot[i1bot-1-iii][j1bot+(i+1)*math.ceil(subdividh2bot-lengthbox2bot/2)+ii+((i)%2)*math.floor(lengthbox2bot/2)]=1

    for i in range(numboxes2):
        for ii in range(lengthbox2):
            for iii in range(heightbox2):
                #iterate every cell i wish to place on right side of top top coil
                #conditional to check out of bounds
                if i2+1+iii>=0 and i2+1+iii<40 and j1+(i+1)*math.ceil(subdividh2-lengthbox2/2)+ii>=0 and j1+(i+1)*math.ceil(subdividh2-lengthbox2/2)+ii<40:
                    top[i2+1+iii][j1+(i+1)*math.ceil(subdividh2-lengthbox2/2)+ii+((i)%2)*math.floor(lengthbox2/2)]=1
    for i in range(numboxes2bot):
        for ii in range(lengthbox2bot):
            for iii in range(heightbox2bot):
                #iterate every cell i wish to place on right side of top top coil
                #conditional to check out of bounds
                if i2bot+1+iii>=0 and i2bot+1+iii<40 and j1bot+(i+1)*math.ceil(subdividh2bot-lengthbox2bot/2)+ii>=0 and j1bot+(i+1)*math.ceil(subdividh2bot-lengthbox2bot/2)+ii<40:
                    bot[i2bot+1+iii][j1bot+(i+1)*math.ceil(subdividh2bot-lengthbox2bot/2)+ii+((i)%2)*math.floor(lengthbox2bot/2)]=1

    i2+=1
    j2+=1
    i1=i2
    j1=j2
    j2-=1

    i2bot+=1
    j2bot+=1
    i1bot=i2bot
    j1bot=j2bot
    j2bot-=1

    while 1==1:
        if top[i1][j1]==0 or j1==39:
            if j1!=39:
                j1-=1
            break
        j1+=1
    while 1==1:
        if top[i2][j2]==1:
            i2-=1
            j2+=1
            break
        i2+=1
    #bot
    while 1==1:
        if bot[i1bot][j1bot]==0 or j1bot==39:
            if j1bot!=39:
                j1bot-=1
            break
        j1bot+=1
    while 1==1:
        if bot[i2bot][j2bot]==1:
            i2bot-=1
            j2bot+=1
            break
        i2bot+=1

    
    

    availableh3=i2-i1
    availablew3=j1-j2

    availableh3bot=abs(i2bot-i1bot)
    availablew3bot=j1bot-j2bot

    #available length on top side to place protrusions

    subdividh3=availableh3/(numboxes3+1)
    subdividh3bot=availableh3bot/(numboxes3bot+1)

    for i in range(numboxes3):
        for ii in range(lengthbox3):
            for iii in range(heightbox3):
                #iterate every cell i wish to place on left side of left coil
                #conditional to check out of bounds
                if i2-(i+1)*math.ceil(subdividh3-lengthbox3/2)-ii>=0 and i2-(i+1)*math.ceil(subdividh3-lengthbox3/2)-ii<40 and j1+1+iii>=0 and j1+1+iii<40:
                    top[i2-(i+1)*math.ceil(subdividh3-lengthbox3/2)-ii][j1+1+iii]=1
    for i in range(numboxes3bot):
        for ii in range(lengthbox3bot):
            for iii in range(heightbox3bot):
                #iterate every cell i wish to place on left side of left coil
                #conditional to check out of bounds
                if i2bot-(i+1)*math.ceil(subdividh3bot-lengthbox3bot/2)-ii>=0 and i2bot-(i+1)*math.ceil(subdividh3bot-lengthbox3bot/2)-ii<40 and j1bot+1+iii>=0 and j1bot+1+iii<40:
                    bot[i2bot-(i+1)*math.ceil(subdividh3bot-lengthbox3bot/2)-ii][j1bot+1+iii]=1

    for i in range(numboxes3):
        for ii in range(lengthbox3):
            for iii in range(heightbox3):
                #iterate every cell i wish to place on right side of left coil
                #conditional to check out of bounds
                if i2-(i+1)*math.ceil(subdividh3-lengthbox3/2)-ii>=0 and i2-(i+1)*math.ceil(subdividh3-lengthbox3/2)-ii<40 and j2-1-iii>=0 and j2-1-iii<40:
                    top[i2-(i+1)*math.ceil(subdividh3-lengthbox3/2)-ii][j2-1-iii]=1
    for i in range(numboxes3bot):
        for ii in range(lengthbox3bot):
            for iii in range(heightbox3bot):
                #iterate every cell i wish to place on right side of left coil
                #conditional to check out of bounds
                if i2bot-(i+1)*math.ceil(subdividh3bot-lengthbox3bot/2)-ii>=0 and i2bot-(i+1)*math.ceil(subdividh3bot-lengthbox3bot/2)-ii<40 and j2bot-1-iii>=0 and j2bot-1-iii<40:
                    bot[i2bot-(i+1)*math.ceil(subdividh3bot-lengthbox3bot/2)-ii][j2bot-1-iii]=1

    bot=np.rot90(bot)
    bot=np.rot90(bot)
    #reprocess data into multilayerform
    #data indexing 0-39
    #PixMap==0: no top, no bottom, no gnd
    #PixMap==1: top, no bottom, no gnd
    #PixMap==2: no top, bottom, no gnd
    #PixMap==3: top, bottom, no gnd
    #PixMap==4: no top, no bottom, gnd
    #PixMap==5: top, no bottom, gnd
    #PixMap==6: no top, bottom, gnd
    #PixMap==7: top, bottom, gnd
                    
    rawdata = func_encode_pixel_top(rawdata, top, bot)
    #col, row = 2, 1
    #fig, axes = plt.subplots(row, col, figsize=(col*3, rows*3))
    #axes[0].imshow(np.rot90(top, k=-1), cmap='Greys', origin='lower')
    #axes[1].imshow(np.rot90(bot, k=-1), cmap='Greys', origin='lower')
    #plt.show()

    #send file to csv
    #on windows: csv line terminator '\r\n' is translated into '\r\r\n' resulting in a newline between each row, so newline must be specified
    #may be different for other os
    #newdir=r'C:\Users\sunsh\Downloads\sample_gds_pixmap\pixelMaps'
    with open(newdir+'\\new_'+filename, 'w', newline='') as f:
    
    # Create a CSV writer object that will write to the file 'f'
        csv_writer = csv.writer(f,delimiter=',')
    
    # Write the field names (column headers) to the first row of the CSV file
        for line in rawdata:
            csv_writer.writerow(line)

    #pd.DataFrame(np.array(rawdata)).to_csv(newdir+'new_'+filename)

#end iterations write the seeding info and dimensions
with open(newdir+'\\seeding_dimensions.csv', 'w', newline='') as f:
    
    # Create a CSV writer object that will write to the file 'f'
    csv_writer = csv.writer(f,delimiter=',')
    
    # Write the field names (column headers) to the first row of the CSV file
    for line in dimensions:
        csv_writer.writerow(line)
