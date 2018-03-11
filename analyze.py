from simon import SimonCipher
import json

key = "01110010111011111100001011001110000010110111011110101110011111111110111110100100111001000100111001111011000111101011001010010110"
string_key = int(key, 2)
print(hex(string_key))

simon = SimonCipher(0x72efc2ce0b77ae7fefa4e44e7b1eb296, key_size=128)

entries = json.load(open("samples.json", "r"))
counter = 0
for entry in entries:
    text = hex(entry[0])
    #print(type(text))
    a, b = simon.encrypt(int(text, 16))

    if b == entry[1]:
        counter += 1

print("{} correct out of {}".format(counter, len(entries)))
