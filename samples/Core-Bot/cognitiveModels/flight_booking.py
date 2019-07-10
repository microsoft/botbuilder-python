# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from enum import Enum, auto
from typing import List, Dict
from botbuilder.ai.luis.generator import InstanceData
from botbuilder.core import IntentScore

class AutoName(Enum):
     def _generate_next_value_(name, start, count, last_values):
         return name


class FlightBooking(RecognizerConvert):
    class Intent(AutoName):
        BookFlight = auto()
        Cancel = auto()
        GetWeather = auto()
        NoneIntent = auto()

    def __init__(self, text: str = '', altered_text: str = '', intents: Dict[Intent, IntentScore] = {} ):
        self.text = text
        self.altered_text = altered_text
        self.intents = intents

    class _Entities:
        def __init__(self):
            # Built-in entities
            self.datetime = []
            # Lists
            self.airport = [[]]

            self.from_property = []
            self.to = []

        # Composites
        class _InstanceFrom:
            def __init__(self):
                self.airport = []
        
        class FromClass:
            def __init__(self):
                self.airport = [[]]
                self._instance = None

        class _InstanceTo:
            def __init__(self):
                self.airport: Ins
            InstanceData[] Airport
        
        class ToClass:
            string[][] Airport
            [JsonProperty("$instance")]
            _InstanceTo _instance

        # Instance
        class _Instance:
        
            InstanceData[] datetime
            InstanceData[] Airport
            InstanceData[] From
            InstanceData[] To
        
        [JsonProperty("$instance")]
        _Instance _instance
    
    _Entities
    

    [JsonExtensionData(ReadData = true, WriteData = true)]
    IDictionary<string, object> Properties get set 

    void Convert(dynamic result)
    
        var app = JsonConvert.DeserializeObject<FlightBooking>(JsonConvert.SerializeObject(result, new JsonSerializerSettings  NullValueHandling = NullValueHandling.Ignore ))
        text = app.text
        Alteredtext = app.Alteredtext
        Intents = app.Intents
        Entities = app.Entities
        Properties = app.Properties
    

    def top_intent() -> (Intent intent, double score):
    
        Intent maxIntent = Intent.NoneIntent
        var max = 0.0
        foreach (var entry in Intents)
        
            if (entry.Value.Score > max)
            
                maxIntent = entry.Key
                max = entry.Value.Score.Value
            
        
        return (maxIntent, max)
        
    