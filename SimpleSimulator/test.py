def binary_to_decimal(binary):
    decimal = 0
    for bit in binary:
        decimal = decimal * 2 + int(bit)
    return decimal

binary_number = "0000010"
decimal_number = binary_to_decimal(binary_number)
print(decimal_number)