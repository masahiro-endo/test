# Behavior Tree
import time




# ===== 基本ノード定義 =====

class Status:
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    RUNNING = "RUNNING"


class Node:
    """全ノードの基底クラス"""
    def tick(self):
        raise NotImplementedError("tick() を実装してください")


# ----- Composite Nodes -----

class Sequence(Node):
    """すべて成功したら SUCCESS、一つでも失敗したら FAILURE"""
    def __init__(self, children):
        self.children = children

    def tick(self):
        for child in self.children:
            result = child.tick()
            if result != Status.SUCCESS:
                return result
        return Status.SUCCESS


class Selector(Node):
    """一つ成功したら SUCCESS、すべて失敗したら FAILURE"""
    def __init__(self, children):
        self.children = children

    def tick(self):
        for child in self.children:
            result = child.tick()
            if result == Status.SUCCESS:
                return Status.SUCCESS
        return Status.FAILURE


# ----- Leaf Nodes -----

class Condition(Node):
    """条件チェック"""
    def __init__(self, func):
        self.func = func

    def tick(self):
        try:
            return Status.SUCCESS if self.func() else Status.FAILURE
        except Exception:
            return Status.FAILURE


class Action(Node):
    """行動ノード"""
    def __init__(self, func):
        self.func = func

    def tick(self):
        try:
            ok = self.func()
            return Status.SUCCESS if ok else Status.FAILURE
        except Exception:
            return Status.FAILURE


# ====== 動作サンプル ======

# 状態（本来はロボットの状況などに使う）
state = {"battery": 50, "target_visible": True}

def is_battery_ok():
    return state["battery"] > 20

def is_target_visible():
    return state["target_visible"]

def move_to_target():
    print("ターゲットに移動中...")
    time.sleep(0.2)
    return True

def recharge():
    print("充電中...")
    time.sleep(0.2)
    state["battery"] = 100
    return True


# Behavior Tree 構築
tree = Selector([
    Sequence([
        Condition(is_battery_ok),
        Condition(is_target_visible),
        Action(move_to_target),
    ]),
    Action(recharge)
])


# ====== 実行ループ ======
if __name__ == "__main__":
    for _ in range(3):
        result = tree.tick()
        print("結果:", result, "バッテリー:", state["battery"])
        print("-----")
        time.sleep(0.5)

