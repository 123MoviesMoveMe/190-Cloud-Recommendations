gcloud functions deploy get-recommendations --gen2 --region=us-east4 --runtime=python39 --source=. --entry-point=getRecommendations --trigger-http --memory=512 --verbosity=info