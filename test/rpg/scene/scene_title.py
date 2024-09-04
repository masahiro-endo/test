import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *

import global_value as g
from scene.scene import *
from scene.scene_field import *
from UI import *




class TitleScene(BaseScene):

    def __init__(self):
        self.title = Actor("python_quest.png", topleft=(20,60))
        self.menu = StartWindow(Rect(220, 200, 180, 200))
        self.menu.show()

    def trans_fieldScene(self):
        g.game_state = SCENE.FIELD
        
        # g.map.create("field")  # フィールドマップへ

        g.sceneStack.popleft()
        g.sceneStack.appendleft(FieldScene())

    def update(self):
        super().update()
        self.menu.update()

    def draw(self, screen):
        super().draw(screen)
        self.menu.draw(screen)

    def handler(self, keyboard):
        super().handler(keyboard)
        self.menu.handler(keyboard)

        if g.game_state==SCENE.FIELD:
            # g.map.create("field")  # フィールドマップへ
            g.sceneStack.popleft()
            g.sceneStack.appendleft(FieldScene())


    def play_bgm(self):
        pass
        bgm_file = "title.mp3"
        bgm_file = os.path.join("bgm", bgm_file)
        pygame.mixer.music.load(bgm_file)
        pygame.mixer.music.play(-1)



