from collections import OrderedDict, deque
import pygame
from pygame import rect
from pygame import draw
from pygame.locals import *
import global_value as g
from enum import IntEnum, auto
import math
from typing import Any, Dict, List, Text, Tuple
from enum import Enum



class LineCursor():

    def __init__(self, x: int, y: int, color):
        self.x = x
        self.y = y
        self.color = color
        self.theta = 0

    def update(self):
        self.theta += 10

    def draw(self, screen):
        self.theta %= 360 
        r = abs( 5 * math.sin(math.radians(self.theta)) )
        pygame.draw.polygon(screen.surface, self.color, 
                ([self.x - r, self.y], [self.x + r, self.y], [self.x, self.y + 12]) )

class SelectCursor():

    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
        self.theta = 0

    def update(self, y: int):
        self.y = y
        self.theta += 10

    def draw(self, screen: pygame.Surface):
        self.theta %= 360 
        r = abs( 5 * math.sin(math.radians(self.theta)) )
        pygame.draw.polygon(screen, self.color, 
                ([self.x, self.y - r], [self.x + 12, self.y], [self.x, self.y + r]) )

class PageCursor():

    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
        self.trans = 0

        self.surf = pygame.Surface( (10, 15), flags=pygame.SRCALPHA)
        self.surf.set_colorkey(Color('black'))
        self.surf.fill(Color('black'))
        self.rect = self.surf.get_rect()

        pygame.draw.polygon(self.surf, self.color, 
                ( [self.rect.x, self.rect.y], 
                  [self.rect.x + 10, self.rect.y], 
                  [self.rect.x + 10, self.rect.y + 10], 
                  [self.rect.x + 5, self.rect.y + 10], 
                  [self.rect.x + 5, self.rect.y + 15], 
                  [self.rect.x, self.rect.y + 15]) )
        pygame.draw.polygon(self.surf, self.color, 
                ( [self.rect.x + 7, self.rect.y + 12], 
                  [self.rect.x + 10, self.rect.y + 12], 
                  [self.rect.x + 7, self.rect.y + 15]) )

    def update(self):
        self.trans += 10

    def draw(self, screen: pygame.Surface):
        self.trans %= 250
        self.surf.set_alpha(self.trans)
        screen.blit(self.surf, (self.x, self.y) )


class FontCursor():

    def __init__(self, x: int, y: int, color: Color):
        self.x = x
        self.y = y
        self.color = color
        self.trans = 0

        self.font: pygame.Surface = g.UIfont.render(f"{'ＰＲＥＳＳ　ＥＮＴＥＲ　ＫＥＹ':<30}")
        self.rect: pygame.Rect = self.font.get_rect()
        self.surf = pygame.Surface( (self.rect.width, self.rect.height), flags=pygame.SRCALPHA)
        self.surf.set_colorkey(Color('black'))
        self.surf.fill(Color('black'))
        self.surf.blit(self.font, (self.rect.left, self.rect.top) )

    def update(self):
        self.trans += 10

    def draw(self, screen: pygame.Surface):
        self.trans %= 250
        self.surf.set_alpha(self.trans)
        screen.blit(self.surf, (self.x, self.y) )


