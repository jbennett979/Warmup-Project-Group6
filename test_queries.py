import authentication

db = authentication.authenticate()
collection_ref = db.collection("Women in Software Engineering")

parsed_query = ['company', '==', 'GitHub']

query = collection_ref.where(*parsed_query).stream()

for doc in query:
    print(f'{doc.id} => {doc.to_dict()}')