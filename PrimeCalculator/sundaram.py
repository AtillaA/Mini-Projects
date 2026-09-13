def sieve_of_sundaram(n):
   k = (n - 1) // 2 # Largest index for odd primes
   primes = [True] * (k + 1) # Initialize primes list
  
   for i in range(1, k + 1): # For each odd number
       j = i
       
       while i + j + 2 * i * j <= k: # So long as the derived Sundaram is below the largest index
           primes[i + j + 2 * i * j] = False # Remove numbers of the form (i+j+2ij)
           j += 1
  
   return [2] + [2 * i + 1 for i in range(1, k + 1) if primes[i]] # Add 2 manually, generate remaining w.r.t. the value of i corresponding to prime (2i+1)

# Example usage
print(sieve_of_sundaram(100))
