import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *

import global_value as g
from scene.scene import *
from scene.scene_field import *
from UI import *




class TitleScene(BaseScene):

    class SELECT(IntEnum):
        START = 0
        CONTINUE = 1
        EXIT = 2
        LENGTH = 3

    class Parameter:
        def __init__(self, curpos, strpos, caption, selected ):
            self.curpos = curpos
            self.strpos = strpos
            self.caption = caption
            self.selected = selected

    Params: Dict[Enum, Any] = {
            SELECT.START    : Parameter,
            SELECT.CONTINUE : Parameter,
            SELECT.EXIT     : Parameter,
    }

    Params[SELECT.START]     = Parameter((20, 30), (40, 15), 'スタート', False)
    Params[SELECT.CONTINUE]  = Parameter((20, 60), (40, 45), 'コンティニュー', False)
    Params[SELECT.EXIT]      = Parameter((20, 90), (40, 75), 'おわり', False)

    def __init__(self):
        self.title = Actor("python_quest.png", topleft=(20,60))
        self.menu = SelectWindow(Rect(220, 200, 180, 200), TitleScene.Params)
        self.menu.show()

    def trans_fieldScene(self):
        g.game_state = SCENE.FIELD
        g.sceneStack.popleft()
        g.sceneStack.appendleft(FieldScene())

    def get_selectnum(self)->int:
        for i in self.menu.params:
            if self.menu.params[i].selected:
                res = i
                break
        return res

    def update(self):
        super().update()
        self.menu.update()

    def draw(self, screen):
        super().draw(screen)
        self.menu.draw(screen)

    def handler(self, keyboard):
        super().handler(keyboard)
        self.menu.handler(keyboard)

        if self.menu.status==self.menu.CHARPTR.IS_ACTIVE:
            selnum = self.get_selectnum()
            if self.SELECT.START==selnum:
                self.trans_fieldScene()
            elif self.SELECT.EXIT==selnum:
                pygame.quit()
                sys.exit()
                   

    def play_bgm(self):
        pass
        bgm_file = "title.mp3"
        bgm_file = os.path.join("bgm", bgm_file)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.play(-1)



