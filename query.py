import pyparsing as pp
import authentication


# main function
# runs for how ever many queries user wants untill enter 'quit'
def main():
    send_query()


# a function that allows the user to query then parses for input validation
def get_query():
    # defining the tokens/patterns to be matched
    string_cols = pp.oneOf("Company Team Last_updated")
    num_cols = pp.oneOf("Num_female Num_eng Percent")
    num_operators = pp.oneOf("== > < >= <= for")
    string_operators = pp.oneOf("== for")
    quotes = pp.QuotedString('"')
    integer = pp.Word(pp.nums)
    day = pp.Word(pp.nums, min=1, max=2)
    month = pp.Word(pp.nums, min=1, max=2)
    year = pp.Word(pp.nums, min=4, max=4)
    date = pp.Combine(month + pp.Literal("/") + day + pp.Literal("/") + year)
    and_or = pp.oneOf("and or")
    help = pp.CaselessKeyword('help')
    quit = pp.CaselessKeyword('quit')
    detail = pp.Optional(pp.CaselessKeyword('detail'))
    show = pp.Optional(pp.CaselessKeyword('show') + integer)
    sort = pp.Optional(pp.oneOf("asc desc"))

    value = quotes | date

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
            parsed_query = query.parseString(user_query)
            print("yay")
            print(parsed_query)
            return parsed_query
        except pp.ParseException:
            print(f"{user_query} is not a valid query. Please refer to the help or try again.")


# TODO: a function that takes in the parsed tokens, and interacts with the data
def send_query():
    parsed_query = get_query()

    # an query
    if 'and' in parsed_query:
        left_query = parsed_query[:3]
        right_query = parsed_query[4:]

    # collection_ref = db.collection("Women in Software Engineering")
    # query = collection_ref.where(filter=FieldFilter(parsed_query))
    print(query)


if __name__ == "__main__":
    main()