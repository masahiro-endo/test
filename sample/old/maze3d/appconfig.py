
class Globals:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            cls._instance.party = None
            cls._instance.map = None
        return cls._instance


@property
def party():
    return Globals().party
@party.setter
def party(new_value):
    Globals().party = new_value

@property
def map():
    return Globals().map
@map.setter
def map(new_value):
    Globals().map = new_value



