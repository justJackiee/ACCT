import hashlib
import requests

# Ciphertext from the challenge
ciphertext = "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"
base_url = "https://aes.cryptohack.org/passwords_as_keys"

# URL for the word list
word_list_url = "https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"

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
            
        # Generate MD5 hash of the word
        password_hash = hashlib.md5(word.encode()).hexdigest()
        
        # Use the API to decrypt
        decrypt_url = f"{base_url}/decrypt/{ciphertext}/{password_hash}/"
        response = requests.get(decrypt_url)
        data = response.json()
        
        if "plaintext" in data:
            plaintext_hex = data["plaintext"]
            try:
                plaintext = bytes.fromhex(plaintext_hex).decode('utf-8')
                if "crypto{" in plaintext:
                    print(f"Found flag with word '{word}': {plaintext}")
                    return
            except:
                pass
    
    print("No valid decryption found.")

# Run the attack
if __name__ == "__main__":
    crack_password()