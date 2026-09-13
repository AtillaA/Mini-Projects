def sieve_of_atkin(limit):
   primes = [False] * (limit + 1) # Assume all numbers are composite
   primes[2] = primes[3] = True # Mark 2 and 3 as prime
  
   for x in range(1, int(limit**0.5) + 1): # Iterate from 1 to sqrt(limit)
       for y in range(1, int(limit**0.5) + 1): # For each combination of x and y, compute n using different formulas to detect candidates
           n = 4 * x**2 + y**2 # Candidate formula 1
         
           if n <= limit and (n % 12 == 1 or n % 12 == 5): # Since primes of the form n are congruent to 1 or 5 modulo 12
               primes[n] = not primes[n] # Toggle primality status
           
           n = 3 * x**2 + y**2 # Candidate formula 2
         
           if n <= limit and n % 12 == 7: # Since primes of the form n are congruent to 7 modulo 12
               primes[n] = not primes[n] # Toggle primality status
           
           n = 3 * x**2 - y**2 # Candidate formula 3
         
           if x > y and n <= limit and n % 12 == 11: # Since primes of the form n are congruent to 11 modulo 12
               primes[n] = not primes[n] # Toggle primality status
             
   for n in range(5, int(limit**0.5) + 1): # Check for the squares of primes and toggle
       if primes[n]:
           for k in range(n**2, limit + 1, n**2): # If n is prime, eliminate its quadratic multiples
               primes[k] = False
  
   return [2, 3] + [x for x in range(5, limit + 1) if primes[x]] # Generate the list of primes up to limit (add 2 and 3 manually, rest via elementary number theory conditions)
  
# Example usage
print(sieve_of_atkin(100))
