"""CSCA08 Fall 2023 Assignment 1"""


from constants import (YR, MON, DAY, DEP, ARR, ROW, SEAT, FFN,
                       WINDOW, AISLE, MIDDLE, SA, SB, SC, SD, SE, SF)


def get_date(ticket: str) -> str:
    """Return the date of ticket 'ticket' in YYYYMMDD format.

    Precondition: 'ticket' is in valid format.

    >>> get_date('20230915YYZYEG12F')
    '20230915'
    >>> get_date('20240915YYZYEG12F1236')
    '20240915'
    >>> get_date('')
    ''
    """

    return get_year(ticket) + get_month(ticket) + get_day(ticket)


def get_year(ticket: str) -> str:
    """Return the year of ticket 'ticket' in YYYY format.

    Precondition: 'ticket' is in valid format.

    >>> get_year('20230915YYZYEG12F')
    '2023'
    >>> get_year('20240915YYZYEG12F1236')
    '2024'
    >>> get_year('')
    ''
    """

    return ticket[YR:YR + 4]


def get_month(ticket: str) -> str:
    """Return the month of ticket 'ticket' in MM format.

    Precondition: 'ticket' is in valid format.

    >>> get_month('20230915YYZYEG12F')
    '09'
    >>> get_month('20241215YYZYEG12F1236')
    '12'
    >>> get_month('')
    ''
    """

    return ticket[MON:MON + 2]


def get_day(ticket: str) -> str:
    """Return the day of ticket 'ticket' DD format.

    Precondition: 'ticket' is in valid format.

    >>> get_day('20230915YYZYEG12F')
    '15'
    >>> get_day('20241223YYZYEG12F1236')
    '23'
    >>> get_day('')
    ''
    """

    return ticket[DAY:DAY + 2]


def get_departure(ticket: str) -> str:
    """Return the departure airport code of ticket 'ticket'.

    Precondition: 'ticket' is in valid format.

    >>> get_departure('20231221YYZYEG25F4442')
    'YYZ'
    >>> get_departure('20241223YOWYEG12F1236')
    'YOW'
    >>> get_departure('')
    ''
    """

    return ticket[DEP:DEP + 3]


def get_arrival(ticket: str) -> str:
    """Return the arrival airport code of ticket 'ticket'.

    Precondition: 'ticket' is in valid format.

    >>> get_arrival('20231221YYZYEG25F4442')
    'YEG'
    >>> get_arrival('20241223YOWLAS12F1236')
    'LAS'
    >>> get_arrival('')
    ''
    """

    return ticket[ARR:ARR + 3]


def get_row(ticket: str) -> int:
    """Return the row number of ticket 'ticket'.

    Precondition: 'ticket' is in valid format.

    >>> get_row('20231221YYZYEG25F4442')
    25
    >>> get_row('20241223YOWLAS12F1236')
    12
    >>> get_row('')
    ''
    """

    if ticket == '':
        return ''

    return int(ticket[ROW:ROW + 2])


def get_seat(ticket: str) -> str:
    """Return the seat of ticket 'ticket'.

    >>> get_seat('20231221YYZYEG25F4442')
    'F'
    >>> get_seat('20241223YOWLAS12G1236')
    'G'
    >>> get_seat('')
    ''
    """

    if ticket == '':
        return ''

    return ticket[SEAT]


def get_ffn(ticket: str) -> str:
    """Return the frequent flyer number of ticket 'ticket'.

    >>> get_ffn('20231221YYZYEG25F4442')
    '4442'
    >>> get_ffn('20241223YOWLAS12G1236')
    '1236'
    >>> get_ffn('')
    ''
    """

    return ticket[FFN:FFN + 4]


def is_valid_seat(ticket: str, first_row: int, last_row: int) -> bool:
    """Return True if and only if this ticket has a valid seat. That is,
    if the seat row is between 'first_row' and 'last_row', inclusive,
    and the seat is SA, SB, SC, SD, SE, or SF.

    Precondition: 'ticket' is in valid format.

    >>> is_valid_seat('20231221YYZYEG25F4442', 1, 30)
    True
    >>> is_valid_seat('20230915YYZYEG42F1236', 1, 30)
    False
    >>> is_valid_seat('20230915YYZYEG21Q1236', 1, 30)
    False
    >>> is_valid_seat('','','')
    False
    """

    row = get_row(ticket)
    seat = get_seat(ticket)

    if seat == "A" or seat == "B" or seat == "C":
        return first_row <= row <= last_row

    if seat == "D" or seat == "E" or seat == "F":
        return first_row <= row <= last_row

    return False


