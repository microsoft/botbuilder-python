# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Example content for an AdaptiveCard."""

ADAPTIVE_CARD_CONTENT = {
    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    "version": "1.0",
    "type": "AdaptiveCard",
    "speak": "Your flight is confirmed for you and 3 other passengers from San Francisco to Amsterdam on Friday, October 10 8:30 AM",
    "body": [
        {
            "type": "TextBlock",
            "text": "Passengers",
            "weight": "bolder",
            "isSubtle": False,
        },
        {"type": "TextBlock", "text": "Sarah Hum", "separator": True},
        {"type": "TextBlock", "text": "Jeremy Goldberg", "spacing": "none"},
        {"type": "TextBlock", "text": "Evan Litvak", "spacing": "none"},
        {
            "type": "TextBlock",
            "text": "2 Stops",
            "weight": "bolder",
            "spacing": "medium",
        },
        {
            "type": "TextBlock",
            "text": "Fri, October 10 8:30 AM",
            "weight": "bolder",
            "spacing": "none",
        },
        {
            "type": "ColumnSet",
            "separator": True,
            "columns": [
                {
                    "type": "Column",
                    "width": 1,
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "San Francisco",
                            "isSubtle": True,
                        },
                        {
                            "type": "TextBlock",
                            "size": "extraLarge",
                            "color": "accent",
                            "text": "SFO",
                            "spacing": "none",
                        },
                    ],
                },
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {"type": "TextBlock", "text": " "},
                        {
                            "type": "Image",
                            "url": "http://messagecardplayground.azurewebsites.net/assets/airplane.png",
                            "size": "small",
                            "spacing": "none",
                        },
                    ],
                },
                {
                    "type": "Column",
                    "width": 1,
                    "items": [
                        {
                            "type": "TextBlock",
                            "horizontalAlignment": "right",
                            "text": "Amsterdam",
                            "isSubtle": True,
                        },
                        {
                            "type": "TextBlock",
                            "horizontalAlignment": "right",
                            "size": "extraLarge",
                            "color": "accent",
                            "text": "AMS",
                            "spacing": "none",
                        },
                    ],
                },
            ],
        },
        {
            "type": "TextBlock",
            "text": "Non-Stop",
            "weight": "bolder",
            "spacing": "medium",
        },
        {
            "type": "TextBlock",
            "text": "Fri, October 18 9:50 PM",
            "weight": "bolder",
            "spacing": "none",
        },
        {
            "type": "ColumnSet",
            "separator": True,
            "columns": [
                {
                    "type": "Column",
                    "width": 1,
                    "items": [
                        {"type": "TextBlock", "text": "Amsterdam", "isSubtle": True},
                        {
                            "type": "TextBlock",
                            "size": "extraLarge",
                            "color": "accent",
                            "text": "AMS",
                            "spacing": "none",
                        },
                    ],
                },
                {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                        {"type": "TextBlock", "text": " "},
                        {
                            "type": "Image",
                            "url": "http://messagecardplayground.azurewebsites.net/assets/airplane.png",
                            "size": "small",
                            "spacing": "none",
                        },
                    ],
                },
                {
                    "type": "Column",
                    "width": 1,
                    "items": [
                        {
                            "type": "TextBlock",
                            "horizontalAlignment": "right",
                            "text": "San Francisco",
                            "isSubtle": True,
                        },
                        {
                            "type": "TextBlock",
                            "horizontalAlignment": "right",
                            "size": "extraLarge",
                            "color": "accent",
                            "text": "SFO",
                            "spacing": "none",
                        },
                    ],
                },
            ],
        },
        {
            "type": "ColumnSet",
            "spacing": "medium",
            "columns": [
                {
                    "type": "Column",
                    "width": "1",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "Total",
                            "size": "medium",
                            "isSubtle": True,
                        }
                    ],
                },
                {
                    "type": "Column",
                    "width": 1,
                    "items": [
                        {
                            "type": "TextBlock",
                            "horizontalAlignment": "right",
                            "text": "$4,032.54",
                            "size": "medium",
                            "weight": "bolder",
                        }
                    ],
                },
            ],
        },
    ],
}
