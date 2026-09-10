
class Globals:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            cls._instance.player = None
            cls._instance.enemies = None
            cls._instance.bullets = None
            cls._instance.explosions = None
            cls._instance.items = None
            cls._instance.stars = None
            cls._instance.obstacles = None
            cls._instance.stack = None
            cls._instance.state = None
            cls._instance.score = None
        return cls._instance


@property
def player():
    return Globals().player
@player.setter
def player(new_value):
    Globals().player = new_value

@property
def enemies():
    return Globals().enemies
@enemies.setter
def enemies(new_value):
    Globals().enemies = new_value

@property
def bullets():
    return Globals().bullets
@bullets.setter
def bullets(new_value):
    Globals().bullets = new_value

@property
def explosions():
    return Globals().explosions
@explosions.setter
def explosions(new_value):
    Globals().explosions = new_value

@property
def items():
    return Globals().items
@items.setter
def items(new_value):
    Globals().items = new_value

@property
def stars():
    return Globals().stars
@stars.setter
def stars(new_value):
    Globals().stars = new_value

@property
def obstacles():
    return Globals().obstacles
@obstacles.setter
def obstacles(new_value):
    Globals().obstacles = new_value

@property
def stack():
    return Globals().stack
@stack.setter
def stack(new_value):
    Globals().stack = new_value

@property
def state():
    return Globals().stack[-1] if Globals().stack else None 
@state.setter
def state(new_value):
    Globals().stack[-1] = new_value

@property
def score():
    return Globals().score
@score.setter
def score(new_value):
    Globals().score = new_value

