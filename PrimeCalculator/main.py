from test_handler import TestHandlers
import subprocess
import time
import os



def clear_screen():
    """ wipes the console screen """
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True)


def pause_and_clear(seconds=1.5):
    """ pauses execution then clears the console screen """
    time.sleep(seconds)
    clear_screen()


def select_test(option, n):
    while True:
        test_text = """
Select the primality test method you wish to use (note that Lucas-Lehmer test will only yield Mersenne primes):

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
        
        handlers = TestHandlers()
        selected_test_method = input("Selection (0-9): ").strip()

        # exit early
        if selected_test_method == "0":
            print("Returning to main menu...")
            pause_and_clear()
            break
        
        # construct the target method name dynamically
        method_name = f"handle_{selected_test_method}"
        
        # look up the method on the class instance
        func = getattr(handlers, method_name, None)
        
        if func:
            func(int(option), int(n))
            break
        else:
            print("Invalid Selection.")
            pause_and_clear()


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

        # 1 or 2
        selected_option = input("Selection: ").strip()

        # handle exit immediately
        if selected_option == "3":
            print("Exiting program.")
            break
        
        target_value = input("\nEnter the target value: ").strip()

        # check if the inputs are numbers
        if not (selected_option.isdigit() and target_value.isdigit()):
            print("\nInvalid input, make a valid selection.")
            pause_and_clear()
            continue

        # check if the selection is valid
        if int(selected_option) == 1 or int(selected_option) == 2:
            select_test(selected_option, target_value)
        else:
            print("\nSelection does not exist. Try again.")
            pause_and_clear()

    return 0


if __name__ == "__main__":
    main()
