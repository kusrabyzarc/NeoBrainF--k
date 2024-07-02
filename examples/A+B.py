from neobrainfuck.core import NeoBrainFuckInterpreter

code = '''
    %           set mode INT
    ,>          input A
    ,           input B
    [-<+>]      B-1 and A+1 while B != 0
    <.          goto A and output
'''

itr = NeoBrainFuckInterpreter(code=code)
itr.run()
