import struct

DELTA = 0x9E3779B9
MASK  = 0xFFFFFFFF

def _rot_left(val, amount):
    """Fast left rotation (inline)."""
    amount &= 0x1F  # amount % 32
    return ((val << amount) | (val >> (32 - amount))) & MASK

def _rot_right(val, amount):
    """Fast right rotation (inline)."""
    amount &= 0x1F  # amount % 32
    return ((val >> amount) | (val << (32 - amount))) & MASK

def encrypt_block(v0, v1, key):
    k0, k1, k2, k3 = key
    s = 0
    for _ in range(32):
        s = (s + DELTA) & MASK
        r1 = v1 & 0x1F
        r2 = (v1 >> 5) & 0x1F
        # Inlined rotations for performance
        v0_rot_left = ((v1 << r1) | (v1 >> (32 - r1))) & MASK
        v1_rot_right = ((v1 >> r2) | (v1 << (32 - r2))) & MASK
        v0 = (v0 + (((v0_rot_left + k0) ^ (v1 + s) ^ (v1_rot_right + k1)))) & MASK
        
        r3 = v0 & 0x1F
        r4 = (v0 >> 5) & 0x1F
        v0_rot_left = ((v0 << r3) | (v0 >> (32 - r3))) & MASK
        v0_rot_right = ((v0 >> r4) | (v0 << (32 - r4))) & MASK
        v1 = (v1 + (((v0_rot_left + k2) ^ (v0 + s) ^ (v0_rot_right + k3)))) & MASK
    return v0, v1

def decrypt_block(v0, v1, key):
    k0, k1, k2, k3 = key
    s = (DELTA * 32) & MASK
    for _ in range(32):
        r3 = v0 & 0x1F
        r4 = (v0 >> 5) & 0x1F
        v0_rot_left = ((v0 << r3) | (v0 >> (32 - r3))) & MASK
        v0_rot_right = ((v0 >> r4) | (v0 << (32 - r4))) & MASK
        v1 = (v1 - (((v0_rot_left + k2) ^ (v0 + s) ^ (v0_rot_right + k3)))) & MASK
        
        r1 = v1 & 0x1F
        r2 = (v1 >> 5) & 0x1F
        v1_rot_left = ((v1 << r1) | (v1 >> (32 - r1))) & MASK
        v1_rot_right = ((v1 >> r2) | (v1 << (32 - r2))) & MASK
        v0 = (v0 - (((v1_rot_left + k0) ^ (v1 + s) ^ (v1_rot_right + k1)))) & MASK
        s = (s - DELTA) & MASK
    return v0, v1