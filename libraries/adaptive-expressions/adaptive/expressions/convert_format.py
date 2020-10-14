from enum import Enum
from datetime import datetime


class State(Enum):
    none = -1
    lower_d1 = 0
    lower_d2 = 1
    lower_d3 = 2
    lower_d4 = 3
    lower_f1 = 4
    lower_f2 = 5
    lower_f3 = 6
    lower_f4 = 7
    lower_f5 = 8
    lower_f6 = 9
    lower_f7 = 10
    capital_f1 = 11
    capital_f2 = 12
    capital_f3 = 13
    capital_f4 = 14
    capital_f5 = 15
    capital_f6 = 16
    capital_f7 = 17
    lower_g = 18
    lower_h1 = 19
    lower_h2 = 20
    capital_h1 = 21
    capital_h2 = 22
    capital_k = 23
    lower_m1 = 24
    lower_m2 = 25
    capital_m1 = 26
    capital_m2 = 27
    capital_m3 = 28
    capital_m4 = 29
    lower_s1 = 30
    lower_s2 = 31
    lower_t1 = 32
    lower_t2 = 33
    lower_y1 = 34
    lower_y2 = 35
    lower_y3 = 36
    lower_y4 = 37
    lower_y5 = 38
    lower_z1 = 39
    lower_z2 = 40
    lower_z3 = 41
    in_single_quoteliteral = 42
    in_double_quoteliteral = 43
    escape_sequence = 44


