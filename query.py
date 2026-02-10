import pyparsing as pp
import authentication
from tabulate import tabulate
from google.cloud.firestore_v1.base_query import FieldFilter, Or

# main function
# runs for however many queries user wants until enter 'quit'
def main():
    # get_query()
    send_query()


# a function that allows the user to query then parses for input validation
def get_query():
    # defining the tokens/patterns to be matched
    string_cols = pp.one_of("company team last_updated")
    num_cols = pp.one_of("num_female_eng num_eng percent_female_eng")
    num_operators = pp.one_of("== > < >= <=")
    string_operators = pp.one_of("==")
    quotes = pp.QuotedString('"')
    integer = pp.Word(pp.nums).set_parse_action(lambda t: int(t[0]))
    day = pp.Word(pp.nums, min=1, max=2)
    month = pp.Word(pp.nums, min=1, max=2)
    year = pp.Word(pp.nums, min=4, max=4)
    date = pp.Combine(month + pp.Literal("/") + day + pp.Literal("/") + year)
    and_or = pp.one_of("and or")
    help = pp.CaselessKeyword('help')
    quit = pp.CaselessKeyword('quit')
    detail = pp.Optional(pp.CaselessKeyword('detail'))
    show = pp.Optional(pp.CaselessKeyword('show') + integer)
    sort = pp.Optional(pp.one_of("ASCENDING DESCENDING"))

    value = quotes | date # dates with single digits type like "1/1/2016" not "01/01/2016", note in help

    num_comparison = num_cols + num_operators + integer
    string_comparison = string_cols + string_operators + value
    comparison = num_comparison | string_comparison
    more_than_one = comparison + and_or + comparison
    help_query = help
    quit_query = quit

    query = (
            more_than_one + detail + show |
            comparison + sort + detail + show |
            help_query |
            quit_query
    )

    correct_input = False
    while not correct_input:
        user_query = input(">> ")
        try:
            parsed_query = query.parse_string(user_query)
            print("yay")
            print(parsed_query)
            return parsed_query
        except pp.ParseException:
            print(f"{user_query} is not a valid query. Please refer to the help or try again.")


# TODO: a function that takes in the parsed tokens, and interacts with the data
def send_query():
    db = authentication.authenticate()
    collection_ref = db.collection("Women in Software Engineering")
    cols = ["company", "team", "num_female_eng", "num_eng", "percent_female_eng", "last_updated"]

    # try:
    parsed_query = get_query().as_list()
    query = collection_ref

    # simple query
    if 'and' not in parsed_query and 'or' not in parsed_query:
        subquery2 = parsed_query
        new_subquery2 = [subquery2[0], subquery2[1], subquery2[2]]
        select_list = ['company', subquery2[0]]

        query = (query
                 .where(filter=FieldFilter(*new_subquery2))
                 )

    # and query
    elif parsed_query[3] == 'and':
        subquery1 = parsed_query[:3]
        subquery2 = parsed_query[4:]
        new_subquery2 = [subquery2[0], subquery2[1], subquery2[2]]
        select_list = ['company', subquery1[0], subquery2[0]]

        query = (query
                 .where(filter=FieldFilter(*subquery1))
                 .where(filter=FieldFilter(*new_subquery2))
                 )

    # Or query
    else:
        subquery1 = parsed_query[:3]
        subquery2 = parsed_query[4:]
        new_subquery2 = [subquery2[0], subquery2[1], subquery2[2]]
        select_list = ['company', subquery1[0], subquery2[0]]

        query = (query
                 .where(filter=Or([FieldFilter(*subquery1),
                                   FieldFilter(*new_subquery2)
                                   ])))

    # simple query
    # if at least one optional
    if any(item in parsed_query for item in ['ASCENDING', 'DESCENDING', 'detail', 'show']):

        optionals = subquery2[3:]
        # all optionals
        if len(optionals) == 4:
            query = (query
                     .order_by(subquery2[0], optionals[0])
                     .limit(optionals[3])
                     )
        # sort and show
        elif len(optionals) == 3:
            if 'ASCENDING' in optionals or 'DESCENDING' in optionals:
                query = (query
                         .select(select_list)
                         .order_by(subquery2[0], optionals[0])
                         .limit(optionals[2])
                         )
            # detail and show
            else:
                query = (query
                         .limit(optionals[2])
                         )
        elif len(optionals) == 2:
            # show
            if 'show' in optionals:
                query = (query
                         .select(select_list)
                         .limit(optionals[1])
                         )
            # sort and detail
            else:
                query = (query
                         .order_by(subquery2[0], optionals[0])
                         )
        else:
            # sort
            if 'ASCENDING' in optionals or 'DESCENDING' in optionals:
                query = (query
                         .select(select_list)
                         .order_by(subquery2[0], optionals[0])
                         )
            # detail
            else:
                query = query

    else:
        # if no optionals
        query = (query
                 .select(select_list))


    # convert query result to list of dictionaries
    result_list = [doc.to_dict() for doc in query.stream()]

    # put cols in correct order since queries return cols in random order
    col_order = [col for col in cols if col in result_list[0].keys()]
    ordered_list = [{key: row[key] for key in col_order} for row in result_list]

    # print results in grid
    print(tabulate(ordered_list, headers="keys", tablefmt="grid"))

    # except IndexError:
    #     print("No rows returned by this query.")
    # except Exception as error:
    #     print("An exception occurred:")
    #     print(f"Exception Type: {type(error).__name__}")
    #     print(f"Exception Message: {error}")

if __name__ == "__main__":
    main()