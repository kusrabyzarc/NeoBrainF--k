class MemoryStack:
    def __init__(self, vanilla):
        self.__vanilla__ = vanilla
        if self.__vanilla__:
            self.__val__ = [0 for _ in range(30_000)]
        else:
            self.__val__ = [0]
        self.__neg_shift__ = 0

    def __getitem__(self, item):
        if not isinstance(item, (int, slice)):
            raise TypeError(f'MemoryStack indices must be int or slice, not {type(item)}')

        if self.__vanilla__:
            throw_error = False
            if self.__neg_shift__ != 0:
                throw_error = True
            if isinstance(item, slice):
                start = item.start or 0
                stop = item.stop or len(self.__val__)
                if start not in range(30_000) or stop not in range(30_000):
                    throw_error = True
            if isinstance(item, int):
                if item not in range(30_000):
                    throw_error = True
            if throw_error:
                raise IndexError(f'vanilla stack out of range ({item}).')

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

        if self.__vanilla__:
            if key not in range(30_000):
                raise IndexError(f'vanilla stack out of range ({key}).')

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
    """
    NeoBrainFuck interpreter class.
    """

    def __init__(self, code: str, *, do_debug: bool = False, vanilla_cell_behaviour: bool = False,
                 vanilla_memory_stack: bool = False):
        """
        :param code: [str] BrainFuck code
        :param do_debug: [bool] print debug info (default: False)
        :param vanilla_cell_behaviour: [bool] clamp values in memory to range 0-255 (default: False)
        :param vanilla_memory_stack: [bool] use static 30k-sized memory stack instead of dynamic (default: False)
        """
        self.__ALLOWED_COMMANDS__ = [',', '.', '>', '<', '+', '-', '[', ']', '$', '%', '^', '&', '0']
        if isinstance(code, str):
            self.obj = code
        else:
            raise TypeError(f'Expected str object, but {type(code)} found.')
        self.__CODE__ = list(filter(lambda x: x in self.__ALLOWED_COMMANDS__, self.obj))
        self.__MEMORY__ = MemoryStack(vanilla=vanilla_memory_stack)
        self.__CHR_MODE__ = True
        self.__DO_DBG__ = do_debug
        self.__MEMORY_POINTER__ = 0
        self.__CODE_POINTER__ = 0
        self.__BRA_KET_VALIDATION__()
        self.__VANILLA_CELL__ = vanilla_cell_behaviour

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
            raise ValueError('Bra-Ket validation failed.')

    def __ADD__(self):
        """Add 1 to current cell (+)"""
        self.__MEMORY__[self.__MEMORY_POINTER__] += 1
        if self.__VANILLA_CELL__:
            self.__MEMORY__[self.__MEMORY_POINTER__] %= 256
        self.__CODE_POINTER__ += 1

    def __SUB__(self):
        """Subtract 1 from current cell (-)"""
        self.__MEMORY__[self.__MEMORY_POINTER__] -= 1
        if self.__VANILLA_CELL__ and self.__MEMORY__[self.__MEMORY_POINTER__] < 0:
            self.__MEMORY__[self.__MEMORY_POINTER__] = 255
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
        """Switches IO mode to ASCII ($)"""
        self.__CHR_MODE__ = True
        self.__CODE_POINTER__ += 1

    def __SET_INT_MODE__(self):
        """Switches IO mode to integers (%)"""
        self.__CHR_MODE__ = False
        self.__CODE_POINTER__ += 1

    def __JMP_MEM__(self):
        """Jumps to memory cell with address which equals the value of current memory cell (^)"""
        shift = self.__READ_MEMORY__() - self.__MEMORY_POINTER__
        if shift > 0:
            for _ in range(shift):
                self.__SHIFT_RIGHT__(__internal_call__=True)
        elif shift < 0:
            for _ in range(abs(shift)):
                self.__SHIFT_LEFT__(__internal_call__=True)
        self.__CODE_POINTER__ += 1

    def __JMP_CODE__(self):
        """Jumps to the instruction with address which equals the value of current memory cell (&)"""
        value = self.__READ_MEMORY__()
        if len(self.__CODE__) <= value or 0 > value:
            raise IndexError(f'tried to jump instruction {value}, but code address range is 0-{len(self.__CODE__)-1}')
        self.__CODE_POINTER__ = value

    def __NOP__(self):
        """No operation (0)"""
        self.__CODE_POINTER__ += 1

    def __dbg__(self):
        """Debug info"""
        print('------------------------------------------------')
        print(f"Memory pointer: {self.__MEMORY_POINTER__}")
        print(f"Code pointer: {self.__CODE_POINTER__} ({self.__CODE__[self.__CODE_POINTER__]})")
        print(f"IO mode: {'ASCII' if self.__CHR_MODE__ else 'INT'}")
        if not self.__MEMORY__.__vanilla__:
            print(f"Memory neg_shift: {-self.__MEMORY__.__neg_shift__}")
        print(
            f"Memory: {self.__MEMORY__.__val__[:self.__MEMORY__.__neg_shift__]}:[{self.__MEMORY__.__val__[self.__MEMORY__.__neg_shift__]}]:{self.__MEMORY__.__val__[self.__MEMORY__.__neg_shift__ + 1:]}")
        print('------------------------------------------------')

    def run(self):
        while self.__CODE_POINTER__ < len(self.__CODE__):
            if self.__MEMORY__.__vanilla__ and self.__MEMORY_POINTER__ not in range(30_000):
                raise IndexError(f'vanilla stack out of range ({self.__MEMORY_POINTER__}).')
            if self.__DO_DBG__:
                self.__dbg__()

            cmd = self.__CODE__[self.__CODE_POINTER__]
            match cmd:
                case ',':
                    self.__INPUT__()
                case '.':
                    self.__OUTPUT__()
                case '>':
                    self.__SHIFT_RIGHT__()
                case '<':
                    self.__SHIFT_LEFT__()
                case '+':
                    self.__ADD__()
                case '-':
                    self.__SUB__()
                case '[':
                    self.__BRA__()
                case ']':
                    self.__KET__()
                case '$':
                    self.__SET_CHR_MODE__()
                case '%':
                    self.__SET_INT_MODE__()
                case '^':
                    self.__JMP_MEM__()
                case '&':
                    self.__JMP_CODE__()
                case '0':
                    self.__NOP__()
