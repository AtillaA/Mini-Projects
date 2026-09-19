Prime Number Calculator
------------------------
A mini project that consists of three different approaches for detecting prime numbers up to a given positive integer N.
A prime number is a whole number greater than 1 that can only be divided evenly by 1 and itself.


1.) Sieves:
    -- Sieve of Eratosthenes: Iterative approach of marking the multiples of each prime number.
        - Iterate over the list of numbers [2,...,n].
        - Mark all multiples of i as composite at each step.
        - Repeat for all numbers up to √n, reamining unmarked numbers are primes.
        - Time Complexity: O(NloglogN) | Space Complexity: O(N)
    
    --Sieve of Sundaram: Remove numbers from list and transform the remaining.
        - Create an integer list from 1 to (n-1)/2.
        - Remove numbers of the form (i+j+2ij).
        - Transform the remaining to get the primes.
        - Time Complexity: O(NlogN) | Space Complexity: O(N)

    -- Sieve of Atkin: Quadratic approach for marking and eliminating multiples of squares.
        - Create an integer list and mark integers using specific quadratic equations.
        - Eliminate multiples of squares, remaining are primes.
        - Time Complexity: O(N / loglogN) | Space Complexity: O(N^{0.5 + o(1)})


2.) Deterministic Primality Tests:
    -- Trial Division: Brute-force approach of testing individual divisors up to the square root. 
        - Exclude even numbers and multiples of 3 to speed up matching.
        - Test if n is evenly divisible by any integer step up to √n.
        - If no factors are found, the number is definitively prime.
        - Time Complexity: O(sqrt{N}) | Space Complexity: O(1)
        
    -- Agrawal–Kayal–Saxena (AKS) Test: General polynomial-time approach utilizing algebraic rings. 
        - Check if n is a perfect power or shares a small common factor.
        - Evaluate polynomial expansion congruences modulo a chosen marker.
        - First general test to prove absolute certainty in guaranteed polynomial time.
        - Time Complexity: O((logN)^6) | Space Complexity: O(rlogN)
        
    -- Lucas-Lehmer Test: Specialized sequence evaluation restricted strictly to Mersenne forms. 
        - Test numbers matching the specific blueprint M_p = 2^p - 1.
        - Run a recursive squaring loop a total of p - 2 times.
        - If the final structural term equals 0, the Mersenne number is prime.
        - Time Complexity: O((P^2)logPlogP) | Space Complexity: O(P)


3.) Probabilistic Primality Tests:
    -- Fermat Primality Test: Modular exponentiation checking based on Fermat's Little Theorem. 
        - Select k random integer bases within the target range.
        - Verify if the modular power condition a^(n-1) ≡ 1 mod n holds.
        - Highly efficient, but inherently fooled by composite Carmichael numbers.
        - Time Complexity: O(k ⋅ (log^3)N) | Space Complexity: O(1)

    -- Miller-Rabin Test: Upgraded randomized check tracking strong modular pseudoprime boundaries.
        - Factor out all powers of 2 from n - 1 to extract components.
        - Analyze successive square roots of 1 modulo n across random bases.
        - Eliminates the Carmichael loophole; accuracy scales infinitely with iteration loops
        - Time Complexity: O(k ⋅ (log^3)N) w/ standard modular multiplication, O(k ⋅ (log^2)NloglogN) w/ FFT acceleration | Space Complexity: O(1)

    -- Baillie-PSW Test: Hybrid non-randomized test combining base-2 and sequence checks.
        - Run a single strong Miller-Rabin test using exactly base 2.
        - Pass the number into a secondary strong Lucas sequence test.
        - Zero known false positives in practice, offering near-absolute certainty without looping.
        - Time Complexity: O((log^3)N) | Space Complexity: O(logN)
