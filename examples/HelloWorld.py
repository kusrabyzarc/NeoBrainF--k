from neobrainfuck.core import NeoBrainFuckInterpreter

# Source: https://habr.com/ru/articles/133087/
code = '''
++++++++++[>+++++++>++++++++++>+++<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.
'''

itr = NeoBrainFuckInterpreter(code=code, vanilla_memory_stack=True, vanilla_cell_behaviour=True, do_debug=False)
itr.run()
