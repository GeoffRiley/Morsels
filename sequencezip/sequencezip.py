class SequenceZip:
    def __init__(self, *args) -> None:
        self.seqs = args

    def __len__(self) -> int:
        return min(len(s) for s in self.seqs)

    def __getitem__(self, idx: int) -> tuple:
        window = tuple(seq[:len(self)] for seq in self.seqs)

        if isinstance(idx, slice):
            new_args = [[seq[i] for i in range(*idx.indices(len(self)))]
                        for seq in window]

            return SequenceZip(*new_args)

        return tuple(x[idx] for x in window)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}{self.seqs!r}"

    def __eq__(self, o: object) -> bool:
        if isinstance(o, SequenceZip):
            ln = len(self)
            if ln == len(o):
                return all(
                    list(self.seqs[i][:ln]) == list(o.seqs[i][:ln])
                    for i in range(len(self.seqs)))
        return False
