# -*- coding: utf-8 -*-
"""
Created on Tue May 30 09:36:46 2017

Function: connect with API to exchange token and data

@author: Monique
"""



def API_GET(url_token, client_id, client_secret, user_agent, url_API):  
    
    import requests
    
    ### POST Request ###
    # Set up
    parameters = {'client_id':client_id, 'client_secret':client_secret}
    head = {'User-Agent':user_agent}

    # Post request
    response_post = requests.post(url=url_token,params=parameters,headers=head)

    # Store token string
    dictionary = response_post.json()
    data_post = dictionary['data']
    data_dict_post = data_post[0]
    token_string = data_dict_post['token']


    ### GET Request ###
    # Define parameters + head
    parameters = {'client_id':client_id, 'client_secret':client_secret}
    head2 = {'User-Agent':user_agent, 'Authorization': 'Bearer '+ token_string}

    # GET requist for getting the 
    response_get = requests.get(url = url_API, params = parameters, headers = head2)
    dictionary_get = response_get.json()
    
    return dictionary_get



def API_POST(url_token, client_id, client_secret, user_agent, url_API, data):  
    
    import requests
    
    ### POST Request ###
    # Set up
    parameters = {'client_id':client_id, 'client_secret':client_secret}
    head = {'User-Agent':user_agent}

    # Post request
    response_post = requests.post(url=url_token,params=parameters,headers=head)

    # Store token string
    dictionary = response_post.json()
    data_post = dictionary['data']
    data_dict_post = data_post[0]
    token_string = data_dict_post['token']


    ### POST Request ###
    # Define parameters + head
    parameters = {'client_id':client_id, 'client_secret':client_secret}
    head2 = {'User-Agent':user_agent, 'Authorization': 'Bearer '+ token_string}

    # GET requist for getting the 
    response_post = requests.post(url = url_API, params = parameters, headers = head2)