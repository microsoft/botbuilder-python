from .expression_type import ADD, SUBTRACT, MULTIPLY, DIVIDE, MOD
from .expression_type import (
    EQUAL,
    LESSTHAN,
    LESSTHANOREQUAL,
    GREATERTHAN,
    GREATERTHANOREQUAL,
    NOT,
    OR,
    AND,
    CONCAT,
)

# Math
from .builtin_functions.add import Add
from .builtin_functions.subtract import Subtract
from .builtin_functions.multiply import Multiply
from .builtin_functions.divide import Divide
from .builtin_functions.min import Min
from .builtin_functions.max import Max
from .builtin_functions.power import Power
from .builtin_functions.mod import Mod
from .builtin_functions.average import Average
from .builtin_functions.sum import Sum
from .builtin_functions.range import Range
from .builtin_functions.floor import Floor
from .builtin_functions.ceiling import Ceiling
from .builtin_functions.round import Round

# Comparisons
from .builtin_functions.equal import Equal
from .builtin_functions.less_than import LessThan
from .builtin_functions.less_than_or_equal import LessThanOrEqual
from .builtin_functions.greater_than import GreaterThan
from .builtin_functions.greater_than_or_equal import GreaterThanOrEqual
from .builtin_functions.not_equal import NotEqual
from .builtin_functions.exists import Exists

# Logic
from .builtin_functions.not_function import Not
from .builtin_functions.or_function import Or
from .builtin_functions.and_function import And

# String
from .builtin_functions.concat import Concat
from .builtin_functions.length import Length
from .builtin_functions.replace import Replace
from .builtin_functions.replace_ignore_case import ReplaceIgnoreCase
from .builtin_functions.split import Split
from .builtin_functions.to_lower import ToLower
from .builtin_functions.to_upper import ToUpper
from .builtin_functions.trim import Trim
from .builtin_functions.ends_with import EndsWith
from .builtin_functions.starts_with import StartsWith
from .builtin_functions.count_word import CountWord
from .builtin_functions.add_ordinal import AddOrdinal
from .builtin_functions.new_guid import NewGuid
from .builtin_functions.index_of import IndexOf
from .builtin_functions.last_index_of import LastIndexOf
from .builtin_functions.eol import Eol
from .builtin_functions.sentence_case import SentenceCase
from .builtin_functions.title_case import TitleCase
from .builtin_functions.substring import SubString

# Colleaction
from .builtin_functions.count import Count
from .builtin_functions.contains import Contains
from .builtin_functions.empty import Empty
from .builtin_functions.join import Join
from .builtin_functions.first import First
from .builtin_functions.last import Last
from .builtin_functions.foreach import Foreach
from .builtin_functions.select import Select
from .builtin_functions.where import Where
from .builtin_functions.union import Union
from .builtin_functions.intersection import Intersection
from .builtin_functions.skip import Skip
from .builtin_functions.take import Take
from .builtin_functions.sub_array import SubArray
from .builtin_functions.sort_by import SortBy
from .builtin_functions.sort_by_descending import SortByDescending
from .builtin_functions.indices_and_values import IndicesAndValues
from .builtin_functions.flatten import Flatten
from .builtin_functions.unique import Unique

# DataTime
from .builtin_functions.add_days import AddDays
from .builtin_functions.add_hours import AddHours
from .builtin_functions.add_minutes import AddMinutes
from .builtin_functions.add_seconds import AddSeconds
from .builtin_functions.day_of_month import DayOfMonth
from .builtin_functions.day_of_week import DayOfWeek
from .builtin_functions.day_of_year import DayOfYear
from .builtin_functions.month import Month
from .builtin_functions.date import Date
from .builtin_functions.year import Year
from .builtin_functions.utc_now import UtcNow
from .builtin_functions.format_date_time import FormatDateTime
from .builtin_functions.format_epoch import FormatEpoch
from .builtin_functions.format_ticks import FormatTicks
from .builtin_functions.subtract_from_time import SubtractFromTime
from .builtin_functions.date_read_back import DateReadBack
from .builtin_functions.get_time_of_day import GetTimeOfDay
from .builtin_functions.get_future_time import GetFutureTime
from .builtin_functions.get_past_time import GetPastTime
from .builtin_functions.convert_from_utc import ConvertFromUtc
from .builtin_functions.convert_to_utc import ConvertToUtc
from .builtin_functions.add_to_time import AddToTime
from .builtin_functions.start_of_day import StartOfDay
from .builtin_functions.start_of_hour import StartOfHour
from .builtin_functions.start_of_month import StartOfMonth
from .builtin_functions.ticks import Ticks
from .builtin_functions.ticks_to_days import TicksToDays
from .builtin_functions.ticks_to_hours import TicksToHours
from .builtin_functions.ticks_to_minutes import TicksToMinutes
from .builtin_functions.date_time_diff import DateTimeDiff

