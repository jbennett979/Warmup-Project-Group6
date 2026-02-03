import firebase_admin
from firebase_admin import credentials, firestore
import json


# Accessing service key to allow changes to be made to firestore project
# DO NOT ADD SERVICEACCOUNT TO REPO
cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)

def delete_collection(coll_ref, batch_size):
    if batch_size == 0:
        return

    docs = coll_ref.list_documents(page_size=batch_size)
    deleted = 0

    for doc in docs:
        print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
        doc.delete()
        deleted = deleted + 1

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)

def upload_json():
    with open('women_in_software_engineering_stats.json', 'r') as json_file:
        data = json.load(json_file)
    return data


def upload_content(data):

    # Variable to access database from firestore
    db = firestore.client()

    collection_ref = db.collection("Women in Software Engineering")

    delete_collection(collection_ref, 500)

    for entry in data:
        collection_ref.add(entry)

data = upload_json()
upload_c
