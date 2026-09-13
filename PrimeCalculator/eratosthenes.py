def sieve_of_eratosthenes(n):
  primes = [True] * (n + 1) # Assume numbers 2 to n are prime
  p = 2 # Starting from 2
  
  while (p * p <= n): # Main loop for iterating over each factor
    if primes[p]: # If current number p is prime
      for i in range(p * p, n + 1, p): # Loop over multiples of p, incrementing by p
        primes[i] = False # Mark as composite
    p += 1 # Check the next number
  return [p for p in range(2, n + 1) if primes[p]] # Return the list of numbers marked as True

# Example usage
print(sieve_of_eratosthenes(100))
