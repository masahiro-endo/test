from enum import IntEnum, Enum, auto
from typing import Any, Dict




class BaseState:

    stateMachine = None

    def __init__(self, stateMachine):
        self.stateMachine = stateMachine


    def Enter():
        pass
        
    def Update():
        pass

    def Exit():
        pass


class IdleState(BaseState):
    pass

class MoveState(BaseState):
    pass

class AttackState(BaseState):
    pass


class stateMachine:

    class STATE(IntEnum):
        IDLE = auto()
        MOVE = auto()
        ATTACK = auto()

    Params: Dict[Enum, Any] = {
            STATE.IDLE    : IdleState(),
            STATE.MOVE    : MoveState(),
            STATE.ATTACK  : AttackState(),
    }

    currentState = None
    states = None

    def __init__(self):
        self.states = stateMachine.Params
        self.switchState(self.states[stateMachine.STATE.IDLE])

    def Update(self):
        self.currentState.Update()

    def switchState(self, newState):
        if (self.currentState != None): 
            self.currentState.Exit()

        self.currentState = newState
        self.currentState.Enter()






# IInitializable：初期化が必要なもの
# IPausable：ポーズに反応するもの
# IResettable：リセット対象のもの

# EntityManager

# GameManagerは「流れ」だけを見る
# Stateは「振る舞い」だけを見る
# Entityは「自分がどう反応するか」だけを見る



# 3-2. Stateパターンを構成する3つの役者
# Stateパターンは、主に次の3つで構成されます。

# State（状態）：振る舞いを定義する
# Context：現在の状態を保持・切り替える
# User（利用者）：Contextを使う側（Playerなど）
# ここで重要なのは、 「状態を切り替える責務」をState自身に持たせないことです。

# 状態遷移の判断はContextが行い、 Stateは自分の振る舞いだけに集中します。


