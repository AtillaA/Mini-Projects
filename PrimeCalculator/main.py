from deterministic import trial_division_test, aks_test, lucas_lehmer_test

from sieve import *


"""
Detect all prime numbers up to N
"""
def main():
    n = 100

    print(sieve_of_eratosthenes(n))
    print(sieve_of_sundaram(n))
    print(sieve_of_atkin(n))

    trial_division_list = []
    aks_list = []
    lucas_lehmer_list = []

    for i in range(0, n):

        if trial_division_test(i):
            trial_division_list.append(i)

        if aks_test(i):
            aks_list.append(i)

        if lucas_lehmer_test(i):
            lucas_lehmer_list.append(i)

    print(trial_division_list)
    print(aks_list)
    print(lucas_lehmer_list) # only prints the prime mersenne numbers
        
    return 0


if __name__ == "__main__":
    main()
