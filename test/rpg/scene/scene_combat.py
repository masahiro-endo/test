
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





class BaseAction:

    class SEL:
        WAIT = auto()
        COMPLETE = auto()

    class Parameter:
        def __init__(self, key):
            self.key = key

    Params: Dict[Enum, Any] = {
            SEL.COMPLETE  : Parameter,
    }

    Params[SEL.COMPLETE]    = Parameter(None)

    def __init__(self):
        self.status = self.SEL.WAIT
        self._snd = None

    def handler(self, keyboard):
        pass


class PlayerAction(BaseAction):

    class ACT:
        ATTACK = auto()
        DEFENCE = auto()
        MAGIC = auto()
        ITEM = auto()

    class Parameter:
        def __init__(self, name, effect, sound):
            self.name = name
            self.effect = effect
            self.sound = sound

    Params: Dict[Enum, Any] = {
            ACT.ATTACK    : Parameter,
            ACT.DEFENCE   : Parameter,
    }

    Params[ACT.ATTACK]    = Parameter("攻撃", None, "/sounds/剣の素振り2.mp3")
    Params[ACT.DEFENCE]   = Parameter("防御", None, "/sounds/ステータス治療1.mp3")

    def __init__(self, enemies):
        super().__init__()
        self.enemies = enemies


class EnemyAction(BaseAction):

    '''
    WOLF
        BITE
        BREATH
    '''
    def __init__(self, players):
        super().__init__()
        self.players = players # 攻撃対象が単体とは限らない


class SelectAction(BaseAction):

    def __init__(self, key, wnd, actor, parties):
        super().__init__()
        self.Params[self.SEL.COMPLETE] = key
        self._wnd = wnd
        
        self.actor = actor
        self.parties = parties

    def update(self):
        super().update()

        for wnd in self._wnd:
            if wnd is None: continue
            if wnd.is_visible(): wnd.update()
                    
    def draw(self, screen):
        super().draw(screen)

        for wnd in self._wnd:
            if wnd is None: continue
            if wnd.is_visible(): wnd.draw(screen)


    def handler(self, event):
        super().handler(event)

        for wnd in self._wnd:
            if wnd is None: continue
            if wnd.is_visible(): wnd.handler(event)

        if keyboard[self.Params[self.SEL.COMPLETE]]: 
                self.hide()
                self.status = self.SEL.COMPLETE

class PartyActTool():

    class ACT:
        ATTACK  = 0
        DEFENCE = 1
        MAGIC   = 2
        ITEM    = 3
        RUN     = 4
        LENGTH  = 5

    class Parameter:
        def __init__(self, curpos, strpos, caption, selected ):
            self.curpos = curpos
            self.strpos = strpos
            self.caption = caption
            self.selected = selected

    Params: Dict[Enum, Any] = {
            ACT.ATTACK    : Parameter,
            ACT.DEFENCE   : Parameter,
    }

    Params[ACT.ATTACK]    = Parameter((20, 30), (40, 15), "こうげき", False)
    Params[ACT.DEFENCE]   = Parameter((20, 60), (40, 45), "ぼうぎょ", False)


class Turn:

    _pause = deque()

    def __init__(self, party):
        self._charalive = []

        for actor in party.member:
            if not actor.is_dead():
                self._charalive.append(actor)

        for actor in self._charalive:
            wnd = SelectWindow(Rect(20,300,120,140), PartyActTool.Params)
            self._pause.append(SelectAction(keys.RETURN, wnd, actor, g.eneparties))

        self._pause[0]._wnd.show()


    def update(self):

        if len(self._pause) > 0 and self._pause[0] != None:
            wnd = self._pause[0]._wnd
            if wnd.is_visible(): wnd.update()
                    
    def draw(self, screen):

        if len(self._pause) > 0 and self._pause[0] != None:
            wnd = self._pause[0]._wnd
            if wnd.is_visible(): wnd.draw(screen)

    def handler(self, event):

        if len(self._pause) > 0 and self._pause[0] != None:
            wnd = self._pause[0]._wnd
            if wnd.is_visible(): wnd.handler(event)

            sl = self._pause[0]
            if sl.status == sl.SEL.COMPLETE:
                self._pause.popleft() # 処理済みを除去
                if len(self._pause[0]) > 0:
                    self._pause[0]._wnd.show() # 次の選択を表示
                else:
                    pass
                    # アクションを実行


class CombatScene(BaseScene):

    def __init__(self):
        self._actlist = deque() # 一時表示
        self.visual = deque() # 常時表示

        '''
        wnd = MessageWindow(Rect(20,300,600,140))
        wnd.setText('なにか　とそうぐうした！')
        wnd.show()
        self._wnd.append(wnd)

        wnd = SelectWindow(Rect(20,300,120,140), PartyActTool.Params)
        wnd.show()
        self._wnd.append(wnd)

        wnd = ScriptWindow(Rect(20,300,600,140))
        wnd.textall = "１２３４５６７８９０/あいうえお/かきくけこ/さしすせそ/たちつてと/なにぬねの/はひふへほ/まみむめもやゆよわをん"
        wnd.show()
        self._wnd.append(wnd)

        wnd = StatusWindow(Rect(20,20,300,100), g.party)
        wnd.show()
        self._wnd.append(wnd)

                # self._actorimg = control.Method.load_image("./assets/images/npc/", "pngegg(32).png", -1)
        # self._actorimg = pygame.transform.scale(self._actorimg, (200, 200))
        self._actorimg = None
        
        # self._actlist.appendleft(PlayerDicide())
        # self._actlist.appendleft(AIDicide())

        wnd = MessageWindow(Rect(20,300,600,140))
        wnd.setText('なにか　とそうぐうした！')
        wnd.show()
        self._actlist.append(WindowAction(keys.RETURN, wnd))
        '''
        self.turn = Turn(g.party)



    def update(self):
        super().update()
        self.turn.update()

        for wnd in self.visual:
            if wnd is None: continue
            if wnd.is_visible(): wnd.update()

        if len(self._actlist) > 0:
            action = self._actlist[0]
            if not action._snd is None:
                action._snd.play()
                action._snd = None
            if not action._wnd is None:
                if action._wnd.is_visible(): action._wnd.update()

            if action.status==action.SEL.COMPLETE:
                self._actlist.popleft()
                    
    def draw(self, screen):
        super().draw(screen)
        self.turn.draw(screen)

        # if not self._actorimg is None:
        #     screen.blit(self._actorimg, (200, 100))

        for wnd in self.visual:
            if wnd is None: continue
            if wnd.is_visible(): wnd.draw(screen)

        if len(self._actlist) > 0:
            action = self._actlist[0]
            if not action._wnd is None:
                if action._wnd.is_visible(): action._wnd.draw(screen)


    def handler(self, event):
        super().handler(event)
        self.turn.handler(event)

        for wnd in self.visual:
            if wnd is None: continue
            if wnd.is_visible(): wnd.handler(event)

        if len(self._actlist) > 0:
            action = self._actlist[0]
            if not action._wnd is None:
                if action._wnd.is_visible(): action._wnd.handler(event)



