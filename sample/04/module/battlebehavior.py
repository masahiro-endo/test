
from UI import *
import appconfig as gbl
from actor import *
from module.battlestate import *
from collections import deque
import heapq
import random



class BattleBehavior():
    def __init__(self, parent):
        self.scene = parent
        self.pt = gbl.player_party()
        self.mspt = EnemyParty()

        self.battlelog = deque()
        self.turn_queue = []

        self.action = BattleStates(self)

    def enter_action(self):
        bt_msg = []
        self.mspt.clear_member()
        ms_id = self.pt.get_enemy_random()

        bt_msg += self.battle_encount(ms_id)
        bt_msg += self.is_enemy_first()
        self.pushlog(bt_msg)
        self.action.BattleLog()

    def update(self):
        self.action.update()
    def draw(self):
        self.action.draw()

        # バトル用draw処理（モンスターグラフィック表示）
        if len(self.mspt._member) > 0:
            act = self.mspt[0]
            u = act.img % 4 * 64
            v = act.img // 4 * 64 + 64
            # blt(x, y, imgbank, u, v, w, h, [colkey])
            px.blt(0, 0, 0, u, v, 64, 64)


    def pushlog(self, log):
        self.battlelog.append(log)
    def poplog(self):
        if len(self.battlelog) <= 0:
            return
        self.battlelog.popleft()



    def fill_turn_queue(self):
        self.turn_queue.clear()
        for char in self.pt._member + self.mspt._member:
            if char.is_alive():
                char.btl_spd = char.spd * px.rndf(1.0, 2.0)
                heapq.heappush(self.turn_queue, (-char.btl_spd, char))

    def next_turn(self):
        if not self.turn_queue:
            self.fill_turn_queue()
        _, self.current_actor = heapq.heappop(self.turn_queue)

        # 戦闘不能はスキップ
        if not self.current_actor.is_alive():
            self.next_turn()
            return

        if self.current_actor.is_player:
            self.action.Command_wait()
        else:
            self.battle_enemy_action()


    def is_enemy_first(self):
        bt_msg = []
        if not self.turn_queue:
            self.fill_turn_queue()

        # 先頭を一時的に取り出し、戻す
        _, first_actor = heapq.heappop(self.turn_queue)
        heapq.heappush(self.turn_queue, (-first_actor.btl_spd, first_actor))
        heapq.heapify(self.turn_queue)

        if not first_actor.is_enemy:
            bt_msg += ["てきに せんてをとられた"]
        return bt_msg


    def battle_encount(self, ms_id, evt=None):
        self.bt_evt = evt

        data = gbl.resource().monsters[ms_id]
        data[0:0] = [self.mspt]
        self.mspt.add_member(Actor(*data))

        self.selected_target = 0
        bt_msg = [f"{self.mspt._member[0].name}が あらわれた"]
        return bt_msg

    def end_action(self):
        if self.is_win() or self.is_lose() or len(self.turn_queue) == 0:
            self.action.BattleLog()
        else:
            self.next_turn()
        

    def is_win(self):
        return self.pt.get_alive_actors() and not self.mspt.get_alive_actors()

    def is_lose(self):
        return not self.pt.get_alive_actors() and self.mspt.get_alive_actors()


    # 敵の行動
    def battle_enemy_action(self, msg_pre=[]):
        bt_msg = []
        bt_msg += msg_pre

        enemy = self.current_actor
        target = random.choice(self.pt.get_alive_actors())

        bt_msg += enemy.battlelog_action_atk(target)

        self.pushlog(bt_msg)
        self.end_action()

