import sys

REGISTERS = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111'
}
lab = {}
variables = {}
imm=['mov','rs','ls']

def binaryof(n):
    binary_number = ""
    while n > 0:
        binary_number = str(n % 2) + binary_number
        n //= 2
    while len(binary_number)!=7:
        binary_number='0'+binary_number
    return binary_number

def add(reg1, reg2, reg3):
    i = '00000' + '00' + REGISTERS[reg1] + REGISTERS[reg2] + REGISTERS[reg3]
    print(i)

def sub(reg1, reg2, reg3):
    i = '00001' + '00' + REGISTERS[reg1] + REGISTERS[reg2] + REGISTERS[reg3]
    print(i)

def addf(reg1,reg2,reg3):
    i='10000'+'00'+REGISTERS[reg1]+ REGISTERS[reg2]+REGISTERS[reg3]
    print(i)

def subf(reg1,reg2,reg3):
      i='10001'+'00'+REGISTERS[reg1]+ REGISTERS[reg2]+REGISTERS[reg3]
      print(i)

def mov(reg1, Imm):
    if(int(Imm[1:])>127):
        print("Immediate value should be less than 127.")
        exit()
    i = '00010' + '0' + REGISTERS[reg1] + binaryof(int(Imm[1:]))
    print(i)

def mov_r(reg1, reg2):
    i = '00011' + '00000' + REGISTERS[reg1] + REGISTERS[reg2]
    print(i)

def ld(reg1, addr):
    i = '00100' + '0' + REGISTERS[reg1] + variables[addr]
    print(i)

def st(r, mem_addr):
    i='00101' + '0' + REGISTERS[r] + variables[mem_addr]
    print(i)

def mul(a, b, c):
    i='00110' + '00' + REGISTERS[a] + REGISTERS[b] + REGISTERS[c]
    print(i)

def div(a,b):
    i='00111' + '00000' + REGISTERS[a] + REGISTERS[a]
    print(i)

def rs(a, n):
    i='01000' + '0' + REGISTERS[a] + binaryof(int(n[1:]))
    print(i)

def ls(a,n):
    i='01001' + '0' + REGISTERS[a] + binaryof(int(n[1:]))
    print(i)

def xor(r1, r2, r3):
    i = '01010' + '00' + REGISTERS[r1] + REGISTERS[r2] + REGISTERS[r3]
    print(i)

def c_or(r1, r2, r3):
    i = '01011' + '00' + REGISTERS[r1] + REGISTERS[r2] + REGISTERS[r3]
    print(i)

def a_and(r1, r2, r3):
    i = '01100' + '00' + REGISTERS[r1] + REGISTERS[r2] + REGISTERS[r3]
    print(i)

def I_not(r1, r2):
    i = '01101' + '00000' + REGISTERS[r1] + REGISTERS[r2]
    print(i)

def c_cmp(r1, r2):
    i = '01110' + '00000' + REGISTERS[r1] + REGISTERS[r2]
    print(i)

def jmp(addr):
    i = '01111' + '0000' + lab[addr]
    print(i)

def jlt(addr):
    i = '11100' + '0000' + lab[addr]
    print(i)

def jgt(addr):
    i = '11101' + '0000' + lab[addr]
    print(i)

def je(addr):
    i = '11111' + '0000' + lab[addr]
    print(i)

def hlt():
    i = '1101000000000000'
    print(i)

def assign_label(file):
        i = 0
        for l in file:
            l = l.split()
            if l[0] == 'var':
                continue
            if l[0].endswith(":"):
                key = l[0].strip(":\n")
                lab[key] = binaryof(i)
            i = i + 1

def assign_mem_var(file):
    lines = file
    c = len(lines)
    c1 = 0
    for l1 in lines:
        l1 = l1.split()
        if l1[0] == 'var':
            c1 = c1 + 1
        else:
            break
    c = c - c1
    for line_number, line in enumerate(lines, start=1):
        if line.strip() == '':
            continue
        parts = line.split()
        instruction = parts[0]
        arguments = parts[1:]
        if instruction == 'var':
            var_name = arguments[0]
            variables[var_name] = binaryof(c)
            c = c + 1
        else:
            break
        
def check_hlt(file,i):
    c = 0 
    for l in file:
        c = c + 1
    l = file
    if i < c:
        l1 = l[i-1].split()
        if 'hlt' in l1:
            print("HLT should be only at end - Error at line ", i)
    elif i == c :
        l1 = l[i-1].split()
        if 'hlt' not in l1:
            print("last line should have hlt statement")
        elif l1.count('hlt') > 1:
            print("Error more hlt are there at last line.")
        else:
            hlt()

key = ['R1', 'R2', 'R0', 'R3', 'R4', 'R5', 'R6'] 

file = sys.stdin.readlines()
assign_label(file)
assign_mem_var(file)
var_k = variables.keys()

