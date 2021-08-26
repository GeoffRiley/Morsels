from collections import UserString
from unicodedata import normalize


class FuzzyString(UserString):

    def _myfuzz_(self, x: object) -> str:
        return normalize('NFKD', str(x).casefold())

    def _myval_(self) -> str:
        return self._myfuzz_(self.data)

    def __eq__(self, x: object) -> bool:
        return self._myval_().__eq__(self._myfuzz_(x))

    def __lt__(self, x: str) -> bool:
        return self._myval_().__lt__(self._myfuzz_(x))

    def __le__(self, x: str) -> bool:
        return self._myval_().__le__(self._myfuzz_(x))

    def __gt__(self, x: str) -> bool:
        return self._myval_().__gt__(self._myfuzz_(x))

    def __ge__(self, x: str) -> bool:
        return self._myval_().__ge__(self._myfuzz_(x))

    def __contains__(self, char: object) -> bool:
        return self._myfuzz_(char) in self._myval_()
