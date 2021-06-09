import re
import sys

compTable = {
    '0':   '0101010',
    '1':   '0111111',
    '-1':  '0111010',
    'D':   '0001100',
    'A':   '0110000',
    '!D':  '0001101',
    '!A':  '0110001',
    '-D':  '0001111',
    '-A':  '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M':   '1110000',
    '!M':  '1110001',
    '-M':  '1110011',
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
ramAddress = 16

fileContents = None
with open(sys.argv[1], 'r') as f:
    fileContents = f.read().splitlines()


def trim(line):
    line = line.lstrip()
    line = line.split(r'//')
    return line[0]


def commandType(line):
    if line[0] == '@':
        return 'A_COMMAND'
    elif line[0] == '(':
        return 'L_COMMAND'
    else:
        return 'C_COMMAND'


def dest(line):
    line = line.split('=')
    if len(line) == 2:
        return line[0].strip()
    else:
        return 'null'


def comp(line):
    line = line.split(';')[0]
    line = line.split('=')
    if len(line) == 2:
        line = line[1]
    else:
        line = line[0]

    return line.strip()


def jump(line):
    line = re.split(';', line)

    if len(line) != 2:
        return 'null'
    else:
        return line[1].strip()


def convertDest(dest):
    return destTable.get(dest)


def convertComp(comp):
    return compTable.get(comp)


def convertJump(jump):
    return jumpTable.get(jump)


def convertA(line):
    global ramAddress
    variable = line.split('@')[1]
    if symbols.get(variable) is not None:
        val = symbols.get(variable)
    else:
        if variable.isnumeric():
            val = int(variable)
        else:  # is a new variable
            symbols[variable] = ramAddress
            ramAddress += 1
            val = ramAddress

    binVal = bin(val).split('b')[1].zfill(16)
    return binVal


def convertC(line):
    c = convertComp(comp(line))
    d = convertDest(dest(line))
    j = convertJump(jump(line))
    print('\n', line, c, d, j,  comp(line), dest(line), jump(line))
    return ('111'+c+d+j)


def firstPass():
    count = 0
    for line in fileContents:
        line = trim(line)
        if line is None or len(line) == 0:
            continue  # go to next line
        command = commandType(line)
        if command == 'L_COMMAND':
            variableName = re.split('\(|\)', line)[1]
            symbols[variableName] = count
        else:
            count += 1


def secondPass():
    outputStrings = []
    for line in fileContents:
        line = trim(line)
        if line is None or len(line) == 0:  # blank or comment
            continue
        command = commandType(line)
        if command == 'A_COMMAND':
            convert = convertA(line)
        elif command == 'C_COMMAND':
            convert = convertC(line)
        else:
            continue

        outputStrings.append(convert)
    return outputStrings


def main():
    firstPass()
    outputStrings = secondPass()
    print("\nthe result is: ")
    print('\n'.join(outputStrings))

    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w') as f:
            f.write('\n'.join(outputStrings))

main()
