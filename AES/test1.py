from Cryptodome.Cipher import AES
import hashlib
import requests

# Ciphertext from the challenge
ciphertext = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"

# URL for the word list
word_list_url = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"

# Function to try decrypting with a word
def try_decrypt_with_word(word, ciphertext_hex):
    # Generate key from word
    key = hashlib.md5(word.encode()).digest()
    
    # Set up cipher
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Decrypt
    try:
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
        decrypted = cipher.decrypt(ciphertext_bytes)
        
        # Check if result looks like a flag (crypto{...})
        try:
            decrypted_text = decrypted.decode('utf-8')
            if 'crypto{' in decrypted_text:
                return decrypted_text
        except:
            pass
        
        return None
    except Exception as e:
        return None

# Main function
def crack_password():
    # Download word list
    response = requests.get(word_list_url)
    words = [w.strip() for w in response.text.splitlines()]
    
    print(f"Downloaded {len(words)} words. Starting attack...")
    
    # Try each word
    for i, word in enumerate(words):
        if i % 1000 == 0:
            print(f"Tried {i} words...")
            
        result = try_decrypt_with_word(word, ciphertext)
        if result:
            print(f"Found flag with word '{word}': {result}")
            return
    
    print("No valid decryption found.")

# Run the attack
if __name__ == "__main__":
    crack_password()