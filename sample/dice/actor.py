import pyxel
import random



dice_dict = [
    (8*0, 128),
    (8*1, 128),
    (8*2, 128),
    (8*3, 128),
    (8*4, 128),
    (8*5, 128)
]


class Die:
    def __init__(self):
        self.init()
    
    def init(self):
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.face_value = 1
        self.active = False
        self.is_roll = False 
        self.fcnt = 0
        self.frames_until_throw = 0
        self.frames_end_roll = 0
        self.roll_behavior = "standard"		# "standard", "bouncy"
    
    def get_value(self):
        return self.face_value
    
    def prepare_to_roll(self, x, y, frames_until_throw, frames_end_roll, roll_behavior="standard"):
        self.active = True
        self.face_value = random.randint(1, 6)
        self.x = x
        self.y = y
        self.init_x = x
        self.init_y = y
        self.vx = -1.0 + random.random() * 2
        self.vy = -4.0 * random.random() - 2.0
        self.frames_until_throw = frames_until_throw
        self.frames_end_roll = frames_end_roll
        self.roll_behavior = roll_behavior
        
    def update(self):
        self.fcnt += 1
        if self.fcnt > self.frames_until_throw:
            if self.is_roll:
                if self.roll_behavior == "standard": self.roll_standard()
                elif self.roll_behavior == "bouncy": self.roll_bouncy()
        elif self.fcnt == self.frames_until_throw:
            self.is_roll = True
        else:
            return

    def roll_standard(self):
        if self.fcnt % 3 == 0:
            self.face_value = pyxel.rndi(1, 6)
        if self.fcnt >= self.frames_end_roll:
            self.is_roll = False       

    def roll_bouncy(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.35
        if not (0 < self.x < pyxel.width - 8):
            self.vx = -self.vx
        if self.y > pyxel.height - 16:
            self.y = pyxel.height - 16
            if self.vy < 2:
                self.is_roll = False
                self.x = self.init_x
                self.y = self.init_y
            else:
                self.vy = -self.vy * 0.5                
        
        if self.fcnt % 3 == 0:
            self.face_value = pyxel.rndi(1, 6)
        

    def draw(self):
        pyxel.blt(self.x, self.y, 0,
                  dice_dict[self.face_value-1][0],
                  dice_dict[self.face_value-1][1],
                  8, 8)


class Dealer():

    def __init__(self):
        pass

    def open_deal(self, max_dice):
        self.total = 0
        self.text_pos = [0, 0]
        self.active_count = 0
        self.dice = [Die() for i in range(max_dice)]
        
    def reset(self):
        self.active_count = 0
        for die in self.dice:
            die.init()

    def set_active_dice_count(self, count):
        self.reset()
        if 0 < count <= len(self.dice):
            self.active_count = count
            for i in range(count):
                self.dice[i].active = True 
        else:
            raise ValueError("roll時の要求数が不適切です")

    def throw(self, count, x, y, behavior):
        self.text_pos = x, y
        self.set_active_dice_count(count)
        i = 0
        for die in self.dice:
            if die.active:
                frm_ut = random.randint(5, 20)
                frm_er = 30 + i*12
                die.prepare_to_roll(x + i*9, y, frm_ut, frm_er, behavior)
                i += 1

    def update(self):
        self.total = 0
        for die in self.dice:
            if die.active:
                die.update()
                self.total += die.get_value()
                
    def draw(self):
        pyxel.text(self.text_pos[0], self.text_pos[1]-9, str(self.total), 3)
        for die in self.dice:
            if die.active:
                die.draw()



