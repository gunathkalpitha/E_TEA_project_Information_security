import timeit, os, random
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import tea, etea, file_io

def generate_test_data(size_bytes):
    return bytes(random.getrandbits(8) for _ in range(size_bytes))

def bench(cipher, data, key, runs=50):
    blocks = file_io.to_blocks(file_io.pad(data))
    t = timeit.timeit(
        lambda: [cipher.encrypt_block(v0, v1, key) for v0, v1 in blocks],
        number=runs
    )
    return (t / runs) * 1000  # ms per run

if __name__ == '__main__':
    key = (0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210)
    sizes = [1_000, 10_000, 100_000, 500_000]  # bytes

    print(f"{'Size':>10}  {'TEA (ms)':>10}  {'E-TEA (ms)':>12}  {'Overhead':>10}")
    for sz in sizes:
        data = generate_test_data(sz)
        t_tea   = bench(tea,  data, key)
        t_etea  = bench(etea, data, key)
        overhead = ((t_etea - t_tea) / t_tea) * 100
        print(f"{sz:>10}  {t_tea:>10.3f}  {t_etea:>12.3f}  {overhead:>+9.1f}%")