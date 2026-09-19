import random
import math

"""
Probabilistic algorithms for detecting whether a given positive integer is prime

These algorithms can determine if a number is composite with 100% certainty
If they yield that a number is prime, there is a micro-fractional chance that it might be composite (a "pseudoprime")
Running the test multiple times reduces this error margin to essentially zero

Three major tests are: Fermat Test, Miller-Rabin Test, Baillie-PSW Test
"""

# -------------------------------------------

"""
Fermat Test:
    Simplest probabilistic test, operating as the foundation for more advanced randomized algorithms
    
    Relies on Fermat's Little Theorem, which states that if N is prime, then for any integer A such that (gcd(a, n) = 1), the congruence (a^{n-1} ≡ 1 mod{n}) must hold
    The algorithm picks a random base (a) and evaluates this modular exponentiation
        - If failed, N is composite
        - If passed, N is a "probable prime"
    
    Note: the algorithm has a flaw where certain composite numbers called Carmichael numbers (like 561 or 1105) satisfy this condition for all valid bases (a)
          meaning the Fermat test can be tricked 100% of the time by the Carmichael numbers regardless of how many random loops you run
"""
def fermat_test(n: int, k: int = 5) -> bool:
    """
    returns False if n is definitively composite, True if probably prime
    k represents the number of random trials to perform
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        # select a random base a in [2, n-2]
        a = random.randint(2, n - 2)
        
        # check FLT congruence
        if pow(a, n - 1, n) != 1:
            return False  # definitively composite
            
    return True  # probably prime

# -------------------------------------------

"""
Miller-Rabin Test:
    Industrial standard for modern computer systems and cryptographic key generation (like RSA)
    Essentially an upgraded, un-trickable version of the Fermat test
    
    Closes the Fermat loophole by leveraging the properties of square roots of 1 modulo a prime
    Factors out all powers of 2 from N - 1, writing it as (2^s ⋅ d) where d is odd
    For a random base (a), it checks if (a^d ≡ 1 mod{n}) or if (a^{2^r ⋅ d} ≡ -1 mod{n}) for some (0 <= r < s)
    Unlike Fermat, there are no numbers that trick the Miller-Rabin test universally
    Every iteration reduces the chance of a false positive to less than 25%
    Running it 40 times drops the probability of a false positive to a practically impossible (2^{-80})
"""
def miller_rabin_test(n: int, k: int = 5) -> bool:
    """
    returns False if n is definitively composite, True if strongly probably prime
    k represents the number of random trials to perform
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # factorize n-1 into (2^s) * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # run k independent random witness loops
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        
        if x == 1 or x == n - 1:
            continue
            
        composite_flag = True

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                composite_flag = False
                break
                
        if composite_flag:
            return False  # definitively composite
            
    return True  # strongly probably prime

# -------------------------------------------

"""
Baillie-PSW Test:
    An exceptionally powerful hybrid test
    Widely used by elite computer algebra software like SymPy and the GNU Multiple Precision Arithmetic Library (GMP) because of its unparalleled accuracy
    
    Instead of relying on multiple loops with random bases, BPSW combines two entirely distinct mathematical tests deterministically: 
        1. A single strong Miller-Rabin test using exactly base
        2.A strong Lucas primality test, which uses the Jacobi Symbol to find a parameter (D) from the sequence (5, -7, 9, -11, ...) and evaluates Lucas sequences
        
    Types of composite numbers that can trick a base-2 Miller-Rabin test belong to completely different mathematical sets than those that trick a Lucas test
    This combination is so robust that there are no known composite numbers that pass the Baillie-PSW test up to at least (2^{64}) and potentially beyond
"""
def _lucas_selfridge(n: int):
    """ internal helper to find Selfridge's parameters (D, P, Q) for Lucas test """
    D = 5
    sign = 1

    while True:
        # compute Jacobi Symbol (D/n)
        g = math.gcd(abs(D), n)

        if 1 < g < n:
            return 0, 0, 0 # composite detected via GCD
        
        # calc Jacobi Symbol manually
        j = _jacobi_symbol(D * sign, n) # custom Jacobi function

        if j == -1:
            break

        D += 2
        sign = -sign

        if D > 1000000: # practical escape bound
            return 0, 0, 0
            
    P = 1
    Q = (1 - (D * sign)) // 4

    return D * sign, P, Q

def _jacobi_symbol(a: int, n: int) -> int:
    """ calculates the Jacobi symbol (a/n) """
    a %= n
    t = 1

    while a != 0:
        while a % 2 == 0:
            a //= 2
            r = n % 8
            
            if r == 3 or r == 5:
                t = -t

        a, n = n, a

        if a % 4 == 3 and n % 4 == 3:
            t = -t

        a %= n

    return t if n == 1 else 0

def _strong_lucas_test(n: int) -> bool:
    """ performs the Strong Lucas Probable Prime Test portion """
    D, P, Q = _lucas_selfridge(n)

    if D == 0:
        return False
        
    # n + 1 = d * 2^s
    k = n + 1
    s = 0
    d = k

    while d % 2 == 0:
        d //= 2
        s += 1
        
    # sequence eval for U_d and V_d using standard recursive doubling method
    U = 1
    V = P
    Q_k = Q  # track pwrs of Q dynamically
    
    binary_d = bin(d)[3:]

    for bit in binary_d:
        U, V = (U * V) % n, (V * V - 2 * Q_k) % n
        Q_k = (Q_k * Q_k) % n

        if bit == '1':
            U_next = P * U + V
            V_next = D * U + P * V

            if U_next % 2 != 0: 
                U_next += n
            
            if V_next % 2 != 0: 
                V_next += n
            
            U = (U_next // 2) % n
            V = (V_next // 2) % n
            Q_k = (Q_k * Q) % n
            
    if U == 0 or V == 0:
        return True
        
    # check the structural squaring steps
    for _ in range(1, s):
        V = (V * V - 2 * Q_k) % n

        if V == 0:
            return True
        Q_k = (Q_k * Q_k) % n
        
    return False

def baillie_psw_test(n: int) -> bool:
    """
    returns True if N passes the Baillie-PSW test (almost certainly prime)
    no parameter k is required since the choice of bases is completely deterministic
    """
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0: return False
    
    # 1. check perfect square condition
    root = math.isqrt(n)

    if root * root == n:
        return False

    # 2. base-2 Miller Rabin Test
    # using prev func config bounded to a single pass with base=2
    s = 0
    d = n - 1

    while d % 2 == 0:
        d //= 2
        s += 1

    x = pow(2, d, n)

    if x != 1 and x != n - 1:
        composite = True

        for _ in range(s - 1):
            x = pow(x, 2, n)

            if x == n - 1:
                composite = False
                break

        if composite:
            return False # Fails base-2 strong pseudoprime test

    # 3. strong Lucas Test
    return _strong_lucas_test(n)
