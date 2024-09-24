
import pgzrun
from pgzero.builtins import *
import pygame
from pygame.locals import *
import codecs
import os
from enum import IntEnum, Enum, auto
from typing import Any, Dict
from collections import deque
import json

import global_value as g
from scene.scene import *
from UIControl import *







class BaseWindow:
    EDGE_WIDTH = 4  # 白枠の幅

    def __init__(self, rect):
        self.rect = rect  # 一番外側の白い矩形
        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)  # 内側の黒い矩形
        self.visible = False

    def update(self):
        pass

    def draw(self, screen):
        if not self.is_visible(): 
            return
        screen.draw.rect(self.rect, pygame.Color('black'))
        screen.draw.rect(self.inner_rect, pygame.Color('white'))

    def handler(self, keyboard):
        pass
    
    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def is_visible(self):
        return self.visible





class SelectWindow(BaseWindow):

    class CHARPTR(IntEnum):
        IS_ACTIVE = 0
        WAIT_LINE = auto()
        WAIT_PAGE = auto()
        ENDOFLINE = auto()
        WAIT_SELECT = auto()

    class Style():
        LINE_SPACE = 5

    def is_pause(self)->bool:
        return self.pause

    def input_pause(self):
        self.pause = True

    def input_allow(self):
        self.pause = False


    def __init__(self, rect, params):
        super().__init__(rect)
        self.rect = rect
        dx = self.rect.left
        dy = self.rect.top
        self.pos = (dx, dy)
        # self.cursor = SelectCursor(dx, dy, Color("white"))

        self.status = self.CHARPTR.WAIT_SELECT

        self.select = 0
        self.init_selectitems(params)
        self.input_allow()

    def init_selectitems(self, params):
        self.params = params
        self.cursor = Actor("cursor_select.png", self.params[self.select].curpos)

    def get_curpos(self, pnum)->Tuple:
        dx, dy = self.pos
        dx += self.params[pnum].curpos[0]
        dy += self.params[pnum].curpos[1]
        return (dx, dy)

    def get_strpos(self, pnum)->Tuple:
        dx, dy = self.pos
        dx += self.params[pnum].strpos[0]
        dy += self.params[pnum].strpos[1]
        return (dx, dy)

    def update(self):
        super().update()

        self.cursor.pos = self.get_curpos(self.select)


    def draw(self, screen):
        super().draw(screen)

        if not self.is_visible():
            return

        # メニューの描画
        for i in range(len(self.params)):
            dx, dy = self.get_strpos(i)
            screen.draw.text(self.params[i].caption , \
                            (dx, dy), fontsize=24, color='WHITE', fontname='dragon_quest_fc.ttf')

        self.cursor.draw()
        
    def handler(self, keyboard):
        super().handler(keyboard)

        if keyboard[keys.RETURN]:
            self.params[self.select].selected = True 
            self.status = self.CHARPTR.IS_ACTIVE
            self.hide()

        if self.is_pause():
            return

        if keyboard[keys.UP]:
            self.select = len(self.params)- 1 if (self.select - 1) < 0 else self.select - 1

        if keyboard[keys.DOWN]:
            self.select = (self.select + 1) % len(self.params)


        if __debug__:
            self.input_pause()
            clock.schedule_interval(self.input_allow, 1)



class MessageWindow(BaseWindow):

    def __init__(self, rect):
        BaseWindow.__init__(self, rect)
        self.rect = rect
        self.text = []
        self.text_pos = (self.rect.left + 20, self.rect.top + 20)
        # self.cursor = Actor("cursor_next.png", self.Params[self.SELECT.START].curpos)

    def setText(self, text):
        self.text = text

    def update(self):
        super().update()

    def draw(self, screen):
        super().draw(screen)
        screen.draw.text(self.text  , \
                        self.text_pos, fontsize=24, color='WHITE', fontname='dragon_quest_fc.ttf')


    def handler(self, keyboard):
        super().handler(keyboard)

        if keyboard[keys.RETURN]: 
            self.hide()


class FontTool(BaseWindow):
    @staticmethod
    def replace_widenum(num)->Any:
        before = ['0','1','2','3','4','5','6','7','8','9']
        after = ['０','１','２','３','４','５','６','７','８','９']

        res = str(num)
        for i in range(len(before)):
            res = res.replace(before[i],after[i])

        return res 


class StatusWindow(BaseWindow):
    ROW_GAP = 20

    def __init__(self, rect, party):
        BaseWindow.__init__(self, rect)
        self.party = party
        self.text_pos = (self.rect.left + 10, self.rect.top + 10)

    def update(self):
        super().update()

    def draw(self, screen):
        super().draw(screen)

        for i in range(len(self.party.memberList)):
            pos = (self.text_pos[0], self.text_pos[1] + (i * self.ROW_GAP))
            name = self.party.memberList[i].name
            hp = FontTool.replace_widenum(self.party.memberList[i].hp)
            mp = FontTool.replace_widenum(self.party.memberList[i].mp)
            screen.draw.text(f"{name:>5}　{hp:>4}　{mp:>4}" , \
                            pos, fontsize=24, color='WHITE', fontname='dragon_quest_fc.ttf')



    def handler(self, keyboard):
        super().handler(keyboard)

        if keyboard[keys.RETURN]: 
            self.hide()