i = 0
for e in file:
        i = i + 1
        if e != None:
            e = e.split()
            if e[0][-1] == ':':
                if len(e) == 1:
                    continue
                e = e[1:]
            if e == '/n':
                continue
            elif "FLAGS" in e:
                if e[0] == "mov":
                    if e[1] in key:
                        if e[2] == "FLAGS":
                            mov_r(e[1],e[2])
                    elif e[1] == "FLAGS":
                        print("Illegal use of Flag at line ",i)
                    else:
                        print("Different registers used at line ",i)
                else:
                    print("Illegal use of Flag at line ",i)
            elif e[0] == 'add':
                if len(e)==4:
                    if e[1] and e[2] and e[3] in key:
                        add(e[1], e[2], e[3])
                        continue
                    else:
                        print("undefined register used ",i)   
                else:
                    print("Syntax error in line",i)
                    
            elif e[0] == 'sub':
                if len(e)==4: 
                    if e[1] and e[2] and e[3] in key:
                        sub(e[1], e[2], e[3])
                        continue
                    else:
                        print("Other registers used, error in line",i) 
                else:
                    print("syntax error in line",i) 
            elif e[0]=='addf':
                if len(e)==4:
                    if e[1] and e[2] and e[3] in key:
                        addf(e[1],e[2],e[3])
                        continue
                    else:
                        print("undifined register used")

            elif e[0]=='subf':
                if len(e)==4:
                    if e[1] and e[2] and e[3] in key:
                        subf(e[1],e[2],e[3])
                        continue
                    else:
                        print("undifined register used")

            elif e[0] == 'mov':
                if len(e)==3:
                    if e[1] and e[2]  in key:
                        mov_r(e[1], e[2])
                        continue
                    elif e[1] in key:
                        if e[2][0] == '$':
                            mov(e[1],e[2])
                        else:
                            print("Error at line",i,"value should start with $.") 
                    else:
                        print("undefined registers used at line",i)  
                else:
                    print("syntax error in line",i)

            elif e[0] == 'ld':
                if e[1] in key:
                    if e[2] in var_k:
                        ld(e[1], e[2])
                    else:
                        print("uninitialized address used at line",i)
                else:
                    print("wrong register at line ",i)
            
            elif e[0] == 'st':
                if e[1] in key:
                    if e[2] in var_k:
                        st(e[1], e[2])
                    else:
                        print("uninitialized address used at line",i)
                else:
                    print("wrong register at line ",i)

            elif e[0] == 'mul':
                if len(e)==4:
                    if e[1] and e[2] and e[3] in key:
                        mul(e[1], e[2], e[3])
                        continue
                    else:
                        print("different registers used error in line",i)   
                else:
                    print("syntax error in line",i) 
            elif e[0] == 'div':
                if len(e)==3:
                    if e[1] and e[2]  in key:
                        div(e[1], e[2])
                        continue
                    else:
                        print("different registers used error in line",i) 
                else:
                    print("syntax error in line",i)
            elif e[0] == 'rs':
                if e[1] in key:
                    if e[2][0] == '$':
                        rs(e[1], e[2])
                    else:
                            print("Error at line",i,"value should start with $.")
                else:
                    print("undefined registers used at line ",i)

            elif e[0] == 'ls':
                if e[1] in key:
                    if e[2][0] == '$':
                        ls(e[1], e[2])
                    else:
                            print("Error at line",i,"value should start with $.")
                else:
                    print("undefined registers used at line ",i)

            elif e[0] == 'xor':
                if len(e)==4:
                    if e[1] and e[2] and e[3] in key:
                        xor(e[1], e[2], e[3])
                        continue
                    else:
                        print("different registers used, error in line",i)       
                else:
                    print("syntax error in line",i)
            elif e[0] == 'or':
                if len(e)==4:
                    if e[1] and e[2] and e[3] in key:
                        c_or(e[1], e[2], e[3])
                        continue
                    else:
                        print("different registers used, error in line",i)    
                else:
                    print("input error in line",i)
            elif e[0] == 'and':
                if len(e)==4:
                    if e[1] and e[2] and e[3] in key:
                        a_and(e[1], e[2], e[3])
                        continue
                    else:
                        print("different registers used, error in line",i)     
                else:
                    print("syntax error in line",i)
            elif e[0] == 'not':
                if len(e)==3:
                    if e[1] and e[2]  in key:
                        I_not(e[1], e[2])
                        continue
                    else:
                        print("different registers used, error in line",i) 
                else:
                    print("input error in line",i) 
            elif e[0] == 'cmp':
                if len(e)==3:
                    if e[1] and e[2]  in key:
                        c_cmp(e[1], e[2])
                        continue
                    else:
                        print("different registers used, error in line",i) 
                else:
                    print("input error in line",i)
            elif e[0] == 'jmp':   
                if e[1] in lab:
                    jmp(e[1])
                else:
                    print("Invalid label at line",i)
            elif e[0] == 'jlt':
                if e[1] in lab:
                    jlt(e[1])                     
                else:
                    print("Invalid label at line",i)
            elif e[0] == 'jgt':
                if e[1] in lab:
                    jgt(e[1])
                else:
                    print("Invalid label at line",i)
            elif e[0] == 'je':
                if e[1] in lab:
                    je(e[1])
                else:
                    print("Invalid label at line",i)
            elif 'hlt' in e:
                check_hlt(file,i)
            elif e[0] == 'var':
                if e[1] in var_k:
                    continue
                else:
                    print("All variables should be defined at the begining of program Error at line ",i) 
            elif i >= 128:
                exit()
            else:
                print("Syntax Error at line ",i)
                
l = file[-1]
l = l.split()
if 'hlt' not in l:
    print("Last line sholud have hlt statement.")
else:
    if l.count('hlt')>1:
        print("only 1 hlt should be there in last line")
    


 