def list2dec(bit_list):
    '''
        list2dec(bit_list):
        Convert a list of bits to its decimal representation.
        Parameters:
            bit_list (list): A list of bits (0s and 1s).
        Returns:
            int: The decimal representation of the bit list.
    '''
    decimal_value = 0
    bit_length = len(bit_list)
    for i in range(bit_length):
        decimal_value = decimal_value * 2 + bit_list[i]
    return decimal_value