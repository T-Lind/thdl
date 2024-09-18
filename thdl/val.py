class Val:
    def __init__(self, value):
        if isinstance(value, int):
            self.value = bool(value)
        elif isinstance(value, str):  # '0' or '1'
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


def from_list(*args) -> list[Val]:
    return [Val(i) for i in args]

def from_binary(binary) -> list[Val]:


