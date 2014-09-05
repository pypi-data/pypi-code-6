
txt="""L8183    FCS    'DEL'    B5
L8186    FCS    'EDIT'    B6
L818A    FCS    'TRON'    B7
L818E    FCS    'TROFF'    B8
L8193    FCS    'DEF'    B9
L8196    FCS    'LET'    BA
L8199    FCS    'LINE'    BB
L819D    FCS    'PCLS'    BC
L81A1    FCS    'PSET'    BD
L81A5    FCS    'PRESET'    BE
L81AB    FCS    'SCREEN'    BF
L81B1    FCS    'PCLEAR'    C0
L81B7    FCS    'COLOR'    C1
L81BC    FCS    'CIRCLE'    C2
L81C2    FCS    'PAINT'    C3
L81C7    FCS    'GET'    C4
L81CA    FCS    'PUT'    C5
L81CD    FCS    'DRAW'    C6
L81D1    FCS    'PCOPY'    C7
L81D6    FCS    'PMODE'    C8
L81DB    FCS    'PLAY'    C9
L81DF    FCS    'DLOAD'    CA
L81E4    FCS    'RENUM'    CB
L81E9    FCS    'FN'    CC
L81EB    FCS    'USING'    CD 
"""
# txt="""L821E    FCS    'ATN'    94
# L8221    FCS    'COS'    95
# L8224    FCS    'TAN'    96
# L8227    FCS    'EXP'    97
# L822A    FCS    'FIX'    98
# L822D    FCS    'LOG'    99
# L8230    FCS    'POS'    9A
# L8233    FCS    'SQR'    9B
# L8236    FCS    'HEX$'    9C
# L823A    FCS    'VARPTR'    9D
# L8240    FCS    'INSTR'    9E
# L8245    FCS    'TIMER'    9F
# L824A    FCS    'PPOINT'    A0
# L8250    FCS    'STRING$'    A1 """

print("{")
for line in txt.splitlines():
#     print(line.split())
    __,__,token, value=line.split()
    token=token.replace("'",'"')
    value=int(value,16)
#     value+=0xff00
    print(("    0x%02x: %s," % (value, token)))
print("}")