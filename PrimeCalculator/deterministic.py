import math

"""
Deterministic algorithms for detecting whether a given positive integer is prime

All algorithms below yield a binary value, there are no false positives or false negatives

Three major tests are: Trial Division Test, AKS Test, Lukas-Lehmer Test
"""

# -------------------------------------------

"""
Trial Division Test:
    Most straightforward, brute-force approach to primality testing
    If a number N is composite, it must have a factor less than or equal to its square root
    Checks every integer starting from 2 up to sqrt{N}
    
    An optimized version checks 2 and 3 first, then skips even numbers and multiples of 3 by stepping through numbers in increments of 6 (checking \(6k \pm 1\))
    
    Perfectly deterministic and highly efficient for small numbers, but completely unusable for massive cryptographic keys due to its exponential time complexity
    
    Efficiency: Time Complexity: O(sqrt{N}) | Space Complexity: O(1)
"""
def trial_division_test(n: int) -> bool:
    """Returns True if n is prime, False otherwise using optimized Trial Division."""
    if n <= 1:
        return False
    if n <= 3:
        return True  # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False  # Exclude multiples of 2 and 3
    
    # Check factors up to the square root of n, stepping by 6
    limit = int(math.isqrt(n))
    for i in range(5, limit + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
            
    return True

# -------------------------------------------

"""
AKS Test (Agrawal–Kayal–Saxena)
    First algorithm that proved primality can be done in polynomial time without relying on unproven mathematical conjectures
    
    Generalizes Fermat's Little Theorem using polynomial rings
    States that N is prime iff the polynomial congruence [ (X+a)^n ≡ X^n + a mod{N} ] holds
    Since expanding (X+a)^n creates too many terms, the algorithm evaluates both sides modulo a carefully chosen small polynomial (X^r - 1)
    Tests the congruence for a specific range of values for (a)
    
    In practice, the overhead constants are so massive that it is far slower than probabilistic tests for everyday calculations
    Note: Due to the complexity of finding the bounds (r) and computing large polynomial coefficients, below is a preliminary implementation of the standard algorithm
    
    Efficiency: Time Complexity: O((logN)^6) | Space Complexity: O(rlogN)
"""
def perfect_power(n: int) -> bool:
    """Step 1: Check if n = a^b for integers a > 1 and b > 1."""
    limit = int(math.log2(n)) + 1
    for b in range(2, limit):
        a = round(n ** (1.0 / b))
        if a ** b == n:
            return True
    return False

def find_r(n: int) -> int:
    """Step 2: Find the smallest r such that order of n modulo r > log2(n)^2."""
    max_log = int(math.log2(n)) ** 2
    r = 2
    while True:
        gcd = math.gcd(n, r)
        if gcd > 1 and gcd < n:
            return r # Will be caught by step 3, but safe to return
            
        # Calculate multiplicative order of n modulo r
        k = 1
        cur = n % r
        while cur > 1:
            cur = (cur * n) % r
            k += 1
        if k > max_log:
            return r
        r += 1

def poly_multiply(p1: list, p2: list, r: int, mod: int) -> list:
    """Multiplies two polynomials modulo (X^r - 1) and modulo 'mod'."""
    res = [0] * r
    for i, c1 in enumerate(p1):
        if c1 == 0: continue
        for j, c2 in enumerate(p2):
            if c2 == 0: continue
            res[(i + j) % r] = (res[(i + j) % r] + c1 * c2) % mod
    return res

def poly_power(poly: list, power: int, r: int, mod: int) -> list:
    """Computes poly^power modulo (X^r - 1) and modulo 'mod' using binary exponentiation."""
    res = [1] + [0] * (r - 1)
    base = poly[:]
    while power > 0:
        if power % 2 == 1:
            res = poly_multiply(res, base, r, mod)
        base = poly_multiply(base, base, r, mod)
        power //= 2
    return res

def aks_test(n: int) -> bool:
    """Returns True if n is prime, False otherwise using the AKS algorithm."""
    if n <= 1: return False
    if n <= 3: return True

    # Step 1: Check if n is a perfect power
    if perfect_power(n):
        return False

    # Step 2: Find appropriate r
    r = find_r(n)

    # Step 3: If 1 < gcd(a, n) < n for some a <= r, n is composite
    for a in range(2, r + 1):
        gcd = math.gcd(a, n)
        if 1 < gcd < n:
            return False
        if n <= a: # If n <= r and passed checks, it's prime
            return True

    # Step 4: Check polynomial congruence
    # (X + a)^n == X^n + a (mod X^r - 1, n)
    limit = int(math.sqrt(r - 1) * math.log2(n))
    for a in range(1, limit + 1):
        # Left hand side: (X + a)^n
        poly_lhs = poly_power([a, 1] + [0]*(r-2), n, r, n)
        
        # Right hand side: X^n + a mod (X^r - 1)
        poly_rhs = [0] * r
        poly_rhs[0] = a % n
        poly_rhs[n % r] = (poly_rhs[n % r] + 1) % n
        
        if poly_lhs != poly_rhs:
            return False

    return True

# -------------------------------------------

"""
Lucas-Lehmer Test
    Specialized, lightning-fast deterministic test used exclusively for Mersenne numbers (numbers that take the form [ M_p = 2^P - 1 ] where P is an odd prime)
    Generates a sequence where the first term (S_0 = 4), and every subsequent term is defined by the recurrence relation (S_i = (S_{i-1}^2 - 2) mod{M_p})
    If the (P-2)-th term of this sequence (S_{p-2}) is exactly 0, then (M_{p}) is a prime number
    
    Incredibly efficient because it leverages fast binary bit-shifting and squaring operations
    Core algorithm used by GIMPS (Great Internet Mersenne Prime Search) to find the largest known primes in the universe
    Main constraint is that it cannot test any numbers that aren't formatted as (2^P - 1)
    
    Efficiency: Time Complexity: O((P^2)logPlogP) | Space Complexity: O(P)
"""
def lucas_lehmer_test(p: int) -> bool:
    """
    Tests if the Mersenne number M_p = 2^p - 1 is prime.
    p must be an odd prime number itself for M_p to have a chance at being prime.
    """
    if p == 2:
        return True # M_2 = 2^2 - 1 = 3 (Prime)
    
    # Initial setup
    m_p = (1 << p) - 1 # Calculates 2^p - 1 using fast bitwise shift
    s = 4
    
    # Run the sequence sequence p - 2 times
    for _ in range(p - 2):
        s = (s * s - 2) % m_p
        
    return s == 0
