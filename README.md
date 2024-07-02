# NeoBrainFuckInterpreter

NeoBrainFuckInterpreter is a Python interpreter for the Brainfuck programming language with additional commands for extended functionality.

## Overview

This interpreter supports the basic Brainfuck commands (`+`, `-`, `<`, `>`, `[`, `]`, `.`, `,`) and introduces three additional commands:

- `$`: Switches IO mode to ASCII.
- `%`: Switches IO mode to integers.
- `^`: Jumps to memory cell with address which equals the value of current memory cell.
- `&`: Jumps to the instruction with address which equals the value of current memory cell.
- `0`: NOP (No operation)

The interpreter manages memory using a dynamic stack (`MemoryStack`), allowing for negative indices and dynamic memory expansion.

## Usage

### Installation

Clone the repository:
```bash
git clone https://github.com/kusrabyzarc/NeoBrainF--k.git
cd NeoBrainF--k
```

### Interpreter args
```text
code: [str] BrainFuck code
do_debug: [bool] print debug info (default: False)
vanilla_cell_behaviour: [bool] clamp the values in memory to the range 0-255 (default: False)
vanilla_memory_stack: [bool] use static 30k-sized memory stack instead of dynamic one (default: False)
```
### Examples
~~You can find examples [here](https://github.com/kusrabyzarc/NeoBrainF--k/tree/main/examples).~~\
In progress.

### License
This project is licensed under the MIT License - see the LICENSE file for details.