from test_handler import TestHandlers
import subprocess
import time
import os



def clear_screen():
    """ wipes the console screen """
    command = 'cls' if os.name == 'nt' else 'clear'
    subprocess.run(command, shell=True)


def pause_and_clear(seconds=1):
    """ pauses execution then clears the console screen """
    time.sleep(seconds)
    clear_screen()


def select_test(n):
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
        print("\n")

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
            func(int(n))
            break
        else:
            print("Invalid Selection.")
            pause_and_clear()


def main():
    menu_text = """
#############################
## PRIME NUMBER CALCULATOR ##
#############################
Welcome. This program prints the prime numbers up the input provided.
The user must provide a target positive integer, and the method that they wish to use.
Note that Lucas-Lehmer Primality Test will only yield the Mersenne Primes, so evaluate the output accordingly.
Input 0 to exit the program.
"""
    print(menu_text)

    while True:
        target_value = input("\nEnter the target value: ").strip()

        # handle exit immediately
        if target_value == "0":
            print("Exiting program.")
            break

        # check the input
        if not (target_value.isdigit()):
            print("\nInvalid input. Try again.")
            pause_and_clear()
            continue

        pause_and_clear()
        select_test(target_value)

    return 0


if __name__ == "__main__":
    main()