class FormatDatetime:
    @staticmethod
    def format(timestamp: datetime, fmt_string: str):
        result = ""
        fmt_state = State.none
        ltoken_buffer = ""
        if len(fmt_string) == 0:
            return result
        if len(fmt_string) == 1:
            if fmt_string in ["R", "r"]:
                raise Exception("RFC 1123 not supported in python datetime")
            if fmt_string in ["o", "O"]:
                fmt_string = "YYYY-MM-DDTHH:mm:ss.fffffffZ"
            elif fmt_string == "U":
                raise Exception("Universal Full Format not supported in python")
            elif fmt_string == "u":
                raise Exception("Universal Sortable Format not supported in python")
            elif fmt_string == "D":
                fmt_string = "dddd, MMMM d, YYYY"

        # pylint:disable=too-many-statements
        def change_state(timestamp: datetime, fmt_state, ltoken_buffer):
            result = ""
            if fmt_state == State.lower_d1:
                result = (
                    timestamp.strftime("%d")
                    if timestamp.day >= 10
                    else timestamp.strftime("%d")[1]
                )
            elif fmt_state == State.lower_d2:
                result = timestamp.strftime("%d")
            elif fmt_state == State.lower_d3:
                result = timestamp.strftime("%a")
            elif fmt_state == State.lower_d4:
                result = timestamp.strftime("%A")
            elif fmt_state in [State.lower_f1, State.capital_f1]:
                result = timestamp.strftime("%f")[:1]
            elif fmt_state in [State.lower_f2, State.capital_f2]:
                result = timestamp.strftime("%f")[:2]
            elif fmt_state in [State.lower_f3, State.capital_f3]:
                result = timestamp.strftime("%f")[:3]
            elif fmt_state in [State.lower_f4, State.capital_f4]:
                result = timestamp.strftime("%f")[:4]
            elif fmt_state in [State.lower_f5, State.capital_f5]:
                result = timestamp.strftime("%f")[:5]
            elif fmt_state in [State.lower_f6, State.capital_f6]:
                result = timestamp.strftime("%f")
            elif fmt_state in [State.lower_f7, State.capital_f7]:
                result = timestamp.strftime("%f")[0:1] + "0"
            elif fmt_state == State.lower_g:
                raise Exception("Era not supported in python")
            elif fmt_state == State.lower_h1:
                result = (
                    timestamp.strftime("%I")
                    if timestamp.strftime("%I")[0] != "0"
                    else timestamp.strftime("%I")[1]
                )
            elif fmt_state == State.lower_h2:
                result = timestamp.strftime("%I")
            elif fmt_state == State.capital_h1:
                result = (
                    timestamp.strftime("%H")
                    if timestamp.hour >= 10
                    else timestamp.strftime("%H")[1]
                )
            elif fmt_state == State.capital_h2:
                result = timestamp.strftime("%H")
            elif fmt_state == State.lower_m1:
                result = str(timestamp.minute)
            elif fmt_state == State.lower_m2:
                result = timestamp.strftime("%M")
            elif fmt_state == State.capital_m1:
                result = str(timestamp.month)
            elif fmt_state == State.capital_m2:
                result = timestamp.strftime("%m")
            elif fmt_state == State.capital_m3:
                result = timestamp.strftime("%b")
            elif fmt_state == State.capital_m4:
                result = timestamp.strftime("%B")
            elif fmt_state == State.lower_s1:
                result = str(timestamp.second)
            elif fmt_state == State.lower_s2:
                result = timestamp.strftime("%S")
            elif fmt_state == State.lower_t1:
                result = timestamp.strftime("%p")[0]
            elif fmt_state == State.lower_t2:
                result = timestamp.strftime("%p")
            elif fmt_state == State.lower_y1:
                result = str(timestamp.year % 100)
            elif fmt_state == State.lower_y2:
                result = (
                    str(timestamp.year % 100)
                    if timestamp.year % 100 >= 10
                    else "0" + str(timestamp.year % 100)
                )
            elif fmt_state == State.lower_y3:
                result = (
                    timestamp.strftime("%Y")
                    if timestamp.year >= 1000
                    else timestamp.strftime("%Y")[1:]
                )
            elif fmt_state == State.lower_y4:
                result = timestamp.strftime("%Y")
            elif fmt_state == State.lower_y5:
                result = "0" + timestamp.strftime("%Y")
            elif fmt_state in [State.lower_z1, State.lower_z2]:
                result = timestamp.strftime("%z")
            elif fmt_state == State.lower_z3:
                result = timestamp.strftime("%z") + ":00"
            elif fmt_state in [
                State.in_single_quoteliteral,
                State.in_double_quoteliteral,
                State.escape_sequence,
            ]:
                for lcharacter in ltoken_buffer:
                    result += lcharacter

            return result

        for character in fmt_string:
            if fmt_state == State.escape_sequence:
                ltoken_buffer += character
                result += change_state(timestamp, fmt_state, ltoken_buffer)
                fmt_state = State.none
                ltoken_buffer = ""
            elif fmt_state == State.in_double_quoteliteral:
                if character == r"\`":
                    result += change_state(timestamp, fmt_state, ltoken_buffer)
                    fmt_state = State.none
                    ltoken_buffer = ""
            elif fmt_state == State.in_single_quoteliteral:
                if character == "'":
                    result += change_state(timestamp, fmt_state, ltoken_buffer)
                    fmt_state = State.none
                    ltoken_buffer = ""
                else:
                    ltoken_buffer += character
            else:
                if character in ["D", "d"]:
                    if fmt_state == State.lower_d1:
                        fmt_state = State.lower_d2
                    elif fmt_state == State.lower_d2:
                        fmt_state = State.lower_d3
                    elif fmt_state == State.lower_d3:
                        fmt_state = State.lower_d4
                    elif fmt_state == State.lower_d4:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_d1
                        ltoken_buffer = ""
                elif character == "f":
                    if fmt_state == State.lower_f1:
                        fmt_state = State.lower_f2
                    elif fmt_state == State.lower_f2:
                        fmt_state = State.lower_f3
                    elif fmt_state == State.lower_f3:
                        fmt_state = State.lower_f4
                    elif fmt_state == State.lower_f4:
                        fmt_state = State.lower_f5
                    elif fmt_state == State.lower_f5:
                        fmt_state = State.lower_f6
                    elif fmt_state == State.lower_f6:
                        fmt_state = State.lower_f7
                    elif fmt_state == State.lower_f7:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_f1
                        ltoken_buffer = ""
                elif character == "F":
                    if fmt_state == State.capital_f1:
                        fmt_state = State.capital_f2
                    elif fmt_state == State.capital_f2:
                        fmt_state = State.capital_f3
                    elif fmt_state == State.capital_f3:
                        fmt_state = State.capital_f4
                    elif fmt_state == State.capital_f4:
                        fmt_state = State.capital_f5
                    elif fmt_state == State.capital_f5:
                        fmt_state = State.capital_f6
                    elif fmt_state == State.capital_f6:
                        fmt_state = State.capital_f7
                    elif fmt_state == State.capital_f7:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.capital_f1
                        ltoken_buffer = ""
                elif character == "g":
                    if fmt_state == State.lower_g:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_g
                        ltoken_buffer = ""
                elif character == "h":
                    if fmt_state == State.lower_h1:
                        fmt_state = State.lower_h2
                    elif fmt_state == State.lower_h2:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_h1
                        ltoken_buffer = ""
                elif character == "H":
                    if fmt_state == State.capital_h1:
                        fmt_state = State.capital_h2
                    elif fmt_state == State.capital_h2:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.capital_h1
                        ltoken_buffer = ""
                elif character == "K":
                    result += change_state(timestamp, fmt_state, ltoken_buffer)
                    fmt_state = State.none
                    ltoken_buffer = ""
                    result += "Z"
                elif character == "m":
                    if fmt_state == State.lower_m1:
                        fmt_state = State.lower_m2
                    elif fmt_state == State.lower_m2:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_m1
                        ltoken_buffer = ""
                elif character == "M":
                    if fmt_state == State.capital_m1:
                        fmt_state = State.capital_m2
                    elif fmt_state == State.capital_m2:
                        fmt_state = State.capital_m3
                    elif fmt_state == State.capital_m3:
                        fmt_state = State.capital_m4
                    elif fmt_state == State.capital_m4:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.capital_m1
                        ltoken_buffer = ""
                elif character == "s":
                    if fmt_state == State.lower_s1:
                        fmt_state = State.lower_s2
                    elif fmt_state == State.lower_s2:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_s1
                        ltoken_buffer = ""
                elif character == "t":
                    if fmt_state == State.lower_t1:
                        fmt_state = State.lower_t2
                    elif fmt_state == State.lower_t2:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_t1
                        ltoken_buffer = ""
                elif character in ["y", "Y"]:
                    if fmt_state == State.lower_y1:
                        fmt_state = State.lower_y2
                    elif fmt_state == State.lower_y2:
                        fmt_state = State.lower_y3
                    elif fmt_state == State.lower_y3:
                        fmt_state = State.lower_y4
                    elif fmt_state == State.lower_y4:
                        fmt_state = State.lower_y5
                    elif fmt_state == State.lower_y5:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_y1
                        ltoken_buffer = ""
                elif character == "z":
                    if fmt_state == State.lower_z1:
                        fmt_state = State.lower_z2
                    elif fmt_state == State.lower_z2:
                        fmt_state = State.lower_z3
                    elif fmt_state == State.lower_z3:
                        pass
                    else:
                        result += change_state(timestamp, fmt_state, ltoken_buffer)
                        fmt_state = State.lower_z1
                        ltoken_buffer = ""
                elif character == ":":
                    result += change_state(timestamp, fmt_state, ltoken_buffer) + ":"
                    fmt_state = State.none
                    ltoken_buffer = ""
                elif character == "/":
                    result += change_state(timestamp, fmt_state, ltoken_buffer) + "/"
                    fmt_state = State.none
                    ltoken_buffer = ""
                elif character == r"\`":
                    result += change_state(timestamp, fmt_state, ltoken_buffer)
                    fmt_state = State.in_double_quoteliteral
                    ltoken_buffer = ""
                elif character == "'":
                    result += change_state(timestamp, fmt_state, ltoken_buffer)
                    fmt_state = State.in_single_quoteliteral
                    ltoken_buffer = ""
                elif character == "%":
                    result += change_state(timestamp, fmt_state, ltoken_buffer)
                    fmt_state = State.none
                    ltoken_buffer = ""
                elif character == "\\":
                    result += change_state(timestamp, fmt_state, ltoken_buffer)
                    fmt_state = State.escape_sequence
                    ltoken_buffer = ""
                else:
                    result += (
                        change_state(timestamp, fmt_state, ltoken_buffer) + character
                    )
                    fmt_state = State.none
                    ltoken_buffer = ""

        if fmt_state in [
            State.in_double_quoteliteral,
            State.in_single_quoteliteral,
            State.escape_sequence,
        ]:
            raise Exception("Invalid Format String")
        result += change_state(timestamp, fmt_state, ltoken_buffer)
        return result
