#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 12:17:59 2019

@author: karel
"""
#Setup:------------------------------------------------------------------------
import matplotlib.pyplot as plt
from itertools import chain
import os
import numpy as np

folderpath = input("Please the path to the folder wher you have your outputs saved:")
plate_scale = 0.06 #How many arseconds one pixel represents in the image
lstfull = []
num_lst = []

#Defining functions needed for analysis ---------------------------------------

#Function to create list of filepaths to Galfit outputs for analysis
def fileloc(folderpath):
    '''
    Takes a folder path, goes to where it is and adds the name of each folder
    onto the end of the path, eventally making a list to all of the individual 
    output files in the folder.
    '''
    filelist = []
    for filename in os.listdir(folderpath):
        if filename.endswith(".txt"):
            listpath = os.path.join(folderpath, filename)
            filelist.append(listpath)
    return(np.sort(filelist)) #returns files in alphabetical order so non-xray sources at start

#Function to get data from files
def getdata(filelist):
    '''
    Goes through each output files and puts al of the information into a list.
    Then it takes that list and removes everything that is not related to the 
    sersic output.
    '''
    lstsersic = []
    for i in filelist:        
        with open(i, "r") as f: #Open file from the file path
            for line in f:
                lstfull.append(line) #Takes each line and appends it into a list
            lstsersic.append(lstfull[-6])
            lstsersic = [y.strip() for y in lstsersic] #Comprehension that removes \n from strings 
    return(lstsersic)

#Function to calculate effective radius and Sersic index of galaxies 
def Sersic_index(data):  
    '''
    Takes the sersic output and splits it into a list. Then goes through that 
    list and removes specifically the sersic index and the effective radius. 
    As these are automatically classed as strings of numbers it converts them
    into floats of numbers and makes them into a list. 
    '''
    num_lst = list(chain(*[s.split() for s in data])) #Takes the list of strings and splits it into one long list           
    eff_rad_raw = list(map(float, num_lst[6::10])) #Gets the effective radius from the list + converts from string to float
    eff_rad = [z*plate_scale for z in eff_rad_raw] #Takes eff rad and multiplies by the plate scale to covert from pixels to arcseconds
    SI = list(map(float, num_lst[7::10])) #Gets the sersic index from the list + converts from string to float
    return(eff_rad, SI)


    
#creating list of paths    
filelist = fileloc(folderpath)
#Get data from files
lstsersic = getdata(filelist)
#Calculate effective radius and sersic index for each galaxy 
eff_rad, SI = Sersic_index(lstsersic)    

#Plotting data-----------------------------------------------------------------

plt.title('Effective Radius (R) vs Sersic Index (n)')
plt.xlabel('Effective Radius (R) [Arcseconds]')
plt.ylabel('Sersic Index (n)')

check = str(input('Do you know how many xray sources your data contains? (y/n):'))

if check == 'y':
    endxray = len(SI) 
    startxray = len(SI)-int(input('How many non x-ray sources do you have?:')) 
    startnonxray = 0
    endnonxray = startxray-1
    plt.scatter(eff_rad[startnonxray:endnonxray+1], SI[startnonxray:endnonxray+1], color=['green'], marker = '+', label = 'Non X-ray source')
    plt.scatter(eff_rad[startxray:endxray], SI[startxray:endxray], color=['red'], marker = '*', label = 'X-ray source')
    plt.legend()
    plt.show()

elif check == 'n':
    start = 0
    end = len(SI)
    plt.scatter(eff_rad[start:end], SI[start:end], color = ['purple'], marker = 'x')
    plt.show()

print('Non x-ray Soruces: \n')
print('Sersic Index =', SI[startnonxray:endnonxray])
print('Effective Radius (in arcseconds) =', eff_rad[startnonxray:endnonxray], "\n")
print('X-Ray sources:\n')
print('Sersic Index =', SI[startxray:endxray])
print('Effective Radius (in arceseconds) =', eff_rad[startxray:endxray])

