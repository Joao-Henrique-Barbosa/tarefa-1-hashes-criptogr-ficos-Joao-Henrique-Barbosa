#!/usr/bin/env python3
"""
Grader for Exercise 4: Hash1 Brute Force Collision Attack
Expected: Two different 8-character ASCII strings that hash to the same value using hash1
"""

import sys
import os
from pathlib import Path

# Add functions directory to path
sys.path.insert(0, 'functions')

try:
    from hash1 import simple_hash

    # Load solution
    solution_file = Path("solutions/exercise04.txt")
    if not solution_file.exists():
        print("FAIL: Solution file solutions/exercise04.txt not found")
        sys.exit(1)

    with open(solution_file, 'r') as f:
        solution = f.read().strip()

    # Parse collision pair
    try:
        string1, string2 = solution.split(',')
        string1, string2 = string1.strip(), string2.strip()
    except ValueError:
        print("FAIL: Solution must be in format 'string1,string2'")
        sys.exit(1)

    # Validate format
    if len(string1) != 8:
        print(f"FAIL: First string must be 8 characters, got {len(string1)}")
        sys.exit(1)

    if len(string2) != 8:
        print(f"FAIL: Second string must be 8 characters, got {len(string2)}")
        sys.exit(1)

    if not string1.isascii():
        print("FAIL: First string must be ASCII")
        sys.exit(1)

    if not string2.isascii():
        print("FAIL: Second string must be ASCII")
        sys.exit(1)

    if string1 == string2:
        print("FAIL: Strings must be different")
        sys.exit(1)

    # Test collision
    hash1 = simple_hash(string1)
    hash2 = simple_hash(string2)

    if hash1 != hash2:
        print(f"FAIL: Hashes don't match: '{string1}'→{hash1}, '{string2}'→{hash2}")
        sys.exit(1)

    print("PASS")

except Exception as e:
    print(f"FAIL: Error - {str(e)}")
    sys.exit(1)
