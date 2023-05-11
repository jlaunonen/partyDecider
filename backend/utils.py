import typing
from typing import Mapping


def parse_bool(inp: str | None, default: bool) -> bool:
    if inp is None or inp == "":
        return default
    if inp.lower() in ("1", "true"):
        return True
    return False


K = typing.TypeVar("K")
V = typing.TypeVar("V")


class ChangeTrackedDict(dict[K, V]):
    _unset = object()

    def __init__(self, seq: typing.Mapping[K, V] = _unset):
        if seq is not self._unset:
            super().__init__(seq)
        else:
            super().__init__()
        self._is_changed = False

    def __setitem__(self, key: K, value: V):
        super().__setitem__(key, value)
        self._is_changed = True

    def __delitem__(self, key: K):
        super().__delitem__(key)
        self._is_changed = True

    def __ior__(self, value: Mapping[K, V]) -> dict[K, V]:
        own_keys = set(self.keys())
        if hasattr(value, "keys"):
            changed_keys = own_keys & set(value.keys())
            if changed_keys:
                self._is_changed = True
            return super().__ior__(value)
        else:
            def proxy() -> typing.Iterator[tuple[K, V]]:
                changed = False
                for element in value:
                    if element[0] in own_keys:
                        changed = True
                    yield element
                self._is_changed |= changed

            return super().__ior__(proxy())

    def setdefault(self, key: K, default: V = None) -> V:
        value = self.get(key, self._unset)
        if value is self._unset:
            # setitem sets changed flag
            self[key] = default
            return default
        return value

    def update(self, m: typing.Mapping[K, V] = None, /, **kwargs: typing.Mapping[K, V]) -> None:
        if m is not None:
            if m or kwargs:
                self._is_changed = True
                super().update(m, **kwargs)
        elif kwargs:
            self._is_changed = True
            super().update(**kwargs)

    def pop(self, key: K, default: V = _unset) -> V:
        if default is not self._unset:
            old_len = len(self)
            value = super().pop(key, default)
            if old_len != len(self):
                self._is_changed = True
        else:
            value = super().pop(key)
            self._is_changed = True
        return value

    def popitem(self) -> tuple[K, V]:
        value = super().popitem()
        self._is_changed = True
        return value

    def clear(self):
        not_empty = len(self) > 0
        super().clear()
        self._is_changed |= not_empty

    def clear_changed(self):
        self._is_changed = False

    @property
    def is_changed(self) -> bool:
        return self._is_changed
