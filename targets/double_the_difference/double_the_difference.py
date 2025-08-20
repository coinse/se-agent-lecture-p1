
def double_the_difference(lst):
    '''
    Given a list of numbers, return the sum of squares of the numbers
    in the list that are odd. Ignore numbers that are negative or not integers.
   
    If the input list is empty, return 0.
    '''
    return sum([i**2 for i in lst if i > 0 and i%2!=0 and "." not in str(i)])
