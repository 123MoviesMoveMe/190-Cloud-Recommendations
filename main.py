def getRecommendations(request):
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
    
    request_json = request.get_json()

    if request_json and "movies" in request_json:
        #cloud storage       
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

        # get user input and get Recommendations
        usersMovies = request_json["movies"]

        setattr(sys.modules["__main__"],'NCF',NCF)
        blob = bucket.blob('NCFRecommender1.pkl')
        pickle_in = blob.download_as_string()
        model = pickle.loads(pickle_in)

        cloudTestMovies = getUserRecommendationsShort(usersMovies,model,users,moviePool, links,movieTitles)
        #cloudTestMovies =["tt0000000","tt0000001",modelProof]
        #usersMovies.extend(cloudTestMovies)
        if cloudTestMovies == "tt0000000":
            return "No user movies match the models movies"
        else:
            resultResponse = ",".join(cloudTestMovies)
        return resultResponse
    
    return "missing movies"
    

"""Responds to any HTTP request.
Args:
    request (flask.Request): HTTP request object.
Returns:
    The response text or any set of values that can be turned into a
    Response object using
    `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
"""
"""
from google.cloud import storage

storage_client = storage.Client()

bucket = storage_client.bucket('your-gcs-bucket')
blob = bucket.blob('dictionary.pickle')
pickle_in = blob.download_as_string()
my_dictionary = pickle.loads(pickle_in)

"""




"""
   request_json = request.get_json(silent=True)
   request_args = request.args

   if request_json and 'name' in request_json:
       name = request_json['name']
   elif request_args and 'name' in request_args:
       name = request_args['name']
   else:
       name = 'World'
   return 'Hello {}!'.format(name)
   """