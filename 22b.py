import json

word_size = 64
mod_mask = (2 ** word_size) - 1

def calculate_xor(x, y):
    ls_1_x = ((x >> (word_size - 1)) + (x << 1)) & mod_mask
    ls_8_x = ((x >> (word_size - 8)) + (x << 8)) & mod_mask
    ls_2_x = ((x >> (word_size - 2)) + (x << 2)) & mod_mask

    # XOR Chain
    xor_1 = (ls_1_x & ls_8_x) ^ y
    xor_2 = xor_1 ^ ls_2_x

    return xor_2

def encrypt(x, y, k):
    xor = calculate_xor(x, y)

    new_xor = xor ^ k
    return new_xor

def calculate_bit(i , entries):

    # find all zeros in i th position
    zero_entries = []
    for entry in entries:
        if entry[2][i] == "0":
            zero_entries.append(entry)

    # calculate average ones
    sum_zero_one = 0
    for entry in zero_entries:
        sum_zero_one += entry[3]

    avg_zero_one = sum_zero_one/len(zero_entries)
    #print (avg_zero_one)

    # find all ones in i th position
    one_entries = []
    for entry in entries:
        if entry[2][i] == "1":
            one_entries.append(entry)

    # calculate average ones
    sum_one_one = 0
    for entry in one_entries:
        sum_one_one += entry[3]

    avg_one_one = sum_one_one/len(one_entries)
    #print (avg_zero_one + avg_one_one)

    if avg_zero_one < avg_one_one:
        return 0
    return 1


def calculate_round_keys(entries):

    round_keys = []

    for i in range(68):
        round_key = ""
        for j in range(64):
            bit = str(calculate_bit(j, entries))
            round_key += bit

        for index in range(len(entries)):
            entry = entries[index]

            int_key = int(round_key, 2)

            encrypted = encrypt(entry[0], entry[1], int_key)
            new_xor = "{0:064b}".format(calculate_xor(encrypted, entry[0]))
            entries[index] = [encrypted, entry[0], new_xor, entry[3]]

        round_keys.append(round_key)
    return round_keys


if __name__ == '__main__':


    samples = json.load(open('samples.json'))
    test_key = "01010110100111111010110010110010000101110000001011011100000101010110111101011100101000111111010000110010001001011100100010111010"
    #print(samples[0])

    entries = []

    for index in range(len(samples)):

        current_sample = samples[index]
        current_plain_text = current_sample[0]
        current_one_count = current_sample[1]
        binary_pt = "{0:0128b}".format(current_plain_text)
        pt1 = int(binary_pt[:64], 2)
        pt2 = int(binary_pt[64:], 2)
        xor = "{0:064b}".format(calculate_xor(pt1, pt2))
        #print(xor)
        entries.append([pt1, pt2, xor, current_one_count])



    round_keys = calculate_round_keys(entries)
    for round_key in round_keys:
        print(round_key)

    master_key = round_keys[1] + round_keys[0]

    print("Key is {}".format(master_key))
    #print(test_key == master_key)
    print(len(round_keys))
