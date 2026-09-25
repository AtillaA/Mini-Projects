from sieve import sieve_of_eratosthenes, sieve_of_sundaram, sieve_of_atkin
from deterministic import trial_division_test, aks_test, lucas_lehmer_test
from probabilistic import fermat_test, miller_rabin_test, baillie_psw_test


def main():
    print("\nPRIME NUMBER CALCULATOR")
    print("-----------------------")
    print("\nWelcome. Capabilities of this program are listed below:\n")

    while True:
        print("1. Find out if an integer is prime or composite.")
        print("2. Print the list of prime integers up to a positive integer.")
        print("3. Exit.")

        option_input = input("\nSelection: ").strip()

        # handle exit immediately
        if option_input == "3":
            print("Exiting program.")
            break

        # check input: 3 options, flag 1 for single or multiple primes
        if not input_checker(option_input, 3, 1):
            print("\nInvalid option input, make a valid selection.\n")
            continue
        
        target_input = input("\nEnter a target positive integer (n): ")

        if not input_checker(target_input, 3, 0):
            print("\nInvalid target input value, returning to main menu...\n")
            continue

        test_input = select_test()

        if not test_input:
            continue
        else:
            n = int(target_input)
            init_primecalculator(option_input, target_input, test_input)


def input_checker(user_input, input_range, flag):
    # check non-digit condition to prevent crashing
    if not user_input.isdigit():
        return False

    if flag:
        # compare the integer against the numeric range
        return 1 <= int(user_input) <= input_range
    else:
        return True


def select_test():
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
        return False

    # check input: 3 options, flag 1 for single or multiple primes
    if not input_checker(test_input, 9, 1):
        print("\nInvalid test selection input, returning to main menu...\n")
        return 0

    return test_input


def init_primecalculator(isRange, n, test_type):
    print(f"Inputs received: Detect primality of N: {isRange} | Target Number: {n} | Type of the Test: {test_type}")
    return 0


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
