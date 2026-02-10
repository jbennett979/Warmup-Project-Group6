import authentication
from tabulate import tabulate
from google.cloud.firestore_v1.base_query import FieldFilter, Or

db = authentication.authenticate()
collection_ref = db.collection("Women in Software Engineering")
cols = ["company", "team", "num_female_eng", "num_eng", "percent_female_eng", "last_updated"]

# simple query with optionals
parsed_query1 = ['percent_female_eng', '>=', 40]
query1 = (collection_ref
         .select(["company", "num_eng"]) # need to specify columns, default prints all (remove line for detail)
         .where(filter=FieldFilter(*parsed_query1))
         .order_by("percent_female_eng", "DESCENDING") # sort
         .limit(5) # show
          )

# compound AND query
parsed_query2 = ["team", "!=", "N/A"]
parsed_query3 = ["num_eng", "<=", 10]
query2 = (collection_ref
          .select(["company", "team", "num_eng"])
          .where(filter=FieldFilter(*parsed_query2))
          .where(filter=FieldFilter(*parsed_query3))
          .order_by("num_eng", "DESCENDING")
          )

# compound OR query
parsed_query4 = ["percent_female_eng", ">=", 40]
query3 = (collection_ref
          .select(["company", "percent_female_eng"])
          .where(filter=Or([FieldFilter(*parsed_query3),
                            FieldFilter(*parsed_query4)
                            ]))
          .order_by("percent_female_eng", "DESCENDING")
          )

parsed_query5 = ["team", "==", "N/A"]
query4 = (collection_ref
          .where(filter=Or([FieldFilter(*parsed_query2),
                            FieldFilter(*parsed_query5)
                            ]))
          .order_by("company", "ASCENDING")
          )

# convert query result to list of dictionaries
result_list = [doc.to_dict() for doc in query2.stream()]

try:
    # put cols in correct order since queries return cols in random order
    col_order = [col for col in cols if col in result_list[0].keys()]
    ordered_list = [{key: row[key] for key in col_order} for row in result_list]

    # print results in grid
    print(tabulate(ordered_list, headers="keys", tablefmt="grid"))

# if query is valid but doesn't return any rows
except IndexError:
    print("No rows returned by this query.")
