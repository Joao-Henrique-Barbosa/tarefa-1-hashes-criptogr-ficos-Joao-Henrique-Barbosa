# Cooking with Hash: Slicing, Dicing, and Mixing Data

Hash functions are everywhere in computer science and cryptography.
We use them to create fingerprints of data for quick comparison, to check file integrity, to organize data in hash tables, and, crucially in cryptography, to commit to a secret—that is, to prove you know something without revealing it.

For many of these applications, especially in cryptography, it’s not enough for a hash function to just scramble data.
A good hash function must resist several types of attacks:

- Collision resistance: It should be practically impossible to find any two different inputs that produce the same hash output.
- First pre-image resistance: Given a hash output, it should be infeasible to figure out what input produced it.
- Second pre-image resistance: Given a pre-image, it should be infeasible to figure out another input that yields the same hash value.

If a hash function is vulnerable to these attacks, it can’t be safely used for cryptographic purposes, as attackers could break commitments, forge digital fingerprints, or violate the security of protocols that rely on hashes.

In this assignment, you’ll experiment with hash functions to discover how and why these properties matter—and what can go wrong if they aren’t satisfied.

### Expected submissions

Your solutions should be in the form of bash scripts in the `solutions` folder of your repo.
They should provide output as specified in the following specifications.
The autograder will run the scripts in the `graders` folder, so you can always check your solution by running e.g. `pythons graders/check_exercise01.py` yourself in the root of the assignment.
DO NOT MODIFY THE GRADER SCRIPTS.

The autograder is triggered anytime you push changes in the `main` branch of your repo.
Check its output on the `Actions` tab in the github interface.

You are supposed to create some brute forcing programs.
DO NOT TRY TO RUN THEM ON THE AUTOGRADER, it's configured to timeout before the expected runtime for them.
Instead, submit text files with your solutions as specified below.

You can use any programming language you see fit and we want to check your source code.
You will probably need to reimplement the given hash functions if you use another language to avoid Python's evaluation overhead, but they are quite simple to follow.
Please commit your source code to the `implementation` folder so that an instructor can provide feedback.

There's a `Feedback` pull request that was automatically openned in your repo.
You can use it to ask for questions and ask for feedback.

---

## When two bytes collide: cryptanalysis of a weak hash function

Consider the hash function `xor32_hash` given in [functions/hash0.py](functions/hash0.py) that produces 32-bit digests.
You are supposed to analyze this hash function and produce the following attacks.
It is simple enough for you do do it by hand, you don't need to brute force anything (we are going to do that later on).

### Exercise 1

Calculate two different strings that will hash to the same value.
Both strings should be composed of ascii characters and be exactly 8 characters long.

*Expected output*: a text file `solutions/exercise01.txt` with both strings separated by a comma (see provided example).

We call this a collision attack.
If it's easy to find collisions for a hash function, it can't be trusted as a unique fingerprint of data, i.e., we can't use digests to identify or commit to data.

### Exercise 2

Calculate an input string that will have exactly the same hash as the input `bitcoin0`.

*Expected output*: a text file `solutions/exercise02.txt` with the required string.

We call this a second pre-image attack.
Second pre-image resistance is crucial for integrity: if someone can create a different message with the same hash, they could replace legitimate data (documents, transactions, etc.) with malicious data that appears to be identical as far as the hash is concerned.
This property is especially important in digital signatures and commitment schemes.
For example, if you sign a document by signing its hash, you want to be sure nobody can forge a different document with the same hash (and thus the same signature).

Note how this is different from the previous exercise: here you are looking for an specific digest knowing a preimage that generates it; in the previous exercise you don't have such a target. 

### Exercise 3

Calculate an input string that will have exactly the hash `1b575451`.

*Expected output*: a text file `solutions/exercise03.txt` with the required string.

We call this a first pre-image attack, i.e., we can construct the pre-image for a given hash.
If a hash function is not pre-image resistant, an attacker could “reverse” a hash value to recover or forge a message.
This would break the use of hashes for commitments (proving you knew a value without revealing it) or for securely storing passwords (as a hash could be reversed to recover the password).

Note that in the previous exercise you know the pre-image you want to attack and can use it as a starting point to mangle with since you know the structure of the hash function.
Here, you don't have such an obvious starting point.

---

## Brute forcing can be an option

For the next exercises, consider the function given in [functions/hash1.py](functions/hash1.py) that also produces 32-bits digests.
This is still an insecure function, but it's algebraic structure is a bit more complicated to render cryptanalysis infeasible for the scope of this course.
Yet, we can always brute force it, i.e., try many combinations of inputs and search for a convenient output.
The search space is quite small since 32-bits will render around 4 billion possible outputs, something that any modern computer can generate in a few minutes (if not seconds if properly implemented).

For the next exercises, you are expected to brute force the solutions.
Expect to let your program run for a few minutes if you are using a multicore solution or a few hours for single core.

### Exercise 4

Calculate two different strings that will hash to the same value (i.e., perform a collision attack).
Both strings should be composed of ascii characters and be 8 characters long (32 bits).

*Expected output*: a text file `solutions/exercise04.txt` with both strings separated by a comma (see provided example).

This should be fairly easy (a few seconds to minutes) if you understand how to take advantage of the birthday paradox.

### Exercise 5

Find a second pre-image for your first name using `simple_hash`.

Example: If your name is "edil", find any string X different from "edil" such that `simple_hash("edil") == simple_hash(X)`.

*Expected output*: a text file `solutions/exercise05.txt` with `yourname,foundstring`.

Finding pre-images is *significantly harder* then finding collisions.
Expect your program to maybe run for a couple hours.
It took me ~1h with a single threaded Python script to find a solution on a Apple M3 Pro processor.

To get a sense for how difficult it is to break 256-bit hashes, remember that each bit you add doubles the search space.

### Exercise 6

For this exercise, consider the function given in [functions/sha256.py](functions/sha256.py) that also produces 256-bit digests.

Compute three partial collision using SHA256 (proof-of-work style).

Find three ASCII strings starting with `bitcoin` (e.g. `bitcoin0`, `bitcoinA0b1`, etc) that, when hashed with SHA256, produces a digest starting with the bytes `0xcafe`, `0xfaded`, and `0xdecade`, in this order.

*Expected output*: a text file `solutions/exercise06.txt` the three strings separated by commas (e.g `bitcoin0,bitcoin1,bitcoin2`).

This exercise mimics Bitcoin's proof-of-work system, where miners search for inputs that produce hashes with specific patterns.
Here, you're looking for specific leading bytes with increasing difficulty.
This should take seconds on modern hardware, it is intended to give you a feel of how to build an adjustable proof of work system.
