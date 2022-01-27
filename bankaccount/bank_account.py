class BankAccount:
    _account_base: int = 1000
    accounts: list = []

    @classmethod
    def _next_account_number(cls) -> int:
        cls._account_base += 1
        return cls._account_base

    def validate(self, value: int):
        if value < 0:
            raise ValueError('Negative amounts not allowed')

    def __init__(self, balance: int = 0) -> None:
        self.validate(balance)
        self._balance = balance
        self._account_number = self._next_account_number()
        BankAccount.accounts.append(self)

    @property
    def balance(self) -> int:
        return self._balance

    @property
    def number(self) -> int:
        return self._account_number

    def _set_balance_(self, value):
        self.validate(value)
        self._balance = value

    def withdraw(self, value: int):
        self.validate(value)
        self._set_balance_(self.balance - value)

    def deposit(self, value: int):
        self.validate(value)
        self._set_balance_(self.balance + value)

    def transfer(self, other: 'BankAccount', value: int):
        self.validate(value)
        self.withdraw(value)
        other.deposit(value)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(balance={self.balance})'
