from sieve import sieve_of_eratosthenes, sieve_of_sundaram, sieve_of_atkin
from deterministic import trial_division_test, aks_test, lucas_lehmer_test
from probabilistic import fermat_test, miller_rabin_test, baillie_psw_test


class TestHandlers:
    def handle_0(self): print("0")
    def handle_1(self): print("1")
    def handle_2(self): print("2")
    def handle_3(self): print("3")
    def handle_4(self): print("4")
    def handle_5(self): print("5")
    def handle_6(self): print("6")
    def handle_7(self): print("7")
    def handle_8(self): print("8")
    def handle_9(self): print("9")


def select_test(option, n):
    while True:

        test_text = """
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
        print(test_text)
        
        handlers = MenuHandlers()
        selected_test_method = input("Selection (0-9): ").strip()
        
        # construct the target method name dynamically
        method_name = f"handle_{selected_test_method}"
        
        # look up the method on the class instance
        func = getattr(handlers, method_name, None)
        
        if func:
            func()
            break
        else:
            print("Invalid Selection.")


def main():
    menu_text = """
#############################
## PRIME NUMBER CALCULATOR ##
#############################
Welcome. Capabilities of this program are listed below:
"""
    print(menu_text)

    while True:
        menu_text = """
1. Find out if an integer is prime or composite.
2. Print the list of prime integers up to a positive integer.
3. Exit.
"""
        print(menu_text)

        selected_option = input("Selection: ").strip()

        # handle exit immediately
        if selected_option == "3":
            print("Exiting program.")
            break
        
        target_value = input("\nEnter the target value: ").strip()

        if not (selected_option.isdigit() and target_value.isdigit()):
            print("\nInvalid input, make a valid selection.")
            continue

        if int(selected_option) == 1 or int(selected_option) == 2:
            select_test(selected_option, target_value)
        else:
            print("\nSelection does not exist. Try again.")

    return 0


if __name__ == "__main__":
    main()
