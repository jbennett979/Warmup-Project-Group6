import firebase_admin
from firebase_admin import credentials, firestore

# Accessing service key to allow changes to be made to firestore project
# DO NOT ADD SERVICEACCOUNT TO REPO
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

# Variable to access database from firestore
db = firestore.client()

# TODO: Send women_in_software_engineering_stats.json to database