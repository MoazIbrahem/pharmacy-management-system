import re


# Main pattern is => (\d+ char (\d+) char \d+) char => between (day,month) and (month,year)
def Accept_pattern(st):
    """the function check if pattern input from user is correct or no""".title()

    # (  pattern     1    ) (  pattern    2   ) (  pattern    3   ) (  pattern    4   ) (  pattern    5   )
    mypattern = re.search(
        r"^((\d+\\(\d+)\\\d+)|(\d+/(\d+)/\d+)|(\d+#(\d+)#\d+)|(\d+%(\d+)%\d+)|(\d+&(\d+)&\d+))$",
        st,
    )
    if mypattern:
        return True
    else:
        return False


def split_str(st):
    """Splits the date string by recognized separators"""
    chars = ["\\", "/", "#", "%", "&"]
    for i in chars:
        if i in st:
            return str(st).split(i)
    return []


def check_month(month):
    """Validates month and returns its index if valid, otherwise -1."""
    month_int = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    if str(month).isdecimal():
        if int(month) in month_int:
            return month_int.index(int(month))
        else:
            return -1


def check_date(*parameters):
    """Checks if the provided day, month, and year form a valid date."""
    days = ["31", "28", "31", "30", "31", "30", "31", "31", "30", "31", "30", "31"]
    if int(parameters[2]) % 4 == 0:
        days[1] = "29"
    test = check_month(str(parameters[1]).title())
    if test != -1:
        if (
            int(parameters[0]) <= int(days[test])
            and int(parameters[0]) > 0
            and int(parameters[2]) > 0
        ):
            return True
        else:
            return False
    else:
        return False


syntax_ex = f"""  Syntax Of Date
  EX => 6/2/2005
  the char avilable is [\\,/,#,%,&]
  note: all numbers in date must be positive
  """
