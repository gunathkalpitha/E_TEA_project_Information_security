import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import tea, etea

def hamming_distance(a, b):
    """Count differing bits between two 64-bit values."""
    diff = (a[0] ^ b[0]) | ((a[1] ^ b[1]) << 32)
    return bin(diff).count('1')

def avalanche_test(cipher, key, num_trials=100):
    results = []
    for _ in range(num_trials):
        v0 = random.randint(0, 0xFFFFFFFF)
        v1 = random.randint(0, 0xFFFFFFFF)
        original = cipher.encrypt_block(v0, v1, key)

        bit_results = []
        for bit in range(64):
            # Flip one bit in the input
            if bit < 32:
                flipped_v0, flipped_v1 = v0 ^ (1 << bit), v1
            else:
                flipped_v0, flipped_v1 = v0, v1 ^ (1 << (bit - 32))

            modified = cipher.encrypt_block(flipped_v0, flipped_v1, key)
            changed_bits = hamming_distance(original, modified)
            bit_results.append(changed_bits / 64 * 100)  # percentage

        results.append(sum(bit_results) / len(bit_results))

    return sum(results) / len(results)  # average % bits changed

if __name__ == '__main__':
    key = (0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210)
    tea_score  = avalanche_test(tea,  key)
    etea_score = avalanche_test(etea, key)
    print(f"TEA  avalanche: {tea_score:.2f}%  (ideal: 50%)")
    print(f"E-TEA avalanche: {etea_score:.2f}%  (ideal: 50%)")