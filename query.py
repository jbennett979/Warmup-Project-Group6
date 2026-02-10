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
    num_operators = pp.one_of("== > < >= <= for")
    string_operators = pp.one_of("== for")
    quotes = pp.QuotedString('"')
    integer = pp.Word(pp.nums)
    day = pp.Word(pp.nums, min=1, max=2)
    month = pp.Word(pp.nums, min=1, max=2)
    year = pp.Word(pp.nums, min=4, max=4)
    date = pp.Combine(month + pp.Literal("/") + day + pp.Literal("/") + year)
    and_or = pp.one_of("and or")
    help = pp.CaselessKeyword('help')
    quit = pp.CaselessKeyword('quit')
    detail = pp.Optional(pp.CaselessKeyword('detail'))
    show = pp.Optional(pp.CaselessKeyword('show') + integer)
    sort = pp.Optional(pp.one_of("asc desc"))

    value = quotes | date # dates with single digits type like "1/1/2016" not "01/01/2016", note in help

    num_comparison = num_cols + num_operators + integer
    string_comparison = string_cols + string_operators + value
    comparison = num_comparison | string_comparison
    more_than_one = comparison + and_or + comparison
    help_query = help
    quit_query = quit

    query = (
            more_than_one + sort + detail + show |
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

    try:
        parsed_query = get_query()
        query = collection_ref

        # simple query
        if all(item not in parsed_query for item in ['and', 'or']):
            # if no optionals
            if 'for' not in parsed_query:
                query = query.where(*parsed_query)

            else:
                pass

            # if at least one optional
            if any(item in parsed_query for item in ['detail', 'show', 'asc', 'desc']):
                subquery = parsed_query[:3]
                optionals = parsed_query[3:]


        # compound query
        else:
            subquery1 = parsed_query[:3]
            # if no optionals
            if all(item not in parsed_query for item in ['detail', 'show', 'asc', 'desc']):
                subquery2 = parsed_query[4:]
            # if at least one optional
            else:
                subquery2 = parsed_query[4:7]
                optionals = parsed_query[7:]

            # and query
            if 'and' in parsed_query:
                pass

            # or query
            else:
                pass

        # convert query result to list of dictionaries
        result_list = [doc.to_dict() for doc in query.stream()]

        # put cols in correct order since queries return cols in random order
        col_order = [col for col in cols if col in result_list[0].keys()]
        ordered_list = [{key: row[key] for key in col_order} for row in result_list]

        # print results in grid
        print(tabulate(ordered_list, headers="keys", tablefmt="grid"))

    except IndexError:
        print("No rows returned by this query.")
    except Exception as error:
        print("An exception occurred:")
        print(f"Exception Type: {type(error).__name__}")
        print(f"Exception Message: {error}")

if __name__ == "__main__":
    main()