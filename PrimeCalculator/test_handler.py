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
    # helper names must not start with "handle_", main.py exposes those as menu options

    def _report(self, name, n, compute):
        """ times the computation only (not the printing), then prints the primes and a summary """
        if n < 2: # no primes below 2, also keeps the sieves away from inputs they mishandle
            print(f"There are no primes up to {n}.")
            return

        start = time.perf_counter()
        primes = compute()
        elapsed = time.perf_counter() - start

        print(primes)
        print(f"\n{name}: {len(primes)} primes up to {n} in {elapsed:.4f} s")

    def _primes_by_test(self, test, n):
        """ builds the list by applying a single-number primality test to every candidate up to n """
        return [k for k in range(2, n + 1) if test(k)]

    def handle_1(self, n): # ERATOSTHENES
        self._report("Sieve of Eratosthenes", n, lambda: sieve_of_eratosthenes(n))

    def handle_2(self, n): # SUNDARAM
        self._report("Sieve of Sundaram", n, lambda: sieve_of_sundaram(n))

    def handle_3(self, n): # ATKIN
        self._report("Sieve of Atkin", n, lambda: sieve_of_atkin(n))

    def handle_4(self, n): # TRIAL DIVISION
        self._report("Trial Division", n, lambda: self._primes_by_test(trial_division_test, n))

    def handle_5(self, n): # AKS
        print(aks_test(n))

    def handle_6(self, n): #LUCAS-LEHMER
        print(lucas_lehmer_test(n))

    def handle_7(self, n): # FERMAT
        self._report("Fermat", n, lambda: self._primes_by_test(fermat_test, n))

    def handle_8(self, n): # MILLER-RABIN
        self._report("Miller-Rabin", n, lambda: self._primes_by_test(miller_rabin_test, n))

    def handle_9(self, n): #BAILLIE-PSW
        self._report("Baillie-PSW", n, lambda: self._primes_by_test(baillie_psw_test, n))
