



# 呪文
class Spell:
    def __init__(self, name, mp, on_menu, desc):
        self.name = name
        self.mp = mp
        self.on_menu = on_menu
        self.desc = desc




class SkillResources:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SkillResources, cls).__new__(cls)
            # 呪文データ
            cls._instance.spells = [
                Spell(
                    "ファイア", 2, False, ["ちいさな ひのたまを", "てきにぶつけて ダメージ"]
                ),
                Spell("リターン", 6, True, ["スタートいちに", "テレポートする"]),
                Spell("ヒール", 0, True, ["HPを かいふく", "かいふくしたぶんMPをつかう"]),
                Spell(
                    "バースト",
                    0,
                    False,
                    ["すべての まりょくを", "てきにぶつけて だいダメージ"],
                ),
            ]

        return cls._instance





