
from collections import deque
from enum import Enum, auto

import appconfig as gbl
from module.UI import *
from module.actorparty import *
from module.state.battlestack import *
from resource.battleevent import *










class BattleBehavior(BaseState):

    def __init__(self, parent):
        self.scene = parent
        self.pt = gbl.player_party()
        self.mspt = None

        # 不意打ち等の、
        # 割り込み処理に対応するためキューを用いる。
        self.comand = deque([])
        self.action = deque([])
        self.btltrm = BattleStack_Term(self)
        self.enter()

    def enter(self):
        self.enemy_spotted()
        self.reset_stack_wait_commands()

    def reset_reserve_action(self):
        for i, actor in enumerate(self.all_chars()):
            if actor.is_alive():
                actor.action = ('？？', None)
            else:
                actor.action = ('しぼう', None)

    def stack_wait_commands(self):
        # 事前に、人数分を積んでおく
        for i, actor in enumerate(self.pt):
            if actor.is_alive():
                self.comand.append(BattleStack_Action(self, actor))
                self.comand.append(BattleStack_Target(self, actor))
        self.comand.append(BattleStack_Confirm(self))

    def reset_stack_wait_commands(self):
        self.reset_reserve_action()
        self.stack_wait_commands()

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
        self.stack_btllog(bt_msg)

    def stack_btllog(self, log, priority=False):
        ins = BattleStack_Log.replicate(self, log)
        if priority:
            self.comand.appendleft(ins)
        else:
            self.comand.append(ins)
    def stack_effect(self):
        self.comand.append(BattleStack_Effect(self))
    def stack_reflect(self, *args, **kwargs):
        self.comand.append(BattleStack_Period(self, *args, **kwargs))
    def stack_delimit(self):
        self.comand.append(BattleStack_Delim(self))
    def stack_btltrm(self):
        self.comand.append(self.btltrm()) # __call__

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
        # ステータス表示
        Window.battle_status(self.pt)


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
        self.exec_next_actor()

    def exec_next_actor(self):
        # while len(self.action) > 0:
        if len(self.action) > 0:
            func, args = self.action.popleft()
            actor = args[0]
            targ  = args[1]

            if isinstance(targ, BaseParty):
                targets = [p for p in targ if p.is_alive()]
            if isinstance(targ, Character):
                targets = targ if targ.is_alive() else None

            if actor.is_alive() and targets:
                self.perform_action(func, actor, targ)

            self.stack_delimit()
        else:
            # 末尾に、分岐用の、
            # Teaminalをstack
            self.stack_btltrm()


    def perform_action(self, func, actor, targ):

        actor.vm.process_status(self)
        if not 'paralyze' in actor.status:
            func(actor, targ, self)

        actor.vm.end_turn_status(self)







