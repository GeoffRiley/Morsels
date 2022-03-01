class running_mean():
    def __init__(self, val_list) -> None:
        self.n = 0
        self.av = 0.0
        self.val_list = iter(val_list)

    def __iter__(self):
        return self

    def _update_mean(self, x):
        self.n += 1
        self.av += (x - self.av) / self.n

    def __next__(self):
        return self.send(self.val_list.__next__())

    def send(self, new_val):
        self._update_mean(new_val)
        return new_val, self.av
