# NeoBrainFuckInterpreter

NeoBrainFuckInterpreter is a Python interpreter for the Brainfuck programming language with additional commands for extended functionality.

## Overview

This interpreter supports the basic Brainfuck commands (`+`, `-`, `<`, `>`, `[`, `]`, `.`, `,`) and introduces three additional commands:

- `$`: Switches IO mode to ASCII.
- `%`: Switches IO mode to integers.
- `^`: Jumps to a memory cell with an address equal to the value of the current memory cell.

The interpreter manages memory using a dynamic stack (`MemoryStack`), allowing for negative indices and dynamic memory expansion.

## Usage

### Installation

Clone the repository:
```bash
git clone https://github.com/kusrabyzarc/NeoBrainF--k.git
cd NeoBrainF--k
```
### Running the Interpreter
Run a Brainfuck program using the interpreter:
```python
from nbfi import NeoBrainFuckInterpreter

code = "+[$,%.]"  # Example Brainfuck program to input a symbol and get its ASCII code
itr = NeoBrainFuckInterpreter(code)
itr.run()
```
### Another Example
```python
from nbfi import NeoBrainFuckInterpreter

code = "%,>,<[->+<]>." # Example Brainfuck program to input 2 numbers and print sum
itr = NeoBrainFuckInterpreter(code, do_debug=True)
itr.run()
```

```plaintext
------------------------------------------------
Memory pointer: 0
Code pointer: 0 (%)
IO mode: ASCII
Memory neg_shift: -0
Memory: []:0:[]
------------------------------------------------
------------------------------------------------
Memory pointer: 0
Code pointer: 1 (,)
IO mode: INT
Memory neg_shift: -0
Memory: []:0:[]
------------------------------------------------
1
------------------------------------------------
Memory pointer: 0
Code pointer: 2 (>)
IO mode: INT
Memory neg_shift: -0
Memory: []:1:[]
------------------------------------------------
------------------------------------------------
Memory pointer: 1
Code pointer: 3 (,)
IO mode: INT
Memory neg_shift: -0
Memory: []:1:[]
------------------------------------------------
2
------------------------------------------------
Memory pointer: 1
Code pointer: 4 (<)
IO mode: INT
Memory neg_shift: -0
Memory: []:1:[2]
------------------------------------------------
------------------------------------------------
Memory pointer: 0
Code pointer: 5 ([)
IO mode: INT
Memory neg_shift: -0
Memory: []:1:[2]
------------------------------------------------
------------------------------------------------
Memory pointer: 0
Code pointer: 6 (-)
IO mode: INT
Memory neg_shift: -0
Memory: []:1:[2]
------------------------------------------------
------------------------------------------------
Memory pointer: 0
Code pointer: 7 (>)
IO mode: INT
Memory neg_shift: -0
Memory: []:0:[2]
------------------------------------------------
------------------------------------------------
Memory pointer: 1
Code pointer: 8 (+)
IO mode: INT
Memory neg_shift: -0
Memory: []:0:[2]
------------------------------------------------
------------------------------------------------
Memory pointer: 1
Code pointer: 9 (<)
IO mode: INT
Memory neg_shift: -0
Memory: []:0:[3]
------------------------------------------------
------------------------------------------------
Memory pointer: 0
Code pointer: 10 (])
IO mode: INT
Memory neg_shift: -0
Memory: []:0:[3]
------------------------------------------------
------------------------------------------------
Memory pointer: 0
Code pointer: 11 (>)
IO mode: INT
Memory neg_shift: -0
Memory: []:0:[3]
------------------------------------------------
------------------------------------------------
Memory pointer: 1
Code pointer: 12 (.)
IO mode: INT
Memory neg_shift: -0
Memory: []:0:[3]
------------------------------------------------
3 
```
### License
This project is licensed under the MIT License - see the LICENSE file for details.