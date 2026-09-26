from sieve import sieve_of_eratosthenes, sieve_of_sundaram, sieve_of_atkin
from deterministic import trial_division_test, aks_test, lucas_lehmer_test
from probabilistic import fermat_test, miller_rabin_test, baillie_psw_test



class Sieve:
    """ natively lists primes up to n, derives the single-number check """
    def __init__(self, func):
        self.func = func

    def is_prime(self, n):
        return n in self.func(n)

    def primes_up_to(self, n):
        return self.func(n)


class PrimalityTest:
    """ natively checks one number, derives the list """
    def __init__(self, func):
        self.func = func

    def is_prime(self, n):
        return self.func(n)

    def primes_up_to(self, n):
        return [k for k in range(2, n + 1) if self.func(k)]


class TestHandlers:
    def run(self, method, option, n):
        """ the only place that checks the option """
        if n < 2:  # nothing below 2 is prime, regardless of the method
            result = False if option == 1 else []
        elif option == 1:
            result = method.is_prime(n)
        else:
            result = method.primes_up_to(n)
        print(result)

    def handle_1(self, option, n): # ERATOSTHENES
        self.run(Sieve(sieve_of_eratosthenes), option, n)

    def handle_2(self, option, n): # SUNDARAM
        print(sieve_of_sundaram(n))

    def handle_3(self, option, n): # ATKIN
        print(sieve_of_atkin(n))

    def handle_4(self, option, n): # TRIAL DIVISION
        self.run(PrimalityTest(trial_division_test), option, n)

    def handle_5(self, option, n): # AKS
        print(aks_test(n))

    def handle_6(self, option, n): #LUCAS-LEHMER
        print(lucas_lehmer_test(n))

    def handle_7(self, option, n): # FERMAT
        print(fermat_test(n))

    def handle_8(self, option, n): # MILLER-RABIN
        print(miller_rabin_test(n))

    def handle_9(self, option, n): #BAILLIE-PSW
        print(baillie_psw_test(n))
