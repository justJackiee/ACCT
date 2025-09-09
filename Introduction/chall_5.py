string = "label"

new_string = ''.join(chr(ord(c)^13) for c in string)

print(new_string)