class ScriptPerser():

    _arg = {
            'scenario': 'scenario1',
            'speed': 1,
    }

    def __init__(self, **kwargs):
        self.validate_args(kwargs)
        scenario = self._arg['scenario']
        self.speed = self._arg['speed']

        self.init_scenario(scenario)
        for self.currPage in self.json_dict: break
        self.init_page(self.currPage)

    def validate_args(self, args):
        for key in self._arg.keys():
            arg = args.get(key)
            if arg != None:
                self._arg[key] = arg

    def init_scenario(self, filename):
        self.json_dict = self.read_json(filename)

    def read_json(self, filename) -> Any:
        f = open(f'./assets/events/{filename}.json', 'r', encoding="utf-8")
        json_dict = json.load(f, object_pairs_hook=OrderedDict)

        if __debug__:
            for x in json_dict:
                print(f'{x}:{json_dict[x]}')

        return json_dict

    def init_page(self, currPage):
        self.text = self.json_dict[currPage]["text"]
        self.next = self.json_dict[currPage]["next"]
        self.speed = int(self.json_dict[currPage]["speed"])




class ScriptWindow(BaseWindow):

    class CHARPTR(IntEnum):
        IS_ACTIVE = 0
        WAIT_LINE = auto()
        WAIT_PAGE = auto()
        ENDOFLINE = auto()
        WAIT_SELECT = auto()

    class LIMIT(IntEnum):
        CHAR_COUNT = 30
        LINE_COUNT = 5
        PAGE_COUNT = 999

    class Parameter:
        def __init__(self, cursor, delim):
            self.cursor = cursor
            self.delim = delim

    Params: Dict[Enum, Any] = {
            CHARPTR.IS_ACTIVE  : Parameter,
            CHARPTR.WAIT_LINE  : Parameter,
            CHARPTR.WAIT_PAGE  : Parameter,
            CHARPTR.WAIT_SELECT: Parameter,
    }

    Params[CHARPTR.IS_ACTIVE]    = Parameter(None,'')
    Params[CHARPTR.WAIT_LINE]    = Parameter(LineCursor,'/')
    Params[CHARPTR.WAIT_PAGE]    = Parameter(PageCursor,'%')
    Params[CHARPTR.WAIT_SELECT]  = Parameter(None,'#')



    def __init__(self, rect):
        BaseWindow.__init__(self, rect)
        self.rect = rect
        dx = rect.left + (rect.width // 2)
        dy = rect.top + (rect.height - 20)
        self.Params[self.CHARPTR.WAIT_LINE].cursor = LineCursor(dx, dy, Color("white"))
        self.Params[self.CHARPTR.WAIT_PAGE].cursor = PageCursor(dx, dy, Color("white"))

        self.surfs = deque()

        self.text_pos = (self.rect.left + 20, self.rect.top + 20)
        self.textall = []
        self.buf = ""
        self.ptr = 0
        
        self.pause = 0
        self.speed = 1
        self.status = self.CHARPTR.IS_ACTIVE

    def update(self):
        super().update()
        self.pause += 1
        
        if not self.Params[self.status].cursor == None:
            self.Params[self.status].cursor.update()
            return

        self.pause %= self.speed
        if not self.pause == 0:
            return

        if len(self.buf) >= self.LIMIT.CHAR_COUNT:
            self.buf = "" # バッファをクリア
            self.surfs.append(self.buf) # 末尾に空の要素を追加

        if len(self.surfs) >= self.LIMIT.LINE_COUNT:
            self.surfs.popleft()

        if len(self.buf) >= len(self.textall) or self.ptr >= len(self.textall):
            self.status = self.CHARPTR.WAIT_PAGE
            return

        ch = self.textall[self.ptr]

        if ch == "/":
            self.buf = ""
            self.surfs.append(self.buf)
            self.ptr += 1
            self.status = self.CHARPTR.WAIT_LINE
            return

        if ch == "%":
            self.status = self.CHARPTR.WAIT_PAGE
            return

        if ch == "#":
            self.ptr += 1
            self.status = self.CHARPTR.WAIT_SELECT
            return

        if ch == "$":
            pass

        self.buf += self.textall[self.ptr]
        # dequeの要素数は最低でも１つ用意して、
        # 末尾のdequeに対して、その内容を一文字ずつ更新
        if len(self.surfs) == 0:self.surfs.append('')
        self.surfs[-1] = self.buf
        self.ptr += 1

    def draw(self, screen):
        super().draw(screen)

        if not self.Params[self.status].cursor == None:
            self.Params[self.status].cursor.draw(screen)

        for i in range(len(self.surfs)):
            dx, dy = self.text_pos
            dy += (i * 20)
            screen.draw.text(self.surfs[i] , \
                            (dx, dy), fontsize=24, color='WHITE', fontname='dragon_quest_fc.ttf')

            if __debug__:
                print(f"{i}{self.surfs[i]}")

        
    def handler(self, keyboard):
        super().handler(keyboard)

        if keyboard[keys.RETURN]: 
            if self.status == self.CHARPTR.WAIT_LINE:
                self.status = self.CHARPTR.IS_ACTIVE
            elif self.status == self.CHARPTR.WAIT_PAGE:
                self.hide()
            elif self.status == self.CHARPTR.WAIT_SELECT:
                self.status = self.CHARPTR.IS_ACTIVE


