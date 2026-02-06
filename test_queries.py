import authentication
from tabulate import tabulate

db = authentication.authenticate()
collection_ref = db.collection("Women in Software Engineering")
col_order = ["company", "team", "num_female_eng", "num_eng", "percent_female_eng", "last_updated"]

parsed_query = ['num_eng', '>=', 0]

query = (collection_ref
         .select(["company", "num_eng"]) # need to specify columns, default prints all (remove line for detail)
         .where(*parsed_query)
         .order_by("num_eng", "DESCENDING") # sort
         .limit(5) # show
         .stream())

result_list = [doc.to_dict() for doc in query]

print(tabulate(result_list, headers="keys", tablefmt="grid")) # firestore doesn't support column ordering
