#!/usr/bin/env python
import pgzrun
from pgzero.builtins import *
from collections import deque
import os
# os.chdir(os.path.dirname(__file__))
# sys.path.append(os.path.dirname(__file__))

import global_value as g
from actor import *
from control import *
from scene.scene import *
from scene.scene_title import *
from scene.scene_combat import *
from UI import *







class Game:
    class Setting:
        class DisplayResolution():
            VGA = (640, 480)
            SVGA = (800, 600)
            XGA = (1024, 768)
        
        def is_dispay_area(pos: tuple) -> bool:
            x, y = pos
            if (0 < x < WIDTH) and (0 < y < HEIGHT):
                return True
            return False

    def init():

        g.objects = []  # スプライトのリスト
        g.game_state = SCENE.TITLE

        g.party = PlayerParty()
        player1 = Player("せんし", AvatorTool.JOB.SWORDMAN)
        player2 = Player("ねこ", AvatorTool.JOB.WHITECAT)
        g.party.addMember(player1)
        g.party.addMember(player2)

        g.eneparties = deque()

        party = EnemyParty()
        enemy1 = Enemy("スライム１", AvatorTool.JOB.SWORDMAN)
        enemy2 = Enemy("スライム２", AvatorTool.JOB.WHITECAT)
        party.addMember(enemy1)
        party.addMember(enemy2)
        g.eneparties.append(party)

        party = EnemyParty()
        enemy1 = Enemy("オオカミ１", AvatorTool.JOB.SWORDMAN)
        enemy2 = Enemy("オオカミ２", AvatorTool.JOB.WHITECAT)
        party.addMember(enemy1)
        party.addMember(enemy2)
        g.eneparties.append(party)

        '''
        avator1 = Avator(AvatorTool.JOB.WHITECAT)
        avator2 = Avator(AvatorTool.JOB.SWORDMAN)
        g.party.addMember(avator1)
        g.party.addMember(avator2)
        g.map = []
        g.blocks = deque()
        '''
        g.sceneStack = deque()
        g.sceneStack.appendleft(CombatScene())

        g.mainDir = os.path.dirname(__file__)

        g.fontPath = './test/rpg/fonts/dragon_quest_fc.ttf'
        font = pygame.font.Font(g.fontPath, 11)


WIDTH, HEIGHT = Game.Setting.DisplayResolution.VGA






def draw():
    screen.clear()

    if len(g.sceneStack) > 0 and g.sceneStack[0] != None:
        g.sceneStack[0].draw(screen)
    '''    
    for scene in reversed(g.sceneStack):
        if scene is None:
            continue
        scene.draw(screen)
    '''

    if g.game_state==SCENE.TITLE:
        pass
    else:
        for sp in g.objects:
            sp.draw()



def update():
    
    if len(g.sceneStack) > 0 and g.sceneStack[0] != None:
        g.sceneStack[0].update()
        g.sceneStack[0].handler(keyboard)
    '''
    for scene in reversed(g.sceneStack):
        if scene is None:
            continue
        scene.update()
        scene.handler(keyboard)
    '''

    if g.game_state==SCENE.TITLE:
        pass        
        return

    elif g.game_state==SCENE.GAMEOVER:
        pass
        return

    elif g.game_state==SCENE.WINDOW_OPEN:
        pass
        return
    else:
        pass

    for sp in reversed(g.objects):
        sp.update()
        sp.count+=1

        if sp.hp<=0:
            g.objects.remove(sp)  # 耐久値ゼロのスプライトを消去
            continue
        
        if not Game.Setting.is_dispay_area(sp.pos):
            g.objects.remove(sp)  # 画面外のスプライトを消去
            continue







Game.init()
pgzrun.go()





