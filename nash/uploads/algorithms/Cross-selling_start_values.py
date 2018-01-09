# -*- coding: utf-8 -*-
# Your imports here
from . import api_connection
import pandas as pd
import numpy as np
import os


"""
# API
    Array 'execute_data' contain: 
    {
        'host_api'
        'client_id',
        'client_secret',
        'url_token',
        'user_agent',
        'output_name'
    }

# FILE
    Array 'execute_data' contain:
    {
        'input_path',
        'output_path'
    }

"""

# Can be 'API' or 'FILE'
EXECUTE_TYPE = 'API'

def main(execute_data):
    # Your algorithm here
    # In the end, you need to 'return True'


    #==============================================================================
    #                           NEEDED FOR API CONNECTION
    #==============================================================================
    # General needed for API connection
    url_token = execute_data['url_token']
    client_id = execute_data['client_id']
    client_secret = execute_data['client_secret']
    user_agent = execute_data['user_agent']
    
    # Needed urls
    url_Products = execute_data['host_api'] + '/v1/products?limit=all&fields=id,title,functionalNameId,visible,brandId,urlCode'
    url_Brands = execute_data['host_api'] + '/v1/brands?limit=all&fields=id,urlCode'
    url_FunctionalNames = execute_data['host_api'] + '/v1/functionalnames?limit=all&fields=id,title'
    url_ProductAttributeValues = execute_data['host_api'] + '/v1/productattributevalues/by?or=[{"attributeId":{"e":["29","26"]}}]&limit=all&fields=productId,value,attributeId'


    #==============================================================================
    #                               PRODUCT - API
    #==============================================================================
    # API Connection
    data = api_connection.API_GET(url_token, client_id, client_secret, user_agent, url_Products)
    list_Data = data['data']
    
    
    # Get data from dictionary
    list_ProductIds = [None]*len(list_Data) 
    list_Title = [None]*len(list_Data)
    list_urlCode = [None]*len(list_Data)
    list_BrandId = [None]*len(list_Data)
    list_FunctionalNameId = [None]*len(list_Data)
    list_urlCode = [None]*len(list_Data)
    list_Visible = [None]*len(list_Data)
    
    for index in range(0, len(list_Data)):
        data = list_Data[index]
        attributes = data['attributes']
         
        list_ProductIds[index] = int(attributes['id'])
        list_Title[index] = str(attributes['title'])
        list_urlCode[index] = str(attributes['urlCode'])
        list_BrandId[index] = int(attributes['brandId'])
        list_FunctionalNameId[index] = int(attributes['functionalNameId'])
        list_Visible[index] = int(attributes['visible'])
    
    
    # Make dataframe    
    df_Products = pd.DataFrame([list_ProductIds, list_Title, list_urlCode, list_BrandId, list_FunctionalNameId, list_Visible])    
    df_Products = df_Products.T
    df_Products.columns = ['ID', 'Title', 'URL code', 'Brand', 'Functional name', 'Visible']
    
    
    
    #==============================================================================
    #                               BRANDS - API
    #==============================================================================
    # API Connection
    data = api_connection.API_GET(url_token, client_id, client_secret, user_agent, url_Brands)
    list_Data = data['data']
    
    
    # Get data from dictionary
    list_IDs = [None]*len(list_Data) 
    list_urlCode = [None]*len(list_Data)
    
    for index in range(0, len(list_Data)):
        data = list_Data[index]
        attributes = data['attributes']
         
        list_IDs[index] = int(attributes['id'])
        list_urlCode[index] = str(attributes['urlCode'])
    
    
    # Make dataframe       
    df_Brands = pd.DataFrame([list_IDs, list_urlCode])    
    df_Brands = df_Brands.T
    df_Brands.columns = ['ID', 'urlCode']
    
    
    
    #==============================================================================
    #                         FUNCTIONAL NAMES - API
    #==============================================================================
    # API Connection
    data = api_connection.API_GET(url_token, client_id, client_secret, user_agent, url_FunctionalNames)
    list_Data = data['data']
    
    
    # Get data from dictionary
    list_IDs = [None]*len(list_Data) 
    list_Title = [None]*len(list_Data)
    
    for index in range(0, len(list_Data)):
        data = list_Data[index]
        attributes = data['attributes']
         
        list_IDs[index] = int(attributes['id'])
        list_Title[index] = str(attributes['title'])
    
    
    # Make dataframe       
    df_FunctionalNames = pd.DataFrame([list_IDs, list_Title])    
    df_FunctionalNames = df_FunctionalNames.T
    df_FunctionalNames.columns = ['ID', 'Title']
    
    
    
    #==============================================================================
    #                         PRODUCT ATTRIBUTE VALUES - API
    #==============================================================================
    # API Connection
    data = api_connection.API_GET(url_token, client_id, client_secret, user_agent, url_ProductAttributeValues)
    list_Data = data['data']
    
    
    # Get data from dictionary
    list_AttributeId = [None]*len(list_Data) 
    list_ProductId = [None]*len(list_Data)
    list_Value = [None]*len(list_Data)
    
    for index in range(0, len(list_Data)):
        data = list_Data[index]
        attributes = data['attributes']
         
        list_AttributeId[index] = int(attributes['attributeId'])
        list_ProductId[index] = int(attributes['productId'])
        list_Value[index] = str(attributes['value'])
    
    
    # Make dataframe       
    df_ProductAttributeValues = pd.DataFrame([list_AttributeId, list_ProductId, list_Value])    
    df_ProductAttributeValues = df_ProductAttributeValues.T
    df_ProductAttributeValues.columns = ['AttributeId', 'ProductId', 'Value']
    
    
    
    #==============================================================================
    #                       DF_PRODUCTS: IDS TO VALUES
    #==============================================================================
    ## BRANDS
    df_Brands.sort_values('ID', inplace=True, ascending=True)
    df_Brands = df_Brands.reset_index(drop=True)
    
    # Brands in products
    unique,pos = np.unique(np.asarray(df_Products.Brand),return_inverse=True) #Finds all unique elements and their positions
    
    list_BrandValue = []
    for index in pos:
        list_BrandValue.append(df_Brands.ix[index,'urlCode'])
        
    df = pd.DataFrame(list_BrandValue)      
    df.columns = ['name']  
    df_Products['Brand'] = df['name']
    
     
    
    ## FUNCTIONAL NAMES
    df_FunctionalNames.sort_values('ID', inplace=True, ascending=True)
    df_FunctionalNames = df_FunctionalNames.reset_index(drop=True)
    
    # Brands in products
    unique,pos = np.unique(np.asarray(df_Products['Functional name']), return_inverse=True) #Finds all unique elements and their positions
    
    list_temp = []
    for index in pos:
        list_temp.append(df_FunctionalNames.ix[index,'Title'])    
        
    df = pd.DataFrame(list_temp)      
    df.columns = ['name']  
    df_Products['Functional name'] = df.name 
    
    
    
    #==============================================================================
    #                   ADD PRODUCT ATTRIBUTE VALUE TO PRODUCTS
    #==============================================================================
    ### Pivot product attribute values
    df_ProductAttributeValues = df_ProductAttributeValues.pivot(index='ProductId', columns = 'AttributeId', values = 'Value' )
    df_ProductAttributeValues.reset_index(level=0, inplace=True)
    df_ProductAttributeValues.columns = ['ProductId', 'EarSide', 'Add Protection Plan']
    
    # Get productids - subset
    list_PID = df_ProductAttributeValues.ProductId.tolist() # product ids 
    
    # Get productids - whole set
    list_ProductIds = df_Products.ID.tolist()
    
    # Create new dataframe to get right values 
    np_empty  = np.empty((len(list_ProductIds),len(df_ProductAttributeValues.columns)))
    np_empty[:] = np.nan
    df = pd.DataFrame(np_empty)
    df.columns = ['ProductId', 'EarSide', 'Add Protection Plan']
    df.ProductId = list_ProductIds 
    
    # Loop to fill dataframe
    for i in range(0,len(list_ProductIds)):
        if list_ProductIds[i] in list_PID:
            ind = list_PID.index(list_ProductIds[i])
            df.ix[i,'EarSide'] = df_ProductAttributeValues.ix[ind,'EarSide']
            df.ix[i,'Add Protection Plan'] = df_ProductAttributeValues.ix[ind,'Add Protection Plan']
    
    # Append temporary df
    df_Products = df_Products.join([df.iloc[:,1], df.iloc[:,2]])
    
    df = df_Products
    
    
    
    #==============================================================================
    #                           CROSS CORRELATIONS
    #==============================================================================
    
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
    list_word = ['pro', 'air', 'lux', 'control', 'core']
    
    for i in range(0,len(df)):
        for word in list_word: 
            if word in str(list_df_URLCode[i]):
                list_Type[i] = word[:].upper()
        
    
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
    
    
    # add protection plan values into EarSidelist
    for i in range(0,len(list_FN)):
        if list_FN[i] == 'PP':
            if '2' in df_Products.Title[i]:
                list_EarSide[i] = 'P'  
                
    
    # Protection plan
    list_ProtectionPlan = [None]*len(df)
    list_df_ProtectionPlan = (df.loc[:,'Add Protection Plan']).tolist()
    
    for i in range(0,len(df)):
        if list_FN[i] == 'HA' and 'Included' in str(list_df_ProtectionPlan[i]):
            list_ProtectionPlan[i] = 0
        elif list_FN[i] == 'HA' and 'Included' not in str(list_df_ProtectionPlan[i]):
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
            # Check row element with each column element
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
                        if df.Title[j] == 'UV Clean and Dry Box':
                            np_CrossCorrelation[i,j] = 1
                        else:
                            np_CrossCorrelation[i,j] = np.random.uniform(0.8,0.95,1)
                        
                    # Product j is battery
                    elif list_FN[j] == 'BAT':
                        if (list_Type[i] == 'LUX' or list_Type[i]== 'CORE') and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
                            np_CrossCorrelation[i,j] = 1
                        elif (list_Type[i] == 'AIR' or list_Type[i] == 'PRO') and (list_Type[j]=='AIR' or list_Type[j] == 'PRO'):
                            np_CrossCorrelation[i,j] = 1
                             
                    # Product j is tubing domes and tips
                    elif list_FN[j] == 'TDT':
                        # Hearing aid LUX {l,R,P} and CORE
                        if (list_Type[i] == 'LUX' or list_Type[i] == 'CORE') and list_Type[j] == 'LUX':
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
                        elif list_ProtectionPlan[i] == 'LUX' and list_Type[j] == 'LUX' and list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 1
                        # CONTROL protection plan
                        elif list_ProtectionPlan[i] == 'CONTROL' and list_Type[j] == 'CONTROL' and list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 1
                        # PRO protection plan
                        elif list_ProtectionPlan[i] == 'PRO' and list_Type[j] == 'PRO' and list_EarSide[j] != 'P':
                            np_CrossCorrelation[i,j] = 1
                        # CORE protection plan
                        elif list_ProtectionPlan[i] == 'CORE' and list_Type[j] == 'CORE':
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
                        elif list_Type[i] == 'LUX' and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,1,1)
                            
                    # Product j is a Protection plan
                    elif list_FN[j] == 'PP':
                        if (list_Type[i] == 'AIR' or list_Type[i] == 'PRO') and (list_Type[j] == 'AIR' or list_Type[j] == 'PRO'):
                            if list_EarSide[j] != 'P':
                                np_CrossCorrelation[i,j] = 0
                        elif (list_Type[i] == 'LUX' or list_Type[i] == 'CORE') and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
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
                        if (list_Type[i] == 'LUX' or list_Type[i] == 'CORE') and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                        elif (list_Type[i] == 'AIR' or list_Type[i] == 'PRO') and (list_Type[j] == 'AIR' or list_Type[j] == 'PRO'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.6,0.9,1)
                            
                    elif list_FN[j] == 'ACC':
                        np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                    
                    elif list_FN[j] == 'TDT':
                        if i == j:
                            np_CrossCorrelation[i,j] = 0
                        elif list_Type[i] == 'LUX' and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
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
                        elif list_Type[i] == 'LUX' and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
                            if (list_EarSide[i] == 'L' or list_EarSide[i] == 'R') and list_EarSide[j] != 'P':
                                np_CrossCorrelation[i,j] = 0
     
    
                ### PRODUCT i IS A PROTECTION PLAN ###
                elif list_FN[i] == 'PP':
                    if list_FN[j] == 'HA':
                        np_CrossCorrelation[i,j] = 0
                    
                    # Product j is battery
                    elif list_FN[j] == 'BAT':
                        if list_Type[i] == 'LUX' and list_Type[j] == 'LUX':
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                        elif list_Type[i] == 'AIR' and (list_Type[j] == 'AIR'or list_Type[j] == 'PRO'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1)
                        elif list_Type[i] == 'PRO' and (list_Type[j] == 'AIR'or list_Type[j] == 'PRO'):
                            np_CrossCorrelation[i,j] = np.random.uniform(0.7,0.95,1) 
                        elif list_Type[i] == 'CONTROL':
                            np_CrossCorrelation[i,j] = np.random.uniform(0.4,0.8,1)
                        elif list_Type[i] == 'CORE' and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
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
                                if list_Type[i] == 'CORE' and (list_Type[j] == 'LUX' or list_Type[j] == 'CORE'):
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
                                if list_Type[i] == 'CORE' and (list_Type[j] == 'CORE' or list_Type[j] == 'LUX'):
                                    np_CrossCorrelation[i,j] = np.random.uniform(0.7,0,95,1)
                                    
                    elif list_FN[j] == 'PP':
                        np_CrossCorrelation[i,j] = 0
    
    
    # Store in dataframe
    df_CrossCorrelation = pd.DataFrame(np_CrossCorrelation)

    # Write to csv file
    df_CrossCorrelation.to_csv(execute_data['output_name'])


def get_result(data):
    return main(data)