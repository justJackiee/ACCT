from operator import xor

key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
key2_key1 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
key2_key3 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
flag_key1_key2_key3 = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"


bytes_key1 = bytes.fromhex(key1)
bytes_key12 = bytes.fromhex(key2_key1)
bytes_key23 = bytes.fromhex(key2_key3)
bytes_key123 = bytes.fromhex(flag_key1_key2_key3)

def xor_bytes(b1,b2):
    return bytes(a ^ b for a, b in zip(b1,b2))

key2 = xor_bytes(bytes_key1, bytes_key12)
key3 = xor_bytes(bytes_key23, key2)
flag = xor_bytes(bytes_key123, xor_bytes(bytes_key1, xor_bytes(key2, key3)))
print(flag.decode())