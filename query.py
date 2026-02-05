import pyparsing as pp

# a function that allows the user to query then parses for input validation
def get_query():
    #defining the tokens/patterns to be matched
    cols = pp.oneOf("Company Team Num_female Num_eng Percent")
    operators = pp.oneOf("== > < >= <= for")
    quotes = pp.QuotedString('"')
    integer = pp.Word(pp.nums)
    and_or = pp.oneOf("and or")
    help = pp.CaselessKeyword('help')
    quit = pp.CaselessKeyword('quit')
    detail = pp.Optional(pp.CaselessKeyword('detail'))
    show10 = pp.Optional(pp.CaselessKeyword('show10'))

    value = integer | quotes

    comparison = cols + operators + value + detail + show10
    more_than_one = comparison + and_or + comparison
    help_query = help
    quit_query = quit

    query = (
        more_than_one |
        comparison |
        help_query |
        quit_query
    )

    correct_input = False
    while not correct_input:
        user_query = input(">>")
        try:
            parsed_query = query.parseString(user_query)
            print("yay")
            print(parsed_query)
            return parsed_query
        except pp.ParseException:
            print(f"{user_query} is not a valid query. Please refer to the help or try again.")

# TODO: a function that takes in the parsed tokens, and interacts with the data

get_query()