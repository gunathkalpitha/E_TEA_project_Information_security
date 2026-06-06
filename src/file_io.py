import struct

def pad(data: bytes) -> bytes:
    """Pad to multiple of 8 bytes (64-bit blocks)."""
    pad_len = (8 - len(data) % 8) % 8
    return data + bytes([pad_len] * pad_len) if pad_len else data + b'\x00' * 8

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len] if 0 < pad_len <= 8 else data

def to_blocks(data: bytes):
    """Split bytes into list of (v0, v1) 32-bit pairs."""
    blocks = []
    for i in range(0, len(data), 8):
        v0, v1 = struct.unpack('>II', data[i:i+8])
        blocks.append((v0, v1))
    return blocks

def from_blocks(blocks) -> bytes:
    return b''.join(struct.pack('>II', v0, v1) for v0, v1 in blocks)

def encrypt_file(path_in, path_out, key, cipher_module):
    with open(path_in, 'rb') as f:
        data = pad(f.read())
    blocks = to_blocks(data)
    encrypted = [cipher_module.encrypt_block(v0, v1, key) for v0, v1 in blocks]
    with open(path_out, 'wb') as f:
        f.write(from_blocks(encrypted))