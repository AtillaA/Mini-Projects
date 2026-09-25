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


def input_checker(user_input, n, isRange):
    # check non-digit condition to prevent crashing
    if not user_input.isdigit():
        return False

    if isRange:
        # compare the integer against the numeric range
        return 1 <= int(user_input) <= n
    else:
        return True


def select_test():
    menu_text = """
    Select the primality test method you wish to use (note that Lucas-Lehmer test will only yield Mersenne prime(s)):

    Sieves:
    -------
    1. Sieve of Eratosthenes
    2. Sieve of Sundaram
    3. Sieve of Atkin

    Deterministic Tests:
    ----------------------
    4. Trial Division
    5. Agrawal–Kayal–Saxena
    6. Lucas-Lehmer

    Probabilistic Tests:
    ----------------------
    7. Fermat
    8. Miller-Rabin
    9. Baillie-PSW

    0. Back
    """
    print(menu_text)
    
    test_input = input("Selection: ").strip()

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
    print(f"Inputs received: Detect primality of N: {bool(int(isRange) - 1)} | Target Number: {n} | Type of the Test: {test_type}")
    return 0


if __name__ == "__main__":
    main()
