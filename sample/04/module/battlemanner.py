
from collections import deque
from enum import Enum, auto

import appconfig as gbl
from module.UI import *
from module.actorparty import *
from module.state.battlestack import *
from resource.battleevent import *










class BattleManner(BaseState):
    def __init__(self, parent):
        self.scene = parent
        self.pt = gbl.player_party()
        self.mspt = None

        self.phase = PhASE.IMPUT
        self.current_actor_index = 0
        self.selected_target_index = 0


        # self.action = deque([BattleStates(self)])
        self.action = deque([])
        self.btllog = BattleStack_Log(self)
        self.enter()

    def enter(self):
        self.enemy_spotted()
        self.stack_wait_actions()

    def stack_wait_actions(self):
        # actor = self.pt[self.current_actor_index]
        # 事前に、人数分を積んでおく
        for i, actor in enumerate(self.pt):
            self.action.append(BattleStack_Action(self, actor))
            self.action.append(BattleStack_Target(self, actor))
        self.action.append(BattleStack_Confirm(self))

    def enemy_spotted(self):
        ms_id = self.pt.get_enemy_random()
        data = gbl.map_resource().monsters[ms_id]

        del self.mspt
        self.mspt = EnemyParty(data[0])
        data[0:0] = [self.mspt]
        self.mspt.add_member(Enemy(*data))
        self.mspt.add_member(Enemy(*data))
        self.mspt.add_member(Enemy(*data))

        self.selected_target = 0
        bt_msg = [f"{self.mspt.race}が あらわれた"]
        self.btllog.push(bt_msg)
        self.stack_btllog()

    def stack_btllog(self):
        self.action.appendleft(self.btllog)

    def update(self):
        self.action[0].update()

    def draw(self):
        self.action[0].draw()

        # バトル用draw処理（モンスターグラフィック表示）
        if not self.mspt:
            return
        act = self.mspt[0]
        u = act.img % 4 * 64
        v = act.img // 4 * 64 + 64
        # blt(x, y, imgbank, u, v, w, h, [colkey])
        px.blt(0, 0, 0, u, v, 64, 64)


    def ai_enemy_action(self):
        # 敵AI：ランダムで生きているプレイヤーを攻撃
        for i, actor in enumerate(self.mspt):
            targets = [p for p in self.pt if p.is_alive()]
            if targets:
                actor.action = "attack"
                actor.target = random.choice(targets)

    def build_turn_order(self):
        # 生存キャラを素早さ降順で並べる
        self.all_chars = [c for c in self.pt + self.mspt if c.is_alive()]
        self.turn_order = sorted(self.all_chars, key=lambda c: c.btl_spd, reverse=True)
        self.turn_index = 0


    def handle_execute_phase(self):
        self.ai_enemy_action()
        self.build_turn_order()

        while self.turn_index < len(self.turn_order):
            actor = self.turn_order[self.turn_index]
            targ = actor.target
            if isinstance(targ, Party):
                targets = [p for p in targ if p.is_alive()]
                if targets:
                    actor.target = random.choice(targets)

            if actor.is_alive() and actor.target and actor.target.is_alive():
                self.perform_action(actor)

            actor.action = None
            actor.target = None
            self.turn_index += 1
        #内部的には次ターンまで先行処理
        #外部的にはログ表示
        self.stack_btllog()
        self.next_turn()

    def perform_action(self, actor):
        action = actor.action
        target = actor.target

        bt_msg  = [f"{actor.name} が"]
        bt_msg += [f"{target.name} へ {action}"]
        bt_msg += [f"{1} のダメージ"]
        self.btllog.push(bt_msg)

    def next_turn(self):
        if not any(c.is_alive() and c.is_player for c in self.all_chars):
            self.message = "Enemies win!"
            self.phase = "end"
        elif not any(c.is_alive() and not c.is_player for c in self.all_chars):
            self.player_win()
        else:
            self.stack_wait_actions()
            bt_msg = [f"次のターン"]
            self.btllog.push(bt_msg)
            self.stack_btllog()



    def player_win(self):
        gld = 0
        for i, actor in enumerate(self.mspt):
            gld += int(actor.gold * px.rndf(0.7, 1.0) + 0.99)

        bt_msg  = ["たたかいに かった"]
        bt_msg += [f"{gld}G てにいれた"]
        self.add_gold(gld)

        self.btllog.push(bt_msg)
        self.stack_btllog()
        
        gbl.current_scene().Main()





