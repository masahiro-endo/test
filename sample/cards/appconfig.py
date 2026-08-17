# 循環参照防止のため、ここではimportしない



class Globals:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            cls._instance.BOF = None
            cls._instance.columns = None
            cls._instance.homecells = None
        return cls._instance


@property
def BOF():
    return Globals().BOF
@BOF.setter
def BOF(new_value):
    Globals().BOF = new_value

@property
def columns():
    return Globals().columns
@columns.setter
def columns(new_value):
    Globals().columns = new_value

@property
def homecells():
    return Globals().homecells
@homecells.setter
def homecells(new_value):
    Globals().homecells = new_value
