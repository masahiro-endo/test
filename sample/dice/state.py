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

