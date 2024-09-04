
import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *
from enum import IntEnum, Enum, auto
from typing import Any, Dict
from collections import deque

import global_value as g
from scene.scene import *
from UI import *





class CombatAction:

    _msg: str
    _snd: pygame.mixer.Sound
    
    def __init__(self):
        self._msg = "１１１のダメージ%"
    
class PlayerDicide(CombatAction):
    def __init__(self):
        super().__init__()
        # self._snd = pygame.mixer.Sound("./assets/sounds/" + "ステータス治療1.mp3")

class AIDicide(CombatAction):
    def __init__(self):
        super().__init__()
        # self._snd = pygame.mixer.Sound("./assets/sounds/" + "剣の素振り2.mp3")




class CombatScene(BaseScene):

    def __init__(self):
        self._actlist = deque()
        self._wnd = deque()
        '''
        wnd = MessageWindow(Rect(20,300,600,140))
        wnd.setText('なにか　とそうぐうした！')
        wnd.show()
        self._wnd.append(wnd)
        '''
        wnd = ScriptWindow(Rect(20,300,600,140))
        wnd.textall = "１２３４５６７８９０/あいうえお/かきくけこ/さしすせそ/たちつてと/なにぬねの/はひふへほ/まみむめもやゆよわをん"
        wnd.show()
        self._wnd.append(wnd)

        '''
        wnd = StatusWindow(Rect(20,20,300,100), g.party)
        wnd.show()
        self._wnd.append(wnd)
        '''
        # self._actorimg = control.Method.load_image("./assets/images/npc/", "pngegg(32).png", -1)
        # self._actorimg = pygame.transform.scale(self._actorimg, (200, 200))
        self._actorimg = None
        
        # self._actlist.appendleft(PlayerDicide())
        # self._actlist.appendleft(AIDicide())

    def update(self):
        super().update()

        if len(self._actlist) > 0:
            if not self._actlist[0]._snd is None:
                self._actlist[0]._snd.play()
                self._actlist[0]._snd = None

        for wnd in self._wnd:
            if wnd is None: continue
            if wnd.is_visible(): wnd.update()


                    
    def draw(self, screen):
        super().draw(screen)

        if not self._actorimg is None:
            screen.blit(self._actorimg, (200, 100))

        for wnd in self._wnd:
            if wnd is None: continue
            if wnd.is_visible(): wnd.draw(screen)


    def handler(self, event):
        super().handler(event)

        for wnd in self._wnd:
            if wnd is None: continue
            if wnd.is_visible(): wnd.handler(event)

        '''
        if event.type == KEYDOWN:
            
            if self._wnd.is_visible:
                self._wnd.hide()
                
            if event.key == K_SPACE:
                g.currentScene.popleft()

            if event.key == K_RETURN:
                if len(self._actlist) > 0:
                    self._wnd.settext(self._actlist[0]._msg)
                    self._actlist.popleft()
        '''


