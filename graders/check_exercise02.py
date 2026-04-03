#!/usr/bin/env python3
"""
Grader for Exercise 2: Hash0 Second Pre-image Attack
Expected: 8-character ASCII string with same hash as "bitcoin0"
"""

import sys
import os
from pathlib import Path

# Add functions directory to path
sys.path.insert(0, 'functions')

try:
    from hash0 import xor32_hash

    # Load solution
    solution_file = Path("solutions/exercise02.txt")
    if not solution_file.exists():
        print("FAIL: Solution file solutions/exercise02.txt not found")
        sys.exit(1)

    with open(solution_file, 'r') as f:
        solution = f.read().strip()

    # Validate format
    if len(solution) != 8:
        print(f"FAIL: Solution must be 8 characters, got {len(solution)}")
        sys.exit(1)

    if not solution.isascii():
        print("FAIL: Solution must be ASCII")
        sys.exit(1)

    if solution == "bitcoin0":
        print("FAIL: Solution must be different from 'bitcoin0'")
        sys.exit(1)

    # Test second pre-image
    target_hash = xor32_hash("bitcoin0")
    solution_hash = xor32_hash(solution)

    if solution_hash != target_hash:
        print(f"FAIL: Solution hash {solution_hash} doesn't match bitcoin0 hash {target_hash}")
        sys.exit(1)

    print("PASS")

except Exception as e:
    print(f"FAIL: Error - {str(e)}")
    sys.exit(1)
