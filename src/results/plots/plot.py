import matplotlib.pyplot as plt
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src import tea, etea
import random

# Avalanche bar chart
def plot_avalanche(tea_score, etea_score):
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(['TEA', 'E-TEA'], [tea_score, etea_score], color=['#5b7fa6', '#e07b54'], width=0.6)
    ax.axhline(50, color='green', linestyle='--', linewidth=2, label='Ideal (50%)')
    
    # Zoom in on the 45-55% range to highlight differences
    ax.set_ylim(45, 55)
    
    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_ylabel('Avg Bits Changed (%)', fontsize=12)
    ax.set_title('Avalanche Effect Comparison (Zoomed)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Cipher', fontsize=12)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('results/plots/avalanche.png', dpi=150)
    print("✓ Plot saved to results/plots/avalanche.png")

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
            if bit < 32:
                flipped_v0, flipped_v1 = v0 ^ (1 << bit), v1
            else:
                flipped_v0, flipped_v1 = v0, v1 ^ (1 << (bit - 32))

            modified = cipher.encrypt_block(flipped_v0, flipped_v1, key)
            changed_bits = hamming_distance(original, modified)
            bit_results.append(changed_bits / 64 * 100)

        results.append(sum(bit_results) / len(bit_results))

    return sum(results) / len(results)

if __name__ == '__main__':
    key = (0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210)
    print("Running avalanche tests...")
    tea_score = avalanche_test(tea, key)
    etea_score = avalanche_test(etea, key)
    print(f"TEA  avalanche: {tea_score:.2f}%  (ideal: 50%)")
    print(f"E-TEA avalanche: {etea_score:.2f}%  (ideal: 50%)")
    print("\nGenerating plot...")
    plot_avalanche(tea_score, etea_score)