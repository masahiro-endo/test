
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

        # 不意打ち等の、
        # 割り込み処理に対応するためキューを用いる。
        self.comand = deque([])
        self.action = deque([])
        self.btllog = BattleStack_Log(self)
        self.btltrm = BattleStack_Term(self)
        self.enter()

    def enter(self):
        self.enemy_spotted()
        self.stack_wait_commands()

    def stack_wait_commands(self):
        # 事前に、人数分を積んでおく
        for i, actor in enumerate(self.pt):
            self.comand.append(BattleStack_Action(self, actor))
            self.comand.append(BattleStack_Target(self, actor))
        self.comand.append(BattleStack_Confirm(self))

    def enemy_spotted(self):
        ms_id = self.pt.get_enemy_random()
        data = gbl.map_resource().monsters[ms_id]

        del self.mspt
        self.mspt = EnemyParty(data[0])
        data[0:0] = [self.mspt]
        self.mspt.add_member(Enemy(*data))
        self.mspt.add_member(Enemy(*data))
        self.mspt.add_member(Enemy(*data))

        bt_msg = [f"{self.mspt.race}が あらわれた"]
        self.btllog.push(bt_msg)
        self.stack_btllog()

    def stack_btllog(self):
        if len(self.comand) > 0:
            if isinstance(self.comand[0], BattleStack_Log):
                return
        self.comand.appendleft(self.btllog)
    def stack_btltrm(self):
        self.btltrm.enter()
        self.comand.append(self.btltrm)

    def update(self):
        self.comand[0].update()

    def draw(self):
        self.comand[0].draw()

        # バトル用draw処理（モンスターグラフィック表示）
        if not self.mspt:
            return
        act = self.mspt[0]
        u = act.img % 4 * 64
        v = act.img // 4 * 64 + 64
        # blt(x, y, imgbank, u, v, w, h, [colkey])
        px.blt(0, 0, 0, u, v, 64, 64)


    def push_action(self, func, *args, priority=False):
        if priority:
            self.action.appendleft((func, args))
        else:
            self.action.append((func, args))

    def all_chars(self):
        return [c for c in self.pt + self.mspt if c.is_alive()]

    def build_turn_order(self):
        self.action.clear()
        # 生存キャラを素早さ降順で並べる
        turn_order = sorted(self.all_chars(), key=lambda c: c.btl_spd, reverse=True)

        for actor in turn_order:
            if actor.is_alive():
                skl_name, skl_func = actor.action
                target = actor.target
                self.push_action(skl_func, actor, target)


    def ai_enemy_action(self):
        # 敵AI：ランダムで生きているプレイヤーを攻撃
        for i, actor in enumerate(self.mspt):
            targets = [p for p in self.pt if p.is_alive()]
            if targets:
                actor.target = random.choice(targets)
                actor.action = random.choice(actor.skills)

    def handle_execute_phase(self):
        self.ai_enemy_action()
        self.build_turn_order()

        while len(self.action) > 0:
            func, args = self.action.popleft()
            actor = args[0]
            targ  = args[1]

            if isinstance(targ, BaseParty):
                targets = [p for p in targ if p.is_alive()]
            if isinstance(targ, Character):
                targets = targ if targ.is_alive() else None

            if actor.is_alive() and targets:
                self.perform_action(func, actor, targ)

            actor.action = None
            actor.target = None

        #内部的には次ターンまで先行処理
        #外部的にはログ表示
        self.stack_btllog()
        self.stack_btltrm()


    def perform_action(self, func, actor, targ):

        log = actor.vm.process_status()
        if not '麻痺' in log:
            log = func(actor, targ)

        actor.vm.end_turn_status()
        self.btllog.push(log)







