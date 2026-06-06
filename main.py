from src import tea, etea, file_io

KEY = (0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210)

# Demo: encrypt a string with both ciphers
plaintext = b"Hello, E-TEA!"
padded = file_io.pad(plaintext)
blocks = file_io.to_blocks(padded)

print("=== TEA ===")
tea_enc = [tea.encrypt_block(v0, v1, KEY) for v0, v1 in blocks]
tea_dec = [tea.decrypt_block(v0, v1, KEY) for v0, v1 in tea_enc]
print("Decrypted:", file_io.unpad(file_io.from_blocks(tea_dec)))

print("=== E-TEA ===")
etea_enc = [etea.encrypt_block(v0, v1, KEY) for v0, v1 in blocks]
etea_dec = [etea.decrypt_block(v0, v1, KEY) for v0, v1 in etea_enc]
print("Decrypted:", file_io.unpad(file_io.from_blocks(etea_dec)))