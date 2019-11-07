class TeamInfo:
    def __init__(self, id = "", name = ""):
        self.id = id
        self.name = name
    
    @property
    def id():
        return self.id
    
    @property
    def name():
        return self.name