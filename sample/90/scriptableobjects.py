# ScriptableObject Architecture
import json
from typing import Any, Callable, List


# --------------------------------------------------------------------
# Base ScriptableObject
# --------------------------------------------------------------------
class ScriptableObject:
    """
    Base data container similar to Unity's ScriptableObject.
    Supports loading/saving JSON data.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def save(self, path: str):
        """Save object data to a JSON file."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.__dict__, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Failed to save ScriptableObject: {e}")

    @classmethod
    def load(cls, path: str):
        """Load object data from a JSON file."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(**data)
        except Exception as e:
            raise RuntimeError(f"Failed to load ScriptableObject: {e}")


# --------------------------------------------------------------------
# ScriptableEvent – observer pattern
# --------------------------------------------------------------------
class ScriptableEvent:
    """Simple event system supporting multiple listeners."""

    def __init__(self):
        self._listeners: List[Callable[[Any], None]] = []

    def subscribe(self, callback: Callable[[Any], None]):
        if not callable(callback):
            raise TypeError("Listener must be callable.")
        if callback not in self._listeners:
            self._listeners.append(callback)

    def unsubscribe(self, callback: Callable[[Any], None]):
        if callback in self._listeners:
            self._listeners.remove(callback)

    def raise_event(self, data: Any = None):
        """Notify all listeners."""
        for listener in list(self._listeners):
            try:
                listener(data)
            except Exception as e:
                print(f"Listener error: {e}")


# --------------------------------------------------------------------
# RuntimeSet – similar to Unity RuntimeSet ScriptableObject
# --------------------------------------------------------------------
class RuntimeSet(ScriptableObject):
    """Keeps track of active objects at runtime."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.items: List[Any] = []

    def add(self, item: Any):
        if item not in self.items:
            self.items.append(item)

    def remove(self, item: Any):
        if item in self.items:
            self.items.remove(item)

    def clear(self):
        self.items.clear()


# --------------------------------------------------------------------
# Example usage
# --------------------------------------------------------------------
if __name__ == "__main__":

    # Example Scriptable Data Object
    player_stats = ScriptableObject(
        health=100,
        mana=50,
        player_name="Hero"
    )

    # Save / load example
    player_stats.save("player_stats.json")
    loaded = ScriptableObject.load("player_stats.json")
    print("Loaded:", loaded.__dict__)

    # Event example
    on_damage = ScriptableEvent()

    def handle_damage(amount):
        print(f"Player took {amount} damage.")

    on_damage.subscribe(handle_damage)
    on_damage.raise_event(20)  # triggers callback

    # RuntimeSet example
    enemies = RuntimeSet()
    enemies.add("Goblin")
    enemies.add("Orc")
    print("Active enemies:", enemies.items)


