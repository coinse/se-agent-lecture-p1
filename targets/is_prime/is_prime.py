

def is_prime(n):
    """Return true if a given number is prime, and false otherwise.
    """
    if n < 2:
        return False
    for k in range(2, n - 1):
        if n % k == 0:
            return False
    return True
