from sieve import sieve_of_eratosthenes, sieve_of_sundaram, sieve_of_atkin
from deterministic import trial_division_test, aks_test, lucas_lehmer_test
from probabilistic import fermat_test, miller_rabin_test, baillie_psw_test


"""
Detect all prime numbers up to N

NOTE: Edit the main method accordingly to the algorithm that you wish to examine
      All algorithms are checked in the current version, which may cause lag for very big values of N
"""
def main():
    print("PRIME NUMBER CALCULATOR")
    print("-----------------------")
    print("Welcome. Capabilities of this program are listed below:\n")
    print("1. Find out if an integer is prime or composite.")
    print("2. Print the list of prime integers up to a positive integer.")
    print("3. Print the list of Mersenne numbers up to a positive integer.")
    print("4. Exit.")
    
    user_input = input("\nSelection: ")

    # init_primecalculator(user_input)


def init_primecalculator(n):
    n = 100 # <--- detect primes up to here
    
    # print sieves results
    print(sieve_of_eratosthenes(n))
    print(sieve_of_sundaram(n))
    print(sieve_of_atkin(n))

    # deterministic results
    trial_division_list = []
    aks_list = []
    lucas_lehmer_list = []

    # probabilistic results
    fermat_list = []
    miller_rabin_list = []
    baillie_psw_list = []

    for i in range(0, n):
        # deterministic tests
        if trial_division_test(i):
            trial_division_list.append(i)
        if aks_test(i):
            aks_list.append(i)
        if lucas_lehmer_test(i):
            lucas_lehmer_list.append(i)

        # probabilistic tests
        if fermat_test(i):
            fermat_list.append(i)
        if miller_rabin_test(i):
            miller_rabin_list.append(i)
        if baillie_psw_test(i):
            baillie_psw_list.append(i)

    # print deterministic results
    print(trial_division_list)
    print(aks_list)
    print(lucas_lehmer_list) # <--- only prints the prime mersenne numbers

    # print probabilistic results
    print(fermat_list)
    print(miller_rabin_list)
    print(baillie_psw_list)
        
    return 0


if __name__ == "__main__":
    main()
