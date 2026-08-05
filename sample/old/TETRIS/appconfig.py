# 循環参照防止のため、ここではimportしない



class Globals:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            cls._instance.puyo = None
            cls._instance.puyos = None
            cls._instance.field = None
            cls._instance.board = None
        return cls._instance


@property
def puyo():
    return Globals().puyo
@puyo.setter
def puyo(new_value):
    Globals().puyo = new_value

@property
def puyos():
    return Globals().puyos
@puyos.setter
def puyos(new_value):
    Globals().puyos = new_value

@property
def field():
    return Globals().field
@field.setter
def field(new_value):
    Globals().field = new_value

@property
def board():
    return Globals().board
@board.setter
def board(new_value):
    Globals().board = new_value