# Timex
from .builtin_functions.is_definite import IsDefinite
from .builtin_functions.is_time import IsTime
from .builtin_functions.is_duration import IsDuration
from .builtin_functions.is_date import IsDate
from .builtin_functions.is_timerange import IsTimeRange
from .builtin_functions.is_daterange import IsDateRange
from .builtin_functions.is_present import IsPresent

# Conversions
from .builtin_functions.string import String

# URI Parsing Functions
from .builtin_functions.uri_host import UriHost
from .builtin_functions.uri_path import UriPath
from .builtin_functions.uri_path_and_query import UriPathAndQuery
from .builtin_functions.uri_query import UriQuery
from .builtin_functions.uri_port import UriPort
from .builtin_functions.uri_scheme import UriScheme

# Memory
from .builtin_functions.accessor import Accessor
from .builtin_functions.element import Element
from .builtin_functions.create_array import CreateArray

# Misc

# Object manipulation and construction functions
from .builtin_functions.json import Json
from .builtin_functions.get_property import GetProperty
from .builtin_functions.add_property import AddProperty
from .builtin_functions.remove_property import RemoveProperty
from .builtin_functions.set_property import SetProperty
from .builtin_functions.coalesce import Coalesce
from .builtin_functions.xpath import XPath
from .builtin_functions.set_path_to_value import SetPathToValue
from .builtin_functions.jpath import JPath
from .builtin_functions.merge import Merge

# Regular expression
from .builtin_functions.is_match import IsMatch

# Type Checking
from .builtin_functions.is_boolean import IsBoolean
from .builtin_functions.is_string import IsString
from .builtin_functions.is_array import IsArray
from .builtin_functions.is_float import IsFloat
from .builtin_functions.is_integer import IsInteger
from .builtin_functions.is_object import IsObject
from .builtin_functions.is_datetime import IsDateTime

