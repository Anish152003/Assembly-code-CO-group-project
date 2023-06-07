#                          ------------------------------declaring some global variables---------------------------- 
import sys
PC = '0000000'  

mem = {}
instruction = {}

RF = {'000':'0000000000000000',
      '001':'0000000000000000',
      '010':'0000000000000000',
      '011':'0000000000000000',
      '100':'0000000000000000',
      '101':'0000000000000000',
      '110':'0000000000000000',
      '111':'0000000000000000'
}

#                                =================-------------helper functions-------------==============

def printf():
    print(f"{PC}        {RF['000']} {RF['001']} {RF['010']} {RF['011']} {RF['100']} {RF['101']} {RF['110']} {RF['111']}")
    
def binary_to_decimal(binary):
    decimal = 0
    for bit in binary:
        decimal = decimal * 2 + int(bit)
    return decimal

def decimal_to_binary(decimal):
    binary = bin(decimal)[2:]  # Convert decimal to binary string, excluding the '0b' prefix
    padding = 7 - len(binary)  # Calculate the number of leading zeros needed
    if padding < 0:
        raise ValueError("Number cannot be represented in 7 bits")
    binary = "0" * padding + binary  # Add leading zeros
    return binary

def add_binary_numbers(a, b):  #returns 7 bit binary
    # Ensure both numbers have the same length
    if len(a) != len(b):
        raise ValueError("Input numbers must have the same length")
    # Reverse the input strings for easier addition
    a = a[::-1]
    b = b[::-1]
    carry = 0
    result = []
    for i in range(len(a)):
        bit_a = int(a[i])
        bit_b = int(b[i])
        sum_bits = bit_a + bit_b + carry
        bit_result = sum_bits % 2
        carry = sum_bits // 2
        result.append(str(bit_result))
    if carry != 0:
        result.append(str(carry))
    # Reverse the result string
    result = ''.join(result[::-1])
    return result

def complement(binary):
    # Invert all the bits in the binary string
    complemented = ''.join('1' if bit == '0' else '0' for bit in binary)
    return complemented

def dec_bin(decimal):          
    binary = bin(decimal)[2:]  
    binary = binary.zfill(16)  
    return binary
#                                       =================-------------main functions-------------==============

    
def add(r1,r2,r3):
    RF[r1] = add_binary_numbers(RF[r2],RF[r3])
    if(len(RF[r1])>16):
        RF[r1] = '0000000000000000'
        RF['111'] = '0000000000001000'
    printf()

def sub(r1, r2, r3):
    # Check if reg3 > reg2
    if RF[r3] > RF[r2]:
        RF[r1] = '0000000000000000'  # Set reg1 to 0
        RF['111'] = '0000000000001000'  # Set overflow flag
    else:
        # Perform subtraction
        p = complement(RF[r3])
        p = add_binary_numbers(p, '0000000000000001')
        if len(p) > 16:
            p = p[1:]
        RF[r1] = add_binary_numbers(RF[r2], p)
        if len(RF[r1]) > 16:
            RF[r1] = RF[r1][1:]
    printf() 
    
def mul(r1, r2, r3):
    result = bin(int(RF[r2], 2) * int(RF[r3], 2))[2:].zfill(16)
    if len(result) > 16:
        RF[r1] = '0000000000000000'
        RF['111'] = '0000000000001000'
    else:
        RF[r1] = result
    printf()
    
def div(r3, r4):
    quotient = 0
    remainder = 0

    if RF[r4] == '0000000000000000':
        RF['111'] = '0000000000001000'
        RF['000'] = '0000000000000000'
        RF['001'] = '0000000000000000'
        printf()
        return

    dividend = int(RF[r3], 2)
    divisor = int(RF[r4], 2)

    quotient = dividend // divisor
    remainder = dividend % divisor
    print(quotient)
    print(remainder)
    RF['000'] = dec_bin(quotient)
    RF['001'] = dec_bin(remainder)
    printf()
    
def xor(r1,r2,r3):
    # Convert the input binary numbers to integers
    int1 = int(RF[r2], 2)
    int2 = int(RF[r3], 2)
    
    # Perform the bitwise XOR operation
    result = int1 ^ int2
    
    # Convert the result back to a 16-bit binary number
    RF[r1] = bin(result)[2:].zfill(16)
    printf()
    
def Or(r1, r2,r3):
    # Convert the input binary numbers to integers
    int1 = int(RF[r2], 2)
    int2 = int(RF[r3], 2)
    
    # Perform the bitwise OR operation
    result = int1 | int2
    
    # Convert the result back to a 16-bit binary number
    RF[r1] = bin(result)[2:].zfill(16)
    printf()

def And(r1,r2, r3):
    # Convert the input binary numbers to integers
    int1 = int(RF[r2], 2)
    int2 = int(RF[r3], 2)
    
    # Perform the bitwise AND operation
    result = int1 & int2
    
    # Convert the result back to a 16-bit binary number
    RF[r1] = bin(result)[2:].zfill(16)
    printf()
    
def Not(r1,r2):
    # Convert the input binary number to an integer
    integer = int(RF[r2], 2)
    
    # Perform the bitwise NOT operation
    result = ~integer
    
    # Apply a bitmask to limit the result to 16 bits
    result = result & 0xFFFF
    
    # Convert the result back to a 16-bit binary number
    RF[r1] = bin(result)[2:].zfill(16)
    printf()

