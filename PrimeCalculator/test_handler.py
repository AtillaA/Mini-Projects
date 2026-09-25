from sieve import sieve_of_eratosthenes, sieve_of_sundaram, sieve_of_atkin
from deterministic import trial_division_test, aks_test, lucas_lehmer_test
from probabilistic import fermat_test, miller_rabin_test, baillie_psw_test



# INCOMPLETE: ADD FUNCTIONALITY FOR DETERMINING THE OUTPUT BASED ON THE OPTION
class TestHandlers:
    def handle_1(self, option, n): # ERATOSTHENES
        sieve_of_eratosthenes(n)

    def handle_2(self, option, n): # SUNDARAM
        sieve_of_sundaram(n)

    def handle_3(self, option, n): # ATKIN
        sieve_of_atkin(n)

    def handle_4(self, option, n): # TRIAL DIVISION
        print(trial_division_test(n))

    def handle_5(self, option, n): # AKS
        aks_test(n)

    def handle_6(self, option, n): #LUCAS-LEHMER
        lucas_lehmer_test(n)

    def handle_7(self, option, n): # FERMAT
        fermat_test(n)

    def handle_8(self, option, n): # MILLER-RABIN
        miller_rabin_test(n)

    def handle_9(self, option, n): #BAILLIE-PSW
        baillie_psw_test(n)
