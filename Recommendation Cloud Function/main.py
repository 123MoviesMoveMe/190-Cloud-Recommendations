def getRecommendation(request):
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',#'http://127.0.0.1:5500'
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            #'Access-Control-Allow-Credentials': 'true',

            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }


    import pickle
    import pandas as pd
    import torch
    import numpy as np
    import torch.nn as nn
    from google.cloud import storage

    from pytorch_lightning import LightningModule
    from localpackage import NCF
    from localpackage import getUserRecommendationsShort
    import sys
    from flask import jsonify
    
    request_json = request.get_json()

    if request_json and "movies" in request_json: 

        # Load all files from storage bucket storage and instantiate
        storage_client = storage.Client()

        bucket = storage_client.bucket('software-engineering-7af33.appspot.com')


        blob = bucket.blob('usersList')
        pickle_in = blob.download_as_string()
        users = pickle.loads(pickle_in)

        blob = bucket.blob('moviePool')
        pickle_in = blob.download_as_string()
        moviePool = pickle.loads(pickle_in)

        blob = bucket.blob('links.pickle')
        pickle_in = blob.download_as_string()
        links = pickle.loads(pickle_in)

        blob = bucket.blob('movieTitles.pickle')
        pickle_in = blob.download_as_string()
        movieTitles = pickle.loads(pickle_in)

        blob = bucket.blob('usersCorrespondingClusters.pkl')
        pickle_in = blob.download_as_string()
        usersCorrespondingClusters = pickle.loads(pickle_in)

        setattr(sys.modules["__main__"],'NCF',NCF)
        blob = bucket.blob('NCFRecommender1.pkl')
        pickle_in = blob.download_as_string()
        model = pickle.loads(pickle_in)

        medoidUsers = [88501, 26432, 94491, 66265, 16124, 122988, 20649, 95986, 120838, 2745]

        # get user input and get Recommendations
        usersMovies = request_json["movies"]

        recommendations = getUserRecommendationsShort(usersMovies,model,users,moviePool, links,movieTitles, usersCorrespondingClusters, medoidUsers)

        if recommendations == "tt0000000":
            return jsonify({"problem":"No user movies match the models movies"}),200,headers
        return jsonify({"movies":recommendations}),200, headers
    
    return jsonify({"problem":"No movies were received to make a recommendation"}), 200, headers