def is_valid_ffn(ticket: str) -> bool:
    """Return True if the frequent flyer number on the ticket is valid.

    Precondition: 'ticket' is in valid format.

    >>> is_valid_ffn('20231221YYZYEG25F4442')
    True
    >>> is_valid_ffn('20230915YYZYEG32F')
    True
    >>> is_valid_ffn('20230915YYZYEG12H1237')
    False
    >>> is_valid_ffn('')
    False
    """

    if int(len(ticket)) == int(FFN + 4):
        ffn_sum = int(ticket[FFN]) + int(ticket[FFN + 1]) + int(ticket[FFN + 2])

        if ffn_sum % 10 == int(ticket[FFN + 3]):
            return True
    elif len(ticket) == FFN:
        return True
    return False


def is_valid_date(ticket: str) -> bool:
    """Return True if the date on the ticket is valid.

    Precondition: 'ticket' is in valid format.

    >>> is_valid_date('20231231YYZYEG12F1236')
    True
    >>> is_valid_date('20Y30E1IYYZYEG12F1236')
    False
    >>> is_valid_date('20231313YYZYEG12F1236')
    False
    >>> is_valid_date('20230431YYZYEG12F1236')
    False
    >>> is_valid_date('')
    False

    """

    month = get_month(ticket)
    year = get_year(ticket)
    day = get_day(ticket)
    max_days = 31

    if month == '02':
        leap_year = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
        max_days = 29 if leap_year else 28
    elif month == '04' or month == '06' or month == '09' or month == '11':
        max_days = 30
    if year.isdigit() and month.isdigit() and 1 <= int(month) <= 12:
        if day.isdigit() and 1 <= int(day) <= max_days:
            return True

    return False


def is_valid_ticket(ticket: str, first_row: int, last_row: int) -> bool:
    """Return True if the ticket and all its infromation is valid.

    >>> is_valid_ticket('20230915YYZYEG12F1236', 1, 30)
    True
    >>> is_valid_ticket('20230915YYZYEG32F1236', 1, 30)
    False
    >>> is_valid_ticket('20230915YYZYEG12H1236', 1, 30)
    False
    >>> is_valid_ticket('','','')
    False
    """

    return (is_valid_ticket_format(ticket)
            and is_valid_seat(ticket, first_row, last_row)
            and is_valid_ffn(ticket)
            and is_valid_date(ticket))


def visits_airport(ticket: str, airport: str) -> bool:
    """Return True if and only if either departure or arrival airport on
    ticket 'ticket' is the same as 'airport'.

    Precondition: The ticket is valid.

    >>> visits_airport('20230915YYZYEG12F1236', 'YEG')
    True
    >>> visits_airport('20230915YEGYYZ12F1236', 'YEG')
    True
    >>> visits_airport('20230915YYZYEG12F1236', 'YVR')
    False
    >>> visits_airport('', '')
    False
    """

    if ticket == '' or airport == '':
        return False

    return get_departure(ticket) == airport or get_arrival(ticket) == airport


def connecting(ticket1: str, ticket2: str) -> bool:
    """Return True if and only if flight1 arrives in the same airport as the
    departure of flight2 and the dates are the same.

    Precondition: ticket1 and ticket2 are valid tickets.

    >>> connecting('20230915YYZYEG12F1236', '20230915YEGYQB12F1236')
    True
    >>> connecting('20230915YEGYYZ12F1236', '20230915YQBYEG12F1236')
    False
    >>> connecting('20230915YYZYEG12F1236', '20230917YEGYQB12F1236')
    False
    >>> connecting('', '')
    False
    """
    day1 = get_date(ticket1)
    day2 = get_date(ticket2)

    if ticket1 == '' or ticket2 == '':
        return False
    if (get_arrival(ticket1) == get_departure(ticket2) and day1 == day2):
        return True
    return False


def adjacent(ticket1: str, ticket2: str) -> bool:
    """Return True if any only if the seats in tickets 'ticket1' and
    'ticket2' are adjacent (next to each other). Seats across an aisle
    are not considered to be adjacent.

    Precondition: ticket1 and ticket2 are valid tickets.

    >>> adjacent('20230915YYZYEG12D1236', '20230915YYZYEG12E1236')
    True
    >>> adjacent('20230915YYZYEG12B1236', '20230915YYZYEG12A1236')
    True
    >>> adjacent('20230915YYZYEG12C1236', '20230915YYZYEG12D1236')
    False
    >>> adjacent('20230915YYZYEG12A1236', '20230915YYZYEG11B1236')
    False
    >>> adjacent('', '')
    False
    """

    s1 = get_seat(ticket1)  # seat 1
    s2 = get_seat(ticket2)  # seat 2
    r1 = get_row(ticket1)  # row 1
    r2 = get_row(ticket2)  # row 2

    if r1 == r2 and ((s1 == 'A' and s2 == 'B') or (s1 == 'B' and s2 == 'A')):
        return True
    if r1 == r2 and ((s1 == 'B' and s2 == 'C') or (s1 == 'C' and s2 == 'B')):
        return True
    if r1 == r2 and ((s1 == 'D' and s2 == 'E') or (s1 == 'E' and s2 == 'D')):
        return True
    if r1 == r2 and ((s1 == 'E' and s2 == 'F') or (s1 == 'F' and s2 == 'E')):
        return True

    return False


