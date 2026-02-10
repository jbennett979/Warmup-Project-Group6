import authentication
import json
import sys

# Obtained this delect_collection function from firestore.google.com
# Loops through all the documents of the collection and deletes them
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


def upload_json(json_file):
    with open(str(json_file), 'r') as json_file:
        data = json.load(json_file)
    return data


def upload_content(data):
    # Variable to access database from firestore
    db = authentication.authenticate()

    # Name of collection in firestore
    collection_ref = db.collection("Women in Software Engineering")

    # Deletes anything that was in the collection before
    delete_collection(collection_ref, 500)

    for entry in data:
        collection_ref.add(entry)

# Import json file
json_file = sys.argv[1]
data = upload_json(json_file)
# Upload file content to firestore
upload_content(data)
