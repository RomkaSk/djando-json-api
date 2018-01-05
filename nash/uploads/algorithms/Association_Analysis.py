# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 09:57:20 2017

PROJECT: AN Direct

PURPOSE: Association Analysis with ECLAT Algorithm

@author: Monique
"""

# Import packages
import pandas as pd
import numpy as np
import re
import os
from . import api_connection


def main(api_data):
    # Set path
    # path = 'E:\\Projects\\nash-environment\\algorithms'
    # path = 
    # os.chdir(path)

    ###############################################################################
    #                               API CONNECTION                                #
    ###############################################################################

    # Login
    # url_token = 'http://gateway-an.alpha.spheremall.net:8085/v1/oauth/token'
    # client_id = 'monique_client'
    # client_secret = 'DFhj3MDz6GYXdUU34534sdhLKJHw78665Ds'
    # user_agent = 'monique' 

    url_token = api_data['url_token']
    client_id = api_data['client_id']
    client_secret = api_data['client_secret']
    user_agent = api_data['user_agent']

    # Needed urls
    # url_Orders = 'http://gateway-an.alpha.spheremall.net:8085/v1/orders?limit=all'
    # url_OrdersItems = 'http://gateway-an.alpha.spheremall.net:8085/v1/orderitems?limit=all'
    # url_Products = 'http://gateway-an.alpha.spheremall.net:8085/v1/products?limit=all'

    url_Orders = api_data['host_api'] + '/v1/orders?limit=all'
    url_OrdersItems = api_data['host_api'] + '/v1/orderitems?limit=all'
    url_Products = api_data['host_api'] + '/v1/products?limit=all'


    ###############################################################################
    #                               PRODUCT - API                                 #
    ###############################################################################
    # API connection
    data_Orders = api_connection.API_GET(url_token, client_id, client_secret, user_agent, url_Products)
    list_Data = data_Orders['data']

    list_ProductIds = [None]*len(list_Data) 

    for index in range(0, len(list_Data)):
        data = list_Data[index]
        attributes = data['attributes']
        
        if 'id' in attributes: 
            list_ProductIds[index] = int(attributes['id'])
            


    ###############################################################################
    #                               ORDER DATA - API                              #
    ###############################################################################

    # API connection
    data_Orders = api_connection.API_GET(url_token, client_id, client_secret, user_agent, url_Orders)
    print(':::: Api Connection' )
    list_Data = data_Orders['data']

    list_Date = [None]*len(list_Data)    
    list_TID = [None]*len(list_Data)
    list_ItemsAmount = [None]*len(list_Data)
    list_PaymentStatusId = [None]*len(list_Data)
    list_StatusId = [None]*len(list_Data)
    list_UserId = [None]*len(list_Data)
        
    for index in range(0, len(list_Data)):
        data = list_Data[index]
        attributes = data['attributes']
        
        if 'id' in attributes: 
            list_TID[index] = int(attributes['id'])
        if 'updateDate' in attributes:        
            list_Date[index] = str(attributes['updateDate'])
        if 'itemsAmount' in attributes:
            list_ItemsAmount[index] = int(attributes['itemsAmount'])
        if 'paymentStatusId' in attributes:
            list_PaymentStatusId[index] = str(attributes['paymentStatusId'])
        if 'statusId' in attributes:
            list_StatusId[index] = str(attributes['statusId'])
        if 'userId' in attributes:
            list_UserId[index] = str(attributes['userId'])

    
    

    # Create dataframe with all lists 
    df_X = pd.DataFrame([list_Date, list_TID, list_UserId, list_ItemsAmount, list_PaymentStatusId, list_StatusId])
    df_X = df_X.T
    df_X.columns = ['Date', 'TID', 'UserId', 'itemsAmount', 'PaymentStatusId', 'StatusId']

    # Sort on TID
    df_X.sort_values('TID',inplace=True, ascending=True)

    # Only real orders
    df_XG = df_X[(df_X.PaymentStatusId == '2') & (df_X.StatusId == '2')]
    df_XG.index= np.arange(0,len(df_XG))     

    # Needed columns
    list_Right_TID = df_XG['TID'].tolist()
    list_Right_Amount = df_XG['itemsAmount'].tolist()



    ###############################################################################
    #                              ORDER ITEMS - API                              #
    ###############################################################################
    
    # Get data
    data_OrderItems = api_connection.API_GET(url_token, client_id, client_secret, user_agent, url_OrdersItems)
    list_Data = data_OrderItems['data'] 
    print('::::  ORDER ITEMS - API' )
    list_Amount = [None]*len(list_Data)
    list_PID = [None]*len(list_Data)
    list_TID_F = [None]*len(list_Data)

    for index in range(0, len(list_Data)):
        data = list_Data[index]
        attributes = data['attributes']
        
        list_TID_F[index] = int(attributes['orderId'])
        list_PID[index] = str(attributes['productId'])
        list_Amount[index] = int(attributes['amount'])

    # Create dataframe 
    df_OrderItems= pd.DataFrame([list_TID_F, list_Amount, list_PID])
    df_OrderItems = df_OrderItems.T
    df_OrderItems.columns = ['OrderIds', 'Amount', 'ProductIds']



    ###############################################################################
    #                          ORDERS + ORDER ITEMS COMBINED                      #
    ###############################################################################

    list_TPID = [None]*len(df_XG)
    index = 0
    for tid in list_Right_TID:
        list_Products = []
        if tid in list_TID_F:
            ind = [i for i, x in enumerate(list_TID_F) if x == tid]
            for i in range(0,len(ind)):
                list_Products.append(int(list_PID[ind[i]]))
            list_TPID[index] = list_Products
        index += 1

    totalNumberOfOrders = len(list_TPID)



    ###############################################################################
    #             OTHER WAY AROUND: PRODUCTIDS + ORDER IDS COMBINED               #
    ###############################################################################
    #1. Frequent 1-item set
    list_Eclat_PID = []
    list_Eclat_TID = []

    # For transaction ids
    for i in range(0,len(list_Right_TID)):
        # For product in transaction id
        for j in range(0,len(list_TPID[i])):
            if list_TPID[i][j] not in list_Eclat_PID:
                list_Eclat_PID.append(list_TPID[i][j])
                extra = []
                extra.append(list_Right_TID[i])
                list_Eclat_TID.append(extra)
            elif list_TPID[i][j] in list_Eclat_PID:
                ind = list_Eclat_PID.index(list_TPID[i][j])
                list_Eclat_TID[ind].append(list_Right_TID[i])
                
    # Sort by productId
    df_Eclat = pd.DataFrame([list_Eclat_PID,list_Eclat_TID])   
    df_Eclat = df_Eclat.T
    df_Eclat.columns = ['ProductIds', 'TIDs']    
    df_Eclat.sort_values('ProductIds',inplace=True, ascending=True)
    
    list_Eclat_PID = df_Eclat.ProductIds.tolist()
    list_Eclat_TID = df_Eclat.TIDs.tolist()


        
    ###############################################################################
    #                               ECLAT ALGORITHM                               #
    ###############################################################################

    def calculateSupport(TID, totalNumberOfOrders):
        np_Support = np.zeros([len(TID),1])
        for i in range(0,len(TID)):
            np_Support[i] = float(len(TID[i]))/float(totalNumberOfOrders)
            
        return np_Support
        
    def intersect(a, b):
        return list(set(a) & set(b))    

    #2. Calculate Support 
    np_Support = np.zeros([len(list_Eclat_PID),1])
    for i in range(0,len(list_Eclat_PID)):
        np_Support[i] = float(len(list_Eclat_TID[i]))/float(totalNumberOfOrders)

    #3. Make combinations of itemsets (only 2)
    list_Combinations = []
    copy_PID = list_Eclat_PID[:]
    for pid in list_Eclat_PID:
        number = copy_PID.pop(0)
        for productId in copy_PID:
            s = []
            s.append(pid)
            s.append(productId)
            list_Combinations.append(s)

    #4. Make corresponding tid sets for this intersection
    list_Eclat_TID_Revised = []
    list_Combinations_Revised = []
    for combi in list_Combinations:
        a = list_Eclat_PID.index(combi[0])
        b = list_Eclat_PID.index(combi[1])
        list_a = list_Eclat_TID[a]
        list_b = list_Eclat_TID[b]
        intersection = intersect(list_a,list_b)
        if intersection: 
            list_Eclat_TID_Revised.append(intersection)
            list_Combinations_Revised.append(combi)

    #5. Calculate support
    np_Support_Revised = calculateSupport(list_Eclat_TID_Revised, totalNumberOfOrders)

    #6. Calculate confidence
    list_Confidence = []
    for combi in list_Combinations_Revised:
        tel = 0
        a = list_Eclat_PID.index(combi[0])
        b = list_Eclat_PID.index(combi[1])
        conf1 = float(np_Support_Revised[tel]/np_Support[a])
        conf2 = float(np_Support_Revised[tel]/np_Support[b])
        list_Confidence.append(conf1)
        list_Confidence.append(conf2)

    # Make a dataframe of results
    df_CrossCorrelations = pd.DataFrame(np.zeros([len(list_ProductIds), len(list_ProductIds)]))
    df_CrossCorrelations.index = list_ProductIds
    df_CrossCorrelations.columns = list_ProductIds

    for i in range(0,len(list_Combinations_Revised)):
        df_CrossCorrelations.iloc[(list_Combinations_Revised[i][0]-1),(list_Combinations_Revised[i][1]-1)] = list_Confidence[(2*i)]
        df_CrossCorrelations.iloc[(list_Combinations_Revised[i][1]-1),(list_Combinations_Revised[i][0]-1)] = list_Confidence[(2*i+1)]


    # df_CrossCorrelations.to_csv("CrossCorrelations-ECLAT.csv") 
    df_CrossCorrelations.to_csv(api_data['output_name'] + '.csv')


def get_api_result(input_api_data):
    return main(input_api_data)
            
        
