# 循環参照防止のため、ここではimportしない



class Globals:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            cls._instance.BOF = None
        return cls._instance


@property
def BOF():
    return Globals().BOF
@BOF.setter
def BOF(new_value):
    Globals().BOF = new_value


