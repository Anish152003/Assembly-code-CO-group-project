def float_to_binary_IEEE754(num):
    # Check for special cases: 0, infinity, and NaN
    if num == 0:
        return '0' * 16
    elif num == float('inf'):
        return '0111111100000000'
    elif num == float('-inf'):
        return '1111111100000000'
    elif num != num:  # NaN check (NaN != NaN)
        return '0111111111111111'

    # Determine the sign bit
    if num < 0:
        sign_bit = '1'
        num = abs(num)
    else:
        sign_bit = '0'

    # Convert the number to binary
    binary = ''
    whole_part = int(num)
    fractional_part = num - whole_part

    # Convert the whole part to binary
    while whole_part > 0:
        binary = str(whole_part % 2) + binary
        whole_part //= 2

    # Convert the fractional part to binary
    binary += '.'

    while fractional_part > 0:
        if len(binary) >= 16:  # Maximum length for 16-bit representation
            break
        fractional_part *= 2
        bit = int(fractional_part)
        if bit == 1:
            fractional_part -= bit
            binary += '1'
        else:
            binary += '0'

    # Normalize the binary representation
    exponent = binary.index('.') - 1
    binary = binary.replace('.', '')
    mantissa = binary[1:]

    # Adjust the exponent based on the bias (3-bit exponent: bias = 2^(3-1) - 1 = 3)
    exponent += 3

    # Convert the exponent to binary with leading zeros
    exponent_bits = format(exponent, '03b')

    # Convert the mantissa to binary with leading zeros
    mantissa_bits = mantissa.ljust(5, '0')[:5]

    # Combine the sign bit, exponent bits, and mantissa bits
    binary_IEEE754 = exponent_bits + mantissa_bits + '0' * 8

    return binary_IEEE754

num = 3.14159
binary = float_to_binary_IEEE754(num)
print(binary)
