
from pgzero.builtins import *
import pygame
from typing import Any, Dict
import global_value as g


class BaseWindow:

    class Style():
        BORDER = 2

    def __init__(self, rect: pygame.Rect):
        linewidth: int = 0

        self.surf: pygame.Surface = pygame.Surface( (rect.width, rect.height) )
        self.surf.fill(pygame.Color('black'))
        self.rect = self.surf.get_rect(topleft=(rect.top,rect.left))

        self.inner_rect = self.rect.inflate(-self.Style.BORDER * 2, -self.Style.BORDER * 2)
        pygame.draw.rect(self.surf, pygame.Color('white'), self.rect, linewidth)
        pygame.draw.rect(self.surf, pygame.Color('black'), self.inner_rect, linewidth)
        # self.rect = rect

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, (self.rect.left, self.rect.top) )



class CaptionWindow(BaseWindow):

    EDGE_WIDTH = 2
    _caption = ''

    def __init__(self, rect: Rect, caption: str):
        linewidth: int = 0

        self.surf = pygame.Surface( (rect.width, rect.height) )
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

        self.inner_rect = self.rect.inflate(-self.EDGE_WIDTH * 2, -self.EDGE_WIDTH * 2)
        pygame.draw.rect(self.surf, pygame.Color('white'), self.rect, linewidth)
        pygame.draw.rect(self.surf, pygame.Color('black'), self.inner_rect, linewidth)
        self.rect = rect

        self._caption = caption

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.surf, (self.rect.left, self.rect.top) )
        screen.draw.text("{self._caption}\n", \
                         left=self.rect.left,top=self.rect.top,fontsize=64,color='YELLOW')

    def handler(self, keyboard):
        pass



                