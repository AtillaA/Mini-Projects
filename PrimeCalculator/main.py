from sieve import sieve_of_eratosthenes, sieve_of_sundaram, sieve_of_atkin
from deterministic import trial_division_test, aks_test, lucas_lehmer_test
from probabilistic import fermat_test, miller_rabin_test, baillie_psw_test


"""
Prime Number Calculator:
    Check primality of a given input, or list the prime numbers up to that input
"""
def main():
    print("\nPRIME NUMBER CALCULATOR")
    print("-----------------------")
    print("\nWelcome. Capabilities of this program are listed below:\n")

    while True:
        print("1. Find out if an integer is prime or composite.")
        print("2. Print the list of prime integers up to a positive integer.")
        print("3. Exit.")

        user_input = input("\nSelection: ").strip()

        # handle exit immediately
        if user_input == "4":
            print("\nExiting program.")
            break

        # check out-of-bounds/non-digit inputs
        if not user_input.isdigit() or user_input not in ["1", "2"]:
            print("\nInvalid input, make a valid selection.\n")
            continue

        # process valid choices
        selection_input = int(user_input)
        
        target_input = input("\nEnter a target positive integer (n): ")

        if not target_input.isdigit():
            print("\nInvalid number input, returning to main menu...\n")
            continue
            
        n = int(target_input)

        if selection_input == 1 or selection_input == 2:
            init_primecalculator(selection_input, n)


def init_primecalculator(selection, n):
    print("\nSelect the primality test method you wish to use (note that Lucas-Lehmer test will only yield Mersenne prime(s)):")
    print("\nSieves:")
    print("-------")
    print("1. Sieve of Eratosthenes")
    print("2. Sieve of Sundaram")
    print("3. Sieve of Atkin")
    print("\nDeterministic Tests:")
    print("----------------------")
    print("4. Trial Division")
    print("5. AKS")
    print("6. Lucas-Lehmer")
    #print(f"{"\033[9m"}Lucas-Lehmer{"\033[0m"}")
    print("\nProbabilistic Tests:")
    print("----------------------")
    print("7. Fermat")
    print("8. Miller-Rabin")
    print("9. Baillie-PSW")
    print("\n0. Back\n")

    test_input = input("\nSelection: ").strip()

    # handle exit immediately
    if test_input == "0":
        print("Returning to main menu...\n")
        return 0

    # check out-of-bounds/non-digit inputs
    if not test_input.isdigit() or not (1 <= int(test_input) <= 9):
        print("\nInvalid test selection input, returning to main menu...\n")


def dummy_func():
    n = 200

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
