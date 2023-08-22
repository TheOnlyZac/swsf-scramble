"""
benchmark.py

This file contains a benchmarking function to measure the time it takes to generate
a large number of hashes.
"""
import sys
import timeit
from swsf import scramble

def benchmark(num_hashes: int = 500_000):
    """
    Measures the time it takes to generate 500k hashes and finds the average.
    """
    test_codes = ["password", "pnyrcade", "headhunt", "director", "quentin", "maggie", "jarjar", "nohud", "darkside", "credits"]

    print(f"Benchmarking swsf_scramble with {len(test_codes)} trials of {num_hashes:,} hashes each...")

    total_times = []
    for code in test_codes:
        start = timeit.default_timer()

        for _ in range(num_hashes):
            scramble.swsf_scramble(code)

        end = timeit.default_timer()
        total_times.append(end - start)

    total_time = sum(total_times)
    total_average = sum(total_times) / len(total_times)
    hash_average = sum(total_times) / (len(total_times) * num_hashes)
    print(f"\nTotal time: {total_time:2f}s")
    print(f"Average total time: {total_average:2f}s")
    print(f"Average time per hash: {hash_average:2f}s")

def main(argc: int, argv: list) -> None:
    """
    Calls the benchmark function.
    """
    if argc == 2:
        benchmark(int(argv[1]))
    else:
        benchmark()

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
