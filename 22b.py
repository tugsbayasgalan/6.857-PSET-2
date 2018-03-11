import json
from os import urandom
from struct import unpack
from simon import SimonCipher



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
    sum_one = 0
    for entry in zero_entries:
        sum_one += entry[3]

    avg_one = sum_one/len(zero_entries)
    #print (avg_one)

    if avg_one <= 4352: # 128*68/2
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



        #print(round_key)
        round_keys.append(round_key)
    return round_keys





if __name__ == '__main__':


    samples = json.load(open('test_samples.json'))
    print(samples[0])

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
    print(len(round_keys))
