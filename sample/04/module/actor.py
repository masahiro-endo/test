
from enum import Enum, auto
from module.actorvm import *






class JOB(Enum):
    WARRIOR = 'warrior'
    MAGE    = 'mage'
    PRIEST  = 'priest'
    NINJA   = 'ninja'






# Model
class Character():
    def __init__(self, parent, name, hp, mp, atk, spd, is_player,resist=0, img=None, gold=0, skills=None):
        super().__init__()
        self.party = parent
        self.name = name
        self.mhp = hp
        self.hp = hp
        self.mmp = mp
        self.mp = mp
        self.atk = atk
        self.spd = spd
        self.btl_spd = spd
        self.is_player = is_player
        self.resist = resist 
        self.img = img  
        self.gold = gold 
        
        self.status = {}  # {"poison": 残りターン, "paralyze": 残りターン}
        self.action = None
        self.target = None
        self.skills = skills if skills else []  # (スキル名, 関数)
        self.vm = ActorViewModel(self)

    def __lt__(self, other):
        return self.btl_spd < other.btl_spd


    def is_alive(self):
        return self.hp > 0






class Player(Character):
    def __init__(self, parent, name, hp, mp, atk, spd, job):
        self.is_player = True
        self.job = job
        super().__init__(parent, name, hp, mp, atk, spd, self.is_player)

class Enemy(Character):
    def __init__(self, parent, name, hp, mp, atk, spd, resist=0, img=None, gold=0, skills=None):
        self.race = name
        self.is_player = False
        super().__init__(parent, name, hp, mp, atk, spd, self.is_player,resist, img, gold, skills)






class ActorResources:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActorResources, cls).__new__(cls)

            cls._instance.raceabiliy = {
                'human': [],
                'slime': [],
                'ghost': [],
            }

            cls._instance.jobability = {
                JOB.WARRIOR: {
                    'こうげき': [],
                    'ぼうぎょ': [],
                },
                JOB.MAGE: {
                    'ぼうぎょ': [],
                    'じゅもん': [],
                },
                JOB.PRIEST: {
                    'こうげき': [],
                    'じゅもん': [],
                },
            }

        return cls._instance





