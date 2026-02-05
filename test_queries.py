import authentication

db = authentication.authenticate()

collection_ref = db.collection("Women in Software Engineering")

query = collection_ref.where('company', '==', 'GitHub')

results = query.stream()
# print(query)

for doc in results:
    print(f'{doc.id} => {doc.to_dict()}')