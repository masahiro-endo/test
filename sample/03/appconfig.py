# 循環参照防止のため、ここではimportしない



class Globals:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Globals, cls).__new__(cls)
            # デフォルト設定の初期化
            # 循環参照防止のため、この時点では生成しない
            cls._instance.BDF = None
            cls._instance.screen = None
            cls._instance.party = None
            cls._instance.cursor = None
        return cls._instance

def get_settings():
    return Globals()
def get_screen():
    return Globals().screen
def get_party():
    return Globals().party