def behind(ticket1: str, ticket2: str) -> bool:
    """Return True if and only if the seats on ticket1 and ticket2 are
    immediately behind one another.

    Precondition: ticket1 and ticket2 are valid tickets.

    >>> behind('20230915YYZYEG11D1236', '20230915YYZYEG12D1236')
    True
    >>> behind('20230915YYZYEG13D1236', '20230915YYZYEG12D1236')
    True
    >>> behind('20230915YYZYEG12C1236', '20230915YYZYEG12B1236')
    False
    >>> behind('20230915YYZYEG12A1236', '20230915YYZYEG14A1236')
    False
    >>> behind('', '')
    False
    """

    if ticket1 == '' or ticket2 == '':
        return False

    difference1 = (int(get_row(ticket1)) - int(get_row(ticket2)))
    difference2 = (int(get_row(ticket2)) - int(get_row(ticket1)))

    if get_seat(ticket1) == get_seat(ticket2):
        if difference1 == 1 or difference2 == 1:
            return True

    return False


def get_seat_type(ticket: str) -> str:
    """Return WINDOW, AISLE, or MIDDLE depending on the type of seat in
    ticket 'ticket'.

    Precondition: 'ticket' is a valid ticket.

    >>> get_seat_type('20230915YYZYEG12F1236')
    'window'
    >>> get_seat_type('20230915YYZYEG08B')
    'middle'
    >>> get_seat_type('20230915YYZYEG12C1236')
    'aisle'
    >>> get_seat_type('')
    ''
    """

    if get_seat(ticket) == 'A' or get_seat(ticket) == 'F':
        return 'window'
    if get_seat(ticket) == 'B' or get_seat(ticket) == 'E':
        return 'middle'
    if get_seat(ticket) == 'C' or get_seat(ticket) == 'D':
        return 'aisle'
    if ticket == '':
        return ''
    return False


def change_seat(ticket: str, row_num: str, seat: str) -> str:
    """Return a ticket with a different row number and seat
    but every other information remains the same.

    Precondition: 'ticket' is a valid ticket.

    >>> change_seat('20230915YYZYEG12F1236', '24', 'B')
    '20230915YYZYEG24B1236'
    >>> change_seat('', '', '')
    ''
    """

    ticket = ticket[: ROW] + row_num + seat + ticket[FFN:]

    return ticket


def change_date(ticket: str, day: str, months: str, year: str) -> str:
    """Return True if and only if either departure or arrival airport on
    ticket 'ticket' is the same as 'airport'.

    Precondition: 'ticket' is a valid ticket.

    >>> change_date('20230915YYZYEG12F1236', '20', '11', '2024')
    '20241120YYZYEG12F1236'
    >>> change_date('', '', '', '')
    ''
    """

    ticket = ticket[: YR] + year + months + day + ticket[DEP:]

    return ticket


def is_valid_ticket_format(ticket: str) -> bool:
    """Return True if and only if ticket 'ticket' is in valid format:

    - year is 4 digits
    - months is 2 digits
    - day is 2 digits
    - departure is 3 letters
    - arrival is 3 letters
    - row is 2 digits
    - seat is a characters
    - frequent flyer number is either empty or 4 digits, and
      it is the last record in 'ticket'

    >>> is_valid_ticket_format('20241020YYZYEG12C1236')
    True
    >>> is_valid_ticket_format('20241020YYZYEG12C12361236')
    False
    >>> is_valid_ticket_format('ABC41020YYZYEG12C1236')
    False
    """

    return (FFN == 17
            and (len(ticket) == 17
                 or len(ticket) == 21 and ticket[FFN:FFN + 4].isdigit())
            and ticket[YR:YR + 4].isdigit()
            and ticket[MON:MON + 2].isdigit()
            and ticket[DAY:DAY + 2].isdigit()
            and ticket[DEP:DEP + 3].isalpha()
            and ticket[ARR:ARR + 3].isalpha()
            and ticket[ROW:ROW + 2].isdigit()
            and ticket[SEAT].isalpha())

