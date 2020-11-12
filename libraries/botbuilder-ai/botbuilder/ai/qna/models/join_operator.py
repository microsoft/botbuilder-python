# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from enum import Enum


class JoinOperator(str, Enum):
    """
    Join Operator for Strict Filters.

    remarks:
    --------
    For example, when using multiple filters in a query, if you want results that
    have metadata that matches all filters, then use `AND` operator.

    If instead you only wish that the results from knowledge base match
    at least one of the filters, then use `OR` operator.
    """

    AND = "AND"
    OR = "OR"
