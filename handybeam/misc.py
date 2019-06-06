"""
file :code:`misc.py`, module :py:mod:`handybeam.misc`

Functions and helpers that would not fit anywhere else.

Some of them might be awaiting refactoring or deletion.

"""


def copy_docstring(from_function, separator="\n", prepend=True):


    '''
    ---------------------------------------------
    copy_docstring(from_function,separator,prepend)
    ---------------------------------------------
            
    DESCRIPTION HERE

    Parameters
    ----------

    from_function : DESCRIPTION HERE
            DESCRIPTION HERE
    separator : DESCRIPTION HERE
            DESCRIPTION HERE
    prepend : DESCRIPTION HERE
            DESCRIPTION HERE
    
    '''



    """
    Decorator. Copies the docstring of `from_function` into the decorated function.

    This is used to make the documentation of the overriding methods nicer: enables to join the documentation of the super class and the current class in a single place.

    if :code:`prepend` is true, the current(local) function's goes first. Otherwise, the :code:`from_function`'s docstring goes first.

    Modified and extended from `https://stackoverflow.com/questions/13741998 <https://stackoverflow.com/questions/13741998/is-there-a-way-to-let-classes-inherit-the-documentation-of-their-superclass-with>`_
    """


    def _decorator(func):

        '''
        ---------------------------------------------
        _decorator(func)
        ---------------------------------------------
                
        DESCRIPTION HERE

        Parameters
        ----------

        func : DESCRIPTION HERE
                DESCRIPTION HERE
        
        '''

        
        """ creates a new, modified function, to be returned instead of the original.

        Combines the docstrings of two functions: the decorated, and the one from  'from_function'
        """
        
        source_doc = from_function.__doc__

        if func.__doc__ is None:  # if there is no docstring at the local function
            func.__doc__ = source_doc
        else:  # if there is, connect the two
            if prepend:
                func.__doc__ = separator.join([func.__doc__, source_doc])
            else:
                func.__doc__ = separator.join([source_doc, func.__doc__, ])

        return func
    return _decorator
