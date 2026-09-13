Prime Number Calculator
------------------------
A mini project that consists three different algorithms (sieves) for detecting prime numbers in a given list of consecutive numbers [2,...,n].

A prime number is a whole number greater than 1 that can only be divided evenly by 1 and itself.

1.) Sieve of Eratosthenes: Iterative approach of marking the multiples of each prime number. Time complexity O(n log log n)
                              - Iterate over the list of numbers [2,...,n]
                              - Mark all multiples of i as composite at each step
                              - Repeat for all numbers up to √n, reamining unmarked numbers are primes

2.) Sieve of Sundaram: Remove numbers from list and transform the remaining. Time complexity O(n log n)
                              - Create an integer list from 1 to (n-1)/2
                              - Remove numbers of the form (i+j+2ij)
                              - Transform the remaining to get the primes

3.) Sieve of Atkin: Quadratic approach for marking and eliminating multiples of squares. Time complexity O(n log n)
                              - Create an integer list and mark integers using specific quadratic equations
                              - Eliminate multiples of squares, remaining are primes

Other popular approaches include: Miller-Rabin and Baillie-PSW Tests for Probabilistic Primality Tests which are fastest for huge numbers,
                                  Trial Division, AKS (Agrawal–Kayal–Saxena), and Lucas-Lehmer Tests for Deterministic Primality Tests.
