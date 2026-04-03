#!/usr/bin/env python3
"""
Grader for Exercise 6: SHA256 Three Partial Collisions (Proof-of-Work)
Expected: Three ASCII strings starting with "bitcoin" that hash to targets:
1. First string hash starts with "cafe" (16 bits)
2. Second string hash starts with "faded" (20 bits)
3. Third string hash starts with "decade" (24 bits)
Format: "string1,string2,string3"
"""

import hashlib
import sys
from pathlib import Path

def compute_sha256(text):
    """Compute SHA256 hash of text"""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main():
    try:
        # Load solution file
        solution_file = Path("solutions/exercise06.txt")
        if not solution_file.exists():
            print("FAIL: Solution file solutions/exercise06.txt not found")
            sys.exit(1)

        with open(solution_file, 'r') as f:
            solution = f.read().strip()

        # Parse the three comma-separated strings
        try:
            parts = solution.split(',')
            if len(parts) != 3:
                print(f"FAIL: Expected 3 comma-separated strings, got {len(parts)}")
                print(f"Format should be: 'bitcoin_string1,bitcoin_string2,bitcoin_string3'")
                sys.exit(1)

            string1, string2, string3 = [part.strip() for part in parts]
        except ValueError:
            print("FAIL: Could not parse solution as 3 comma-separated strings")
            print("Format should be: 'bitcoin_string1,bitcoin_string2,bitcoin_string3'")
            sys.exit(1)

        # Validation targets
        targets = [
            ("cafe", "16-bit"),
            ("faded", "20-bit"),
            ("decade", "24-bit")
        ]

        strings = [string1, string2, string3]

        # Validate each string
        for i, (string, (target, bits)) in enumerate(zip(strings, targets), 1):
            # Check if string is ASCII
            if not string.isascii():
                print(f"FAIL: String {i} '{string}' must be ASCII")
                sys.exit(1)

            # Check if string starts with "bitcoin"
            if not string.startswith("bitcoin"):
                print(f"FAIL: String {i} '{string}' must start with 'bitcoin'")
                sys.exit(1)

            # Check if string is not empty after "bitcoin"
            if len(string) <= 7:  # "bitcoin" is 7 characters
                print(f"FAIL: String {i} '{string}' must have content after 'bitcoin'")
                sys.exit(1)

            # Compute hash
            hash_digest = compute_sha256(string)

            # Check if hash starts with target
            if not hash_digest.startswith(target):
                print(f"FAIL: String {i} '{string}' hash {hash_digest[:10]}... does not start with '{target}' ({bits})")
                sys.exit(1)

        # All tests passed
        print("PASS")

    except Exception as e:
        print(f"FAIL: Error - {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
