import authentication

db = authentication.authenticate()
collection_ref = db.collection("Women in Software Engineering")

query = collection_ref.where('company', '==', 'GitHub').stream()

for doc in query:
    print(f'{doc.id} => {doc.to_dict()}')