# pylint: disable=too-many-statements
def get_standard_functions() -> dict:
    functions = []

    # Math
    functions.append(Add())
    functions.append(Subtract())
    functions.append(Multiply())
    functions.append(Divide())
    functions.append(Min())
    functions.append(Max())
    functions.append(Power())
    functions.append(Mod())
    functions.append(Average())
    functions.append(Sum())
    functions.append(Range())
    functions.append(Floor())
    functions.append(Ceiling())
    functions.append(Round())

    # Comparisons
    functions.append(Equal())
    functions.append(LessThan())
    functions.append(LessThanOrEqual())
    functions.append(GreaterThan())
    functions.append(GreaterThanOrEqual())
    functions.append(NotEqual())
    functions.append(Exists())

    # Logic
    functions.append(Not())
    functions.append(Or())
    functions.append(And())

    # String
    functions.append(Concat())
    functions.append(Length())
    functions.append(Replace())
    functions.append(ReplaceIgnoreCase())
    functions.append(Split())
    functions.append(SubString())
    functions.append(ToLower())
    functions.append(ToUpper())
    functions.append(Trim())
    functions.append(EndsWith())
    functions.append(StartsWith())
    functions.append(CountWord())
    functions.append(AddOrdinal())
    functions.append(NewGuid())
    functions.append(IndexOf())
    functions.append(LastIndexOf())
    functions.append(Eol())
    functions.append(SentenceCase())
    functions.append(TitleCase())

    # Colleaction
    functions.append(Count())
    functions.append(Contains())
    functions.append(Empty())
    functions.append(Join())
    functions.append(First())
    functions.append(Last())
    functions.append(Foreach())
    functions.append(Select())
    functions.append(Where())
    functions.append(Union())
    functions.append(Intersection())
    functions.append(Skip())
    functions.append(Take())
    functions.append(SubArray())
    functions.append(SortBy())
    functions.append(SortByDescending())
    functions.append(IndicesAndValues())
    functions.append(Flatten())
    functions.append(Unique())

    # DataTime
    functions.append(AddDays())
    functions.append(AddHours())
    functions.append(AddMinutes())
    functions.append(AddSeconds())
    functions.append(DayOfMonth())
    functions.append(DayOfWeek())
    functions.append(DayOfYear())
    functions.append(Month())
    functions.append(Date())
    functions.append(Year())
    functions.append(UtcNow())
    functions.append(FormatDateTime())
    functions.append(FormatEpoch())
    functions.append(FormatTicks())
    functions.append(SubtractFromTime())
    functions.append(DateReadBack())
    functions.append(GetTimeOfDay())
    functions.append(GetFutureTime())
    functions.append(GetPastTime())
    functions.append(ConvertFromUtc())
    functions.append(ConvertToUtc())
    functions.append(AddToTime())
    functions.append(StartOfDay())
    functions.append(StartOfHour())
    functions.append(StartOfMonth())
    functions.append(Ticks())
    functions.append(TicksToDays())
    functions.append(TicksToHours())
    functions.append(TicksToMinutes())
    functions.append(DateTimeDiff())

    # Timex
    functions.append(IsDefinite())
    functions.append(IsTime())
    functions.append(IsDuration())
    functions.append(IsDate())
    functions.append(IsTimeRange())
    functions.append(IsDateRange())
    functions.append(IsPresent())

    # Conversions
    functions.append(String())

    # URI Parsing Functions
    functions.append(UriHost())
    functions.append(UriPath())
    functions.append(UriPathAndQuery())
    functions.append(UriQuery())
    functions.append(UriPort())
    functions.append(UriScheme())

    # Memory
    functions.append(Accessor())
    functions.append(Element())
    functions.append(CreateArray())

    # Misc

    # Object manipulation and construction functions
    functions.append(Json())
    functions.append(GetProperty())
    functions.append(AddProperty())
    functions.append(RemoveProperty())
    functions.append(SetProperty())
    functions.append(Coalesce())
    functions.append(XPath())
    functions.append(SetPathToValue())
    functions.append(JPath())
    functions.append(Merge())

    # Regular expression
    functions.append(IsMatch())

    # Type Checking
    functions.append(IsBoolean())
    functions.append(IsString())
    functions.append(IsArray())
    functions.append(IsInteger())
    functions.append(IsFloat())
    functions.append(IsObject())
    functions.append(IsDateTime())

    lookup = dict()
    for function in functions:
        lookup[function.expr_type] = function

    # Math aliases
    lookup["add"] = lookup[ADD]
    lookup["sub"] = lookup[SUBTRACT]
    lookup["mul"] = lookup[MULTIPLY]
    lookup["div"] = lookup[DIVIDE]
    lookup["mod"] = lookup[MOD]

    # Comparison aliases
    lookup["equals"] = lookup[EQUAL]
    lookup["less"] = lookup[LESSTHAN]
    lookup["lessOrEuqals"] = lookup[LESSTHANOREQUAL]
    lookup["greater"] = lookup[GREATERTHAN]
    lookup["greaterOrEquals"] = lookup[GREATERTHANOREQUAL]

    # Logic aliases
    lookup["not"] = lookup[NOT]
    lookup["or"] = lookup[OR]
    lookup["and"] = lookup[AND]

    lookup["&"] = lookup[CONCAT]

    return lookup


class ExpressionFunctions:
    standard_functions = staticmethod(get_standard_functions())
