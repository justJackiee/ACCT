hex_strings = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

new_string = bytes.fromhex(hex_strings)
for i in range(1,100):
    print(''.join(chr(b^i) for b in new_string))
