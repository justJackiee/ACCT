#!/usr/bin/env python3

import requests
import string

class LiveECBAttack:
    def __init__(self, base_url):
        self.base_url = base_url
        self.block_size = 16
        
    def encrypt(self, plaintext_bytes):
        """Send plaintext to oracle and get ciphertext"""
        plaintext_hex = plaintext_bytes.hex()
        url = f"{self.base_url}/ecb_oracle/encrypt/{plaintext_hex}/"
        
        try:
            response = requests.get(url)
            return response.json()["ciphertext"]
        except Exception as e:
            print(f"Error: {e}")
            return None

    def find_block_size_and_flag_length(self):
        """Determine block size and approximate flag length"""
        print("🔍 Analyzing encryption behavior...")
        
        # Test with increasing input sizes
        lengths = []
        for i in range(50):
            plaintext = b'A' * i
            ciphertext = self.encrypt(plaintext)
            if ciphertext:
                lengths.append(len(ciphertext))
                
        print("Input length -> Ciphertext length:")
        for i, length in enumerate(lengths[:20]):
            print(f"  {i:2d} -> {length}")
            
        # Find when length jumps (indicates new block)
        block_size = None
        for i in range(1, len(lengths)):
            if lengths[i] > lengths[i-1]:
                block_size = lengths[i] - lengths[i-1]
                print(f"📏 Detected block size: {block_size//2} bytes")
                break
        
        return block_size//2 if block_size else 16

    def extract_flag(self):
        """Extract flag using ECB oracle attack"""
        print("🎯 Starting ECB Oracle Attack...")
        
        flag = b""
        charset = string.printable.encode()
        
        # Start with no input to see baseline
        baseline_ct = self.encrypt(b"")
        print(f"Baseline ciphertext length: {len(baseline_ct)} chars")
        
        for byte_position in range(100):  # Try up to 100 characters
            print(f"\n🔎 Extracting byte {byte_position + 1}...")
            
            # Calculate padding needed to align the target byte at end of block
            padding_length = (15 - byte_position) % 16
            padding = b'A' * padding_length
            
            print(f"Using {padding_length} padding bytes")
            
            # Get target ciphertext (what we're trying to match)
            target_ciphertext = self.encrypt(padding)
            if not target_ciphertext:
                print("❌ Failed to get target ciphertext")
                break
                
            # Determine which block contains our target
            total_prefix_len = padding_length + byte_position
            target_block_idx = total_prefix_len // 16
            
            if target_block_idx * 32 + 32 > len(target_ciphertext):
                print(f"🏁 Reached end of ciphertext")
                break
                
            target_block = target_ciphertext[target_block_idx*32:(target_block_idx+1)*32]
            print(f"Target block {target_block_idx}: {target_block}")
            
            # Try each possible byte
            found = False
            for test_byte in charset:
                # Create our test input: padding + known_flag + guess
                test_input = padding + flag + bytes([test_byte])
                
                # Make sure we're testing the right alignment
                test_ciphertext = self.encrypt(test_input)
                if not test_ciphertext:
                    continue
                
                # Get the corresponding block from test
                test_block = test_ciphertext[target_block_idx*32:(target_block_idx+1)*32]
                
                # Check if blocks match
                if test_block == target_block:
                    flag += bytes([test_byte])
                    char_display = chr(test_byte) if 32 <= test_byte <= 126 else f"\\x{test_byte:02x}"
                    print(f"✅ Found: '{char_display}'")
                    print(f"🚩 Flag so far: {flag.decode('utf-8', errors='ignore')}")
                    found = True
                    
                    # Check if we found the flag end
                    if test_byte == ord('}') and b'{' in flag:
                        print(f"\n🎉 COMPLETE FLAG EXTRACTED! 🎉")
                        print(f"🏆 Final flag: {flag.decode('utf-8', errors='ignore')}")
                        return flag.decode('utf-8', errors='ignore')
                    break
            
            if not found:
                print(f"❌ Could not find byte {byte_position + 1}")
                # Try a few more common characters
                for test_byte in b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f':
                    test_input = padding + flag + bytes([test_byte])
                    test_ciphertext = self.encrypt(test_input)
                    if test_ciphertext:
                        test_block = test_ciphertext[target_block_idx*32:(target_block_idx+1)*32]
                        if test_block == target_block:
                            flag += bytes([test_byte])
                            print(f"✅ Found control char: \\x{test_byte:02x}")
                            found = True
                            break
                
                if not found:
                    break
        
        final_flag = flag.decode('utf-8', errors='ignore')
        print(f"\n🏁 Extracted: {final_flag}")
        return final_flag

def manual_test_helper():
    """Helper to test manual inputs"""
    print("=== Manual Testing Helper ===")
    print("\n🧪 Test inputs to try:")
    
    test_cases = [
        ("Empty input", ""),
        ("Single A", "41"),
        ("15 A's", "41" * 15), 
        ("16 A's", "41" * 16),
        ("17 A's", "41" * 17),
        ("32 A's", "41" * 32),
    ]
    
    for description, hex_input in test_cases:
        print(f"{description:12}: {hex_input}")
    
    print(f"\n💡 Key observations to make:")
    print("1. How does ciphertext length change as you add input?")
    print("2. When does a new block appear?") 
    print("3. Do identical input blocks create identical output blocks?")
    
    print(f"\n🎯 Start your attack with:")
    print("Input: '' (empty) - this shows baseline flag encryption")
    print("Then: '41' (single A)")
    print("Then: '4141' (two A's)")
    print("Continue adding A's and watch the pattern!")

if __name__ == "__main__":
    print("Live ECB Oracle Attack")
    print("=" * 30)
    
    # For manual testing
    manual_test_helper()
    
    print(f"\n" + "="*50)
    print("To run automated attack:")
    print("attack = LiveECBAttack('http://your-challenge-url')")  
    print("flag = attack.extract_flag()")
    attack = LiveECBAttack('https://aes.cryptohack.org/ecb_oracle/')  # Replace with actual URL
    flag = attack.extract_flag()