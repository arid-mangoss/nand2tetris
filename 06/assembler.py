
compTable = {
    '0': '101010',
    '1': '111111',
    '-1': '111010',
    'D': '001100',
    'A': '0110000',
    '!D': '001101',
    '!A': '0110001',
    '-D': '001111',
    '-A': '0110011',
    'D+1': '011111',
    'A+1': '0110111',
    'D-1': '001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101'
}

jumpTable = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111'
}

destTable = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111'
}

symbols = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576
}


''' --- parsing --- '''

fileContents = None
with open('add/Add.asm', 'r') as f:
    fileContents = f.readlines()


def trim(line):
    line = line.lstrip()
    line = line.split(r'//')
    return line[0]

def commandType(line):
    if line[0]=='@':
        return 'A_COMMAND'
    elif line[0] == '(':
        return 'L_COMMAND'
    else: 
        return 'C_COMMAND'

def dest(line):
    return line.split('=')[0]

def comp(line):
    line = line.split('=')[1]
    line = line.split(';')[0]

    return line


def jump(line):
    line = line.split('=')[1]
    line = line.split(';')

    if len(line) != 2:
        return 'null'
    else:
        return line[1]

def convertDest(dest):
    return destTable.get(dest)

def convertComp(comp):
    return compTable.get(comp)

def convertJump(jump):
    return jumpTable.get(jump)

def firstPass():
    for line in fileContents:
        