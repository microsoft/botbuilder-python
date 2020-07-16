from enum import IntFlag


class ReturnType(IntFlag):
    "True or false boolean value."
    Boolean = (1,)

    "Numerical value like int, float, double, ..."
    Number = (2,)

    "Any value is possible."
    Object = (4,)

    "String value."
    String = (8,)

    "Array value."
    Array = 16
