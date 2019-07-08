from enum import Enum


class FlightBooking(RecognizerConvert):
    def __init__(self):
        self.text = ''
        self.altered_text = ''
        self.intents = {}
        class Intent(Enum):
            BookFlight
            Cancel 
            GetWeather 
            NoneIntent

    class _Entities:
        def __init__():
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
    

    def TopIntent() -> (Intent intent, double score):
    
        Intent maxIntent = Intent.NoneIntent
        var max = 0.0
        foreach (var entry in Intents)
        
            if (entry.Value.Score > max)
            
                maxIntent = entry.Key
                max = entry.Value.Score.Value
            
        
        return (maxIntent, max)
        
    