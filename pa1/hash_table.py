'''
CAPP 30122 W'21: Markov models and hash tables

YOUR NAME HERE
'''


TOO_FULL = 0.5
GROWTH_RATIO = 2


class Hashtable:

    def __init__(self, cells, defval):
        '''
        Construct a new hash table with a fixed number of cells equal to the
        parameter "cells", and which yields the value defval upon a lookup to a
        key that has not previously been inserted
        '''
        ### YOUR CODE HERE ###
        pass

    def __getitem__(self, key):
        '''
        Similiar to the __getitem__ method for a Python dictionary, this function
        retrieves the value associated with the specified key in the hash table,
        or return the default value if it has not previously been inserted.
        '''
        ### YOUR CODE HERE ###
        pass

    def __setitem__(self, key, value):
        '''
        Similiar to the __setitem__ method for a Python dictionary, this function
        will change the value associated with key "key" to value "val".
        If "key" is not currently present in the hash table, insert it with
        value "val".
        '''
        ### YOUR CODE HERE ###
        pass

    def __delitem__(self, key):
        '''
        Similiar to the __delitem__ method for a Python dictionary, this will
        "remove" the key-value pairing inside the hash table. Remember this function
        will not actually remove the key-value pairing from the table but "mark" for
        removal during a rehashing.

        If the key is not found inside the table. Then you must raise the following
        error:
             raise RuntimeError("Key was not found in table")
        '''
        ### YOUR CODE HERE ###
        pass

    def __contains__(self, key):
        '''
        Similiar to the __contains__ method for a Python dictionary, this will
        return true if the key is inside the hash table; otherwise, if not
        then return false.
        '''
        ### YOUR CODE HERE ###
        return True

    def keys(self):
        '''
        Returns a list with all the keys inside the hashtable.
        '''
        ### YOUR CODE HERE ###
        pass

    def values(self):
        '''
        Returns a list with all the values inside the map.
        '''
        ### YOUR CODE HERE ###
        pass

    def __len__(self):
        '''
           Returns the number key-value pairings inside the hashtable.
        '''
        ### YOUR CODE HERE ###
        pass
