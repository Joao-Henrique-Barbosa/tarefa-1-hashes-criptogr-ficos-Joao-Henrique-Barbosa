#!/usr/bin/env python3
"""
Grader for Exercise 3: Hash0 First Pre-image Attack
Expected: ASCII string that hashes to 631a000d
"""

import sys
import os
from pathlib import Path

# Add functions directory to path
sys.path.insert(0, 'functions')

try:
    from hash0 import xor32_hash

    # Load solution
    solution_file = Path("solutions/exercise03.txt")
    if not solution_file.exists():
        print("FAIL: Solution file solutions/exercise03.txt not found")
        sys.exit(1)

    with open(solution_file, 'r') as f:
        solution = f.read().strip()

    # Validate format
    if not solution.isascii():
        print("FAIL: Solution must be ASCII")
        sys.exit(1)

    # Test first pre-image
    target_hash = "1b575451"
    solution_hash = xor32_hash(solution)

    if solution_hash != target_hash:
        print(f"FAIL: Solution hash {solution_hash} doesn't match target {target_hash}")
        sys.exit(1)

    print("PASS")

except Exception as e:
    print(f"FAIL: Error - {str(e)}")
    sys.exit(1)
