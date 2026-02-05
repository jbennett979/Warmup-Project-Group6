import firebase_admin
from firebase_admin import credentials, firestore

# Accessing service key to allow changes to be made to firestore project
# DO NOT ADD SERVICEACCOUNT TO REPO
def authenticate():
    cred = credentials.Certificate("serviceAccount.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db
