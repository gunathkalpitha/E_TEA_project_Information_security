import struct

DELTA = 0x9E3779B9
MASK  = 0xFFFFFFFF

def encrypt_block(v0, v1, key):
    k0, k1, k2, k3 = key
    s = 0
    for _ in range(32):
        s = (s + DELTA) & MASK
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & MASK
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & MASK
    return v0, v1

def decrypt_block(v0, v1, key):
    k0, k1, k2, k3 = key
    s = (DELTA * 32) & MASK
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & MASK
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & MASK
        s = (s - DELTA) & MASK
    return v0, v1
