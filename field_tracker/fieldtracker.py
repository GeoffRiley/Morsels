from abc import ABC
from typing import Any

SEMAPHORE = object()
NOVAL = object()


class _FieldTrackerABC(ABC):
    _fields: dict
    fields: set

    def __init__(self, *_args, **_kwargs) -> None:
        setattr(self, '_fields', {})
        super().__init__(*_args, **_kwargs)
        self._save()

    def changed(self):
        try:
            return {
                k: v
                for k, v in self._fields.items() if self.has_changed(k)
            }
        except AttributeError:
            return {}

    def has_changed(self, name: str):
        if name not in self.fields:
            raise ValueError(f'Variable "{name}" not specified in "fields"')
        return self._fields.get(name, NOVAL) != getattr(self, name, None)

    def _save(self):
        try:
            for name in self.fields:
                self._fields[name] = getattr(self, name)
        except AttributeError as exc:
            raise TypeError('fields variable must be assigned') from exc

    def previous(self, name: str):
        try:
            return self._fields[name]
        except KeyError as exc:
            raise ValueError(f'No value for {name}') from exc

    def save(self):
        try:
            super().save()
        except AttributeError:
            pass
        self._save()


class FieldTracker(_FieldTrackerABC):
    '''
    '''


class FieldTrackerMixin(_FieldTrackerABC):
    '''
    '''
    def init_tracking(self):
        super().__init__()
        self._save()

    def set_saved_fields(self):
        self._save()

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self.fields and getattr(self, '_fields',
                                           None) and name not in self._fields:
            self._fields[name] = value
        super().__setattr__(name, value)
