
from module.UI import *




class UIResources:

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UIResources, cls).__new__(cls)

            # Cursorに渡す引数リスト　＋Windowメッセージ用の文言
            cls._instance.cursors = {
                CSR.WELCOME :[ [CSR.WELCOME , [1, 5, 10]   , 12   ], [" New Cont Exit"] ], 
                CSR.MENU    :[ [CSR.MENU    , [1, 5, 10]   , 14, MENU_SEL.Cancel ], [f"いま ちか%FLOOR%かいに います", " セーブ じゅもん とじる"] ],
                CSR.SPELLS  :[ [], [] ], 
                CSR.SHOP    :[ [CSR.SHOP    , [1, 4, 7, 11], 14, SHOP_SEL.Cancel] , ["レベルアップするかい？", " HP MP ちから はやさ"] ],
                CSR.BOSS1   :[ [CSR.BOSS1   , [1, 5]       , 14, 1], ["じゅんびは よいか？", " はい  いいえ"] ],
                CSR.BOSS2   :[ [CSR.BOSS2   , [1, 5]       , 14, 1], ["おれと たたかうのか？", " はい  いいえ"] ],
                CSR.BOSS3   :[ [CSR.BOSS3   , [1, 5]       , 14, 1], ["この ひほうが ほしいか？", " はい  いいえ"] ],
                CSR.BTL_CMD :[ [CSR.BTL_CMD , [1, 6, 11]   , 14   ], ["どうする？", " たたかう じゅもん にげる"] ],
                CSR.BTL_SPL :[ [], [] ], # 可変長のため、実行時に生成
            }


        return cls._instance


class CommandTree:

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(CommandTree, cls).__new__(cls)

            # 関数末尾の()は除く。付与していると即時実行してしまう。
            cls._instance.commands = {
                CSR.WELCOME : {
                    'New' : [gbl.scene_state().Main],
                    'Cont': [None],
                    'Exit': [px.quit],
                },
                CSR.MENU     : {
                    'セーブ'  : [None],
                    'じゅもん': [None],
                    'とじる'  : [px.quit],
                },
            }


        return cls._instance

