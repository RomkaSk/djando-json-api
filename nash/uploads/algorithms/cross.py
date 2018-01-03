# -*- coding: utf-8 -*-
"""
Created on Mon Oct 09 13:40:07 2017

PROJECT:    MD HEARING
GOAL:       Create start correlations values for cross-selling 

@author: Monique
"""


# Import packages
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import re
import os
from sklearn.linear_model import LogisticRegression as logm 
import ast
import math


def main(input_path, output_path):
    
    # Set path
    # path = 'C:\\Users\\XE\\Downloads\\Telegram Desktop'
    # os.chdir(path)


    ### OPEN EXCEL ###
    file = input_path
    data = pd.ExcelFile(file)       # Make a connection
    df = data.parse(0)              # Make a datafram

    # Change structure
    df.columns = df.iloc[1,:]
    df = df.drop(df.index[[0,1]])
    df.index = df.iloc[:,0]

    # Select right columns
    list_ColumnNames = ['ID', 'Title', 'Visible', 'Brand', 'Functional name', 'EarSide', 'Add Protection Plan', 'URL code']
    df = df.loc[:,list_ColumnNames]

    # Visible list
    list_Visible = [None]*len(df)
    list_df_Visible = df.loc[:,'Visible'].tolist()

    for i in range(0,len(df)):
        if str(list_df_Visible[i]) == 'nan':
            list_Visible[i] = 0
        else:
            list_Visible[i] = 1
    
    # Change functional name to {Hearing Aid, Accessoires, Batteries, TDT, Protection Plan}
    list_FN = [None]*len(df)
    list_df_FN = (df.loc[:,'Functional name']).tolist()
    for i in range(0,len(df)):
        if str(list_df_FN[i]) == 'Hearing aid':
            list_FN[i] = 'HA'
        elif str(list_df_FN[i]) == 'Batteries':
            list_FN[i] = 'BAT'
        elif str(list_df_FN[i]) == 'Tubing Domes and Tips':
            list_FN[i] = 'TDT'
        elif str(list_df_FN[i]) == 'Protection Plan':
            list_FN[i] = 'PP'
        else:
            list_FN[i] = 'ACC'

    # Make list to store type data - from URL Code
    list_Type = [None]*len(df)
    list_df_URLCode = (df.loc[:,'URL code']).tolist()
    list_word = ['air-', 'lux-', 'control-', 'pro-']

    for i in range(0,len(df)):
        for word in list_word: 
            if word in str(list_df_URLCode[i]):
                list_Type[i] = word[:-1].upper()
                
    list_Type[14] = 'LUX'            

    # EarSide = {Left, right, pair, one}
    list_EarSide = [None]*len(df)
    list_df_EarSide = (df.loc[:,'EarSide']).tolist()
    for i in range(0,len(df)):
        if str(list_df_EarSide[i]) == 'Left':
            list_EarSide[i] = 'L'
        elif str(list_df_EarSide[i]) == 'Right':
            list_EarSide[i] = 'R'
        elif str(list_df_EarSide[i]) == 'Pair':
            list_EarSide[i] = 'P'
        elif str(list_df_EarSide[i]) == 'One':
            list_EarSide[i] = 'O'
    
    # add protection plan values into list
    index = [126, 128, 130, 132]
    for i in range(0,len(index)):
        tel = index[i] - 1
        list_EarSide[tel] =   'P'    

    # Protection plan
    list_ProtectionPlan = [None]*len(df)
    list_df_ProtectionPlan = (df.loc[:,'Add Protection Plan']).tolist()

    for i in range(0,len(df)):
        if list_FN[i] == 'HA' and 'Included' in str(list_df_ProtectionPlan[i]):
            list_ProtectionPlan[i] = 0
        elif list_FN[i] == 'HA' and 'Included' not in str(list_df_ProtectionPlan[i]) and str(list_df_ProtectionPlan[i]) != 'nan':
            list_ProtectionPlan[i] = list_Type[i]

    # Merge right data
    df_MDHearing = pd.DataFrame.from_records([list_Visible, list_Type, list_FN, list_EarSide, list_ProtectionPlan])
    df_MDHearing = df_MDHearing.T
    df_MDHearing.columns = ['Visible', 'Type', 'FunctionalName', 'EarSide', 'PPlan']


    ### MAKE CROSS CORRELATION MATRIX TO STORE RESULTS ###
    # Define dataframe
    np_CrossCorrelation = np.zeros([len(df),len(df)])
    df_CrossCorrelation = pd.DataFrame(np_CrossCorrelation)
    df_CrossCorrelation.index = df.index
    df_CrossCorrelation.columns = df.index 

    # Calculate correlations
    # Row products
    for i in range(0,len(df)):
        # Check if row product is visible
        if list_Visible[i] == 0:
            np_CrossCorrelation[i,:] = np.zeros([1,len(df)])
        else:
            # Chcek row element with each column element
            for j in range(0,len(df)):
                # Check if column element is visible
                if list_Visible[j] == 0:
                    np_CrossCorrelation[i,j] = 0
                
                ### PRODUCT i IS A HEARING AID ###
                elif list_FN[i] == 'HA':
                    # Product j is hearing aid
                    if list_FN[j] == 'HA':
                        np_CrossCorrelation[i,j] = 0
                        
                    # Product j is hearing accessoire
                    elif list_FN[j] == 'ACC':
                        # UV box gets 1
                        if j == 16:
                            np_CrossCorrelation[i,j] = 1
                        else:
                            np_CrossCorrelation[i,j] = np.random.uniform(0.8,0.95,1)
                        
                    # Product j is battery
                    elif list_FN[j] == 'BAT':
                        if list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            np_CrossCorrelation[i,j] = 1
                        elif (list_Type[i] == 'AIR' or list_Type[i] == 'PRO') and list_Type[j]=='AIR':
                            np_CrossCorrelation[i,j] = 1
                            
                    # Product j is tubing domes and tips
                    elif list_FN[j] == 'TDT':
                        # Hearing aid LUX {l,R,P}
                        if list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            if list_EarSide[i] == 'L' and list_EarSide[j] == 'L':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                            elif list_EarSide[i] == 'R' and list_EarSide[j] == 'R':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                            elif list_EarSide[i] == 'P' and list_EarSide[j] == 'P':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                        # Hearing aid AIR {l,R,P}
                        elif list_Type[i] == 'AIR' and list_Type[j] == 'AIR':
                            if list_EarSide[i] == 'L' and list_EarSide[j] == 'L':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                            elif list_EarSide[i] == 'R' and list_EarSide[j] == 'R':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                            elif list_EarSide[i] == 'P' and list_EarSide[j] == 'P':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                        # Hearing aid CONTROL {l,R,P} - does not have special TBT for this product
                        elif list_Type[i] == 'CONTROL':
                            if list_EarSide[i] == 'L' and list_EarSide[j] == 'L':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.95,1)
                            elif list_EarSide[i] == 'R' and list_EarSide[j] == 'R':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.95,1)
                            elif list_EarSide[i] == 'P' and list_EarSide[j] == 'P':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.95,1)
                        # Hearing aid PRO {O,P} - does not have special TBT for this product
                        elif list_Type[i] == 'PRO' and list_Type[j] == 'PRO':
                            if list_EarSide[i] == 'O' and list_EarSide[j] == 'L':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                            elif list_EarSide[i] == 'O' and list_EarSide[j] == 'R':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                            elif list_EarSide[i] == 'P' and list_EarSide[j] == 'P':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                            elif (list_EarSide[i] == 'O' or list_EarSide[i] == 'P') and list_EarSide[j] == None:
                                np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                                

                    # Product j is a protection plan
                    elif list_FN[j] == 'PP': 
                        # AIR protection plan
                        if list_ProtectionPlan[i] == 'AIR' and list_Type[j] == 'AIR' and list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 1
                        # LUX protection plan
                        if list_ProtectionPlan[i] == 'LUX' and list_Type[j] == 'LUX' and list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 1
                        # CONTROL protection plan
                        if list_ProtectionPlan[i] == 'CONTROL' and list_Type[j] == 'CONTROL' and list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 1
                        # PRO protection plan
                        if list_ProtectionPlan[i] == 'PRO' and list_Type[j] == 'PRO' and list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 1
                
                
                ### PRODUCT i IS A BATTERY ###
                elif list_FN[i] == 'BAT':
                    # Product j is hearing aid
                    if list_FN[j] == 'HA':
                        np_CrossCorrelation[i,j] = 0
                        
                    # Product j is a battery    
                    elif list_FN[j] == 'BAT':
                        np_CrossCorrelation[i,j] = 0
                        
                    # Product j is an accesoire    
                    elif list_FN[j] == 'ACC':
                        np_CrossCorrelation[i,j] = np.random.uniform(0.8,1,1)
                    
                    # Product j is tubing domes and tips    
                    elif list_FN[j] == 'TDT':
                        if list_Type[i] == 'AIR' and (list_Type[j] == 'AIR' or list_Type[j] == 'PRO'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,1,1)
                        elif list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,1,1)
                            
                    # Product j is a Protection plan
                    elif list_FN[j] == 'PP':
                        if list_Type[i] == 'AIR' and (list_Type[j] == 'AIR' or list_Type[j] == 'PRO'):
                            if list_EarSide[j] != 'P':
                                np_CrossCorrelation[i,j] = 0
                        elif list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            if list_EarSide[j] != 'P':
                                np_CrossCorrelation[i,j] = 0
                
                
                ### PRODUCT i IS AN ACCESSOIRE ###
                elif list_FN[i] == 'ACC':
                    
                    if list_FN[j] == 'HA':
                        np_CrossCorrelation[i,j] = 0
                        
                    elif list_FN[j] == 'BAT':
                        np_CrossCorrelation[i,j] = np.random.uniform(0.4,0.9,1)
                        
                    elif list_FN[j] == 'ACC':
                        np_CrossCorrelation[i,j] = np.random.uniform(0.85,1,1)
                        
                    elif list_FN[j] == 'TDT':
                        np_CrossCorrelation[i,j] = np.random.uniform(0.4,0.9,1)
                        
                    elif list_FN[j] == 'PP':
                        if list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 0
                
                
                ### PRODUCT i IS A TUBING DOME AND TIPS ###
                elif list_FN[i] == 'TDT':
                    if list_FN[j] == 'HA':
                        np_CrossCorrelation[i,j] = 0
                        
                    elif list_FN[j] == 'BAT':
                        if list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                        elif (list_Type[i] == 'AIR' or list_Type[i] == 'PRO') and list_Type[j] == 'AIR':
                            np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            
                    elif list_FN[j] == 'ACC':
                        np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                    
                    elif list_FN[j] == 'TDT':
                        if i == j:
                            np_CrossCorrelation[i,j] = 0
                        elif list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            if list_EarSide[i] == 'L' and list_EarSide[j] == 'L':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            elif list_EarSide[i] == 'R' and list_EarSide[j] == 'R':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            elif list_EarSide[i] == 'P' and list_EarSide[j] == 'P':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                        elif list_Type[i] == 'PRO' and list_Type[j] == 'PRO':
                            if list_EarSide[i] == 'L' and list_EarSide[j] == 'L':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            elif list_EarSide[i] == 'R' and list_EarSide[j] == 'R':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            elif list_EarSide[i] == 'P' and list_EarSide[j] == 'P':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                        elif list_Type[i] == 'AIR' and list_Type[j] == 'AIR':
                            if list_EarSide[i] == 'L' and list_EarSide[j] == 'L':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            elif list_EarSide[i] == 'R' and list_EarSide[j] == 'R':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            elif list_EarSide[i] == 'P' and list_EarSide[j] == 'P':
                                np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                    
                    elif list_FN[j] == 'PP':
                        if list_Type[i] == 'AIR' and list_Type[j] == 'AIR':
                            if (list_EarSide[i] == 'L' or list_EarSide[i] == 'R') and list_EarSide[j] != 'P':
                                np_CrossCorrelation[i,j] = 0
                        elif list_Type[i] == 'PRO' and list_Type[j] == 'PRO':
                            if (list_EarSide[i] == 'L' or list_EarSide[i] == 'R') and list_EarSide[j] != 'P':
                                np_CrossCorrelation[i,j] = 0
                        elif list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            if (list_EarSide[i] == 'L' or list_EarSide[i] == 'R') and list_EarSide[j] != 'P':
                                np_CrossCorrelation[i,j] = 0
    

                ### PRODUCT i IS A PROTECTION PLAN ###
                elif list_FN[i] == 'PP':
                    if list_FN[j] == 'HA':
                        np_CrossCorrelation[i,j] = 0
                        
                    elif list_FN[j] == 'BAT':
                        if list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                        elif list_Type[j] == 'AIR' and (list_Type[j] == 'AIR'or list_Type[j] == 'PRO'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                        elif list_Type[j] == 'PRO' and (list_Type[j] == 'AIR'or list_Type[j] == 'PRO'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1) 
                        elif list_Type[j] == 'CONTROL':
                            np_CrossCorrelation[i,j] = np.random.uniform(0.4,0.8,1)
                            
                    elif list_FN[j] == 'ACC':
                        np_CrossCorrelation[i,j] = np.random.uniform(0.75,0.95,1)
                        
                    elif list_FN[j] == 'TDT':
                        if list_EarSide[i] != 'P':
                            if list_EarSide[j] != 'P':
                                if list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                                if list_Type[i] == 'AIR' and list_Type[j] == 'AIR':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                                if list_Type[i] == 'PRO' and list_Type[j] == 'PRO':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                                if list_Type[i] == 'CONTROL':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                        elif list_EarSide[i] == 'P':
                            if list_EarSide[j] == 'P':
                                if list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                                if list_Type[i] == 'AIR' and list_Type[j] == 'AIR':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                                if list_Type[i] == 'PRO' and list_Type[j] == 'PRO':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                                if list_Type[i] == 'CONTROL':
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                                    
                    elif list_FN[j] == 'PP':
                        np_CrossCorrelation[i,j] = 0

    # For backend AN Direct - transpose correlations
    np_CrossCorrelationT = np_CrossCorrelation.T

    ### Store results ###
    df_CrossCorrelation = pd.DataFrame(np_CrossCorrelation)
    # df_CrossCorrelation.to_csv("CrossCorrelationsFIRST.csv")
    df_CrossCorrelation.to_csv(output_path + ".csv")


def get_result(input_path, output_path):
    return main(input_path, output_path)