def cmp(r1,r2):
    # Convert the input binary numbers to integers
    int1 = int(RF[r1], 2)
    int2 = int(RF[r2], 2)
    
    # Perform the bitwise AND operation
    if int1 > int2 :
        RF['111'] = '0000000000000010'
    elif int1 < int2 :
        RF['111'] = '0000000000000100'
    elif int1==int2:
        RF['111']='0000000000000001'
    printf()
    
def jmp(instruction_addr):
    printf()

def jlt(instruction_addr):
    if RF['111']=='0000000000000100':
        PC=instruction_addr
    printf()

def jgt(instruction_addr):
    if RF['111']=='0000000000000010':
        PC=instruction_addr
    printf()

def je(instruction_addr):
    if RF['111']=='0000000000000001':
        PC=instruction_addr
    printf()

def movi(r1, Imm):
    Imm = Imm.zfill(16)
    RF[r1] = Imm
    printf()  
    
def store(r1, instruction_addr):
    mem[instruction_addr] = RF[r1]
    printf()
   
def load(r1, instruction_addr):
    RF[r1] = mem[instruction_addr]
    printf()  
    
def mov_r(r1, r2):
    RF[r1] = RF[r2]
    printf()
    
def rs(r1, Imm):
    shift_amount = int(Imm, 2)
    RF[r1] = RF[r1][-shift_amount:].zfill(16)
    printf()  
    
def ls(r1, Imm):
    shift_amount = int(Imm, 2)
    RF[r1] = RF[r1][shift_amount:].ljust(16, '0')
    printf()
    
#                                     >>>>>>>>>>>>>--------------main program starts here---------------<<<<<<<<<<<<<<
#initializing memory 
for j in range(124):
    mem[decimal_to_binary(j)] = '0000000000000000'

# initializing binary instructions(reading from file)
#with open('input.txt', 'r') as file:
#    lines = file.readlines()
#    lines = [l.strip('\n') for l in lines]
lines = sys.stdin.readlines()
i = 0
c = 0
while i < len(lines):
    if len(lines[i]) > 16:
        i = i + 1
        continue
    instruction[decimal_to_binary(c)] = lines[i]
    if(lines[i] == '1101000000000000'):
        break
    c = c + 1
    i = i + 1
    
# Execution engine

#print(len(instruction))

pc1 = list(instruction.keys())
i = 0
while i < len(pc1):
    PC = pc1[i]
    if instruction[PC][:5] == '00000':
        add(instruction[PC][7:10],instruction[PC][10:13],instruction[PC][13:])
    elif instruction[PC][:5] == '00001':
        sub(instruction[PC][7:10],instruction[PC][10:13],instruction[PC][13:])
    elif instruction[PC][:5] == '00010':
        movi(instruction[PC][6:9],instruction[PC][9:])
    elif instruction[PC][:5] == '00011':
        mov_r(instruction[PC][10:13],instruction[PC][13:])
    elif instruction[PC][:5] == '00100':
        load(instruction[PC][6:9],instruction[PC][9:])
    elif instruction[PC][:5] == '00101':
        store(instruction[PC][6:9],instruction[PC][9:])
    elif instruction[PC][:5] == '00110':
        mul(instruction[PC][7:10],instruction[PC][10:13],instruction[PC][13:])
    elif instruction[PC][:5] == '00111':
        div(instruction[PC][10:13],instruction[PC][13:])
    elif instruction[PC][:5] == '01000':
        rs(instruction[PC][6:9],instruction[PC][9:])
    elif instruction[PC][:5] == '01001':
        ls(instruction[PC][6:9],instruction[PC][9:])
    elif instruction[PC][:5] == '01010':
        xor(instruction[PC][7:10],instruction[PC][10:13],instruction[PC][13:])
    elif instruction[PC][:5] == '01011':
        Or(instruction[PC][7:10],instruction[PC][10:13],instruction[PC][13:])
    elif instruction[PC][:5] == '01100':
        And(instruction[PC][7:10],instruction[PC][10:13],instruction[PC][13:]) 
    elif instruction[PC][:5] == '01101':
        Not(instruction[PC][10:13],instruction[PC][13:]) 
    elif instruction[PC][:5] == '01110':
        cmp(instruction[PC][10:13],instruction[PC][13:]) 
    elif instruction[PC][:5] == '01111':
        i = binary_to_decimal(instruction[PC][9:])
        PC = pc1[i]
        i = i - 1
        printf()
    elif instruction[PC][:5] == '11100':
        if RF['111']=='0000000000000100':
            i = binary_to_decimal(instruction[PC][9:])
            PC = pc1[i]
            i = i - 1
            RF['111'] = '0000000000000000'
        printf()
    elif instruction[PC][:5] == '11101':
        if RF['111']=='0000000000000010':
            i = binary_to_decimal(instruction[PC][9:])
            PC = pc1[i]
            i = i - 1
            RF['111'] = '0000000000000000'
        printf()
    elif instruction[PC][:5] == '11111':
        if RF['111']=='0000000000000001':
            i = binary_to_decimal(instruction[PC][9:])
            PC = pc1[i]
            i = i - 1
            RF['111'] = '0000000000000000'
        printf()
    elif instruction[PC][:5] == '11010':
        printf()
        break
    i = i + 1

for j in instruction.values():
    print(j)
for i in mem.values():
    print(i)