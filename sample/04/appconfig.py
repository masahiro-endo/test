# 循環参照防止のため、ここではimportしない



class Globals:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            # デフォルト設定の初期化
            # 循環参照防止のため、この時点では生成しない
            cls._instance.BDF = None
            cls._instance.scene = None
            cls._instance.map = None
            cls._instance.party = None
            cls._instance.cursor = None
            cls._instance.resource = None
        return cls._instance


def global_setting():
    return Globals()

def scene():
    return Globals().scene

def field_map():
    return Globals().map

def player_party():
    return Globals().party

def current_cursor():
    return Globals().cursor

def map_resource():
    return Globals().resource


