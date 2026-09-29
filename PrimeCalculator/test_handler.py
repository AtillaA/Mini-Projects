from sieve import sieve_of_eratosthenes, sieve_of_sundaram, sieve_of_atkin
from deterministic import trial_division_test, aks_test, lucas_lehmer_test
from probabilistic import fermat_test, miller_rabin_test, baillie_psw_test
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


class TestHandlers:
    def handle_1(self, n): # ERATOSTHENES
        print(sieve_of_eratosthenes(n))

    def handle_2(self, n): # SUNDARAM
        print(sieve_of_sundaram(n))

    def handle_3(self, n): # ATKIN
        print(sieve_of_atkin(n))

    def handle_4(self, n): # TRIAL DIVISION
        print(trial_division_test(n))       
        # self.run(PrimalityTest(trial_division_test), n)
        # return [k for k in range(2, n + 1) if self.func(k)]

    def handle_5(self, n): # AKS
        print(aks_test(n))

    def handle_6(self, n): #LUCAS-LEHMER
        print(lucas_lehmer_test(n))

    def handle_7(self, n): # FERMAT
        print(fermat_test(n))

    def handle_8(self, n): # MILLER-RABIN
        print(miller_rabin_test(n))

    def handle_9(self, n): #BAILLIE-PSW
        print(baillie_psw_test(n))
