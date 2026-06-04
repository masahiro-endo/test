import pyxel




class GuiButton():
    def __init__(self, x, y, w, h, text):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.idle_color = 12
        self.active_color = 5
        self.cur_color = self.idle_color
        self.text_color = 0        
    
    def update(self):
        msg = ""
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx = pyxel.mouse_x
            my = pyxel.mouse_y
            if (self.x <= mx <= self.x + self.w) and (self.y <= my <= self.y + self.h): 
                msg = self.text
        self.cur_color = self.idle_color
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            mx = pyxel.mouse_x
            my = pyxel.mouse_y
            if (self.x <= mx <= self.x + self.w) and (self.y <= my <= self.y + self.h): 
                self.cur_color = self.active_color
        
        return msg
    
    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.cur_color)
        ofs_h = (self.h - 6)/2
        pyxel.text(self.x+2, self.y+ofs_h, self.text, self.text_color)


class ButtonContainer:
    def __init__(self, labels, x, y):
        self.w = max(len(s) for s in labels) * 4 + 2
        self.h = 8
        self.gbtns = []
        for i, v in enumerate(labels):
            self.gbtns.append(GuiButton(x, y+i*(self.h+1), self.w, self.h, v))
    
    def update(self):
        msg = ""
        for gbtn in self.gbtns:
            tmp_msg = gbtn.update()
            if tmp_msg != "": msg = tmp_msg
        return msg
    
    def draw(self):
        for gbtn in self.gbtns:
            gbtn.draw()


