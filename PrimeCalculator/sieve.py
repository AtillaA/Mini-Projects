"""
Sieve of Eratosthenes:
    The oldest and most intuitive sieve algorithm
    Works on the principle that any multiple of a prime number must be a composite number
"""
def sieve_of_eratosthenes(n):
  primes = [True] * (n + 1) # assume numbers 2 to n are prime
  p = 2 # starting from 2
  
  while (p * p <= n): # main loop for iterating over each factor
    if primes[p]: # if current number p is prime
      for i in range(p * p, n + 1, p): # loop over multiples of p, incrementing by p
        primes[i] = False # mark as composite
    p += 1 # check the next number
  return [p for p in range(2, n + 1) if primes[p]] # return the list of numbers marked as True

# -------------------------------------------

"""
Sieve of Sundaram:
    Focuses strictly on odd integers
    Completely ignores even numbers, which inherently speeds up the data handling

    Utilizes an algebraic formula to identify numbers of the form (2k + 1) that are composite
    If an int K can be represented as (K = i + j + 2ij) where (1 <= i <= j), then (2K + 1) is composite
"""
def sieve_of_sundaram(n):
   k = (n - 1) // 2 # largest index for odd primes
   primes = [True] * (k + 1) # init primes list
  
   for i in range(1, k + 1): # for each odd number
       j = i
       
       while i + j + 2 * i * j <= k: # so long as the derived Sundaram is below the largest index
           primes[i + j + 2 * i * j] = False # remove numbers of the form (i + j + 2ij)
           j += 1
  
   return [2] + [2 * i + 1 for i in range(1, k + 1) if primes[i]] # add 2 manually, generate remaining w.r.t. the value of i corresponding to prime (2i + 1)

# -------------------------------------------

"""
Sieve of Atkin:
    A modern, highly optimized algorithm
    Utilizes advanced number theory
    Instead of marking multiples, checks the remainders of numbers modulo 60 and counts the number of integer solutions to specific quadratic equations
"""
def sieve_of_atkin(limit):
   # base case
   if limit == 2:
      return [2]
   
   primes = [False] * (limit + 1) # assume all numbers are composite
   primes[2] = primes[3] = True # mark 2 and 3 as prime
  
   for x in range(1, int(limit**0.5) + 1): # iterate from 1 to sqrt(limit)
       for y in range(1, int(limit**0.5) + 1): # for each combination of x and y, compute n using different formulas to detect candidates
           n = 4 * x**2 + y**2 # candidate formula #1
         
           if n <= limit and (n % 12 == 1 or n % 12 == 5): # since primes of the form n are congruent to 1 or 5 modulo 12
               primes[n] = not primes[n] # toggle status
           
           n = 3 * x**2 + y**2 # candidate formula #2
         
           if n <= limit and n % 12 == 7: # since primes of the form n are congruent to 7 modulo 12
               primes[n] = not primes[n] # toggle status
           
           n = 3 * x**2 - y**2 # Candidate formula 3
         
           if x > y and n <= limit and n % 12 == 11: # since primes of the form n are congruent to 11 modulo 12
               primes[n] = not primes[n] # toggle status
             
   for n in range(5, int(limit**0.5) + 1): # check for the squares of primes and toggle
       if primes[n]:
           for k in range(n**2, limit + 1, n**2): # if n is prime, eliminate its quadratic multiples
               primes[k] = False
  
   return [2, 3] + [x for x in range(5, limit + 1) if primes[x]] # generate the list of primes up to limit (add 2 and 3 manually, rest via elementary number theory conditions)
