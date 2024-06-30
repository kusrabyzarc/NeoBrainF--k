class MemoryStack:
    def __init__(self):
        self.__val__ = [0]
        self.__neg_shift__ = 0

    def __getitem__(self, item):
        if not isinstance(item, (int, slice)):
            raise TypeError(f'MemoryStack indices must be int or slice, not {type(item)}')

        if isinstance(item, slice):
            start = item.start or 0
            stop = item.stop or len(self.__val__)
            start += self.__neg_shift__
            stop += self.__neg_shift__

            while start < 0:
                start += 1
                self.__neg_shift__ += 1
                self.__val__.insert(0, 0)

            while len(self.__val__) < start:
                self.__val__.append(0)

            while stop < 0:
                stop += 1
                self.__neg_shift__ += 1
                self.__val__.insert(0, 0)

            while len(self.__val__) < stop:
                self.__val__.append(0)

            item = slice(start, stop)

        else:
            item += self.__neg_shift__
            while item < 0:
                item += 1
                self.__neg_shift__ += 1
                self.__val__.insert(0, 0)

            while len(self.__val__) <= item:
                self.__val__.append(0)

        return self.__val__[item]

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise TypeError(f'MemoryStack indices must be int, not {type(key)}')

        key += self.__neg_shift__
        while key < 0:
            key += 1
            self.__neg_shift__ += 1
            self.__val__.insert(0, 0)

        while len(self.__val__) <= key:
            self.__val__.append(0)

        self.__val__[key] = value

    def __len__(self):
        return len(self.__val__)


class NeoBrainFuckInterpreter:
    def __init__(self, obj, *, do_debug=False):
        self.__ALLOWED_COMMANDS__ = [',', '.', '>', '<', '+', '-', '[', ']', '$', '%', '^']
        if isinstance(obj, str):
            self.obj = obj
        else:
            raise TypeError(f'Expected str object, but {type(obj)} found.')
        self.__CODE__ = list(filter(lambda x: x in self.__ALLOWED_COMMANDS__, self.obj))
        self.__MEMORY__ = MemoryStack()
        self.__CHR_MODE__ = True
        self.__DO_DBG__ = do_debug
        self.__MEMORY_POINTER__ = 0
        self.__CODE_POINTER__ = 0
        self.__BRA_KET_VALIDATION__()

    def __BRA_KET_VALIDATION__(self):
        """Correct loops validation"""
        cnt = 0
        for symb in self.__CODE__:
            if symb == '[':
                cnt += 1
            elif symb == ']':
                cnt -= 1
                if cnt < 0:
                    break
        if cnt != 0:
            raise AssertionError('Bra-Ket validation failed.')

    def __ADD__(self):
        """Add 1 to current cell (+)"""
        self.__MEMORY__[self.__MEMORY_POINTER__] += 1
        self.__CODE_POINTER__ += 1

    def __SUB__(self):
        """Subtract 1 from current cell (-)"""
        self.__MEMORY__[self.__MEMORY_POINTER__] -= 1
        self.__CODE_POINTER__ += 1

    def __READ_MEMORY__(self):
        """Read current cell"""
        return self.__MEMORY__[self.__MEMORY_POINTER__]

    def __SHIFT_RIGHT__(self, *, __internal_call__=False):
        """Shift cell 1 right (>)"""
        self.__MEMORY_POINTER__ += 1
        if not __internal_call__:
            self.__CODE_POINTER__ += 1

    def __SHIFT_LEFT__(self, *, __internal_call__=False):
        """Shift cell 1 left (<)"""
        self.__MEMORY_POINTER__ -= 1
        if not __internal_call__:
            self.__CODE_POINTER__ += 1

    def __OUTPUT__(self):
        """Output value (.)"""
        if self.__CHR_MODE__:
            print(chr(self.__READ_MEMORY__()), end='')
        else:
            print(self.__READ_MEMORY__(), end=' ')
        self.__CODE_POINTER__ += 1

    def __INPUT__(self):
        """Input value (,)"""
        if self.__CHR_MODE__:
            self.__MEMORY__[self.__MEMORY_POINTER__] = ord(input()[0])
        else:
            self.__MEMORY__[self.__MEMORY_POINTER__] = int(input())
        self.__CODE_POINTER__ += 1

    def __BRA__(self):
        """Loop entry ([)"""
        if self.__READ_MEMORY__() == 0:
            while self.__CODE__[self.__CODE_POINTER__] != ']':
                self.__CODE_POINTER__ += 1
        else:
            self.__CODE_POINTER__ += 1

    def __KET__(self):
        """Loop exit (])"""
        if self.__READ_MEMORY__() != 0:
            while self.__CODE__[self.__CODE_POINTER__] != '[':
                self.__CODE_POINTER__ -= 1
        else:
            self.__CODE_POINTER__ += 1

    def __SET_CHR_MODE__(self):
        """Set IO mode to ASCII ($)"""
        self.__CHR_MODE__ = True
        self.__CODE_POINTER__ += 1

    def __SET_INT_MODE__(self):
        """Set IO mode to INT (%)"""
        self.__CHR_MODE__ = False
        self.__CODE_POINTER__ += 1

    def __JMP_MEM__(self):
        """Jump to memory cell with address eq value of current memory cell (^)"""
        shift = self.__READ_MEMORY__() - self.__MEMORY_POINTER__
        if shift > 0:
            for _ in range(shift):
                self.__SHIFT_RIGHT__(__internal_call__=True)
        elif shift < 0:
            for _ in range(abs(shift)):
                self.__SHIFT_LEFT__(__internal_call__=True)
        self.__CODE_POINTER__ += 1

    def __dbg__(self):
        """Debug info"""
        print('------------------------------------------------')
        print(f"Memory pointer: {self.__MEMORY_POINTER__}")
        print(f"Code pointer: {self.__CODE_POINTER__} ({self.__CODE__[self.__CODE_POINTER__]})")
        print(f"IO mode: {'ASCII' if self.__CHR_MODE__ else 'INT'}")
        print(f"Memory neg_shift: -{self.__MEMORY__.__neg_shift__}")
        print(f"Memory: {self.__MEMORY__.__val__[:self.__MEMORY__.__neg_shift__]}:{self.__MEMORY__.__val__[self.__MEMORY__.__neg_shift__]}:{self.__MEMORY__.__val__[self.__MEMORY__.__neg_shift__ + 1:]}")
        print('------------------------------------------------')

    def run(self):
        while self.__CODE_POINTER__ < len(self.__CODE__):
            if self.__DO_DBG__:
                self.__dbg__()

            cmd = self.__CODE__[self.__CODE_POINTER__]
            if cmd == ',':
                self.__INPUT__()
            elif cmd == '.':
                self.__OUTPUT__()
            elif cmd == '>':
                self.__SHIFT_RIGHT__()
            elif cmd == '<':
                self.__SHIFT_LEFT__()
            elif cmd == '+':
                self.__ADD__()
            elif cmd == '-':
                self.__SUB__()
            elif cmd == '[':
                self.__BRA__()
            elif cmd == ']':
                self.__KET__()
            elif cmd == '$':
                self.__SET_CHR_MODE__()
            elif cmd == '%':
                self.__SET_INT_MODE__()
            elif cmd == '^':
                self.__JMP_MEM__()
