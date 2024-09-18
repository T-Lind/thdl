class Val:
    def __init__(self, value):
        if isinstance(value, int):
            if value not in [0, 1]:
                raise ValueError('Value must be 0 or 1')
            self.value = bool(value)
        elif isinstance(value, str):
            if value not in ['0', '1']:
                raise ValueError('Value must be "0" or "1"')
            self.value = bool(int(value))
        elif isinstance(value, bool):
            self.value = value
        else:
            raise ValueError('Value must be an int, str, or bool')

    def __call__(self):
        return self.value

    def __set__(self, value):
        self.value = value

    def __invert__(self):
        self.value = not self.value
        return self

    def __str__(self):
        return str(int(self.value))

    def __repr__(self):
        return str(int(self.value))


class ValList:
    def __init__(self, binary=None, list=None):
        if binary:
            binary_str = bin(binary)[2:]
            self.vals = [Val(int(bit)) for bit in binary_str]
        elif list:
            self.vals = list
        else:
            raise ValueError('Must provide binary or list')

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self.vals))
            return [self.vals[len(self.vals) - 1 - i] for i in range(start, stop, step)]
        else:
            return self.vals[len(self.vals) - 1 - key]

    def __setitem__(self, key, value):
        self.vals[len(self.vals) - 1 - key] = value

    def __len__(self):
        return len(self.vals)

    def __str__(self):
        return to_bin(self.vals)

    def __repr__(self):
        return to_bin(self.vals)

    def __add__(self, other):
        return ValList(list=self.vals + other.vals)


def from_bin(binary) -> list[Val]:
    binary_str = bin(binary)[2:]  # Convert to binary string and remove '0b' prefix
    return [Val(int(bit)) for bit in binary_str]

def to_bin(val_list: list[Val]) -> str:
    return ''.join([str(int(val())) for val in val_list])
